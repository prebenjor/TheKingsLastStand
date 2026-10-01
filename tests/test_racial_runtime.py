import unittest
from pathlib import Path
from test_backpack_panel import compile_handler

class RacialRuntime(unittest.TestCase):
    def buff_environment(self):
        state={};timers={};serial=[10];current=[0];damage=[100.0]
        caster=dict(handle=1,owner=0,life=900,armor=3.,cooldown=2.,move=240.)
        target=dict(handle=2,owner=0,life=100,armor=7.,cooldown=2.,move=240.)
        def create():serial[0]+=1;return serial[0]
        def flush(h,k):
            for pair in list(h):
                if pair[0]==k:del h[pair]
        env=dict(KLS_RacialData=state,UNIT_RF_DEFENSE='armor',GetHandleId=lambda u:u['handle'] if isinstance(u,dict) else u,
          GetUnitTypeId=lambda u:1 if u else 0,GetOwningPlayer=lambda u:u['owner'],GetWidgetLife=lambda u:u['life'],
          BlzGetUnitMaxHP=lambda u:1000,SetWidgetLife=lambda u,v:u.__setitem__('life',v),
          BlzGetUnitRealField=lambda u,f:u[f],BlzSetUnitRealField=lambda u,f,v:u.__setitem__(f,v),
          GetUnitMoveSpeed=lambda u:u['move'],SetUnitMoveSpeed=lambda u,v:u.__setitem__('move',v),
          BlzGetUnitAttackCooldown=lambda u,i:u.get('cooldown' if i==0 else 'cooldown1',0.),BlzSetUnitAttackCooldown=lambda u,v,i:u.__setitem__('cooldown' if i==0 else 'cooldown1',v),
          CreateTimer=create,TimerStart=lambda t,d,r,f:timers.__setitem__(t,f),GetExpiredTimer=lambda:current[0],
          PauseTimer=lambda t:None,DestroyTimer=lambda t:timers.pop(t,None),FlushChildHashtable=flush,
          RemoveSavedHandle=lambda h,k,c:h.pop((k,c),None),UnitRemoveAbility=lambda *a:None,
          R2I=int,I2R=float,RMinBJ=min,ModuloInteger=lambda a,b:a%b,
          ATTACK_TYPE_NORMAL=0,DAMAGE_TYPE_MAGIC=0,WEAPON_TYPE_WHOKNOWS=0,
          UnitDamageTarget=lambda u,v,d,*a:v.__setitem__('life',v['life']-d),
          GetTriggerUnit=lambda:target,GetEventDamage=lambda:damage[0],BlzSetEventDamage=lambda v:damage.__setitem__(0,v))
        for name in ('UnitHandle','PlayerHandle','Integer','Real','TimerHandle'):
            env['Load'+name]=lambda h,k,c,kind=name:h.get((k,c),None if 'Handle' in kind else 0)
            env['Save'+name]=lambda h,k,c,v:h.__setitem__((k,c),v)
        source=(Path(__file__).resolve().parents[1]/'source/racial.j').read_text()
        for name in ('KLS_RacialExpire','KLS_RacialTick','KLS_RacialBuff','KLS_RacialShield'):compile_handler(source,name,env)
        return env,caster,target,state,timers,current,damage

    def test_timed_effects_refresh_expire_and_cleanup_owner_changes(self):
        for kind,value,duration in ((0,4.,8.),(2,.20,3.),(3,.15,6.),(7,-3.,4.)):
            env,caster,target,state,timers,current,_=self.buff_environment()
            baseline=(target['armor'],target['cooldown'],target['move'])
            for _ in range(2):env['KLS_RacialBuff'](caster,target,kind,duration,value,1.)
            self.assertEqual(len(timers),1)
            self.assertEqual(target['armor'],baseline[0]+value if kind in (0,7) else baseline[0])
            if kind==3:self.assertAlmostEqual(target['cooldown'],baseline[1]/1.15)
            for _ in range(int(duration*4)):
                current[0]=next(iter(timers));env['KLS_RacialTick']()
            self.assertEqual((target['armor'],target['cooldown'],target['move']),baseline)
            self.assertEqual(len(timers),0)
            if kind==7:self.assertEqual(target['life'],0)
            env['KLS_RacialBuff'](caster,target,kind,duration,value,1.)
            target['owner']=1;current[0]=next(iter(timers));env['KLS_RacialTick']()
            self.assertEqual(len(timers),0)
            self.assertEqual((target['armor'],target['cooldown'],target['move']),baseline)

    def test_repair_total_and_shield_never_overheal_or_create_damage(self):
        env,caster,target,state,timers,current,damage=self.buff_environment()
        env['KLS_RacialBuff'](caster,target,1,5.,0.,1.)
        for _ in range(20):current[0]=next(iter(timers));env['KLS_RacialTick']()
        self.assertEqual(target['life'],400)
        env['KLS_RacialBuff'](caster,target,6,8.,250.,1.)
        for amount,expected in ((100,0),(200,50),(100,100)):
            damage[0]=amount;env['KLS_RacialShield']();self.assertEqual(damage[0],expected)
        self.assertEqual(len(timers),0)

    def test_removed_target_clears_its_saved_timer_before_handle_reuse(self):
        env,caster,target,state,timers,current,_=self.buff_environment()
        env['KLS_RacialBuff'](caster,target,0,8.,4.,1.)
        key=next(iter(timers));env['GetUnitTypeId']=lambda u:0
        env['KLS_RacialExpire'](key)
        self.assertEqual(state,{})

    def test_shield_stops_immediately_when_caster_ownership_changes(self):
        env,caster,target,state,timers,current,damage=self.buff_environment()
        env['KLS_RacialBuff'](caster,target,6,8.,250.,1.)
        caster['owner']=1
        env['KLS_RacialShield']()
        self.assertEqual(damage[0],100.)
        self.assertEqual(len(timers),0)

    def test_buff_cleanup_restores_only_applied_armor_delta(self):
        path=Path(__file__).resolve().parents[1]/'source/racial.j'
        self.assertTrue(path.exists(),'Specialist runtime not implemented')
        unit={'armor':11.0,'cooldown':2.0,'move':240.0}
        state={(7,0):unit,(7,3):0,(7,5):4.0}
        env=dict(KLS_RacialData=state,UNIT_RF_DEFENSE='armor',
          LoadUnitHandle=lambda h,k,c:h.get((k,c)),LoadInteger=lambda h,k,c:h.get((k,c),0),LoadReal=lambda h,k,c:h.get((k,c),0),
          GetUnitTypeId=lambda u:1,BlzGetUnitRealField=lambda u,f:u[f],
          BlzSetUnitRealField=lambda u,f,v:u.__setitem__(f,v),
          LoadTimerHandle=lambda h,k,c:7,SaveTimerHandle=lambda *a:None,
          GetUnitMoveSpeed=lambda u:u['move'],SetUnitMoveSpeed=lambda u,v:u.__setitem__('move',v),
          BlzGetUnitAttackCooldown=lambda u,i:u['cooldown'],BlzSetUnitAttackCooldown=lambda u,v,i:u.__setitem__('cooldown',v),
          PauseTimer=lambda t:None,DestroyTimer=lambda t:None,FlushChildHashtable=lambda h,k:h.update({}),
          RemoveSavedHandle=lambda *a:None,GetHandleId=lambda t:t)
        compile_handler(path.read_text(),'KLS_RacialExpire',env)
        env['KLS_RacialExpire'](7)
        self.assertEqual(unit['armor'],7.0)

    def test_work_order_blocks_switch_even_after_current_order_becomes_channel(self):
        worker=dict(handle=17,owner=0,life=100.,mana=20.,type=1)
        saved={};morphs=[];messages=[];disabled=[];order=[77]
        env=dict(KLS_WorkerPageData=saved,KLS_WorkerStandardId=[1,2,3,4],KLS_WorkerExpansionId=[5,6,7,8],
          KLS_WorkerToExpansion=[9,10,11,12],KLS_WorkerToStandard=[13,14,15,16],
          GetTriggerUnit=lambda:worker,GetUnitTypeId=lambda u:u['type'],GetHandleId=lambda u:u['handle'],
          GetOwningPlayer=lambda u:u['owner'],GetWidgetLife=lambda u:u['life'],GetUnitState=lambda u,s:u['mana'],
          UNIT_STATE_MANA=0,GetSpellAbilityId=lambda: 'rPg0',GetUnitCurrentOrder=lambda u:88,
          GetIssuedOrderId=lambda:order[0],OrderId=lambda s:88 if s=='channel' else 99,
          GetUnitAbilityLevel=lambda u,a:1,
          SaveInteger=lambda h,k,c,v:h.__setitem__((k,c),v),LoadInteger=lambda h,k,c:h.get((k,c),0),
          BlzUnitDisableAbility=lambda u,a,d,h:disabled.append(d),DisplayTimedTextToPlayer=lambda *a:messages.append(a[-1]),
          IsUnitLoaded=lambda u:False,UnitAddAbility=lambda u,a:morphs.append(a),UnitRemoveAbility=lambda *a:None,
          SetWidgetLife=lambda *a:None,SetUnitState=lambda *a:None,UnitMakeAbilityPermanent=lambda *a:None,
          KLS_Log=lambda *a:None,I2S=str,GetPlayerId=lambda p:p)
        source=(Path(__file__).resolve().parents[1]/'source/worker_pages.j').read_text()
        for name in ('KLS_WorkerPageOrdered','KLS_WorkerPageCast'):compile_handler(source,name,env)
        env['KLS_WorkerPageOrdered']();order[0]=88;env['KLS_WorkerPageOrdered']();env['KLS_WorkerPageCast']()
        self.assertEqual(morphs,[])
        self.assertEqual(disabled,[True])
        self.assertTrue(messages)

    def test_worker_switch_is_not_integrated_without_native_acceptance(self):
        path=Path(__file__).resolve().parents[1]/'source/worker_pages.j'
        self.assertTrue(path.exists(),'Worker switching prototype missing')
        text=path.read_text()
        self.assertIn('KLS_WorkerPagesAccepted = false',text)
        self.assertIn('EVENT_PLAYER_UNIT_ISSUED_TARGET_ORDER',text)
        self.assertIn('LoadInteger(KLS_WorkerPageData,workerHandle,0)',text)
        self.assertNotIn('RemoveUnit(worker)',text)
        self.assertNotIn('CreateUnit(',text)

    def test_idle_refresh_does_not_disable_the_toggle_during_its_own_cast(self):
        worker=dict(type=1,handle=17);disabled=[]
        env=dict(KLS_WorkerPageData={},KLS_WorkerPagesAccepted=False,KLS_WorkerStandardId=[1,2,3,4],KLS_WorkerExpansionId=[5,6,7,8],
          GetEnumUnit=lambda:worker,GetUnitTypeId=lambda u:u['type'],GetHandleId=lambda u:u['handle'],
          GetUnitCurrentOrder=lambda u:88,OrderId=lambda s:88 if s=='channel' else 99,
          SaveInteger=lambda *a:None,IsUnitLoaded=lambda u:False,
          BlzUnitDisableAbility=lambda u,a,d,h:disabled.append(d))
        source=(Path(__file__).resolve().parents[1]/'source/worker_pages.j').read_text()
        compile_handler(source,'KLS_WorkerPageRefreshEnum',env)
        env['KLS_WorkerPageRefreshEnum']()
        self.assertEqual(disabled,[False])

if __name__=='__main__':unittest.main()
