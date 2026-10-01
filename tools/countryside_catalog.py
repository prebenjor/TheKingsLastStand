"""Deterministic countryside dressing, fitted to the saved authored map."""
import heapq
import json
import math
import random
import struct
from collections import deque
from pathlib import Path
from editor_layout import terrain_height
from editor_workshop import decode_units
from forest_catalog import segment_distance
from map_info import PLOTS

ORIGIN = -12288
STEP = 128
TREE_TYPES = {'LTlt','ATtr','VTlt','LTrt','YTft','ATtc','YT48'}
ROUTES = (
    ('Western settlement trail', ((-1900,-2500),(-2800,-3100),(-4400,-3500),(-4900,-5000),(-5000,-6500),(-4200,-7450),(-3400,-7400))),
    ('Western bandit branch', ((-4400,-3500),(-6500,-2800),(-7800,-1700),(-8200,600),(-8900,2100),(-9200,2400))),
    ('Western satyr branch', ((-4900,-5000),(-6500,-5000),(-7600,-5700),(-8050,-6500))),
    ('Western gnoll approach', ((-4400,-3500),(-3800,-3500),(-3500,-3800))),
    ('Eastern settlement trail', ((2200,-3200),(2300,-2200),(4100,-2200),(6300,-2300),(8000,-2300),(9000,-3300))),
    ('Eastern wolf approach', ((8000,-2300),(9000,-3500),(8900,-4700))),
    ('Eastern furbolg approach', ((6300,-2300),(6400,-3700),(6300,-4800),(6200,-5700))),
    ('Eastern quilboar branch', ((2200,-3200),(2400,-4700),(3300,-5900),(3400,-7300),(4000,-7500))),
    ('Eastern mine trail', ((8000,-2300),(8400,-1300),(8200,500),(8000,2400),(8400,3600))),
)


def protected(x,y):
    return (y >= 4608 or abs(x) >= 11520 or y <= -10500
            or abs(x)<1408 and -2600<y<2200 or abs(x)<640
            or any(abs(x-px)<1280 and abs(y-py)<1408 for px,py in PLOTS))


def nearest_distance(x,y,paths):
    return min((segment_distance(x,y,a,b) for path in paths for a,b in zip(path,path[1:])),default=1e9)


def circles(feature):
    return feature.get('lobes',[(feature['x'],feature['y'],feature['radius'])])


def inside(x,y,feature,extra=0):
    return any(math.hypot(x-a,y-b)<=r+extra for a,b,r in circles(feature))


def has_water(tile):
    return bool(struct.unpack_from('<H',tile,4)[0]&0x0100)


def has_ramp(tile):
    return bool(struct.unpack_from('<H',tile,4)[0]&0x0040)


def countryside_plan(folder):
    folder=Path(folder)
    terrain=(folder/'war3map.w3e').read_bytes()
    pathing=(folder/'war3map.wpm').read_bytes()
    units=list(decode_units((folder/'war3mapUnits.doo').read_bytes()).values())
    doodads=json.loads((folder/'baseline-doodads.json').read_text())
    obstacles=[(d['position'][0],d['position'][1],128 if d['type_id'] in TREE_TYPES else 64)
               for d in doodads if d['type_id'] in TREE_TYPES or d['type_id'] in {'LRrk','ARrk','LOlp','YOec','LSwl'}]
    obstacles += [(u['position'][0],u['position'][1],160 if u['owner']!=24 else 96)
                  for u in units if u['rawcode']!='sloc']
    def tile(x,y):
        col,row=round((x-ORIGIN)/128),round((y-ORIGIN)/128)
        return terrain[69+(row*193+col)*8:77+(row*193+col)*8]
    def clear(x,y,margin=256):
        return not protected(x,y) and all(math.hypot(x-a,y-b)>=r+margin for a,b,r in obstacles)
    # A* on the native corner lattice. Fit paths around scenery rather than
    # clearing existing trees or painting straight through their footprints.
    cache={}
    def walk(node):
        if node not in cache:
            x,y=node[0]*128+ORIGIN,node[1]*128+ORIGIN
            t=tile(x,y)
            blocked=protected(x,y) or not clear(x,y,280) or has_water(t) or (t[7]&15)!=2
            idx=16+(node[1]*4+2)*768+node[0]*4+2
            blocked=blocked or bool(pathing[idx]&2)
            cache[node]=not blocked
        return cache[node]
    regions={}; sizes={}; region_sides={}; next_region=0
    for row in range(14,133):
        for col in range(7,186):
            seed=(col,row)
            if seed in regions or not walk(seed):continue
            next_region+=1;queue=deque([seed]);regions[seed]=next_region;sizes[next_region]=0
            region_sides[next_region]=col<96
            while queue:
                c,r=queue.popleft();sizes[next_region]+=1
                for dc,dr in ((0,1),(1,0),(0,-1),(-1,0)):
                    n=(c+dc,r+dr)
                    if 7<=n[0]<186 and 14<=n[1]<133 and n not in regions and walk(n):
                        regions[n]=next_region;queue.append(n)
    main_regions={side:max((n for n in sizes if region_sides[n]==side),key=sizes.get)
                  for side in (False,True)}
    def node(p):return round((p[0]-ORIGIN)/128),round((p[1]-ORIGIN)/128)
    def nearest(p):
        c=node(p)
        candidates=[(math.hypot(dx,dy),c[0]+dx,c[1]+dy) for dx in range(-18,19) for dy in range(-18,19)]
        for _,a,b in sorted(candidates):
            if regions.get((a,b))==main_regions[p[0]<0]:return a,b
        raise ValueError('No clear trail anchor near '+str(p))
    def route(a,b):
        a,b=nearest(a),nearest(b)
        queue=[(0,a)]; costs={a:0}; previous={}
        while queue:
            _,current=heapq.heappop(queue)
            if current==b:
                chain=[b]
                while chain[-1]!=a:chain.append(previous[chain[-1]])
                return [(c*128+ORIGIN,r*128+ORIGIN) for c,r in reversed(chain)]
            for dc,dr in ((0,1),(1,0),(0,-1),(-1,0),(1,1),(-1,1),(1,-1),(-1,-1)):
                next_=(current[0]+dc,current[1]+dr)
                if not (2<=next_[0]<191 and 2<=next_[1]<191) or not walk(next_):continue
                if dc and dr and (not walk((current[0]+dc,current[1])) or not walk((current[0],current[1]+dr))):continue
                x,y=next_[0]*128+ORIGIN,next_[1]*128+ORIGIN
                t=tile(x,y)
                # Existing worn dirt is preferred, avoiding a parallel road.
                cost=costs[current]+math.hypot(dc,dr)*(0.8 if (t[4]&15)<3 else 1)
                if cost<costs.get(next_,1e9):
                    costs[next_]=cost;previous[next_]=current
                    heapq.heappush(queue,(cost+math.dist(next_,b)*.8,next_))
        raise ValueError('No preserved-pathing route between '+str((a,b)))
    paths=[]; names=[]
    for name,anchors in ROUTES:
        chain=[]
        for a,b in zip(anchors,anchors[1:]):
            segment=route(a,b);chain+=segment if not chain else segment[1:]
        paths.append(chain);names.append(name)
    def feature_site(preferred,radius):
        candidates=[(math.hypot(dx,dy),preferred[0]+dx,preferred[1]+dy)
                    for dx in range(-768,769,128) for dy in range(-768,769,128)]
        for _,x,y in sorted(candidates):
            if nearest_distance(x,y,paths)<radius+450 or not clear(x,y,radius+160):continue
            samples=[tile(x+dx,y+dy) for dx in (-radius,0,radius) for dy in (-radius,0,radius)]
            if all((t[7]&15)==2 and not has_water(t) for t in samples):
                heights=[terrain_height(terrain,x+dx,y+dy) for dx in (-radius,0,radius) for dy in (-radius,0,radius)]
                if max(heights)-min(heights)<48:return x,y
        raise ValueError('No untouched clearing for feature '+str(preferred))
    ponds=[]
    for name,preferred in (('Willow Rest',(-6500,-3700)),('Moonbark Reflection',(7600,-2400)),('Fernwater',(9900,1000))):
        x,y=feature_site(preferred,384)
        ground=terrain_height(terrain,x,y)
        ponds.append(dict(name=name,x=x,y=y,radius=384,surface=ground-24,floor=ground-120,
                          lobes=[(x,y,320),(x+192,y+64,256),(x-128,y-192,224)]))
        anchor=min((p for path in paths for p in path),key=lambda p:math.dist(p,(x,y)))
        shore_x=x+(-768 if anchor[0]<x else 768)
        paths.append(route(anchor,(shore_x,y)))
        names.append(name+' shore trail')
    hills=[]
    for name,preferred in (('Western lookout',(-6000,-5900)),('Eastern lookout',(7300,2200))):
        x,y=feature_site(preferred,512)
        hills.append(dict(name=name,x=x,y=y,radius=576,height=terrain_height(terrain,x,y)+128,
                          ramp=(x,y-384),ramp_width=640))
        anchor=min((p for path in paths for p in path),key=lambda p:math.dist(p,(x,y-768)))
        paths.append(route(anchor,(x,y-640))+[(x,y-512),(x,y-256),(x,y)])
        names.append(name+' spur')
    rng=random.Random(202610012)
    props=[]
    def prop(raw,x,y,rotation=None,scale=1,variation=0,z=None):
        if protected(x,y):return False
        if raw in {'LTlt','LRrk','YOec','LOlp','LOcb','YObw'} and any(
                protected(x+dx,y+dy) for dx in (-112,112) for dy in (-112,112)):return False
        if any(math.hypot(x-p['x'],y-p['y'])<100 for p in props):return False
        if not clear(x,y,40):return False
        clearance={'YOec':320,'LOlp':320,'YObw':352,'LOcb':352,'LTlt':384,'LRrk':352}.get(raw,0)
        if clearance and nearest_distance(x,y,paths)<clearance:return False
        props.append(dict(type_id=raw,x=x,y=y,z=terrain_height(terrain,x,y) if z is None else z,
                          rotation=rng.uniform(0,math.tau) if rotation is None else rotation,
                          scale=scale,variation=variation))
        return True
    def nearby_prop(raw,cx,cy,**kwargs):
        candidates=sorted((math.hypot(dx,dy),cx+dx,cy+dy)
                          for dx in range(-768,769,128) for dy in range(-768,769,128))
        for _,x,y in candidates:
            if nearest_distance(x,y,paths)>900:continue
            if any(inside(x,y,p,96) for p in ponds):continue
            if prop(raw,x,y,**kwargs):return True
        raise ValueError('Cannot place requested scenery '+raw+' near '+str((cx,cy)))
    # Useful supplies concentrated at inhabited entrances, not sprinkled along
    # forest trails. Find free ground near each authored commercial cluster.
    for cx,cy in ((-4100,-7700),(2850,-3750),(5600,-3900),(9200,-3200)):
        placed=0
        for dx,dy in ((0,0),(128,0),(0,-128),(-128,0),(128,-128),(-256,0),(0,256),(256,0),
                      (-256,-256),(256,-256),(-384,128),(384,128),(0,-384),(0,384)):
            if prop('YOec',cx+dx,cy+dy,variation=placed%3,scale=.9):placed+=1
            if placed==3:break
        while placed<3:
            nearby_prop('YOec',cx,cy,variation=placed%3,scale=.9)
            placed+=1
    for cx,cy in ((-2300,-2800),(-4200,-7300),(-4700,-3800),(-8300,1200),
                  (2200,-3800),(3600,-5100),(5600,-4900),(9000,-3800),(9100,-2300),(8000,3300)):
        candidate=min((p for path in paths for p in path),key=lambda p:math.dist(p,(cx,cy)))
        added=False
        for dx,dy in ((-320,0),(320,0),(0,-320),(0,320),(-448,0),(448,0)):
            x,y=candidate[0]+dx,candidate[1]+dy
            if nearest_distance(x,y,paths)>270 and prop('LOlp',x,y,variation=len(props)%6):
                added=True;break
        if not added:nearby_prop('LOlp',cx,cy,variation=len(props)%6)
    for hill in hills:
        prop('YObw',hill['x']-256,hill['y']+320,rotation=math.pi,z=hill['height'])
        prop('LOsp',hill['x']-192,hill['y']+128,rotation=0,z=hill['height'])
    nearby_prop('LOcb',-7100,-5200,rotation=1.2,scale=.9)
    for pond in ponds:
        x,y,z=pond['x'],pond['y'],pond['surface']
        for dx,dy in ((-128,0),(0,96),(128,0),(192,96),(0,-160),(-160,-128),(64,-64)):
            prop('LPlp',x+dx,y+dy,scale=rng.uniform(.8,1.2),z=z+2)
        for dx,dy in ((-512,128),(-384,384),(384,256),(128,-512)):
            prop('LRrk',x+dx,y+dy,scale=.65,variation=rng.randrange(6))
            prop('ZPsh',x+dx+96,y+dy+64,scale=.8,variation=0)
        prop('YObw',x+576,y,rotation=math.pi/2)
        prop('LOsp',x+576,y-160,rotation=0)
    # Small woodland clusters flank selected trail sections. Keep the full
    # corridor open and avoid every original scenery/placement footprint.
    for path in paths:
        for i in range(4,len(path)-4,6):
            a,b=path[i-1],path[i+1];dx,dy=b[0]-a[0],b[1]-a[1];length=math.hypot(dx,dy)
            if not length:continue
            for side in (-1,1):
                x=path[i][0]+side*(-dy/length)*rng.uniform(480,650)
                y=path[i][1]+side*(dx/length)*rng.uniform(480,650)
                if (nearest_distance(x,y,paths)>400 and clear(x,y,150)
                        and not any(inside(x,y,p,180) for p in ponds+hills)
                        and (tile(x,y)[7]&15)==2 and not has_water(tile(x,y))):
                    prop('LTlt',round(x),round(y),scale=rng.uniform(.9,1.2),variation=rng.randrange(10))
    # A pair of roadside rest spots, separate from the pond overlooks.
    for cx,cy in ((-5300,-6400),(6600,-3800)):
        nearby_prop('YObw',cx,cy,rotation=math.pi/2)
        nearby_prop('LOsp',cx+192,cy)
    return dict(paths=paths,path_names=names,ponds=ponds,hills=hills,props=props,
                original_obstacles=obstacles,version=1)


def countryside_pathing(original,plan,terrain=None):
    """Only new basins/cliff edges/ramps and new solid props alter WPM."""
    if original[:4]!=b'MP3W' or struct.unpack_from('<III',original,4)!=(0,768,768):
        raise ValueError('Requires preserved 192-cell pathing grid')
    data=bytearray(original)
    for row in range(768):
        y=ORIGIN+row*32+16
        for col in range(768):
            x=ORIGIN+col*32+16;idx=16+row*768+col
            for pond in plan['ponds']:
                if inside(x,y,pond,256):
                    watered=inside(x,y,pond,32)
                    if terrain is not None:
                        c,r=col//4,row//4
                        corners=[terrain[69+((r+dr)*193+c+dc)*8:77+((r+dr)*193+c+dc)*8]
                                 for dc,dr in ((0,0),(1,0),(0,1),(1,1))]
                        watered=any(has_water(t) for t in corners) and terrain_height(terrain,x,y)<pond['surface']-8
                    if watered:data[idx]=(data[idx]&~64)|2|8
            for hill in plan['hills']:
                distance=math.hypot(x-hill['x'],y-hill['y'])
                if distance>hill['radius']+256:continue
                if terrain is not None:
                    c,r=col//4,row//4
                    corners=[terrain[69+((r+dr)*193+c+dc)*8:77+((r+dr)*193+c+dc)*8]
                             for dc,dr in ((0,0),(1,0),(0,1),(1,1))]
                    layers=[t[7]&15 for t in corners]
                    edge=max(layers)!=min(layers)
                    if edge and not all(has_ramp(t) for t in corners):data[idx]|=2|8
                    else:data[idx]&=~2
                    continue
                ramp=abs(x-hill['x'])<=hill.get('ramp_width',640)/2 and hill['y']-704<=y<=hill['y']+64
                if hill['radius']-128<=distance<=hill['radius']+160 and not ramp:data[idx]|=2|8
                if ramp and distance<hill['radius']+224:data[idx]&=~2
    for prop in plan.get('props',[]):
        radius={'YOec':48,'LOlp':48,'YObw':80,'LOcb':80,'LTlt':80,'LRrk':80}.get(prop['type_id'],0)
        if not radius:continue
        for row in range(max(0,int((prop['y']-radius-ORIGIN)//32)),min(768,int((prop['y']+radius-ORIGIN)//32)+1)):
            for col in range(max(0,int((prop['x']-radius-ORIGIN)//32)),min(768,int((prop['x']+radius-ORIGIN)//32)+1)):
                if protected(ORIGIN+col*32+16,ORIGIN+row*32+16):continue
                data[16+row*768+col]|=2|8
    return bytes(data)
