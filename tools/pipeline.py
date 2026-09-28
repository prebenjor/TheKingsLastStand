"""Reproducible, verified diagnostic build. Release publication is gated."""
import hashlib
import json
import re
import shutil
import struct
import subprocess
from pathlib import Path
from archive_pack import pack, member, lookup
from map_archive import MPQArchive
from map_info import four_player_info, PLOTS, MAP_EDGE
from objects import units, items
from equipment_catalog import abilities, catalog_script
from wave_rosters import wave_script, boss_script
from signature_spells import spell_script as signature_spell_script
from hero_progression import spell_script as hero_spell_script
from recipes import recipe_script
from gui_sources import gui_sources
from terrain import expanded_terrain, expanded_pathing

ROOT = Path(__file__).resolve().parents[1]
MODULES = ('diagnostics.j', 'heroes.j', 'backpack.j', 'shops.j', 'equipment.j', 'hud.j', 'castle.j', 'combat.j', 'wave_environment.j', 'signatures.j', 'game.j')
BASELINE_SHA = '3b68da520c3d14084c7eec4fffae5cfc76315c58990a1415a4f897c0b781e8d9'
INFO_SHA = 'a6275d4b92e8c8f1267536d0e175eb1ece7dbb031f1447a2a0295c0b86a461cc'
GAME = Path(r'C:\Program Files (x86)\Warcraft III')


def digest(data):
    return hashlib.sha256(data).hexdigest()


def misc_data():
    return b'[Misc]\nMaxHeroLevel=100\n'


def baseline():
    target = ROOT / 'backups/Blank-DE.w3m'
    if not target.exists():
        original = ROOT / 'TheKingsLastStand.blank-backup.w3m'
        if digest(original.read_bytes()) != BASELINE_SHA:
            raise ValueError('Starter map differs from the proven DE baseline; revalidate its metadata first.')
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(original, target)
    if digest(target.read_bytes()) != BASELINE_SHA:
        raise ValueError('backups/Blank-DE.w3m changed; restore the known blank baseline.')
    return target


def check_api():
    folder = ROOT / 'tools/reference/installed'
    path = folder / 'provenance.json'
    if not path.exists():
        raise ValueError('Extract installed APIs first: python kings-last-stand/tools/extract_game_api.py')
    data = json.loads(path.read_text())
    if digest((GAME / '.build.info').read_bytes()) != data['build_info_sha256']:
        raise ValueError('Warcraft III installation changed. Re-extract its API declarations before building.')
    for name, entry in data['files'].items():
        if digest((folder / name).read_bytes()) != entry['sha256']:
            raise ValueError('Installed game reference changed: ' + name + '. Re-extract from the installed game.')
    return data


def runtime_script(build_id):
    declarations = []
    functions = []
    for name in MODULES:
        text = (ROOT / 'source' / name).read_text()
        if name == 'shops.j':
            text = text.replace('// GENERATED_CATALOG', catalog_script())
            text = text.replace('// GENERATED_RECIPES', recipe_script())
        if name == 'heroes.j':
            text = text.replace('// GENERATED_HERO_PROGRESSION', hero_spell_script())
        if name == 'hud.j':
            text = text.replace('// GENERATED_BOSSES', boss_script())
        if name == 'wave_environment.j':
            text = text.replace('// GENERATED_WAVES', wave_script())
        if name == 'signatures.j':
            text = text.replace('// GENERATED_SIGNATURES', signature_spell_script())
        blocks = re.findall(r'^globals\s*\n(.*?)^endglobals\s*$', text, re.M | re.S)
        if len(blocks) != 1:
            raise ValueError('Expected one globals section in ' + name)
        declarations.extend(blocks)
        functions.append(re.sub(r'^globals\s*\n.*?^endglobals\s*$', '', text, flags=re.M | re.S))
    scalar_initializers = []
    for block in declarations:
        for line in block.splitlines():
            match = re.fullmatch(r'\s*\w+\s+(KLS_\w+)\s*=\s*(.+)', line)
            if match:
                scalar_initializers.append('    set ' + match[1] + ' = ' + match[2])
    declarations.append('    boolean KLS_Initialized = false')
    body = '\n'.join(functions).replace('KLS_BUILD_ID', build_id)
    marker = '    set KLS_Enemies = CreateGroup()'
    if body.count(marker) != 1:
        raise ValueError('Initializer structure changed; explicitly update the initialization insertion point.')
    initial = '\n'.join(['    if KLS_Initialized then', '        return', '    endif', '    set KLS_Initialized = true'] + scalar_initializers)
    body = body.replace(marker, initial + '\n' + marker)
    body = body.replace('The King\'s Last Stand: defend King Aldric!', 'DEVELOPMENT ' + build_id + ': defend King Aldric!')
    template = (ROOT / 'source/template/war3map.j').read_text()
    main = re.search(r'function main takes nothing returns nothing.*?endfunction', template, re.S).group()
    main = main.replace('    call InitGlobals(  )\n    call InitCustomTriggers(  )\n    call RunInitializationTriggers(  )', '    call KLS_Init()')
    if 'InitCustomTriggers' in main:
        raise ValueError('Blank main initializer replacement failed')
    edge = MAP_EDGE - 6 * 128
    camera = ('    call SetCameraBounds(' + ', '.join(str(float(v)) for v in
              (-edge, -edge, edge, edge, -edge, edge, edge, -edge)) + ')')
    main, replacements = re.subn(r'    call SetCameraBounds\([\s\S]*?\) \)', camera, main, count=1)
    if replacements != 1:
        raise ValueError('Expected one baseline camera bounds call; update the camera generator.')
    config = ['function config takes nothing returns nothing', f'    call SetMapName("KLS DEVELOPMENT {build_id}")', '    call SetMapDescription("Diagnostic build: editor and game startup check")', '    call SetPlayers(4)', '    call SetTeams(1)', '    call SetGamePlacement(MAP_PLACEMENT_USE_MAP_SETTINGS)']
    for i, (x, y) in enumerate(PLOTS):
        config += [f'    call DefineStartLocation({i}, {x}, {y})', f'    call SetPlayerStartLocation(Player({i}), {i})', f'    call SetPlayerColor(Player({i}), ConvertPlayerColor({i}))', f'    call SetPlayerRacePreference(Player({i}), RACE_PREF_HUMAN)', f'    call SetPlayerRaceSelectable(Player({i}), false)', f'    call SetPlayerController(Player({i}), MAP_CONTROL_USER)', f'    call SetPlayerSlotAvailable(Player({i}), MAP_CONTROL_USER)', f'    call SetPlayerTeam(Player({i}), 0)']
    config += ['    call InitGenericPlayerSlots()', 'endfunction']
    return 'globals\n'+'\n'.join(declarations)+'\nendglobals\n'+body+'\n'+main+'\n'+'\n'.join(config)+'\n'


def check_objects(data, extended=False):
    cursor = 0
    def integer():
        nonlocal cursor
        result = struct.unpack_from('<I', data, cursor)[0]
        cursor += 4
        return result
    if integer() != 2:
        raise ValueError('Unsupported object format')
    count = 0
    for _ in range(2):
        for _ in range(integer()):
            original, custom = data[cursor:cursor+4], data[cursor+4:cursor+8]
            cursor += 8
            for _ in range(integer()):
                cursor += 4
                typ = integer()
                if extended:
                    cursor += 8
                if typ == 3:
                    cursor = data.index(b'\0', cursor)+1
                elif typ in (0, 1, 2):
                    cursor += 4
                else:
                    raise ValueError('Invalid object field type')
                end = data[cursor:cursor+4]
                cursor += 4
                if end not in (original, custom, b'\0'*4):
                    raise ValueError('Invalid object field end marker')
            count += 1
    if cursor != len(data):
        raise ValueError('Unexpected trailing object bytes')
    return count


def compile_script(script_path):
    folder = ROOT / 'tools/reference/installed'
    exe = GAME / '_retail_/x86_64/JassHelper/pjass.exe'
    result = subprocess.run([str(exe), str(folder/'common.j'), str(folder/'blizzard.j'), str(script_path)], capture_output=True, text=True)
    if result.returncode:
        raise ValueError(result.stdout + result.stderr)
    return result.stdout


def diagnostic_output_path(build_id):
    """Return an immutable, build-specific artifact path."""
    return ROOT / 'build' / ('DIAGNOSTIC-' + build_id + '.w3m')


def build():
    source = baseline()
    api = check_api()
    source_paths = [ROOT/'source'/n for n in MODULES] + sorted((ROOT/'tools').glob('*.py'))
    source_paths += [ROOT/'tools/reference/installed'/n for n in ('ItemData.slk','AbilityData.slk','UnitMetaData.slk','AbilityMetaData.slk','WorldEditStrings.txt','UnitData.slk','ItemAbilityFunc.txt','commandbuttons.txt')]
    hashes = {str(p.relative_to(ROOT)).replace('\\','/'): digest(p.read_bytes()) for p in source_paths}
    build_id = 'KLS-D-' + digest(json.dumps({'sources':hashes,'api':api}, sort_keys=True).encode())[:10]
    raw_script = runtime_script(build_id)
    script, wtg, wct = gui_sources(raw_script)
    info = (ROOT/'source/template/war3map.w3i').read_bytes()
    if digest(info) != INFO_SHA or struct.unpack_from('<I', info)[0] != 39:
        raise ValueError('Unknown version 39 metadata fixture. Re-extract and validate the supplied DE baseline.')
    info = four_player_info(info)
    title_end = info.index(b'\0', 28)+1
    info = info[:28] + ('KLS DEVELOPMENT '+build_id).encode()+b'\0'+info[title_end:]
    components = {'war3map.j':script.encode(), 'war3map.wtg':wtg, 'war3map.wct':wct, 'war3map.w3i':info, 'war3map.w3u':units(), 'war3map.w3t':items(), 'war3map.w3a':abilities(), 'war3map.w3e':expanded_terrain((ROOT/'source/template/war3map.w3e').read_bytes(), PLOTS), 'war3map.wpm':expanded_pathing((ROOT/'source/template/war3map.wpm').read_bytes()), 'war3map.shd':bytes(512 * 512), 'war3mapMisc.txt':misc_data()}
    if 'call Melee' in script or b'Melee Initialization' in wtg or b'call Melee' in wct:
        raise ValueError('Default melee initialization found in output')
    for name in ('war3map.w3u','war3map.w3t'):
        check_objects(components[name])
    check_objects(components['war3map.w3a'], extended=True)
    output = diagnostic_output_path(build_id)
    output.parent.mkdir(parents=True, exist_ok=True)
    script_path = ROOT/'build/diagnostic-war3map.j'
    script_path.write_bytes(script.encode())
    syntax = compile_script(script_path)
    pack(source, output, components)
    a = MPQArchive(output, listfile=False)
    inventory = []
    try:
        names = member(a, '(listfile)').decode().splitlines()
        for name in names:
            if lookup(a, name) is None:
                raise ValueError('Invalid engine lookup: '+name)
            data = member(a, name)
            inventory.append({'name':name,'size':len(data),'sha256':digest(data)})
        for name, data in components.items():
            if name not in names or member(a,name) != data:
                raise ValueError('Package differs from source: '+name)
    finally:
        a.file.close()
    manifest = {'build_id':build_id,'status':'development: startup proof pending','output_path':str(output),'sha256':digest(output.read_bytes()),'baseline_sha256':BASELINE_SHA,'source_hashes':hashes,'installed_api':api,'components':inventory,'checks':{'syntax_installed_api':'passed','archive_readback':'passed','editor_roundtrip':'pending','game_startup':'pending','multiplayer':'pending'}}
    (ROOT/'build/diagnostic-manifest.json').write_text(json.dumps(manifest,indent=2))
    (ROOT/'build/diagnostic-syntax.txt').write_text(syntax)
    (ROOT/'source/war3map.j').write_bytes(script.encode())
    print(build_id)
    print(output)
    print('Package and installed-API syntax checks passed. Editor/game startup proof is pending.')
    return manifest


if __name__ == '__main__':
    raise SystemExit('Run tools/build_map.py instead.')
