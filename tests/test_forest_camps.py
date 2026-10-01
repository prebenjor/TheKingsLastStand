"""Northern forest route, scenery clearance, and personal camp-loot contracts."""
import re
import sys
import struct
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'tools'))
from forest_catalog import CAMPS, forest_plan, path_distance, camp_script, forest_pathing, PATHS


class ForestCamps(unittest.TestCase):
    def test_cliff_pathing_preserves_routes_and_all_ground_south_of_the_forest(self):
        before = b'MP3W'+struct.pack('<III',0,768,768)+bytes([64])*(768*768)
        after = forest_pathing(before)
        self.assertEqual(after[:16],before[:16])
        def flags(x,y):
            return after[16+int((y+12288)//32)*768+int((x+12288)//32)]
        self.assertEqual(after[:16+int((6500+12288)//32)*768],before[:16+int((6500+12288)//32)*768])
        for path in PATHS:
            for x,y in path:
                self.assertFalse(flags(x,y)&2)
        for cliff in forest_plan()['cliffs']:
            self.assertTrue(flags(cliff['x'],cliff['y'])&2)
        with self.assertRaises(ValueError):
            forest_pathing(b'MP3W'+bytes(20))

    def test_forest_surrounds_three_sides_but_keeps_wave_forecourt_open(self):
        plan = forest_plan()
        trees = plan['trees']
        self.assertGreater(len(trees), 250)
        self.assertTrue(any(t['x'] < -2500 and t['y'] < 8500 for t in trees))
        self.assertTrue(any(t['x'] > 2500 and t['y'] < 8500 for t in trees))
        self.assertTrue(any(abs(t['x']) < 2000 and t['y'] > 9000 for t in trees))
        for tree in trees:
            self.assertGreater(path_distance(tree['x'], tree['y']), 340)
            self.assertFalse(abs(tree['x']) < 1900 and tree['y'] < 8500)

    def test_cliffs_and_rocks_leave_paths_and_coves_clear(self):
        plan = forest_plan()
        for cliff in plan['cliffs']:
            self.assertGreater(path_distance(cliff['x'], cliff['y']), cliff['radius'] * 128 + 420)
        for rock in plan['rocks']:
            self.assertGreater(path_distance(rock['x'], rock['y']), 300)
        for camp in CAMPS:
            self.assertLessEqual(path_distance(camp['x'], camp['y']), 1)

    def test_loot_is_personal_one_time_and_camps_are_outside_wave_accounting(self):
        script = camp_script()
        self.assertIn('KLS_PersonalRewardEnqueue', script)
        self.assertIn('p < 0 or p >= 4 or not KLS_Active[p]', script)
        reward = script[:script.index('function KLS_ForestInit')]
        for forbidden in ('KLS_Alive', 'KLS_Enemies', 'CreateUnit', 'TimerStart', 'GetLocalPlayer'):
            self.assertNotIn(forbidden, reward)
        self.assertIn('Player(PLAYER_NEUTRAL_AGGRESSIVE)', script)
        self.assertIn('SetUnitCreepGuard(u,true)', script)
        self.assertEqual({c['quality'] for c in CAMPS}, {0, 1})

    def test_camp_death_branch_precedes_wave_death_and_awards_xp(self):
        game = (ROOT / 'source/game.j').read_text()
        death = re.search(r'function KLS_Death takes.*?endfunction', game, re.S)[0]
        self.assertIn('KLS_IsForestMonster(GetUnitTypeId(dead))', death)
        branch = death[death.index('KLS_IsForestMonster'):death.index('elseif IsUnitInGroup(dead, KLS_Enemies)')]
        self.assertIn('KLS_AwardKillXP(dead)', branch)
        self.assertIn('KLS_ForestReward(dead,GetKillingUnit())', branch)
        self.assertNotIn('KLS_Alive', branch)


if __name__ == '__main__':
    unittest.main()
