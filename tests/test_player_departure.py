import re
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'tools'))
from pipeline import runtime_script


def function_body(script, name):
    match = re.search(r'^function ' + re.escape(name) + r' takes [\s\S]*?^endfunction$', script, re.M)
    if not match:
        raise AssertionError('Missing runtime function ' + name)
    return match.group()


class PlayerDeparture(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.script = runtime_script('KLS-D-TEST')

    def test_leaving_player_is_removed_from_scaling_and_selection_without_unit_transfer(self):
        leave = function_body(self.script, 'KLS_PlayerLeft')
        self.assertIn('set KLS_Active[p] = false', leave)
        self.assertIn('set KLS_Players = KLS_Players-1', leave)
        self.assertIn('call KLS_FinishSelection()', leave)
        self.assertIn('if KLS_Players == 0 then', leave)
        self.assertIn('call KLS_End(false)', leave)
        self.assertNotIn('SetUnitOwner', leave)
        self.assertNotIn('SetPlayerAlliance', leave)

    def test_every_defender_slot_registers_a_leave_event(self):
        init = function_body(self.script, 'KLS_Init')
        self.assertIn('TriggerRegisterPlayerEvent(leaves,Player(i),EVENT_PLAYER_LEAVE)', init)
        self.assertIn('TriggerAddAction(leaves,function KLS_PlayerLeft)', init)

    def test_enemy_bounty_is_shared_and_remainder_follows_player_slot_order(self):
        award = function_body(self.script, 'KLS_AwardBounty')
        death = function_body(self.script, 'KLS_Death')
        self.assertIn('if KLS_Active[i] then', award)
        self.assertIn('set share = bounty / activeCount', award)
        self.assertIn('set remainder = ModuloInteger(bounty, activeCount)', award)
        self.assertIn('if remainder > 0 then', award)
        self.assertRegex(award, r'loop[\s\S]*?set i = i \+ 1[\s\S]*?if KLS_Active\[i\] then[\s\S]*?remainder = remainder - 1')
        self.assertIn('call KLS_AwardBounty(KLS_EnemyBounty(dead))', death)
        self.assertNotIn('GetOwningPlayer(killer)', death)

        def shares(active_slots, bounty):
            ordered = sorted(active_slots)
            if not ordered:
                return {}
            base, remainder = divmod(bounty, len(ordered))
            return {slot: base + (index < remainder) for index, slot in enumerate(ordered)}

        self.assertEqual(shares([3, 1], 11), {1: 6, 3: 5})
        self.assertEqual(shares([2, 0, 3], 8), {0: 3, 2: 3, 3: 2})
        self.assertEqual(shares([2], 9), {2: 9})


if __name__ == '__main__':
    unittest.main()
