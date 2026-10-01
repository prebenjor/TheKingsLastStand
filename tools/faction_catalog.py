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
_ARCANE_TOOLTIPS = {
    'Human': 'Human arcane college. Trains Priests to heal and Sorceresses to control the field; researches both orders’ spellcraft.',
    'Orc': 'Orc Spirit Lodge. Trains Shamans, Witch Doctors and Spirit Walkers, with their native spell training and research.',
    'Night Elf': 'Night Elf Ancient Lore Grove. Trains Druids of the Claw, Dryads and Mountain Giants, and researches their nature arts.',
    'Undead': 'Undead Temple of the Damned. Trains Necromancers and Banshees and researches their native dark rituals.',
}
for _race in _ARCANE_TOOLTIPS:
    _ARCANE_TOOLTIPS[_race] += ' Offers Spiritcraft Accord research: +25% potency to your company support powers.'

_ALTAR_TOOLTIPS = {
    'Human': 'The Human Altar of Kings calls your chosen champion. Fallen heroes return here after 20 seconds.',
    'Orc': 'The Orc Altar of Storms calls your chosen hero. Fallen heroes return here after 20 seconds.',
    'Night Elf': 'The Night Elf Altar of Elders calls your chosen hero. Fallen heroes return here after 20 seconds.',
    'Undead': 'The Undead Altar of Darkness calls your chosen hero. Fallen heroes return here after 20 seconds.',
}
_TOWER_NAMES = {
    'Human': ('Guard Tower','Cannon Tower','Sanctuary Tower'),
    'Orc': ('Watch Tower','War Drum Tower','Spirit Ward'),
    'Night Elf': ('Ancient Protector','Moonfire Spire','Moonwell Sentinel'),
    'Undead': ('Ziggurat Tower','Frost Tower','Soulwell Spire'),
}
_TOWER_TOOLTIPS = {
    'Human': (
        'A Human roadside watchtower. Its arrows deal 18 base damage to attackers.',
        'A Human bombardment tower. Heavy shots deal 70 base damage to attackers.',
        "A consecrated watchtower that shelters Aldric's defenders. Automatically restores 15 health to living allied heroes and troops within 650 range every 3 seconds. Does not heal buildings. Healing stops during boss tower suppression.",
    ),
    'Orc': (
        'An Orc lookout tower. Its attacks deal 18 base damage to approaching enemies.',
        'An Orc Redtusk heavy tower. Its crushing shots deal 70 base damage to attackers.',
        'Ancestral spirits shelter warriors beneath this ward. Automatically restores 15 health to living allied heroes and troops within 650 range every 3 seconds. Does not heal buildings. Healing stops during boss tower suppression.',
    ),
    'Night Elf': (
        'A Night Elf Ancient Protector guarding the woodland road. Its attacks deal 18 base damage.',
        'A Night Elf Moonfire Spire that lashes invaders for 70 base damage.',
        'Moonlit waters sustain the defenders of the glade. Automatically restores 15 health to living allied heroes and troops within 650 range every 3 seconds. Does not heal buildings. Healing stops during boss tower suppression.',
    ),
    'Undead': (
        'An Undead Ziggurat Tower guarding the approach. Its attacks deal 18 base damage.',
        'An Undead Frost Tower that strikes invaders for 70 base damage.',
        'Bound souls sustain the armies of the crown. Automatically restores 15 health to living allied heroes and troops within 650 range every 3 seconds. Does not heal buildings. Healing stops during boss tower suppression.',
    ),
}
_COMPANY_TOOLTIPS = {
    'Human': {
        'hall': 'Raise the Lion Banner to unlock your chosen hero’s personal company at the Barracks.',
        'foundry': 'Royal smiths grant company/support +20% health and base damage. Sells the Last King’s Oath pattern.',
        'siege_yard': 'The King’s engineers prepare the support unit chosen for your hero. This yard stocks only your own company.',
    },
    'Orc': {
        'hall': 'Beat the Redtusk war drums to unlock your chosen hero’s personal warband at the Barracks.',
        'foundry': 'The Ashen forge grants warband/support +20% health and base damage. Sells the Worldrend pattern.',
        'siege_yard': 'Orc war-drummers muster the support unit chosen for your hero. This lodge stocks only your own company.',
    },
    'Night Elf': {
        'hall': 'Gather Sentinels beneath the Moonlit Banners to unlock your chosen hero’s company at the Ancient of War.',
        'foundry': 'Moonbark runes grant company/support +20% health and base damage. Sells the Silvermoon Vigil pattern.',
        'siege_yard': 'The War Grove prepares the support unit chosen for your hero. Its stock belongs to you alone.',
    },
    'Undead': {
        'hall': 'Raise the bone standard to unlock your chosen hero’s graveguard company at the Crypt.',
        'foundry': 'Wraithforged arms grant company/support +20% health and base damage. Sells the Night’s Covenant pattern.',
        'siege_yard': 'The Graveyard of Arms musters the support unit chosen for your hero. This yard stocks only your own company.',
    },
}

FACTIONS = [
    {'race':'Human','worker':'hpea','town_hall':'htow','altar':'h000','altar_parent':'halt',
     'food':'hhou','barracks':'hbar','blacksmith':'hbla','arcane':'h004','arcane_parent':'hars',
     'towers':('h001','h002','h003'),'tower_parents':('hgtw','hctw','hatw')},
    {'race':'Orc','worker':'opeo','town_hall':'ogre','altar':'kA01','altar_parent':'oalt',
     'food':'otrb','barracks':'obar','blacksmith':'ofor','arcane':'kR01','arcane_parent':'osld',
     'towers':('kT10','kT11','kT12'),'tower_parents':('owtw','owtw','owtw')},
    {'race':'Night Elf','worker':'ewsp','town_hall':'etol','altar':'kA02','altar_parent':'eate',
     'food':'emow','barracks':'eaom','blacksmith':'edob','arcane':'kR02','arcane_parent':'eaoe',
     'towers':('kT20','kT21','kT22'),'tower_parents':('etrp','etrp','etrp')},
    {'race':'Undead','worker':'uaco','town_hall':'unpl','altar':'kA03','altar_parent':'uaod',
     'food':'uzig','barracks':'usep','blacksmith':'uslh','arcane':'kR03','arcane_parent':'utod',
     'towers':('kT30','kT31','kT32'),'tower_parents':('uzig','uzg2','uzig')},
]

for race_index, faction in enumerate(FACTIONS):
    hall_name, foundry_name, yard_name = _COMPANY_NAMES[faction['race']]
    faction['company_buildings'] = {
        'hall': {'rawcode':f'kH0{race_index}','parent':('hgra','obea','edob','utom')[race_index],
                 'name':hall_name,'tooltip':_COMPANY_TOOLTIPS[faction['race']]['hall']},
        'foundry': {'rawcode':f'kF0{race_index}','parent':('hbla','ofor','eaoe','uslh')[race_index],
                    'name':foundry_name,'tooltip':_COMPANY_TOOLTIPS[faction['race']]['foundry']},
        'siege_yard': {'rawcode':f'kY0{race_index}','parent':('harm','obar','eaow','usep')[race_index],
                       'name':yard_name,'tooltip':_COMPANY_TOOLTIPS[faction['race']]['siege_yard']},
    }
    for key, building in faction['company_buildings'].items():
        gold,lumber,build_time,hit_points = _COMPANY_COSTS[key]
        building.update(gold=gold,lumber=lumber,build_time=build_time,hit_points=hit_points)
    faction['company_buildings']['hall']['tooltip'] += ' Research three Company Chapters: each adds 5% base health/damage and 15% power potency. Chapters unlock through town recovery or waves 10/20/30.'
    faction['company_buildings']['foundry']['tooltip'] += ' Research three weapon ranks (+10% base damage each) and armor ranks (+10% base health and +2 armor each).'
    faction['company_buildings']['siege_yard']['tooltip'] += ' Research Counter-Siege Drill for +50% support attack damage against invading siege units and enemy structures.'
    faction['build_menu'] = [faction['town_hall'], faction['altar'], faction['food'],
        faction['barracks'], faction['blacksmith'], faction['arcane'], *faction['towers'],
        *[faction['company_buildings'][key]['rawcode'] for key in ('hall','foundry','siege_yard')]]
    for index, entry in enumerate(faction['company_buildings'].values()):
        entry['race'] = faction['race']
        entry['role'] = ('hall','foundry','siege_yard')[index]
        entry['build_time'] = _COMPANY_COSTS[entry['role']][2]

def faction_script():
    from equipment_catalog import item_catalog
    from recipes import recipe_catalog

    foundry_recipes = {recipe['race']: recipe['rawcode']
                       for recipe in recipe_catalog(item_catalog())
                       if recipe.get('race')}
    lines=['function KLS_FactionCatalogInit takes nothing returns nothing']
    for index, faction in enumerate(FACTIONS):
        for key, field in (('TownHall','town_hall'),('Worker','worker'),('Altar','altar'),
                           ('Barracks','barracks'),('Food','food'),('Blacksmith','blacksmith'),('Arcane','arcane')):
            lines.append(f"    set KLS_Faction{key}Id[{index}] = '{faction[field]}'")
        for index_tower, rawcode in enumerate(faction['towers']):
            lines.append(f"    set KLS_FactionTowerId[{index*3+index_tower}] = '{rawcode}'")
        for key in ('hall','foundry','siege_yard'):
            lines.append(f"    set KLS_Faction{key.title().replace('_','')}Id[{index}] = '{faction['company_buildings'][key]['rawcode']}'")
        lines.append(f"    set KLS_FactionFoundryRecipeId[{index}] = '{foundry_recipes[faction['race']]}'")
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
