"""Regressions for reward feedback, native item movement/sale, and spring regen."""
import re
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'tools'))
sys.path.insert(0, str(ROOT / 'tests'))

from equipment_catalog import item_catalog
from objects import items
from pipeline import runtime_script
from test_equipment import decode


def function_body(script, name):
    match = re.search(r'^function ' + re.escape(name) + r' takes [\s\S]*?^endfunction$', script, re.M)
    if not match:
        raise AssertionError('Missing runtime function ' + name)
    return match.group()


class ReportedRewardInventoryAndSpring(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.script = runtime_script('KLS-D-TEST')

    def test_enemy_and_boss_gold_rewards_show_the_actual_personal_payout(self):
        toast = function_body(self.script, 'KLS_GoldToast')
        self.assertIn('I2S(amount)', toast)
        self.assertRegex(toast, r'DisplayTimedTextToPlayer\(Player\(p\)[\s\S]*?\+I2S\(amount\)\+" gold')
        # Keep the text message and add a rising number over the recipient's
        # hero so the reward stays visible while the camera is in battle.
        for fragment in ('CreateTextTag()', 'SetTextTagPosUnit(rewardTag,KLS_Hero[p]',
                         'SetTextTagColor(rewardTag,255,214,64,255)',
                         'SetTextTagVisibility(rewardTag,false)',
                         'GetLocalPlayer() != Player(p)'):
            self.assertIn(fragment, toast)

        bounty = function_body(self.script, 'KLS_AwardBounty')
        self.assertIn('call KLS_GoldToast(i,payout)', bounty)
        self.assertRegex(bounty, r'SetPlayerState\([\s\S]*?call KLS_GoldToast\(i,payout\)')

        boss = function_body(self.script, 'KLS_BossReward')
        self.assertIn('call KLS_GoldToast(i,250 + KLS_Wave * 10)', boss)

    def test_catalog_gear_can_move_between_backpack_and_normal_inventory_and_be_pawned(self):
        records = decode(items())
        for entry in item_catalog():
            with self.subTest(item=entry['rawcode']):
                fields = records[entry['rawcode']][1]
                # Warcraft's droppable flag enables native inventory drag/move;
                # pawnable plus the item gold value enables the shop buyback.
                self.assertEqual(fields[('idro', 0)][0], 1)
                self.assertEqual(fields[('ipaw', 0)][0], 1)
                self.assertEqual(fields[('igol', 0)][0], entry['price'])

        # Boss rewards use the same native equipment movement, while remaining
        # impossible to sell back.
        for rawcode in ('I010', 'I011', 'I012', 'I013'):
            with self.subTest(relic=rawcode):
                fields = records[rawcode][1]
                self.assertEqual(fields[('idro', 0)][0], 1)
                self.assertEqual(fields[('ipaw', 0)][0], 0)

    def test_restoring_spring_ticks_one_percent_of_each_maximum_every_second(self):
        tick = function_body(self.script, 'KLS_PoolTick')
        self.assertIn('GetWidgetLife(hero)+maxHP*0.01', tick)
        self.assertIn('GetUnitState(hero,UNIT_STATE_MANA)+maxMana*0.01', tick)
        self.assertNotIn('KLS_RestoreToast', tick)
        self.assertNotIn('AddSpecialEffectTarget', tick)
        self.assertNotIn('CreateTextTag', tick)
        self.assertNotIn('DisplayTimedTextToPlayer', tick)
        self.assertNotIn('GetWidgetLife(hero)+200.0', tick)
        self.assertNotIn('UNIT_STATE_MANA)+120.0', tick)
        init = function_body(self.script, 'KLS_WaveEnvironmentInit')
        self.assertRegex(init, r'TimerStart\(KLS_PoolClock,1\.0,true,function KLS_PoolTick\)')
        self.assertNotIn('if KLS_RestorePool == null then\n        return', init)
        self.assertIn("KLS_CreateUnitOptional(Player(PLAYER_NEUTRAL_PASSIVE),'nfoh',-900,-1600,270,\"restoring spring visual\")", init)
        self.assertNotIn("CreateUnit(Player(PLAYER_NEUTRAL_PASSIVE),'nfoh'", init)


if __name__ == '__main__':
    unittest.main()
