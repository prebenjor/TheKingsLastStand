"""Guard the authored invasion site and surviving-settlement boundary."""
import re
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'tools'))
from town_catalog import TOWNS, town_placements
from pipeline import runtime_script
from editor_layout import replace_runtime_functions


class NorthernOrigin(unittest.TestCase):
    def test_editor_handoff_preserves_native_code_and_orders_new_helpers(self):
        original = ('function NativeMain takes nothing returns nothing\nendfunction\n'
                    'function KLS_CrownlandsBuildTowns takes nothing returns nothing\nendfunction\n'
                    'function Existing takes nothing returns nothing\n    call DoNothing()\nendfunction\n')
        find = 'function Find takes nothing returns nothing\nendfunction'
        initialize = 'function Initialize takes nothing returns nothing\n    call Find()\nendfunction'
        result = replace_runtime_functions(original, {'Find': find, 'Initialize': initialize})
        self.assertLess(result.index(find), result.index(initialize))
        self.assertLess(result.index(initialize), result.index('function KLS_CrownlandsBuildTowns'))
        self.assertEqual(result.replace(find + '\n\n' + initialize + '\n\n', ''), original)

    def test_editor_handoff_rejects_duplicate_function_definitions(self):
        body = 'function Existing takes nothing returns nothing\nendfunction'
        with self.assertRaisesRegex(ValueError, 'Duplicate'):
            replace_runtime_functions(body + '\n' + body, {'Existing': body})

    def test_removed_settlements_emit_only_relocated_services(self):
        self.assertEqual([t['race'] for t in TOWNS if t.get('active', True)], ['Human', 'Night Elf'])
        for race in ('Orc', 'Undead'):
            placements = [p for p in town_placements() if p[0] == race]
            self.assertEqual(len(placements), 2)

    def test_restoration_and_garrisons_require_a_surviving_hall(self):
        script = runtime_script('KLS-D-NORTH-TEST')
        unlock = re.search(r'function KLS_StoryApplyUnlock.*?endfunction', script, re.S)[0]
        self.assertIn('elseif stage == 2 and KLS_TownHall[i] != null then', unlock)
        self.assertIn('elseif stage == 3 and KLS_TownHall[i] != null then', unlock)

    def test_authored_cliffs_are_not_overlaid_with_old_barriers(self):
        script = runtime_script('KLS-D-NORTH-TEST')
        landscape = re.search(r'function KLS_BuildLandscape.*?endfunction', script, re.S)[0]
        self.assertNotIn("'LTg1'", landscape)
        self.assertNotIn("'BTsk'", landscape)

    def test_waves_use_gate_position_and_gate_is_invulnerable(self):
        script = runtime_script('KLS-D-NORTH-TEST')
        spawn = re.search(r'function KLS_Spawn takes.*?endfunction', script, re.S)[0]
        self.assertIn('local unit gate = KLS_FindInvasionGate()', spawn)
        self.assertIn('GetUnitY(gate) - 1400', spawn)
        self.assertIn('GetUnitY(gate) - 760', spawn)
        self.assertIn('call SetUnitInvulnerable(gate,true)', script)


if __name__ == '__main__':
    unittest.main()
