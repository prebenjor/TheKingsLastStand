# Northern forest and loot coves — 1 October 2026

## Approved scope and artifact

The user approved forest exploration north, east and west of the Northern Summoning Gate: trees, rocks, cliffs, small paths and secluded monster coves. Preserve the southern invasion forecourt and all existing manual placements.

Final DEVELOPMENT editor handoff: `build/KLS-D-68303d69bf-Forest-Coves-Final-20261001.w3m`.

SHA-256: `c7d91e762808683fae708105b1d0fdda5cf21291cd4bcdc61e93b3a2db892929`.

This supersedes the northern-site editing copy for ongoing editing. It retains base identity KLS-D-68303d69bf and is not a new installed gameplay package. No dist manifest, installed map or canonical authored-layer capture was changed. The full handoff is open in Forge through MCP, with camera centered on the forest. Native editor visual inspection and gameplay are pending.

## Woodland and camps

251 Summer Tree Walls, 50 native rocks and nine isolated one-level dirt-cliff outcrops frame two winding side paths and a rear cross-connection. Four rough-dirt coves join the trails. The paths leave room for movement and combat; the southern wave formation remains outside the new terrain changes.

| Cove | Center | Monsters | Leader reward |
|---|---|---|---|
| Briarwolf Hollow | (-4800, 8200) | Giant Wolf and two Timber Wolves | One Common catalog item and healing potion |
| Mossfang Enclave | (4800, 8200) | Forest Troll Berserker and two Forest Trolls | One Common catalog item and healing potion |
| Silkweb Cove | (-6400, 10100) | Forest Spider and two Black Spiders | One Uncommon catalog item and healing potion |
| Stonejaw Den | (6400, 10100) | Ogre Mauler and two Ogre Warriors | One Uncommon catalog item and healing potion |

Leader definitions kL00–kL03 have 900/1200/1600/2200 HP and 20/26/35/45 base damage, retaining native dice, armor and skills. Guard definitions kM00–kM03 retain their respective native combat data. All have native gold bounty disabled so the source bounty is not doubled.

The 12 placed units are Neutral Extra editor markers. Startup removes them together with the established disposable references, then creates exactly 12 Neutral Aggressive monsters at the catalog positions. They use native creep guarding and 500 acquisition range. Runtime spawns are once per match under the existing initialization guard; no respawn timer or wave group is added. Moving a marker requires a corresponding catalog-coordinate update; its position does not automatically alter fallback runtime coordinates.

Camp deaths give the existing full nearby XP award and killer-owned gold equal to unit level × 20. Leaders guarantee a Common/Uncommon personal catalog reward plus a healing potion to the killing defender. Guards have a synchronized 25% chance to award a personal healing or mana potion. Rewards use the existing ownership/delivery queue, including full-inventory and item-creation-failure handling. Camps do not increment/decrement wave counts, delay wave completion, or chase King Aldric through wave reorders. Removing racial villages remains in effect.

## Source and repeatable workflow

`tools/forest_catalog.py` owns paths, geometry, scenery, camp rawcodes, rewards and startup placements. `source/crownlands.j` carries its explicit generation marker; `tools/pipeline.py` expands it in the existing module order. `source/game.j` routes camp deaths before the invasion group branch and initializes the camps once. `tools/objects.py` emits the eight matching custom unit definitions.

`tools/forge_forest.py` applies the catalog through the documented local Forge MCP JSON-RPC bridge, sequentially and with undo history. It checks the open folder, checkpoints additions, and never prints authentication. Start from a new extracted folder and keep the native baseline. Apply dressing with:

    python -B tools/build_map.py --dress-forest <dedicated-folder> --forge-lock <selected-pid.lock>

Then close/stop editing the folder and create a new immutable handoff with:

    python -B tools/build_map.py --northern-editor-map <dedicated-folder> --editor-baseline <preserved-raw-MPQ.w3m> --forest-camps --editor-output <new-output.w3m>

The handoff updates only the explicit northern/camp functions in JASS and the editor custom-script header, plus isolated cliff pathing. It does not regenerate unrelated gameplay, native main, variables, objects or art. New forest object/placement/art data comes from the saved Forge folder. Its terrain, units, objects and doodads are checked byte-for-byte against that input. Native metadata and archive CRC bookkeeping are preserved/regenerated as appropriate.

## Verification and limits

- Installed-API PJASS passed: 8,892 map-script lines; 24,719 lines including declarations. JASS and editor custom-script header were updated together.
- Final package readback and SHA passed. Forge MCP reopened this exact artifact with 151 placed units.
- All 139 original unit records and all 1,448 original doodad record bytes are preserved; exactly 12 camp markers and 301 scenery records were appended. All unrelated content members survive the targeted runtime handoff.
- 1,180 changed terrain corners are confined to Y ≥ 6,912. Existing southern terrain remains unchanged. Saved forest folder matches final packaged terrain, doodads, units and unit definitions.
- All 713 sampled trail-center pathing positions are walkable in the saved WPM. New isolated cliff outcrops are marked unwalkable/unbuildable without changing other authored pathing. This is a static check, not native collision/navigation proof.
- Five forest regressions pass, alongside the six earlier northern-site checks. Full suite: 216 tests, 214 passed, the same two earlier signature-base and Human tower-tooltip failures remain. Log: `build/forest-coves-tests.log`; preservation: `build/forest-coves-preservation.json`.

Next human-run check: open this exact file in standard World Editor and Test Map it. Walk both side trails and the rear connection, clear a leader, confirm personal loot and that the wave counter is unchanged, then check one invasion still reaches King Aldric. Current-build editor round-trip, native tree/cliff/rock collisions, neutral creep leash, live loot/ownership, multiplayer and endurance remain pending.
