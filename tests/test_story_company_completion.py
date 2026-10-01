"""Coverage for the town escort, shared unlock and company expansion contract."""
import sys
import unittest
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'tools')); sys.path.insert(0,str(ROOT/'tests'))
import company_catalog
from pipeline import runtime_script
from test_equipment import decode
from equipment_catalog import abilities
from objects import units
from test_backpack_panel import compile_handler
from test_multiplayer_ui_safety import local_allocations

class StoryCompletion(unittest.TestCase):
    def test_caravan_waits_for_a_nearby_living_escort(self):
        cart = dict(x=0.,y=-9000.,life=1800.)
        positions=[]
        env=dict(KLS_StoryCart=cart,KLS_Ended=False,KLS_Selecting=False,
                 KLS_StoryCartClock='clock',KLS_StoryCartSteps=0,KLS_StoryStage=1,
                 KLS_Active=[True]*4,KLS_Hero=[None]*4,KLS_StoryContributor=[False]*16,
                 GetWidgetLife=lambda u:u['life'],GetUnitX=lambda u:u['x'],GetUnitY=lambda u:u['y'],
                 SetUnitX=lambda u,x:positions.append(('x',x)), SetUnitY=lambda u,y:positions.append(('y',y)),
                 IssuePointOrder=lambda *a:positions.append(('move',a)),IssueImmediateOrder=lambda *a:None,
                 PauseTimer=lambda t:None,I2R=float,KLS_StoryComplete=lambda:None,
                 KLS_StoryEscortFailed=lambda:None)
        compile_handler(runtime_script('KLS-D-TEST'),'KLS_StoryCartTick',env)
        env['KLS_StoryCartTick']()
        self.assertEqual(positions,[])
        self.assertEqual(env['KLS_StoryCartSteps'],0)

    def test_story_has_nonmodal_interaction_and_shared_gameplay_unlocks(self):
        script=runtime_script('KLS-D-TEST')
        source=(ROOT/'source/crownlands.j').read_text(encoding='utf-8')
        self.assertNotIn('DialogDisplay',source)
        self.assertIn('function KLS_StoryApplyUnlock',script)
        self.assertIn('function KLS_StoryEscortFailed',script)
        self.assertEqual(local_allocations(script,'KLS_CrownlandsInit'),[])

class CompanyCompletion(unittest.TestCase):
    def test_every_company_and_support_has_an_authored_active(self):
        spells=decode(abilities(),True); records=decode(units())
        for entry in company_catalog.HERO_COMPANIES:
            for role in ('company','support'):
                self.assertIn(role+'_ability',entry)
                code=entry[role+'_ability']; unit=entry[role+'_id']
                self.assertIn(code,spells)
                self.assertIn(code,records[unit][1][('uabi',0)][0])
                self.assertEqual(spells[code][0],'ANcl')

    def test_support_recruits_are_mobile_units(self):
        for entry in company_catalog.HERO_COMPANIES:
            self.assertNotIn(entry['support_parent'],('etrp','etol','etoa','etoe'))

    def test_personal_research_covers_all_building_roles(self):
        self.assertTrue(hasattr(company_catalog,'company_research_catalog'))
        catalog=company_catalog.company_research_catalog()
        self.assertEqual({e['role'] for e in catalog},{'hall','foundry','siege_yard','arcane'})
        self.assertEqual({e['branch'] for e in catalog},{'chapter','weapon','armor','counter_siege','arcane'})
        for branch in ('chapter','weapon','armor'):
            self.assertEqual([e['rank'] for e in catalog if e['branch']==branch],[1,2,3])
        script=runtime_script('KLS-D-TEST')
        self.assertIn('function KLS_CompanyResearchBuy',script)
        self.assertIn('GetOwningPlayer(shop) != Player(p)',script)
        self.assertIn('KLS_CompanyResearchRefresh',script)


class ResearchBehavior(unittest.TestCase):
    def test_chapter_requires_progress_and_next_rank(self):
        env=dict(KLS_CompanyResearchBranch=[0,0,0],KLS_CompanyResearchLevel=[1,2,3],
                 KLS_CompanyResearchRank=[0]*20,KLS_Wave=0,KLS_StoryStage=0)
        compile_handler(runtime_script('KLS-D-TEST'),'KLS_CompanyResearchAllowed',env)
        allowed=env['KLS_CompanyResearchAllowed']
        self.assertFalse(allowed(0,0))
        env['KLS_Wave']=10
        self.assertTrue(allowed(0,0))
        self.assertFalse(allowed(0,1))
        env['KLS_CompanyResearchRank'][0]=1
        env['KLS_StoryStage']=2
        self.assertTrue(allowed(0,1))
        self.assertFalse(allowed(1,1))

    def test_reapplying_upgrades_does_not_stack_or_change_other_players(self):
        unit=dict(owner=0,kind='kC00',hp=900,life=900,damage=34,armor=2.)
        table={}
        ranks=[0]*20
        env=dict(GetPlayerId=lambda p:p,GetOwningPlayer=lambda u:u['owner'],
                 GetUnitTypeId=lambda u:u['kind'],GetHandleId=lambda u:17,
                 KLS_Active=[True]*4,KLS_HeroChoice=[0,0,0,0],
                 KLS_CompanyUnitId=['kC00'],KLS_CompanySupportId=['kS00'],
                 KLS_CompanyUnitHP=[900],KLS_CompanySupportHP=[650],KLS_SpecialistIndex=lambda rawcode:-1,
                 KLS_CompanyUnitDamage=[34],KLS_CompanySupportDamage=[22],
                 KLS_CompanyFoundry=[True,False,False,False],
                 KLS_CompanyResearchRank=ranks,KLS_CompanyUpgradeData=table,
                 LoadInteger=lambda t,k,f:t.get((k,f),0),
                 SaveInteger=lambda t,k,f,v:t.__setitem__((k,f),v),
                 SetUnitUserData=lambda u,d:u.__setitem__('user_data',d),
                 GetWidgetLife=lambda u:u['life'],I2R=float,R2I=int,RMinBJ=min,
                 BlzGetUnitMaxHP=lambda u:u['hp'],
                 BlzSetUnitMaxHP=lambda u,v:u.__setitem__('hp',v),
                 SetWidgetLife=lambda u,v:u.__setitem__('life',v),
                 BlzGetUnitBaseDamage=lambda u,i:u['damage'],
                 BlzSetUnitBaseDamage=lambda u,v,i:u.__setitem__('damage',v),
                 UNIT_RF_DEFENSE='armor',BlzGetUnitRealField=lambda u,f:u[f],
                 BlzSetUnitRealField=lambda u,f,v:u.__setitem__(f,v))
        compile_handler(runtime_script('KLS-D-TEST'),'KLS_CompanyApplyUpgrades',env)
        apply=env['KLS_CompanyApplyUpgrades']
        apply(unit); apply(unit)
        self.assertEqual((unit['hp'],unit['damage']), (1080,40))
        ranks[0]=1; ranks[1]=2; ranks[2]=1
        apply(unit); snapshot=dict(unit); apply(unit)
        self.assertEqual(unit,snapshot)
        self.assertEqual((unit['hp'],unit['damage'],unit['armor']), (1215,49,4))
        other=dict(owner=1,kind='kC00',hp=900,life=900,damage=34,armor=2.)
        env['GetHandleId']=lambda u:18
        apply(other)
        self.assertEqual((other['hp'],other['damage'],other['armor']), (900,34,2))

    def test_research_wrong_owner_refunds_and_duplicate_rank_cannot_reapply(self):
        hero=dict(owner=0,x=0.,y=0.,life=100.)
        shop=dict(owner=1,x=0.,y=0.)
        removed=[];updates=[];resources={('gold',0):0,('wood',0):0}
        env=dict(KLS_CompanyServiceIndex=lambda i:0,GetItemTypeId=lambda i:'KW01',
                 GetPlayerId=lambda p:p,GetOwningPlayer=lambda u:u['owner'],Player=lambda p:p,
                 GetUnitX=lambda u:u['x'],GetUnitY=lambda u:u['y'],GetWidgetLife=lambda u:u['life'],
                 KLS_Ended=False,KLS_Active=[True]*4,KLS_Hero=[hero,None,None,None],
                 KLS_CompanyResearchRole=[1],KLS_CompanyResearchGold=[350],KLS_CompanyResearchLumber=[100],
                 KLS_CompanyResearchBranch=[1],KLS_CompanyResearchLevel=[1],KLS_CompanyResearchRank=[0]*20,
                 KLS_CompanyBuildingRole=lambda s:1,PLAYER_STATE_RESOURCE_GOLD='gold',PLAYER_STATE_RESOURCE_LUMBER='wood',
                 GetPlayerState=lambda p,f:resources[(f,p)],SetPlayerState=lambda p,f,v:resources.__setitem__((f,p),v),
                 DisplayTimedTextToPlayer=lambda *a:None,RemoveItem=lambda i:removed.append(i),
                 KLS_CompanyResearchRefresh=lambda:None,CreateGroup=lambda:[],GroupEnumUnitsOfPlayer=lambda *a:None,
                 ForGroup=lambda *a:updates.append(1),KLS_CompanyUpgradeEnum=lambda:None,DestroyGroup=lambda g:None,
                 GetItemName=lambda i:'Weapon Research')
        env['KLS_CompanyResearchAllowed']=lambda p,i:env['KLS_CompanyResearchRank'][p*5+1]==0
        compile_handler(runtime_script('TEST'),'KLS_CompanyResearchBuy',env)
        buy=env['KLS_CompanyResearchBuy'];buy(shop,hero,'wrong-owner')
        self.assertEqual(resources,{('gold',0):350,('wood',0):100})
        self.assertEqual(updates,[])
        shop['owner']=0;buy(shop,hero,'valid');buy(shop,hero,'stale-rank')
        self.assertEqual(updates,[1])
        self.assertEqual(env['KLS_CompanyResearchRank'][1],1)
        self.assertEqual(env['KLS_CompanyResearchRank'][6],0)
        self.assertEqual(len(removed),3)
        self.assertEqual(resources,{('gold',0):700,('wood',0):200})

    def test_escort_presence_ambush_arrival_and_death_retry(self):
        cart=dict(x=0.,y=-8400.,life=1800.)
        hero=dict(x=0.,y=-8400.,life=100.)
        moves=[];events=[]
        env=dict(KLS_StoryCart=cart,KLS_Ended=False,KLS_StoryCartClock='clock',
                 KLS_StoryCartSteps=7,KLS_Active=[True,False,False,False],
                 KLS_Hero=[hero,None,None,None],KLS_StoryContributor=[False]*16,
                 GetWidgetLife=lambda u:u['life'],GetUnitX=lambda u:u['x'],GetUnitY=lambda u:u['y'],
                 IssuePointOrder=lambda *a:moves.append(a),IssueImmediateOrder=lambda *a:None,
                 PauseTimer=lambda t:events.append('pause'),RemoveUnit=lambda u:events.append('removed'),
                 KLS_StoryClearEncounter=lambda:events.append('cleared'),KLS_StoryComplete=lambda:events.append('complete'),
                 KLS_StoryEscortFailed=lambda:events.append('retry'),KLS_StoryAmbush=lambda:events.append('ambush'))
        compile_handler(runtime_script('TEST'),'KLS_StoryCartTick',env)
        tick=env['KLS_StoryCartTick'];tick()
        self.assertEqual(events,['ambush'])
        self.assertTrue(env['KLS_StoryContributor'][4])
        self.assertEqual(env['KLS_StoryCartSteps'],8)
        cart['y']=-4900.;hero['y']=-4900.;tick()
        self.assertIn('complete',events);self.assertIsNone(env['KLS_StoryCart'])
        env['KLS_StoryCart']=dict(x=0.,y=-8000.,life=0.)
        tick();self.assertEqual(events[-1],'retry')

    def test_counter_siege_hits_actual_siege_invaders_only(self):
        attacker=dict(owner=0,kind='support');victim=dict(kind='umtw')
        damage=[100.]
        env=dict(GetEventDamageSource=lambda:attacker,GetTriggerUnit=lambda:victim,
                 GetPlayerId=lambda p:p,GetOwningPlayer=lambda u:u['owner'],Player=lambda p:p,
                 KLS_Active=[True]*4,KLS_HeroChoice=[0]*4,KLS_CompanyResearchRank=[0,0,0,1,0]*4,
                 KLS_CompanySupportId=['support'],BlzGetEventIsAttack=lambda:True,
                 GetEventDamage=lambda:damage[0],BlzSetEventDamage=lambda v:damage.__setitem__(0,v),
                 GetUnitTypeId=lambda u:u['kind'],IsUnitEnemy=lambda u,p:True,
                 IsUnitType=lambda u,t:False,UNIT_TYPE_STRUCTURE='structure')
        script=runtime_script('TEST')
        compile_handler(script,'KLS_IsSiegeInvader',env)
        compile_handler(script,'KLS_CompanyCounterSiege',env)
        for code in ('umtw','hbew','nhyc'):
            victim['kind']=code;damage[0]=100.;env['KLS_CompanyCounterSiege']()
            self.assertEqual(damage[0],150.)
        victim['kind']='ugho';damage[0]=100.;env['KLS_CompanyCounterSiege']()
        self.assertEqual(damage[0],100.)
        victim['kind']='umtw';env['BlzGetEventIsAttack']=lambda:False
        env['KLS_CompanyCounterSiege']();self.assertEqual(damage[0],100.)

    def test_new_recruit_clears_recycled_handle_bookkeeping(self):
        table={(17,0):180,(17,1):6,(17,2):2,(17,3):True}
        applied=[]
        env=dict(KLS_CompanyUpgradeData=table,GetHandleId=lambda u:17,
                 FlushChildHashtable=lambda t,k:[t.pop(key) for key in list(t) if key[0]==k],
                 KLS_CompanyApplyUpgrades=lambda u:applied.append(dict(table)))
        compile_handler(runtime_script('TEST'),'KLS_CompanyPrepareNewRecruit',env)
        env['KLS_CompanyPrepareNewRecruit']('new-unit')
        self.assertEqual(applied,[{}])
