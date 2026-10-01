# Editor layout revision — 2026-09-30

## Northern-site continuation — 2026-10-01

The current editing handoff removes both deleted racial settlements from runtime placement. Crownshire and Moonbark Glade remain; the four playable races and their gear/services remain independent. Northwatch and the Crown Ritual Warden are relocated kingdom contacts. Only surviving settlement halls receive restoration refuges and garrisons. Waves originate south of the invulnerable Northern Summoning Gate at (0, 7680), and moving that placed building also moves the wave origin. Startup no longer recreates the removed barrier structures over authored cliffs.

Open `build/KLS-D-68303d69bf-Northern-Spawn-Final-20261001.w3m`. This is a separate DEVELOPMENT editor handoff based on KLS-D-68303d69bf, not a new installed gameplay package. See `docs/NORTHERN-SPAWN-20261001.md` for exact preservation and verification evidence. Older sections describing pending layout integration are superseded for these specific changes only.


## Explicit user decisions

- The user removed the **entire Orc village, Redtusk Hold**, in World Editor.
- The user replaced **gates with cliffs**.
- The user placed a **troll camp**.
- The user's current hand-authored terrain, doodads and units are the visual direction for subsequent work. Preserve their composition and use observed examples when extending it. Do not restore the repeated grass islands or automatically reconstruct removed scenery.

These supersede the original four-settlement/open-gate layout. Four playable races and four personal bases remain. The remaining planned settlements are Crownshire and Moonbark Glade. The troll camp is an authored encounter landmark; it is not automatically a replacement Orc town or a mandatory story objective.

## Evidence and limits

The full saved revision is now archived under `backups/wc3-forge/20261001-f9c9276256ed/` with SHA-256 `f9c9276256edd2531f37efa9a029e0334bb1f71dfa3ac7c297a98cff26ea55da`. The original saved map and separately opened Forge copy remain unchanged. A read-only creation-ID review found moved references, reused IDs and new units; see [AUTHORED-LAYOUT-INTEGRATION-REVIEW.md](AUTHORED-LAYOUT-INTEGRATION-REVIEW.md). This revision has not yet been integrated into the gameplay package and is not a clean Chapter 0 baseline. Do not rebuild from art alone or replace the open Forge file.

Live Computer Use observation was attempted, reset and retried. Both attempts failed before app enumeration with `failed to write kernel assets: The system cannot find the path specified. (os error 3)`. No current editor screenshot was obtained. Exact cliff openings, troll type/ownership, scenery style, placement identities and coordinates remain unobserved; ask for screenshots or retry the supported helper when available. Do not invent a visual inspection.

## Revised story specification

Keep the existing four-stage optional recovery arc, shared match progress, personal contributor rewards, active-wave availability and separate story-enemy accounting.

1. **Reclaim Northwatch:** the request comes from a surviving allied settlement/frontier contact, no longer Redtusk Hold. Relocate the Northwatch Vanguard rather than respawning the deleted village. Choose its exact host/position from the saved layout. The four-threat encounter and restored watchposts must use reachable locations in the new cliff landscape.
2. **Escort the supplies:** retain Crownshire's supply caravan. Reconcile its destination and route with the authored roads and cliffs; keep participation, vulnerability and retry rules.
3. **Restore the surviving quarters:** retain the Moonbark contribution objective. Activate refuges at the two remaining settlements, not at an invisible/deleted Orc settlement. The original restoration prices, quiet regeneration and personal rewards remain.
4. **Break the Crown Ritual Service ritual:** retain the northern ritual objective, but move guards and its contact as needed to match reachable authored ground. Existing completion perks remain; garrison placement must use extant sites, not dereference a removed town slot.

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
