"""Prepare one terrain work copy with disposable native unit previews.

DE 13.11 fixed records match the user's World Editor save of 2026-09-30.
The classic fields are documented by mdx-m3-viewer's unitsdoo/unit.ts;
DE adds the skin flags and three reserved trailing integers. No optional
inventory/ability/drop tables are emitted. The runtime removes Neutral Extra
previews before spawning gameplay; unit placement data is never art-captured.
"""
import hashlib
import json
import math
import struct
from pathlib import Path
from archive_pack import MPQArchive, member, pack
from layout_catalog import editor_placements
from map_info import PLOTS

PREVIEW_OWNER = 26  # DE's 24 playable slots + neutral hostile/victim.
RECORD_SIZE = 131


def unit_record(rawcode, x, y, z, owner, number, variation=0, angle=None):
    raw = rawcode.encode('ascii')
    if len(raw) != 4:
        raise ValueError('Unit rawcode must contain four ASCII bytes')
    data = raw + struct.pack('<i7f', variation, x, y, z, math.radians(270) if angle is None else angle, 1, 1, 1)
    data += raw + struct.pack('<iBiHiii', -1, 2, owner, 0, -1, -1, -1)
    data += struct.pack('<iif7i', 0, 1000000 if rawcode == 'ngol' else 12500,
                        -1.0, 1, 0, 0, 0, 0, 0, 0)
    data += bytes((1, 0, 0, 0)) + struct.pack('<6i', -1, -1, number, 0, 0, 0)
    if len(data) != RECORD_SIZE:
        raise ValueError('Unexpected DE unit placement size')
    return data


def terrain_height(terrain, x, y):
    width, height = struct.unpack_from('<II', terrain, 53)
    ox, oy = struct.unpack_from('<ff', terrain, 61)
    vx, vy = (x - ox) / 128, (y - oy) / 128
    ix, iy = int(vx), int(vy)
    if not (0 <= ix < width - 1 and 0 <= iy < height - 1):
        raise ValueError('Editor reference lies outside terrain')
    def sample(px, py):
        offset = 69 + (py * width + px) * 8
        ground = struct.unpack_from('<H', terrain, offset)[0]
        cliff = terrain[offset + 7] & 15
        return (ground - 8192) / 4 + (cliff - 2) * 128
    fx, fy = vx - ix, vy - iy
    return ((1 - fx) * sample(ix, iy) + fx * sample(ix + 1, iy)) * (1 - fy) + \
           ((1 - fx) * sample(ix, iy + 1) + fx * sample(ix + 1, iy + 1)) * fy


def placement_data(terrain, previews=False):
    records = [unit_record('sloc', x, y, 0, i, i, variation=i)
               for i, (x, y) in enumerate(PLOTS)]
    if previews:
        for raw, x, y, _ in editor_placements():
            records.append(unit_record(raw, x, y, terrain_height(terrain, x, y),
                                       PREVIEW_OWNER, len(records)))
    return b'W3do' + struct.pack('<3I', 13, 11, len(records)) + b''.join(records)


def prepare_editor_copy(manifest):
    root = Path(__file__).resolve().parents[1]
    source = Path(manifest['output_path'])
    if hashlib.sha256(source.read_bytes()).hexdigest() != manifest['sha256']:
        raise ValueError('Current development package differs from its manifest')
    target = root / 'build' / (manifest['build_id'] + '-Development-Terrain.w3m')
    if target.exists():
        raise ValueError('Terrain work copy exists; preserve/capture it before preparing a new copy')
    archive = MPQArchive(source, listfile=False)
    try:
        terrain = member(archive, 'war3map.w3e')
        expected_art = {name: member(archive, name) for name in
                        ('war3map.w3e', 'war3map.wpm', 'war3map.doo', 'war3map.shd', 'war3map.mmp', 'war3mapMap.blp')}
    finally:
        archive.file.close()
    placements = placement_data(terrain, previews=True)
    pack(source, target, {'war3mapUnits.doo': placements})
    archive = MPQArchive(target, listfile=False)
    try:
        if member(archive, 'war3mapUnits.doo') != placements:
            raise ValueError('Editor placements differ from generated data')
        for name, data in expected_art.items():
            if member(archive, name) != data:
                raise ValueError('Preparing editor references changed captured art: ' + name)
    finally:
        archive.file.close()
    report = {'build_id': manifest['build_id'], 'path': str(target),
              'sha256': hashlib.sha256(target.read_bytes()).hexdigest(),
              'preview_owner': PREVIEW_OWNER, 'preview_count': len(editor_placements()),
              'art_readback': 'all six layers identical to development package',
              'editor_open': 'pending', 'placements': editor_placements()}
    (root / 'build' / 'editor-layout.json').write_text(json.dumps(report, indent=2), encoding='utf-8')
    print('Terrain work copy:', target)
    return report
