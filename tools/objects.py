"""Native object editor modifications, kept as source data for reproducible builds."""
import struct


def record(base, custom, fields):
    data = bytearray(base.encode() + custom.encode() + struct.pack('<I', len(fields)))
    for key, value in fields.items():
        typ = 3 if isinstance(value, str) else (2 if isinstance(value, float) else 0)
        data.extend(key.encode() + struct.pack('<I', typ))
        data.extend(value.encode()+b'\0' if typ == 3 else struct.pack('<f' if typ in (1,2) else '<i', value))
        data.extend(custom.encode())
    return bytes(data)


def table(original, custom):
    return struct.pack('<II', 2, len(original)) + b''.join(original) + struct.pack('<I', len(custom)) + b''.join(custom)


def units():
    # The Altar is placed for every player at match start, so it does not
    # consume a Peasant build-card slot. Replace the ordinary Workshop button
    # with its hero-specific Siege Yard child; retain twelve usable buttons.
    from faction_catalog import FACTIONS, _ALTAR_TOOLTIPS, _ARCANE_NAMES, _ARCANE_TOOLTIPS, _TOWER_NAMES, _TOWER_TOOLTIPS
    from hero_progression import HERO_ABILITIES
    # Keep each hero's native learn list limited to its four normal skills.
    # Repeatable primary-stat choices are provided by owner-local UI buttons
    # and consume the same hero skill point without becoming ranked abilities.
    def learned_hero_skills(hero_id):
        return ','.join(dict.fromkeys(HERO_ABILITIES[hero_id]))
    from hero_catalog import NEW_HEROES, HERO_BASE_HP_OVERRIDES, HERO_TYPES, HERO_PARENT_TYPES
    from hero_progression import _slk, ROOT
    from signature_spells import spell_id
    native_unit_abilities = _slk(ROOT / 'tools/reference/installed/UnitAbilities.slk')
    native_normal_column = next(k for k, v in native_unit_abilities[1].items() if v == 'abilList')
    native_normal = {row.get(1): row.get(native_normal_column, '')
                     for row in native_unit_abilities.values() if row.get(1)}
    signature_indices = {hero_id: i for i, hero_id in enumerate(HERO_TYPES)}
    signature_indices.update({h['unit_id']: h['signature_index'] for h in NEW_HEROES})
    def normal_hero_skills(hero_id, parent):
        return ','.join(dict.fromkeys(
            [a for a in native_normal[parent].split(',') if a not in ('', '_', '-')]
            + [spell_id(signature_indices[hero_id])]))
    zero_hero_growth = {'ustp':0.0,'uinp':0.0,'uagp':0.0}
    original = [record(faction['worker'], '\0\0\0\0', {
        'ubui':','.join(faction['build_menu']), 'ureq':''}) for faction in FACTIONS]
    # Each race builds a custom altar child rather than Warcraft's stock altar.
    # Native tier-two town halls still require the stock altar rawcode, which
    # makes the displayed Altar of Kings requirement impossible to satisfy.
    # Point each upgrade target at the matching altar and race core buildings.
    town_hall_upgrade_requirements = (
        ('hcas', 'hbar', 'hbla', 'h000'),
        ('ostr', 'obar', 'ofor', 'kA01'),
        # Night Elf Tier Two core upgrades must use Tier One buildings. The
        # former Ancient of Wind/Lore requirements both require Tree of Ages.
        ('etoa', 'eaom', 'edob', 'kA02'),
        ('unp1', 'usep', 'uslh', 'kA03'),
    )
    original.extend(record(town_hall, '\0\0\0\0', {
        'ureq': ','.join((barracks, blacksmith, altar))})
        for town_hall, barracks, blacksmith, altar in town_hall_upgrade_requirements)
    custom_hero_ids = {entry['unit_id'] for entry in NEW_HEROES} | {'H000'}
    for hero_id, abilities in HERO_ABILITIES.items():
        if hero_id not in custom_hero_ids:
            original.append(record(hero_id, '\0\0\0\0', {
                'uhab': learned_hero_skills(hero_id), 'uhas': learned_hero_skills(hero_id),
                'uabi': normal_hero_skills(hero_id, HERO_PARENT_TYPES[hero_id]),
                'uabs': normal_hero_skills(hero_id, HERO_PARENT_TYPES[hero_id]), **zero_hero_growth}))
    custom = [
        record('ndmg', 'kInv', {'unam':'Northern Summoning Gate','uabi':'Avul','utra':'','ureq':'','uaen':0,'utub':'An impenetrable summoning gate. Enemy waves emerge from its southern forecourt.'}),
        record('Hamg', 'H000', {'unam':'Priest','uhab':learned_hero_skills('H000'),'uhas':learned_hero_skills('H000'),'uabi':normal_hero_skills('H000','Hamg'),'uabs':normal_hero_skills('H000','Hamg'),'ureq':'','uhpm':HERO_BASE_HP_OVERRIDES['H000'],**zero_hero_growth}),
        record('Hvwd', 'H001', {'unam':'Ranger','uhab':'ANba,ANsi,ANdr,ANch','ureq':''}),
        record('halt', 'h000', {'unam':'Altar of Kings','utip':'Build Altar of Kings','utub':_ALTAR_TOOLTIPS['Human']+' Only one hero per player.','utra':'','ures':'','urev':0,'ureq':'','ugol':160,'ulum':70,'ubld':30,'uhpm':900}),
        record('hars', 'h004', {'unam':'Arcane Sanctum','utip':'Build Arcane Sanctum','utub':_ARCANE_TOOLTIPS['Human'],'utra':'hmpr,hsor','ures':'Rhpt,Rhst','ureq':'','ugol':160,'ulum':70,'ubld':30}),
        record('hgtw', 'h001', {'unam':_TOWER_NAMES['Human'][0],'utip':_TOWER_NAMES['Human'][0],'utub':_TOWER_TOOLTIPS['Human'][0],'ureq':'','uupt':'','ua1b':18,'ugol':140,'ulum':50,'ubld':25,'uhpm':650}),
        record('hctw', 'h002', {'unam':_TOWER_NAMES['Human'][1],'utip':_TOWER_NAMES['Human'][1],'utub':_TOWER_TOOLTIPS['Human'][1],'ureq':'','uupt':'','ua1b':70,'ugol':260,'ulum':100,'ubld':35,'uhpm':850}),
        record('hatw', 'h003', {'unam':_TOWER_NAMES['Human'][2],'utip':_TOWER_NAMES['Human'][2],'utub':_TOWER_TOOLTIPS['Human'][2],'ureq':'','uupt':'','ua1b':14,'ugol':220,'ulum':100,'ubld':30,'uhpm':750}),
    ]
    from forest_catalog import CAMPS
    for i, camp in enumerate(CAMPS):
        for prefix, base, name in (('L', camp['leader'], camp['name']+' Guardian'),
                                   ('M', camp['guard'], camp['name']+' Defender')):
            fields = {'unam':name, 'ureq':'', 'ubba':0, 'ubdi':0, 'ubsi':0}
            if prefix == 'L':
                fields.update({'uhpm':(900,1200,1600,2200)[i], 'ua1b':(20,26,35,45)[i],
                               'utub':'Defeat this camp leader for personal '+('Common' if camp['quality']==0 else 'Uncommon')+' equipment and healing supplies.'})
            custom.append(record(base,f'k{prefix}{i:02d}',fields))
    for rank in range(1, 11):
        health, damage = ((300,15),(450,22),(600,30))[rank-1] if rank <= 3 else (round(600*(1+.1*(rank-3))),round(30*(1+.1*(rank-3))))
        from hero_progression import briar_unit_id
        custom.append(record('efon',briar_unit_id(rank),{'unam':'Briar Host Treant','uhpm':health,'ua1b':damage,'ua1d':0,'ua1s':0,'ureq':''}))
    custom.append(record('hbew','kCar',{'unam':'Northwatch Supply Caravan','uabi':'','uhpm':1800,'umvt':'foot','umvs':140,'uaen':0,'upat':'','ucol':32.0,'ufoo':0}))
    from town_catalog import TOWNS, QUEST_RAWCODES
    for town in TOWNS:
        custom.append(record(town['worker'],QUEST_RAWCODES[town['quest_id']],{
            'unam':town['quest'],'utip':town['quest'],'utub':'Optional shared Crownlands story objective. Select during a wave to begin or contribute; objectives never pause the defense.','ureq':'','uabi':'Avul','uhpm':500,
        }))
    for hero in NEW_HEROES:
        custom.append(record(hero['base'], hero['unit_id'], {
            'unam':hero['name'], 'upro':hero['name'],
            'uabi':normal_hero_skills(hero['unit_id'], hero['base']),
            'uabs':normal_hero_skills(hero['unit_id'], hero['base']),
            'uhas':learned_hero_skills(hero['unit_id']),
            'uhab':learned_hero_skills(hero['unit_id']), 'ureq':'', **zero_hero_growth,
        }))
    from company_catalog import HERO_COMPANIES
    for faction in FACTIONS:
        race = faction['race']
        if faction['arcane'] != 'h004':
            name = _ARCANE_NAMES[FACTIONS.index(faction)]
            arcane_fields = {
                'unam':name,'utip':name,'utub':_ARCANE_TOOLTIPS[race],
                'ugol':160,'ulum':70,'ubld':30,'uhpm':1100,'ureq':'',
            }
            if race == 'Undead':
                # The custom Temple inherited the Meat Wagon command icon in
                # Warcraft III despite using utod as its object-data parent.
                arcane_fields['uico'] = r'ReplaceableTextures\CommandButtons\BTNTempleOfTheDamned.dds'
            custom.append(record(faction['arcane_parent'],faction['arcane'],arcane_fields))
        for tower_index, rawcode in enumerate(faction['towers']):
            if faction['race'] == 'Human':
                continue
            name = _TOWER_NAMES[race][tower_index]
            gold,lumber,build_time,hit_points,damage = ((140,50,25,650,18),(260,100,35,850,70),(220,100,30,750,14))[tower_index]
            custom.append(record(faction['tower_parents'][tower_index],rawcode,{
                'unam':name,'utip':name,'utub':_TOWER_TOOLTIPS[race][tower_index],
                'ugol':gold,'ulum':lumber,'ubld':build_time,'uhpm':hit_points,'ua1b':damage,
                'ureq':'',
            }))
        for role, entry in faction['company_buildings'].items():
            fields = {
                'unam':entry['name'], 'utip':'Build '+entry['name'],
                'utub':entry['tooltip'], 'ugol':entry['gold'],
                'ulum':entry['lumber'], 'ubld':entry['build_time'],
                'uhpm':entry['hit_points'], 'ureq':faction['barracks'], 'ures':'', 'urev':0,
                'uabi':'', 'utra':'', 'uupt':'',
            }
            if role in ('hall','foundry','siege_yard'):
                fields['uabi'] = 'Aneu,Apit,Asid,Asud'
            custom.append(record(entry['parent'],entry['rawcode'],fields))
        if faction['race'] != 'Human':
            custom.append(record(faction['altar_parent'],faction['altar'],{
                'unam':race+' Hero Shrine','utip':'Build '+race+' Hero Shrine',
                'utub':_ALTAR_TOOLTIPS[race]+' Only one hero per player.',
                'ureq':'','utra':'','ures':'','urev':0,'ugol':160,'ulum':70,'ubld':30,'uhpm':900,
            }))
    for entry in HERO_COMPANIES:
        company_fields = {
            'unam':entry['company_name'], 'utip':entry['company_name'],
            'utub':entry['hero_name']+' company recruit. Trained only from your Barracks after you raise this hero banner.',
            'ugol':entry['company_gold'], 'ulum':entry['company_lumber'],
            'uhpm':entry['company_hp'], 'ua1b':entry['company_damage'], 'ureq':'',
            'uabi':entry['company_ability'], 'upgr':'', 'umpm':180,'umpi':180,'umpr':1.0,
        }
        support_fields = {
            'unam':entry['support_name'], 'utip':entry['support_name'],
            'utub':entry['hero_name']+' tactical support. Trained only at your personal Siege Yard.',
            'ugol':entry['support_gold'], 'ulum':entry['support_lumber'],
            'uhpm':entry['support_hp'], 'ua1b':entry['support_damage'], 'ureq':'',
            'uabi':entry['support_ability'], 'upgr':'', 'umpm':180,'umpi':180,'umpr':1.0,
        }
        custom.append(record(entry['company_parent'],entry['company_id'],company_fields))
        custom.append(record(entry['support_parent'],entry['support_id'],support_fields))
    custom.append(record('ngme','hS00',{'unam':'Kingdom Merchant','usei':'','umki':'','uabi':'Avul,Aneu,Apit,Asid,Asud','utub':'Select to browse equipment. Bring your hero within 700 range to buy.'}))
    custom.append(record('hars','hS02',{'unam':"Sage's Archive",'utip':"Sage's Archive",'utub':'A quiet shop for permanent Strength, Agility and Intelligence tomes. Select your hero before buying.','uabi':'Avul,Aneu,Apit,Asid,Asud','usei':'','umki':''}))
    custom.append(record('hcas','hC01',{"unam":"King Aldric's Castle",'uabi':'Avul,Aneu,Apit,Asid,Asud','usei':'','umki':''}))
    custom.append(record('hpea','hS01',{'unam':'Frost effect','uabi':'Aloc,ASl0','umdl':'','umvs':0,'ucol':0.0,'umpm':100,'umpi':100,'ufoo':0}))
    return table(original, custom)


from equipment_catalog import color_rarity_text, item_catalog

def items():
    from equipment_catalog import attribute_books
    from recipes import recipe_catalog

    # Use the installed generic Backpack identity, not Anya's campaign-specific
    # `ebua` variant. Keep the native 30-slot inventory and grant the equipment
    # panel/stat details needed by this co-op map through its item abilities.
    original = [record('ebac','\0\0\0\0',{'unam':'Backpack','utip':'Backpack','utub':'Native Forsaken Kingdom Backpack: 30 storage slots and nine equipment slots. Keep this Backpack in your hero inventory.','iabi':'AIni,AEqu,ASde','iequ':0,'iusa':1,'iper':0,'iuse':0,'idro':0,'ipaw':0,'isel':0,'iprn':0,'igol':0,'isto':1})]
    custom = []
    for entry in item_catalog():
        display_name=entry['colored_name']
        fields={'unam':display_name,'utip':display_name,
                'icla':'Equipment','igol':entry['price'],'iper':0,'iabi':entry['abilities'],'utub':entry['description'],'iusa':0,'ilev':1,'ilvo':1,'ilum':0,'iuse':0,
                # Native backpack dragging between storage, the normal hero
                # inventory, and equipment requires the item to be droppable.
                # Pawnability separately enables vendor buyback.
                'idro':1,'ipaw':1,'isel':1}
        custom.append(record(entry['parent'],entry['rawcode'],fields))
    for book in attribute_books():
        fields={'icla':'Power-ups','unam':book['name'],'utip':book['name'],
                'utub':book['description'],'igol':book['price'],'iabi':'',
                'iequ':0,'iusa':0,'iper':0,'iuse':0,'idro':0,'ipaw':0,'isel':1,'isto':99,'istr':0,'isst':0}
        custom.append(record(book['parent'],book['rawcode'],fields))
    for recipe in recipe_catalog(item_catalog()):
        fields={'icla':'Power-ups','unam':'Forge Recipe: '+recipe['name'],
                'utip':'Forge Recipe: '+recipe['name'],'utub':recipe['description'],
                'igol':recipe['price'],'iabi':'','iequ':0,'iusa':0,'iper':0,
                'iuse':0,'idro':0,'ipaw':0,'isel':1}
        custom.append(record('arsc',recipe['rawcode'],fields))
    from company_catalog import company_research_catalog
    for research in company_research_catalog():
        custom.append(record('ckng',research['rawcode'],{
            'icla':'Miscellaneous','unam':research['name'],'utip':research['name'],
            'utub':research['description'],'igol':research['gold'],'ilum':research['lumber'],
            'iabi':'','iequ':0,'iusa':0,'iper':0,'iuse':0,'idro':0,'ipaw':0,'isel':0,
        }))
    controls=[record('phea','KHE1',{'icla':'Miscellaneous','unam':'Heal King Aldric','utip':'Heal King Aldric','utub':'Restore up to 2,000 King Aldric health. Costs 150 gold and 50 lumber. Available again after one second. If he is at full health, the cost is refunded.','igol':150,'ilum':50,'iequ':0,'iusa':0,'iper':0,'idro':0,'ipaw':0,'isel':0,'isto':1,'istr':1,'isst':0})]
    for tier in range(5):
        raw='KUP'+str(tier+1)
        cost=400+200*tier
        controls.append(record('ckng',raw,{'icla':'Miscellaneous','unam':'Royal Defense Upgrade - Tier '+str(tier+1),'utip':'Royal Defense Upgrade - Tier '+str(tier+1),'utub':'Upgrade King Aldric: +4,000 maximum/current health and +30 damage. Tier '+str(tier+1)+' costs '+str(cost)+' gold and 150 lumber.','igol':cost,'ilum':150,'iequ':0,'iusa':0,'iper':0,'idro':0,'ipaw':0,'isel':0}))
    custom.extend(controls+[
        record('ratf','I010',{'icla':'Equipment','unam':color_rarity_text('Uncommon','Gravetide Cleaver'),'utip':color_rarity_text('Uncommon','Gravetide Cleaver'),'utub':color_rarity_text('Uncommon','Uncommon')+' boss relic. Chapter I: +15 damage.','iequ':6,'igol':0,'ipaw':0,'isel':0,'idro':1}),
        record('rhth','I011',{'icla':'Equipment','unam':color_rarity_text('Rare','Heart of the Watch'),'utip':color_rarity_text('Rare','Heart of the Watch'),'utub':color_rarity_text('Rare','Rare')+' boss relic. Chapter II: increases maximum health.','iequ':2,'igol':0,'ipaw':0,'isel':0,'idro':1}),
        record('lgdh','I012',{'icla':'Equipment','unam':color_rarity_text('Epic','Crown of Dawn'),'utip':color_rarity_text('Epic','Crown of Dawn'),'utub':color_rarity_text('Epic','Epic')+' boss relic. Chapter III: grants a healing aura.','iequ':8,'igol':0,'ipaw':0,'isel':0,'idro':1}),
        record('ckng','I013',{'icla':'Equipment','unam':color_rarity_text('Legendary','Oath of the Last King'),'utip':color_rarity_text('Legendary','Oath of the Last King'),'utub':color_rarity_text('Legendary','Legendary')+' boss relic. Chapter IV: +5 to all attributes.','iequ':5,'igol':0,'ipaw':0,'isel':0,'idro':1}),
    ])
    return table(original, custom)
