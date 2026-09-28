"""Modify only known fields in this editor's version 39 starter metadata."""
import struct

MAP_CELLS = 192
MAP_EDGE = MAP_CELLS * 64
PLOTS = [(-6000.0, -500.0), (-3300.0, -500.0), (3300.0, -500.0), (6000.0, -500.0)]
from town_catalog import TOWNS as TOWN_CATALOG
TOWNS = [(town['race'], town['x'], town['y']) for town in TOWN_CATALOG]


def four_player_info(data):
    if struct.unpack_from('<I', data)[0] != 39:
        raise ValueError('Expected the supplied version 39 editor baseline')
    if len(data) < 138:
        raise ValueError('Version 39 metadata is shorter than the validated starter layout.')
    data = bytearray(data)
    name = data.index(b'TRIGSTR_001\0')
    start = name - 20
    count = start - 4
    end = name + len(b'TRIGSTR_001\0')
    if struct.unpack_from('<I', data, count)[0] != 1:
        raise ValueError('Expected one baseline player')
    prefix = data[:count]
    players = bytearray(struct.pack('<I', 4))
    for i, (x, y) in enumerate(PLOTS):
        fixed = bytearray(data[start:name])
        struct.pack_into('<III', fixed, 0, i, 1, 1)
        players.extend(fixed)
        players.extend(('Defender ' + str(i+1)).encode() + b'\0')
        players.extend(struct.pack('<2f4I', x, y, 15 ^ (1 << i), 0, 0, 0))
    # One allied force, shared vision, no shared unit control.
    force = struct.pack('<III', 1, 3, 15) + b'Kingdom Defenders\0'
    old_force_name_end = data.index(b'\0', end + 24 + 12) + 1
    result = prefix + players + force + data[old_force_name_end:]
    # Four initial header strings; all newer DE fields remain in the suffix.
    pos = 28
    for _ in range(4):
        pos = result.index(b'\0', pos) + 1
    strings = b"The King's Last Stand\0Kingdom Defense\0Co-op defense against forty undead waves.\0" + b'2-4\0'
    header_shift = len(strings) - (pos - 28)
    result = bytearray(result[:28] + strings + result[pos:])
    playable_edge = MAP_EDGE - 6 * 128
    bounds = (-playable_edge, -playable_edge, playable_edge, playable_edge,
              -playable_edge, playable_edge, playable_edge, -playable_edge)
    struct.pack_into('<8f', result, 82 + header_shift, *bounds)
    struct.pack_into('<4I', result, 114 + header_shift, 6, 6, 6, 6)
    struct.pack_into('<2I', result, 130 + header_shift, MAP_CELLS - 12, MAP_CELLS - 12)
    return bytes(result)
