"""Native preview serialization, shared placement sources and cleanup boundary."""
import re
import struct
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'tools'))
from editor_layout import placement_data, unit_record, RECORD_SIZE, PREVIEW_OWNER, terrain_height
from layout_catalog import editor_placements, market_placements, POINTS
from map_info import PLOTS
from pipeline import runtime_script
from terrain import expanded_terrain
from town_catalog import town_placements


class EditorLayout(unittest.TestCase):
    def terrain(self):
        return expanded_terrain((ROOT / 'source/template/war3map.w3e').read_bytes(), PLOTS)

    def records(self, data):
        self.assertEqual(data[:4], b'W3do')
        version, subversion, count = struct.unpack_from('<3I', data, 4)
        self.assertEqual((version, subversion), (13, 11))
        self.assertEqual(len(data), 16 + count * RECORD_SIZE)
        return [data[16 + i * RECORD_SIZE:16 + (i + 1) * RECORD_SIZE] for i in range(count)]

    def test_serializer_matches_unit_record_saved_by_installed_world_editor(self):
        # This unmodified native record is from the user's own saved map.
        native = (ROOT / 'tests/fixtures/editor-unit-13-11.bin').read_bytes()
        raw = native[:4].decode('ascii')
        x, y, z, angle = struct.unpack_from('<4f', native, 8)
        owner = struct.unpack_from('<i', native, 45)[0]
        number = struct.unpack_from('<i', native, 115)[0]
        self.assertEqual(unit_record(raw, x, y, z, owner, number, angle=angle), native)

    def test_game_package_contains_only_four_matching_native_start_markers(self):
        records = self.records(placement_data(self.terrain()))
        self.assertEqual(len(records), 4)
        for i, (record, point) in enumerate(zip(records, PLOTS)):
            self.assertEqual(record[:4], b'sloc')
            self.assertEqual(struct.unpack_from('<2f', record, 8), point)
            self.assertEqual(struct.unpack_from('<i', record, 45)[0], i)

    def test_editor_copy_adds_every_preview_with_reserved_owner_and_unique_number(self):
        records = self.records(placement_data(self.terrain(), previews=True))
        previews = records[4:]
        self.assertEqual(len(previews), 85)
        self.assertEqual(len(previews), len(editor_placements()))
        for record, (raw, x, y, _) in zip(previews, editor_placements()):
            self.assertEqual(record[:4].decode(), raw)
            self.assertEqual(struct.unpack_from('<2f', record, 8), (x, y))
            self.assertEqual(struct.unpack_from('<i', record, 45)[0], PREVIEW_OWNER)
        self.assertEqual([struct.unpack_from('<i', r, 115)[0] for r in records], list(range(len(records))))

    def test_shared_catalog_covers_market_four_towns_hub_and_plot_resources(self):
        self.assertEqual(len(market_placements()), 13)
        self.assertEqual(len(town_placements()), 32)
        placements = editor_placements()
        self.assertEqual(sum(label.startswith('Hero choice') for *_, label in placements), 25)
        self.assertEqual(sum(raw == 'ngol' for raw, *_ in placements), 4)
        script = runtime_script('KLS-D-LAYOUTTEST')
        for name, (x, y) in POINTS.items():
            self.assertIn(f'real KLS_{name}X = {x:.1f}', script)
            self.assertIn(f'real KLS_{name}Y = {y:.1f}', script)
        self.assertNotIn('call SetTerrainType(', script)
        self.assertIn('KLS_MarketX(tier*2+i),KLS_MarketY(tier*2+i)', script)
        self.assertIn('KLS_HeroHubX + ModuloInteger(n, KLS_HubColumns)', script)

    def test_cleanup_precedes_landscape_and_spawn_and_survives_editor_trigger_export(self):
        from gui_sources import gui_sources
        script = runtime_script('KLS-D-LAYOUTTEST')
        init = re.search(r'function KLS_Init takes.*?endfunction', script, re.S)[0]
        self.assertLess(init.index('if KLS_Initialized then'), init.index('call KLS_ClearEditorPreviews()'))
        self.assertLess(init.index('call KLS_ClearEditorPreviews()'), init.index('call KLS_BuildLandscape()'))
        cleanup = re.search(r'function KLS_ClearEditorPreviews takes.*?endfunction', script, re.S)[0]
        self.assertIn('Player(bj_PLAYER_NEUTRAL_EXTRA)', cleanup)
        self.assertIn('call GroupRemoveUnit(previews,preview)', cleanup)
        self.assertIn('call RemoveUnit(preview)', cleanup)
        self.assertIn('call DestroyGroup(previews)', cleanup)
        _, _, wct = gui_sources(script)
        self.assertIn(b'call KLS_ClearEditorPreviews()', wct)
        self.assertIn(b'Player(bj_PLAYER_NEUTRAL_EXTRA)', wct)

    def test_preview_height_tracks_authored_ground_and_rejects_outside_bounds(self):
        terrain = self.terrain()
        self.assertTrue(-1000 < terrain_height(terrain, 0, 0) < 1000)
        with self.assertRaises(ValueError):
            terrain_height(terrain, 13000, 0)


if __name__ == '__main__':
    unittest.main()
