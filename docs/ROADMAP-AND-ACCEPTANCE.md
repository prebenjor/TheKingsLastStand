# Roadmap and acceptance gates

## Status of repository snapshot

Build: **KLS-D-2cd4884e7f**

Map SHA-256: **fb8a6adede04d1475c5668c44d1b77616fbff19215ec712d7150cdf64502a2cd**
Label: **DEVELOPMENT BUILD — NOT A VERIFIED RELEASE**

| Stage | Evidence in this snapshot | Status |
|---|---|---|
| Source package / generated objects / archive inventory and readback | 23 packaged members checked; current output hash recorded | Passed statically |
| JASS compile against installed editor API | Installed-version declarations and provenance validated | Passed statically |
| Focused automated regressions | 65/65 passed on this build; includes native backpack identity, exact reward toast, gear movement/sale flags, spring cadence, worker identity diagnostics, campaign records, and changelog checks | Passed |
| World Editor Test Map | User reports success for the earlier build KLS-D-fd638ddcf5; retain as a pass for that build | Passed (user-reported, earlier build) |
| Editor save/reopen | No evidence that a separate save/reopen cycle was performed | Pending |
| Current-build Test Map / Custom Game startup | KLS-D-2cd4884e7f has not yet been tested; the earlier Test Map pass remains recorded separately | Pending (not failed) |
| Shop windows, backpack/equipment, purchases, crafting and full inventory | Pack now modifies the installed `ebua` record; gear remains droppable/pawnable by object data. Native click, transfer, equipment and buyback need the current-build game check | Pending / known report |
| Kill-reward feedback | Regression confirms each active player sees the exact personal kill/boss gold payout; visual readability needs the current-build game check | Pending in game |
| Restoring Spring cadence | Regression confirms 1% max health and mana per second; healing appearance and range need the current-build game check | Pending in game |
| All construction, gathering, king and tower systems | Source/regression evidence only | Pending live |
| All forty waves, four boss mechanics and end states | Source/regression evidence only | Pending live |
| Real 2/3/4-player synchronization | No network session evidence | Pending |
| Full 40-wave two- and four-player endurance | No normal-speed match evidence | Pending |

Passing syntax or simulated tests never clears an in-game gate.

## Ordered work plan

### Gate 1 — package and startup

1. Verify current manifest, component inventory, object record structure, valid archive name lookups, source hashes, and installed API provenance.
2. Continue with the existing World Editor session and current build; preserve its open document instead of making a second round-trip copy.
3. Run Test Map on the current build-ID-named map in the existing test workflow. The previous Test Map already succeeded per the user; do not record it as failed or repeat it solely to satisfy stale wording.
4. Confirm build ID, 15-hero selection court, correct active-player plots/resources, King Aldric and castle, selection/preparation countdown, and no automatic victory. Record which build ID was tested.
5. Launch the same build via Warcraft III → Single Player → Custom Game. Confirm the same visible ID and objects. Capture screenshot and full -diag output if anything is missing.

### Gate 2 — native items/backpack and player systems

1. Open the Forsaken Kingdom backpack UI; confirm 30 storage and nine equipment slots.
2. Buy one weapon and chest item, equip, inspect actual stat/proc changes, unequip, and confirm no loss across death/revival.
3. Repeat all 30 storage slots, all nine equipment slots, full six-item inventory, ownership, repeated transfers, consumables, simultaneous purchases, recipe failure/success, and pending boss reward behavior.
4. Confirm every shop shows icon stock and accurate hover stats/effects; test tomes and 3 recipes.
5. Test building requirements, footprint rejection/refund, worker mine/tree access, towers, Altar of Kings, castle healing/upgrades, talent controls, and restorative pool.
6. Verify first prep 45s, ordinary break 90s, boss break 180s, HUD updates, spell ranks through level 100, and each signature ability.

### Gate 3 — waves, network, and endurance

1. Run all 40 wave compositions, boss actions, summon accounting, last-enemy removal, final boss victory, king defeat, same-tick deaths, departures, and next-wave scaling.
2. Test actual 2-player and 4-player sessions with UI actions, ownership, shared vision/no shared control, purchases, rewards and synchronized outcomes. Check three-player initialization/scaling.
3. Complete normal-speed 40-wave games with 2 and 4 players. Record stalls, resource pressure, pathing, frame rate, and all balance edits by build ID.

## Current exact human-run check

1. The user's earlier Test Map success remains recorded for `KLS-D-fd638ddcf5`; it is not a failed step. UI automation is unavailable in this session, so no editor input has been sent.
2. Installing `KLS-D-2cd4884e7f` remains blocked because Warcraft III PID 46920 still has an older project map open. The previous package was archived locally. After the user finishes testing and closes Warcraft III, run `python -B tools/build_map.py --install-test-map`; the installer should archive the old project map and leave one current `<build-id>-Development.w3m`.
3. Test `KLS-D-2cd4884e7f` through the established World Editor Test Map workflow. The earlier build's Test Map is a passed user-reported result; this new build remains pending until tried.
4. Confirm the visible build ID, 15 selection previews, correct player plot and resources, castle and king, countdown, and absence of victory.
5. Launch that exact map through Custom Game and report its ID and results.
6. If anything is missing, type -diag, capture full output and screenshot (including the worker race/object identity lines), then collect logs with `python -B tools/collect_test_logs.py` from the repository root.

For the first item-system check after startup, click the Forsaken Field Pack and confirm its native UI opens. Then buy common boots, move them between backpack storage and the normal inventory, and sell them to a shop. The same run should also confirm a kill reward popup and one-second visible HP/mana restoration at the spring.

## Release criterion

Do not rename a diagnostic to a release or remove the development label until every required editor/startup, gameplay, multiplayer, and endurance check is passed and tied to the exact release build ID and SHA-256. Any unresolved shop/backpack behavior blocks declaring the equipment experience complete.
