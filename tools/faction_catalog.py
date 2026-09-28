"""Shared four-race worker, town, building, and tower role catalog."""

_COMPANY_COSTS = {
    'hall': (240,100,35,1400),
    'foundry': (360,150,45,1600),
    'siege_yard': (300,125,40,1500),
}
_COMPANY_NAMES = {
    'Human': ('Hall of Banners','Royal Foundry','Siege Yard'),
    'Orc': ('Redtusk Banner Hall','Ashen War Forge','War Drummer Lodge'),
    'Night Elf': ('Moonlit Banner Hall','Moonbark Runeforge','Sentinel War Grove'),
    'Undead': ('Bone Banner Hall','Wraithforged Smithy','Graveyard of Arms'),
}
_ARCANE_NAMES = ('Arcane Sanctum','Spirit Lodge','Ancient Lore Grove','Temple of the Damned')
_TOWER_NAMES = {
    'Human': ('Guard Tower','Cannon Tower','Sanctuary Tower'),
    'Orc': ('Watch Tower','War Drum Tower','Spirit Ward'),
    'Night Elf': ('Ancient Protector','Moonfire Spire','Moonwell Sentinel'),
    'Undead': ('Ziggurat Tower','Frost Tower','Soulwell Spire'),
}

FACTIONS = [
    {'race':'Human','worker':'hpea','town_hall':'htow','altar':'h000','altar_parent':'halt',
     'food':'hhou','barracks':'hbar','blacksmith':'hbla','arcane':'h004','arcane_parent':'hars',
     'towers':('h001','h002','h003'),'tower_parents':('hgtw','hctw','hatw')},
    {'race':'Orc','worker':'opeo','town_hall':'ogre','altar':'kA01','altar_parent':'oalt',
     'food':'otrb','barracks':'obar','blacksmith':'ofor','arcane':'kR01','arcane_parent':'osld',
     'towers':('kT10','kT11','kT12'),'tower_parents':('owtw','owtw','owtw')},
    {'race':'Night Elf','worker':'ewsp','town_hall':'etol','altar':'kA02','altar_parent':'eate',
     'food':'emow','barracks':'eaow','blacksmith':'eaoe','arcane':'kR02','arcane_parent':'eaoe',
     'towers':('kT20','kT21','kT22'),'tower_parents':('etrp','etrp','etrp')},
    {'race':'Undead','worker':'uaco','town_hall':'unpl','altar':'kA03','altar_parent':'uaod',
     'food':'uzig','barracks':'usep','blacksmith':'uslh','arcane':'kR03','arcane_parent':'umtw',
     'towers':('kT30','kT31','kT32'),'tower_parents':('uzig','uzg2','uzig')},
]

for race_index, faction in enumerate(FACTIONS):
    hall_name, foundry_name, yard_name = _COMPANY_NAMES[faction['race']]
    faction['company_buildings'] = {
        'hall': {'rawcode':f'kH0{race_index}','parent':('hcas','ofrt','etol','unpl')[race_index],
                 'name':hall_name,'tooltip':'Raise the company banner for your chosen hero and unlock its personal Barracks recruit.'},
        'foundry': {'rawcode':f'kF0{race_index}','parent':('hbla','ofor','eaoe','uslh')[race_index],
                    'name':foundry_name,'tooltip':'Veteran arms grant your company and support troops +20% maximum health and +20% base damage.'},
        'siege_yard': {'rawcode':f'kY0{race_index}','parent':('harm','obar','eaow','usep')[race_index],
                       'name':yard_name,'tooltip':'Train the tactical support unit chosen for your hero. Stock belongs to this player.'},
    }
    for key, building in faction['company_buildings'].items():
        gold,lumber,build_time,hit_points = _COMPANY_COSTS[key]
        building.update(gold=gold,lumber=lumber,build_time=build_time,hit_points=hit_points)
    faction['build_menu'] = [faction['town_hall'], faction['altar'], faction['food'],
        faction['barracks'], faction['blacksmith'], faction['arcane'], *faction['towers'],
        *[faction['company_buildings'][key]['rawcode'] for key in ('hall','foundry','siege_yard')]]
    for index, entry in enumerate(faction['company_buildings'].values()):
        entry['race'] = faction['race']
        entry['role'] = ('hall','foundry','siege_yard')[index]
        entry['build_time'] = _COMPANY_COSTS[entry['role']][2]

def faction_script():
    lines=['function KLS_FactionCatalogInit takes nothing returns nothing']
    for index, faction in enumerate(FACTIONS):
        for key, field in (('TownHall','town_hall'),('Worker','worker'),('Altar','altar'),
                           ('Barracks','barracks'),('Food','food'),('Blacksmith','blacksmith'),('Arcane','arcane')):
            lines.append(f"    set KLS_Faction{key}Id[{index}] = '{faction[field]}'")
        for index_tower, rawcode in enumerate(faction['towers']):
            lines.append(f"    set KLS_FactionTowerId[{index*3+index_tower}] = '{rawcode}'")
        for key in ('hall','foundry','siege_yard'):
            lines.append(f"    set KLS_Faction{key.title().replace('_','')}Id[{index}] = '{faction['company_buildings'][key]['rawcode']}'")
    lines.append('endfunction')
    for role in ('Hall','Foundry','SiegeYard','Barracks','Altar','Tower','SanctuaryTower'):
        lines.append(f'function KLS_IsFaction{role} takes integer rawcode returns boolean')
        ids=[]
        if role=='Hall': ids=[f['company_buildings']['hall']['rawcode'] for f in FACTIONS]
        elif role=='Foundry': ids=[f['company_buildings']['foundry']['rawcode'] for f in FACTIONS]
        elif role=='SiegeYard': ids=[f['company_buildings']['siege_yard']['rawcode'] for f in FACTIONS]
        elif role=='Barracks': ids=[f['barracks'] for f in FACTIONS]
        elif role=='Altar': ids=[f['altar'] for f in FACTIONS]
        elif role=='Tower': ids=[raw for f in FACTIONS for raw in f['towers']]
        elif role=='SanctuaryTower': ids=[f['towers'][2] for f in FACTIONS]
        lines.append('    return ' + ' or '.join("rawcode == '"+code+"'" for code in ids))
        lines.append('endfunction')
    return '\n'.join(lines)
