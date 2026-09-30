import json
import struct
import sys
import tempfile
import unittest
from unittest.mock import patch
from types import SimpleNamespace
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'tools'))
from editor_workshop import decode_objects, decode_units, compare_members, preserve_baseline, review_map, inventory_gaps, MapMembers
from editor_layout import unit_record


def objects(version=3, value=27.5, rank=4):
    record = b'AHas' + bytes(4)
    if version == 3:
        record += struct.pack('<2i', 1, 0)
    record += struct.pack('<i', 1) + b'hsa2' + struct.pack('<3i', 1, rank, 0)
    record += struct.pack('<f', value) + bytes(4)
    return struct.pack('<2i', version, 1) + record + struct.pack('<i', 0)


def units(x=0, owner=26, raw='hC01'):
    return b'W3do' + struct.pack('<3i', 13, 11, 1) + unit_record(raw, x, -500, 0, owner, 4)


class WorkshopTests(unittest.TestCase):
    def test_unlisted_archive_entries_are_flagged_even_when_unchanged(self):
        known = SimpleNamespace(block_table_index=0, hash_a=1, hash_b=2)
        unknown = SimpleNamespace(block_table_index=1, hash_a=3, hash_b=4)
        deleted = SimpleNamespace(block_table_index=0xFFFFFFFE, hash_a=9, hash_b=10)
        archive = SimpleNamespace(hash_table=[known, unknown, deleted],
                                  get_hash_table_entry=lambda name: known if name == 'known' else None)
        gaps = inventory_gaps(archive, ['known'])
        self.assertEqual(len(gaps), 1)
        self.assertEqual(gaps[0]['block_index'], 1)
        contents = MapMembers({'known': b'unchanged'})
        contents.unlisted = gaps
        report = compare_members(contents, contents, {})
        self.assertTrue(report['archive_inventory_warnings'])
        self.assertTrue(any('Unenumerated' in warning for warning in report['unresolved']))

    def native_members(self, x=0):
        records = [unit_record('sloc', 0, 0, 0, i, i) for i in range(4)]
        records.append(unit_record('hC01', x, -500, 0, 26, 4))
        return {'war3mapUnits.doo': b'W3do' + struct.pack('<3i', 13, 11, 5) + b''.join(records),
                'war3map.w3u': struct.pack('<3i', 3, 0, 0),
                'war3map.w3t': struct.pack('<3i', 3, 0, 0), 'war3map.w3a': objects()}

    def layout(self):
        return {'build_id': 'KLS-D-TEST', 'sha256': 'generated', 'placements': [['hC01', 0, -500, 'Castle']]}

    def test_baseline_requires_closed_native_save_and_matching_build(self):
        with tempfile.TemporaryDirectory() as directory:
            with self.assertRaisesRegex(ValueError, 'closed'):
                preserve_baseline('map.w3m', self.layout(), directory, 1)
            with patch('editor_workshop.read_map', return_value=(b'native', self.native_members(), 'KLS-D-OLD')):
                with self.assertRaisesRegex(ValueError, 'Stale'):
                    preserve_baseline('map.w3m', self.layout(), directory, 1, True)
            layout = self.layout()
            import hashlib
            layout['sha256'] = hashlib.sha256(b'native').hexdigest()
            with patch('editor_workshop.read_map', return_value=(b'native', self.native_members(), 'KLS-D-TEST')):
                with self.assertRaisesRegex(ValueError, 'Save once'):
                    preserve_baseline('map.w3m', layout, directory, 1, True)

    def test_baseline_archives_exact_bytes_and_refuses_overwrite(self):
        with tempfile.TemporaryDirectory() as directory:
            with patch('editor_workshop.read_map', return_value=(b'native', self.native_members(), 'KLS-D-TEST')):
                baseline = preserve_baseline('map.w3m', self.layout(), directory, 1, True)
                self.assertEqual((baseline.parent / 'map.w3m').read_bytes(), b'native')
                self.assertEqual(json.loads(baseline.read_text())['labels']['4'], 'Castle')
                with self.assertRaises(FileExistsError):
                    preserve_baseline('map.w3m', self.layout(), directory, 1, True)

    def test_baseline_refuses_untraceable_references(self):
        with tempfile.TemporaryDirectory() as directory:
            changed = self.native_members()
            changed['war3mapUnits.doo'] = units(raw='htow')
            with patch('editor_workshop.read_map', return_value=(b'native', changed, 'KLS-D-TEST')):
                with self.assertRaisesRegex(ValueError, 'identities'):
                    preserve_baseline('map.w3m', self.layout(), directory, 1, True)

    def test_review_preserves_map_reports_move_and_rejects_tampered_baseline(self):
        with tempfile.TemporaryDirectory() as directory:
            old = (b'native', self.native_members(), 'KLS-D-TEST')
            new = (b'edited', self.native_members(123), 'KLS-D-TEST')
            with patch('editor_workshop.read_map', return_value=old):
                baseline = preserve_baseline('map.w3m', self.layout(), directory, 1, True)
            with patch('editor_workshop.read_map', side_effect=[old, new]):
                report = review_map('edited.w3m', baseline, directory, 1, True)
                self.assertEqual((report.parent / 'edited.w3m').read_bytes(), b'edited')
                self.assertEqual(json.loads(report.read_text())['units'][0]['changes']['position']['after'][0], 123)
            with patch('editor_workshop.read_map', return_value=(b'tampered', old[1], old[2])):
                with self.assertRaisesRegex(ValueError, 'checksum'):
                    review_map('edited.w3m', baseline, directory, 1, True)

    def test_review_rejects_wrong_chapter_and_build(self):
        with tempfile.TemporaryDirectory() as directory:
            old = (b'native', self.native_members(), 'KLS-D-TEST')
            with patch('editor_workshop.read_map', return_value=old):
                baseline = preserve_baseline('map.w3m', self.layout(), directory, 1, True)
            with self.assertRaisesRegex(ValueError, 'chapter'):
                review_map('edited.w3m', baseline, directory, 2, True)
            with patch('editor_workshop.read_map', side_effect=[old, (b'edited', old[1], 'KLS-D-OTHER')]):
                with self.assertRaisesRegex(ValueError, 'different builds'):
                    review_map('edited.w3m', baseline, directory, 1, True)

    def test_object_versions_normalize_and_rank_change_is_named(self):
        self.assertEqual(decode_objects(objects(2), True), decode_objects(objects(3), True))
        report = compare_members({'war3map.w3a': objects()}, {'war3map.w3a': objects(value=30)}, {})
        self.assertEqual(report['objects']['war3map.w3a'][0]['key'], 'original/AHas/hsa2/4/0')
        self.assertEqual(report['objects']['war3map.w3a'][0]['after']['value'], 30)

    def test_creation_identity_tracks_move_and_flags_replacement(self):
        report = compare_members({'war3mapUnits.doo': units()}, {'war3mapUnits.doo': units(100)}, {'4': 'Castle'})
        self.assertEqual(report['units'][0]['label'], 'Castle')
        self.assertEqual(report['units'][0]['changes']['position']['after'][0], 100)
        replaced = compare_members({'war3mapUnits.doo': units()}, {'war3mapUnits.doo': units(raw='htow')}, {})
        self.assertEqual(replaced['units'][0]['status'], 'replacement-needs-review')

    def test_duplicate_creation_id_is_not_guessed(self):
        data = units()
        duplicate = data[:12] + struct.pack('<i', 2) + data[16:] * 2
        with self.assertRaisesRegex(ValueError, 'Duplicate'):
            decode_units(duplicate)

    def test_unknown_and_malformed_changes_remain_visible(self):
        report = compare_members({'war3map.w3a': objects()}, {'war3map.w3a': b'broken', 'custom.ai': b'AI'}, {})
        self.assertTrue(report['unresolved'])
        self.assertIn('custom.ai', report['other_changed_members'])
        self.assertIn('war3map.w3a', report['changed_members'])

    def test_trigger_edits_and_art_are_separate(self):
        report = compare_members({'war3map.j': b'function Foo takes nothing returns nothing\nendfunction\n', 'war3map.w3e': b'a'}, {'war3map.j': b'function Foo takes nothing returns nothing\ncall Bar()\nendfunction\n', 'war3map.w3e': b'b', 'war3map.wtg': b'GUI'}, {})
        self.assertEqual(report['script_functions_changed'], ['Foo'])
        self.assertIn('war3map.wtg', report['trigger_members_changed'])
        self.assertEqual(report['art_members_changed'], ['war3map.w3e'])

    def test_native_optional_inventory_does_not_shift_identity(self):
        raw = unit_record('Hpal', 0, 0, 0, 26, 19)
        raw = raw[:91] + struct.pack('<i', 1) + struct.pack('<i4s', 0, b'ratf') + raw[95:]
        decoded = decode_units(b'W3do' + struct.pack('<3i', 13, 11, 1) + raw)
        self.assertEqual(decoded['19']['rawcode'], 'Hpal')
        self.assertEqual(decoded['19']['inventory'], [{'slot': 0, 'item': 'ratf'}])


if __name__ == '__main__':
    unittest.main()
