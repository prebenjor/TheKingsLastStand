# Build the diagnostic map

Read docs/TECHNICAL-ARCHITECTURE.md for the build contract. From the repository root, run:

    python -B tools/extract_game_api.py
    python -B tools/build_map.py
    python -B -m unittest discover -s tests -v

Add --install-test-map to install the package-proven build in the one designated Warcraft III test folder. The older --install-diagnostic option remains an alias. A clean checkout must use the supported locally installed Warcraft III editor/API. Do not copy machine-local reference tables into Git.

The current packaged development artifact is `dist/KLS-D-1739daf903-Development.w3m` (SHA-256 `807f84919dd59097d31157fd8aabfe8de1c11661b32951a4df028114a06d1940`). Package readback and installed-API JASS syntax passed; all 142 source regressions passed. The current map is not installed because the prior `KLS-D-7951d852c3-Development.w3m` is still open in World Editor PID 22184. Save and close that editor normally, then rerun `python -B tools/build_map.py --install-test-map`. See docs/ROADMAP-AND-ACCEPTANCE.md.
