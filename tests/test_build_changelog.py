"""Every current immutable map build must have its own changelog entry."""
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class BuildChangelog(unittest.TestCase):
    def test_current_manifest_build_id_has_a_changelog_section(self):
        manifest_path = ROOT / 'dist' / 'build-manifest.json'
        if not manifest_path.exists():
            self.skipTest('Build the map before checking its per-build changelog.')
        manifest = json.loads(manifest_path.read_text())
        changelog = (ROOT / 'CHANGELOG.md').read_text()
        self.assertIn('## ' + manifest['build_id'] + ' - ', changelog)
        self.assertIn(manifest['sha256'], changelog)


if __name__ == '__main__':
    unittest.main()
