# Native forge compatibility — 1 October 2026

## Working result

The approved compatibility workaround is implemented in a separate checkout:
`C:/Users/asphy/Documents/Warcraft3Maps/wc3-forge-compat`.
Upstream base: `4ce58432ec47d073822222929bdb8603c257c9fb`.

Patched executable:
`C:/Users/asphy/Documents/Warcraft3Maps/wc3-forge-compat/build/bin/wc3-forge-compatible.exe`.
Codex's `wc3-forge` MCP entry now uses this executable with `--mcp`.
Configuration backup: `C:/Users/asphy/.codex/config.toml.before-forge-compatible-20261001.bak`.
The original installed forge executable is unchanged. Its older instance can still
be open; select the patched instance using `sessions_list` and `session_select`
after restarting clients. PID 60644 was selected during this run; PIDs change.

Editing copy, successfully opened through MCP:
`build/KLS-D-68303d69bf-Development-Forge.w3m`.
The user's Terrain working copy remains unchanged. The editing copy initially
has exactly the same archive bytes as the preserved human save.

## Implemented changes

- W3I version 39: loading-screen source, fog extension, water extension and
  per-player HUD skin. Unknown/float words retain their original bit patterns.
- Unit placement version 13: group identity, roll/pitch and opaque native light
  records. Version-13 scale edits use natural scale values.
- Doodad placement version 13: group identity, extra opaque word, roll/pitch
  and native light records. Original placement versions remain unchanged.
- MPQ saving retains source listfile names alongside the raw file blocks.
  Previously raw blocks survived but some native member names disappeared
  from the regenerated index, making archive inspection incomplete.

Readers and writers were compared with current HiveWE format readers. No format
downgrade or removal of native map sections was performed. New native fields
are preserved, but this patch does not add UI controls/rendering for tilt or lights.

## Evidence

Preserved input SHA-256:
`f9c9276256edd2531f37efa9a029e0334bb1f71dfa3ac7c297a98cff26ea55da`.
Complete immutable input:
`backups/wc3-forge/20261001-f9c9276256ed/KLS-D-68303d69bf-Development-Terrain.w3m`.

- Frontend and patched Windows executable compiled successfully.
- Native diagnostic: W3I39 (590 bytes, four players), units13 (13,378 bytes,
  102 entities), doodads13 (81,548 bytes, 1,100 doodads) each passed a
  byte-identical parse/encode comparison.
- MCP opened the final patched editor's isolated copy successfully.
- Assigning one unit and one doodad their existing coordinates exercised both
  placement writers without changing layout. Save succeeded.
- Full archive comparison: 26 members before and after, no missing/added or
  unlisted members; only `(listfile)` text changed. All other members, including
  terrain, groups, lights, skin files, native triggers and JASS, stayed identical.
- The native Trigger Editor tree loaded the existing initialization trigger,
  variables and global JASS. No trigger or object edits were made.
- Original Terrain map and immutable backup retain the input hash.

The final diagnostic save is `wc3-forge-compat/build/Final-Preservation-Check.w3m`.
Machine-local comparison: `build/forge-session/compatibility-result.json`.
These are targeted compatibility checks, not in-game, multiplayer, endurance,
visual rendering or arbitrary object/trigger editing acceptance. Current gameplay
package stays **KLS-D-68303d69bf Development**; no rebuild or installation occurred.

## Reproduce the patch

Repository artifacts: `tools/wc3-forge/native-compat.patch` and
`tools/wc3-forge/nativecheck.go`. The separate checkout contains the diagnostic
at `cmd/nativecheck/main.go`.

1. Check out the pinned upstream base in a separate forge checkout.
2. Apply `native-compat.patch` with `git apply`.
3. Copy `nativecheck.go` to `cmd/nativecheck/main.go`.
4. Build the locked frontend with `npm ci`, then `npm run build` in `frontend`.
5. Build from the checkout root with Go:
   `go build -tags desktop,production -ldflags "-H windowsgui" -o build/bin/wc3-forge-compatible.exe .`
6. Place both installed Forge runtime DLLs, CascLib.dll and zlib1.dll, beside the executable.
7. Run `go run ./cmd/nativecheck <extracted-fixture-folder>` against an isolated
   full map extraction, then repeat the MCP save and archive comparison.

A checksum-verified portable Go 1.27.1 compiler is local under `.toolchain`.
The Wails CLI build hit an upstream type-loader error with that compiler;
the explicit frontend/Go build above succeeded. Do not check in toolchains,
dependency caches, compiled executables or the user's complete map.

## Continue editing

Preserve the removed Orc village, cliff defenses, troll camp and all authored
terrain/doodads/units. Forge compatibility does not integrate those placements
into the runtime catalogs. Continue the workshop handoff separately; keep the
immutable human save and compare every intentional change before integration.

## Asset-loading correction

The first visible open had black terrain and no models because zlib1.dll was missing beside CascLib.dll. Runtime diagnostics explicitly reported failure to load CascLib.dll. Copied the installed Forge zlib1.dll into the patched bin folder; direct DLL loading then succeeded. Restarted the unchanged visible editor and reopened the same Forge copy. Live diagnostics now show CASC hits, healthy terrain/cliff/water tables with no poisoned caches, 89 rendered units and 1,084 rendered doodads (four start markers separately). Nine unit records and sixteen doodads still skip rendering; this remains an asset-resolution limitation, not a claimed complete visual pass. No map edits or saves occurred.


## Missing units and building doodads — 2026-10-01

The current executable is `C:/Users/asphy/Documents/Warcraft3Maps/wc3-forge-compat/build/bin/wc3-forge-render-compatible.exe`; the MCP registration points to it. The earlier compatible executable remains a historical build.

Renderer repairs (map content unchanged):

- Add the installed `_de.w3mod` asset mount as a fallback after existing asset mounts. This supplies house variants 3–7, Ilastar and other newer scenery without replacing already resolved Classic models.
- Read VERS >= 1400 geoset SKIN values as uint16, then convert losslessly to the viewer's byte representation; reject values outside its supported range. Read modern light static fields before animation tracks, passing the model version to the light reader. Schema reference: HiveWE `src/file_formats/mdx/mdx_reader.cpp`, `read_GEOS` and `read_LITE`.
- Resolve stock `file:sd` / `file:hd` model keys for Demon Hunter, Death Knight, gnolls and forest trolls.
- Merge an unambiguous missing doodad skin row across Blizzard's `Ycgd` / `YCgd` casing mismatch. Unit FourCC case remains significant.

The visible final session loaded all **98 non-start units + four start markers** and **1,100 doodads**, with **zero skipped units/doodads, zero failed unit/doodad models and zero empty-geoset models**. GL error was zero; frontend and Go production builds succeeded. Both working map hashes remain `f9c9276256edd2531f37efa9a029e0334bb1f71dfa3ac7c297a98cff26ea55da`; no map saves or placement edits occurred.

These are live renderer diagnostics, not a screenshot comparison: computer-use initialization remains unavailable on this host. One cliff cell still has an unresolved mesh and the viewer reports 29 cliff/texture lookup warnings (including optional variant attempts). Do not call the entire renderer warning-free or claim complete visual fidelity. Human terrain/runtime integration and gameplay acceptance are separate.

The combined reproducible `native-compat.patch` includes these repairs. Build as above, using the current executable name, and keep both runtime DLLs beside it. No game assets or executables are checked into this repository.
