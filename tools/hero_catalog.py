"""User-authored hero additions and the player-race identity for all heroes."""

HERO_COUNT = 25
RACES = ('Human', 'Orc', 'Night Elf', 'Undead')
_RACE_INDEX = {name: index for index, name in enumerate(RACES)}

_BASE_HERO_RACES = {
    'Hpal': 'Human', 'Hmkg': 'Human', 'H000': 'Human', 'Hblm': 'Human',
    'Obla': 'Orc', 'Ofar': 'Orc', 'Otch': 'Orc', 'Oshd': 'Orc',
    'Edem': 'Night Elf', 'Ekee': 'Night Elf', 'Emoo': 'Night Elf', 'Ewar': 'Night Elf',
    'Udea': 'Undead', 'Ulic': 'Undead', 'Nbrn': 'Undead',
    'Hjsm': 'Human', 'Npal': 'Undead',
}

# The native hero parents supply installed models, portraits, animations, and
# four safe Warcraft skills. Each addition receives its own generated company
# and signature ability below.
NEW_HEROES = [
    {'unit_id':'Havl','name':'Aveline Ashford','race':'Human','base':'Hpal',
     'description':'Banner defender: protects allies and turns a rally into a counterattack.',
     'abilities':('AHhb','AHds','AHad','AHre'),
     'signature':('Crownward Rally','HolyBolt',100,250,80,0,0,0,'Aveline plants the crown banner, striking nearby foes and renewing every nearby defender.'),
     'company':('Lionguard','hfoo','Banner Chaplain','hmpr',290,80,980,36,340,110,700,24,'AHad')},
    {'unit_id':'Htor','name':'Toren Flintlock','race':'Human','base':'Hmkg',
     'description':'Siege artificer: disrupts clustered attackers and empowers his company.',
     'abilities':('AHtb','AHtc','AHbh','AHav'),
     'signature':('Flintlock Barrage','ThunderClap',320,0,0,0,0,1,'Toren detonates a controlled shell burst that damages and slows attackers around the impact.'),
     'company':('Powderwrights','hmtm','Field Engineer','hmpr',300,100,900,42,380,140,680,32,'AHad')},
    {'unit_id':'Okrg','name':'Korgal Redtusk','race':'Orc','base':'Otch',
     'description':'Cleaving frontline: breaks the enemy line with heavy area attacks.',
     'abilities':('AOsh','AOws','AOae','AOre'),
     'signature':('Redtusk Earthshatter','WarStomp',380,0,0,0,0,2,'Korgal smashes the ground, crushing nearby enemies and restoring his own vitality.'),
     'company':('Redtusk Breakers','otau','Bloodfire Drummer','oshm',340,120,1320,48,390,140,900,30,'AOae')},
    {'unit_id':'Omor','name':'Morgra Ashcaller','race':'Orc','base':'Oshd',
     'description':'Spirit caster: drains enemy power and calls ancestral wolves to the fight.',
     'abilities':('AOhw','AOhx','AOsw','AOvd'),
     'signature':('Ashen Spiritpack','SpiritWolf',180,0,60,'osw1',3,0,'Morgra calls three ash spirits to hunt down the invasion around the target point.'),
     'company':('Ashcallers','oshm','Spirit Guide','orai',290,95,820,34,390,140,760,28,'AOae')},
    {'unit_id':'Esly','name':'Selyra Moonlance','race':'Night Elf','base':'Emoo',
     'description':'Precision huntress: marks a target zone for a focused moonlit volley.',
     'abilities':('AEst','AHfa','AEar','AEsf'),
     'signature':('Moonlance Volley','Starfall',300,0,0,0,0,0,'Selyra focuses a volley of moonfire on enemies near the target point.'),
     'company':('Moonlance Sentinels','esen','Moonwell Keeper','edry',300,100,900,40,430,150,780,34,'AEar')},
    {'unit_id':'Efal','name':'Faelor Briarward','race':'Night Elf','base':'Ekee',
     'description':'Thorn-control sentinel: roots threats and summons treants without needing nearby trees.',
     'abilities':('AEer','AEfn','AEah','AEtq'),
     'signature':('Briarward Stand','ForceOfNature',180,100,40,'efon',3,0,'Faelor calls three treants from the land itself; no nearby trees are needed.'),
     'company':('Briarward Guard','edry','Thornmender','etrp',280,100,850,31,410,145,840,29,'AEar')},
    {'unit_id':'Uvyr','name':'Veyra Wraithveil','race':'Undead','base':'Nbrn',
     'description':'Curse banshee: silences a cluster of invaders and siphons their strength.',
     'abilities':('ANsi','ANba','ANdr','ANch'),
     'signature':('Wraithveil Curse','FanOfKnives',260,0,0,0,0,3,'Veyra tears through nearby enemies and draws up to 40 mana from each into herself.'),
     'company':('Veilbound Wraiths','uban','Grave Cantor','ucry',300,100,820,38,420,160,780,40,'AUau')},
    {'unit_id':'Utha','name':'Tharos Bonecrown','race':'Undead','base':'Udea',
     'description':'Gravewarden: holds the line with durable bone guards summoned from the dead.',
     'abilities':('AUdc','AUdp','AUau','AUan'),
     'signature':('Bonecrown Guard','DeathCoil',120,80,0,'uske',3,0,'Tharos raises three bone guards to protect the road and assault the nearest attackers.'),
     'company':('Bonecrown Wardens','ugho','Crypt Acolyte','ucry',330,110,1150,46,430,160,1050,39,'AUau')},
]
for _signature_offset, _hero in enumerate(NEW_HEROES, start=HERO_COUNT-len(NEW_HEROES)):
    _hero['signature_index'] = _signature_offset

HERO_RACES = [_BASE_HERO_RACES[kind] for kind in (
    'Hpal','Hmkg','H000','Hblm','Obla','Ofar','Otch','Oshd','Edem','Ekee',
    'Emoo','Ewar','Udea','Ulic','Nbrn','Hjsm','Npal')]
HERO_RACES.extend(entry['race'] for entry in NEW_HEROES)

def hero_selection_script():
    """Emit catalog statements into the existing selector initializer."""
    lines = []
    for index, race in enumerate(HERO_RACES):
        lines.append(f'    set KLS_HeroRace[{index}] = {_RACE_INDEX[race]}')
    for offset, hero in enumerate(NEW_HEROES, start=HERO_COUNT-len(NEW_HEROES)):
        lines += [
            f"    set KLS_HeroType[{offset}] = '{hero['unit_id']}'",
            f"    set KLS_HeroName[{offset}] = \"{hero['name']}\"",
            f"    set KLS_HeroDescription[{offset}] = \"{hero['description']}\"",
        ]
    return '\n'.join(lines)

def faction_index(race):
    return _RACE_INDEX[race]
