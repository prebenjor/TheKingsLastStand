"""Installed-unit based army and building catalog for the 25 selectable heroes."""

COMPANY_BUILDINGS = {
    'hall': {
        'rawcode': 'kH00', 'parent': 'hcas', 'name': 'Hall of Banners',
        'gold': 240, 'lumber': 100, 'build_time': 35, 'hit_points': 1400,
        'tooltip': 'Raise your hero banner. Grants your company a personal doctrine aura and unlocks its Barracks recruit.',
    },
    'foundry': {
        'rawcode': 'kF00', 'parent': 'hbla', 'name': 'Royal Foundry',
        'gold': 360, 'lumber': 150, 'build_time': 45, 'hit_points': 1600,
        'tooltip': 'Forge veteran arms. Permanently grants your company and support troops +20% maximum health and +20% base damage.',
    },
    'siege_yard': {
        'rawcode': 'kY00', 'parent': 'harm', 'name': 'Siege Yard',
        'gold': 300, 'lumber': 125, 'build_time': 40, 'hit_points': 1500,
        'tooltip': 'Train your hero-matched tactical support unit. Stock is personal to this player.',
    },
}

# hero type, display name, company name/model, support name/model, doctrine,
# recruit gold/lumber/HP/damage, support gold/lumber/HP/damage.
_ROSTER = (
    ('Hpal','Paladin','Oathguard','hfoo','Dawn Chaplain','hmpr','AHad',260,70,900,34,320,100,650,22),
    ('Hmkg','Mountain King','Rune-Breakers','hfoo','Siege Sappers','hmtm','AOae',280,85,1000,40,360,120,680,28),
    ('H000','Priest','Dawnweavers','hmpr','Beacon Acolyte','hmpr','AHab',240,75,720,23,300,100,620,18),
    ('Hblm','Blood Mage','Emberguard','hsor','Phoenix Sentry','hgry','AHab',270,80,760,30,400,140,620,34),
    ('Obla','Blademaster','Windcutters','ogru','Shadow Scout','orai','AOae',270,80,850,38,340,110,650,30),
    ('Ofar','Far Seer','Stormcallers','oshm','Spirit Wolf','orai','AHab',260,85,750,25,350,120,700,33),
    ('Otch','Tauren Chieftain','Ancestral Guard','otau','War Drummer','okod','AOae',320,110,1250,44,360,130,850,25),
    ('Oshd','Shadow Hunter','Serpent Wardens','ohun','Field Witch Doctor','oshm','AHad',250,80,780,31,360,120,700,24),
    ('Edem','Demon Hunter','Felbreakers','esen','Warden Seeker','edry','AOae',280,90,850,38,360,120,720,30),
    ('Ekee','Keeper of the Grove','Thornwatch','edry','Grove Warden','etrp','AHad',250,90,760,25,380,130,800,28),
    ('Emoo','Priestess of the Moon','Moonstriders','esen','Starfall Ballista','ebal','AEar',270,85,780,35,420,150,700,38),
    ('Ewar','Warden','Gloomblades','esen','Shadow Trapwright','efdr','AOae',270,85,800,40,400,140,700,30),
    ('Udea','Death Knight','Graveguard','ugho','Bone Cavalier','uabo','AHad',280,90,900,36,430,150,1050,42),
    ('Ulic','Lich','Frostbound','ucry','Rime Mortar','uban','AHab',300,100,850,34,430,160,740,36),
    ('Nbrn','Dark Ranger','Black Arrow Company','nska','Forsaken Marksman','nfel','AEar',270,90,760,35,390,135,760,38),
    ('Hjsm','Ilastar, Human','Light’s Vanguard','hfoo','Mercy Bearer','hmpr','AHad',300,90,920,36,380,120,720,26),
    ('Npal','Forsaken Paladin','Argent Revenants','ugho','Cleansing Pyre','hmpr','AHad',310,100,1000,39,400,135,740,30),
)

from hero_catalog import NEW_HEROES, HERO_RACES
_ROSTER += tuple(
    (hero['unit_id'], hero['name'], hero['company'][0], hero['company'][1],
     hero['company'][2], hero['company'][3], hero['company'][12],
     *hero['company'][4:12])
    for hero in NEW_HEROES)

HERO_COMPANIES = [
    {
        'hero_type': hero_type, 'hero_name': hero_name,
        'company_id': f'kC{index:02d}', 'company_name': company_name,
        'company_parent': company_parent, 'company_gold': company_gold,
        'company_lumber': company_lumber, 'company_hp': company_hp,
        'company_damage': company_damage,
        'support_id': f'kS{index:02d}', 'support_name': support_name,
        'support_parent': support_parent, 'support_gold': support_gold,
        'support_lumber': support_lumber, 'support_hp': support_hp,
        'support_damage': support_damage, 'banner_ability': banner_ability,
        'banner_name': f'{hero_name} Banner',
        'race': HERO_RACES[index],
    }
    for index, (hero_type, hero_name, company_name, company_parent,
                support_name, support_parent, banner_ability, company_gold,
                company_lumber, company_hp, company_damage, support_gold,
                support_lumber, support_hp, support_damage) in enumerate(_ROSTER)
]


def company_script():
    from faction_catalog import faction_script
    lines = ['function KLS_CompanyCatalogInit takes nothing returns nothing']
    for index, entry in enumerate(HERO_COMPANIES):
        lines += [
            f"    set KLS_CompanyUnitId[{index}] = '{entry['company_id']}'",
            f"    set KLS_CompanySupportId[{index}] = '{entry['support_id']}'",
            f"    set KLS_CompanyBannerAbility[{index}] = '{entry['banner_ability']}'",
            f"    set KLS_CompanyUnitGold[{index}] = {entry['company_gold']}",
            f"    set KLS_CompanyUnitLumber[{index}] = {entry['company_lumber']}",
            f"    set KLS_CompanySupportGold[{index}] = {entry['support_gold']}",
            f"    set KLS_CompanySupportLumber[{index}] = {entry['support_lumber']}",
        ]
    lines += ['endfunction', faction_script()]
    return '\n'.join(lines)
