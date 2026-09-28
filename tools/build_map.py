"""The supported entry point for building The King's Last Stand."""
import argparse
from pipeline import build
from install_diagnostic import install

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--install-diagnostic', action='store_true', help='Copy the verified diagnostic map to the local Custom Game maps folder')
    args = parser.parse_args()
    manifest = build()
    if args.install_diagnostic:
        install(manifest)
