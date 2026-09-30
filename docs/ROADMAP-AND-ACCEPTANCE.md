# Roadmap and acceptance gates

## Status of repository snapshot

Build: **KLS-D-8048eea39b**

Artifact: `dist/KLS-D-8048eea39b-Development.w3m`
SHA-256: `6759047254a8fd3bef830e32af7af4f8804fe732237a25b87957004138664247`
Installed: `C:\Users\asphy\Documents\Warcraft III\Maps\TheKingsLastStand\KLS-D-8048eea39b-Development.w3m` (matching SHA-256).

Map SHA-256: **6759047254a8fd3bef830e32af7af4f8804fe732237a25b87957004138664247**
Label: **DEVELOPMENT BUILD — NOT A VERIFIED RELEASE**

| Stage | Evidence in this snapshot | Status |
|---|---|---|
| Source package / generated objects / archive inventory and readback | Current package inventory, component hashes and archive readback checked | Passed |
| JASS compile against installed editor API | Installed-version declarations and provenance validated by the current package command | Passed |
| Full automated regressions | 181 tests passed, including actual handler decisions through native-boundary stubs; see AUDIT-COMPLETION.md | Passed |
| Test-folder installation | Build `KLS-D-8048eea39b` is installed as the sole project map; package and installed hashes match | Passed |
| Runtime diagnostic retention | Source retains the latest 32 ERROR/FATAL/WARN entries separately from routine events and displays the most recent eight | Current-build `-diag` capture pending |
| World Editor Test Map | User reports success for the earlier build KLS-D-fd638ddcf5; retain as a pass for that build | Passed (user-reported, earlier build) |
| Editor save/reopen | Current package is installed; save/reopen in World Editor has not been checked | Pending |
| Current-build Test Map / Custom Game startup | Open the installed map and confirm visible ID `KLS-D-8048eea39b`. The earlier Test Map pass remains recorded separately | Pending (not failed) |
| 192×192 map, towns, bounds, pathing and navigation | Terrain, pathing, W3I bounds, camera bounds and minimap were generated together; compact base lumber stands now sit 500/700 units south of each hall; visual routes, tree clearance and playability need live inspection | Pending in game |
| Four-race selection and construction | Per-player race, matching workers/menus, Temple of the Damned parent and explicit Temple icon, race-specific role descriptions, and expected/actual mine status in `-diag` are source checked. All four starting reserves are normalized to 1,000,000; Undead/Elf use owned Haunted/Entangled mines and Human/Orc use neutral Gold Mines. Night Elf Barracks and upgrade structure use Ancient of War (`eaom`) and Hunter's Hall (`edob`) | Pending in mixed-race game |
| Eight new heroes, signatures, companies and support units | Source/catalog links and installed parent IDs are present; Keeper/Faelor retain signatures and learn tree-free Briar Host. Company chapter/weapon/armor/support research and all 50 authored powers are in the package. Visuals, recruits and ownership need live checks | Pending in game |
| Level 1–50 progression and talents | Selection sets hero level 1 / 0 XP. No automatic stat growth. Every level gives one shared skill point for a manual native spell rank or one of three owner-local, unranked +3 attribute buttons; safe rank 4–5 data remains manual. Fifth-level talents are a separate track. Verify in game | Pending in game |
| Difficulty selection and spawn scaling | Owner-local Easy/Normal/Hard/Very Hard votes during selection; highest vote wins, ties/defaults Normal. Regular unit count/HP/damage and boss/reinforcement scaling use the selected synchronized multipliers; HUD and `-diag` report it | Pending in game |
| Unanimous early wave start | Toggleable owner-local Ready vote during wave-free preparation. Starts only on unanimity; otherwise 50/180-second countdown remains. No pause and vote resets between waves | Pending in multiplayer game |
| Endless waves after wave 40 | Ten repeating roster rows and rotating bosses scale from the live wave number | Pending in game |
| Shops, rarity colors, drops, gear and Foundry recipes | Catalog has 80 general, 20 racial and three general crafted items plus four racial recipe outputs. Normal enemies have 0% world gear; Elite have 1% Common/Uncommon only; Boss has 0% random world gear. Personal boss milestones award Uncommon/Rare/Epic/Legendary at waves 10/20/30/40+. Independent potion rolls remain 4%/8%/18%. `tools/power_curve.py` reports item effects/components; the generated audit has no rarity outliers or tier-order warnings. Shop, equipment and craft interactions remain live checks | Pending in game |
| Boss/story item reliability | Both reward sources use one null-safe owner queue; failed `CreateItem` retries every five seconds, while full inventory falls back to a visible owner-bound item at base | Current-build failure injection and pickup pending in game |
| Optional Crownlands recovery story | Four chapters use a separate enemy group, vulnerable participating escort with retry, and shared permanent town unlocks. Handler/catalog tests pass; native paths/rewards need live play | Pending in game |
| Sacred Aura `AHas` / `AHpa` descriptions and values | Generated rank 1–5 effect values and current/next-rank description paths; visible rank 4/5 text still needs Warcraft verification | Pending in game |
| Shop windows, backpack/equipment, purchases, crafting and full inventory | Pack now uses generic installed `ebac` with 30-slot storage and nine equipment slots; gear object flags and inventory/catalog relationships are source checked. Shop transfer detaches the backpack item before creating its normal-inventory copy; recipe scrolls are guarded against duplicate craft starts. Multiplayer open/close independence, native click, transfer, equipment, duplication prevention and buyback still need live checks | Pending / known report |
| Kill-reward feedback | Source pays full gold bounty to the player owning the killing unit; King Aldric awards 25% to each active player. Toast readability and owner attribution need the current-build game check | Pending in game |
| Shared XP | Native XP is disabled; runtime gives the full per-unit XP award to each active hero within 1,200 range. Includes race and life-state cases | Pending in game |
| Restoring Spring cadence | Source restores 1% max health and mana per second silently within 450 range | Pending in game |
| Wave-break timers | Normal break 50s; pre-boss break 180s | Pending in game |
| All construction, gathering, king and tower systems | Source inspection only; 181 automated tests passed; native behavior still needs live checks | Pending live |
| Original waves 1-40 and endless crossover loop | Wave roster generator data is unchanged; spawn/scaling paths were edited. Check the original and endless cycles, 41-50 campaign units, bounded loop, 50/60/70 boss rotation, rewards, and king-death behavior in game. 181 automated tests passed; native behavior still needs live checks | Pending live |
| Real 2/3/4-player synchronization | No network session evidence | Pending |
| Full Crownlands plus endless two- and four-player endurance | No current-build normal-speed match evidence | Pending |

Passing syntax or simulated tests never clears an in-game gate.

## Ordered work plan

### Gate 1 — package and startup

1. Verify current manifest, component inventory, object record structure, valid archive name lookups, source hashes, and installed API provenance.
2. Current package `dist/KLS-D-8048eea39b-Development.w3m` has SHA-256 `6759047254a8fd3bef830e32af7af4f8804fe732237a25b87957004138664247` and is installed with a matching hash. Open this build and verify its visible ID before save/reopen or startup checks.
3. Run Test Map on the current build-ID-named map in the existing test workflow. The previous Test Map already succeeded per the user; do not record it as failed or repeat it solely to satisfy stale wording.
4. Confirm build ID, 25-hero selection court, correct active-player plots/resources and race-matched workers, King Aldric and castle, selection/preparation countdown, and no automatic victory. Record which build ID was tested.
5. Launch the same build via Warcraft III → Single Player → Custom Game. Confirm the same visible ID and objects. Capture screenshot and full -diag output if anything is missing.

### Gate 2 — native items/backpack and player systems

1. Open the Forsaken Kingdom backpack UI; confirm 30 storage and nine equipment slots.
2. Buy one weapon and chest item, equip, inspect actual stat/proc changes, unequip, and confirm no loss across death/revival.
3. Repeat all 30 storage slots, all nine equipment slots, full six-item inventory, ownership, repeated transfers, consumables, simultaneous purchases, recipe failure/success, and pending boss reward behavior.
4. Confirm every shop shows icon stock, rarity colors and accurate hover stats/effects; test tomes, the four racial recipes and the twenty new items.
5. Test building requirements, footprint rejection/refund, worker mine/tree access, towers, Altar of Kings, castle healing/upgrades, talent controls, and restorative pool.
6. Verify first prep 45s, ordinary break 50s, boss break 180s, HUD updates, and every signature ability. Confirm supported spells retain all authored ranks and that ranks 4–5 apply the tagged +10%-per-rank effect increase without changing cost, cooldown, range, duration, or targeting. Confirm unsupported spells stay at the native cap. Check the five rarity colors in item/shop names and item tooltips.

### Gate 3 — waves, network, and endurance

1. Preserve and run the original 40 wave compositions, then play through waves 40-50 and at least one later boss. Check bosses 50, 60, and 70, their telegraphs, summons, exactly-once bounties/XP/counts, and one personal Legendary item per active player. Wave 40 must continue; King Aldric's death must end the run and show the highest wave.
2. Test actual 2-player and 4-player sessions with UI actions, ownership, shared vision/no shared control, purchases, rewards and synchronized outcomes. Check three-player initialization/scaling.
3. Complete normal-speed runs through at least one endless boss with 2 and 4 players. Record stalls, resource pressure, pathing, frame rate, and all balance edits by build ID.

## Current exact human-run check

Current DEVELOPMENT build **KLS-D-8048eea39b**: `dist/KLS-D-8048eea39b-Development.w3m`; SHA-256: `6759047254a8fd3bef830e32af7af4f8804fe732237a25b87957004138664247`. Installed bytes match the package. Full audit details: [AUDIT-COMPLETION.md](AUDIT-COMPLETION.md). Engine/multiplayer/endurance checks remain pending.

Next human-run check: launch the installed **KLS-D-8048eea39b** in a two-player Custom Game, confirm both displayed build IDs, choose different-race heroes, and open both backpacks simultaneously. Confirm each retains its own contents and Player 2 can vote Ready and spend a stat/talent point without affecting or pausing Player 1. Record screenshots/full `-diag` output on this exact build, then use the broader [acceptance register](ROADMAP-AND-ACCEPTANCE.md).
