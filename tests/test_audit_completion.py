"""Behavioral regressions for confirmed September 30 audit defects.

JASS handlers execute through the existing straight-line translator with native
boundaries supplied by the test. These do not prove Warcraft UI rendering.
"""
import json
import sys
import unittest
from pathlib import Path
from types import SimpleNamespace
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'tools'))
sys.path.insert(0, str(ROOT / 'tests'))
from equipment_catalog import item_catalog, abilities
from power_curve import parse_item_options, custom_projection, item_report
from hero_progression import HERO_ABILITIES
from objects import units
from pipeline import runtime_script
from test_equipment import decode
from test_market_controls import function_body
from test_backpack_panel import compile_handler
from test_multiplayer_ui_safety import local_allocations


class PowerProjection(unittest.TestCase):
    def test_general_and_racial_primary_weapons_conflict(self):
        with self.assertRaisesRegex(ValueError, 'slot collision'):
            parse_item_options('I100,I23P', item_catalog())

    def test_mixed_catalog_rings_share_two_slots(self):
        rings = [x for x in item_catalog() if x['slot'] == 5]
        general = next(x for x in rings if not x.get('slot_name'))
        racial = next(x for x in rings if x.get('slot_name'))
        with self.assertRaisesRegex(ValueError, 'slot collision'):
            parse_item_options(','.join([general['rawcode'], general['rawcode'], racial['rawcode']]), item_catalog())

    def test_attributes_contribute_secondary_stats(self):
        hero = dict(name='Probe', unit_id='Hpal', primary='strength',
                    base_stats=dict(strength=10., agility=10., intelligence=10.),
                    base_hp=350., base_mana=150., hp_regen=.75, mana_regen=.51,
                    weapon_min=2., weapon_max=12.)
        args = SimpleNamespace(hero='Hpal', level=4, strength_points=1,
                               agility_points=1, intelligence_points=1,
                               talents='', tomes='', items='')
        result = json.loads(custom_projection(args, {'Hpal': hero}, []))
        self.assertEqual(result['hp'], 425)
        self.assertEqual(result['mana'], 195)
        self.assertAlmostEqual(result['hp_regen'], .9)
        self.assertAlmostEqual(result['mana_regen'], .66)
        self.assertAlmostEqual(result['agility_attack_speed_bonus'], .26)

    def test_level_one_has_one_skill_point_to_spend(self):
        hero = dict(name='Probe', unit_id='Hpal', primary='strength',
                    base_stats=dict(strength=10., agility=10., intelligence=10.),
                    base_hp=350., base_mana=150., hp_regen=.75, mana_regen=.51,
                    weapon_min=2., weapon_max=12.)
        args = SimpleNamespace(hero='Hpal', level=1, strength_points=1,
                               agility_points=0, intelligence_points=0,
                               talents='', tomes='', items='')
        result = json.loads(custom_projection(args, {'Hpal': hero}, []))
        self.assertEqual(result['stats']['strength'], 13)
        self.assertEqual(result['skill_points_remaining_for_spells'], 0)
        args.strength_points = 2
        with self.assertRaises(ValueError):
            custom_projection(args, {'Hpal': hero}, [])

    def test_cross_tier_rule_checks_each_item(self):
        items = [dict(rawcode=code, name=code, tier=tier, slot=6, stats={'damage': damage})
                 for code,tier,damage in [('lowA',0,10),('lowB',0,10),('lowC',0,20),('high',1,12)]]
        report = '\n'.join(item_report(items))
        self.assertRegex(report, r'Cross-tier item warning.*lowC')


class HeroLearnData(unittest.TestCase):
    def test_keeper_and_faelor_have_four_tree_free_learnable_skills(self):
        records = decode(units())
        spells = decode(abilities(), True)
        for hero in ('Ekee', 'Efal'):
            self.assertEqual(len(HERO_ABILITIES[hero]), 4)
            self.assertNotIn('AEfn', records[hero][1][('uhab',0)][0])
            self.assertIn('AKfn', HERO_ABILITIES[hero])
        parent, fields = spells['AKfn']
        self.assertEqual(parent, 'AOsf')
        self.assertEqual(fields[('alev',0)][0], 10)
        for rank in range(1,11):
            self.assertEqual(fields[('Osf1',rank)][0], f'kT{rank:02d}' if rank <= 5 else f'bT{rank:02d}')
            self.assertIn('trees', fields[('aub1',rank)][0])
        health = [records[f'kT{rank:02d}'][1][('uhpm',0)][0] for rank in range(1,6)]
        self.assertEqual(health, [300,450,600,660,720])


class SynchronizedChoices(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.script = runtime_script('KLS-D-TEST')

    def ready_env(self, payload):
        env = dict(GetTriggerPlayer=lambda: 1, GetPlayerId=lambda p:p,
                   BlzGetTriggerSyncData=lambda:payload, S2I=lambda s:int(s) if s.isdigit() else 0,
                   I2S=str, SubString=lambda s,a,b:s[a:b], StringLength=len,
                   KLS_Active=[True]*4, KLS_Ended=False, KLS_Selecting=False,
                   KLS_Alive=0, KLS_Prep=50, KLS_Players=4, KLS_ReadyEpoch=7,
                   KLS_ReadyVote=[False]*4, KLS_Log=lambda s:None,
                   KLS_ReadyCount=lambda:0, KLS_ReadyCheck=lambda:None,
                   KLS_VoteUIRefresh=lambda:None, KLS_HUDUpdate=lambda:None)
        compile_handler(self.script, 'KLS_ReadyVoteSync', env)
        return env

    def test_repeated_ready_message_is_idempotent(self):
        env = self.ready_env('7:1')
        env['KLS_ReadyVoteSync']()
        self.assertTrue(env['KLS_ReadyVote'][1])
        env['KLS_ReadyVoteSync']()
        self.assertTrue(env['KLS_ReadyVote'][1])

    def test_previous_preparation_vote_is_rejected(self):
        env = self.ready_env('6:1')
        env['KLS_ReadyVoteSync']()
        self.assertEqual(env['KLS_ReadyVote'], [False]*4)

    def test_malformed_ready_message_is_rejected(self):
        for payload in ('toggle','7:2','07:1','garbage','7:'):
            env = self.ready_env(payload)
            env['KLS_ReadyVoteSync']()
            self.assertEqual(env['KLS_ReadyVote'], [False]*4, payload)

    def test_talents_have_no_dialog_and_identical_client_allocations(self):
        module = (ROOT/'source/combat.j').read_text()
        self.assertNotIn('DialogDisplay', module)
        self.assertEqual(local_allocations(self.script, 'KLS_ProgressionInit'), [])
        self.assertIn('KLS_TalentChoiceApplySync', self.script)

    def test_talent_sync_spends_only_the_senders_earned_points(self):
        chosen=[]
        env=dict(GetTriggerPlayer=lambda:1, GetPlayerId=lambda p:p,
                 BlzGetTriggerSyncData=lambda:'2',S2I=lambda s:int(s) if s.isdigit() else 0,I2S=str,
                 KLS_Active=[True]*4,KLS_Ended=False,KLS_Hero=['h0','h1','h2','h3'],
                 Player=lambda p:p,GetOwningPlayer=lambda u:int(u[1]),KLS_TalentPoints=[3,1,2,0],
                 KLS_TalentApply=lambda p,c:chosen.append((p,c)),KLS_StatChoiceRefresh=lambda:None)
        compile_handler(self.script,'KLS_TalentChoiceApplySync',env)
        apply=env['KLS_TalentChoiceApplySync'];apply();apply()
        self.assertEqual(chosen,[(1,2)])
        self.assertEqual(env['KLS_TalentPoints'],[3,0,2,0])
        env['KLS_TalentPoints'][1]=1
        for payload in ('garbage','02','3','-1'):
            env['BlzGetTriggerSyncData']=lambda:payload
            apply()
        self.assertEqual(env['KLS_TalentPoints'][1],1)
        env['BlzGetTriggerSyncData']=lambda:'0'
        env['GetOwningPlayer']=lambda u:0
        apply()
        self.assertEqual(env['KLS_TalentPoints'][1],1)

    def test_evasion_does_not_cancel_spell_damage(self):
        for attack,damage,expected in [(False,100,100),(True,100,0),(True,0,0),(False,-100,-100)]:
            result = [damage]
            env = dict(GetTriggerUnit=lambda:'hero', GetOwningPlayer=lambda u:0,
                       GetPlayerId=lambda p:p, KLS_Hero=['hero',None,None,None],
                       KLS_TalentAgilityRank=[10,0,0,0], GetRandomInt=lambda a,b:1,
                       BlzGetEventIsAttack=lambda:attack, GetEventDamage=lambda:damage,
                       BlzSetEventDamage=lambda value:result.__setitem__(0,value))
            compile_handler(self.script, 'KLS_TalentAvoidDamage', env)
            env['KLS_TalentAvoidDamage']()
            self.assertEqual(result[0], expected)
