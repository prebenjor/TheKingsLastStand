"""Forty preserved story rosters and a repeating campaign crossover roster."""
BOSS_MECHANICS = (
    {'wave':10, 'id':1, 'name':'Bonequake', 'warning':'Leave the marked circle.', 'actions':('slam',)},
    {'wave':20, 'id':2, 'name':'Grave Muster', 'warning':'Skeletons and felguards are incoming.', 'actions':('summon',)},
    {'wave':30, 'id':3, 'name':'Siege Blight', 'warning':'Defender towers will be suppressed.', 'actions':('tower_suppression',)},
    {'wave':40, 'id':4, 'name':'The Last March', 'warning':'Dodge, then survive the horde and tower blackout.', 'actions':('slam','summon','tower_suppression')},
    {'wave':50, 'id':5, 'name':'Endless Convergence', 'warning':'Dodge the slam, stop the reinforcements, and weather the tower blackout.', 'actions':('slam','summon','tower_suppression')},
)

# These ten rows repeat forever. The source row is always bounded to waves
# 41–50; live wave number still drives count, health, damage, bounty and boss
# scaling. All additions are installed campaign or native game records.
ENDLESS_ROSTERS = (
    ('nmyr','nmyr','nnsw','nnmg','ucry','uske','nfel','nbel','nbee','nchg','nfgu','nska'),
    ('nnrg','nnsw','nhyc','nbel','nbee','hbew','uske','unec','nchg','nchw','nfgu','nfel','nwgs'),
    ('nchg','nchg','nchr','nchw','nckb','nnmg','nnrg','ucry','nska','nbel','nbal','nfgu','nmyr'),
    ('nfgu','nfel','nbal','ninf','nchr','nchw','nmyr','nnsw','uabo','unec','nbel','nbee','hbew'),
    ('uske','uske','nska','ugho','ucry','ucry','unec','uabo','umtw','nmyr','nnsw','nfel','nchr','nbel'),
    ('nmyr','nnmg','nwgs','nbel','nbee','nchw','nfgu','ucry','nska','unec','nbal','uabo','hbew','nhyc'),
    ('nchg','nchr','nchw','nckb','nnrg','nhyc','nbel','hbew','nfel','nfgu','uske','uabo','umtw','nwgs'),
    ('nmyr','nnmg','nnsw','nbel','nbee','hbew','nchg','nchr','nchw','nckb','nfel','nfgu','nbal','ucry','unec','umtw','nwgs'),
    ('nmyr','nnrg','nbel','nbee','nchg','nchr','nfgu','ninf','uske','umtw','nnsw','nfel','nchw','ucry','nska','unec','nhyc','hbew'),
    ('nnrg','nwgs','nmyr','nnsw','nbel','nchw','nchr','nfgu','nfel','ucry','uabo','ninf','hbew','unec','umtw'),
)

ENDLESS_WAVE_NAMES = (
    'The Drowned Vanguard', 'The Sunken Embassy', 'The Ashen Pact',
    'Legion Inheritance', 'The Barrow Tide', 'The Returned Host',
    'Four Oathbreakers', 'The Open Confluence', 'Crownlands Convergence',
    'Vashj Ascendant',
)
ENDLESS_BOSS_UNITS = ('Hvsh', 'Usyl', 'Uanb', 'Hjsm', 'Ujsm')
ENDLESS_MECHANIC_CYCLE = (5, 1, 2, 3)

# Base personal-team bounty by installed enemy rawcode. Add KLS_Wave when paid
# so later appearances of a role stay valuable without erasing role differences.
BOUNTY_BY_UNIT = {
    'uske': 5,    # Skeleton Warrior
    'ugho': 8,    # Ghoul
    'hfoo': 9,    # Footman escort
    'ucry': 12,   # Crypt Fiend
    'nska': 12,   # Skeletal Archer
    'nsat': 14,   # Satyr Trickster
    'ndqn': 16,   # Succubus
    'nvdw': 16,   # Voidwalker
    'nfel': 18,   # Fel Stalker
    'unec': 22,   # Necromancer
    'nfgu': 24,   # Felguard
    'uabo': 32,   # Abomination
    'umtw': 36,   # Meat Wagon
    'nbal': 40,   # Doom Guard
    'ninf': 45,   # Infernal
    'nmyr': 28,   # Naga Myrmidon
    'nnsw': 24,   # Naga Siren
    'nnmg': 28,   # Mur'gul Reaver
    'nnrg': 40,   # Naga Royal Guard
    'nhyc': 42,   # Naga Dragon Turtle
    'nwgs': 36,   # Naga Couatl
    'nbel': 25,   # Blood Elf Lieutenant
    'nbee': 22,   # Blood Elf Engineer
    'hbew': 36,   # Blood Elf Siege Wagon
    'nchg': 24,   # Chaos Grunt (Fel Orc)
    'nchr': 30,   # Chaos Wolf Rider (Fel Orc)
    'nchw': 30,   # Chaos Warlock (Fel Orc)
    'nckb': 34,   # Chaos Kodo Beast (Fel Orc)
}

SIEGE_UNIT_CODES = ('umtw', 'hbew', 'nhyc')

BOSS_UNIT_CODES = ('Udea', 'Ulic', 'Udre', 'Uanb', 'Hvsh', 'Usyl', 'Hjsm', 'Ujsm')

ENEMY_LOOT_TIER_BY_UNIT = {
    # Recruits and basic infantry remain the baseline loot tier.
    'uske': 'normal',
    'ugho': 'normal',
    'hfoo': 'normal',
    'nska': 'normal',
    'nsat': 'normal',
    # Durable, elite, siege and high-threat campaign roles use richer drops.
    'ucry': 'elite',
    'ndqn': 'elite',
    'nvdw': 'elite',
    'nfel': 'elite',
    'unec': 'elite',
    'nfgu': 'elite',
    'uabo': 'elite',
    'umtw': 'elite',
    'nbal': 'elite',
    'ninf': 'elite',
    'nmyr': 'elite',
    'nnsw': 'elite',
    'nnmg': 'elite',
    'nnrg': 'elite',
    'nhyc': 'elite',
    'nwgs': 'elite',
    'nbel': 'elite',
    'nbee': 'elite',
    'hbew': 'elite',
    'nchg': 'elite',
    'nchr': 'elite',
    'nchw': 'elite',
    'nckb': 'elite',
}


def bounty_script():
    boss_condition = ' or '.join(f"unitCode == '{unit_code}'" for unit_code in BOSS_UNIT_CODES)
    lines = [
        'function KLS_EnemyBounty takes unit enemy returns integer',
        '    local integer unitCode = GetUnitTypeId(enemy)',
        f'    if {boss_condition} then',
        '        return 100 + KLS_Wave * 5',
        '    endif',
    ]
    for unit_code, base_bounty in BOUNTY_BY_UNIT.items():
        lines += [
            f"    if unitCode == '{unit_code}' then",
            f'        return {base_bounty} + KLS_Wave',
            '    endif',
        ]
    lines += [
        '    return 8 + KLS_Wave',
        'endfunction',
    ]
    return '\n'.join(lines)

def endless_wave_rosters():
    """Return fresh copies of the ten generated endless-mode roster rows."""
    return [list(roster) for roster in ENDLESS_ROSTERS]


def roster_source_wave(wave):
    """Map a live wave to a generated row without an unbounded roster index."""
    if wave <= 40:
        return max(1, wave)
    return 41 + ((wave - 41) % 10)


def roster_for_wave(wave):
    source_wave = roster_source_wave(wave)
    if source_wave <= 40:
        return wave_rosters()[source_wave - 1]
    return list(ENDLESS_ROSTERS[source_wave - 41])


def boss_mechanic_for_wave(wave):
    for mechanic in BOSS_MECHANICS:
        if mechanic['wave'] == wave:
            return mechanic['id']
    if wave >= 60 and wave % 10 == 0:
        return ENDLESS_MECHANIC_CYCLE[((wave // 10) - 5) % len(ENDLESS_MECHANIC_CYCLE)]
    return 0


def boss_unit_for_wave(wave):
    original = {10: 'Udea', 20: 'Ulic', 30: 'Udre', 40: 'Uanb'}
    if wave in original:
        return original[wave]
    if wave >= 50 and wave % 10 == 0:
        return ENDLESS_BOSS_UNITS[((wave // 10) - 5) % len(ENDLESS_BOSS_UNITS)]
    return None


def boss_script():
    lines = ['function KLS_BossMechanicForWave takes integer wave returns integer', '    local integer cycle = 0']
    for mechanic in BOSS_MECHANICS:
        lines += [f"    if wave == {mechanic['wave']} then", f"        return {mechanic['id']}", '    endif']
    lines += [
        '    if wave >= 60 and ModuloInteger(wave, 10) == 0 then',
        '        set cycle = ModuloInteger(wave / 10 - 6, 4)',
        '        if cycle == 0 then', '            return 1',
        '        elseif cycle == 1 then', '            return 2',
        '        elseif cycle == 2 then', '            return 3',
        '        else', '            return 5',
        '        endif', '    endif',
        '    return 0', 'endfunction',
        'function KLS_BossUnitForWave takes integer wave returns integer',
        '    local integer cycle = 0',
    ]
    for wave, unit_code in ((10, 'Udea'), (20, 'Ulic'), (30, 'Udre'), (40, 'Uanb')):
        lines += [f"    if wave == {wave} then", f"        return '{unit_code}'", '    endif']
    lines += ['    if wave >= 50 and ModuloInteger(wave, 10) == 0 then',
              '        set cycle = ModuloInteger(wave / 10 - 5, 5)']
    for index, unit_code in enumerate(ENDLESS_BOSS_UNITS):
        branch = 'if' if index == 0 else 'elseif'
        lines += [f'        {branch} cycle == {index} then', f"            return '{unit_code}'"]
    lines += ['        endif', '    endif', '    return 0', 'endfunction',
              'function KLS_BossMechanicName takes integer mechanic returns string']
    for mechanic in BOSS_MECHANICS:
        lines += [f"    if mechanic == {mechanic['id']} then", f"        return \"{mechanic['name']}\"", '    endif']
    lines += ['    return "No active boss"', 'endfunction', 'function KLS_BossMechanicWarning takes integer mechanic returns string']
    for mechanic in BOSS_MECHANICS:
        lines += [f"    if mechanic == {mechanic['id']} then", f"        return \"{mechanic['warning']}\"", '    endif']
    lines += ['    return ""', 'endfunction']
    return '\n'.join(lines)

def wave_rosters():
    result=[]
    for wave in range(1,41):
        # Every wave retains both living and undead targets. Rotate its emphasis.
        base=['ugho','uske','ugho','ucry','nska','nfel','hfoo','ugho']
        if wave>=4:base[7]='nfgu'
        if wave>=7:base+=['unec','nsat']
        if wave>=11:base+=['uabo','ndqn']
        if wave>=16:base+=['ucry','nvdw']
        if wave>=21:base+=['umtw','nbal']
        if wave>=26:base+=['unec','nfgu']
        if wave>=31:base+=['ninf','uabo']
        rotation=(wave-1)%len(base)
        result.append(base[rotation:]+base[:rotation])
    return result


def all_wave_rosters():
    return wave_rosters() + endless_wave_rosters()


def wave_script():
    lines = [
        'function KLS_RosterSourceWave takes integer wave returns integer',
        '    if wave <= 40 then',
        '        return wave',
        '    endif',
        '    return 41 + ModuloInteger(wave - 41, 10)',
        'endfunction',
        'function KLS_WaveRosterInit takes nothing returns nothing',
    ]
    for wave, roster in enumerate(all_wave_rosters(), 1):
        lines.append(f'    set KLS_RosterSize[{wave}] = {len(roster)}')
        for i, kind in enumerate(roster):
            lines.append(f"    set KLS_Roster[{wave * 20 + i}] = '{kind}'")
    lines += ['endfunction']
    return '\n'.join(lines)


def roster_catalog_markdown():
    chapter_names = (
        'The Broken Verge', 'The Grave March', 'The Siege Tide', 'The Last Host',
    )
    lines = [
        '# Generated wave roster catalog',
        '',
        'Generated from `tools/wave_rosters.py`; this table is the ordered rawcode sequence used by the wave generator. Waves 1-40 remain the original four chapters. Waves 41-50 introduce the Naga, Blood Elf, Fel Orc, Burning Legion and Scourge campaign crossover. Wave 49 is the five-force convergence; the campaign Lady Vashj leads the separate Wave 50 boss spawn.',
        '',
        'Live waves after 50 reuse these ten rows with the bounded source index `41 + ((wave - 41) % 10)`. Counts and unit health, damage, bounty, and boss scaling continue to use the live wave number. Bosses spawn separately every ten waves.',
        '',
        '| Wave | Chapter / crossover | Ordered unit rawcodes |',
        '|---:|---|---|',
    ]
    for wave, roster in enumerate(all_wave_rosters(), 1):
        if wave <= 40:
            arc = chapter_names[(wave - 1) // 10]
        else:
            arc = ENDLESS_WAVE_NAMES[wave - 41]
        lines.append(f"| {wave} | {arc} | {', '.join(roster)} |")
    lines.append('')
    return '\n'.join(lines)


if __name__ == '__main__':
    from pathlib import Path
    root = Path(__file__).resolve().parents[1]
    (root / 'docs' / 'WAVE-ROSTER-CATALOG.md').write_text(roster_catalog_markdown(), encoding='utf-8')
