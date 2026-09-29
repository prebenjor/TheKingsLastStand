# Build the diagnostic map

Read docs/TECHNICAL-ARCHITECTURE.md for the build contract. From the repository root, run:

    python -B tools/extract_game_api.py
    python -B tools/build_map.py
    python -B -m unittest discover -s tests -v

Add --install-test-map to install the package-proven build in the one designated Warcraft III test folder. The older --install-diagnostic option remains an alias. A clean checkout must use the supported locally installed Warcraft III editor/API. Do not copy machine-local reference tables into Git.

The current development artifact is `dist/KLS-D-f873a5b24f-Development.w3m` (SHA-256 `30fd0594806fd7e2cf9294b6750bb6ecc6e3855d9261852e01ab03fbe51c6d6e`), installed as the sole project map in the designated test folder. Package readback, installed-API JASS syntax, and 130 source regressions pass; this exact build still needs World Editor save/reopen, Test Map, Custom Game, gameplay, multiplayer, and endurance checks. See docs/ROADMAP-AND-ACCEPTANCE.md.
