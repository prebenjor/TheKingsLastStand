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

    def test_playable_terrain_is_192_cells_square(self):
        self.assertEqual(getattr(map_info, 'MAP_CELLS', None), 192)

    def test_settlement_and_relocated_service_coordinates_match_catalog(self):
        towns = getattr(map_info, 'TOWNS', ())
        self.assertEqual(len(towns), 4)
        self.assertEqual({(name, round(x), round(y)) for name, x, y in towns},
                         {('Human', 0, -9000), ('Orc', 1792, -2304),
                          ('Night Elf', 9000, 0), ('Undead', 2112, -2560)})

    def test_expanded_ground_pathing_and_editor_bounds_match_layout(self):
        template = ROOT / 'source/template'
        plots = map_info.PLOTS
        terrain = expanded_terrain((template / 'war3map.w3e').read_bytes(), plots)
        self.assertEqual(struct.unpack_from('<II', terrain, 53), (193, 193))
        self.assertEqual(struct.unpack_from('<ff', terrain, 61), (-12288.0, -12288.0))

        def texture_at(x, y):
            col = round((x + 12288) / 128)
            row = round((y + 12288) / 128)
            return struct.unpack_from('<H', terrain, 69 + (row * 193 + col) * 8 + 4)[0] & 0x3f

        self.assertEqual(texture_at(0, 3000), 3)       # stone central road
        self.assertEqual(texture_at(-6000, -500), 5)  # first build plot
        self.assertEqual(texture_at(-2200, 5200), 3)  # gate approach hills
        self.assertEqual(texture_at(-9000, 0), 3)     # western settlement road
        self.assertEqual(texture_at(9000, 0), 3)      # eastern settlement road
        self.assertEqual(texture_at(0, 9000), 3)      # northern settlement road

        pathing = expanded_pathing((template / 'war3map.wpm').read_bytes())
        self.assertEqual(struct.unpack_from('<III', pathing, 4), (0, 768, 768))
        self.assertEqual(pathing[16 + 24 * 768 + 24], 64)
        self.assertEqual(pathing[16], 206)

        source_info = (template / 'war3map.w3i').read_bytes()
        info = map_info.four_player_info(source_info)
        end = 28
        for _ in range(4):
            end = source_info.index(b'\0', end) + 1
        new_strings = b"The King's Last Stand\0Kingdom Defense\0Co-op defense against forty undead waves.\0" + b'2-4\0'
        shift = len(new_strings) - (end - 28)
        self.assertEqual(struct.unpack_from('<2I', info, 130 + shift), (180, 180))
        self.assertEqual(struct.unpack_from('<4I', info, 114 + shift), (6, 6, 6, 6))
        self.assertEqual(struct.unpack_from('<8f', info, 82 + shift),
                         (-11520.0, -11520.0, 11520.0, 11520.0,
                          -11520.0, 11520.0, 11520.0, -11520.0))

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
        for x, y in map_info.PLOTS + [(0, -3900), (0, 6800)] + [(x, y) for _, x, y in map_info.TOWNS]:
            self.assertLess(bounds[0], x)
            self.assertGreater(bounds[2], x)
            self.assertLess(bounds[1], y)
            self.assertGreater(bounds[3], y)

    def test_gate_blocks_flanks_but_leaves_ground_route_to_king(self):
        data = expanded_pathing((ROOT / 'source/template/war3map.wpm').read_bytes())
        def flags(x, y):
            pixels = map_info.MAP_CELLS * 4
            return data[16 + int((y + map_info.MAP_EDGE) // 32) * pixels + int((x + map_info.MAP_EDGE) // 32)]
        for x in range(-7000, 7001, 200):
            if abs(x) >= 1100:
                self.assertTrue(flags(x, 5200) & 2)
        # Wide enough for multiple siege units; static WPM does not prove
        # engine collision with destructibles, which is an acceptance check.
        for x in (-600, 0, 600):
            for y in range(350, 7100, 32):
                self.assertFalse(flags(x, y) & 2)

    def test_runtime_uses_northern_origin_castle_and_player_plot_coordinates(self):
        script = runtime_script('TEST-BUILD')
        for marker in ['call KLS_InvasionGateInit()', "'hC01'",
                       'set KLS_X[0] = -6000', 'set KLS_X[3] = 6000',
                       'GetUnitY(gate) - 1400', 'KLS_CreateShops()']:
            self.assertIn(marker, script)

    def test_base_lumber_stands_are_closer_without_occupying_the_hall_or_altar_side(self):
        script = runtime_script('BASE-TREE-SPACING')
        self.assertIn('KLS_AddTree(KLS_X[i]+150+j*150,KLS_Y[i]-500)', script)
        self.assertIn('KLS_AddTree(KLS_X[i]+150+j*150,KLS_Y[i]-700)', script)
        self.assertNotIn('KLS_AddTree(KLS_X[i]+180+j*180,KLS_Y[i]-650)', script)
        self.assertNotIn('KLS_AddTree(KLS_X[i]+180+j*180,KLS_Y[i]-850)', script)

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
