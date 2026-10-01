"""Read-only preservation evidence for the targeted racial DEVELOPMENT package."""
import hashlib,json,re,struct,sys
from pathlib import Path
from editor_workshop import read_map
from hero_market_handoff import object_rows
from hero_progression import HERO_ABILITIES

def rows(data,extended=False):
    version,tables=object_rows(data,extended)
    assert version==3
    return {(row['custom'] if row['custom']!='\0'*4 else row['base']):row for table in tables for row in table}

def functions(data):
    return dict(re.findall(r'^function (\w+)\b(.*?^endfunction)',data.decode().replace('\r\n','\n'),re.M|re.S))

def verify(folder,target):
    folder=Path(folder);target=Path(target)
    plan=json.loads((folder/'racial-plan.json').read_text())
    manifest=json.loads(target.with_suffix('.json').read_text())
    _,before,_=read_map(plan['source']);_,after,_=read_map(target)
    assert hashlib.sha256(target.read_bytes()).hexdigest()==manifest['sha256']
    changed=set(manifest['changed_members'])|{'(attributes)','(listfile)'}
    protected=[name for name in before if name not in changed]
    for name in protected:assert before[name]==after[name],name
    for path in (folder/'expected').iterdir():
        if manifest['prototype'] and path.suffix=='.w3u':
            from faction_catalog import FACTIONS
            expected=rows(path.read_bytes());actual=rows(after[path.name])
            workers={identity for f in FACTIONS for identity in (f['worker'],f['expansion_worker'])}
            assert expected.keys()==actual.keys()
            for identity in expected:
                a,b=expected[identity],actual[identity]
                if identity not in workers:assert a==b,identity
                else:
                    assert (a['base'],a['custom'],a['extras'])==(b['base'],b['custom'],b['extras'])
                    assert [v for v in a['fields'] if v[0] not in ('uabi','uabs')]==[v for v in b['fields'] if v[0] not in ('uabi','uabs')]
                    assert all('rPg0' in v[4].split(',') for v in b['fields'] if v[0] in ('uabi','uabs'))
        else:assert after[path.name]==path.read_bytes(),path.name
    skills={a for kit in HERO_ABILITIES.values() for a in kit}|{f'AK{i:02d}' for i in range(25)}
    for skin in ('','Skin'):
        for kind,suffix,extended in [('units','w3u',False),('abilities','w3a',True),('buffs','w3h',False)]:
            name=f'war3map{skin}.{suffix}'
            if name not in before:continue
            old_rows=rows(before[name],extended);new_rows=rows(after[name],extended)
            allowed={identity:set(fields or []) for identity,fields in plan['allowed_fields'][kind].items()}
            for identity,row in old_rows.items():
                current=new_rows[identity]
                assert (row['base'],row['custom'],row['extras'])==(current['base'],current['custom'],current['extras']),identity
                permitted=allowed.get(identity,set())
                if manifest['prototype'] and identity in ('hpea','opeo','ewsp','uaco'):permitted=permitted|{'uabi','uabs'}
                field_bytes=lambda record:{(f[0],f[2],f[3]):f[5] for f in record['fields'] if f[0] not in permitted}
                assert field_bytes(row)==field_bytes(current),identity
        for suffix,identities,extended in [('w3u',HERO_ABILITIES,False),('w3a',skills,True)]:
            name=f'war3map{skin}.{suffix}';old=rows(before[name],extended);new=rows(after[name],extended)
            for identity in identities:assert old[identity]==new[identity],identity
    old=functions(before['war3map.j']);new=functions(after['war3map.j'])
    excluded=set(manifest['functions'])
    untouched=[name for name in old if name not in excluded]
    for name in untouched:
        assert old[name].replace(plan['baseline_build_id'],manifest['build_id'])==new[name],name
    wct=after['war3map.wct'];offset=wct.index(b'\0',8)+1;size=struct.unpack_from('<I',wct,offset)[0]
    header=functions(wct[offset+4:offset+4+size].rstrip(b'\0'))
    for name in manifest['functions']:assert new[name]==header[name],name
    report=dict(build_id=manifest['build_id'],sha256=manifest['sha256'],baseline_sha256=plan['sha256'],
        protected_members=protected,unchanged_hero_objects=25,unchanged_hero_abilities=len(skills),
        preserved_runtime_functions=len(untouched),synchronized_runtime_functions=len(manifest['functions']),
        typed_main_skin_payloads='Expected bytes; prototype adds page ability only; version-three headers preserved',
        native_gameplay='Pending: worker handle/cargo, queues, powers, prerequisites and multiplayer',
        known_issues=['Native sale popup discrepancy: actual 12000 payment preserved',
          'Baseline AK21 parent expectation regression','Baseline Human tower tooltip regression'])
    target.with_suffix('.preservation.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
    return report

if __name__=='__main__':print(json.dumps(verify(*sys.argv[1:]),indent=2))
