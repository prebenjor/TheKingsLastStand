"""Regression coverage for recoverable personal boss and story rewards."""
import re
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'tools'))
sys.path.insert(0, str(ROOT / 'tests'))

from pipeline import runtime_script


def function_body(script, name):
    match = re.search(r'^function ' + re.escape(name) + r' takes [\s\S]*?^endfunction$', script, re.M)
    if not match:
        raise AssertionError('Missing runtime function ' + name)
    return match.group()


class PersonalRewardDelivery(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.script = runtime_script('KLS-D-REWARD-TEST')

    def test_boss_and_story_rewards_use_one_personal_delivery_queue(self):
        boss = function_body(self.script, 'KLS_BossReward')
        story = function_body(self.script, 'KLS_StoryComplete')
        self.assertNotIn('CreateItem(', boss)
        self.assertIn('call KLS_PersonalRewardEnqueue(i,gear,"Boss")', boss)
        self.assertNotIn('CreateItem(', story)
        self.assertIn('call KLS_PersonalRewardEnqueue(p,itemCode,"Crownlands story")', story)

    def test_null_item_creation_is_queued_before_any_item_native_uses_the_handle(self):
        deliver = function_body(self.script, 'KLS_PersonalRewardDeliver')
        created = deliver.index('set reward = CreateItem(itemCode')
        null_guard = deliver.index('if reward == null then', created)
        self.assertLess(null_guard, deliver.index('SetItemPlayer(reward', created))
        self.assertLess(null_guard, deliver.index('SetItemUserData(reward', created))
        self.assertLess(null_guard, deliver.index('UnitAddItem(hero,reward)', created))
        enqueue = function_body(self.script, 'KLS_PersonalRewardEnqueue')
        self.assertRegex(enqueue, r'if KLS_PersonalRewardDeliver\(p,itemCode\) then\s+return\s+endif[\s\S]*?SaveInteger\(KLS_PersonalRewardData,p,KLS_PersonalRewardTail\[p\],itemCode\)')

    def test_reward_creation_and_retry_errors_log_item_rawcode_owner_and_position(self):
        enqueue = function_body(self.script, 'KLS_PersonalRewardEnqueue')
        retry = function_body(self.script, 'KLS_PersonalRewardTick')
        self.assertIn('ERROR "+source+" item creation failed', enqueue)
        self.assertIn('ERROR personal reward retry failed', retry)
        for detail in ('GetObjectName(itemCode)', 'I2S(itemCode)',
                       'I2S(p+1)', 'R2S(KLS_X[p])', 'R2S(KLS_Y[p])'):
            with self.subTest(stage='enqueue', detail=detail):
                self.assertIn(detail, enqueue)
            with self.subTest(stage='retry', detail=detail):
                self.assertIn(detail, retry)

    def test_full_inventory_leaves_a_personal_retrievable_item_at_the_player_plot(self):
        deliver = function_body(self.script, 'KLS_PersonalRewardDeliver')
        self.assertRegex(deliver, r'if hero != null then\s+set stored = UnitAddItem\(hero,reward\)\s+endif\s+if stored then[\s\S]*?else[\s\S]*?SetItemPosition\(reward,KLS_X\[p\],KLS_Y\[p\]\)[\s\S]*?endif[\s\S]*?return true')
        self.assertIn('SetItemPlayer(reward,Player(p),false)', deliver)
        self.assertIn('SetItemUserData(reward,p+1)', deliver)
        self.assertIn('Your personal reward is waiting at your base.', deliver)

    def test_retry_tick_is_initialized_and_runs_from_the_active_match_clock(self):
        init = function_body(self.script, 'KLS_Init')
        tick = function_body(self.script, 'KLS_Tick')
        retry = function_body(self.script, 'KLS_PersonalRewardTick')
        self.assertIn('call KLS_PersonalRewardInit()', init)
        self.assertLess(init.index('call KLS_PersonalRewardInit()'), init.index('call KLS_CrownlandsInit()'))
        self.assertIn('call KLS_PersonalRewardTick()', tick)
        self.assertIn('KLS_PersonalRewardRetry[p] = 5', retry)
        self.assertIn('KLS_PersonalRewardDeliver(p,itemCode)', retry)
        self.assertIn('FlushChildHashtable(KLS_PersonalRewardData,p)', retry)


if __name__ == '__main__':
    unittest.main()
