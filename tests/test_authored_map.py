"""Round-trip tests for World Editor authored terrain and art layers."""
import hashlib
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'tools'))

from archive_pack import MPQArchive, member, pack
from map_info import four_player_info
from terrain import expanded_pathing, expanded_terrain
from authored_map import capture_authored_map, read_authored_layer


BUILD_ID = 'KLS-D-AUTHORED01'
ART_MEMBERS = (
    'war3map.w3e',
    'war3map.wpm',
    'war3map.doo',
    'war3map.shd',
    'war3map.mmp',
    'war3mapMap.blp',
)


def build_info(build_id):
    info = four_player_info((ROOT / 'source/template/war3map.w3i').read_bytes())
    title_end = info.index(b'\0', 28) + 1
    return info[:28] + ('KLS DEVELOPMENT ' + build_id).encode() + b'\0' + info[title_end:]


class AuthoredMapRoundTrip(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.baseline = ROOT / 'backups/Blank-DE.w3m'
        if not cls.baseline.exists():
            cls.baseline = ROOT / 'TheKingsLastStand.blank-backup.w3m'
        cls.baseline_archive = MPQArchive(cls.baseline, listfile=False)

    @classmethod
    def tearDownClass(cls):
        cls.baseline_archive.file.close()

    def source_layers(self):
        template = ROOT / 'source/template'
        return {
            'war3map.w3e': expanded_terrain((template / 'war3map.w3e').read_bytes(),
                                            [(-6000, -500), (-3300, -500), (3300, -500), (6000, -500)]),
            'war3map.wpm': expanded_pathing((template / 'war3map.wpm').read_bytes()),
            'war3map.doo': member(self.baseline_archive, 'war3map.doo'),
            'war3map.shd': bytes(768 * 768),
            'war3map.mmp': member(self.baseline_archive, 'war3map.mmp'),
            'war3mapMap.blp': member(self.baseline_archive, 'war3mapMap.blp'),
        }

    def make_map(self, path, overrides=None):
        replacements = self.source_layers()
        replacements['war3map.w3i'] = build_info(BUILD_ID)
        replacements.update(overrides or {})
        pack(self.baseline, path, replacements)
        return replacements

    def test_runtime_preserves_authored_ground_textures(self):
        game = (ROOT / 'source/game.j').read_text(encoding='utf-8')
        self.assertFalse('call SetTerrainType(' in game,
                         'Match startup must not repaint authored roads or plot edges.')
        self.assertNotIn('call KLS_StampPlot(', game)
        self.assertIn("KLS_CreateDestructable('LTg1'", game)
        self.assertIn('call KLS_AddTree(', game)
        heroes = (ROOT / 'source/heroes.j').read_text(encoding='utf-8')
        self.assertNotIn('call SetTerrainType(', heroes)

    def test_capture_round_trips_every_world_editor_art_layer_with_provenance(self):
        with tempfile.TemporaryDirectory() as folder:
            map_path = Path(folder) / (BUILD_ID + '-Development.w3m')
            bundle_path = Path(folder) / 'editor-layer.zip'
            expected = self.make_map(map_path)

            captured = capture_authored_map(map_path, BUILD_ID, bundle_path)
            metadata, layers = read_authored_layer(bundle_path)

            self.assertEqual(captured['source_build_id'], BUILD_ID)
            self.assertEqual(metadata['source_build_id'], BUILD_ID)
            for name in ART_MEMBERS:
                with self.subTest(member=name):
                    self.assertEqual(layers[name], expected[name])
                    self.assertEqual(metadata['members'][name]['sha256'],
                                     hashlib.sha256(expected[name]).hexdigest())

    def test_capture_rejects_a_map_from_another_build(self):
        with tempfile.TemporaryDirectory() as folder:
            map_path = Path(folder) / 'older-Development.w3m'
            bundle_path = Path(folder) / 'editor-layer.zip'
            self.make_map(map_path, {'war3map.w3i': build_info('KLS-D-OLD')})

            with self.assertRaisesRegex(ValueError, 'build ID'):
                capture_authored_map(map_path, BUILD_ID, bundle_path)
            self.assertFalse(bundle_path.exists())

    def test_capture_rejects_bad_terrain_or_pathing_extents_without_writing_a_bundle(self):
        invalid_layers = (
            ('war3map.w3e', b'not an expanded terrain file'),
            ('war3map.wpm', b'MP3W' + bytes(12)),
        )
        for member_name, invalid in invalid_layers:
            with self.subTest(member=member_name), tempfile.TemporaryDirectory() as folder:
                map_path = Path(folder) / (BUILD_ID + '-Development.w3m')
                bundle_path = Path(folder) / 'editor-layer.zip'
                self.make_map(map_path, {member_name: invalid})

                with self.assertRaises(ValueError):
                    capture_authored_map(map_path, BUILD_ID, bundle_path)
                self.assertFalse(bundle_path.exists())

    def test_read_rejects_layer_payloads_that_do_not_match_the_capture_manifest(self):
        with tempfile.TemporaryDirectory() as folder:
            map_path = Path(folder) / (BUILD_ID + '-Development.w3m')
            bundle_path = Path(folder) / 'editor-layer.zip'
            self.make_map(map_path)
            capture_authored_map(map_path, BUILD_ID, bundle_path)

            import zipfile
            with zipfile.ZipFile(bundle_path) as archive:
                entries = {name: archive.read(name) for name in archive.namelist()}
            entries['war3map.w3e'] = b'tampered terrain'
            with zipfile.ZipFile(bundle_path, 'w', compression=zipfile.ZIP_DEFLATED) as archive:
                for name, data in entries.items():
                    archive.writestr(name, data)

            with self.assertRaisesRegex(ValueError, 'checksum'):
                read_authored_layer(bundle_path)


if __name__ == '__main__':
    unittest.main()
