"""Preservation-first racial repair catalog, MCP pass and native handoff."""
import hashlib,json,re,shutil,socket,struct
from pathlib import Path
from editor_workshop import read_map
from hero_market_handoff import merge_objects,object_rows
from archive_pack import pack
from faction_catalog import FACTIONS
from racial_catalog import SPECIALISTS

class Forge:
    def __init__(self,lock):
        self.lock=json.loads(Path(lock).read_text());self.n=0
    def __enter__(self):
        self.socket=socket.create_connection(('127.0.0.1',self.lock['port']),timeout=120)
        self.reader=self.socket.makefile('rb');return self
    def __exit__(self,*args):self.reader.close();self.socket.close()
    def call(self,method,**params):
        self.n+=1;self.socket.sendall(json.dumps(dict(jsonrpc='2.0',id=self.n,method=method,params=dict(params,_token=self.lock['token']))).encode()+b'\n')
        response=json.loads(self.reader.readline())
        if 'error' in response:raise ValueError(method+': '+str(response['error']))
        return response['result']

def prepare(source,folder,lock):
    folder=Path(folder);source=Path(source)
    if folder.exists():raise ValueError('Use a new versioned folder')
    _,contents,build_id=read_map(source)
    folder.mkdir(parents=True);(folder/'expected').mkdir()
    sha=hashlib.sha256(source.read_bytes()).hexdigest()
    backup=folder.parents[1]/'backups'/'racial'/('20261001-'+sha[:12]);backup.mkdir(parents=True,exist_ok=True)
    shutil.copy2(source,backup/source.name)
    for name,data in contents.items():
        path=folder/name.replace('\\','/');path.parent.mkdir(parents=True,exist_ok=True);path.write_bytes(data)
    capture={}
    with Forge(lock) as api:
        if Path(api.call('bridge.ping')['map_path']).resolve()!=source.resolve():raise ValueError('Open the saved baseline map first')
        ids={id for f in FACTIONS for id in f['standard_menu']+f['expansion_menu']+[f['worker'],f['arcane']]}
        ids.update(('hkee','hcas','ostr','ofrt','etoa','etoe','unp1','unp2','uzg1','uzg2'))
        for identity in sorted(ids):
            result=api.call('objects.units.get',id=identity)
            wanted={'ubui','uabi','uabs','ureq','urqa','utra','ures','uupt','uupg','ubpx','ubpy','ugol','ulum','ubld','ufoo','urac','umdl'}
            capture[identity]=dict(name=result['name'],fields={f['id']:f['value'] for f in result['fields'] if f['id'] in wanted})
    (folder/'building-matrix-before.json').write_text(json.dumps(capture,indent=2),encoding='utf-8')
    plan=dict(source=str(source.resolve()),sha256=sha,baseline_build_id=build_id,backup=str(backup.resolve()),changes={})
    (folder/'racial-plan.json').write_text(json.dumps(plan,indent=2),encoding='utf-8')
    refresh(folder)
    return dict(baseline=sha,folder=str(folder.resolve()),buildings=len(capture))

def refresh(folder):
    from objects import units,racial_buffs,record,table
    from equipment_catalog import abilities
    from company_catalog import HERO_COMPANIES
    folder=Path(folder);plan=json.loads((folder/'racial-plan.json').read_text());_,contents,_=read_map(plan['source'])
    capture=json.loads((folder/'building-matrix-before.json').read_text())
    unit_selection={f['worker']:{'ubui'} for f in FACTIONS}
    unit_selection.update({f['expansion_worker']:None for f in FACTIONS})
    for f in FACTIONS:
        for identity in f['standard_menu']:unit_selection[identity]={'ubpx','ubpy','ureq'}
        unit_selection[f['worker']]={'ubui'}
        unit_selection[f['altar']]={'ubpx','ubpy'}
        for identity in f['expansion_menu']:unit_selection[identity]={'ubpx','ubpy','utra','uabi','uabs'}
    unit_selection.update({s['id']:None for s in SPECIALISTS});unit_selection['rD00']=None
    for e in HERO_COMPANIES:
        unit_selection[e['company_id']]={'ubpx','ubpy'};unit_selection[e['support_id']]={'ubpx','ubpy'}
    # Capture the actual saved/native prerequisite graph and redirect stock
    # altar references without erasing any other native prerequisite.
    altar={f['altar_parent']:f['altar'] for f in FACTIONS}
    rows=[]
    for identity,entry in capture.items():
        requires=entry['fields'].get('ureq','')
        if any(part in altar for part in requires.split(',')):
            rows.append(record(identity,'\0'*4,{'ureq':','.join(altar.get(p,p) for p in requires.split(','))}))
            unit_selection.setdefault(identity,set()).add('ureq')
    generated=units()
    if rows:generated,_=merge_objects(generated,table(rows,[]),{identity:{'ureq'} for identity in unit_selection})
    # Correct the authored Undead tier-two prerequisite role while preserving
    # the rest of that saved graph.
    generated,_=merge_objects(generated,table([record('unp1','\0'*4,{'ureq':'usep,ugrv,kA03'})],[]),{'unp1':{'ureq'}})
    unit_selection['unp1']={'ureq'}
    ability_selection={s['ability']:None for s in SPECIALISTS}
    ability_selection.update({f'r{prefix}0{i}':None for prefix in ('X','S') for i in range(4)})
    ability_selection.update({'rPg0':None,'rRt0':None})
    for kind,suffix,data,selection,extended in [('units','w3u',generated,unit_selection,False),('abilities','w3a',abilities(),ability_selection,True),('buffs','w3h',racial_buffs(),{'rBr0':None,'rBa0':None},False)]:
        for skin in ('','Skin'):
            name=f'war3map{skin}.{suffix}'
            original=contents.get(name,struct.pack('<III',3,0,0))
            _,original_tables=object_rows(original,extended)
            occupied={r['custom'] if r['custom']!='\0'*4 else r['base'] for table in original_tables for r in table}
            collisions={identity for identity,allowed in selection.items() if allowed is None and identity in occupied}
            if collisions:raise ValueError('Reserved IDs collide with baseline: '+str(sorted(collisions)))
            payload,changes=merge_objects(original,data,selection,extended)
            (folder/'expected'/name).write_bytes(payload)
            if not skin:plan['changes'][kind]=changes
    plan['selection']=list(unit_selection)
    plan['allowed_fields']={kind:{identity:sorted(fields) if fields is not None else None for identity,fields in selection.items()}
        for kind,selection in [('units',unit_selection),('abilities',ability_selection),('buffs',{'rBr0':None,'rBa0':None})]}
    (folder/'racial-plan.json').write_text(json.dumps(plan,indent=2),encoding='utf-8')
    return {k:len(v) for k,v in plan['changes'].items()}

def apply(folder,lock):
    folder=Path(folder);plan=json.loads((folder/'racial-plan.json').read_text())
    with Forge(lock) as api:
        if Path(api.call('bridge.ping')['map_path']).resolve()!=folder.resolve():raise ValueError('Open dedicated folder first')
        seen=set()
        groups={}
        for kind,changes in plan['changes'].items():
            for change in changes:
                identity=change['id']
                label='Recruitment buildings and existing companies'
                if kind!='units' or identity.startswith(('rU','rD')):
                    label='Specialist units and powers'
                if identity.startswith(('rW','rX','rS','rPg')):
                    label='Worker page prototype definitions'
                elif kind=='units':
                    for faction in FACTIONS:
                        if identity in [faction['worker']]+faction['standard_menu']:
                            label=faction['race']+' standard construction'
                            break
                groups.setdefault((kind,label),[]).append(change)
        for (kind,label),changes in groups.items():
            api.call('history.begin_group',label=label)
            for change in changes:
                identity=change['id'];pair=(kind,identity)
                if pair not in seen:
                    try:
                        current=api.call('objects.'+kind+'.get',id=identity)
                        if current.get('is_custom') and current.get('base_id')!=change['base']:
                            # Only our newly reserved prototype definitions can
                            # change parent; no saved authored object is deleted.
                            if not identity.startswith('r'):raise ValueError('Unexpected parent migration '+identity)
                            api.call('objects.'+kind+'.delete_custom',id=identity)
                            api.call('objects.'+kind+'.create_custom',base_id=change['base'],id=identity)
                    except ValueError as error:
                        if 'no '+kind+' object' not in str(error):raise
                        api.call('objects.'+kind+'.create_custom',base_id=change['base'],id=identity)
                    seen.add(pair)
                args=dict(id=identity,column=change['field'],value=str(change['value']))
                if change['level']:args['level']=change['level']
                api.call('objects.'+kind+'.set_field',**args)
            api.call('history.end_group')
        api.call('map.save')
    (folder/'mcp-completed.json').write_text(json.dumps(dict(objects=len(seen),changes=sum(len(v) for v in plan['changes'].values()))))
    return dict(objects=len(seen))

def audit(folder,lock):
    from hero_progression import HERO_ABILITIES
    from company_catalog import HERO_COMPANIES
    folder=Path(folder);plan=json.loads((folder/'racial-plan.json').read_text())
    report={'units':{},'abilities':{},'heroes':{}}
    with Forge(lock) as api:
        report['map']=api.call('bridge.ping')['map_path']
        units=set(plan['selection'])|{id for f in FACTIONS for id in f['standard_menu']+f['expansion_menu']}
        units|={id for e in HERO_COMPANIES for id in (e['company_id'],e['support_id'])}
        wanted={'ureq','utra','ures','uupt','uabi','uabs','ubui','ubpx','ubpy','ufoo','ubld','ugol','ulum','uhpm','ua1b'}
        for identity in sorted(units):
            result=api.call('objects.units.get',id=identity)
            report['units'][identity]=dict(name=result['name'],base_id=result.get('base_id'),fields={f['id']:f['value'] for f in result['fields'] if f['id'] in wanted})
        for identity in HERO_ABILITIES:
            result=api.call('objects.units.get',id=identity)
            report['heroes'][identity]=dict(name=result['name'],fields={f['id']:f['value'] for f in result['fields'] if f['id'] in ('uhab','uhas','uabi','uabs')})
        skills={a for kit in HERO_ABILITIES.values() for a in kit}|{f'AK{i:02d}' for i in range(25)}
        skills|={s['ability'] for s in SPECIALISTS}|{code for e in HERO_COMPANIES for code in (e['company_ability'],e['support_ability'])}
        for identity in sorted(skills):
            result=api.call('objects.abilities.get',id=identity)
            report['abilities'][identity]=dict(name=result['name'],base_id=result.get('base_id'),fields=[{k:f[k] for k in ('id','value','display_name')} for f in result['fields'] if f['value']])
    (folder/'mcp-racial-readback.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
    return {k:len(report[k]) for k in ('units','abilities','heroes')}

def package(folder,target,prototype=False):
    from pipeline import runtime_script,compile_script,ROOT
    from gui_sources import gui_sources
    folder=Path(folder);target=Path(target);plan=json.loads((folder/'racial-plan.json').read_text())
    if target.exists():raise ValueError('Existing output is immutable')
    if not (folder/'mcp-completed.json').exists():raise ValueError('MCP application required')
    assert hashlib.sha256(Path(plan['source']).read_bytes()).hexdigest()==plan['sha256']
    _,before,_=read_map(plan['source'])
    identity=hashlib.sha256(b''.join((ROOT/'source'/n).read_bytes() for n in ('racial.j','worker_pages.j','companies.j'))+b''.join(p.read_bytes() for p in sorted((folder/'expected').iterdir()))+bytes([int(prototype)])).hexdigest()[:10]
    build_id='KLS-D-'+identity
    generated,wtg,_=gui_sources(runtime_script(build_id))
    source=before['war3map.j'].decode('utf-8').replace('\r\n','\n')
    # Replace only this subsystem; all market, hero, placement and encounter
    # functions remain baseline-identical.
    names=[m[1] for m in re.finditer(r'^function (KLS_(?:Company|Faction|IsFaction|IsSiegeInvader|Racial|Specialist|Worker)\w*)\b',generated,re.M)]
    existing=set(re.findall(r'^function (\w+)\b',source,re.M))
    bodies={name:re.search(r'^function '+name+r'\b.*?^endfunction',generated,re.M|re.S)[0] for name in names}
    # Racial helpers must precede their callers and company helpers stay in
    # generator dependency order: replace the entire company function block.
    company_names=[n for n in names if n in existing]
    for name in company_names:
        source=re.sub(r'^function '+name+r'\b.*?^endfunction\s*','',source,count=1,flags=re.M|re.S)
    subsystem='\n\n'.join(bodies[n] for n in names)+'\n\n'
    anchor=source.index('function KLS_Mining')
    source=source[:anchor]+subsystem+source[anchor:]
    old_globals=re.search(r'^globals\n(.*?)^endglobals',source,re.M|re.S)[1]
    generated_globals=re.search(r'^globals\n(.*?)^endglobals',generated,re.M|re.S)[1]
    declared=set(re.findall(r'\budg_KLS_\w+',old_globals))
    added=[line for line in generated_globals.splitlines() if (m:=re.search(r'\budg_KLS_\w+',line)) and m[0] not in declared]
    source=source.replace(old_globals,old_globals+'\n'+'\n'.join(added)+'\n',1)
    source=source.replace(plan['baseline_build_id'],build_id)
    # Existing editable header has the same subsystem functions and receives
    # the same replacements, including the new declarations through WTG.
    wct=before['war3map.wct'];at=wct.index(b'\0',8)+1;size=struct.unpack_from('<I',wct,at)[0]
    header=wct[at+4:at+4+size].rstrip(b'\0').decode().replace('\r\n','\n')
    for name in company_names:header=re.sub(r'^function '+name+r'\b.*?^endfunction\s*','',header,count=1,flags=re.M|re.S)
    anchor=header.index('function KLS_Mining');header=header[:anchor]+subsystem+header[anchor:]
    header=header.replace(plan['baseline_build_id'],build_id)
    code=header.encode()+b'\0'
    changed={'war3map.j':source.encode(),'war3map.wct':wct[:at]+struct.pack('<I',len(code))+code+wct[at+4+size:],'war3map.wtg':wtg}
    changed['war3map.w3i']=before['war3map.w3i'].replace(plan['baseline_build_id'].encode(),build_id.encode())
    for path in (folder/'expected').iterdir():changed[path.name]=path.read_bytes()
    if prototype:
        from objects import table,record
        capture=json.loads((folder/'building-matrix-before.json').read_text())
        rows=[]
        for f in FACTIONS:
            native=capture[f['worker']]['fields']['uabi']
            for id in (f['worker'],f['expansion_worker']):
                rows.append(record(f['worker'],'\0'*4 if id==f['worker'] else id,{'uabi':native+',rPg0','uabs':native+',rPg0'}))
        for skin in ('','Skin'):
            name=f'war3map{skin}.w3u'
            edits=table([r for r in rows if r[4:8]==b'\0'*4],[r for r in rows if r[4:8]!=b'\0'*4])
            changed[name],_=merge_objects(changed[name],edits,{id:{'uabi','uabs'} for f in FACTIONS for id in (f['worker'],f['expansion_worker'])})
    script=target.with_suffix('.j');script.write_text(source,encoding='utf-8');syntax=compile_script(script)
    pack(plan['source'],target,changed);_,after,_=read_map(target)
    for name,data in before.items():
        if name=='(listfile)':
            old_names={n.lower() for n in data.decode().splitlines()}
            new_names={n.lower() for n in after[name].decode().splitlines()}
            if not old_names<=new_names or new_names-old_names!={n.lower() for n in changed if n not in before}:raise ValueError('Unexpected archive inventory change')
        elif name!='(attributes)' and after[name]!=changed.get(name,data):raise ValueError('Unexpected archive change '+name)
    report=dict(path=str(target.resolve()),sha256=hashlib.sha256(target.read_bytes()).hexdigest(),build_id=build_id,baseline_sha256=plan['sha256'],prototype=prototype,changed_members=list(changed),syntax=syntax,protected='Terrain, placements, pathing, market, encounters and hero runtime preserved',native_checks='Pending; worker switching not accepted',functions=names)
    target.with_suffix('.json').write_text(json.dumps(report,indent=2),encoding='utf-8');return report
