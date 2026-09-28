"""Regressions for the launch/archive failures seen in the first handoff."""
import sys
import shutil
import tempfile
import unittest
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'tools'))
from map_archive import MPQArchive, read_encrypted
from pack import pack


class DiagnosticOutputPaths(unittest.TestCase):
    def test_build_writes_the_current_development_name_and_preserves_the_open_editor_file(self):
        import pipeline
        from unittest.mock import patch

        with tempfile.TemporaryDirectory() as folder:
            project = Path(folder) / 'project'
            build_dir = project / 'build'
            build_dir.mkdir(parents=True)
            dist_dir = project / 'dist'
            dist_dir.mkdir(parents=True)
            shutil.copytree(ROOT / 'source', project / 'source')
            tools_dir = project / 'tools'
            tools_dir.mkdir()
            for source_file in (ROOT / 'tools').glob('*.py'):
                shutil.copy2(source_file, tools_dir / source_file.name)
            shutil.copytree(ROOT / 'tools/reference/installed', tools_dir / 'reference/installed')
            backups_dir = project / 'backups'
            backups_dir.mkdir()
            shutil.copy2(ROOT / 'backups/Blank-DE.w3m', backups_dir / 'Blank-DE.w3m')

            legacy = build_dir / 'DIAGNOSTIC-TheKingsLastStand.w3m'
            legacy.write_bytes(b'older editor copy held open by the editor')

            with patch.object(pipeline, 'ROOT', project):
                manifest = pipeline.build()

            output = Path(manifest['output_path'])
            self.assertEqual(output.parent, dist_dir)
            self.assertEqual(output.name, manifest['build_id']+'-Development.w3m')
            self.assertNotEqual(output, legacy)
            self.assertTrue(output.is_file())
            self.assertEqual(legacy.read_bytes(), b'older editor copy held open by the editor')
            self.assertEqual(manifest['checks']['editor_test_map'], 'pending')
            self.assertEqual(manifest['checks']['editor_save_reopen'], 'pending')
            published = json.loads((dist_dir / 'build-manifest.json').read_text())
            self.assertEqual(published['output_path'], 'dist/' + output.name)
            self.assertEqual(published['sha256'], manifest['sha256'])


def read(a, name):
    entry = a.get_hash_table_entry(name)
    if entry is None:
        raise AssertionError('Missing member: ' + name)
    flags = a.block_table[entry.block_table_index].flags
    return read_encrypted(a, name) if flags & 0x10000 else a.read_file(name)


class ArchiveRegression(unittest.TestCase):
    def setUp(self):
        self.base = ROOT / 'backups/Blank-DE.w3m'
        if not self.base.exists():
            self.base = ROOT / 'TheKingsLastStand.blank-backup.w3m'

    def test_added_objects_are_enumerated_and_readable(self):
        additions = {'war3map.w3u': b'unit-object-fixture', 'war3map.w3t': b'item-object-fixture', 'war3mapMisc.txt': b'[Misc]\nMaxHeroLevel=30\n'}
        with tempfile.TemporaryDirectory() as folder:
            target = Path(folder) / 'map.w3m'
            pack(self.base, target, additions)
            a = MPQArchive(target, listfile=False)
            try:
                listed = read(a, '(listfile)').decode().splitlines()
                for name, data in additions.items():
                    self.assertIn(name, listed)
                    self.assertEqual(read(a, name), data)
            finally:
                a.file.close()


    def test_equipment_catalog_has_five_tiers_and_two_icon_shops_per_tier(self):
        from objects import item_catalog
        catalog = item_catalog()
        installed_ids = set()
        import re
        for line in (ROOT / 'tools/reference/installed/ItemData.slk').read_text().splitlines():
            if line.startswith('C;') and ';Y' in line and ';X1;' in line:
                match = re.search(r';K"?([^";]+)', line)
                if match: installed_ids.add(match.group(1))
        self.assertEqual(len(catalog), 83)
        self.assertEqual(len({entry['rawcode'] for entry in catalog}), 83)
        self.assertTrue({entry['rawcode'] for entry in catalog}.isdisjoint(installed_ids))
        self.assertEqual({entry['tier'] for entry in catalog}, set(range(5)))
        self.assertEqual({entry['family'] for entry in catalog}, {
            'Blade', 'Bow', 'Staff', 'Shield', 'Focus', 'Helmet', 'Chest',
            'Gloves', 'Boots', 'Offensive Ring', 'Defensive Ring', 'Trinket', 'Cape',
            'Might Chestplate', 'Windrunner Boots', 'Arcanist Focus'})
        self.assertEqual([sum(e['tier'] == tier and not e.get('crafted') for e in catalog) for tier in range(5)], [16]*5)
        self.assertEqual(len({e['parent'] for e in catalog if e['family'] == 'Blade'}), 5)
        self.assertEqual(len({e['parent'] for e in catalog if e['family'] == 'Bow'}), 2)
        self.assertEqual(len({e['parent'] for e in catalog if e['family'] == 'Trinket'}), 5)
        rows = {}
        row_num = 0
        import re
        for line in (ROOT / 'tools/reference/installed/ItemData.slk').read_text().splitlines():
            if not line.startswith('C;'):
                continue
            match = re.search(r';Y(\d+)', line)
            if match:
                row_num = int(match.group(1))
            col = re.search(r';X(\d+)', line)
            val = re.search(r';K(.*)', line)
            if col and val:
                rows.setdefault(row_num, {})[int(col.group(1))] = val.group(1).strip('"')
        for item in catalog:
            parent = next(row for row in rows.values() if row.get(1) == item['parent'])
            self.assertEqual(parent.get(5), 'Equipment', item['parent'])
            self.assertEqual({'Head':1,'Chest':2,'Gloves':3,'Boots':4,'Ring':5,'Primary':6,'Offhand':7,'Trinket':8}[parent.get(32)], item['slot'], item['name'])
        self.assertNotIn('Ibpk', {e['rawcode'] for e in catalog})
        from equipment_catalog import catalog_script
        generated=catalog_script()
        for tier in range(5):
            self.assertIn(f'AddItemToStock(KLS_Shops[{tier*2}],',generated)
            self.assertIn(f'AddItemToStock(KLS_Shops[{tier*2+1}],',generated)
        self.assertNotIn('DialogAddButton', generated)

    def test_backpack_uses_native_extended_inventory_abilities(self):
        from objects import items
        blob=items()
        self.assertIn(b'ebua\x00\x00\x00\x00', blob)
        self.assertNotIn(b'Ibpk', blob)
        self.assertIn(b'AIni,AEqu,ASde', blob)
        self.assertNotIn(b'ATua', items())

    def test_preserves_all_unmodified_editor_members(self):
        with tempfile.TemporaryDirectory() as folder:
            target = Path(folder) / 'map.w3m'
            pack(self.base, target, {'war3map.j': b'// replacement script\n'})
            a = MPQArchive(self.base, listfile=False)
            b = MPQArchive(target, listfile=False)
            try:
                for name in read(a, '(listfile)').decode().splitlines():
                    if name != 'war3map.j':
                        self.assertEqual(read(a, name), read(b, name), name)
                self.assertEqual(read(b, 'war3map.j'), b'// replacement script\n')
            finally:
                a.file.close()
                b.file.close()


class InstalledEditorData(unittest.TestCase):
    def test_build_reference_pins_the_installed_forsaken_kingdom_object_tables(self):
        from pipeline import check_api, digest
        installed = check_api()
        expected = {'ItemData.slk', 'UnitData.slk', 'AbilityData.slk',
                    'UnitMetaData.slk', 'AbilityMetaData.slk', 'ItemAbilityFunc.txt',
                    'UnitBalance.slk', 'UnitUI.slk', 'UnitAbilities.slk',
                    'UnitWeapons.slk', 'commandbuttons.txt'}
        self.assertTrue(expected <= installed['files'].keys(), installed['files'].keys())
        for name in expected:
            reference = ROOT / 'tools/reference/installed' / name
            self.assertEqual(digest(reference.read_bytes()), installed['files'][name]['sha256'], name)


if __name__ == '__main__':
    unittest.main()
