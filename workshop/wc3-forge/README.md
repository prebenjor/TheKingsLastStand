# wc3-forge workspace (branch `wc3-forge`)

This branch is the sandbox for editing the map with [wc3-forge](https://github.com/StephenSHorton/wc3-forge), the alpha Warcraft III editor with an embedded MCP server that lets Claude drive the same editing session you use by hand (shared undo history).

## What is here

| File | Purpose |
|---|---|
| `KLS-D-68303d69bf-Forge.w3m` | Work copy of the current development package `KLS-D-68303d69bf` (SHA-256 `baa024fd…b0d1c3`, checked against `dist/build-manifest.json` when copied). Open and save this one in wc3-forge; `dist/` stays untouched. |
| `../../.mcp.json` | Project MCP registration so Claude Code started in this repository finds wc3-forge automatically. |

**Note:** this copy is the last *packaged* build. The September 30 World Editor revision (Orc village removed, gates replaced by cliffs, troll camp) exists only in your saved map on your PC. If you want to continue from that revision, open that saved map in wc3-forge instead, or copy it here as `KLS-D-68303d69bf-Forge-authored.w3m` first.

## One-time setup on Windows

1. Download the latest Windows installer or portable zip from the [releases page](https://github.com/StephenSHorton/wc3-forge/releases) (v1.0.7 at setup time) and install it. Default path: `C:\Program Files\wc3-forge\wc3-forge\wc3-forge.exe`. Warcraft III: Reforged must be installed; wc3-forge reads its game data (CASC) for models, icons and object data.
2. Launch wc3-forge and open `workshop\wc3-forge\KLS-D-68303d69bf-Forge.w3m` from your local checkout of this branch.
3. Connect Claude to it, with either option:
   - **Claude desktop app:** add a local MCP server named `wc3-forge` with command `C:\Program Files\wc3-forge\wc3-forge\wc3-forge.exe` and argument `--mcp`. Tools from local MCP servers are available to Claude sessions linked to that computer.
   - **Claude Code on the same PC:** run `claude` from the repository root. `.mcp.json` registers the server; approve it when prompted. Alternatively register it for every project:
     `claude mcp add wc3-forge --scope user -- "C:\Program Files\wc3-forge\wc3-forge\wc3-forge.exe" --mcp`
     Then check that `claude mcp list` shows `wc3-forge ✓ Connected`.
4. The `--mcp` process is a stdio proxy to the **running** editor (JSON-RPC over TCP on 127.0.0.1), so wc3-forge must be open with the map loaded while Claude works. Press Ctrl+` inside wc3-forge to see the Agent Console showing each tool call as it happens.

## Working rules (from `AGENTS.md` and `docs/WC3-FORGE-ASSESSMENT.md`)

- Edit only the work copy here, never `dist/` or the installed test-folder map.
- First session: open → `map_info_get` → save with **no changes** → run `tools/editor_workshop.py review` against the original to check that the round-trip does not drop or alter data (skins, imports, WCT/WTG triggers, v3 objects, 192×192 terrain). Adopt forge for wider edits only once that passes.
- Terrain, doodad and pathing art comes back through `python -B tools/capture_authored_map.py --map <saved map>` (six art layers only).
- Gameplay (units, objects, triggers, coordinates) stays owned by `source/` and `tools/` catalogs. Moves made in forge have to be ported into those sources before `python -B tools/build_map.py`; the builder regenerates `war3map.j`, so script edits made only inside forge are overwritten.
- Record build ID, hashes and checks in `docs/PROGRESS-LEDGER.md` for each change.
