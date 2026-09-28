"""Build the enlarged grassland, road, player plots, gate approach and pathing."""
from collections import Counter
import struct
from town_catalog import TOWNS

MAP_CELLS = 192
TILE_UNITS = 128
W3E_HEADER_SIZE = 69


def _ground_palette(data):
    count = struct.unpack_from('<I', data, 13)[0]
    ids = [data[17 + i * 4:21 + i * 4].decode('ascii') for i in range(count)]
    required = {'Ldrt', 'Ldro', 'Ldrg', 'Lrok', 'Lgrs', 'Lgrd'}
    if not required.issubset(ids):
        raise ValueError('Starter terrain palette does not contain the expected Lordaeron ground tiles.')
    return {tile: ids.index(tile) for tile in required}


def _near_segment(x, y, x1, y1, x2, y2, radius):
    dx, dy = x2 - x1, y2 - y1
    length_sq = dx * dx + dy * dy
    if length_sq == 0:
        return (x - x1) ** 2 + (y - y1) ** 2 <= radius * radius
    t = max(0.0, min(1.0, ((x - x1) * dx + (y - y1) * dy) / length_sq))
    px, py = x1 + t * dx, y1 + t * dy
    return (x - px) ** 2 + (y - py) ** 2 <= radius * radius


def _paint(x, y, plots, tiles):
    # The central lane is visibly paved and remains clear from the south market
    # square to the northern gate and spawn approach.
    if abs(x) <= 448 and -10200 <= y <= 10200:
        return tiles['Lrok']
    if abs(x) <= 640 and -10200 <= y <= 10200:
        return tiles['Ldro']

    # A rocky gateway throat narrows at the open center lane.
    if 4800 <= y <= 5600 and abs(x) >= 1100:
        return tiles['Lrok']

    # Four distinct build plots are painted in one horizontal row. Stone
    # borders mark ownership without adding an impassable wall.
    for px, py in plots:
        dx, dy = abs(x - px), abs(y - py)
        if dx <= 1024 and dy <= 1024:
            if dx >= 896 or dy >= 896:
                return tiles['Lrok']
            return tiles['Lgrd']

    # Crownlands routes connect the four allied towns to the defended road.
    # The northern/southern towns use the existing north-south avenue. East
    # and west branches angle away from the four building plots and leave the
    # defense road well below the gate, so they cannot bypass it.
    for end_x in (-9000, 9000):
        if _near_segment(x, y, 0, 2500, end_x, 0, 320):
            return tiles['Lrok']
        if _near_segment(x, y, 0, 2500, end_x, 0, 512):
            return tiles['Ldro']

    # Broad connected town squares give every settlement a readable paved
    # center while leaving its branch road open through the middle.
    for town in TOWNS:
        dx, dy = abs(x-town['x']), abs(y-town['y'])
        if dx <= 1280 and dy <= 1280:
            if dx >= 1152 or dy >= 1152:
                return tiles['Lrok']
            return tiles['Lgrd']

    # King's courtyard and the larger shared-market square sit south of the
    # player row. The market plaza remains connected to the central road.
    if abs(x) <= 1400 and -1900 <= y <= 250:
        return tiles['Lrok']
    if abs(x) <= 1900 and -5100 <= y <= -3000:
        return tiles['Lrok']

    # Break up the grass with broad, deterministic patches instead of leaving
    # the enlarged playable area as a uniform dirt field.
    patch = ((x // 512) * 13 + (y // 512) * 17) % 29
    if patch in (0, 1, 2):
        return tiles['Ldrg']
    if patch in (8, 9, 10, 11):
        return tiles['Lgrd']
    return tiles['Lgrs']


def expanded_terrain(template, plots, map_cells=MAP_CELLS):
    if len(template) < W3E_HEADER_SIZE or template[:4] != b'W3E!':
        raise ValueError('Invalid W3E terrain header.')
    version = struct.unpack_from('<I', template, 4)[0]
    width, height = struct.unpack_from('<II', template, 53)
    if version != 12 or width != 65 or height != 65 or len(template) != W3E_HEADER_SIZE + width * height * 8:
        raise ValueError('Expected the validated 64-cell version 12 terrain fixture.')
    if map_cells != 192:
        raise ValueError('This build is configured for a 192-cell battlefield.')

    tiles = _ground_palette(template)
    old_vertices = [template[W3E_HEADER_SIZE + i * 8:W3E_HEADER_SIZE + (i + 1) * 8]
                    for i in range(width * height)]
    # Keep the flat starter's height and water level, and normalize cliff
    # metadata. The new terrain surfaces are painted with ground textures.
    modes = Counter((v[:6], v[7:8]) for v in old_vertices)
    base_height_flags, base_layer = modes.most_common(1)[0][0]
    base = bytearray(base_height_flags + b'\0' + base_layer)

    result = bytearray(template[:W3E_HEADER_SIZE])
    struct.pack_into('<II', result, 53, map_cells + 1, map_cells + 1)
    edge = map_cells * TILE_UNITS / 2
    struct.pack_into('<ff', result, 61, -edge, -edge)
    for row in range(map_cells + 1):
        y = -edge + row * TILE_UNITS
        for col in range(map_cells + 1):
            x = -edge + col * TILE_UNITS
            vertex = bytearray(base)
            # W3E v12: little-endian uint16 at offset 4; texture in low 6 bits.
            # Writing offset 5 sets water/boundary flags instead of painting.
            struct.pack_into('<H', vertex, 4, _paint(x, y, plots, tiles))
            result.extend(vertex)
    return bytes(result)


def expanded_pathing(template, map_cells=MAP_CELLS):
    if len(template) < 16:
        raise ValueError('Invalid WPM pathing header.')
    magic, version, width, height = struct.unpack_from('<4sIII', template)
    if magic != b'MP3W' or version != 0 or width != 256 or height != 256 or len(template) != 16 + width * height:
        raise ValueError('Expected the validated 64-cell blank-map pathing fixture.')
    if map_cells != 192:
        raise ValueError('This build is configured for a 192-cell battlefield.')
    pixels = map_cells * 4
    margin = 6 * 4
    data = bytearray([206]) * (pixels * pixels)
    for y in range(margin, pixels - margin):
        start = y * pixels + margin
        data[start:start + pixels - 2 * margin] = bytes([64]) * (pixels - 2 * margin)
    # Permanent ground barriers flank the open gate. Trees are not relied on
    # for containment: harvesting cannot open a route around the gateway.
    for row in range(margin, pixels - margin):
        world_y = -map_cells * 64 + (row + 0.5) * 32
        if 4800 <= world_y <= 5600:
            for col in range(margin, pixels - margin):
                world_x = -map_cells * 64 + (col + 0.5) * 32
                if abs(world_x) >= 1100:
                    data[row * pixels + col] |= 2  # ground movement blocked
    return struct.pack('<4sIII', magic, version, pixels, pixels) + data
