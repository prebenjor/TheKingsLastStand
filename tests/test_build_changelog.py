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

    def test_current_package_acceptance_references_match_the_manifest(self):
        manifest_path = ROOT / 'dist' / 'build-manifest.json'
        if not manifest_path.exists():
            self.skipTest('Build the map before checking current-package documentation.')
        manifest = json.loads(manifest_path.read_text())
        roadmap = (ROOT / 'docs' / 'ROADMAP-AND-ACCEPTANCE.md').read_text()
        current_check = roadmap.split('## Current exact human-run check', 1)[1]
        technical_architecture = (ROOT / 'docs' / 'TECHNICAL-ARCHITECTURE.md').read_text()
        progress_ledger = (ROOT / 'docs' / 'PROGRESS-LEDGER.md').read_text()
        current_progress = progress_ledger.split('## Previous package-proven build', 1)[0]
        current_package_docs = {
            'README': (ROOT / 'README.md').read_text(),
            'player guide': (ROOT / 'docs' / 'PLAYER-GUIDE.md').read_text(),
            'roadmap current check': current_check,
            'technical architecture': technical_architecture,
            'progress ledger current section': current_progress,
        }
        for document, content in current_package_docs.items():
            with self.subTest(document=document):
                self.assertIn(manifest['build_id'], content)
                self.assertIn(manifest['output_path'], content)
                self.assertIn(manifest['sha256'], content)
        item_catalog = (ROOT / 'docs' / 'ITEM-CATALOG.md').read_text()
        self.assertIn(manifest['build_id'], item_catalog)


if __name__ == '__main__':
    unittest.main()
