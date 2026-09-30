# Editor layout revision — 2026-09-30

## Explicit user decisions

- The user removed the **entire Orc village, Redtusk Hold**, in World Editor.
- The user replaced **gates with cliffs**.
- The user placed a **troll camp**.
- The user's current hand-authored terrain, doodads and units are the visual direction for subsequent work. Preserve their composition and use observed examples when extending it. Do not restore the repeated grass islands or automatically reconstruct removed scenery.

These supersede the original four-settlement/open-gate layout. Four playable races and four personal bases remain. The remaining planned settlements are Crownshire, Moonbark Glade and Wraithfall. The troll camp is an authored encounter landmark; it is not automatically a replacement Orc town or a mandatory story objective.

## Evidence and limits

The changes above are **user-reported edits in the currently open editor**. They are not yet extracted, archived or integrated into the gameplay package. We have no fresh save-and-close confirmation for this revision. Do not capture/rebuild/replace that open map.

Live Computer Use observation was attempted, reset and retried. Both attempts failed before app enumeration with `failed to write kernel assets: The system cannot find the path specified. (os error 3)`. No current editor screenshot was obtained. Exact cliff openings, troll type/ownership, scenery style, placement identities and coordinates remain unobserved; ask for screenshots or retry the supported helper when available. Do not invent a visual inspection.

## Revised story specification

Keep the existing four-stage optional recovery arc, shared match progress, personal contributor rewards, active-wave availability and separate story-enemy accounting.

1. **Reclaim Northwatch:** the request comes from a surviving allied settlement/frontier contact, no longer Redtusk Hold. Relocate the Northwatch Vanguard rather than respawning the deleted village. Choose its exact host/position from the saved layout. The four-threat encounter and restored watchposts must use reachable locations in the new cliff landscape.
2. **Escort the supplies:** retain Crownshire's supply caravan. Reconcile its destination and route with the authored roads and cliffs; keep participation, vulnerability and retry rules.
3. **Restore the surviving quarters:** retain the Moonbark contribution objective. Activate refuges at the three remaining settlements, not at an invisible/deleted Orc settlement. The original restoration prices, quiet regeneration and personal rewards remain.
4. **Break the Wraithfall ritual:** retain the northern ritual objective, but move guards and its contact as needed to match reachable authored ground. Existing completion perks remain; garrison placement must use extant sites, not dereference a removed town slot.

The troll camp's allegiance, respawn behavior, rewards and story role are **undecided**. Preserve the user's placed units. During integration, identify intended gameplay units and add explicit spawning/ownership rules so art-only capture does not lose them; do not put independent camp units into wave accounting by default.

## Equipment and racial services

All Orc heroes, workers, personal structures, companies, doctrines and five themed items remain. Removing Redtusk's shop must not make its four Common-through-Epic relics or Legendary recipe ingredients unobtainable. Plan to distribute those four relics to matching-rarity vendors in the existing kingdom market, with a native command-card capacity check. The Orc Foundry retains its Legendary pattern. This is a specified future stock change, not a current package claim.

## Pending source integration after save/close

- Review `tools/town_catalog.py`: it currently emits all eight Redtusk references and a four-entry town array. Remove the village's actual runtime structures and references while preserving stable race indices. Town presence must be separate from playable race identity.
- Review `source/crownlands.j`: `KLS_StoryExpectedSite` currently chooses site 1 for Northwatch; unlock/regeneration/garrison loops assume four sites. Relocate the stage-1 contact and guard all missing-site consumers. Preserve Orc company research unlocks independently of town presence.
- Review `source/game.j` → `KLS_BuildLandscape`: it still creates `LTg1` gate runs and `BTsk` gateway pieces around Y=5200. Remove/replace those spawns after capturing the authored cliff layout, so old gates do not appear over the user's cliffs.
- Port troll camp gameplay units from the complete saved map into a dedicated placement/encounter catalog. Archive all native unit data; six-layer art capture alone excludes those units.
- Preserve moved shops, heroes, structures, trees, terrain, heights and facing. Resolve deleted references explicitly rather than silently recreating them.
- Validate invasion, caravan, worker and boss routes through the cliff passages; review camera bounds/minimap. Never require a decorative gate object for progress.
- Record a native comparison baseline if one was saved before these edits. If none exists, preserve the complete revision and compare conservatively against generated references plus native format evidence; do not call an already-edited save a clean Chapter 0 baseline.

Current package remains **KLS-D-68303d69bf** until a saved/closed handoff is reviewed and source changes are built. The workshop's finite Chapters 0–7 still apply with a three-village Chapter 3 and troll-camp inspection.
