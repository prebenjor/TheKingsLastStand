"""Enemy combat gold is tiered by the installed wave-roster unit identity."""
import sys
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'tools'))

from pipeline import runtime_script
from wave_rosters import BOUNTY_BY_UNIT, bounty_script, wave_rosters


def function_body(script, name):
    match = re.search(r'^function ' + re.escape(name) + r' takes [\s\S]*?^endfunction$', script, re.M)
    if not match:
        raise AssertionError('Missing runtime function ' + name)
    return match.group()


class EnemyBounties(unittest.TestCase):
    def test_every_roster_unit_has_an_explicit_role_bounty(self):
        roster_units = {unit for roster in wave_rosters() for unit in roster}
        self.assertTrue(roster_units.issubset(BOUNTY_BY_UNIT))
        self.assertEqual(roster_units, set(BOUNTY_BY_UNIT))

        expected = {
            'uske': 5,       # basic skeleton
            'ugho': 8,       # ghoul
            'ucry': 12,      # crypt fiend
            'nfel': 18,      # fel stalker
            'unec': 22,      # necromancer
            'nfgu': 24,      # felguard
            'uabo': 32,      # abomination
            'umtw': 36,      # meat wagon
            'ninf': 45,      # infernal
        }
        for unit, bounty in expected.items():
            self.assertEqual(BOUNTY_BY_UNIT[unit], bounty, unit)
        tiers = ('uske', 'ugho', 'ucry', 'nfel', 'unec', 'nfgu', 'uabo', 'umtw', 'nbal', 'ninf')
        self.assertEqual(sorted(BOUNTY_BY_UNIT[unit] for unit in tiers),
                         [BOUNTY_BY_UNIT[unit] for unit in tiers])

    def test_generated_runtime_awards_role_bounty_plus_wave_scaling_once_on_tracked_death(self):
        script = runtime_script('KLS-D-TEST')
        self.assertIn(bounty_script(), script)
        bounty = function_body(script, 'KLS_EnemyBounty')
        self.assertIn("if unitCode == 'ninf' then\n        return 45 + KLS_Wave", bounty)
        self.assertIn("if unitCode == 'umtw' then\n        return 36 + KLS_Wave", bounty)
        self.assertIn("if unitCode == 'uske' then\n        return 5 + KLS_Wave", bounty)
        death = function_body(script, 'KLS_Death')
        self.assertIn('call KLS_AwardBounty(KLS_EnemyBounty(dead))', death)

    def test_bosses_and_boss_summons_use_strength_based_bounty(self):
        script = runtime_script('KLS-D-TEST')
        bounty = function_body(script, 'KLS_EnemyBounty')
        self.assertIn("if unitCode == 'Udea' or unitCode == 'Ulic' or unitCode == 'Udre' or unitCode == 'Uanb' then\n        return 100 + KLS_Wave * 5", bounty)
        self.assertIn("if unitCode == 'nfgu' then\n        return 24 + KLS_Wave", bounty)
        self.assertIn("if unitCode == 'uske' then\n        return 5 + KLS_Wave", bounty)


if __name__ == '__main__':
    unittest.main()
