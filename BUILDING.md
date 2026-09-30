# Build the diagnostic map

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

The capture checks that the map carries the build ID in the current `dist/build-manifest.json`, validates the 192 × 192 terrain/pathing extent, stores source-map and per-layer checksums, and rejects unexpected archive members. If `--map` is omitted, the exact checksum-verified current package seeds or refreshes the authored layer. The next build hashes and includes this bundle; without a bundle, the existing procedural terrain generation remains the fallback. Inspect the result in World Editor after building because edited terrain, pathing and placed doodads must still agree for navigation.

Do not capture an older build under the current ID. If the chosen saved map no longer identifies the current build, rebuild/install the current package first, then reopen that exact map and reapply or carry forward the desired art before capturing.

## Visible buildings while editing

After capturing the saved, closed current map, run `python -X utf8 -B tools/build_map.py --prepare-editor` to create the current `build/<build-id>-Development-Terrain.w3m`. This copy includes disposable references for shops, towns, quest sites, castle, spring, bases and the hero hub. The installed Development package remains the normal gameplay map. See [EDITOR-LAYOUT.md](docs/EDITOR-LAYOUT.md) for shared placement sources, Neutral Extra cleanup and the limits of moving reference units. Preserve/close old work copies before replacing or archiving them.
