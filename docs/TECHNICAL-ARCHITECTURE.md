# Technical architecture and reproducible build

## Runtime shape

- Warcraft III Definitive Edition / Reforged map, packaged as a W3M diagnostic artifact from the user's blank DE starter.
- JASS runtime split into explicit modules in source/: diagnostics, hero selection, backpack, shops, equipment, HUD, castle controls, combat, wave environment, signatures, personal rewards, Crownlands story, and match flow.
- tools/pipeline.py assembles those modules in a fixed order, generates native custom object files and editable trigger source, compiles the runtime against the installed Warcraft API, and writes a deterministic package manifest.
- tools/equipment_catalog.py is the source for native gear objects, rawcodes, shop stock, costs, stats, descriptions, effects, and item metadata.
- tools/hero_progression.py derives extended skill objects/rank logic from installed AbilityData/AbilityMetaData, including the installed Hjsm and Npal campaign skill sets. tools/hero_catalog.py defines eight added hero records and per-player race identity. tools/signature_spells.py defines the 25 custom AK00–AK24 abilities.
- tools/faction_catalog.py defines the four race-specific worker/building/tower menus; tools/company_catalog.py defines 25 hero-matched company/support pairs. tools/town_catalog.py is the source of truth for the four settlement and story-site placements; source/crownlands.j owns settlement construction and match-scoped story progression.
- tools/wave_rosters.py defines forty story and ten crossover roster rows, role bounties, explicit Normal/Elite loot tiers for every ordinary unit, and boss mechanic definitions. tools/equipment_catalog.py generates the matching gear/potion drop thresholds, roll handling, owner markers, and failure diagnostics.
- tools/recipes.py builds crafting transactions from the catalog. tools/objects.py builds unit/item object records. tools/terrain.py updates terrain and pathing extents. tools/gui_sources.py produces editable WTG/WCT sources from the same assembled runtime.
- tools/archive_pack.py and tools/map_archive.py update/read the MPQ, its listfile, hashes, blocks and checksum/attributes and verify exact component readback.
- source/war3map.j and build/ files are derived outputs. Edit source modules and generators instead.

## Supported commands

Run from the repository root:

    python -B tools/extract_game_api.py
    python -B tools/build_map.py
    python -B tools/build_map.py --install-test-map
    python -B -m unittest discover -s tests -v

The extractor reads the local installed Warcraft III and writes tools/reference/installed plus provenance.json. It records the installed .build.info fingerprint and hashes of each extracted reference, including UnitBalance.slk, UnitUI.slk, UnitAbilities.slk, and UnitWeapons.slk for hero stats, ability lists, portraits, weapons, and models. The build refuses stale references after an installation update. Do not commit those extracted tables or declarations; each developer extracts from their own installed game.

The extractor also requires a locally prepared `tools/vendor/casclib-build/Release/CascLib.dll` and a CASC-compatible file list at `tools/vendor/casclib-src/listfile/listfile.txt`. The source snapshot does not include those generated/local prerequisites. The extractor currently assumes the game at `C:\\Program Files (x86)\\Warcraft III`; parameterizing its path and documenting a clean-machine CascLib/listfile bootstrap remain setup work.

The local builder currently assumes Warcraft III at C:\Program Files (x86)\Warcraft III and uses that installation's World Editor/JASS helper. If a developer's install differs, parameterize the path with an explicit tested change rather than silently pointing at an old editor.

## Pinned baseline and metadata

- Build input is backups/Blank-DE.w3m; its expected SHA-256 is 3b68da520c3d14084c7eec4fffae5cfc76315c58990a1415a4f897c0b781e8d9.
- The validated source/template/war3map.w3i metadata is version 39 with pinned SHA-256 a6275d4b92e8c8f1267536d0e175eb1ece7dbb031f1447a2a0295c0b86a461cc.
- Reject any baseline or metadata that differs. Preserve all untouched Definitive Edition settings.
- The map is expanded to 192 × 192 terrain cells. Four starts/plots are centered at (-6000,-500), (-3300,-500), (3300,-500), (6000,-500). Playable bounds, terrain, pathing, camera bounds, minimap, towns and visual routes must stay in sync. tools/town_catalog.py is the settlement layout source of truth.
- Generated W3I has four human defender slots in one allied force, shared vision, no shared control, and one hostile undead owner.
- The output title and first startup message carry the immutable development build ID. Initialization uses one generated runtime for compiled JASS and editable trigger sources, sets initial globals explicitly, and guards against a second initialization.
- No default melee initializer or automatic victory rule may be present.

## Object/API ID policy

Warcraft rawcodes, campaign backpack functions, item/hero/ability metadata and icon paths are version-sensitive. Generate and validate against tables extracted from the installed editor version. Never treat a successful parse against another version as proof of compatibility. A stale/missing rawcode or icon should fail clearly and be recorded as unresolved.

The Forsaken Kingdom backpack APIs are expected to be discovered from the current installed declarations and object tables, not guessed from a public/editor version. Keep 30 storage slots, nine equipment slots, and native six-slot hero inventory with one permanent backpack item in the design.

## Current custom object registry

This registry records project-owned object rawcodes that agents are likely to confuse. Letter case is significant.

| Rawcode | Current object |
|---|---|
| h000 | Player Altar of Kings building, based on the native Altar object |
| H000 | Custom Human Priest hero |
| H001 | Custom Ranger hero object, retained for project data |
| h001 | Watchtower |
| h002 | Bombard Tower |
| h003 | Sanctuary Tower |
| h004 | Arcane Sanctum |
| hS00 | Neutral Kingdom Merchant template reused for tiered vendors |
| hS01 | Hidden temporary frost-effect helper |
| hS02 | Sage's Archive |
| hC01 | King Aldric's Castle |
| AK00–AK24 | Twenty-five custom hero signature spells in hero-selector order |
| Havl, Htor, Okrg, Omor, Esly, Efal, Uvyr, Utha | Eight custom selectable heroes based on installed race-native hero models |
| kH00–kH03, kF00–kF03, kY00–kY03 | Four race-themed Hall, Foundry and Siege Yard roles |
| kQ00–kQ03 | Crownlands story characters for the four settlements |
| I23C–I23V | Twenty race-themed item records, five per race |
| RCP4–RCP7 | Four race-themed Legendary Foundry recipes |
| I010–I013 | Four boss relic items; see ITEMS-AND-EQUIPMENT.md |
| I100–I127 and I128–I12A | Generated equipment families and crafted legendary variants; see ITEM-CATALOG.md |
| KSTR, KAGI, KINT | +3 Strength, Agility, Intelligence hero skill choices using the native Attribute Bonus ability |
| KS05/10/20, KA05/10/20, KI05/10/20 | Strength, Agility, Intelligence attribute tomes |

The native-shop stock map uses `KLS_Shops[0..9]` for the five rarity tiers' Arms & Armor and Apparel & Relics vendors, `[10]` for the Field Apothecary, `[11]` for Sage's Archive, and `[12]` for the Master Forge's three general recipe patterns. Four `KLS_TownShop` instances stock each race's four non-Legendary relics plus health and mana potions. A constructed racial Foundry stocks one owner-only Legendary recipe using `KLS_FactionFoundryRecipeId[race]`; its selling vendor is saved in the recipe timer's `KLS_GearData` key 32 so successful and failed crafts restock the correct building. A destroyed vendor falls back to the Master Forge. Racial Legendary relics remain eligible for existing enemy-drop rules. Keep each vendor at twelve or fewer stock entries to fit Warcraft's native shop command card.

The same case-sensitive collision caution applies to unit heroes, building IDs, abilities, and items. Let generator serialization, installed data validation, and archive object-record checks determine whether an ID is safe; do not infer safety from a missing visual icon.

## Packaging and outputs

- python -B tools/build_map.py is the only supported build entry point.
- The repository keeps one current map artifact in `dist/`, named `<build-id>-Development.w3m`. Build manifests, JASS, and temporary package stages live under `build/`; no second persistent map copy is written there.
- `--install-test-map` copies that exact package-proven map into `Documents/Warcraft III/Maps/TheKingsLastStand/`, the user's designated live test folder. That folder contains one current project map so the Custom Game entry is unambiguous.
- When a new build replaces a prior development map, the previous `dist/` map is archived under the ignored local `backups/development-builds/`; previous installed test maps are archived under `backups/installed-diagnostics/`. Git history preserves prior checked-in `dist/` snapshots for remote recovery.
- World Editor authored map art lives in the checked-in `source/authored-map/editor-layer.zip` sidecar. `tools/authored_map.py` validates its build provenance, checksums, World Editor terrain/pathing dimensions, doodad format, and the six-member allowlist. `tools/capture_authored_map.py --map <saved-map.w3m>` captures only `war3map.w3e`, `war3map.wpm`, `war3map.doo`, `war3map.shd`, `war3map.mmp`, and `war3mapMap.blp`; W3I identity, JASS, triggers and custom object data are always generated from source. The source-map hash and each member hash are written into the ZIP manifest and propagated to `dist/build-manifest.json`. The sidecar bytes participate in the immutable build ID. If absent, the current procedural terrain/pathing/shadow fallback is used.
- A capture is accepted only when the saved map's W3I scenario name identifies the current build ID. Capturing is art-layer-only; any terrain/pathing edits must be checked in World Editor for road, tree, town, boss and worker-route access after the next build.
- Current package: `dist/KLS-D-8a93630281-Development.w3m`, SHA-256 `bd158009334e911f835d4b9c82d9f0068d89cf0bac9e6c218bd80f9bd97a56ec`. It includes the validated World Editor art sidecar captured from `KLS-D-b0fccf974c`; the six bundled terrain/pathing/doodad/shadow/minimap/preview members pass checksum, dimension and archive-readback checks. Installation was attempted after the map was closed, but `WinError 32` prevented removal of the old `KLS-D-b0fccf974c` map. The prior file remains in the test folder and a verified copy is retained under `backups/installed-diagnostics/20260929T111716941276Z-KLS-D-8a93630281/`; retry only after Warcraft III exits. Existing role, race, item, wave and diagnostic behavior remains source- and regression-checked. Editor round-trip, current-build Test Map, Custom Game, gameplay, multiplayer and endurance remain pending.
- Manifest includes build ID, package SHA-256, source hashes, API provenance, member inventory and check states.
- Root CHANGELOG.md carries one entry for every packaged build, including the build ID, package SHA-256, changes and exact verification/pending status. Update it with each build and verify the latest manifest against its entry.
- The current source regression suite has 147 tests; all **147/147 passed** for `KLS-D-8a93630281`. Package readback and installed-editor API syntax checks passed. The older user-reported Test Map pass remains assigned to `KLS-D-fd638ddcf5`; current-build save/reopen, Test Map, Custom Game, live gameplay, multiplayer and endurance checks remain pending.

## Personal item rewards

`source/rewards.j` owns the per-player item reward queue shared by chapter-boss relics and Crownlands story rewards. It checks `CreateItem` before calling item natives, assigns both native owner and the project's item-owner marker, places successfully created items in the hero inventory or visibly at the owner's base when inventory delivery fails, and retries failed creation every five seconds while the match clock runs. A queue entry is cleared only after a physical item exists. Regression tests check the source routing and queue state; item-handle failures and pickup still need engine testing.
- Kill XP uses a custom path: map `GrantNormalXP` and `GrantHeroXP` are zeroed, native `HeroExpRange` is disabled, and `KLS_AwardKillXP` applies one full award to every active player hero within 1,200 world units. Keep the default Warcraft unit-level award table/formula aligned with `KLS_UnitKillXP`. This avoids native alliance splitting. Dead-hero and campaign-hero behavior remain pending game verification.
- Personal kill gold is separate from XP: owner gets full role bounty, while a King Aldric kill gives 25% to every active defender. Ordinary breaks are 50 seconds; boss breaks are 180 seconds. The Restoring Spring uses silent one-percent-per-second health/mana recovery.

## Network determinism and ownership

All gameplay state belongs in synchronized JASS triggers: wave counter, enemy group, resource transactions, item ownership, hero selection, building placement, boss effects, rewards, revival, and terminal result. Player-local branches may display UI or move that user's camera; they may not selectively create gameplay objects or change match state.

For every multi-step transaction (castle contribution, item purchase/equip, recipe, boss reward), validate owner/active state, payment, eligibility, inventory capacity, and terminal state before finalizing. Refund and restore on failure. Recheck race/class assumptions for mixed allied defenders.

## Spawn/error diagnostics

source/diagnostics.j keeps a bounded recent diagnostic log and reports build ID, attempted unit/scenery creation, and failures. `-diag` displays runtime counters, recent events, and each active player's runtime race plus the actual first worker's object/unit name. This distinguishes an Acolyte spawn from a selection/portrait mismatch without guessing from the unit's appearance. `tools/collect_test_logs.py` snapshots Warcraft/World Editor logs with manifest linkage and lists observed map build IDs separately from the target build. Its JSON groups warnings/errors/failures and labels load/spawn events; findings include the nearest preceding build ID as a timing correlation only. Map-open references may be menu scans and never prove gameplay or causality. A current build is considered played only after a person confirms its visible in-game ID.

Never attribute a model-creation failure in a stale menu/catalogue scan to the current build. Record exact log lines and package identity, then reproduce on the current map. Report every failed CreateUnit/destructable creation with object rawcode, phase, coordinates if available, owner and failure count.

## Git exclusions and clean-clone setup

Do not check in machine-local API tables, Blizzard script/API declarations, game/editor installation paths beyond what local configuration requires, generated build/test logs, Python caches, compiled CASC/Lua helper binaries, or local map archives. Keep the user's blank starter and the one current development map with the source package. A clean clone needs an installed supported Warcraft III editor and a fresh API extraction before building.
