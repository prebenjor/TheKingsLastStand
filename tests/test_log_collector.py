"""Log snapshots must not be attributed to a stale or test-only build manifest."""
import json
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


if __name__ == '__main__':
    unittest.main()
