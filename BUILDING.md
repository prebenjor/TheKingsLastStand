# Build the diagnostic map

Read docs/TECHNICAL-ARCHITECTURE.md for the build contract. From the repository root, run:

    python -B tools/extract_game_api.py
    python -B tools/build_map.py
    python -B -m unittest discover -s tests -v

Add --install-test-map to install the package-proven build in the one designated Warcraft III test folder. The older --install-diagnostic option remains an alias. A clean checkout must use the supported locally installed Warcraft III editor/API. Do not copy machine-local reference tables into Git.

The current development artifact is `dist/KLS-D-7951d852c3-Development.w3m` (SHA-256 `42922eb38fd46bd6f6071fef7df08f4329e4abd921d8773bdfc32286f9421b1c`), installed as the sole project map in the designated test folder. Package readback, installed-API JASS syntax, and 139 source regressions pass; this exact build still needs World Editor save/reopen, Test Map, Custom Game, gameplay, multiplayer, and endurance checks. See docs/ROADMAP-AND-ACCEPTANCE.md.
