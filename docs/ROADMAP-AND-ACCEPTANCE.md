# Roadmap and acceptance gates

## Status of repository snapshot

Build: **KLS-D-5604bb3f70**

Map SHA-256: **8e80a85f14a289f61bbf23260423754f1d3fee0441fee0882dfddefa479576bd**
Label: **DEVELOPMENT BUILD — NOT A VERIFIED RELEASE**

| Stage | Evidence in this snapshot | Status |
|---|---|---|
| Source package / generated objects / archive inventory and readback | Current package inventory, component hashes and archive readback checked | Passed statically |
| JASS compile against installed editor API | Installed-version declarations and provenance validated | Passed statically |
| Focused automated regressions | 136 source-level tests, including once-only counting of unit, scenery, item, recipe and retry ERROR events, separate ERROR/FATAL/WARN retention, distinct Hall models, racial Foundry pattern stock/returns, native-shop limits, race-town relic stock, spawn diagnostics, inventory delivery, hero progression, story and documentation alignment | Passed for this source snapshot |
| Runtime diagnostic retention | `-diag` keeps the latest 32 ERROR/FATAL/WARN entries separately from routine events and displays the most recent eight. Recipe output creation/delivery and queued boss/story reward creation/retry failures join unit, scenery and random-drop errors in that buffer; the `-diag` header counts every ERROR once across categories with item, owner and location context | Source regression passed; live capture pending |
| World Editor Test Map | User reports success for the earlier build KLS-D-fd638ddcf5; retain as a pass for that build | Passed (user-reported, earlier build) |
| Editor save/reopen | `KLS-D-5604bb3f70` is installed in the designated test folder with a SHA-256 matching its manifest; editor save/reopen remains unverified | Pending |
| Current-build Test Map / Custom Game startup | `KLS-D-5604bb3f70` is installed as the sole project map in the designated test folder. The earlier Test Map pass remains recorded separately | Pending (not failed) |
| 192×192 map, towns, bounds, pathing and navigation | Terrain, pathing, W3I bounds, camera bounds and minimap were generated together; visual routes and playability need live inspection | Pending in game |
| Four-race selection and construction | Per-player race, matching workers/menus, Temple of the Damned parent, race-specific role descriptions, pre-owned Undead Haunted and Night Elf Entangled starting mines at 1,000,000 gold, native Acolyte haunting orders, and expected/actual mine status in `-diag` are source/regression checked | Pending in mixed-race game |
| Eight new heroes, signatures, companies and support units | Object/catalog links and installed parent IDs are regression checked; Keeper/Faelor suppress the tree-targeted native ability in favor of usable signatures; visuals, recruits and ownership need live checks | Pending in game |
| Level 1–50 progression and talents | Per-level +3 Strength/Agility/Intelligence choices are native hero `+` skills; the stat-choice dialog was removed. Fifth-level specialty talent dialog and stat changes need live checks | Pending in game |
| Endless waves after wave 40 | Ten repeating roster rows and rotating bosses scale from the live wave number | Pending in game |
| Shops, rarity colors, drops, gear and Foundry recipes | Generic rarity shops, four matching town relic shops, three-pattern Master Forge stock, one owner-only matching Legendary pattern at each constructed racial Foundry, all-vendor 12-slot cap, four racial recipes, explicit 3%/10%/50% Normal/Elite/Boss gear chances, independent 4%/8%/18% potion rolls and personal drop ownership are package/regression checked; Hall appearance, shop interface, equipment and craft interactions need live checks | Pending in game |
| Boss/story item reliability | Both reward sources use one null-safe owner queue; failed `CreateItem` retries every five seconds, while full inventory falls back to a visible owner-bound item at base | Source regression passed; injected failure and pickup remain pending in game |
| Optional Crownlands recovery story | Four chapters use a separate story enemy group and do not modify wave count/timer in source checks; all objective/reward paths need live play | Pending in game |
| Sacred Aura `AHas` / `AHpa` descriptions and values | Generated ranks 1–5 and learned/learn-menu strings are regression checked; verify visible rank 4/5 text in Warcraft | Pending in game |
| Shop windows, backpack/equipment, purchases, crafting and full inventory | Pack modifies installed `ebua`; gear object flags and inventory/catalog relationships are source checked. Native click, transfer, equipment and buyback still need live checks | Pending / known report |
| Kill-reward feedback | Source pays full gold bounty to the player owning the killing unit; King Aldric awards 25% to each active player. Toast readability and owner attribution need the current-build game check | Pending in game |
| Shared XP | Native XP is disabled; runtime gives the full per-unit XP award to each active hero within 1,200 range. Includes race and life-state cases | Pending in game |
| Restoring Spring cadence | Source restores 1% max health and mana per second silently within 450 range | Pending in game |
| Wave-break timers | Normal break 50s; pre-boss break 180s | Pending in game |
| All construction, gathering, king and tower systems | Source/regression evidence only | Pending live |
| Original waves 1-40 and endless crossover loop | Generator preserves the original roster fingerprint; 41-50 campaign units, bounded cycle, 50/60/70 boss rotation, rewards, and king-death outcome are regression checked | Pending live |
| Real 2/3/4-player synchronization | No network session evidence | Pending |
| Full Crownlands plus endless two- and four-player endurance | No current-build normal-speed match evidence | Pending |

Passing syntax or simulated tests never clears an in-game gate.

## Ordered work plan

### Gate 1 — package and startup

1. Verify current manifest, component inventory, object record structure, valid archive name lookups, source hashes, and installed API provenance.
2. Current package `dist/KLS-D-5604bb3f70-Development.w3m` is installed in the designated test folder and matches the package manifest. Open that exact map for editor save/reopen and current-build startup checks.
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
The user reported completing a test but did not include the displayed build ID or observations. That report is unassigned and does not verify `KLS-D-5604bb3f70`.


1. The user's earlier Test Map success remains recorded for `KLS-D-fd638ddcf5`; it is not a failed step.
2. Current package `KLS-D-5604bb3f70` is at `dist/KLS-D-5604bb3f70-Development.w3m`, SHA-256 `8e80a85f14a289f61bbf23260423754f1d3fee0441fee0882dfddefa479576bd`. It is installed at `Documents/Warcraft III/Maps/TheKingsLastStand/KLS-D-5604bb3f70-Development.w3m`; the installed hash matches and the folder contains one project map. The earlier Test Map pass remains attributed to `KLS-D-fd638ddcf5` and is not a failed step.
3. Current-build startup is pending. Open the new exact map in World Editor and run Test Map, then launch that same installed map through Warcraft III → Single Player → Custom Game. Confirm its visible build ID and that the match starts without errors or premature victory.
4. Exercise mixed-race selection, racial build menus and worker jobs; inspect the Undead Temple icon/queues, + stat buttons, fifth-level talents, towns and road navigation; test item stock, equipment, drops, recipes, story rewards, Sacred Aura rank 4/5 tooltips, and both race-specific mine orders.
5. Continue with the existing kill gold/XP, castle, shop/backpack, spring and 50/180-second break checks, then verify automatic wave 40 continuation, the wave 49 convergence, Lady Vashj at wave 50, and one later rotating boss. Confirm the optional Crownlands story stays outside wave accounting. Finish with real multiplayer and endless endurance acceptance.

For the first item-system check after startup, click the Forsaken Field Pack and confirm its native UI opens. Then buy common boots, move them between backpack storage and the normal inventory, and sell them to a shop. Separately, stand at the spring with missing HP/mana and confirm both bars tick upward each second without a burst effect or message.

## Release criterion

Do not rename a diagnostic to a release or remove the development label until every required editor/startup, gameplay, multiplayer, and endurance check is passed and tied to the exact release build ID and SHA-256. Any unresolved shop/backpack behavior blocks declaring the equipment experience complete.
