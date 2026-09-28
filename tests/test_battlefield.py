import sys
import struct
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'tools'))
import map_info
from terrain import expanded_pathing, expanded_terrain
from pipeline import runtime_script


class BattlefieldRegression(unittest.TestCase):
    def test_four_player_plots_form_one_horizontal_defense_row(self):
        plots = map_info.PLOTS
        self.assertEqual([round(x) for x, _ in plots], [-6000, -3300, 3300, 6000])
        self.assertEqual({round(y) for _, y in plots}, {-500})

    def test_playable_terrain_is_128_cells_square(self):
        self.assertEqual(getattr(map_info, 'MAP_CELLS', None), 128)

    def test_expanded_ground_pathing_and_editor_bounds_match_layout(self):
        template = ROOT / 'source/template'
        plots = map_info.PLOTS
        terrain = expanded_terrain((template / 'war3map.w3e').read_bytes(), plots)
        self.assertEqual(struct.unpack_from('<II', terrain, 53), (129, 129))
        self.assertEqual(struct.unpack_from('<ff', terrain, 61), (-8192.0, -8192.0))

        def texture_at(x, y):
            col = round((x + 8192) / 128)
            row = round((y + 8192) / 128)
            return struct.unpack_from('<H', terrain, 69 + (row * 129 + col) * 8 + 4)[0] & 0x3f

        self.assertEqual(texture_at(0, 3000), 3)       # stone central road
        self.assertEqual(texture_at(-6000, -500), 5)  # first build plot
        self.assertEqual(texture_at(-2200, 5200), 3)  # gate approach hills

        pathing = expanded_pathing((template / 'war3map.wpm').read_bytes())
        self.assertEqual(struct.unpack_from('<III', pathing, 4), (0, 512, 512))
        self.assertEqual(pathing[16 + 24 * 512 + 24], 64)
        self.assertEqual(pathing[16], 206)

        source_info = (template / 'war3map.w3i').read_bytes()
        info = map_info.four_player_info(source_info)
        end = 28
        for _ in range(4):
            end = source_info.index(b'\0', end) + 1
        new_strings = b"The King's Last Stand\0Kingdom Defense\0Co-op defense against forty undead waves.\0" + b'2-4\0'
        shift = len(new_strings) - (end - 28)
        self.assertEqual(struct.unpack_from('<2I', info, 130 + shift), (116, 116))
        self.assertEqual(struct.unpack_from('<4I', info, 114 + shift), (6, 6, 6, 6))
        self.assertEqual(struct.unpack_from('<8f', info, 82 + shift),
                         (-7424.0, -7424.0, 7424.0, 7424.0,
                          -7424.0, 7424.0, 7424.0, -7424.0))

    def test_generated_ground_has_no_water_or_boundary_flags(self):
        terrain = expanded_terrain((ROOT / 'source/template/war3map.w3e').read_bytes(), map_info.PLOTS)
        for offset in range(69, len(terrain), 8):
            packed = struct.unpack_from('<H', terrain, offset + 4)[0]
            self.assertEqual(packed & 0xffc0, 0, 'Ground texture must not set water/boundary flags')
        textures = {struct.unpack_from('<H', terrain, offset + 4)[0] & 0x3f
                    for offset in range(69, len(terrain), 8)}
        self.assertTrue({3, 4, 5}.issubset(textures))

    def test_camera_reaches_every_plot_and_southern_market(self):
        import re
        call = re.search(r'call SetCameraBounds\((.*?)\)', runtime_script('CAMERA'), re.S)
        bounds = [float(v) for v in call[1].split(',')]
        for x, y in map_info.PLOTS + [(0, -3900), (0, 6800)]:
            self.assertLess(bounds[0], x)
            self.assertGreater(bounds[2], x)
            self.assertLess(bounds[1], y)
            self.assertGreater(bounds[3], y)

    def test_gate_blocks_flanks_but_leaves_ground_route_to_king(self):
        data = expanded_pathing((ROOT / 'source/template/war3map.wpm').read_bytes())
        def flags(x, y):
            return data[16 + int((y + 8192) // 32) * 512 + int((x + 8192) // 32)]
        for x in range(-7000, 7001, 200):
            if abs(x) >= 1100:
                self.assertTrue(flags(x, 5200) & 2)
        # Wide enough for multiple siege units; static WPM does not prove
        # engine collision with destructibles, which is an acceptance check.
        for x in (-600, 0, 600):
            for y in range(350, 7100, 32):
                self.assertFalse(flags(x, y) & 2)

    def test_runtime_builds_gates_castle_and_player_plot_coordinates(self):
        script = runtime_script('TEST-BUILD')
        for marker in ["CreateDestructable('LTg1'", "'hC01'",
                       'set KLS_X[0] = -6000', 'set KLS_X[3] = 6000',
                       '6200 + I2R(n / 5) * 40', 'KLS_CreateShops()']:
            self.assertIn(marker, script)

    def test_closed_slots_create_no_mines_halls_altars_or_workers(self):
        import re
        script = runtime_script('CLOSED-SLOTS')
        init = re.search(r'^function KLS_Init takes nothing returns nothing[\s\S]*?^endfunction$',
                         script, re.M)[0]
        self.assertNotIn('Reserved Defender Plot', init)
        self.assertRegex(init, r'if KLS_Active\[i\] then[\s\S]*?KLS_CreateUnit\(Player\(PLAYER_NEUTRAL_PASSIVE\), \'ngol\'[\s\S]*?KLS_CreateUnit\(Player\(i\), \'htow\'[\s\S]*?KLS_CreateUnit\(Player\(i\), \'h000\'[\s\S]*?KLS_CreateUnit\(Player\(i\), \'hpea\'[\s\S]*?endif')
        self.assertNotRegex(init, r'else\s+set u = KLS_CreateUnit\(Player\(PLAYER_NEUTRAL_PASSIVE\), \'htow\'')


if __name__ == '__main__':
    unittest.main()
