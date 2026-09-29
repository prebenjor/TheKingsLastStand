# Build the diagnostic map

Read docs/TECHNICAL-ARCHITECTURE.md for the build contract. From the repository root, run:

    python -B tools/extract_game_api.py
    python -B tools/build_map.py
    python -B -m unittest discover -s tests -v

Add --install-test-map to install the package-proven build in the one designated Warcraft III test folder. The older --install-diagnostic option remains an alias. A clean checkout must use the supported locally installed Warcraft III editor/API. Do not copy machine-local reference tables into Git.

The current packaged development artifact is `dist/KLS-D-660b4bdeea-Development.w3m` (SHA-256 `719de46b17be26b7165d59d3f47e6d13b98117af9b77de1270077e39e78f74eb`). Package readback and installed-API JASS syntax passed; all 141 source regressions passed. Installing the package was attempted, but Windows returned `WinError 32` for the prior installed `KLS-D-7951d852c3-Development.w3m`; Restart Manager identified a remaining `World Editor.exe` process (PID 22184) as the holder. That older file remains installed and its backup is preserved; the new build is not installed. Close that editor normally when its work is saved, then rerun `python -B tools/build_map.py --install-test-map`. Editor/gameplay checks remain pending for the new build. See docs/ROADMAP-AND-ACCEPTANCE.md.
