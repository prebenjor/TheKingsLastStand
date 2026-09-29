# Build the diagnostic map

Read docs/TECHNICAL-ARCHITECTURE.md for the build contract. From the repository root, run:

    python -B tools/extract_game_api.py
    python -B tools/build_map.py
    python -B -m unittest discover -s tests -v

Add --install-test-map to install the package-proven build in the one designated Warcraft III test folder. The older --install-diagnostic option remains an alias. A clean checkout must use the supported locally installed Warcraft III editor/API. Do not copy machine-local reference tables into Git.

The current packaged development artifact is `dist/KLS-D-1739daf903-Development.w3m` (SHA-256 `807f84919dd59097d31157fd8aabfe8de1c11661b32951a4df028114a06d1940`). Package readback and installed-API JASS syntax passed; all 142 source regressions passed. It is installed as the sole project map in the designated test folder, and the installed hash matches the package. World Editor loaded this exact file, but save/reopen, Test Map, Custom Game, gameplay, multiplayer and endurance checks remain pending. The earlier Test Map pass remains attached only to `KLS-D-fd638ddcf5`. See docs/ROADMAP-AND-ACCEPTANCE.md.
