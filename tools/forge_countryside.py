"""Apply the approved countryside catalog via the documented Forge MCP bridge."""
import json
import math
import socket
from pathlib import Path
from countryside_catalog import countryside_plan, protected
from editor_layout import terrain_height


def drape_land_props(plan,terrain):
    result=dict(plan)
    result['props']=[dict(p,z=terrain_height(terrain,p['x'],p['y']))
                     if p['type_id']!='LPlp' else dict(p) for p in plan['props']]
    return result


def validate_checkpoint(state,pid):
    if state.get('active'):
        raise ValueError('Partial MCP group cannot be replayed safely; restore its saved group boundary before resuming')
    state['session_pid']=pid


def lookout_access_ramps(plan):
    """Follow the fitted approach across the actual cliff edge, keeping plots intact."""
    corners=set()
    for hill in plan['hills']:
        index=plan['path_names'].index(hill['name']+' spur')
        for x,y in plan['paths'][index]:
            if math.dist((x,y),(hill['x'],hill['y']))>hill['radius']+320:continue
            col,row=round((x+12288)/128),round((y+12288)/128)
            for dr in range(-3,4):
                for dc in range(-3,4):
                    c,r=col+dc,row+dr
                    if math.hypot(dc,dr)<=3 and not protected(c*128-12288,r*128-12288):corners.add((c,r))
    return [('terrain.brush_ramp',dict(col=c,row=r,on=True,radius=0)) for c,r in sorted(corners)]


def fit_applied_pond_access(plan):
    """Keep an already-painted shore loop connected around its new water basin."""
    from countryside_catalog import inside
    bypasses=[]
    for pond in plan['ponds']:
        index=plan['path_names'].index(pond['name']+' shore trail')
        old=plan['paths'][index]
        if not any(inside(*p,pond,160) for p in old):continue
        plan.setdefault('legacy_paths',[]).append(old)
        x,y=pond['x'],pond['y']
        anchors=[old[0],(x-1024,y+640),(x-512,y+1024),
                 (x+512,y+1024),(x+1024,y+640),old[-1]]
        path=[]
        for a,b in zip(anchors,anchors[1:]):
            steps=max(1,math.ceil(math.dist(a,b)/128))
            path += [(round(a[0]+(b[0]-a[0])*i/steps),round(a[1]+(b[1]-a[1])*i/steps)) for i in range(steps)]
        path.append(old[-1]);plan['paths'][index]=path;bypasses.append(path)
    return bypasses


def relocate_pathside_props(plan,terrain):
    """Relocate only added scenery when a refined shore trail needs clearance."""
    from countryside_catalog import nearest_distance,inside
    result=dict(plan);result['props']=[dict(p) for p in plan['props']]
    for p in result['props']:
        clearance={'LTlt':384,'LRrk':352,'YOec':320,'LOlp':320,'YObw':352,'LOcb':352}.get(p['type_id'],0)
        touches_plot=any(protected(p['x']+dx,p['y']+dy) for dx in (-112,112) for dy in (-112,112))
        if not clearance or nearest_distance(p['x'],p['y'],plan['paths'])>=clearance and not touches_plot:continue
        cx,cy=p['x'],p['y']
        for _,x,y in sorted((math.hypot(dx,dy),cx+dx,cy+dy) for dx in range(-1024,1025,128) for dy in range(-1024,1025,128)):
            if protected(x,y) or nearest_distance(x,y,plan['paths'])<clearance:continue
            if any(protected(x+dx,y+dy) for dx in (-112,112) for dy in (-112,112)):continue
            if any(inside(x,y,f,192) for f in plan['ponds']+plan['hills']):continue
            if any(math.hypot(x-a,y-b)<r+160 for a,b,r in plan['original_obstacles']):continue
            if any(q is not p and math.hypot(x-q['x'],y-q['y'])<192 for q in result['props']):continue
            p.update(x=x,y=y,z=terrain_height(terrain,x,y));break
        else:raise ValueError('No safe replacement position for added trail-side scenery')
    return result


def commands(plan):
    groups={'Western countryside paths':[], 'Eastern countryside paths':[],
            'Countryside ponds and accessible lookouts':[], 'Countryside supplies and scenery':[]}
    seen=set()
    for path in plan['paths']:
        for i,(x,y) in enumerate(path):
            col,row=round((x+12288)/128),round((y+12288)/128)
            group='Western countryside paths' if x<0 else 'Eastern countryside paths'
            for dc,dr in ((0,0),(-1,0),(1,0),(0,-1),(0,1)):
                c,r=col+dc,row+dr;px,py=c*128-12288,r*128-12288
                if (c,r) in seen or protected(px,py):continue
                seen.add((c,r))
                groups[group].append(('terrain.paint_tile',dict(col=c,row=r,ground_tile_id='Ldrt',radius=0,shape='circle')))
            # Sparse rough-dirt edges break up the clean continuous strip.
            if i%7==3:
                c,r=col-2,row
                if not protected(c*128-12288,r*128-12288) and (c,r) not in seen:
                    groups[group].append(('terrain.paint_tile',dict(col=c,row=r,ground_tile_id='Ldro',radius=0)))
    terrain=groups['Countryside ponds and accessible lookouts']
    for pond in plan['ponds']:
        for x,y,radius in pond['lobes']:
            common=dict(col=round((x+12288)/128),row=round((y+12288)/128),shape='circle')
            terrain.append(('terrain.paint_tile',dict(common,ground_tile_id='Ldro',radius=radius/128+1)))
            terrain.append(('terrain.brush_height',dict(common,mode='lower',strength=32,radius=radius/128+1)))
            terrain.append(('terrain.brush_height',dict(common,mode='flatten',target=pond['floor'],radius=radius/128)))
            terrain.append(('terrain.brush_water',dict(common,mode='add',height=pond['surface'],radius=radius/128)))
    for hill in plan['hills']:
        common=dict(col=round((hill['x']+12288)/128),row=round((hill['y']+12288)/128),shape='circle')
        terrain += [('terrain.brush_height',dict(common,mode='raise',strength=16,radius=5)),
                    ('terrain.brush_height',dict(common,mode='flatten',target=hill['height']-128,radius=4.5)),
                    ('terrain.brush_cliff',dict(common,mode='set',level=3,cliff_tile_id='CLdi',radius=4.5)),
                    ('terrain.brush_ramp',dict(col=common['col'],row=round((hill['ramp'][1]+12288)/128),on=True,radius=2.5,shape='square'))]
    terrain += lookout_access_ramps(plan)
    groups['Countryside supplies and scenery']=[('doodads.create',p) for p in plan['props']]
    return groups


def apply_countryside(lock_path,expected_folder,refine=False):
    folder=Path(expected_folder).resolve()
    plan_path=folder/'countryside-plan.json'
    if not plan_path.exists():plan_path.write_text(json.dumps(countryside_plan(folder),indent=2))
    plan=json.loads(plan_path.read_text())
    groups=commands(plan)
    checkpoint=folder/'countryside-application.json'
    lock=json.loads(Path(lock_path).read_text())
    state=json.loads(checkpoint.read_text()) if checkpoint.exists() else {'completed':[],'active':None,'next':0,'session_pid':lock['pid']}
    validate_checkpoint(state,lock['pid'])
    if refine:
        if len(state['completed'])<4:raise ValueError('Refinement requires the completed first dressing pass')
        for hill in plan['hills']:hill['radius']=576
        bypasses=fit_applied_pond_access(plan)
        plan_path.write_text(json.dumps(plan,indent=2))
        ops=[]
        for hill in plan['hills']:
            common=dict(col=round((hill['x']+12288)/128),row=round((hill['y']+12288)/128),shape='circle',radius=4.5)
            ops += [('terrain.brush_height',dict(common,mode='flatten',target=hill['height']-128)),
                    ('terrain.brush_cliff',dict(common,mode='set',level=3,cliff_tile_id='CLdi'))]
        groups={'Lookout plateau refinement':ops,'Follow lookout approach ramps':lookout_access_ramps(plan),
                'Align countryside props to saved ground':[],'Keep shoreline loop scenery clear':[],
                'Keep player plot borders clear':[]}
        if bypasses:
            bypass_groups=commands(dict(paths=bypasses,path_names=[],hills=[],ponds=[],props=[]))
            groups['Pond shore approach bypasses']=[op for ops in bypass_groups.values() for op in ops]
    with socket.create_connection(('127.0.0.1',lock['port']),timeout=30) as connection:
        reader=connection.makefile('rb');request_id=0
        def call(method,params=None):
            nonlocal request_id
            request_id+=1
            connection.sendall(json.dumps({'jsonrpc':'2.0','id':request_id,'method':method,
                                           'params':dict(params or {},_token=lock['token'])}).encode()+b'\n')
            raw=reader.readline()
            if not raw:raise ValueError('Forge disconnected during '+method)
            reply=json.loads(raw)
            if reply.get('id')!=request_id or 'error' in reply:raise ValueError('Forge operation failed: '+method+' '+str(reply.get('error',{}).get('message','')))
            return reply['result']
        def record():checkpoint.write_text(json.dumps(state,indent=2))
        if Path(call('bridge.ping').get('map_path','')).resolve()!=folder:
            raise ValueError('The dedicated countryside folder must be open in the selected Forge instance')
        for name,operations in groups.items():
            if name in state['completed']:continue
            if name in ('Keep shoreline loop scenery clear','Keep player plot borders clear'):
                previous=plan
                plan=relocate_pathside_props(plan,(folder/'war3map.w3e').read_bytes())
                originals={d['creation_number'] for d in json.loads((folder/'baseline-doodads.json').read_text())}
                added=[d for d in call('doodads.list')['doodads'] if d['creation_number'] not in originals]
                operations=[]
                for old,p in zip(previous['props'],plan['props']):
                    if (old['x'],old['y'])==(p['x'],p['y']):continue
                    matches=[d for d in added if d['type_id']==old['type_id'] and math.dist(d['position'][:2],(old['x'],old['y']))<1]
                    if len(matches)!=1:raise ValueError('Cannot uniquely match added scenery relocation')
                    operations.append(('doodads.move',dict(creation_number=matches[0]['creation_number'],x=p['x'],y=p['y'],z=p['z'])))
                plan_path.write_text(json.dumps(plan,indent=2))
            if name in ('Countryside supplies and scenery','Align countryside props to saved ground'):
                plan=drape_land_props(plan,(folder/'war3map.w3e').read_bytes())
                plan_path.write_text(json.dumps(plan,indent=2))
                if name=='Countryside supplies and scenery':
                    operations=[('doodads.create',p) for p in plan['props']]
                else:
                    originals={d['creation_number'] for d in json.loads((folder/'baseline-doodads.json').read_text())}
                    added=[d for d in call('doodads.list')['doodads'] if d['creation_number'] not in originals]
                    operations=[]
                    for p in plan['props']:
                        matches=[d for d in added if d['type_id']==p['type_id'] and math.dist(d['position'][:2],(p['x'],p['y']))<1]
                        if len(matches)!=1:raise ValueError('Cannot uniquely match added scenery for terrain alignment')
                        operations.append(('doodads.move',dict(creation_number=matches[0]['creation_number'],x=p['x'],y=p['y'],z=p['z'])))
            if not call('history.list').get('open_group_depth'):call('history.begin_group',{'label':name})
            state['active']=name;record()
            try:
                for i in range(state['next'],len(operations)):
                    method,params=operations[i]
                    call(method,params)
                    state['next']=i+1;record()
                    if (i+1)%80==0:print(name+': '+str(i+1)+'/'+str(len(operations)),flush=True)
                call('history.end_group')
                call('map.save')
                state['completed'].append(name);state['active']=None;state['next']=0;record()
                print(name+': saved '+str(len(operations))+' operations',flush=True)
            except Exception:
                if call('history.list').get('open_group_depth'):call('history.end_group')
                raise
    return state
