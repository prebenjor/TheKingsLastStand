"""Installed-unit based army and building catalog for the 25 selectable heroes."""

COMPANY_BUILDINGS = {
    'hall': {
        'rawcode': 'kH00', 'parent': 'hgra', 'name': 'Hall of Banners',
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
    ('Ekee','Keeper of the Grove','Thornwatch','edry','Grove Warden','edry','AHad',250,90,760,25,380,130,800,28),
    ('Emoo','Priestess of the Moon','Moonstriders','esen','Starfall Ballista','ebal','AEar',270,85,780,35,420,150,700,38),
    ('Ewar','Warden','Gloomblades','esen','Shadow Trapwright','efdr','AOae',270,85,800,40,400,140,700,30),
    ('Udea','Death Knight','Graveguard','ugho','Bone Cavalier','uabo','AHad',280,90,900,36,430,150,1050,42),
    ('Ulic','Lich','Frostbound','ucry','Rime Mortar','uban','AHab',300,100,850,34,430,160,740,36),
    ('Nbrn','Dark Ranger','Black Arrow Company','nska','Forsaken Marksman','nska','AEar',270,90,760,35,390,135,760,38),
    ('Hjsm','Ilastar, Human','Light’s Vanguard','hfoo','Mercy Bearer','hmpr','AHad',300,90,920,36,380,120,720,26),
    ('Npal','Forsaken Paladin','Argent Revenants','ugho','Cleansing Pyre','uban','AHad',310,100,1000,39,400,135,740,30),
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


# Native Channel supplies point targeting; every authored effect is handled by
# synchronized company runtime and works against living and undead targets.
_COMPANY_POWERS = (
 ('Dawn Ward',80,80,0,False), ('Rune Impact',140,0,0,True),
 ('Dawn Renewal',30,140,30,False), ('Emberburst',160,0,0,False),
 ('Windcut',150,0,0,False), ('Stormcall',120,0,30,True),
 ('Ancestor Pulse',90,100,0,False), ('Serpent Venom',130,0,0,True),
 ('Fel Rupture',150,0,0,False), ('Verdant Ward',60,120,0,False),
 ('Moon Volley',150,0,0,False), ('Gloomstrike',150,0,0,True),
 ('Grave Covenant',90,100,0,False), ('Rime Burst',130,0,0,True),
 ('Black Volley',150,0,0,False), ('Mercy Flare',70,120,30,False),
 ('Cleansing Brand',120,80,0,False), ('Crownward Pulse',80,120,0,False),
 ('Powderburst',160,0,0,True), ('Bloodfire Break',160,0,0,False),
 ('Ashen Communion',80,100,30,False), ('Moonlance Salvo',160,0,0,False),
 ('Briar Renewal',80,120,0,True), ('Veil Dirge',100,80,30,False),
 ('Boneward Pulse',100,100,0,False),
)
for index, entry in enumerate(HERO_COMPANIES):
    name,damage,heal,mana,slow = _COMPANY_POWERS[index]
    entry['company_ability'] = f'Kc{index:02d}'
    entry['support_ability'] = f'Ks{index:02d}'
    entry['powers'] = (
        dict(name=name,damage=damage,heal=heal,mana=mana,slow=slow),
        dict(name=entry['support_name']+' Accord',damage=damage//2,
             heal=max(120,heal),mana=max(20,mana),slow=slow),
    )


def company_research_catalog():
    entries=[]
    for branch,prefix,role,branch_id in [('chapter','KC','hall',0),
                                        ('weapon','KW','foundry',1),
                                        ('armor','KA','foundry',2)]:
        for rank in range(1,4):
            gold,lumber=(350,100) if rank==1 else ((700,200) if rank==2 else (1400,350))
            effect={'chapter':'+5% base health and damage; +15% company ability potency',
                    'weapon':'+10% base damage', 'armor':'+10% base health and +2 armor'}[branch]
            entries.append(dict(rawcode=f'{prefix}{rank:02d}',branch=branch,branch_id=branch_id,
                                role=role,rank=rank,gold=gold,lumber=lumber,
                                name=branch.title()+' Research '+str(rank),
                                description=effect+'. Applies to existing and future company/support recruits. '+
                                (f'Unlock: story chapter {rank} or wave {rank*10}.' if branch=='chapter' else 'Requires the previous rank.')))
    for code,branch,role,branch_id,effect in [
        ('KS01','counter_siege','siege_yard',3,'Support attacks deal 50% extra damage to Meat Wagons, Blood Elf Siege Wagons, Dragon Turtles and enemy structures.'),
        ('KT01','arcane','arcane',4,'Support active abilities gain 25% damage, healing and mana restoration.')]:
        entries.append(dict(rawcode=code,branch=branch,branch_id=branch_id,role=role,rank=1,
                            gold=650,lumber=200,name=branch.replace('_',' ').title()+' Research',
                            description=effect+' Applies only to your company support units.'))
    return entries


def company_spell_records(ability):
    from signature_spells import SIGNATURES
    records=[]
    for index,entry in enumerate(HERO_COMPANIES):
        for role,power in enumerate(entry['powers']):
            code=entry['support_ability'] if role else entry['company_ability']
            description=(f"Deals {power['damage']} damage to enemies; restores {power['heal']} HP and {power['mana']} mana to friendly troops in a 250 radius. "
                         + ('Slows enemies by 20% for 2 seconds. ' if power['slow'] else '')
                         + 'Works for all races. Does not restore King Aldric or structures. 40 mana; 20-second cooldown. Chapter and Arcane research increase potency.')
            records.append(ability('ANcl',code,[
                ('anam',3,0,0,power['name']),('aher',0,0,0,0),('alev',0,0,0,1),('areq',3,0,0,''),
                ('aart',3,0,0,'ReplaceableTextures\\CommandButtons\\BTN'+SIGNATURES[index][1]+'.dds'),
                ('abpx',0,0,0,0),('abpy',0,0,0,2),('ahky',3,0,0,'Q'),
                ('atp1',3,1,0,power['name']+' (Q)'),('aub1',3,1,0,description),
                ('amcs',0,1,0,40),('acdn',2,1,0,20.0),('aran',2,1,0,600.0),
                ('Ncl1',2,1,1,0.0),('Ncl2',0,1,2,2),('Ncl3',0,1,3,1),
                ('Ncl4',2,1,4,0.0),('Ncl5',0,1,5,0),('Ncl6',3,1,6,'channel')]))
    return records


def company_script():
    from faction_catalog import faction_script
    lines = ['function KLS_CompanyCatalogInit takes nothing returns nothing']
    for index, entry in enumerate(HERO_COMPANIES):
        lines += [
            f"    set KLS_CompanyUnitHP[{index}] = {entry['company_hp']}",
            f"    set KLS_CompanySupportHP[{index}] = {entry['support_hp']}",
            f"    set KLS_CompanyUnitDamage[{index}] = {entry['company_damage']}",
            f"    set KLS_CompanySupportDamage[{index}] = {entry['support_damage']}",
            f"    set KLS_CompanyUnitId[{index}] = '{entry['company_id']}'",
            f"    set KLS_CompanySupportId[{index}] = '{entry['support_id']}'",
            f"    set KLS_CompanyBannerAbility[{index}] = '{entry['banner_ability']}'",
            f"    set KLS_CompanyUnitGold[{index}] = {entry['company_gold']}",
            f"    set KLS_CompanyUnitLumber[{index}] = {entry['company_lumber']}",
            f"    set KLS_CompanySupportGold[{index}] = {entry['support_gold']}",
            f"    set KLS_CompanySupportLumber[{index}] = {entry['support_lumber']}",
        ]
    for index,entry in enumerate(HERO_COMPANIES):
        for role,power in enumerate(entry['powers']):
            key=index*2+role
            code=entry['support_ability'] if role else entry['company_ability']
            lines += [f"    set KLS_CompanyPowerId[{key}] = '{code}'",
                      f"    set KLS_CompanyPowerDamage[{key}] = {power['damage']}",
                      f"    set KLS_CompanyPowerHeal[{key}] = {power['heal']}",
                      f"    set KLS_CompanyPowerMana[{key}] = {power['mana']}",
                      f"    set KLS_CompanyPowerSlow[{key}] = {str(power['slow']).lower()}"]
    for index,entry in enumerate(company_research_catalog()):
        role_id={'hall':0,'foundry':1,'siege_yard':2,'arcane':3}[entry['role']]
        lines += [f"    set KLS_CompanyResearchId[{index}] = '{entry['rawcode']}'",
                  f"    set KLS_CompanyResearchRole[{index}] = {role_id}",
                  f"    set KLS_CompanyResearchBranch[{index}] = {entry['branch_id']}",
                  f"    set KLS_CompanyResearchLevel[{index}] = {entry['rank']}",
                  f"    set KLS_CompanyResearchGold[{index}] = {entry['gold']}",
                  f"    set KLS_CompanyResearchLumber[{index}] = {entry['lumber']}"]
    from wave_rosters import SIEGE_UNIT_CODES
    lines += ['endfunction', faction_script(),
              'function KLS_IsSiegeInvader takes integer rawcode returns boolean',
              '    return ' + ' or '.join("rawcode == '"+code+"'" for code in SIEGE_UNIT_CODES),
              'endfunction']
    return '\n'.join(lines)
