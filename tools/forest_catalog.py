"""Approved north/east/west exploration dressing and one-time camp catalog."""
import math
import random
import struct

CAMPS = (
    dict(name='Briarwolf Hollow', x=-4800, y=8200, leader='nwlg', guard='nwlt', quality=0),
    dict(name='Mossfang Enclave', x=4800, y=8200, leader='nftb', guard='nftr', quality=0),
    dict(name='Silkweb Cove', x=-6400, y=10100, leader='nspg', guard='nspb', quality=1),
    dict(name='Stonejaw Den', x=6400, y=10100, leader='nogm', guard='nogr', quality=1),
)
PATHS = (
    ((-1500,7000),(-2200,7400),(-3200,7550),(-4000,7900),(-4800,8200),(-5400,9000),(-5700,9600),(-6400,10100)),
    ((1500,7000),(2300,7400),(3300,7600),(4100,7850),(4800,8200),(5300,9000),(5900,9600),(6400,10100)),
    ((-3200,7550),(-3300,8700),(-2400,9500),(-1200,9900),(0,10100),(1400,9850),(2500,9400),(3300,8700),(3300,7600)),
)


def segment_distance(x, y, a, b):
    dx, dy = b[0]-a[0], b[1]-a[1]
    t = max(0, min(1, ((x-a[0])*dx+(y-a[1])*dy)/(dx*dx+dy*dy)))
    return math.hypot(x-a[0]-t*dx, y-a[1]-t*dy)


def path_distance(x, y):
    return min(segment_distance(x,y,a,b) for path in PATHS for a,b in zip(path,path[1:]))


def cove_distance(x, y):
    return min(math.hypot(x-c['x'], y-c['y']) for c in CAMPS)


def forest_plan():
    rng = random.Random(20261001)
    cliffs = []
    for x,y,r in ((-8100,7700,3),(-7900,9500,4),(-5400,10880,3),(-2400,10920,3),
                  (0,8700,3),(2400,10920,3),(5300,10900,3),(8000,9500,4),(8100,7700,3)):
        if path_distance(x,y) > r*128+420 and cove_distance(x,y) > r*128+850:
            cliffs.append(dict(x=x,y=y,radius=r))
    def clear(x,y,margin):
        return (path_distance(x,y)>margin and cove_distance(x,y)>690
                and not (abs(x)<1900 and y<8500)
                and all(math.hypot(x-c['x'],y-c['y'])>c['radius']*128+230 for c in cliffs))
    trees = []
    for y in range(6900,11200,360):
        for x in range(-8500,8700,420):
            px,py=x+rng.uniform(-135,135),y+rng.uniform(-110,110)
            if clear(px,py,365) and all(math.hypot(px-t['x'],py-t['y'])>235 for t in trees):
                trees.append(dict(type_id='LTlt',x=round(px,1),y=round(py,1),
                                  rotation=round(rng.random()*math.tau,3),scale=round(rng.uniform(.9,1.35),2),variation=rng.randrange(10)))
    rocks = []
    for _ in range(200):
        x,y=rng.uniform(-8600,8600),rng.uniform(7000,11100)
        if clear(x,y,340) and all(math.hypot(x-r['x'],y-r['y'])>400 for r in rocks):
            rocks.append(dict(type_id='LRrk',x=round(x,1),y=round(y,1),rotation=round(rng.random()*math.tau,3),
                              scale=round(rng.uniform(.65,1.25),2),variation=rng.randrange(6)))
            if len(rocks)==50:
                break
    trail = []
    for path in PATHS:
        for a,b in zip(path,path[1:]):
            steps=math.ceil(math.dist(a,b)/180)
            for n in range(steps+1):
                t=n/steps
                trail.append(dict(x=round(a[0]+t*(b[0]-a[0])),y=round(a[1]+t*(b[1]-a[1]))))
    return dict(trees=trees,rocks=rocks,cliffs=cliffs,trail=trail,camps=CAMPS)


def camp_script():
    ids = [f'k{prefix}{i:02d}' for i in range(4) for prefix in ('L','M')]
    lines=['function KLS_IsForestMonster takes integer kind returns boolean',
           '    return '+' or '.join(f"kind == '{raw}'" for raw in ids),'endfunction','',
           'function KLS_ForestReward takes unit dead, unit killer returns nothing',
           '    local integer p', '    local integer kind = GetUnitTypeId(dead)',
           '    local integer quality = -1', '    local integer itemCode',
           '    if KLS_Ended or killer == null then', '        return', '    endif',
           '    set p = GetPlayerId(GetOwningPlayer(killer))',
           '    if p < 0 or p >= 4 or not KLS_Active[p] then', '        return','    endif']
    for i,c in enumerate(CAMPS):
        lines += [('    if' if i==0 else '    elseif')+f" kind == 'kL{i:02d}' then", f'        set quality = {c["quality"]}']
    lines += ['    endif','    if quality >= 0 then',
              '        set itemCode = KLS_RandomCatalogDrop(quality)',
              '        call KLS_PersonalRewardEnqueue(p,itemCode,"Forest camp leader")',
              "        call KLS_PersonalRewardEnqueue(p,'phea',\"Forest camp supplies\")",
              '    elseif GetRandomInt(1,4) == 1 then',
              "        set itemCode = 'phea'",'        if GetRandomInt(0,1) == 1 then',
              "            set itemCode = 'pman'",'        endif',
              '        call KLS_PersonalRewardEnqueue(p,itemCode,"Forest camp supplies")','    endif','endfunction']
    lines += ['', 'function KLS_ForestInit takes nothing returns nothing', '    local unit u']
    for i,c in enumerate(CAMPS):
        for raw,x,y in ((f'kL{i:02d}',c['x'],c['y']+120),
                        (f'kM{i:02d}',c['x']-220,c['y']-100),
                        (f'kM{i:02d}',c['x']+220,c['y']-100)):
            lines += [f"    set u = KLS_CreateUnitOptional(Player(PLAYER_NEUTRAL_AGGRESSIVE),'{raw}',{x:.1f},{y:.1f},270,\"Forest camp\")",
                      '    if u != null then', '        call SetUnitAcquireRange(u,500)',
                      '        call SetUnitCreepGuard(u,true)', '    endif']
    lines += ['    set u = null', 'endfunction']
    return '\n'.join(lines)


def forest_pathing(original):
    """Block only the new isolated cliff outcrops; preserve authored pathing."""
    if original[:4] != b'MP3W' or struct.unpack_from('<III', original, 4) != (0,768,768):
        raise ValueError('Forest handoff requires the preserved 192-cell pathing grid')
    data = bytearray(original)
    for cliff in forest_plan()['cliffs']:
        r = cliff['radius']*128+150
        for y in range(max(0,int((cliff['y']-r+12288)//32)),min(768,int((cliff['y']+r+12288)//32)+1)):
            for x in range(max(0,int((cliff['x']-r+12288)//32)),min(768,int((cliff['x']+r+12288)//32)+1)):
                if math.hypot(x*32-12288+16-cliff['x'],y*32-12288+16-cliff['y'])<=r:
                    data[16+y*768+x] |= 2|8
    return bytes(data)
