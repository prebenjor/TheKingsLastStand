# wc3-forge assessment — 2026-09-30

User reference: [StephenSHorton/wc3-forge](https://github.com/StephenSHorton/wc3-forge).

## Subsequent authorized connection attempt

The owner subsequently installed/launched forge and explicitly requested connection and map work. See [WC3-FORGE-CONNECTION.md](WC3-FORGE-CONNECTION.md): Codex MCP is registered, initialization and 153-tool discovery succeed, and the latest saved map is completely archived. Loading a separate trial copy fails in forge's W3I parser on native metadata version 39. No map save/edit/conversion occurred. The sections below preserve the earlier assessment; their "not installed/connected" state is historical.

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
