"""Snapshot local engine logs with build provenance; does not prove the build was played."""
import datetime
import hashlib
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def collect():
    manifest = json.loads((ROOT / 'build/diagnostic-manifest.json').read_text())
    output = Path(manifest.get('output_path', ''))
    if not output.is_file() or hashlib.sha256(output.read_bytes()).hexdigest() != manifest.get('sha256'):
        raise ValueError('Diagnostic manifest does not match the current build artifact; rebuild before collecting logs.')
    stamp = datetime.datetime.now(datetime.timezone.utc).strftime('%Y%m%dT%H%M%S%fZ')
    out = ROOT / 'test-results' / (stamp + '-' + manifest['build_id'])
    out.mkdir(parents=True)
    (out / 'build-manifest.json').write_text(json.dumps(manifest, indent=2))
    folder = Path.home() / 'Documents/Warcraft III/Logs'
    records = []
    findings = []
    for name in ('War3Log.txt', 'War3EditorLog.txt', 'selection.log'):
        path = folder / name
        if not path.exists():
            records.append({'file': name, 'status': 'missing'})
            continue
        data = path.read_bytes()
        (out / name).write_bytes(data)
        records.append({'file': name, 'bytes': len(data), 'modified_unix': path.stat().st_mtime,
                        'sha256': hashlib.sha256(data).hexdigest()})
        for number, line in enumerate(data.decode('utf-8', errors='replace').splitlines(), 1):
            if re.search(r'error|fail|missing|exception|KingsLastStand|KLS-', line, re.I):
                findings.append(f'{name}:{number}: {line}')
    report = {'collected_utc': stamp, 'associated_build': manifest['build_id'],
              'played_build_confirmed': False, 'logs': records,
              'note': 'Logs may be stale or buffered and map-opening entries may be menu scans. Confirm the in-game identifier. Spawn diagnostics are currently in-game only (-diag).'}
    (out / 'collection.json').write_text(json.dumps(report, indent=2))
    (out / 'findings.txt').write_text('\n'.join(findings), encoding='utf-8')
    print(out)

if __name__ == '__main__':
    collect()
