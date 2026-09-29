from wave_rosters import ENEMY_LOOT_TIER_BY_UNIT

FAMILIES = [
    ('Blade', (('ecss','Steel Sword'),('elbc','Lesser Blade of the Cultist'),('epbs','Plaguebearer Shortsword'),('erpb','Purifier Blade'),('ebr2',"Blademaster's Greatsword")), 6, 1.5, 'Primary'),
    # The installed FK item set contains only two equipment-class bows; retain
    # those native visuals rather than giving the upper tiers sword/lance art.
    ('Bow', (('efpb','Forsaken Plaguebow'),('efpb','Forsaken Plaguebow'),('efpb','Forsaken Plaguebow'),('epsb','Skeletal Bow'),('epsb','Skeletal Bow')), 6, 1.5, 'Primary'),
    ('Staff', (('epmw','Mundane Wand'),('edds','Dalaran Diamond Staff'),('esah','Staff of Arcane Hunger'),('essi','Staff of the Scarlet Inquisitor'),('egse',"Selene, Grand Scepter of Elune")), 3, 1.0, 'Primary'),
    ('Shield', (('eobb','Bone Buckler'),('eops','Phalanx Shield'),('edis','Dark Iron Shield'),('eosc','Shield of the Scarlet Crusade'),('esot','Shield of the Titans')), 2, 1.0, 'Offhand'),
    ('Focus', (('ewoa','Wand of the Apprentice'),('etoo','Twilight Opal Orb'),('eslo','Lich Orb'),('ewob','Wand of the Battlemage'),('ehls','Horn of the Lost Spirits')), 75, 1.0, 'Offhand'),
    ('Helmet', (('ecgh','Guardsman Helmet'),('edsh','Damaged Spellbreaker Helmet'),('efch',"Forsaken Champion's Helm"),('edrh',"Dark Ranger's Hood"),('ebr1','Blackrock Chain Helm')), 60, 1.0, 'Head'),
    ('Chest', (('ecgc','Guardsman Chestplate'),('efla','Frail Leather Armor'),('easc','Armor of the Scarlet Crusade'),('ebsp','Breastplate of the Scarlet Paladin'),('eaor','Armor of Reanimation')), 100, 1.0, 'Chest'),
    ('Gloves', (('eclg','Deerskin Gloves'),('efsh',"Frayed Sorcerer's Handwraps"),('eggn','Gloves of Necromancy'),('egdb','Gloves of the Deathbringer'),('ecmg',"Chronomaster's Gloves")), 5, 1.0, 'Gloves'),
    ('Boots', (('brpb','Rusty Plated Boots'),('ebhb','Heavyduty Boots'),('ebnp',"Necromancer's Plaguegreaves"),('eboi','Boots of the Icewalker'),('ebsw','Stormwalkers Boots')), 10, 1.0, 'Boots'),
    ('Offensive Ring', (('ecrr','Ring of Regeneration'),('erfa','Ring of the Fortunate Adventurer'),('ejjr','Jagged Jade Ring'),('erfl','Ring of the Firelands'),('ehfi','Ring of Holy Fire')), 3, 1.0, 'Ring'),
    ('Defensive Ring', (('ecav','Amulet of Vitality'),('ersf','Ring of Stone Fortitude'),('eres','Earthen Signet'),('eicc','Icecrown Ring'),('erdr','Diamond Ring')), 1, 1.0, 'Ring'),
    ('Trinket', (('elmt','Lesser Mark of Time'),('elmf','Lesser Mark of the Forsaken'),('ebdf','Blue Dragon Figurine'),('etkj',"Knight's Javelin"),('eege','Essencium, the Gathering of Elements')), 50, 1.0, 'Trinket'),
]
TIERS = [('Common',300),('Uncommon',1000),('Rare',3000),('Epic',8000),('Legendary',20000)]
ENEMY_DROP_THRESHOLDS = {
    'normal': (160, 250, 290, 298, 300),
    'elite': (350, 650, 850, 950, 1000),
    'boss': (1500, 2800, 4100, 4800, 5000),
}
ENEMY_POTION_THRESHOLDS_PER_1000 = {'normal': 40, 'elite': 80, 'boss': 180}
RARITY_COLORS = {
    'Common':'|cffffffff',
    'Uncommon':'|cff1eff00',
    'Rare':'|cff0070dd',
    'Epic':'|cffa335ee',
    'Legendary':'|cffff8000',
}
SLOTS = {'Head':1,'Chest':2,'Gloves':3,'Boots':4,'Ring':5,'Primary':6,'Offhand':7,'Trinket':8}


def color_rarity_text(quality, text):
    """Color a Warcraft UI string with its quality color, then reset it."""
    return RARITY_COLORS[quality] + text + '|r'

# Native item ability templates and their installed Object Editor data fields.
STATS = {
 'damage':('AIat','Iatt',1,0), 'armor':('AId1','Idef',1,0),
 'strength':('AIs1','Istr',3,0), 'agility':('AIa1','Iagi',1,0),
 'intelligence':('AIi3','Iint',2,0), 'health':('AIlf','Ilif',1,0),
 'mana':('AImb','Iman',1,0), 'attack speed':('AIsx','Isx1',1,2),
 'movement speed':('AIms','Imvb',1,0),
}
FAMILY_STATS=[{'damage':6},{'damage':6},{'intelligence':3},{'armor':2},{'mana':75},
 {'health':60},{'health':100},{'attack speed':5},{'movement speed':10},
 {'damage':3},{'armor':1},{'health':50,'mana':50},{'health':50,'armor':1},
 {'strength':2},{'agility':2},{'intelligence':2}]
NAMES = [
 ('Militia Blade','Veteran Longsword','Gravebreaker','Cinderfang','Kingswrath'),
 ('Hunting Bow','Sentinel Longbow','Bloodthorn','Widowmaker','Endless Hunt'),
 ('Apprentice Staff','Runewood Staff','Wintercall','Glacierheart','Staff of the Last Winter'),
 ('Iron Buckler','Wardens Shield','Dawnward','Adamant Aegis','Unbroken Oath'),
 ('Apprentice Focus','Sapphire Focus','Spellwell','Astral Prism','Heart of the Leyline'),
 ('Watchmans Helm','Veteran Greathelm','Crown of Vigilance','Dawnguard Helm','Crown of the Unbowed'),
 ('Militia Cuirass','Tempered Breastplate','Bastion Plate','Royal Bulwark','Armor of the Last Stand'),
 ('Scouts Gloves','Duelists Grips','Stormgrasp','Tempest Gauntlets','Hands of the Thunderlord'),
 ('Marching Boots','Pathfinders Boots','Windstriders','Gale Treads','Steps of the First Dawn'),
 ('Copper Warband','Veterans Signet','Ring of Conquest','Crimson Covenant','Sovereigns Fury'),
 ('Iron Ward Ring','Guardians Band','Stoneheart Signet','Circle of Resolve','Eternal Bastion'),
 ('Watchmans Charm','Healers Emblem','Dawnseed','Beacon of Hope','Heart of the Kingdom'),
 ('Travelers Cape','Wardens Mantle','Mistweave Cape','Royal Phoenix Mantle','Shroud of the Eternal Watch'),
 ('Recruit Plate','Vanguard Plate','Lionheart Cuirass','Kingsguard Plate','Aldrics Mightplate'),
 ('Swiftwalk Boots','Windrunner Boots','Stormpath Boots','Tempest Boots','Boots of the Unbound Gale'),
 ('Apprentice Focus','Sage Focus','Runebound Focus','Astral Focus','The Crownless Star'),
]

_CAPE = ('Cape',(('edsm',"Decrepit Sorcerer's Mantle"),('emoh','Mantle of the Highborne'),
        ('evow','Vestments of the Waterlord'),('erkt',"Robes of the Kirin'Tor"),
        ('erbm','Robes of the Battlemage')),50,1.0,'Chest')
_ATTRIBUTE_FAMILIES = [
    ('Might Chestplate',(('ecgc','Guardsman Chestplate'),('efla','Frail Leather Armor'),
     ('easc','Armor of the Scarlet Crusade'),('ebsp','Breastplate of the Scarlet Paladin'),
     ('eaor','Armor of Reanimation')),2,1.0,'Chest'),
    ('Windrunner Boots',(('brpb','Rusty Plated Boots'),('ebhb','Heavyduty Boots'),
     ('ebnp',"Necromancer's Plaguegreaves"),('eboi','Boots of the Icewalker'),
     ('ebsw','Stormwalkers Boots')),2,1.0,'Boots'),
    ('Arcanist Focus',(('ewoa','Wand of the Apprentice'),('etoo','Twilight Opal Orb'),
     ('eslo','Lich Orb'),('ewob','Wand of the Battlemage'),('ehls','Horn of the Lost Spirits')),
     2,1.0,'Offhand'),
]

# Five universal pieces per playable race. The catalog owns their quality,
# native icon parent, slot, stat abilities, tooltip color, and shop/drop data.
_RACE_ITEM_ROWS = (
    ('Human', 'Crown Relics', (
        ('Watchman’s Token','Trinket','health',120,'elmt',{'strength':2}),
        ('Lionroad Mantle','Chest','strength',4,'emoh',{'health':180}),
        ('Aldric’s Aegis','Offhand','armor',5,'eosc',{'strength':5}),
        ('Crownward Pennant','Trinket','strength',6,'ebdf',{'health':300}),
        ('Last King’s Oath','Ring','strength',8,'erdr',{'damage':20,'health':500}),
    )),
    ('Orc', 'Redtusk Relics', (
        ('Redtusk Fetish','Trinket','strength',3,'elmt',{'damage':3}),
        ('Ashen War Drum','Trinket','strength',3,'etkj',{'attack speed':5}),
        ('Stormscar Bracers','Gloves','strength',4,'eggn',{'attack speed':7}),
        ('Grudgebreaker','Primary','damage',24,'efpb',{'strength':4}),
        ('Worldrend Standard','Offhand','damage',20,'ehls',{'strength':9}),
    )),
    ('Night Elf', 'Moonbark Relics', (
        ('Moonbark Charm','Trinket','agility',2,'ebdf',{'health':100}),
        ('Starleaf Quiver','Primary','agility',3,'epsb',{'attack speed':5}),
        ('Duskwatch Longbow','Primary','damage',15,'epsb',{'agility':4}),
        ('Briarheart Mantle','Chest','agility',6,'emoh',{'health':250}),
        ('Silvermoon Vigil','Ring','agility',8,'ejjr',{'attack speed':8}),
    )),
    ('Undead', 'Wraith Relics', (
        ('Crypt-Iron Band','Ring','intelligence',2,'ecav',{'armor':1}),
        ('Wraithsilk Cape','Chest','intelligence',3,'edsm',{'mana':100}),
        ('Soulreaper’s Fang','Primary','damage',9,'epbs',{'intelligence':5}),
        ('Mourning Reliquary','Trinket','intelligence',6,'eege',{'mana':300}),
        ('Night’s Covenant','Offhand','intelligence',8,'ehls',{'health':250,'mana':400}),
    )),
)
_TIER_MULTIPLIER = (1,2,4,7,11)
CUSTOM_RACE_ITEMS = []
for race_index, (race, family, rows) in enumerate(_RACE_ITEM_ROWS):
    for tier, (name, slot_name, main_stat, base_amount, icon, extra_stats) in enumerate(rows):
        stats = {main_stat:base_amount*_TIER_MULTIPLIER[tier]}
        stats.update({stat:amount*_TIER_MULTIPLIER[tier] for stat, amount in extra_stats.items()})
        serial = 120 + tier*4 + race_index
        suffix = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ'[serial//36] + '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ'[serial%36]
        quality = TIERS[tier][0]
        bonus = max(stats.values())
        colored = color_rarity_text(quality,name)
        bonuses = '; '.join('+'+str(value)+' '+stat for stat,value in stats.items())
        CUSTOM_RACE_ITEMS.append({
            'rawcode':'I2'+suffix, 'tier':tier, 'quality':quality, 'family':family,
            'family_index':16+race_index, 'race':race, 'slot':SLOTS[slot_name],
            'slot_name':slot_name, 'bonus':bonus, 'price':int(TIERS[tier][1]*(1.5 if slot_name=='Primary' else 1)),
            'name':name, 'native_name':name, 'parent':icon,
            'abilities':','.join(f'A{n}{suffix}' for n in range(len(stats))),
            'stats':stats, 'effect':'', 'colored_name':colored,
            'description':color_rarity_text(quality,quality)+f' | {family} | {slot_name} slot.|n{bonuses}.|n'+
                'Universally equippable by all heroes. Bonuses apply while equipped. Sells for 50%.',
            'craft_output':tier==4,
        })

_CRAFTED = [
    {'rawcode':'I128','name':"Oathforged Kingswrath",'parent':'ebr2','tier':4,
     'family':'Blade','family_index':0,'slot':6,'price':30000,
     'native_name':"Blademaster's Greatsword",'stats':{'damage':88,'strength':10},
     'effect':'Cleave attacks deal 35% damage to nearby secondary enemies.'},
    {'rawcode':'I129','name':'Stormheart Prism','parent':'ehls','tier':4,
     'family':'Focus','family_index':4,'slot':7,'price':28000,
     'native_name':'Horn of the Lost Spirits','stats':{'intelligence':22,'mana':550},
     'effect':'Restores 50 mana after a spell cast; 8-second cooldown.'},
    {'rawcode':'I12A','name':"Sovereign's Mantle",'parent':'erbm','tier':4,
     'family':'Cape','family_index':12,'slot':2,'price':36000,
     'native_name':'Robes of the Battlemage',
     'stats':{'strength':10,'agility':10,'intelligence':10,'health':800,'armor':10},
     'effect':'Reduces incoming spell damage by 15%.'},
]

_BOOKS = []
for stat, prefix, parent, display in (
        ('strength','S','tstr','Strength'), ('agility','A','tdex','Agility'),
        ('intelligence','I','tint','Intelligence')):
    for amount, price in ((5,1000),(10,3000),(20,8000)):
        _BOOKS.append({'rawcode':'K'+prefix+str(amount).zfill(2),
                       'name':'Tome of '+display+' +'+str(amount),
                       'stat':stat,'amount':amount,'price':price,'parent':parent,
                       'description':'Permanently increases your hero '+display+
                         ' by '+str(amount)+'. Applies instantly when purchased from the Sage\'s Archive.'})

def item_catalog():
    result=[]
    alphabet='0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    families=FAMILIES+[_CAPE]+_ATTRIBUTE_FAMILIES
    for tier,(quality,base_price) in enumerate(TIERS):
        for index,(family,parents,stat,factor,slot) in enumerate(families):
            if index < 12:
                serial=tier*12+index
            elif index == 12:
                serial=60+tier
            else:
                serial=65+tier*3+(index-13)
            code=alphabet[serial//36]+alphabet[serial%36]
            stats={key:value*(1,2,4,7,11)[tier] for key,value in FAMILY_STATS[index].items()}
            ability_ids=['A'+str(n)+code for n in range(len(stats))]
            effect=''
            power=0
            if tier>=2:
                power=(40,80,140)[tier-2]
                effect={0:f'Cleave: attacks deal {(15,25,35)[tier-2]}% damage to other enemies within 250 of the target.',
                 1:f'Bloodthorn: attacks bleed for {(30,60,100)[tier-2]} damage over 3 seconds. Cooldown: 5 seconds.',
                 2:f'Wintercall: attacks burst for {power} damage within 250 and slow movement by 20% for 2 seconds. Cooldown: 8 seconds.',
                 3:f'Dawnward: absorb up to {power} damage from one incoming hit. Cooldown: 8 seconds.',
                 4:f'Spellwell: restore {(15,30,50)[tier-2]} mana after casting a spell. Cooldown: 8 seconds.',
                 11:f'Dawnseed: heal you and allied heroes within 400 for {power} every 10 seconds.',
                 12:f'Mistweave: reduce incoming spell damage by {(5,10,15)[tier-2]}%.'}.get(index,'')
            price=int(base_price*(1.5 if index<3 else 1))
            desc='; '.join('+'+str(v)+('%' if k=='attack speed' else '')+' '+k for k,v in stats.items())+'.'
            desc=color_rarity_text(quality, quality)+f' {family} | {slot} slot.|n'+desc+'|n'+effect+'|nBonuses apply while equipped. All heroes. Sells for 50%.'
            if index==12:desc+=' Cape replaces chest armor in the chest slot.'
            if effect:desc+=' Named effects use the strongest equipped copy; swapping does not reset cooldowns.'
            result.append(dict(rawcode='I1'+code,tier=tier,quality=quality,family=family,parent=parents[tier][0],
              slot=SLOTS[slot],bonus=stat*(1,2,4,7,11)[tier],price=price,name=NAMES[index][tier],native_name=parents[tier][1],
              colored_name=color_rarity_text(quality,NAMES[index][tier]),
              stats=stats,abilities=','.join(ability_ids),description=desc,effect=effect,family_index=index))
    for item in _CRAFTED:
        entry=dict(item)
        suffix=entry['rawcode'][2:]
        entry['quality']='Legendary'
        entry['bonus']=max(entry['stats'].values())
        entry['abilities']=','.join('A'+str(n)+suffix for n in range(len(entry['stats'])))
        bonuses='; '.join('+'+str(value)+' '+stat for stat,value in entry['stats'].items())
        entry['colored_name']=color_rarity_text('Legendary',entry['name'])
        entry['description']=color_rarity_text('Legendary','Legendary')+' crafted '+entry['family']+' | '+str(entry['slot'])+' slot.|n'+bonuses+'.|n'+entry['effect']+'|nBonuses apply while equipped. All heroes. Sells for 50%.'
        entry['crafted']=True
        result.append(entry)
    result.extend(dict(entry) for entry in CUSTOM_RACE_ITEMS)
    return result


def attribute_books():
    return [dict(book) for book in _BOOKS]


def crafted_items():
    return [dict(item) for item in item_catalog() if item.get('crafted')]

def abilities():
    import struct
    records=[]
    def ability(base,code,fields):
        out=bytearray(base.encode()+code.encode()+struct.pack('<I',len(fields)))
        for key,typ,level,pointer,value in fields:
            out.extend(key.encode()+struct.pack('<III',typ,level,pointer))
            out.extend(value.encode()+b'\0' if typ==3 else struct.pack('<f' if typ in (1,2) else '<i',value))
            out.extend(code.encode())
        return bytes(out)
    for entry in item_catalog():
        for code,(stat,value) in zip(entry['abilities'].split(','),entry['stats'].items()):
            base,field,pointer,typ=STATS[stat]
            if stat=='attack speed':value/=100
            records.append(ability(base,code,[('anam',3,0,0,entry['name']+' '+stat),('alev',0,0,0,1),
              (field,typ,1,pointer,value)]))
    records.append(ability('Aslo','ASl0',[('alev',0,0,0,1),('areq',3,0,0,''),('amcs',0,1,0,0),('aran',2,1,0,9999.0),('adur',2,1,0,2.0),('ahdu',2,1,0,2.0),('Slo1',2,1,1,0.2),('Slo2',2,1,2,0.0)]))
    from signature_spells import spell_records
    records.extend(spell_records(ability))
    # AEqu's campaign level requirement is unnecessary in this co-op map.
    original=[ability('AEqu','\0'*4,[('equ1',0,level,6,0) for level in (1,2,3)])]
    from hero_progression import hero_ability_records
    original.extend(hero_ability_records(ability))
    from hero_progression import hero_choice_ability_records
    records.extend(hero_choice_ability_records(ability))
    # Entangle Gold Mine is a native Night Elf town-hall action. The mine is
    # 1,200 units from the starting Tree of Life, beyond the installed 500 range.
    original.append(ability('Aent','\0' * 4,[('aran',2,1,0,1450.0)]))
    return struct.pack('<II',2,len(original))+b''.join(original)+struct.pack('<I',len(records))+b''.join(records)

def catalog_script():
    lines=['function KLS_CatalogInit takes nothing returns nothing',
           '    // The item object data holds the native icon, stat abilities, name and full tooltip.']
    for e in item_catalog():
        lines += [f"    call SaveInteger(KLS_GearData, '{e['rawcode']}', 0, {e['family_index']+1})",
                  f"    call SaveInteger(KLS_GearData, '{e['rawcode']}', 1, {e['tier']})",
                  f"    call SaveInteger(KLS_GearData, '{e['rawcode']}', 2, {e['slot']})"]
    for race_index, race in enumerate(('Human','Orc','Night Elf','Undead')):
        for entry in CUSTOM_RACE_ITEMS:
            if entry['race'] == race:
                lines.append(f"    set KLS_RaceItemId[{race_index*5+entry['tier']}] = '{entry['rawcode']}'")
    lines+=['endfunction','function KLS_StockCatalog takes nothing returns nothing']
    for e in item_catalog():
        # Race-themed relics belong to their matching Crownlands town shop;
        # Legendary race relics are outputs of their Foundry recipes.
        if e.get('crafted') or e.get('race'):
            continue
        merchant=e['tier']*2+(0 if e['family_index']<7 else 1)
        lines.append(f"    call AddItemToStock(KLS_Shops[{merchant}], '{e['rawcode']}', 1, 1)")
    for book in attribute_books():
        lines.append(f"    call AddItemToStock(KLS_Shops[11], '{book['rawcode']}', 1, 1)")
    lines += [
        'endfunction',
        'function KLS_BookAmount takes integer itemCode returns integer',
        '    if false then',
        '        return 0',
    ]
    for book in attribute_books():
        lines += [f"    elseif itemCode == '{book['rawcode']}' then", f"        return {book['amount']}"]
    lines += ['    endif', '    return 0', 'endfunction',
              'function KLS_BookPrice takes integer itemCode returns integer',
              '    if false then', '        return 0']
    for book in attribute_books():
        lines += [f"    elseif itemCode == '{book['rawcode']}' then", f"        return {book['price']}"]
    lines += ['    endif', '    return 0', 'endfunction',
              'function KLS_BookStat takes integer itemCode returns integer',
              '    if false then', '        return bj_HEROSTAT_STR']
    stat_id={'strength':'bj_HEROSTAT_STR','agility':'bj_HEROSTAT_AGI','intelligence':'bj_HEROSTAT_INT'}
    for stat, constant in stat_id.items():
        codes=[book['rawcode'] for book in attribute_books() if book['stat']==stat]
        condition=' or '.join("itemCode == '"+code+"'" for code in codes)
        lines += ['    elseif '+condition+' then', f'        return {constant}']
    lines += ['    endif', '    return bj_HEROSTAT_STR', 'endfunction']
    droppable=[entry for entry in item_catalog() if not entry.get('crafted')]
    lines += [
        'function KLS_RandomCatalogDrop takes integer tier returns integer',
        '    local integer choice = 0',
        '    local integer n = 0',
    ]
    for tier, (quality, _) in enumerate(TIERS):
        rows=[entry for entry in droppable if entry['tier']==tier]
        lines += [f'    if tier == {tier} then',
                  f'        set choice = GetRandomInt(0,{len(rows)-1})']
        for index, entry in enumerate(rows):
            branch='if' if index==0 else 'elseif'
            lines.append(f"        {branch} choice == {index} then")
            lines.append(f"            return '{entry['rawcode']}'")
        lines += ['        endif', '    endif']
    lines += [
        "    return 'I100'",
        'endfunction',
    ]
    lines += [
        'function KLS_EnemyLootTier takes unit enemy, boolean boss returns integer',
        '    local integer unitCode = GetUnitTypeId(enemy)',
        '    if boss then',
        '        return 2',
        '    endif',
    ]
    for unit_code, loot_tier in ENEMY_LOOT_TIER_BY_UNIT.items():
        tier = 1 if loot_tier == 'elite' else 0
        lines += [
            f"    if unitCode == '{unit_code}' then",
            f'        return {tier}',
            '    endif',
        ]
    lines += ['    return 0', 'endfunction',
              'function KLS_EnemyDropRarity takes integer tier, integer roll returns integer']
    for tier, loot_tier in enumerate(('normal', 'elite', 'boss')):
        outer = 'if' if tier == 0 else 'elseif'
        lines.append(f'    {outer} tier == {tier} then')
        for rarity, threshold in enumerate(ENEMY_DROP_THRESHOLDS[loot_tier]):
            inner = 'if' if rarity == 0 else 'elseif'
            lines += [
                f'        {inner} roll <= {threshold} then',
                f'            return {rarity}',
            ]
        lines.append('        endif')
    lines += [
        '    endif',
        '    return -1',
        'endfunction',
        'function KLS_EnemyPotionThreshold takes integer tier returns integer',
        '    if tier == 2 then',
        f"        return {ENEMY_POTION_THRESHOLDS_PER_1000['boss']}",
        '    elseif tier == 1 then',
        f"        return {ENEMY_POTION_THRESHOLDS_PER_1000['elite']}",
        '    endif',
        f"    return {ENEMY_POTION_THRESHOLDS_PER_1000['normal']}",
        'endfunction',
        'function KLS_DropEnemyItem takes unit enemy, integer itemCode, integer p, real offsetX returns nothing',
        '    local item drop',
        '    if itemCode != 0 and enemy != null then',
        '        set drop = CreateItem(itemCode,GetUnitX(enemy)+offsetX,GetUnitY(enemy))',
        '        if drop != null then',
        '            if p >= 0 and p < 4 and KLS_Active[p] then',
        '                call SetItemPlayer(drop,Player(p),false)',
        '                call SetItemUserData(drop,p+1)',
        '                call DisplayTimedTextToPlayer(Player(p),0,0,6,GetItemName(drop)+\" dropped nearby.\")',
        '            endif',
        '        else',
        '            call KLS_Log(\"ERROR enemy item drop creation failed: item=\"+GetObjectName(itemCode)+\" rawcode=\"+I2S(itemCode)+\" enemy=\"+GetObjectName(GetUnitTypeId(enemy))+\" enemyXY=\"+R2S(GetUnitX(enemy))+\",\"+R2S(GetUnitY(enemy))+\" killerPlayerId=\"+I2S(p))',
        '        endif',
        '    endif',
        '    set drop = null',
        'endfunction',
        'function KLS_EnemyDrop takes unit enemy, boolean boss returns nothing',
        '    local integer roll = GetRandomInt(1,10000)',
        '    local integer potionRoll = GetRandomInt(1,1000)',
        '    local integer tier = 0',
        '    local integer rarity = -1',
        '    local integer gearCode = 0',
        '    local integer potionCode = 0',
        '    local integer p = 4',
        '    local unit killer = GetKillingUnit()',
        '    if enemy == null then',
        '        set killer = null',
        '        return',
        '    endif',
        '    if killer != null then',
        '        set p = GetPlayerId(GetOwningPlayer(killer))',
        '    endif',
        '    set tier = KLS_EnemyLootTier(enemy,boss)',
        '    set rarity = KLS_EnemyDropRarity(tier,roll)',
        '    if rarity >= 0 then',
        '        set gearCode = KLS_RandomCatalogDrop(rarity)',
        '    endif',
        '    if potionRoll <= KLS_EnemyPotionThreshold(tier) then',
        '        set roll = GetRandomInt(0,3)',
        '        if roll == 0 then',
        "            set potionCode = 'phea'",
        '        elseif roll == 1 then',
        "            set potionCode = 'pman'",
        '        elseif roll == 2 then',
        "            set potionCode = 'stwp'",
        '        else',
        "            set potionCode = 'shea'",
        '        endif',
        '    endif',
        '    call KLS_DropEnemyItem(enemy,gearCode,p,0.0)',
        '    call KLS_DropEnemyItem(enemy,potionCode,p,48.0)',
        '    set killer = null',
        'endfunction',
    ]
    return '\n'.join(lines)
