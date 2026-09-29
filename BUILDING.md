# Build the diagnostic map

Read docs/TECHNICAL-ARCHITECTURE.md for the build contract. From the repository root, run:

    python -B tools/extract_game_api.py
    python -B tools/build_map.py
    python -B -m unittest discover -s tests -v

Add --install-test-map to install the package-proven build in the one designated Warcraft III test folder. The older --install-diagnostic option remains an alias. A clean checkout must use the supported locally installed Warcraft III editor/API. Do not copy machine-local reference tables into Git.

The current development artifact is `dist/KLS-D-6d3db36ecf-Development.w3m` (SHA-256 `4612c5a61bd95ee06ce46dec9bf67c2f01f413eca5771029c015de41b455a478`), installed as the sole project map in the designated test folder. Package readback, installed-API JASS syntax, and 133 source regressions pass; this exact build still needs World Editor save/reopen, Test Map, Custom Game, gameplay, multiplayer, and endurance checks. See docs/ROADMAP-AND-ACCEPTANCE.md.
