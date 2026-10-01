# Build the diagnostic map

## Racial preservation-first handoff and publication

Read [the current racial report](docs/RACIAL-CONSTRUCTION-20261002.md). Use the latest saved native map and archive its SHA256/content; never regenerate authored terrain for these repairs. The supported entry point is `tools/build_map.py` with `--racial-action prepare|refresh|apply|package|audit` and `--racial-folder`. Prepare additionally requires `--editor-baseline` and `--forge-lock`; apply/audit require the selected existing authenticated Forge lock. Open the dedicated folder before apply. Package requires a **new** `--editor-output`; `--worker-page-prototype` is permitted only for a separate native acceptance map. Regular handoffs retain the false production gate until native evidence passes. Run `tools/verify_racial_handoff.py <folder> <map>` and native-format readback after packaging. Never use Forge Test Map when it would replace synchronized JASS with generated Lua.

For **every new DEVELOPMENT map**, commit relevant source/tests/documentation and compatibility patches, review credentials/caches/installed-data exclusions, then push an authorized branch. Publish an immutable prerelease in `prebenjor/TheKingsLastStand` attaching the map, SHA/preservation manifests and verification report. Keep binaries outside ordinary Git history. Add a dated immutable CHANGELOG entry per packaged handoff and update README with the latest download, build identifier, changes and outstanding checks. Never relabel an older build's tests as new gameplay evidence. If authentication is unavailable, retain the complete local bundle and report publication blocked pending sign-in. Default-branch changes require the approved PR merge path after the direct-main automatic review rejection.

## Current countryside handoff — 2026-10-01

Continue editing `build/KLS-D-68303d69bf-Castle-Countryside-Final-R4-20261001.w3m` (SHA256 `8d04cabf92ef4ddf68559a66636f80d6603645d08804c13528cc60d7bfe822d6`). This supersedes earlier countryside and forest editing handoffs. West/east countryside scenery, shop placement synchronization and portal/monster group corrections are implemented. Compilation, preservation and static route checks passed; standard World Editor selection and gameplay checks remain pending. This is a DEVELOPMENT editor copy, not an installed release. See `docs/CASTLE-COUNTRYSIDE-20261001.md` for preservation evidence and the required saved-shop import workflow. The original forest baseline is archived and untouched.

## Workshop handoffs

Use [EDITOR-WORKSHOP.md](docs/EDITOR-WORKSHOP.md) and [EDITOR-WORKSHOP-HANDOFF.md](docs/EDITOR-WORKSHOP-HANDOFF.md) for the approved editor-first workflow. `tools/editor_workshop.py baseline` archives a clean native editor save; `review` archives a later chapter save and reports semantic placement/object changes plus trigger/script differences. Both require the human's saved/closed confirmation. Review reports import nothing automatically: port deliberate gameplay changes to generators/modules, and keep six-layer art capture separate. Archive originals under `backups/editor-workshop/` outside the installed test folder. Establish a fresh native baseline after each regenerated work copy before intentional edits.

Read docs/TECHNICAL-ARCHITECTURE.md for the build contract. From the repository root, run:

    python -B tools/extract_game_api.py
    python -B tools/build_map.py
    python -B -m unittest discover -s tests -v

Add --install-test-map to install the package-proven build in the one designated Warcraft III test folder. The older --install-diagnostic option remains an alias. A clean checkout must use the supported locally installed Warcraft III editor/API. Do not copy machine-local reference tables into Git.

The current map and verified evidence are recorded in `README.md`, `dist/build-manifest.json`, and `docs/ROADMAP-AND-ACCEPTANCE.md`. The earlier Test Map pass remains attached only to `KLS-D-fd638ddcf5`.

## Preserve World Editor terrain and dressing

The authoritative World Editor art input is `source/authored-map/editor-layer.zip`. It stores only terrain (`war3map.w3e`), pathing (`war3map.wpm`), doodads/destructables (`war3map.doo`), shadows, minimap markers, and the map preview. Runtime code, object data, players and generated metadata still come from this repository's source.

After dressing the current build in World Editor, save a copy and close the map. Capture its supported art layers by passing the saved map path:

    python -B tools/capture_authored_map.py --map "C:\path\to\saved-current-build.w3m"

The capture checks that the map carries the build ID in the current `dist/build-manifest.json`, validates the 192 Ã— 192 terrain/pathing extent, stores source-map and per-layer checksums, and rejects unexpected archive members. If `--map` is omitted, the exact checksum-verified current package seeds or refreshes the authored layer. The next build hashes and includes this bundle; without a bundle, the existing procedural terrain generation remains the fallback. Inspect the result in World Editor after building because edited terrain, pathing and placed doodads must still agree for navigation.

Do not capture an older build under the current ID. If the chosen saved map no longer identifies the current build, rebuild/install the current package first, then reopen that exact map and reapply or carry forward the desired art before capturing.

## Visible buildings while editing

After capturing the saved, closed current map, run `python -X utf8 -B tools/build_map.py --prepare-editor` to create the current `build/<build-id>-Development-Terrain.w3m`. This copy includes disposable references for shops, towns, quest sites, castle, spring, bases and the hero hub. The installed Development package remains the normal gameplay map. See [EDITOR-LAYOUT.md](docs/EDITOR-LAYOUT.md) for shared placement sources, Neutral Extra cleanup and the limits of moving reference units. Preserve/close old work copies before replacing or archiving them.

## Targeted northern editor handoff

The supported build entry point can update just the northern wave and settlement runtime in a preserved DE editing copy, leaving unrelated functions, native initialization and every placement/object/art member unchanged. It updates both compiled JASS and the native editor custom-script header, compiles with the installed API, checks content preservation, refuses existing output paths and emits a SHA-tagged report. It does not install a gameplay package or change the current build manifest.

    python -B tools/build_map.py --northern-editor-map <extracted-Forge-folder> --editor-baseline <original-raw-MPQ.w3m> --editor-output <new-editing-copy.w3m>

The baseline supplies archive metadata; the saved Forge folder supplies all current war3map members. Preserve that folder before edits and close the map before refreshing it. HM3W-wrapped Forge exports are not supported by the native MPQ reader; use the saved extracted folder and original raw MPQ baseline. Runtime function changes are explicitly limited by tools/editor_layout.py and all other content members are checked byte-for-byte.

For the approved forest pass, append `--forest-camps` to the targeted editor handoff. Apply live geometry with `--dress-forest <dedicated-folder> --forge-lock <selected-pid.lock>`. See docs/FOREST-COVES-20261001.md for preservation, marker ownership, native pathing limitations and exact checks.
