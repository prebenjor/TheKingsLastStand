"""Saved-package preservation and static navigation evidence for countryside."""
import hashlib
import json
import math
import re
import struct
from pathlib import Path
from countryside_catalog import protected, inside
from editor_layout import ungroup_forest_units, terrain_height, market_coordinates_from_units
from editor_workshop import Reader, read_map, functions
from forge_countryside import commands
from layout_catalog import MARKET_SQUARE


def doodad_spans(data):
    r=Reader(data)
    if r.take(4)!=b'W3do' or (r.number(),r.number())!=(13,11):
        raise ValueError('Requires native DE doodads 13.11')
    result=[]
    for _ in range(r.count()):
        start=r.pos;raw=r.raw();r.take(32);r.take(4);r.take(10)
        for _ in range(r.count()):r.take(r.count()*8)
        r.take(4)  # Native DEUnknown field precedes creation identity.
        identity=r.number();r.take(8);r.take(r.count()*36)
        result.append((identity,raw,start,r.pos))
    return result,r.pos


def verify_countryside(baseline,target,folder):
    folder=Path(folder);target=Path(target)
    _,before,build_id=read_map(baseline)
    _,after,_=read_map(target)
    plan=json.loads((folder/'countryside-plan.json').read_text())
    allowed={'(attributes)','war3map.doo','war3map.w3e','war3map.wpm',
             'war3mapUnits.doo','war3map.j','war3map.wct'}
    assert set(before)==set(after),'Archive inventory changed'
    changed=[n for n in before if before[n]!=after[n]]
    assert set(changed)<=allowed,'Unapproved content changed'
    assert after['war3mapUnits.doo']==ungroup_forest_units(before['war3mapUnits.doo']),'Unit properties changed beyond target grouping'
    old_spans,old_end=doodad_spans(before['war3map.doo'])
    new_spans,new_end=doodad_spans(after['war3map.doo'])
    assert len(new_spans)==len(old_spans)+len(plan['props']),'Added scenery count differs'
    assert before['war3map.doo'][16:old_end]==after['war3map.doo'][16:old_end],'Original doodad records changed'
    assert before['war3map.doo'][old_end:]==after['war3map.doo'][new_end:],'Special doodads changed'
    for entry,prop in zip(new_spans[len(old_spans):],plan['props']):
        identity,raw,start,end=entry
        x,y,z=struct.unpack_from('<3f',after['war3map.doo'],start+8)
        assert raw==prop['type_id'] and math.dist((x,y),(prop['x'],prop['y']))<1
        assert struct.unpack_from('<i',after['war3map.doo'],start+40)[0]==-1,'New scenery is grouped'
        expected=prop['z'] if raw=='LPlp' else terrain_height(after['war3map.w3e'],x,y)
        assert abs(z-expected)<.1,'Scenery elevation differs from saved terrain'
    geometry=set()
    footprint_plan=dict(plan,paths=plan['paths']+plan.get('legacy_paths',[]))
    for group in commands(footprint_plan).values():
        for method,p in group:
            if not method.startswith('terrain.'):continue
            radius=p.get('radius',0)+.5  # Forge includes half a corner of brush reach.
            for dr in range(-math.ceil(radius),math.ceil(radius)+1):
                for dc in range(-math.ceil(radius),math.ceil(radius)+1):
                    if (p.get('shape')=='square' and max(abs(dc),abs(dr))<=radius
                            or p.get('shape')!='square' and math.hypot(dc,dr)<=radius):
                        geometry.add((p['col']+dc,p['row']+dr))
    corners=[]
    for row in range(193):
        for col in range(193):
            i=row*193+col
            if before['war3map.w3e'][69+i*8:77+i*8]!=after['war3map.w3e'][69+i*8:77+i*8]:
                x,y=col*128-12288,row*128-12288
                assert not protected(x,y),'Protected terrain changed'
                assert (col,row) in geometry,'Terrain changed outside the applied brush footprints'
                corners.append((col,row))
    movement=after['war3map.wpm'];samples=0
    for path in plan['paths']:
        for a,b in zip(path,path[1:]):
            count=max(1,math.ceil(math.dist(a,b)/32))
            for n in range(count+1):
                x=a[0]+(b[0]-a[0])*n/count;y=a[1]+(b[1]-a[1])*n/count
                idx=16+int((y+12288)//32)*768+int((x+12288)//32)
                assert not movement[idx]&2,'New trail center is blocked at '+str((x,y))
                samples+=1
    changed_pixels=0
    for i,(old,new) in enumerate(zip(before['war3map.wpm'][16:],movement[16:])):
        if old==new:continue
        changed_pixels+=1;x=i%768*32-12288+16;y=i//768*32-12288+16
        assert not protected(x,y),'Protected pathing changed'
        assert (any(inside(x,y,p,256) for p in plan['ponds'])
                or any(math.dist((x,y),(h['x'],h['y']))<=h['radius']+256 for h in plan['hills'])
                or any(abs(x-p['x'])<112 and abs(y-p['y'])<112 for p in plan['props'])), 'Pathing changed outside new feature footprints'
    assert market_coordinates_from_units(after['war3mapUnits.doo'])==MARKET_SQUARE,'Saved vendors and source coordinates differ'
    old_functions=functions(before['war3map.j']);new_functions=functions(after['war3map.j'])
    assert set(new_functions)-set(old_functions)<={'KLS_MarketFacing'}
    assert not set(old_functions)-set(new_functions)
    for name,body in old_functions.items():
        if name=='KLS_CreateShops':
            for index in ('tier*2+i','10','11','12'):
                body=body.replace(f'KLS_MarketY({index}),270)',f'KLS_MarketY({index}),KLS_MarketFacing({index}))')
            assert body==new_functions[name],'Vendor stock/service behavior changed'
        elif name not in {'KLS_MarketX','KLS_MarketY','KLS_MarketFacing'}:
            assert body==new_functions[name],'Unrelated runtime function changed: '+name
    for name in ('KLS_MarketX','KLS_MarketY','KLS_MarketFacing'):
        assert new_functions[name].encode() in after['war3map.wct'],'Market runtime/header mismatch'
    report=dict(path=str(target.resolve()),sha256=hashlib.sha256(target.read_bytes()).hexdigest(),
                base_build_id=build_id,changed_members=changed,original_unit_count=151,
                corrected_group_ids=list(range(146,159)),original_doodads=len(old_spans),
                added_doodads=len(plan['props']),terrain_corners_changed=len(corners),
                protected_terrain_changes=0,pathing_pixels_changed=changed_pixels,
                walkable_trail_samples=samples,land_props_match_saved_ground=True,
                vendors_match_source=True,unrelated_runtime_functions_preserved=True,
                limits='Static package checks only; standard World Editor selection and Warcraft gameplay/navigation remain pending')
    target.with_suffix('.preservation.json').write_text(json.dumps(report,indent=2))
    return report
