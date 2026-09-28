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
    from faction_catalog import FACTIONS
    original = [record(faction['worker'], '\0\0\0\0', {
        'ubui':','.join(faction['build_menu']), 'ureq':''}) for faction in FACTIONS]
    custom = [
        record('Hamg', 'H000', {'unam':'Priest','uhab':'AHhb,AHab,AHds,AHre','ureq':'','uhpm':600}),
        record('Hvwd', 'H001', {'unam':'Ranger','uhab':'ANba,ANsi,ANdr,ANch','ureq':''}),
        record('halt', 'h000', {'unam':'Altar of Kings','utip':'Build Altar of Kings','utub':'Select this altar to choose your hero before your choice is locked. Fallen heroes return here automatically after 20 seconds. Only one hero per player.','utra':'','ures':'','urev':0,'ureq':'','ugol':160,'ulum':70,'ubld':30,'uhpm':900}),
        record('hars', 'h004', {'unam':'Arcane Sanctum','utip':'Build Arcane Sanctum','utub':'Trains Priests for healing and Sorceresses for battlefield control. Provides Priest and Sorceress training upgrades.','utra':'hmpr,hsor','ures':'Rhpt,Rhst','ureq':'','ugol':160,'ulum':70,'ubld':30}),
        record('hgtw', 'h001', {'unam':'Watchtower','ureq':'','uupt':'','ua1b':18,'ugol':140,'ulum':50,'ubld':25,'uhpm':650}),
        record('hctw', 'h002', {'unam':'Bombard Tower','ureq':'','uupt':'','ua1b':70,'ugol':260,'ulum':100,'ubld':35,'uhpm':850}),
        record('hatw', 'h003', {'unam':'Sanctuary Tower','utub':'Restores 15 health to nearby allied units every 3 seconds. Range 650.','ureq':'','uupt':'','ua1b':14,'ugol':220,'ulum':100,'ubld':30,'uhpm':750}),
    ]
    from town_catalog import TOWNS, QUEST_RAWCODES
    for town in TOWNS:
        custom.append(record(town['worker'],QUEST_RAWCODES[town['quest_id']],{
            'unam':town['quest'],'utip':town['quest'],'utub':'Optional shared Crownlands story objective. Select during a wave to begin or contribute; objectives never pause the defense.','ureq':'','uabi':'Avul','uhpm':500,
        }))
    from hero_catalog import NEW_HEROES
    for hero in NEW_HEROES:
        custom.append(record(hero['base'], hero['unit_id'], {
            'unam':hero['name'], 'upro':hero['name'],
            'uhab':','.join(hero['abilities']), 'ureq':'',
        }))
    from company_catalog import HERO_COMPANIES
    from faction_catalog import _ARCANE_NAMES, _TOWER_NAMES
    for faction in FACTIONS:
        race = faction['race']
        if faction['arcane'] != 'h004':
            name = _ARCANE_NAMES[FACTIONS.index(faction)]
            custom.append(record(faction['arcane_parent'],faction['arcane'],{
                'unam':name,'utip':name,'utub':'Race-themed arcane support structure. Provides the same role as the Human Arcane Sanctum.',
                'ugol':160,'ulum':70,'ubld':30,'uhpm':1100,'ureq':'','ures':'','urev':0,
            }))
        for tower_index, rawcode in enumerate(faction['towers']):
            if rawcode in ('h001','h002','h003'):
                continue
            name = _TOWER_NAMES[race][tower_index]
            gold,lumber,build_time,hit_points,damage = ((140,50,25,650,18),(260,100,35,850,70),(220,100,30,750,14))[tower_index]
            custom.append(record(faction['tower_parents'][tower_index],rawcode,{
                'unam':name,'utip':name,'utub':'Race-themed tower. Uses the same range, damage, cost, and support behavior as its Human counterpart.',
                'ugol':gold,'ulum':lumber,'ubld':build_time,'uhpm':hit_points,'ua1b':damage,
                'ureq':'','ures':'','urev':0,
            }))
        for role, entry in faction['company_buildings'].items():
            fields = {
                'unam':entry['name'], 'utip':'Build '+entry['name'],
                'utub':entry['tooltip'], 'ugol':entry['gold'],
                'ulum':entry['lumber'], 'ubld':entry['build_time'],
                'uhpm':entry['hit_points'], 'ureq':faction['barracks'], 'ures':'', 'urev':0,
            }
            if role == 'siege_yard':
                fields['uabi'] = 'Aneu,Apit,Asid,Asud'
            custom.append(record(entry['parent'],entry['rawcode'],fields))
        if faction['race'] != 'Human':
            custom.append(record(faction['altar_parent'],faction['altar'],{
                'unam':race+' Hero Shrine','utip':'Build '+race+' Hero Shrine',
                'utub':'Select to choose your hero or revive the chosen hero. Hero creation is managed by the shared selection system.',
                'ureq':'','utra':'','ures':'','urev':0,'ugol':160,'ulum':70,'ubld':30,'uhpm':900,
            }))
    for entry in HERO_COMPANIES:
        company_fields = {
            'unam':entry['company_name'], 'utip':entry['company_name'],
            'utub':entry['hero_name']+' company recruit. Trained only from your Barracks after you raise this hero banner.',
            'ugol':entry['company_gold'], 'ulum':entry['company_lumber'],
            'uhpm':entry['company_hp'], 'ua1b':entry['company_damage'], 'ureq':'',
        }
        support_fields = {
            'unam':entry['support_name'], 'utip':entry['support_name'],
            'utub':entry['hero_name']+' tactical support. Trained only at your personal Siege Yard.',
            'ugol':entry['support_gold'], 'ulum':entry['support_lumber'],
            'uhpm':entry['support_hp'], 'ua1b':entry['support_damage'], 'ureq':'',
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

    # Preserve the installed native item identity. The campaign record's
    # EquipmentBackpackAnya script is bound to ebua; a custom child item can
    # report 30 extended slots while missing the click-to-open UI behavior.
    original = [record('ebua','\0\0\0\0',{'unam':'Forsaken Field Pack','utip':'Forsaken Field Pack','utub':'Native Forsaken Kingdom backpack: 30 storage slots and nine equipment slots. Keep this pack in your hero inventory.','iabi':'AIni,AEqu,ASde','iequ':0,'iusa':1,'iper':0,'iuse':0,'idro':0,'ipaw':0,'isel':0,'iprn':0,'igol':0,'isto':1})]
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
                'iequ':0,'iusa':0,'iper':0,'iuse':0,'idro':0,'ipaw':0,'isel':1}
        custom.append(record(book['parent'],book['rawcode'],fields))
    for recipe in recipe_catalog(item_catalog()):
        fields={'icla':'Power-ups','unam':'Forge Recipe: '+recipe['name'],
                'utip':'Forge Recipe: '+recipe['name'],'utub':recipe['description'],
                'igol':recipe['price'],'iabi':'','iequ':0,'iusa':0,'iper':0,
                'iuse':0,'idro':0,'ipaw':0,'isel':1}
        custom.append(record('arsc',recipe['rawcode'],fields))
    controls=[record('phea','KHE1',{'icla':'Miscellaneous','unam':'Heal King Aldric','utip':'Heal King Aldric','utub':'Restore up to 2,000 King Aldric health. Costs 150 gold and 50 lumber. If he is at full health, the cost is refunded.','igol':150,'ilum':50,'iequ':0,'iusa':0,'iper':0,'idro':0,'ipaw':0,'isel':0})]
    for tier in range(5):
        raw='KUP'+str(tier+1)
        cost=400+200*tier
        controls.append(record('ckng',raw,{'icla':'Miscellaneous','unam':'Royal Defense Upgrade - Tier '+str(tier+1),'utip':'Royal Defense Upgrade - Tier '+str(tier+1),'utub':'Upgrade King Aldric: +4,000 maximum/current health and +30 damage. Tier '+str(tier+1)+' costs '+str(cost)+' gold and 150 lumber.','igol':cost,'ilum':150,'iequ':0,'iusa':0,'iper':0,'idro':0,'ipaw':0,'isel':0}))
    custom.extend(controls+[
        record('ratf','I010',{'icla':'Equipment','unam':color_rarity_text('Rare','Gravetide Cleaver'),'utip':color_rarity_text('Rare','Gravetide Cleaver'),'utub':color_rarity_text('Rare','Rare')+' boss relic. Chapter I: +15 damage.','iequ':6,'igol':0,'ipaw':0,'isel':0,'idro':1}),
        record('rhth','I011',{'icla':'Equipment','unam':color_rarity_text('Epic','Heart of the Watch'),'utip':color_rarity_text('Epic','Heart of the Watch'),'utub':color_rarity_text('Epic','Epic')+' boss relic. Chapter II: increases maximum health.','iequ':2,'igol':0,'ipaw':0,'isel':0,'idro':1}),
        record('lgdh','I012',{'icla':'Equipment','unam':color_rarity_text('Epic','Crown of Dawn'),'utip':color_rarity_text('Epic','Crown of Dawn'),'utub':color_rarity_text('Epic','Epic')+' boss relic. Chapter III: grants a healing aura.','iequ':8,'igol':0,'ipaw':0,'isel':0,'idro':1}),
        record('ckng','I013',{'icla':'Equipment','unam':color_rarity_text('Legendary','Oath of the Last King'),'utip':color_rarity_text('Legendary','Oath of the Last King'),'utub':color_rarity_text('Legendary','Legendary')+' boss relic. Chapter IV: +5 to all attributes.','iequ':5,'igol':0,'ipaw':0,'isel':0,'idro':1}),
    ])
    return table(original, custom)
