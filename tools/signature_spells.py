"""Additional, automatically granted signature spells in hero-selector order."""
SIGNATURES = [
 ('Dawn Verdict','HolyBolt',80,100,0,0,0,0,'Damages enemies and heals defending troops, regardless of race.'),
 ('Runebreaker','ThunderClap',180,0,0,0,0,1,'Deals area damage and slows enemies by 20% for 2 seconds.'),
 ('Sanctuary of Hope','Heal',0,220,60,0,0,0,'Restores health and mana to defending troops of every race.'),
 ('Phoenix Flare','HeroAvatarOfFlame',280,0,0,0,0,0,'Unleashes a concentrated burst of fire on the target area.'),
 ('Steel Tempest','StormOfSteel',180,0,0,0,0,2,'Slices enemies in the area and restores 150 health to the caster.'),
 ('Stormpack','SpiritWolf',90,0,0,'osw1',2,0,'Strikes enemies and calls two spirit wolves for 25 seconds.'),
 ('Ancestral Reckoning','WarStomp',120,120,0,0,0,0,'Damages enemies while restoring nearby defending troops.'),
 ('Serpent Communion','SerpentWard',0,150,0,'osp1',2,0,'Heals defending troops and summons two serpent wards for 25 seconds.'),
 ('Fel Hunger','ManaBurn',130,0,0,0,0,3,'Damages enemies, draining up to 40 mana from each and restoring the drained mana to you.'),
 ('Grove Awakening','ForceOfNature',0,0,0,'efon',3,0,'Summons three Treants for 25 seconds on open ground. No trees required.'),
 ('Moonwell Convergence','Starfall',120,160,0,0,0,0,'Moonlight damages enemies and heals defending troops in the same area.'),
 ('Umbral Harvest','FanOfKnives',230,0,0,0,0,2,'Cuts through the target area and restores 150 health to the caster.'),
 ('Soul Covenant','DeathCoil',150,180,0,0,0,0,'Damages enemies and heals defending troops, including both living and undead allies.'),
 ('Winters Grasp','Frost',200,0,0,0,0,1,'Deals frost damage and slows enemies by 20% for 2 seconds.'),
 ('Black Hunt','TheBlackArrow',100,0,0,'nska',2,0,'Damages enemies and summons two skeletal archers for 25 seconds.'),
 ("Ilastar's Last Light",'HolyBolt',240,200,0,0,0,0,'A final flare of holy light damages nearby foes and restores defending allies of every race.'),
 ('Cleansing Pyre','DispelMagic',200,150,0,0,0,0,'Consecrated fire burns enemies while renewing nearby allied heroes and troops.'),
]

from hero_catalog import NEW_HEROES
SIGNATURES.extend(entry['signature'] for entry in NEW_HEROES)

def spell_id(index):return 'AK'+str(index).zfill(2)

def description(entry):
    name,icon,damage,heal,mana,summon,count,extra,flavor=entry
    text=flavor+'|n700 cast range; 350 effect radius. 70 mana, 30-second cooldown.'
    if damage:text+=f'|nDamage: {damage} + 20 per hero level.'
    if heal:text+=f'|nHealing: {heal} + 15 per hero level. Heals King Aldric and defending allies; excludes buildings.'
    if mana:text+=f'|nRestores {mana} mana per allied unit.'
    if summon:text+='|nSummons: 300 + 30 health per hero level; 12 + 2 base damage per hero level.'
    return text

def spell_records(ability):
    records=[]
    for i,e in enumerate(SIGNATURES):
        if i == 21:  # Selyra: native point-targeted, single-wave area damage.
            records.append(ability('ANrf', spell_id(i), [
                ('anam',3,0,0,e[0]),('aher',0,0,0,0),('aite',0,0,0,0),('alev',0,0,0,1),
                ('areq',3,0,0,''),('aart',3,0,0,'ReplaceableTextures\\CommandButtons\\BTNStarfall.dds'),
                ('abpx',0,0,0,2),('abpy',0,0,0,1),('ahky',3,0,0,'Z'),
                ('atp1',3,1,0,e[0]+' (Z)'),
                ('aub1',3,1,0,description(e)+'|nA single native spell wave delivers the impact.'),
                ('amcs',0,1,0,70),('acdn',2,1,0,30.0),('aran',2,1,0,700.0),
                ('aare',2,1,0,350.0),('atar',3,1,0,'air,ground,enemy,nonstructure'),
                ('adur',2,1,0,0.0),('ahdu',2,1,0,0.0),
                ('Hbz1',0,1,1,1),('Hbz2',2,1,2,float(e[2])),('Hbz3',0,1,3,6),
                ('Hbz4',2,1,4,0.5),('Hbz5',2,1,5,0.0),('Hbz6',2,1,6,1000000.0),
            ]))
            continue
        records.append(ability('ANcl',spell_id(i),[
          ('anam',3,0,0,e[0]),('aher',0,0,0,0),('aite',0,0,0,0),('alev',0,0,0,1),
          ('areq',3,0,0,''),('aart',3,0,0,'ReplaceableTextures\\CommandButtons\\BTN'+e[1]+'.dds'),
          ('abpx',0,0,0,2),('abpy',0,0,0,1),('ahky',3,0,0,'Z'),
          ('atp1',3,1,0,e[0]+' (Z)'),('aub1',3,1,0,description(e)),
          ('amcs',0,1,0,70),('acdn',2,1,0,30.0),('aran',2,1,0,700.0),
          ('Ncl1',2,1,1,0.0),('Ncl2',0,1,2,2),('Ncl3',0,1,3,1),('Ncl4',2,1,4,0.0),
          ('Ncl5',0,1,5,0),('Ncl6',3,1,6,'channel')]))
    return records

def spell_script():
    lines=['function KLS_SignatureData takes nothing returns nothing']
    for i,e in enumerate(SIGNATURES):
        lines += [f"    set KLS_SignatureId[{i}] = '{spell_id(i)}'",f'    set KLS_SignatureName[{i}] = "{e[0]}"',
         f'    set KLS_SignatureDescription[{i}] = "{description(e)}"']
        for field,value in zip(('Damage','Heal','Mana','Summon','Count','Extra'),e[2:8]):
            value="'"+value+"'" if isinstance(value,str) else str(value)
            lines.append(f'    set KLS_Signature{field}[{i}] = {value}')
    return '\n'.join(lines+['endfunction'])
