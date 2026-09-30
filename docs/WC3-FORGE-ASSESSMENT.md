# wc3-forge assessment — 2026-09-30

User reference: [StephenSHorton/wc3-forge](https://github.com/StephenSHorton/wc3-forge).

## Could we use it?

**Yes, as a candidate authoring tool. Exact map compatibility is unverified.** It is a separate map editor, not a control interface for the already-open Blizzard World Editor.

The project's [README](https://github.com/StephenSHorton/wc3-forge/blob/main/README.md) describes an alpha Windows editor with a built-in MCP server. The same session and undo history support manual and agent changes. Its tools cover terrain, placed units/doodads, object definitions, regions, triggers and saving packaged MPQ maps. It supports native JASS editing without mandatory Lua conversion. Those capabilities are a close match for our manual-placement/source-integration workflow. The listed [Windows releases](https://github.com/StephenSHorton/wc3-forge/releases) include v1.0.7 at the time of this review, with recent Reforged water/skin fixes.

No wc3-forge tools are currently callable in this session. It has not been installed, launched, connected or used to inspect/save this map. A standard MCP connection would be the intended agent control path; suitability for this client still needs setup and verification.

## Where it would help

- Inspect and manipulate exact placement coordinates/facing and creation numbers through tools.
- Let the human and agent work on the same scene with a common undo history.
- Read and review object/rank data without fragile UI navigation.
- Make terrain/doodad authoring easier to capture and reconcile with source catalogs.

It would not automatically update this project's runtime spawning catalogs. A moved editor reference still needs source integration, and deleted Redtusk/gate references must be removed from the runtime explicitly. Keep the existing supported `tools/build_map.py` entry point and archived baseline workflow.

## Bounded evaluation before adoption

1. Wait for the human to save and close the current World Editor map. Archive the complete revision first, preserving cliffs, village deletions and troll units.
2. Use one temporary trial copy under the archive/workshop area. Keep the installed/current map outside the trial.
3. Establish exact tool version and connect its MCP server to the intended wc3-forge session. Read map status before any mutation.
4. Open/read the trial copy. Confirm 192×192 terrain, W3I version 39 bounds, DE unit 13.11, native v3 objects, Reforged models/icons/skins, quest sites, units, and JASS/WCT/WTG trigger data are interpreted.
5. Save once with no deliberate changes. Compare every member and flag dropped/unknown data using the workshop review tools. Native skin files/imports and trigger formats need particular attention; unchanged visual appearance is not enough.
6. On the trial copy, move/rotate one reference and adjust one small terrain/doodad area. Exercise undo, then save/reopen and inspect the semantic changes.
7. Reopen that saved trial in Blizzard World Editor and perform a targeted Test Map/Custom Game check. Preserve existing package checks and keep exact-build acceptance pending until run.
8. Adopt it for authoring only if the round-trip is acceptable; source generators remain authoritative for gameplay. Document any unsupported native fields before using it for broader changes.

This is an evaluation proposal, not installation authorization or a completed compatibility result. No project map was modified during this assessment.

## Result — 2026-09-30 (branch `wc3-forge`)

wc3-forge v1.0.7 was installed on the user's PC and the work copy `KLS-D-68303d69bf-Forge.w3m` was opened via File → Open Map File. It failed before loading anything:

    open failed: parse war3map.w3i: w3i: tech count 12800 exceeds 291 bytes remaining (min 8 bytes/element) at offset 309: unexpected EOF

Cause: our `war3map.w3i` is format version 39 (World Editor 2.0, game 2.0.3.24268), inherited unchanged from the Blizzard DE starter in `source/template/war3map.w3i`. wc3-forge's parser (`internal/formats/w3i/w3i.go`, identical on `main` at 2026-09-05) only knows layouts up to version 33 and reads v39 with the v33 shape, so it misaligns after the loading-screen fields. This is an upstream wc3-forge limitation, not a defect in our build. Any map saved by the current World Editor will hit it.

The map was not modified. The MCP lockfile (`~/.wc3-forge/mcp/<pid>.lock`) showed the editor's MCP listener running; the Claude desktop app had not yet registered the `wc3-forge` local server at the time of the test.
