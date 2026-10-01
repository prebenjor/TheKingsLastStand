"""Approved construction pages and eight timed racial specialists."""
from faction_catalog import FACTIONS

_ROSTER=(
 ('Royal Bulwark','hfoo','Bulwark Formation','armor',4,8),
 ('Field Engineer','hmpr','Field Repairs','repair',300,5),
 ('Spiritguard','otau','Spirit Shock','shock',60,3),
 ('Storm Drummer','okod','Storm Rhythm','haste',.15,6),
 ('Thorn Sentinel','esen','Binding Thorns','root',3,3),
 ('Moonwell Tender','edry','Moonwell Renewal','renewal',150,0),
 ('Bone Warden','uske','Bone Aegis','shield',250,8),
 ('Plague Artificer','umtw','Plague Canister','plague',25,4),
)
SPECIALISTS=[]
for i,(name,parent,power,mechanic,value,duration) in enumerate(_ROSTER):
    support=i%2==1
    SPECIALISTS.append(dict(id=f'rU{i:02d}',ability=f'rP{i:02d}',name=name,parent=parent,
        power=power,mechanic=mechanic,value=value,duration=duration,race=FACTIONS[i//2]['race'],
        race_index=i//2,role='siege_yard' if support else 'hall',support=support,
        gold=350 if support else 300,lumber=125 if support else 100,food=3,
        train_time=30 if support else 25,hp=650 if support else 900,damage=18 if support else 28))

def specialist_unit_fields(s):
    return dict(unam=s['name'],utip='Train '+s['name'],utub=f"{s['race']} specialist. {s['power']}; 40 mana, 20-second cooldown. Trained at your {s['role'].replace('_',' ')}. Uses 3 food.",
        ugol=s['gold'],ulum=s['lumber'],ufoo=3,ubld=s['train_time'],uhpm=s['hp'],ua1b=s['damage'],
        uabi=s['ability'],uabs=s['ability'],ureq='',upgr='',umpm=180,umpi=180,umpr=1.0,ubpx=0,ubpy=0)

def racial_unit_records(record):
    rows=[]
    for f in FACTIONS:
        rows.append(record(f['worker'],f['expansion_worker'],dict(unam=f['race']+' Worker — Expansion',
            ubui=','.join(f['expansion_menu']),ureq='')))
    rows += [record(s['parent'],s['id'],specialist_unit_fields(s)) for s in SPECIALISTS]
    rows.append(record('hpea','rD00',dict(unam='Binding Thorns effect',uabi='Aloc,rRt0',uabs='Aloc,rRt0',umdl='',umvs=0,ucol=0.0,umpm=100,umpi=100,ufoo=0)))
    return rows

def racial_spell_records(ability):
    descriptions=(
        'Living allied troops in 250 range gain 4 armor for 8 seconds. Refreshes without stacking.',
        'Repairs an allied structure for 300 HP over 5 seconds. Cannot repair King Aldric.',
        'Deals 60 magic damage in 250 range; slows enemy movement 20% for 3 seconds.',
        'Living allied troops in 250 range gain 15% attack speed for 6 seconds. Refreshes without stacking.',
        'Roots an enemy for 3 seconds; bosses are rooted for 1 second.',
        'Restores 150 HP and 30 mana to living allied troops in 250 range. Excludes King Aldric and structures.',
        'Absorbs 250 incoming damage over 8 seconds. Refreshes without stacking.',
        'Enemies in 250 range take 25 damage per second for 4 seconds and lose 3 armor. Refreshes without stacking.',
    )
    rows=[]
    rows.append(ability('Aens','rRt0',[
        ('anam',3,0,0,'Binding Thorns effect'),('aher',0,0,0,0),('alev',0,0,0,2),('areq',3,0,0,''),
        ('amcs',0,1,0,0),('amcs',0,2,0,0),('acdn',2,1,0,0.0),('acdn',2,2,0,0.0),
        ('aran',2,1,0,99999.0),('aran',2,2,0,99999.0),('adur',2,1,0,3.0),('ahdu',2,1,0,3.0),
        ('adur',2,2,0,1.0),('ahdu',2,2,0,1.0),('abuf',3,1,0,'rBa0,rBr0'),('abuf',3,2,0,'rBa0,rBr0')]))
    for i,f in enumerate(FACTIONS):
        for identity,target in ((f'rX0{i}',f['expansion_worker']),(f'rS0{i}',f['worker'])):
            rows.append(ability('Sca5',identity,[('anam',3,0,0,'Worker construction page'),('aher',0,0,0,0),('alev',0,0,0,1),('areq',3,0,0,''),('Cha1',3,1,1,target)]))
    rows.append(ability('ANcl','rPg0',[
        ('anam',3,0,0,'Standard / Expansion Construction'),('aher',0,0,0,0),('alev',0,0,0,1),('areq',3,0,0,''),
        ('aart',3,0,0,'ReplaceableTextures\\CommandButtons\\BTNRepair.dds'),('abpx',0,0,0,2),('abpy',0,0,0,2),('ahky',3,0,0,'V'),
        ('atp1',3,1,0,'Standard / Expansion Construction (V)'),('aub1',3,1,0,'Change construction page. Native prototype; finish your current work first.'),
        ('amcs',0,1,0,0),('acdn',2,1,0,0.0),('Ncl1',2,1,1,0.0),('Ncl2',0,1,2,0),('Ncl3',0,1,3,1),('Ncl4',2,1,4,0.0),('Ncl5',0,1,5,0),('Ncl6',3,1,6,'channel')]))
    for i,s in enumerate(SPECIALISTS):
        target=1 if s['mechanic'] in ('repair','root') else 2
        if s['mechanic']=='shield':target=0
        rows.append(ability('ANcl',s['ability'],[
            ('anam',3,0,0,s['power']),('aher',0,0,0,0),('alev',0,0,0,1),('areq',3,0,0,''),
            ('aart',3,0,0,('ReplaceableTextures\\CommandButtons\\BTN'+('Footman','Priest','Tauren','KotoBeast','Huntress','Dryad','SkeletonWarrior','MeatWagon')[i]+'.dds')),
            ('abpx',0,0,0,0),('abpy',0,0,0,2),('ahky',3,0,0,'Q'),
            ('atp1',3,1,0,s['power']+' (Q)'),('aub1',3,1,0,descriptions[i]+' 40 mana; 20-second cooldown.'),
            ('amcs',0,1,0,40),('acdn',2,1,0,20.0),('aran',2,1,0,600.0),('atar',3,1,0,'ground,air,organic,mechanical,structure'),
            ('Ncl1',2,1,1,0.0),('Ncl2',0,1,2,target),('Ncl3',0,1,3,1),
            ('Ncl4',2,1,4,0.0),('Ncl5',0,1,5,0),('Ncl6',3,1,6,'channel')]))
    return rows

def racial_script():
    lines=['function KLS_RacialCatalog takes nothing returns nothing']
    for i,s in enumerate(SPECIALISTS):
        for field,value in [('Id',"'"+s['id']+"'"),('Ability',"'"+s['ability']+"'"),('HP',s['hp']),('Damage',s['damage'])]:
            lines.append(f'    set KLS_Specialist{field}[{i}] = {value}')
    lines.append('endfunction')
    return '\n'.join(lines)

def worker_pages_script():
    lines=['function KLS_WorkerPagesCatalog takes nothing returns nothing']
    for i,f in enumerate(FACTIONS):
        for name,value in [('StandardId',f['worker']),('ExpansionId',f['expansion_worker']),('ToExpansion',f'rX0{i}'),('ToStandard',f'rS0{i}')]:
            lines.append(f"    set KLS_Worker{name}[{i}] = '{value}'")
    return '\n'.join(lines+['endfunction'])
