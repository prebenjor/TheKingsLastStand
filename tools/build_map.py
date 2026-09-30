"""The supported entry point for building The King's Last Stand."""
import argparse
from pipeline import build
from install_diagnostic import install
from editor_layout import prepare_editor_copy

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--install-test-map', '--install-diagnostic', dest='install_test_map', action='store_true', help='Install the current development build in the local Warcraft III test folder')
    parser.add_argument('--prepare-editor', action='store_true', help='Create a terrain work copy with disposable editor layout references')
    args = parser.parse_args()
    manifest = build()
    if args.prepare_editor:
        prepare_editor_copy(manifest)
    if args.install_test_map:
        install(manifest)
