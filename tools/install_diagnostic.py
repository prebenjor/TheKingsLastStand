"""Install the verified diagnostic artifact in Warcraft III's Custom Game folder."""
from pathlib import Path
import hashlib
import json
import shutil
import datetime

ROOT = Path(__file__).resolve().parents[1]


def install(manifest, maps_root=None):
    source = Path(manifest['output_path'])
    persist_manifest = maps_root is None
    if maps_root is None:
        maps_root = Path.home()/'Documents/Warcraft III/Maps/TheKingsLastStand'
    else:
        maps_root = Path(maps_root)
    target = maps_root/('DIAGNOSTIC-'+manifest['build_id']+'.w3m')
    data = source.read_bytes()
    source_hash = hashlib.sha256(data).hexdigest()
    if source_hash != manifest['sha256']:
        raise ValueError('Diagnostic map changed since verification; rebuild before installing.')
    target.parent.mkdir(parents=True, exist_ok=True)
    if target.exists():
        if hashlib.sha256(target.read_bytes()).hexdigest() != source_hash:
            raise ValueError('Build-specific installed map exists with different content: '+str(target))
    else:
        shutil.copy2(source,target)
    if hashlib.sha256(target.read_bytes()).hexdigest() != source_hash:
        raise ValueError('Installed map differs from build')
    # Warcraft's Custom Game list also contains any older diagnostic files in
    # this folder. Move only this project's known naming patterns to a
    # recoverable workspace backup so an old unversioned map cannot be picked
    # accidentally.
    obsolete = sorted(
        path for path in maps_root.glob('DIAGNOSTIC-*.w3m')
        if path != target and (
            path.name == 'DIAGNOSTIC-TheKingsLastStand.w3m'
            or path.name.startswith('DIAGNOSTIC-KLS-D-')
        )
    )
    if obsolete:
        stamp = datetime.datetime.now(datetime.timezone.utc).strftime('%Y%m%dT%H%M%S%fZ')
        archive = ROOT/'backups'/'installed-diagnostics'/(stamp+'-'+manifest['build_id'])
        archive.mkdir(parents=True, exist_ok=False)
        for previous in obsolete:
            destination = archive/previous.name
            if destination.exists():
                raise ValueError('Refusing to overwrite archived diagnostic map: '+str(destination))
            shutil.move(str(previous), str(destination))
        print('Archived older diagnostic maps:',archive)
    manifest['installed_diagnostic_path'] = str(target)
    if persist_manifest:
        (ROOT/'build/diagnostic-manifest.json').write_text(json.dumps(manifest,indent=2))
    print('Custom Game map:',target)
    return target
