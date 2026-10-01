"""Targeted, preservation-first hero/market editor handoff through Forge MCP."""
import hashlib
import json
import re
import shutil
import socket
import struct
from pathlib import Path
from editor_workshop import Reader, read_map, decode_objects
from archive_pack import pack

def object_rows(data, extended=False):
    r=Reader(data); version=r.number(); tables=[]
    if version not in (2,3): raise ValueError('Unsupported object version')
    for _ in range(2):
        rows=[]
        for _ in range(r.count()):
            base,custom=r.raw(),r.raw(); extras=[]
            if version==3: extras=[r.number() for _ in range(r.count())]
            fields=[]
            for _ in range(r.count()):
                start=r.pos; field,typ=r.raw(),r.number()
                level,pointer=(r.number(),r.number()) if extended else (0,0)
                value=r.string() if typ==3 else r.number('f' if typ in (1,2) else 'i')
                r.raw(); fields.append((field,typ,level,pointer,value,r.data[start:r.pos]))
            rows.append(dict(base=base,custom=custom,extras=extras,fields=fields))
        tables.append(rows)
    r.finish(); return version,tables

def merge_objects(original, generated, selected, extended=False):
    version,tables=object_rows(original,extended); _,updates=object_rows(generated,extended)
    changes=[]
    for table_index,rows in enumerate(updates):
        for incoming in rows:
            identity=incoming['custom'] if incoming['custom']!='\0'*4 else incoming['base']
            if identity not in selected: continue
            allowed=selected[identity]
            fields=[f for f in incoming['fields'] if allowed is None or f[0] in allowed]
            matches=[r for r in tables[table_index] if (r['custom'] if r['custom']!='\0'*4 else r['base'])==identity]
            if not matches:
                target=dict(incoming,fields=[],extras=incoming['extras'] or ([0] if version==3 else []));tables[table_index].append(target)
            elif len(matches)==1: target=matches[0]
            else: raise ValueError('Duplicate object '+identity)
            # Parent conversions require a deliberate selection of all fields.
            if allowed is None: target['base']=incoming['base']
            for field in fields:
                key=(field[0],field[2],field[3])
                prior=[f for f in target['fields'] if (f[0],f[2],f[3])==key]
                if not prior or prior[0][1:5]!=field[1:5]:changes.append(dict(id=identity,field=field[0],type=field[1],level=field[2],pointer=field[3],value=field[4],base=incoming['base']))
                target['fields']=[f for f in target['fields'] if (f[0],f[2],f[3])!=key]+[field]
    out=bytearray(struct.pack('<I',version))
    for rows in tables:
        out.extend(struct.pack('<I',len(rows)))
        for row in rows:
            out.extend((row['base']+row['custom']).encode())
            if version==3:out.extend(struct.pack('<I',len(row['extras']))+b''.join(struct.pack('<i',n) for n in row['extras']))
            out.extend(struct.pack('<I',len(row['fields'])))
            for field in row['fields']:out.extend(field[5])
    decode_objects(bytes(out),extended)
    return bytes(out),changes

def prepare(source,folder):
    from objects import units,items
    from equipment_catalog import abilities,attribute_books
    from hero_catalog import HERO_TYPES,NEW_HEROES
    from hero_progression import HERO_ABILITIES,briar_unit_id
    folder=Path(folder);source=Path(source)
    if folder.exists():raise ValueError('Use a new handoff folder')
    _,contents,build_id=read_map(source)
    folder.mkdir(parents=True)
    sha=hashlib.sha256(source.read_bytes()).hexdigest()
    backup=folder.parents[1]/'backups'/'hero-market'/('20261001-'+sha[:12])
    backup.mkdir(parents=True,exist_ok=True);shutil.copy2(source,backup/source.name)
    for name,data in contents.items():
        if '/' not in name and '\\' not in name:(folder/name).write_bytes(data)
    heroes=list(HERO_TYPES)+[h['unit_id'] for h in NEW_HEROES]
    selections={h:{'uhab','uhas','uabi','uabs'} for h in heroes}
    selections.update({briar_unit_id(r):None for r in range(1,11)})
    w3u,uc=merge_objects(contents['war3map.w3u'],units(),selections)
    w3t,tc=merge_objects(contents['war3map.w3t'],items(),{**{b['rawcode']:{'isto','istr','isst'} for b in attribute_books()},'KHE1':{'isto','istr','isst','utub'}})
    skills={a for kit in HERO_ABILITIES.values() for a in kit}
    w3a,ac=merge_objects(contents['war3map.w3a'],abilities(),{**{a:None for a in skills},**{f'AK{i:02d}':{'aub1'} for i in range(25)}},True)
    # Selyra remains the existing Channel/script signature in this targeted handoff.
    payloads={'war3map.w3u':w3u,'war3map.w3t':w3t,'war3map.w3a':w3a}
    expected=folder/'expected';expected.mkdir()
    for name,data in payloads.items():(expected/name).write_bytes(data)
    plan=dict(source=str(source.resolve()),sha256=sha,build_id=build_id,heroes=heroes,
              changes={'units':uc,'items':tc,'abilities':ac},backup=str(backup.resolve()))
    (folder/'hero-market-plan.json').write_text(json.dumps(plan,indent=2),encoding='utf-8')
    return dict(folder=str(folder.resolve()),changes={k:len(v) for k,v in plan['changes'].items()},baseline=sha)

def apply_mcp(folder,lock_path):
    folder=Path(folder).resolve();plan=json.loads((folder/'hero-market-plan.json').read_text());lock=json.loads(Path(lock_path).read_text())
    with socket.create_connection(('127.0.0.1',lock['port']),timeout=120) as connection:
        reader=connection.makefile('rb');request=0
        def call(method,params=None):
            nonlocal request
            request+=1;connection.sendall(json.dumps(dict(jsonrpc='2.0',id=request,method=method,params=dict(params or {},_token=lock['token']))).encode()+b'\n')
            reply=json.loads(reader.readline())
            if 'error' in reply:raise ValueError(method+': '+str(reply['error']))
            return reply['result']
        if Path(call('bridge.ping')['map_path']).resolve()!=folder:raise ValueError('Open the dedicated hero/market folder first')
        audit=[]
        for hero in plan['heroes']:
            before=call('objects.units.get',{'id':hero})
            call('history.begin_group',{'label':'Hero abilities '+hero})
            for c in plan['changes']['units']:
                if c['id']==hero:call('objects.units.set_field',dict(id=hero,column=c['field'],value=str(c['value'])))
            call('history.end_group');after=call('objects.units.get',{'id':hero})
            audit.append(dict(id=hero,before=before,after=after))
        call('history.begin_group',{'label':'Ten-rank skills, summon definitions, and market stock'})
        for kind in ('units','items','abilities'):
            known=set()
            for c in plan['changes'][kind]:
                if kind=='units' and c['id'] in plan['heroes']:continue
                # Create explicit IDs and set every field; import APIs can report
                # partial failures without raising an RPC error.
                if kind=='units' and c['base']=='efon':
                    if c['id'] not in known:
                        try:call('objects.units.get',dict(id=c['id']))
                        except ValueError as error:
                            if 'no units object' not in str(error):raise
                            call('objects.units.create_custom',dict(base_id='efon',id=c['id']))
                        known.add(c['id'])
                args=dict(id=c['id'],column=c['field'],value=str(c['value']))
                if c['level']:args['level']=c['level']
                call('objects.'+kind+'.set_field',args)
        call('history.end_group');call('map.save')
        (folder/'mcp-hero-audit.json').write_text(json.dumps(audit,indent=2),encoding='utf-8')
        (folder/'mcp-completed.json').write_text(json.dumps(dict(pid=lock['pid'],operations=sum(len(v) for v in plan['changes'].values()))))
    return 'MCP object pass completed'

def package(folder,target):
    from pipeline import runtime_script,compile_script
    from gui_sources import gui_sources
    folder=Path(folder);target=Path(target);plan=json.loads((folder/'hero-market-plan.json').read_text())
    if target.exists():raise ValueError('Preserve existing output')
    if not (folder/'mcp-completed.json').exists():raise ValueError('MCP pass required')
    _,contents,_=read_map(plan['source'])
    if hashlib.sha256(Path(plan['source']).read_bytes()).hexdigest()!=plan['sha256']:raise ValueError('Baseline changed')
    generated,_,_=gui_sources(runtime_script(plan['build_id']))
    names=['KLS_SignatureData','KLS_SignatureCast','KLS_MarketEquipContext','KLS_MarketEquipPurchased','KLS_MarketBuy','KLS_KingContribute','KLS_GearPawned','KLS_EnemyPotionThreshold','KLS_StockCatalog']
    replacements={n:re.search(r'^function '+n+r'\b.*?^endfunction',generated,re.M|re.S)[0] for n in names}
    # Preserve existing AK21 native base and its existing scripted effect delivery.
    replacements['KLS_SignatureCast']=re.sub(r"    if GetSpellAbilityId\(\) == 'AK21' then\n.*?    endif\n",'',replacements['KLS_SignatureCast'],count=1,flags=re.S)
    def refresh(text):
        for name,body in replacements.items():
            pattern=r'^function '+name+r'\b.*?^endfunction'
            if re.search(pattern,text,re.M|re.S):text=re.sub(pattern,lambda _:body,text,count=1,flags=re.M|re.S)
            else:
                at=text.index('function KLS_MarketEquipPurchased')
                text=text[:at]+body+'\n\n'+text[at:]
        # Signatures are assigned in native normal/skin lists, not added twice at selection.
        text=re.sub(r'^\s*call UnitAddAbility\(([^\n]*),\s*(udg_)?KLS_SignatureId\[n\]\)\s*$', '',text,flags=re.M)
        text=re.sub(r'^function KLS_MovePurchaseToRegularInventory\b.*?^endfunction\s*', '',text,flags=re.M|re.S)
        return text
    jass=refresh(contents['war3map.j'].decode('utf-8'))
    wct=contents['war3map.wct'];size_at=wct.index(b'\0',8)+1;size=struct.unpack_from('<I',wct,size_at)[0];at=size_at+4
    header=wct[at:at+size];code=refresh(header.rstrip(b'\0').decode('utf-8')).encode()+header[len(header.rstrip(b'\0')):]
    changed={'war3map.j':jass.encode(),'war3map.wct':wct[:size_at]+struct.pack('<I',len(code))+code+wct[at+size:]}
    for name in ('war3map.w3u','war3map.w3t','war3map.w3a','war3mapSkin.w3u','war3mapSkin.w3t','war3mapSkin.w3a'):
        changed[name]=(folder/'expected'/name).read_bytes()
    check=target.with_suffix('.j');check.write_text(jass,encoding='utf-8');syntax=compile_script(check)
    pack(plan['source'],target,changed);_,after,_=read_map(target)
    for name,data in contents.items():
        if name!='(attributes)' and after[name]!=changed.get(name,data):raise ValueError('Unexpected change '+name)
    report=dict(path=str(target.resolve()),sha256=hashlib.sha256(target.read_bytes()).hexdigest(),baseline_sha256=plan['sha256'],changed_members=list(changed),syntax=syntax,protected_members='All terrain, placements, pathing and unrelated archive members byte-identical',engine_checks='Pending',functions=names)
    target.with_suffix('.json').write_text(json.dumps(report,indent=2),encoding='utf-8');return report

def refresh_expected(folder):
    """Refresh typed payloads after source refinements, including shadowed skin tips."""
    from objects import units,items
    from equipment_catalog import abilities,attribute_books
    from hero_progression import HERO_ABILITIES,briar_unit_id
    folder=Path(folder);plan=json.loads((folder/'hero-market-plan.json').read_text());_,contents,_=read_map(plan['source'])
    units_selection={h:{'uhab','uhas','uabi','uabs'} for h in plan['heroes']}
    units_selection.update({briar_unit_id(r):None for r in range(1,11)})
    item_selection={**{b['rawcode']:{'isto','istr','isst'} for b in attribute_books()},'KHE1':{'isto','istr','isst','utub'}}
    skill_selection={**{a:None for kit in HERO_ABILITIES.values() for a in kit},**{f'AK{i:02d}':{'aub1'} for i in range(25) if i!=21}}
    for kind,suffix,generated,selection,extended in [('units','w3u',units(),units_selection,False),('items','w3t',items(),item_selection,False),('abilities','w3a',abilities(),skill_selection,True)]:
        data,changes=merge_objects(contents['war3map.'+suffix],generated,selection,extended)
        plan['changes'][kind]=changes
        (folder/'expected'/('war3map.'+suffix)).write_bytes(data)
        skin_name='war3mapSkin.'+suffix
        # Numeric gameplay changes stay in main tables; synchronize display/skin fields.
        _,generated_tables=object_rows(generated,extended)
        display_fields={'atp1','aub1','aut1','auu1','uhas','uabs','utub'}
        skin_selection={identity:display_fields & (allowed if allowed is not None else display_fields) for identity,allowed in selection.items()}
        skin_data,_=merge_objects(contents[skin_name],generated,skin_selection,extended)
        (folder/'expected'/skin_name).write_bytes(skin_data)
    (folder/'hero-market-plan.json').write_text(json.dumps(plan,indent=2),encoding='utf-8')
    return 'Typed main and skin payloads refreshed'

def audit_mcp(folder,lock_path):
    from hero_progression import HERO_ABILITIES,SCALABLE_EFFECT_FIELDS
    folder=Path(folder);lock=json.loads(Path(lock_path).read_text());audit={};ui={}
    with socket.create_connection(('127.0.0.1',lock['port']),timeout=120) as connection:
        reader=connection.makefile('rb');n=0
        def call(method,params):
            nonlocal n
            n+=1;connection.sendall(json.dumps(dict(jsonrpc='2.0',id=n,method=method,params=dict(params,_token=lock['token']))).encode()+b'\n');reply=json.loads(reader.readline())
            if 'error' in reply:raise ValueError(reply['error'])
            return reply['result']
        for id in sorted({s for kit in HERO_ABILITIES.values() for s in kit}|{f'AK{i:02d}' for i in range(25)}):
            result=call('objects.abilities.get',dict(id=id));audit[id]=result
            ui[id]=dict(name=result['name'],fields={f['id']:f['display_name'] for f in result['fields'] if f['id'] in SCALABLE_EFFECT_FIELDS.get(id,())})
        units={id:call('objects.units.get',dict(id=id)) for id in HERO_ABILITIES}
    (folder/'mcp-ability-audit.json').write_text(json.dumps(dict(abilities=audit,heroes=units),indent=2),encoding='utf-8')
    (Path(__file__).parent/'hero_ability_ui.json').write_text(json.dumps(ui,indent=2),encoding='utf-8')
    return dict(heroes=len(units),abilities=len(audit))
