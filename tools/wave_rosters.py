"""Forty mixed attack rosters; living mercenaries support the undead invasion."""
BOSS_MECHANICS = (
    {'wave':10, 'id':1, 'name':'Bonequake', 'warning':'Leave the marked circle.', 'actions':('slam',)},
    {'wave':20, 'id':2, 'name':'Grave Muster', 'warning':'Skeletons and felguards are incoming.', 'actions':('summon',)},
    {'wave':30, 'id':3, 'name':'Siege Blight', 'warning':'Defender towers will be suppressed.', 'actions':('tower_suppression',)},
    {'wave':40, 'id':4, 'name':'The Last March', 'warning':'Dodge, then survive the horde and tower blackout.', 'actions':('slam','summon','tower_suppression')},
)

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
}

BOSS_UNIT_CODES = ('Udea', 'Ulic', 'Udre', 'Uanb')


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

def boss_mechanic_for_wave(wave):
    for mechanic in BOSS_MECHANICS:
        if mechanic['wave'] == wave:
            return mechanic['id']
    return 0

def boss_script():
    lines = ['function KLS_BossMechanicForWave takes integer wave returns integer']
    for mechanic in BOSS_MECHANICS:
        lines += [f"    if wave == {mechanic['wave']} then", f"        return {mechanic['id']}", '    endif']
    lines += ['    return 0', 'endfunction', 'function KLS_BossMechanicName takes integer mechanic returns string']
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

def wave_script():
    lines=['function KLS_WaveRosterInit takes nothing returns nothing']
    for wave,roster in enumerate(wave_rosters(),1):
        lines.append(f'    set KLS_RosterSize[{wave}] = {len(roster)}')
        for i,kind in enumerate(roster):lines.append(f"    set KLS_Roster[{wave*20+i}] = '{kind}'")
    lines+=['endfunction']
    return '\n'.join(lines)
