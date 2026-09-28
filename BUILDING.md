# Build the diagnostic map

Read docs/TECHNICAL-ARCHITECTURE.md for the build contract. From the repository root, run:

    python -B tools/extract_game_api.py
    python -B tools/build_map.py
    python -B -m unittest discover -s tests -v

Add --install-diagnostic to install a package-proven build locally. A clean checkout must use the supported locally installed Warcraft III editor/API. Do not copy machine-local reference tables into Git.

The current checked-in development artifact is dist/DIAGNOSTIC-KLS-D-fd638ddcf5.w3m. It passes static package/API checks, but not World Editor round-trip, current-build engine startup, full gameplay, multiplayer, or endurance. See docs/ROADMAP-AND-ACCEPTANCE.md.
