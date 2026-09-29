"""Capture and validate World Editor authored terrain/art as a build input."""
from hashlib import sha256
from io import BytesIO
import json
import re
import struct
import tempfile
from pathlib import Path
import zipfile

from archive_pack import MPQArchive, member


FORMAT_VERSION = 1
MAP_CELLS = 192
MAP_EDGE = 12288.0
PATHING_PIXELS = MAP_CELLS * 4
TERRAIN_HEADER_SIZE = 69
AUTHORED_MEMBERS = (
    'war3map.w3e',
    'war3map.wpm',
    'war3map.doo',
    'war3map.shd',
    'war3map.mmp',
    'war3mapMap.blp',
)
MANIFEST_NAME = 'manifest.json'
BUILD_ID_RE = re.compile(r'^KLS-D-[A-Za-z0-9]{4,}$')
SHA256_RE = re.compile(r'^[0-9a-f]{64}$')


def _validate_build_id(build_id):
    if not isinstance(build_id, str) or not BUILD_ID_RE.fullmatch(build_id):
        raise ValueError('Expected a complete KLS-D build ID.')


def _validate_w3e(data):
    if len(data) < TERRAIN_HEADER_SIZE or data[:4] != b'W3E!':
        raise ValueError('Authored terrain is not a Warcraft W3E file.')
    version, = struct.unpack_from('<I', data, 4)
    width, height = struct.unpack_from('<II', data, 53)
    x, y = struct.unpack_from('<ff', data, 61)
    expected_size = TERRAIN_HEADER_SIZE + (MAP_CELLS + 1) ** 2 * 8
    if version != 12 or (width, height) != (MAP_CELLS + 1, MAP_CELLS + 1):
        raise ValueError('Authored terrain must be version 12 at 192 by 192 cells.')
    if len(data) != expected_size:
        raise ValueError('Authored terrain data length does not match its vertex dimensions.')
    if abs(x + MAP_EDGE) > 0.01 or abs(y + MAP_EDGE) > 0.01:
        raise ValueError('Authored terrain origin does not match the approved map bounds.')


def _validate_wpm(data):
    if len(data) < 16:
        raise ValueError('Authored pathing file is shorter than its header.')
    magic, version, width, height = struct.unpack_from('<4sIII', data)
    expected_size = 16 + PATHING_PIXELS * PATHING_PIXELS
    if magic != b'MP3W' or version != 0 or (width, height) != (PATHING_PIXELS, PATHING_PIXELS):
        raise ValueError('Authored pathing must match the 192-cell Warcraft map extent.')
    if len(data) != expected_size:
        raise ValueError('Authored pathing data length does not match its dimensions.')


def _validate_doo(data):
    if len(data) < 16 or data[:4] != b'W3do':
        raise ValueError('Authored doodad layer is not a Warcraft W3do file.')
    version, subversion = struct.unpack_from('<II', data, 4)
    if (version, subversion) != (13, 11):
        raise ValueError('Authored doodad layer must use the installed editor format 13.11.')


def validate_authored_members(members):
    if not isinstance(members, dict) or set(members) != set(AUTHORED_MEMBERS):
        raise ValueError('Authored map layer must contain every required terrain/art member.')
    for name, data in members.items():
        if not isinstance(data, bytes):
            raise ValueError('Authored map member must be binary: ' + name)
    _validate_w3e(members['war3map.w3e'])
    _validate_wpm(members['war3map.wpm'])
    _validate_doo(members['war3map.doo'])
    if len(members['war3map.shd']) != PATHING_PIXELS * PATHING_PIXELS:
        raise ValueError('Authored shadow layer does not match the 192-cell map extent.')
    if not 4 <= len(members['war3map.mmp']) <= 16 * 1024 * 1024:
        raise ValueError('Authored minimap marker layer has an invalid size.')
    if not 16 <= len(members['war3mapMap.blp']) <= 32 * 1024 * 1024:
        raise ValueError('Authored map preview has an invalid size.')
    if members['war3mapMap.blp'][:4] not in (b'BLP1', b'BLP2'):
        raise ValueError('Authored map preview is not a BLP image.')


def _build_identity(w3i):
    if len(w3i) <= 28:
        raise ValueError('Map metadata is too short to contain its build identity.')
    end = w3i.find(b'\0', 28)
    if end < 0:
        raise ValueError('Map metadata is missing its scenario name terminator.')
    try:
        title = w3i[28:end].decode('ascii')
    except UnicodeDecodeError as error:
        raise ValueError('Map metadata build identity is not ASCII.') from error
    prefix = 'KLS DEVELOPMENT '
    if not title.startswith(prefix):
        raise ValueError('Map metadata does not identify a KLS development build.')
    build_id = title[len(prefix):]
    _validate_build_id(build_id)
    return build_id


def _member_metadata(members):
    return {
        name: {'size': len(members[name]), 'sha256': sha256(members[name]).hexdigest()}
        for name in AUTHORED_MEMBERS
    }


def read_authored_layer(layer_path):
    """Return (capture metadata, validated MPQ-member bytes) from the bundle."""
    layer_path = Path(layer_path)
    try:
        with zipfile.ZipFile(layer_path, 'r') as archive:
            names = archive.namelist()
            expected_names = set(AUTHORED_MEMBERS) | {MANIFEST_NAME}
            if len(names) != len(expected_names) or set(names) != expected_names:
                raise ValueError('Authored layer archive has missing, duplicate, or unexpected members.')
            bad_member = archive.testzip()
            if bad_member is not None:
                raise ValueError('Authored layer archive failed its ZIP checksum: ' + bad_member)
            metadata = json.loads(archive.read(MANIFEST_NAME).decode('utf-8'))
            members = {name: archive.read(name) for name in AUTHORED_MEMBERS}
    except (OSError, zipfile.BadZipFile, KeyError, json.JSONDecodeError) as error:
        raise ValueError('Could not read authored map layer bundle: ' + str(error)) from error

    if metadata.get('format_version') != FORMAT_VERSION:
        raise ValueError('Unsupported authored map layer format version.')
    _validate_build_id(metadata.get('source_build_id'))
    source_hash = metadata.get('source_map_sha256')
    if not isinstance(source_hash, str) or not SHA256_RE.fullmatch(source_hash):
        raise ValueError('Authored map layer has invalid source-map provenance.')
    expected_members = metadata.get('members')
    if not isinstance(expected_members, dict) or set(expected_members) != set(AUTHORED_MEMBERS):
        raise ValueError('Authored map layer manifest does not list the required members.')
    for name in AUTHORED_MEMBERS:
        entry = expected_members[name]
        if (not isinstance(entry, dict)
                or entry.get('size') != len(members[name])
                or entry.get('sha256') != sha256(members[name]).hexdigest()):
            raise ValueError('Authored map layer checksum or size mismatch: ' + name)
    validate_authored_members(members)
    return metadata, members


def write_authored_layer(members, source_build_id, source_map_sha256, layer_path):
    """Write one deterministic, checksummed authoring bundle atomically."""
    _validate_build_id(source_build_id)
    if not isinstance(source_map_sha256, str) or not SHA256_RE.fullmatch(source_map_sha256):
        raise ValueError('Source map SHA-256 must be 64 lowercase hexadecimal characters.')
    validate_authored_members(members)
    metadata = {
        'format_version': FORMAT_VERSION,
        'source_build_id': source_build_id,
        'source_map_sha256': source_map_sha256,
        'members': _member_metadata(members),
    }
    manifest = (json.dumps(metadata, sort_keys=True, separators=(',', ':')) + '\n').encode('utf-8')
    layer_path = Path(layer_path)
    layer_path.parent.mkdir(parents=True, exist_ok=True)
    tmp_path = None
    try:
        with tempfile.NamedTemporaryFile(prefix=layer_path.name + '.', suffix='.tmp',
                                         dir=layer_path.parent, delete=False) as stream:
            tmp_path = Path(stream.name)
        with zipfile.ZipFile(tmp_path, 'w', compression=zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
            for name in (MANIFEST_NAME,) + AUTHORED_MEMBERS:
                info = zipfile.ZipInfo(name, date_time=(1980, 1, 1, 0, 0, 0))
                info.compress_type = zipfile.ZIP_DEFLATED
                info.external_attr = 0o600 << 16
                archive.writestr(info, manifest if name == MANIFEST_NAME else members[name], compress_type=zipfile.ZIP_DEFLATED, compresslevel=9)
        read_authored_layer(tmp_path)
        if layer_path.exists() and layer_path.read_bytes() == tmp_path.read_bytes():
            tmp_path.unlink()
        else:
            tmp_path.replace(layer_path)
    finally:
        if tmp_path is not None and tmp_path.exists():
            tmp_path.unlink()
    return metadata


def capture_authored_map(map_path, expected_build_id, layer_path):
    """Extract a matching saved KLS map's art layers, not its game logic."""
    _validate_build_id(expected_build_id)
    map_path = Path(map_path)
    if not map_path.is_file():
        raise ValueError('Saved World Editor map does not exist: ' + str(map_path))
    archive = MPQArchive(map_path, listfile=False)
    try:
        w3i = member(archive, 'war3map.w3i')
        found_build_id = _build_identity(w3i)
        if found_build_id != expected_build_id:
            raise ValueError('Saved map build ID does not match the current build ID: expected '
                             + expected_build_id + ', found ' + found_build_id)
        members = {name: member(archive, name) for name in AUTHORED_MEMBERS}
    finally:
        archive.file.close()
    return write_authored_layer(members, expected_build_id,
                                sha256(map_path.read_bytes()).hexdigest(), layer_path)
