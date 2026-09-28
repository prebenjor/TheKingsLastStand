"""Install the current development build in the dedicated Warcraft III test folder."""
from pathlib import Path
import hashlib
import json
import shutil
import datetime

ROOT = Path(__file__).resolve().parents[1]


def _sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _find_archived_copy(archive_root, filename, expected_hash):
    if not archive_root.exists():
        return None
    for candidate in sorted(archive_root.rglob(filename)):
        if candidate.is_file() and _sha256(candidate) == expected_hash:
            return candidate
    return None


def _restore_missing_maps(previous_maps, archive_paths, expected_hashes):
    errors = []
    for previous in reversed(previous_maps):
        backup = archive_paths.get(previous)
        if previous.exists() or backup is None:
            continue
        try:
            shutil.copy2(backup, previous)
            if _sha256(previous) != expected_hashes[previous]:
                raise OSError('Restored map differs from archived copy: '+str(previous))
        except OSError as error:
            errors.append(error)
    return errors


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
    backup_root = ROOT/'backups'/'installed-diagnostics'
    archive = None
    archive_paths = {}
    old_hashes = {}
    for previous in obsolete:
        old_hash = _sha256(previous)
        old_hashes[previous] = old_hash
        archived = _find_archived_copy(backup_root, previous.name, old_hash)
        if archived is not None:
            archive_paths[previous] = archived
            continue
        if archive is None:
            stamp = datetime.datetime.now(datetime.timezone.utc).strftime('%Y%m%dT%H%M%S%fZ')
            archive = backup_root/(stamp+'-'+manifest['build_id'])
            archive.mkdir(parents=True, exist_ok=False)
        destination = archive/previous.name
        if destination.exists():
            raise ValueError('Refusing to overwrite archived development map: '+str(destination))
        try:
            shutil.copy2(previous, destination)
            if _sha256(destination) != old_hash:
                raise OSError('Archive copy differs from the old map: '+str(previous))
        except OSError as error:
            if destination.exists():
                try:
                    destination.unlink()
                except OSError:
                    pass
            if archive.exists() and not any(archive.iterdir()):
                try:
                    archive.rmdir()
                except OSError:
                    pass
            raise ValueError(
                'Could not create and verify an archive copy. No old map was removed and the current build '
                'was not installed: '+str(error)
            ) from error
        archive_paths[previous] = destination

    try:
        for previous in obsolete:
            previous.unlink()
    except OSError as error:
        recovery_errors = _restore_missing_maps(obsolete, archive_paths, old_hashes)
        archive_paths_used = sorted({str(path.parent) for path in archive_paths.values()})
        archive_note = ' Archived copies are retained in '+', '.join(archive_paths_used)+'.' if archive_paths_used else ''
        recovery_note = ' Recovery also reported: '+str(recovery_errors[0]) if recovery_errors else ''
        raise ValueError(
            'A previous The Kings Last Stand map is open or locked. The current build was not installed. '
            'Close Warcraft III and rerun the installer.'+archive_note+recovery_note
        ) from error

    installed_by_this_call = not target.exists()
    try:
        if installed_by_this_call:
            shutil.copy2(source, target)
        if _sha256(target) != source_hash:
            raise OSError('Installed map differs from build: '+str(target))
    except OSError as error:
        cleanup_errors = []
        if installed_by_this_call and target.exists():
            try:
                target.unlink()
            except OSError as cleanup_error:
                cleanup_errors.append(cleanup_error)
        cleanup_errors.extend(_restore_missing_maps(obsolete, archive_paths, old_hashes))
        archive_paths_used = sorted({str(path.parent) for path in archive_paths.values()})
        archive_note = ' Archived copies are retained in '+', '.join(archive_paths_used)+'.' if archive_paths_used else ''
        cleanup_note = ' Recovery also reported: '+str(cleanup_errors[0]) if cleanup_errors else ''
        raise ValueError(
            'Could not install the verified current build. Previous maps were restored when possible.'
            +archive_note+cleanup_note
        ) from error
    manifest['installed_test_map_path'] = str(target)
    if persist_manifest:
        (ROOT/'build/diagnostic-manifest.json').write_text(json.dumps(manifest,indent=2))
    for archive_path in sorted({path.parent for path in archive_paths.values()}):
        print('Archived older diagnostic maps:',archive_path)
    print('Installed development test map:',target)
    return target


def _is_project_development_map(name):
    return (
        name == 'DIAGNOSTIC-TheKingsLastStand.w3m'
        or name.startswith('DIAGNOSTIC-KLS-D-')
        or (name.startswith('KLS-D-') and name.endswith('-Development.w3m'))
    )
