"""Execute invasion orders against a moved king; this is not engine pathing proof."""
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'tools'))
sys.path.insert(0, str(ROOT / 'tests'))
from pipeline import runtime_script
from test_backpack_panel import compile_handler
from test_boss_mechanics import function_body


class InvaderOrders(unittest.TestCase):
    def environment(self):
        orders = []
        king = dict(x=750., y=-900., life=5000.)
        enemy = dict(life=200., order=0)
        env = dict(KLS_King=king, KLS_Ended=False,
                   GetWidgetLife=lambda u: u['life'],
                   GetUnitX=lambda u: u['x'], GetUnitY=lambda u: u['y'],
                   GetEnumUnit=lambda: enemy, GetUnitCurrentOrder=lambda u: u['order'],
                   IssuePointOrder=lambda *args: orders.append(args))
        script = runtime_script('KLS-D-TEST')
        compile_handler(script, 'KLS_OrderInvader', env)
        compile_handler(script, 'KLS_Reorder', env)
        return env, king, enemy, orders

    def test_orders_follow_actual_king_position_on_each_call(self):
        env, king, enemy, orders = self.environment()
        env['KLS_OrderInvader'](enemy)
        king.update(x=-850., y=1200.)
        env['KLS_OrderInvader'](enemy)
        self.assertEqual(orders, [(enemy, 'attack', 750., -900.),
                                  (enemy, 'attack', -850., 1200.)])

    def test_ended_or_missing_or_dead_objectives_do_not_issue_orders(self):
        for change in ('ended', 'missing', 'dead'):
            env, king, enemy, orders = self.environment()
            if change == 'ended': env['KLS_Ended'] = True
            elif change == 'missing': env['KLS_King'] = None
            else: king['life'] = 0.
            env['KLS_OrderInvader'](enemy)
            self.assertEqual(orders, [])

    def test_null_and_dead_invaders_do_not_issue_orders(self):
        env, king, enemy, orders = self.environment()
        env['KLS_OrderInvader'](None)
        enemy['life'] = 0.
        env['KLS_OrderInvader'](enemy)
        self.assertEqual(orders, [])

    def test_reorder_preserves_active_attack_or_spell_orders(self):
        env, king, enemy, orders = self.environment()
        enemy['order'] = 852095
        env['KLS_Reorder']()
        self.assertEqual(orders, [])
        enemy['order'] = 0
        env['KLS_Reorder']()
        self.assertEqual(orders, [(enemy, 'attack', king['x'], king['y'])])

    def test_wave_boss_and_reinforcement_share_the_same_order_helper(self):
        script = runtime_script('KLS-D-TEST')
        spawn = function_body(script, 'KLS_Spawn')
        self.assertEqual(spawn.count('call KLS_OrderInvader(u)'), 2)
        self.assertIn('call KLS_OrderInvader(summon)', function_body(script, 'KLS_BossSummon'))
        self.assertLess(script.index('function KLS_OrderInvader '),
                        script.index('function KLS_BossSummon '))

