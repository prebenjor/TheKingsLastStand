"""Apply the forest catalog through Forge's documented MCP JSON-RPC bridge.

Uses the same loopback NDJSON API as the installed MCP server. Every mutation
is sequential, undo-aware and checkpointed; authentication is never printed.
"""
import json
import socket
from pathlib import Path
from forest_catalog import forest_plan, CAMPS


def apply_forest(lock_path, expected_folder):
    folder = Path(expected_folder).resolve()
    checkpoint = folder / 'forest-application.json'
    state = json.loads(checkpoint.read_text()) if checkpoint.exists() else {'cliffs':0,'clearings':0,'trail':0,'trees':0,'rocks':0,'camps':0}
    lock = json.loads(Path(lock_path).read_text())
    with socket.create_connection(('127.0.0.1', lock['port']), timeout=30) as connection:
        reader = connection.makefile('rb')
        request_id = 0
        def call(method, params=None):
            nonlocal request_id
            request_id += 1
            request = {'jsonrpc':'2.0','id':request_id,'method':method,
                       'params':dict(params or {}, _token=lock['token'])}
            connection.sendall(json.dumps(request).encode()+b'\n')
            reply = json.loads(reader.readline())
            if reply.get('id') != request_id or 'error' in reply:
                raise ValueError('Forge operation failed: '+method+' '+str(reply.get('error',{}).get('message','')))
            return reply['result']
        ping = call('bridge.ping')
        if Path(ping.get('map_path','')).resolve() != folder:
            raise ValueError('Forge must have the dedicated forest folder open')
        history = call('history.list')
        if not history.get('open_group_depth'):
            call('history.begin_group',{'label':'Northern forest paths and loot coves'})
        plan = forest_plan()
        def record():
            checkpoint.write_text(json.dumps(state,indent=2),encoding='utf-8')
        for i in range(state.get('cliffs',0),len(plan['cliffs'])):
            cliff = plan['cliffs'][i]
            call('terrain.brush_cliff',dict(col=round((cliff['x']+12288)/128),row=round((cliff['y']+12288)/128),
                 mode='set',level=3,radius=cliff['radius'],cliff_tile_id='CLdi'))
            state['cliffs']=i+1
            record()
        for i in range(state.get('clearings',0),len(CAMPS)):
            camp=CAMPS[i]
            call('terrain.paint_tile',dict(col=round((camp['x']+12288)/128),row=round((camp['y']+12288)/128),
                 ground_tile_id='Ldro',radius=4.5,shape='circle'))
            state['clearings']=i+1
            record()
        # Paths are painted last so each cove entrance joins the trail.
        if state.get('saved') and state.get('trail'):
            state['trail']=0
        for group in ('trail','trees','rocks'):
            for i in range(state[group],len(plan[group])):
                entry = plan[group][i]
                if group=='trail':
                    call('terrain.paint_tile',dict(col=round((entry['x']+12288)/128),
                         row=round((entry['y']+12288)/128),ground_tile_id='Ldrt',radius=.9+(i%3)*.15,shape='circle'))
                else:
                    call('doodads.create',entry)
                state[group] = i+1
                record()
            print(group+': '+str(state[group]),flush=True)
        for i in range(state['camps'],len(CAMPS)):
            camp = CAMPS[i]
            for prefix,base,name in (('L',camp['leader'],camp['name']+' Guardian'),
                                      ('M',camp['guard'],camp['name']+' Defender')):
                raw = f'k{prefix}{i:02d}'
                call('objects.units.create_custom',{'base_id':base,'id':raw})
                fields = {'name':name,'requires':'','bountyplus':'0','bountydice':'0','bountysides':'0'}
                if prefix=='L':
                    fields.update(hp=str((900,1200,1600,2200)[i]),dmgplus1=str((20,26,35,45)[i]),
                                  ubertip='Defeat this camp leader for personal '+('Common' if camp['quality']==0 else 'Uncommon')+' equipment and healing supplies.')
                for key,value in fields.items():
                    call('objects.units.set_field',{'id':raw,'column':key,'value':value})
            for raw,x,y in ((f'kL{i:02d}',camp['x'],camp['y']+120),
                            (f'kM{i:02d}',camp['x']-220,camp['y']-100),
                            (f'kM{i:02d}',camp['x']+220,camp['y']-100)):
                # Disposable editor markers are replaced by guarded native camps.
                call('units.create',dict(type_id=raw,player=26,x=x,y=y,rotation=4.712389,scale=1))
            state['camps'] = i+1
            record()
            print('Camp: '+camp['name'],flush=True)
        call('history.end_group')
        call('map.save')
        state['saved'] = True
        record()
    return state
