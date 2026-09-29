"""Capture World Editor terrain/art from a saved copy of the current map."""
import argparse
import hashlib
import json
from pathlib import Path

from authored_map import capture_authored_map


ROOT = Path(__file__).resolve().parents[1]


def capture(map_path=None):
    manifest_path = ROOT / 'dist/build-manifest.json'
    if not manifest_path.is_file():
        raise ValueError('Build the current development map before capturing editor art.')
    manifest = json.loads(manifest_path.read_text(encoding='utf-8'))
    build_id = manifest.get('build_id')
    relative_output = manifest.get('output_path')
    if not isinstance(relative_output, str):
        raise ValueError('Current build manifest has no output map path.')
    current_map = Path(relative_output)
    if not current_map.is_absolute():
        current_map = ROOT / current_map
    if map_path is None:
        map_path = current_map
        actual_sha = hashlib.sha256(map_path.read_bytes()).hexdigest()
        if actual_sha != manifest.get('sha256'):
            raise ValueError('Packaged map checksum differs from the current build manifest.')
    else:
        map_path = Path(map_path).resolve()

    destination = ROOT / 'source/authored-map/editor-layer.zip'
    metadata = capture_authored_map(map_path, build_id, destination)
    return destination, metadata


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--map', help='Saved current-build map with World Editor terrain/art edits')
    args = parser.parse_args(argv)
    try:
        destination, metadata = capture(args.map)
    except (OSError, ValueError, json.JSONDecodeError) as error:
        parser.error(str(error))
    print('Captured art from ' + metadata['source_build_id'])
    print('Source SHA-256: ' + metadata['source_map_sha256'])
    print('Saved: ' + str(destination))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
