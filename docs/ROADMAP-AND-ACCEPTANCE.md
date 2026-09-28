# Roadmap and acceptance gates

## Status of repository snapshot

Build: **KLS-D-1a040d638c**

Map SHA-256: **eaee0e501b3e7ced381bda7c93c530d79499faad94f2bb80304a9aeb1340e362**
Label: **DEVELOPMENT BUILD — NOT A VERIFIED RELEASE**

| Stage | Evidence in this snapshot | Status |
|---|---|---|
| Source package / generated objects / archive inventory and readback | Current build inventory, component hashes and package-to-install equality checked | Passed statically |
| JASS compile against installed editor API | Installed-version declarations and provenance validated | Passed statically |
| Focused automated regressions | 88 source-level tests, including four-race settlements, 25 heroes, company catalogs, story progression/multi-player escort credit, item catalogs/recipes, hero progression and both Sacred Aura tooltip variants | Passed for this source snapshot |
| World Editor Test Map | User reports success for the earlier build KLS-D-fd638ddcf5; retain as a pass for that build | Passed (user-reported, earlier build) |
| Editor save/reopen | World Editor is open and responsive on the exact current map; no save/close/reopen cycle has been run | Pending |
| Current-build Test Map / Custom Game startup | `KLS-D-1a040d638c` installed; no current-build launch evidence yet. The earlier Test Map pass remains recorded separately | Pending (not failed) |
| 192×192 map, towns, bounds, pathing and navigation | Terrain, pathing, W3I bounds, camera bounds and minimap were generated together; visual routes and playability need live inspection | Pending in game |
| Four-race selection and construction | Per-player worker, hall, altar, build menu, towers, Hall of Banners, Foundry, Siege Yard and faction catalog are source/regression checked | Pending in mixed-race game |
| Eight new heroes, signatures, companies and support units | Object/catalog links and installed parent IDs are regression checked; visuals, ability behavior, company recruit and ownership need live checks | Pending in game |
| Level 1–50 progression and talents | +3 attribute choice each level; separate talent choice every fifth level. Dialog rendering, multi-level queues and actual secondary stats need live checks | Pending in game |
| Shops, rarity colors, drops, gear and Foundry recipes | Twenty catalog items, five rarity tiers, shop stock, drops and four racial recipes are package/regression checked; shop interface, equipment and craft interactions need live checks | Pending in game |
| Optional Crownlands recovery story | Four chapters use a separate story enemy group and do not modify wave count/timer in source checks; all objective/reward paths need live play | Pending in game |
| Sacred Aura `AHas` / `AHpa` descriptions and values | Generated ranks 1–5 and learned/learn-menu strings are regression checked; verify visible rank 4/5 text in Warcraft | Pending in game |
| Shop windows, backpack/equipment, purchases, crafting and full inventory | Pack modifies installed `ebua`; gear object flags and inventory/catalog relationships are source checked. Native click, transfer, equipment and buyback still need live checks | Pending / known report |
| Kill-reward feedback | Source pays full gold bounty to the player owning the killing unit; King Aldric awards 25% to each active player. Toast readability and owner attribution need the current-build game check | Pending in game |
| Shared XP | Native XP is disabled; runtime gives the full per-unit XP award to each active hero within 1,200 range. Includes race and life-state cases | Pending in game |
| Restoring Spring cadence | Source restores 1% max health and mana per second silently within 450 range | Pending in game |
| Wave-break timers | Normal break 50s; pre-boss break 180s | Pending in game |
| All construction, gathering, king and tower systems | Source/regression evidence only | Pending live |
| All forty waves, four boss mechanics and end states | Source/regression evidence only | Pending live |
| Real 2/3/4-player synchronization | No network session evidence | Pending |
| Full 40-wave two- and four-player endurance | No normal-speed match evidence | Pending |

Passing syntax or simulated tests never clears an in-game gate.

## Ordered work plan

### Gate 1 — package and startup

1. Verify current manifest, component inventory, object record structure, valid archive name lookups, source hashes, and installed API provenance.
2. The exact current build-ID-named map is open in World Editor. Save/reopen and Test Map are still pending; do not create another round-trip copy.
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

1. Run all 40 wave compositions, boss actions, summon accounting, last-enemy removal, final boss victory, king defeat, same-tick deaths, departures, and next-wave scaling.
2. Test actual 2-player and 4-player sessions with UI actions, ownership, shared vision/no shared control, purchases, rewards and synchronized outcomes. Check three-player initialization/scaling.
3. Complete normal-speed 40-wave games with 2 and 4 players. Record stalls, resource pressure, pathing, frame rate, and all balance edits by build ID.

## Current exact human-run check

1. The user's earlier Test Map success remains recorded for `KLS-D-fd638ddcf5`; it is not a failed step.
2. `KLS-D-1a040d638c` is installed as the single current project map at `C:\Users\asphy\Documents\Warcraft III\Maps\TheKingsLastStand\KLS-D-1a040d638c-Development.w3m`. SHA-256: `eaee0e501b3e7ced381bda7c93c530d79499faad94f2bb80304a9aeb1340e362`; the installed file matches the package. Previous maps were archived outside the Custom Game folder.
3. Current-build startup is pending. Open this exact map in World Editor and run Test Map, then launch the same installed map through Warcraft III → Single Player → Custom Game. Confirm its visible build ID and that the match starts without errors or premature victory.
4. Exercise a mixed-race selection, racial build menus and worker jobs; inspect new heroes/signatures, stat/talent dialogs, towns and road navigation; test item stock, equipment, drops, recipes, story rewards, and Sacred Aura rank 4/5 tooltips.
5. Continue with the existing kill gold/XP, castle, shop/backpack, spring and 50/180-second break checks, followed by real multiplayer and 40-wave endurance acceptance.

For the first item-system check after startup, click the Forsaken Field Pack and confirm its native UI opens. Then buy common boots, move them between backpack storage and the normal inventory, and sell them to a shop. Separately, stand at the spring with missing HP/mana and confirm both bars tick upward each second without a burst effect or message.

## Release criterion

Do not rename a diagnostic to a release or remove the development label until every required editor/startup, gameplay, multiplayer, and endurance check is passed and tied to the exact release build ID and SHA-256. Any unresolved shop/backpack behavior blocks declaring the equipment experience complete.
