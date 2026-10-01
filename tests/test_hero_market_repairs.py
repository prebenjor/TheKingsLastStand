import sys
import unittest
import struct
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'tools'))
from hero_progression import MAX_SPELL_RANK, HERO_ABILITIES, _ability_tables, _modification_fields
from equipment_catalog import ENEMY_POTION_THRESHOLDS_PER_1000, catalog_script
from test_backpack_panel import compile_handler
from types import SimpleNamespace
from objects import items,units
from editor_workshop import decode_objects

ROOT = Path(__file__).resolve().parents[1]

class HeroMarketRepairs(unittest.TestCase):
    def test_new_version_two_objects_receive_version_three_set_header(self):
        from hero_market_handoff import merge_objects, object_rows
        baseline = struct.pack('<III', 3, 0, 0)
        generated = struct.pack('<II', 2, 0) + struct.pack('<I', 1) + b'efonbT10' + struct.pack('<I', 0)
        result, _ = merge_objects(baseline, generated, {'bT10': None})
        self.assertEqual(result, struct.pack('<III', 3, 0, 1) + b'efonbT10' + struct.pack('<III', 1, 0, 0))
        self.assertEqual(object_rows(result)[1][1][0]['extras'], [0])

    def test_ten_ranks_preserve_native_costs_and_bound_percentages(self):
        self.assertEqual(MAX_SPELL_RANK, 10)
        headers, data, metadata = _ability_tables()
        for spell in sorted({a for kit in HERO_ABILITIES.values() for a in kit} - {'AKfn'}):
            fields = _modification_fields(spell, data[spell], headers, metadata)
            cap = next(v for f,t,l,p,v in fields if f == 'alev')
            if cap != 10:
                continue
            for field in ('amcs','acdn','aran','adur','ahdu'):
                values = {l:v for f,t,l,p,v in fields if f == field}
                if values:
                    self.assertEqual(values[10], values[5], (spell,field))
            for f,t,l,p,v in fields:
                if f in ('Eev1','Hbh1','hsa1'):
                    self.assertLessEqual(v, 95 if f == 'Hbh1' else .95, (spell,f,l))

    def test_rare_consumables_and_tome_stock(self):
        self.assertEqual(ENEMY_POTION_THRESHOLDS_PER_1000, {'normal':10,'elite':20,'boss':50})
        stock = catalog_script().split('function KLS_StockCatalog')[1].split('endfunction')[0]
        for line in stock.splitlines():
            if 'KLS_Shops[11]' in line:
                self.assertIn('99, 99', line)

    def test_king_healing_and_purchase_handle_safety(self):
        signature = (ROOT/'source/signatures.j').read_text()
        self.assertIn('u == KLS_King', signature)
        combat = (ROOT/'source/combat.j').read_text()
        equip = combat.split('function KLS_MarketEquipPurchased')[1].split('endfunction')[0]
        self.assertNotIn('CreateItem', equip)
        self.assertNotIn('UnitAddItemToSlotById', equip)
        self.assertIn('UnitHasItemEquipped', equip)
        self.assertIn('rawcode, 99, 99', combat)

    def test_signature_healing_target_matrix(self):
        script=(ROOT/'source/signatures.j').read_text()
        from signature_spells import SIGNATURES
        for index,signature in enumerate(SIGNATURES):
            if signature[3] <= 0:continue
            for level in (1,50):
                for king_life in (0,500,1000):
                    hero=SimpleNamespace(owner=0,life=1000,maximum=1000,structure=False)
                    king=SimpleNamespace(owner=15,life=king_life,maximum=1000,structure=False)
                    ally=SimpleNamespace(owner=1,life=100,maximum=1000,structure=False)
                    neutral=SimpleNamespace(owner=15,life=100,maximum=1000,structure=False)
                    building=SimpleNamespace(owner=0,life=100,maximum=1000,structure=True)
                    enemy=SimpleNamespace(owner=11,life=1000,maximum=1000,structure=False)
                    targets=[king,ally,neutral,building,enemy];hits=[]
                    env=dict(KLS_Hero={0:hero},KLS_Active={0:True},KLS_Ended=False,KLS_King=king,KLS_HeroCount=25,
                        KLS_SignatureId={i:f'AK{i:02d}' for i in range(25)},KLS_SignatureName={index:signature[0]},
                        KLS_SignatureHeal={index:signature[3]},KLS_SignatureMana={index:0},KLS_SignatureDamage={index:signature[2]},KLS_SignatureExtra={index:0},KLS_SignatureCount={index:0},
                        GetTriggerUnit=lambda:hero,GetOwningPlayer=lambda u:u.owner,GetPlayerId=lambda p:p,GetHeroLevel=lambda u:level,
                        GetSpellTargetX=lambda:0,GetSpellTargetY=lambda:0,GetSpellAbilityId=lambda:f'AK{index:02d}',
                        KLS_Log=lambda *a:None,I2S=str,DestroyEffect=lambda *a:None,AddSpecialEffect=lambda *a:None,AddSpecialEffectTarget=lambda *a:None,
                        CreateGroup=lambda:targets,GroupEnumUnitsInRange=lambda *a:None,FirstOfGroup=lambda g:g[0] if g else None,
                        GroupRemoveUnit=lambda g,u:g.remove(u),DestroyGroup=lambda *a:None,GetWidgetLife=lambda u:u.life,
                        IsUnitType=lambda u,t:u.structure,UNIT_TYPE_STRUCTURE=0,IsUnitEnemy=lambda u,p:u.owner==11,
                        IsUnitAlly=lambda u,p:u.owner!=11,BlzGetUnitMaxHP=lambda u:u.maximum,RMinBJ=min,
                        SetWidgetLife=lambda u,v:setattr(u,'life',v),UnitDamageTarget=lambda *a:hits.append(a),
                        ATTACK_TYPE_MAGIC=0,DAMAGE_TYPE_MAGIC=0)
                    compile_handler(script,'KLS_SignatureCast',env);env['KLS_SignatureCast']()
                    self.assertEqual(king.life,min(1000,king_life+signature[3]+15*level) if king_life>.405 else king_life)
                    self.assertEqual(ally.life,min(1000,100+signature[3]+15*level))
                    self.assertEqual(neutral.life,100);self.assertEqual(building.life,100)
                    self.assertEqual(len(hits),int(signature[2]>0))

    def test_purchase_retries_keep_one_handle_for_inventory_states(self):
        script=(ROOT/'source/combat.j').read_text()
        for location in ('inventory','backpack','equipped','lost'):
            for succeeds in (False,True):
                buyer=object();gear=object();calls=[];retries=[];state={'equipped':location=='equipped','attempt':0}
                def equip(u,i):
                    self.assertIs(i,gear);calls.append(i)
                    if succeeds:state['equipped']=True
                    return succeeds
                env=dict(GetExpiredTimer=lambda:7,GetHandleId=lambda t:t,LoadUnitHandle=lambda *a:buyer,LoadItemHandle=lambda *a:gear,
                    LoadInteger=lambda h,k,f:state['attempt'] if f==22 else 1,KLS_GearData=object(),GetOwningPlayer=lambda u:0,GetPlayerId=lambda p:p,
                    GetItemTypeId=lambda i:100,KLS_Hero={0:buyer},GetWidgetLife=lambda u:100,
                    UnitHasItemEquipped=lambda u,i:state['equipped'],GetItemUserData=lambda i:1 if location!='lost' else 2,
                    UnitHasItem=lambda u,i:location=='inventory',UnitHasItemBagged=lambda u,i:location=='backpack',UnitEquipItem=equip,
                    KLS_Log=lambda *a:None,KLS_MarketEquipContext=lambda *a:'',SaveInteger=lambda h,k,f,v:state.update(attempt=v),
                    SaveItemHandle=lambda *a:None,TimerStart=lambda *a:retries.append(a),FlushChildHashtable=lambda *a:None,
                    PauseTimer=lambda *a:None,DestroyTimer=lambda *a:None,DisplayTimedTextToPlayer=lambda *a:None)
                compile_handler(script,'KLS_MarketEquipPurchased',env)
                for _ in range(10):env['KLS_MarketEquipPurchased']()
                self.assertTrue(all(i is gear for i in calls))
                if location in ('equipped','lost'):self.assertEqual(calls,[])
                elif succeeds:self.assertEqual(len(calls),1)
                else:self.assertEqual(state['attempt'],8)

    def test_stock_objects_and_hero_skin_lists(self):
        data=decode_objects(items())
        self.assertEqual(data['custom/KHE1/istr/0/0']['value'],1)
        self.assertEqual(data['custom/KHE1/isto/0/0']['value'],1)
        data=decode_objects(units())
        for hero,kit in HERO_ABILITIES.items():
            prefix=('custom/' if 'custom/'+hero+'/base' in data else 'original/')+hero+'/'
            self.assertEqual(data[prefix+'uhab/0/0']['value'],data[prefix+'uhas/0/0']['value'])
            self.assertEqual(data[prefix+'uabi/0/0']['value'],data[prefix+'uabs/0/0']['value'])

    def test_duplicate_wave_death_rolls_loot_once(self):
        dead=object();enemies={dead};drops=[]
        env=dict(GetTriggerUnit=lambda:dead,KLS_Ended=False,KLS_King=object(),KLS_StoryCart=None,KLS_StoryEnemies=set(),
            IsUnitInGroup=lambda u,g:u in g,KLS_IsForestMonster=lambda t:False,GetUnitTypeId=lambda u:1,
            KLS_Enemies=enemies,GroupRemoveUnit=lambda g,u:g.remove(u),KLS_Alive=3,KLS_AwardKillXP=lambda *a:None,
            KLS_AwardBounty=lambda *a:None,GetKillingUnit=lambda:None,KLS_EnemyBounty=lambda u:1,
            KLS_EnemyDrop=lambda *a:drops.append(a),KLS_Boss=None,KLS_Hero={i:None for i in range(4)},KLS_Respawn={})
        compile_handler((ROOT/'source/game.j').read_text(),'KLS_Death',env)
        env['KLS_Death']();env['KLS_Death']()
        self.assertEqual(len(drops),1);self.assertEqual(env['KLS_Alive'],2)

    def test_castle_heal_payment_refund_and_shared_cooldown(self):
        king=SimpleNamespace(life=1000,maximum=10000);resources={0:1000,1:500};clock={'timer':None,'remaining':0}
        env=dict(KLS_King=king,KLS_KingTier=0,KLS_GearData=object(),KLS_Active={0:True},KLS_Ended=False,
            GetPlayerId=lambda p:p,GetWidgetLife=lambda u:u.life,BlzGetUnitMaxHP=lambda u:u.maximum,GetHandleId=lambda u:1,
            LoadTimerHandle=lambda *a:clock['timer'],TimerGetRemaining=lambda t:clock['remaining'],
            PLAYER_STATE_RESOURCE_GOLD=0,PLAYER_STATE_RESOURCE_LUMBER=1,GetPlayerState=lambda p,k:resources[k],
            SetPlayerState=lambda p,k,v:resources.update({k:v}),DisplayTimedTextToPlayer=lambda *a:None,
            SetWidgetLife=lambda u,v:setattr(u,'life',v),RMinBJ=min,R2I=int,I2S=str,KLS_Log=lambda *a:None,KLS_HUDUpdate=lambda:None,
            CreateTimer=lambda:object(),SaveTimerHandle=lambda h,k,f,t:clock.update(timer=t),
            TimerStart=lambda t,d,repeat,fn:clock.update(remaining=d))
        script=(ROOT/'source/castle.j').read_text()
        compile_handler(script,'KLS_KingRefund',env);compile_handler(script,'KLS_KingContribute',env)
        env['KLS_KingContribute'](0,False,0,False)
        self.assertEqual((king.life,resources[0],resources[1]),(3000,850,450))
        self.assertEqual(clock['remaining'],1)
        # Native stock already charged the second purchase; a shared cooldown refunds it.
        resources.update({0:700,1:400});env['KLS_KingContribute'](0,False,0,True)
        self.assertEqual((king.life,resources[0],resources[1]),(3000,850,450))
        clock['remaining']=0;king.life=10000
        env['KLS_KingContribute'](0,False,0,False)
        self.assertEqual((resources[0],resources[1]),(850,450))
        king.life=0;env['KLS_KingContribute'](0,False,0,False)
        self.assertEqual(king.life,0)

if __name__ == '__main__':
    unittest.main()
