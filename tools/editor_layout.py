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
import re
import struct
from pathlib import Path
from archive_pack import MPQArchive, member, pack
from layout_catalog import editor_placements
from map_info import PLOTS

PREVIEW_OWNER = 26  # DE's 24 playable slots + neutral hostile/victim.
RECORD_SIZE = 131


def native_unit_spans(data):
    """Locate complete DE records without rewriting their optional payloads."""
    from editor_workshop import Reader
    r = Reader(data)
    if r.take(4) != b'W3do' or (r.number(), r.number()) != (13, 11):
        raise ValueError('Requires native unit placement format DE 13.11')
    spans = []
    identities = set()
    for _ in range(r.count()):
        start = r.pos
        raw = r.raw()
        r.take(36)  # variation, position, facing, scale, skin
        r.take(19)  # group, flags, owner, two unknown bytes, HP and mana
        r.take(4)   # map item table
        for _ in range(r.count()):
            r.take(r.count()*8)
        r.take(24)  # gold, acquisition, four hero statistics
        r.take(r.count()*8)
        r.take(r.count()*12)
        mode = r.number()
        if mode == 0:
            r.take(4)
        elif mode == 1:
            r.take(8)
        elif mode == 2:
            r.take(r.count()*8)
        else:
            raise ValueError('Unknown native random-unit mode')
        r.take(8)  # color and waygate
        identity = r.number()
        if identity in identities:
            raise ValueError('Duplicate native creation identity')
        identities.add(identity)
        r.take(8)  # roll and pitch
        r.take(r.count()*36)
        spans.append((identity, raw, start, r.pos))
    r.finish()
    return spans


def ungroup_forest_units(data):
    """Repair only portal/camp identities; preserve every other record byte."""
    result = bytearray(data)
    for identity, raw, start, _ in native_unit_spans(data):
        if identity == 146 and raw == 'kInv' or 147 <= identity <= 158 and raw in {
                f'k{prefix}{i:02d}' for prefix in ('L', 'M') for i in range(4)}:
            struct.pack_into('<i', result, start+40, -1)
    return bytes(result)


def market_coordinates_from_units(data):
    """Import roles by stable native creation identity, never proximity/order."""
    entries = {identity:(raw,start) for identity,raw,start,_ in native_unit_spans(data)}
    points = []
    for identity in range(7,20):
        if identity not in entries:
            raise ValueError('Missing market creation identity '+str(identity))
        raw, start = entries[identity]
        if raw != ('hS02' if identity == 18 else 'hS00'):
            raise ValueError('Unexpected market unit type at '+str(identity))
        if struct.unpack_from('<I', data, start+45)[0] != PREVIEW_OWNER:
            raise ValueError('Market reference must retain Neutral Extra ownership')
        x,y = struct.unpack_from('<2f', data, start+8)
        facing = math.degrees(struct.unpack_from('<f', data, start+20)[0]) % 360
        if not all(math.isfinite(v) for v in (x,y,facing)):
            raise ValueError('Invalid market coordinate')
        points.append((float(x),float(y),round(facing,4)))
    return tuple(points)


def import_market_layout(source):
    """Persist saved shop moves in the shared source catalog."""
    from editor_workshop import read_map
    source = Path(source)
    data = ((source/'war3mapUnits.doo').read_bytes() if source.is_dir()
            else read_map(source)[1]['war3mapUnits.doo'])
    points = market_coordinates_from_units(data)
    catalog = Path(__file__).with_name('layout_catalog.py')
    text = catalog.read_text(encoding='utf-8')
    replacement = 'MARKET_SQUARE = (\n' + ''.join(
        f'    ({x:g}, {y:g}, {angle:g}),\n' for x,y,angle in points) + ')'
    text, count = re.subn(r'MARKET_SQUARE = \(.*?\n\)',replacement,text,count=1,flags=re.S)
    if count != 1:
        raise ValueError('Market catalog declaration not found')
    catalog.write_text(text,encoding='utf-8')
    return {'source':str(source.resolve()),'market_coordinates':points}


def replace_runtime_functions(text, replacements):
    """Replace explicit complete functions, preserving all other editor code."""
    missing = []
    for name, body in replacements.items():
        pattern = rf'^function {re.escape(name)}\b[^\n]*\n.*?^endfunction\b'
        matches = list(re.finditer(pattern, text, re.M | re.S))
        if len(matches) > 1:
            raise ValueError('Duplicate runtime function: ' + name)
        if matches:
            match = matches[0]
            text = text[:match.start()] + body + text[match.end():]
        else:
            missing.append(body)
    if missing:
        # All selected helpers depend on checked spawning and precede story/waves.
        anchor = 'KLS_CreateShops' if 'KLS_MarketFacing' in replacements else 'KLS_CrownlandsBuildTowns'
        at = text.index('function '+anchor)
        text = text[:at] + '\n\n'.join(missing) + '\n\n' + text[at:]
    return text


def update_northern_editor_runtime(source, target, baseline=None, forest=False, countryside=False):
    """Explicit northern-site handoff, with original native members preserved.

    Does not regenerate objects, globals, native main, or placements. Both JASS
    and the editor custom-script header receive the same selected functions.
    """
    from pipeline import runtime_script, compile_script
    from gui_sources import gui_sources
    from editor_workshop import read_map
    if Path(target).exists():
        raise ValueError('Preserve the existing output before refreshing editor runtime')
    countryside_geometry = None
    if countryside:
        if not Path(source).is_dir():
            raise ValueError('Countryside handoff requires the saved dedicated Forge folder')
        countryside_geometry = json.loads((Path(source)/'countryside-plan.json').read_text())
    if Path(source).is_dir():
        if baseline is None:
            raise ValueError('Extracted Forge folders require their preserved native MPQ baseline')
        members = {p.name: p.read_bytes() for p in Path(source).iterdir()
                   if p.is_file() and p.name.startswith('war3map') and not p.name.endswith('.bak')}
        staged = Path(target).with_suffix('.input.w3m')
        if staged.exists():
            raise ValueError('Staged handoff input already exists')
        pack(baseline, staged, members)
        source = staged
    _, contents, build_id = read_map(source)
    script, _, _ = gui_sources(runtime_script(build_id))
    names = ('KLS_FindInvasionGate', 'KLS_InvasionGateInit', 'KLS_OrderInvader',
             'KLS_CrownlandsBuildTowns', 'KLS_StoryApplyUnlock',
             'KLS_StoryComplete', 'KLS_StorySpawnEncounter',
             'KLS_Spawn', 'KLS_BuildLandscape')
    if forest:
        names += ('KLS_IsForestMonster', 'KLS_ForestReward', 'KLS_ForestInit', 'KLS_Death')
    if countryside:
        names = ('KLS_MarketX', 'KLS_MarketY', 'KLS_MarketFacing')
    replacements = {}
    for name in names:
        replacements[name] = re.search(rf'^function {name}\b[^\n]*\n.*?^endfunction\b',
                                       script, re.M | re.S)[0]
    def refresh(text):
        text = replace_runtime_functions(text, replacements)
        if countryside:
            # This older editor runtime used literal 270-degree facings even
            # though its XY helpers were generated. Update only these four
            # constructor arguments, retaining the exact existing stock code.
            for index in ('tier*2+i','10','11','12'):
                text = text.replace(f'KLS_MarketY({index}),270)',
                                    f'KLS_MarketY({index}),KLS_MarketFacing({index}))')
        if not countryside and 'call KLS_InvasionGateInit()' not in text:
            marker = '    call KLS_BuildLandscape()'
            if text.count(marker) != 1:
                raise ValueError('Unexpected initialization structure')
            text = text.replace(marker, '    call KLS_InvasionGateInit()\n' + marker)
        if forest and 'call KLS_ForestInit()' not in text:
            text = text.replace('    call KLS_InvasionGateInit()',
                                '    call KLS_InvasionGateInit()\n    call KLS_ForestInit()')
        return text
    jass = refresh(contents['war3map.j'].decode('utf-8'))
    wct = contents['war3map.wct']
    if struct.unpack_from('<2I', wct) != (0x80000004, 1):
        raise ValueError('Requires the installed DE custom-script header format')
    size_at = wct.index(b'\0', 8) + 1
    size = struct.unpack_from('<I', wct, size_at)[0]
    code_at = size_at + 4
    header = wct[code_at:code_at + size]
    suffix = header[len(header.rstrip(b'\0')):]
    updated = refresh(header.rstrip(b'\0').decode('utf-8')).encode('utf-8') + suffix
    wct = wct[:size_at] + struct.pack('<I', len(updated)) + updated + wct[code_at + size:]
    check = Path(target).with_suffix('.j')
    check.write_text(jass, encoding='utf-8')
    syntax = compile_script(check)
    changed = {'war3map.j': jass.encode('utf-8'), 'war3map.wct': wct}
    if forest:
        from forest_catalog import forest_pathing
        changed['war3map.wpm'] = forest_pathing(contents['war3map.wpm'])
    if countryside:
        from countryside_catalog import countryside_pathing
        changed['war3mapUnits.doo'] = ungroup_forest_units(contents['war3mapUnits.doo'])
        changed['war3map.wpm'] = countryside_pathing(contents['war3map.wpm'],countryside_geometry,contents['war3map.w3e'])
    pack(source, target, changed)
    _, after, _ = read_map(target)
    if set(after) != set(contents) or any(after[name] != changed.get(name, value)
                                         for name, value in contents.items() if name != '(attributes)'):
        raise ValueError('Editor runtime handoff changed an unexpected member')
    report = {'path': str(Path(target).resolve()), 'sha256': hashlib.sha256(Path(target).read_bytes()).hexdigest(),
              'source_build_id': build_id, 'status': 'development editor handoff; engine checks pending',
              'changed_members': list(changed), 'functions': list(names)+(['KLS_CreateShops facing arguments'] if countryside else []), 'syntax': syntax,
              'preservation': 'all other content members byte-identical; archive CRC attributes regenerated'}
    Path(target).with_suffix('.json').write_text(json.dumps(report, indent=2), encoding='utf-8')
    return report


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
