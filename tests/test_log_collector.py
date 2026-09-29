"""Log snapshots must not be attributed to a stale or test-only build manifest."""
import json
import hashlib
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'tools'))
import collect_test_logs


class LogCollectorRegression(unittest.TestCase):
    def test_rejects_manifest_that_does_not_match_the_build_artifact(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            build = root / 'build'
            build.mkdir()
            (build / 'DIAGNOSTIC.w3m').write_bytes(b'actual map')
            (build / 'diagnostic-manifest.json').write_text(json.dumps({
                'build_id': 'TEST-FAKE',
                'output_path': str(build / 'DIAGNOSTIC.w3m'),
                'sha256': '0' * 64,
            }))
            with patch.object(collect_test_logs, 'ROOT', root):
                with self.assertRaisesRegex(ValueError, 'does not match'):
                    collect_test_logs.collect()
            self.assertFalse((root / 'test-results').exists())

    def test_snapshot_separates_current_and_stale_map_log_references(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            build = root / 'build'
            build.mkdir()
            artifact = build / 'KLS-D-current1234-Development.w3m'
            artifact.write_bytes(b'current map')
            (build / 'diagnostic-manifest.json').write_text(json.dumps({
                'build_id': 'KLS-D-current1234',
                'output_path': str(artifact),
                'sha256': hashlib.sha256(b'current map').hexdigest(),
            }))
            logs = root / 'Documents' / 'Warcraft III' / 'Logs'
            logs.mkdir(parents=True)
            (logs / 'War3Log.txt').write_text(
                'Opening map - Maps/TheKingsLastStand/KLS-D-oldbuild9876-Development.w3m\n'
                'model creation failed - old-model.mdl\n'
                'Opening map - Maps/TheKingsLastStand/KLS-D-current1234-Development.w3m\n')
            (logs / 'War3EditorLog.txt').write_text(
                'Command Line: -loadfile KLS-D-current1234-Development.w3m\n')
            with patch.object(collect_test_logs, 'ROOT', root), \
                    patch.object(collect_test_logs.Path, 'home', return_value=root):
                collect_test_logs.collect()
            output = next((root / 'test-results').iterdir())

            report = json.loads((output / 'collection.json').read_text())
            self.assertFalse(report['played_build_confirmed'])
            self.assertEqual(report['current_build_references'][0]['build_id'],
                             'KLS-D-current1234')
            self.assertIn('KLS-D-oldbuild9876', report['other_build_ids'])
            findings = (output / 'findings.txt').read_text()
            self.assertIn('Current build KLS-D-current1234 is referenced', findings)
            self.assertIn('Other or older build IDs referenced: KLS-D-oldbuild9876', findings)
            self.assertIn('do not confirm gameplay', findings)
            self.assertIn('model creation failed - old-model.mdl', findings)
            self.assertIn('last build reference=KLS-D-oldbuild9876; correlation only', findings)

    def test_snapshot_warns_when_all_captured_engine_errors_are_unattributed(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            build = root / 'build'
            build.mkdir()
            artifact = build / 'KLS-D-current1234-Development.w3m'
            artifact.write_bytes(b'current map')
            (build / 'diagnostic-manifest.json').write_text(json.dumps({
                'build_id': 'KLS-D-current1234',
                'output_path': str(artifact),
                'sha256': hashlib.sha256(b'current map').hexdigest(),
            }))
            logs = root / 'Documents' / 'Warcraft III' / 'Logs'
            logs.mkdir(parents=True)
            (logs / 'War3Log.txt').write_text('model creation failed - unknown.mdl\n')
            with patch.object(collect_test_logs, 'ROOT', root), \
                    patch.object(collect_test_logs.Path, 'home', return_value=root):
                collect_test_logs.collect()
            output = next((root / 'test-results').iterdir())

            report = json.loads((output / 'collection.json').read_text())
            self.assertEqual(report['current_build_references'], [])
            findings = (output / 'findings.txt').read_text()
            self.assertIn('No captured log references current build KLS-D-current1234', findings)
            self.assertIn('cannot be attributed to the current build', findings)

    def test_snapshot_classifies_warning_only_spawn_and_load_failures(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            build = root / 'build'
            build.mkdir()
            artifact = build / 'KLS-D-current1234-Development.w3m'
            artifact.write_bytes(b'current map')
            (build / 'diagnostic-manifest.json').write_text(json.dumps({
                'build_id': 'KLS-D-current1234',
                'output_path': str(artifact),
                'sha256': hashlib.sha256(b'current map').hexdigest(),
            }))
            logs = root / 'Documents' / 'Warcraft III' / 'Logs'
            logs.mkdir(parents=True)
            (logs / 'War3Log.txt').write_text(
                'Opening map - KLS-D-current1234-Development.w3m\n'
                'WARNING: Spawn skipped; unable to create unit hfoo at (1, 2)\n'
                'Could not load model: missing-texture.mdl\n')
            with patch.object(collect_test_logs, 'ROOT', root), \
                    patch.object(collect_test_logs.Path, 'home', return_value=root):
                collect_test_logs.collect()
            output = next((root / 'test-results').iterdir())

            report = json.loads((output / 'collection.json').read_text())
            diagnostics = report['diagnostics']
            self.assertEqual(len(diagnostics), 2)
            self.assertEqual(diagnostics[0]['severity'], 'warning')
            self.assertEqual(diagnostics[0]['kind'], 'spawn_or_load')
            self.assertEqual(diagnostics[0]['build_reference'], 'KLS-D-current1234')
            self.assertEqual(diagnostics[1]['severity'], 'failure')
            self.assertEqual(diagnostics[1]['kind'], 'spawn_or_load')
            self.assertEqual(report['diagnostic_summary'], {
                'error': 0, 'fatal': 0, 'warning': 1, 'failure': 1,
                'spawn_or_load': 2, 'total': 2,
            })
            findings = (output / 'findings.txt').read_text()
            self.assertIn('[warning/spawn_or_load; last build reference=KLS-D-current1234; correlation only]', findings)
            self.assertIn('[failure/spawn_or_load; last build reference=KLS-D-current1234; correlation only]', findings)


if __name__ == '__main__':
    unittest.main()
