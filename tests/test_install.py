"""Diagnostic installation must not overwrite a map Warcraft may have open."""
import hashlib
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'tools'))
import install_diagnostic
from install_diagnostic import install


class DiagnosticInstall(unittest.TestCase):
    def test_install_uses_build_specific_filename_and_is_idempotent(self):
        data = b'diagnostic map bytes'
        manifest_path = ROOT / 'build/diagnostic-manifest.json'
        manifest_before = manifest_path.read_bytes() if manifest_path.exists() else None
        manifest = {
            'build_id': 'KLS-D-test123456',
            'output_path': '',
            'sha256': hashlib.sha256(data).hexdigest(),
        }
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            source = root / 'build.w3m'
            maps = root / 'maps'
            source.write_bytes(data)
            manifest['output_path'] = str(source)

            installed = install(manifest, maps_root=maps)

            self.assertEqual(installed.name, 'KLS-D-test123456-Development.w3m')
            self.assertEqual(installed.read_bytes(), data)
            self.assertEqual(manifest['installed_test_map_path'], str(installed))
            self.assertEqual(install(manifest, maps_root=maps), installed)
        if manifest_before is None:
            self.assertFalse(manifest_path.exists())
        else:
            self.assertEqual(manifest_path.read_bytes(), manifest_before)

    def test_install_archives_old_diagnostic_copies_out_of_custom_game_folder(self):
        current_bytes = b'current diagnostic map'
        old_maps = {
            'DIAGNOSTIC-TheKingsLastStand.w3m': b'legacy diagnostic map',
            'DIAGNOSTIC-KLS-D-old1234567890.w3m': b'older versioned diagnostic map',
            'KLS-D-old9876543210-Development.w3m': b'older named development map',
        }

        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            project = root / 'project'
            maps = root / 'Warcraft III' / 'Maps' / 'TheKingsLastStand'
            maps.mkdir(parents=True)
            source = root / 'build.w3m'
            source.write_bytes(current_bytes)
            for name, data in old_maps.items():
                (maps / name).write_bytes(data)
            unrelated_map = maps / 'MyOtherMap.w3x'
            unrelated_map.write_bytes(b'unrelated map')
            unrelated_w3m = maps / 'MyOtherMap.w3m'
            unrelated_w3m.write_bytes(b'unrelated W3M')

            manifest = {
                'build_id': 'KLS-D-new1234567890',
                'output_path': str(source),
                'sha256': hashlib.sha256(current_bytes).hexdigest(),
            }
            with patch.object(install_diagnostic, 'ROOT', project):
                installed = install(manifest, maps_root=maps)

            self.assertEqual(installed.read_bytes(), current_bytes)
            self.assertEqual(
                {path.name for path in maps.glob('*.w3m') if install_diagnostic._is_project_development_map(path.name)},
                {'KLS-D-new1234567890-Development.w3m'},
            )
            self.assertEqual(unrelated_map.read_bytes(), b'unrelated map')
            self.assertEqual(unrelated_w3m.read_bytes(), b'unrelated W3M')
            archived = project / 'backups' / 'installed-diagnostics'
            self.assertEqual(
                {path.name: path.read_bytes() for path in archived.rglob('*.w3m')},
                old_maps,
            )

    def test_locked_old_map_does_not_leave_a_new_test_map_half_installed(self):
        data = b'new map'
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            project = root / 'project'
            maps = root / 'Warcraft III' / 'Maps' / 'TheKingsLastStand'
            maps.mkdir(parents=True)
            source = root / 'build.w3m'
            source.write_bytes(data)
            old = maps / 'DIAGNOSTIC-KLS-D-lockedold.w3m'
            old.write_bytes(b'old map')
            manifest = {
                'build_id': 'KLS-D-locktest',
                'output_path': str(source),
                'sha256': hashlib.sha256(data).hexdigest(),
            }
            with patch.object(install_diagnostic, 'ROOT', project), patch.object(
                install_diagnostic.shutil, 'move', side_effect=PermissionError('map is open')
            ):
                with self.assertRaisesRegex(ValueError, '[Cc]lose Warcraft III'):
                    install(manifest, maps_root=maps)
            self.assertEqual({p.name for p in maps.glob('*.w3m')}, {old.name})
            self.assertEqual(old.read_bytes(), b'old map')
