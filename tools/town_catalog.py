"""Placements and identity for the four allied Crownlands settlements."""

TOWNS = (
    {'race':'Human','name':'Crownshire','x':0.0,'y':-9000.0,'hall':'htow','barracks':'hbar','food':'hhou','blacksmith':'hbla','altar':'h000','worker':'hpea','shop':'Crownshire Provisioner','quest':'Crownshire Supplymaster','quest_id':0},
    {'race':'Orc','name':'Redtusk Hold','x':-9000.0,'y':0.0,'hall':'ogre','barracks':'obar','food':'otrb','blacksmith':'ofor','altar':'kA01','worker':'opeo','shop':'Redtusk Quartermaster','quest':'Northwatch Vanguard','quest_id':1},
    {'race':'Night Elf','name':'Moonbark Glade','x':9000.0,'y':0.0,'hall':'etol','barracks':'eaow','food':'emow','blacksmith':'eaoe','altar':'kA02','worker':'ewsp','shop':'Moonbark Curator','quest':'Moonbark Warden','quest_id':2},
    {'race':'Undead','name':'Wraithfall','x':0.0,'y':9000.0,'hall':'unpl','barracks':'usep','food':'uzig','blacksmith':'uslh','altar':'kA03','worker':'uaco','shop':'Wraithfall Broker','quest':'Wraithfall Keeper','quest_id':3},
)

QUEST_RAWCODES = ('kQ00','kQ01','kQ02','kQ03')


def town_placements():
    """Return fixed, lane-adjacent structure placements for each town."""
    result = []
    for town in TOWNS:
        x, y = town['x'], town['y']
        if town['race'] in ('Human','Undead'):
            sign = -1 if town['race'] == 'Human' else 1
            positions = (
                (town['hall'], x+sign*850, y),
                (town['barracks'], x-sign*1150, y+sign*500),
                (town['food'], x+sign*1250, y-sign*700),
                (town['blacksmith'], x-sign*1450, y-sign*750),
                (town['altar'], x+sign*1500, y+sign*700),
            )
            shop = (x-sign*850, y-sign*1250)
            quest = (x+sign*900, y-sign*1450)
        else:
            sign = -1 if town['race'] == 'Orc' else 1
            positions = (
                (town['hall'], x, y+sign*850),
                (town['barracks'], x+sign*500, y-sign*1150),
                (town['food'], x-sign*700, y+sign*1250),
                (town['blacksmith'], x-sign*750, y-sign*1450),
                (town['altar'], x+sign*700, y-sign*1500),
            )
            shop = (x+sign*1250, y+sign*850)
            quest = (x+sign*1450, y-sign*900)
        for rawcode, px, py in positions:
            result.append((town['race'],rawcode,px,py))
        result.append((town['race'],'shop',shop[0],shop[1]))
        result.append((town['race'],QUEST_RAWCODES[town['quest_id']],quest[0],quest[1]))
        if town['race'] in ('Human','Undead'):
            result.append((town['race'],'tower',x+sign*1550,y))
        else:
            result.append((town['race'],'tower',x,y+sign*1550))
    return result


def town_script():
    lines = [
        'function KLS_CrownlandsBuildTowns takes nothing returns nothing',
        '    local integer i = 0',
        '    local integer tier = 0',
        '    local unit building',
        '    call KLS_FactionCatalogInit()',
    ]
    for town in TOWNS:
        race_index = next(i for i, value in enumerate(TOWNS) if value['race'] == town['race'])
        label = town['name']
        for rawcode, role in ((town['hall'],'hall'),(town['barracks'],'barracks'),(town['food'],'food'),
                              (town['blacksmith'],'blacksmith'),(town['altar'],'altar'),
                              ('tower','tower')):
            match = next((entry for entry in town_placements()
                          if entry[0] == town['race'] and entry[1] == rawcode), None)
            if match is None:
                continue
            _, _, x, y = match
            raw = f'KLS_FactionTowerId[{race_index*3}]' if role == 'tower' else "'"+rawcode+"'"
            lines += [f'    set building = KLS_CreateUnit(Player(PLAYER_NEUTRAL_PASSIVE),{raw},{x:.1f},{y:.1f},270)',
                      '    if building != null then',
                      '        call SetUnitInvulnerable(building,true)',
                      '        call SetUnitAcquireRange(building,0)',
                      '    endif']
            if role == 'hall':
                lines += [f'    if building != null then',
                          f'        call BlzSetUnitName(building,"{label}")',
                          '    endif']
        _, _, sx, sy = next(entry for entry in town_placements()
                            if entry[0] == town['race'] and entry[1] == 'shop')
        lines += [f"    set KLS_TownShop[{race_index}] = KLS_CreateUnit(Player(PLAYER_NEUTRAL_PASSIVE),'hS00',{sx:.1f},{sy:.1f},270)",
                  f'    if KLS_TownShop[{race_index}] != null then',
                  f'        call BlzSetUnitName(KLS_TownShop[{race_index}],"{town["shop"]}")',
                  f'        call SetUnitInvulnerable(KLS_TownShop[{race_index}],true)',
                  f'        call SetUnitAcquireRange(KLS_TownShop[{race_index}],0)',
                  '        set tier = 0',
                  '        loop',
                  '            exitwhen tier == 5',
                  f'            call AddItemToStock(KLS_TownShop[{race_index}],KLS_RaceItemId[{race_index}*5+tier],1,99)',
                  '            set tier = tier+1',
                  '        endloop',
                  f"        call AddItemToStock(KLS_TownShop[{race_index}],'phea',1,99)",
                  f"        call AddItemToStock(KLS_TownShop[{race_index}],'pman',1,99)",
                  '    endif']
        _, _, qx, qy = next(entry for entry in town_placements()
                            if entry[0] == town['race'] and entry[1] == QUEST_RAWCODES[town['quest_id']])
        lines += [f"    set KLS_TownSite[{race_index}] = KLS_CreateUnit(Player(PLAYER_NEUTRAL_PASSIVE),'{QUEST_RAWCODES[town['quest_id']]}',{qx:.1f},{qy:.1f},270)",
                  f'    if KLS_TownSite[{race_index}] != null then',
                  f'        call BlzSetUnitName(KLS_TownSite[{race_index}],"{town["quest"]}")',
                  f'        call SetUnitUserData(KLS_TownSite[{race_index}],{race_index})',
                  f'        call SetUnitInvulnerable(KLS_TownSite[{race_index}],true)',
                  f'        call SetUnitAcquireRange(KLS_TownSite[{race_index}],0)',
                  '    endif']
    lines += ['    set building = null','endfunction']
    return '\n'.join(lines)
