"""Snapshot local engine logs with build provenance; does not prove the build was played."""
import datetime
import hashlib
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BUILD_ID_RE = re.compile(r'\bKLS-[A-Z0-9]-[A-Z0-9]{4,32}\b', re.I)
DIAGNOSTIC_LINE_RE = re.compile(
    r'\b(?:error|fatal|warn(?:ing)?|fail(?:ed|ure|ures)?|missing|not found|'
    r'exception|could not|cannot|unable to|can\'t)\b', re.I)
SPAWN_LOAD_CONTEXT_RE = re.compile(
    r'\b(?:spawn|createunit|createdestructable|create\s+(?:unit|destructable)|'
    r'model creation|load(?:ing)?|(?:unit|destructable)\s+(?:creation|spawn))\b', re.I)


def _diagnostic_severity(line):
    if re.search(r'\bfatal\b', line, re.I):
        return 'fatal'
    if re.search(r'\b(?:error|exception)\b', line, re.I):
        return 'error'
    if re.search(r'\bwarn(?:ing)?\b', line, re.I):
        return 'warning'
    return 'failure'

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
    findings = [f"Target build ID: {manifest['build_id']}"]
    build_references = []
    diagnostics = []
    for name in ('War3Log.txt', 'War3EditorLog.txt', 'selection.log'):
        path = folder / name
        if not path.exists():
            records.append({'file': name, 'status': 'missing'})
            continue
        data = path.read_bytes()
        (out / name).write_bytes(data)
        records.append({'file': name, 'bytes': len(data), 'modified_unix': path.stat().st_mtime,
                        'sha256': hashlib.sha256(data).hexdigest()})
        last_build_id = None
        for number, line in enumerate(data.decode('utf-8', errors='replace').splitlines(), 1):
            line_build_ids = BUILD_ID_RE.findall(line)
            for build_id in line_build_ids:
                build_references.append({'file': name, 'line': number,
                                         'build_id': build_id, 'text': line})
            if line_build_ids:
                last_build_id = line_build_ids[-1]
            if DIAGNOSTIC_LINE_RE.search(line):
                severity = _diagnostic_severity(line)
                kind = 'spawn_or_load' if SPAWN_LOAD_CONTEXT_RE.search(line) else 'engine_diagnostic'
                if last_build_id:
                    provenance = f'last build reference={last_build_id}; correlation only'
                else:
                    provenance = 'no preceding build reference'
                diagnostics.append({
                    'file': name, 'line': number, 'severity': severity, 'kind': kind,
                    'build_reference': last_build_id, 'provenance': provenance, 'text': line,
                })
                findings.append(f'{name}:{number} [{severity}/{kind}; {provenance}]: {line}')
            elif 'KingsLastStand' in line or 'KLS-' in line:
                if last_build_id:
                    provenance = f'last build reference={last_build_id}; correlation only'
                else:
                    provenance = 'no preceding build reference'
                findings.append(f'{name}:{number} [{provenance}]: {line}')
    current_build_references = [reference for reference in build_references
                                if reference['build_id'].casefold() == manifest['build_id'].casefold()]
    other_build_ids = sorted({reference['build_id'] for reference in build_references
                              if reference['build_id'].casefold() != manifest['build_id'].casefold()})
    if current_build_references:
        findings.insert(1, f"Current build {manifest['build_id']} is referenced in "
                        f"{len(current_build_references)} captured log line(s); references do not confirm gameplay.")
    else:
        findings.insert(1, f"No captured log references current build {manifest['build_id']}; "
                        "copied error lines cannot be attributed to the current build.")
    if other_build_ids:
        findings.insert(2, 'Other or older build IDs referenced: ' + ', '.join(other_build_ids))
    findings.insert(3, 'The last preceding build ID is a timing correlation only. '
                    'Map-open references and copied engine errors do not confirm gameplay or causality.')
    diagnostic_summary = {
        'error': sum(entry['severity'] == 'error' for entry in diagnostics),
        'fatal': sum(entry['severity'] == 'fatal' for entry in diagnostics),
        'warning': sum(entry['severity'] == 'warning' for entry in diagnostics),
        'failure': sum(entry['severity'] == 'failure' for entry in diagnostics),
        'spawn_or_load': sum(entry['kind'] == 'spawn_or_load' for entry in diagnostics),
        'total': len(diagnostics),
    }
    report = {'collected_utc': stamp, 'associated_build': manifest['build_id'],
              'played_build_confirmed': False, 'logs': records,
              'build_references': build_references,
              'current_build_references': current_build_references,
              'other_build_ids': other_build_ids,
              'diagnostics': diagnostics, 'diagnostic_summary': diagnostic_summary,
              'note': 'Copied logs can be stale or buffered. Build IDs and nearest preceding IDs are provenance hints only; map-opening entries may be menu scans and do not confirm gameplay. Confirm the visible in-game identifier. Engine warnings and explicit spawn/load failures are included here; map-script spawn diagnostics are also available in-game through -diag.'}
    (out / 'collection.json').write_text(json.dumps(report, indent=2))
    (out / 'findings.txt').write_text('\n'.join(findings), encoding='utf-8')
    print(out)

if __name__ == '__main__':
    collect()
