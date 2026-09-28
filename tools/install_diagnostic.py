"""Install the current development build in the dedicated Warcraft III test folder."""
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
    target = maps_root/(manifest['build_id']+'-Development.w3m')
    data = source.read_bytes()
    source_hash = hashlib.sha256(data).hexdigest()
    if source_hash != manifest['sha256']:
        raise ValueError('Diagnostic map changed since verification; rebuild before installing.')
    target.parent.mkdir(parents=True, exist_ok=True)
    if target.exists() and hashlib.sha256(target.read_bytes()).hexdigest() != source_hash:
        raise ValueError('Build-specific installed map exists with different content: '+str(target))
    # Keep the dedicated project folder focused on the current map. Move only
    # known King's Last Stand names to a recoverable archive; preserve other maps.
    obsolete = sorted(
        path for path in maps_root.glob('*.w3m')
        if path != target and _is_project_development_map(path.name)
    )
    if obsolete:
        stamp = datetime.datetime.now(datetime.timezone.utc).strftime('%Y%m%dT%H%M%S%fZ')
        archive = ROOT/'backups'/'installed-diagnostics'/(stamp+'-'+manifest['build_id'])
        archive.mkdir(parents=True, exist_ok=False)
        moved = []
        try:
            for previous in obsolete:
                destination = archive/previous.name
                if destination.exists():
                    raise ValueError('Refusing to overwrite archived development map: '+str(destination))
                shutil.move(str(previous), str(destination))
                moved.append(previous)
        except OSError as error:
            rollback_errors = []
            for previous in reversed(moved):
                try:
                    shutil.move(str(archive/previous.name), str(previous))
                except OSError as rollback_error:
                    rollback_errors.append(rollback_error)
            if not rollback_errors:
                archive.rmdir()
            raise ValueError(
                'A previous The Kings Last Stand map is open or locked. Close Warcraft III and rerun; '
                'the installer stopped before copying this build.'
            ) from error
        print('Archived older diagnostic maps:',archive)
    if not target.exists():
        shutil.copy2(source,target)
    if hashlib.sha256(target.read_bytes()).hexdigest() != source_hash:
        raise ValueError('Installed map differs from build')
    manifest['installed_test_map_path'] = str(target)
    if persist_manifest:
        (ROOT/'build/diagnostic-manifest.json').write_text(json.dumps(manifest,indent=2))
    print('Installed development test map:',target)
    return target


def _is_project_development_map(name):
    return (
        name == 'DIAGNOSTIC-TheKingsLastStand.w3m'
        or name.startswith('DIAGNOSTIC-KLS-D-')
        or (name.startswith('KLS-D-') and name.endswith('-Development.w3m'))
    )
