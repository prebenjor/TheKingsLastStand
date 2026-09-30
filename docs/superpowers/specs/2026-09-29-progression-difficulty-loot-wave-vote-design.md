# Progression, Difficulty, Loot, and Wave Readiness

**Date:** 2026-09-29  
**Status:** User-approved; implemented in Development build `KLS-D-4e6ae863df`; live acceptance pending
**Project:** The King's Last Stand

## Purpose

Make hero advancement a meaningful per-level choice, let the group set a match-wide challenge level, reserve high-rarity equipment for earned milestones, rebalance outlier equipment and recipes, equalize the starting mine reserve across races, model the hero/item power curve from generated catalogs, and let the group start the next wave early only when everyone is ready.

This specification follows the user's current direction. It supersedes earlier notes that gave heroes automatic `+3` primary and `+1` secondary stats per level. Existing personal gold, nearby full XP awards, 50-second ordinary breaks, 180-second pre-boss breaks, the wave roster, and King Aldric's loss condition remain intact.

## Implementation approach

Three implementation shapes were considered:

1. **Patch each behavior in place.** This changes fewer lines but leaves difficulty, readiness votes, and loot rules spread across unrelated conditions, making future tuning and synchronization harder to follow.
2. **Keep the existing module boundaries and add shared match-rule state.** The game runtime owns synchronized difficulty and skip votes; hero progression owns level choices; the catalog owns loot eligibility and item power. UI stays owner-local and sends choices through synchronized events. This keeps each concern near its existing source while giving match-wide rules one source of truth. **Recommended.**
3. **Create a new general match-services subsystem.** This could centralize more rules, but would be broader than the current needs and add indirection before other match systems require it.

The approved design uses approach 2 and avoids a new general service layer.

## Hero level and stat choices

- Every selected hero starts at level 1 with 0 XP. The hero-selection path explicitly sets both and logs the resulting level and XP before the first wave.
- Remove free automatic `+3` primary and `+1` secondary attribute growth on every level. Native hero attribute growth remains zeroed to prevent hidden growth.
- Each hero level still grants its normal skill point. The player may spend that point on a spell rank using Warcraft's hero skill controls or on one of three owner-local stat choices: `+3 STR`, `+3 AGI`, or `+3 INT`.
- A stat choice consumes exactly one normal skill point and adds exactly three points to the selected attribute. It is unranked and repeatable; the buttons are choices, not abilities with levels.
- Spell ranks remain selectable rather than being granted automatically by hero level. Existing ability data remains capped at its safe generated rank, including the supported rank 4–5 effect scaling, and native requirements govern which rank can be learned. The +3 choices and spell ranks therefore compete for the same normal skill points.
- Keep the separate fifth-level talent track and its secondary effects; it does not replace the per-level skill-point choice.

## Match difficulty

- Add Easy, Normal, Hard, and Very Hard choices to the initial hero-selection phase. The choice is shown as owner-local controls and never pauses the game.
- Each active player has one vote, defaults to Normal, and may change their choice until the hero-selection phase closes. The result locks when selection finishes or its existing timer expires. Highest vote count wins; a tie or no votes resolves to Normal.
- Apply a deterministic preset to all normal enemies, elites, boss units, and boss reinforcements, after the current wave and player-count scaling. Preserve roster composition, bounty rules, and break durations.

| Difficulty | Enemy health | Enemy base damage | Regular wave count |
|---|---:|---:|---:|
| Easy | 0.75× | 0.80× | 0.90× |
| Normal | 1.00× | 1.00× | 1.00× |
| Hard | 1.30× | 1.20× | 1.10× |
| Very Hard | 1.60× | 1.40× | 1.20× |

Round wave counts to the nearest integer and keep at least one regular enemy. Boss count remains one; boss health and damage use the selected difficulty multiplier. Show the locked difficulty in the HUD and diagnostics.

## Equipment drops and item power

- Ordinary enemies no longer roll equipment. Their separate healing/mana consumable drop behavior remains unchanged.
- Elite enemies have a 1% equipment-drop chance, but may drop only Common or Uncommon items. They cannot drop Rare, Epic, or Legendary items.
- Bosses remain the primary source of high-rarity gear. Every boss grants one personal reward to each active player; remove the additional random boss world-gear roll to avoid an uncontrolled second equipment award. Scale the guaranteed reward by boss milestone: Uncommon at wave 10, Rare at wave 20, Epic at wave 30, and Legendary from wave 40 onward, including later ten-wave bosses.
- Preserve player ownership for boss rewards. Keep player-specific kill gold, XP rules, potion drops, shop stock, and recipes unchanged except where an item is rebalanced.
- Rebalance the general 80-item catalog, twenty racial relics, and recipe outputs together. Race flavor comes from names, presentation, and distinct effects; it does not grant a separate higher stat budget. The current outliers are Epic Grudgebreaker (`I23P`, +168 damage, +28 Strength), Legendary Worldrend Standard (`I23T`, +220 damage, +99 Strength), and their comparison point, general Legendary Kingswrath (`I11C`, +66 damage and a 35% cleave effect).
- Create one shared item-power report from catalog-derived base stats and effect fields. Compare entries by equipment slot and rarity. Keep same-tier peers within a 25% band around their tier-and-slot median for each comparable component, require each tier's median to exceed the preceding tier's median, and flag any lower-tier item component more than 25% above the next tier's median for the same slot. Report damage, attributes, armor, health, mana, and speed separately; show named effect magnitude, trigger, duration, and cooldown as separate values instead of hiding them in an opaque aggregate. Recipe outputs use the same budget as shop items.
- Preserve the rarity palette and item names. Adjust item stats, effect strength, cooldowns, or recipe inputs/fees only as needed to meet the power budget; do not compensate for an overpowered effect solely by raising its purchase price.

## Stat power-curve report

- Add `tools/power_curve.py`, using `hero_catalog.py`, `equipment_catalog.py`, and the installed `UnitBalance.slk` data from the existing API extraction flow. Custom heroes use their declared parent hero's base stats.
- Generate `docs/STAT-POWER-CURVE.md` with one row per level from 1 through 50 for all 25 heroes. Show base stats, zero automatic growth, normal skill points remaining, and three stat-allocation scenarios: all points spent on spells, all stat choices spent on the hero's primary stat, and all stat choices spent on each of STR, AGI, and INT. Include each of the three fifth-level talent paths as distinct projections.
- Support command-line overrides for a level, per-attribute stat-point allocations, talent selections, purchased tomes, and equipped item rawcodes. Reject allocations that spend more normal skill points than the selected level provides, and reject invalid item codes or equipment slot collisions.
- Show catalog item power components grouped by rarity and equipment slot, including named effect magnitude, trigger, duration, and cooldown. Flag stat-component outliers against the shared tier budgets. The report is deterministic, repeatable, and does not modify runtime balance data.
- If installed reference data is missing or does not match the installed-game provenance, fail with the existing API extraction command rather than silently using guessed hero base stats.

## Race economy parity

- Every player's starting mine reserve is set to 1,000,000 gold, using the high reserve requested earlier for the map. Undead and Night Elf keep their race-specific Haunted and Entangled mine units; Human and Orc keep their neutral Gold Mine unit. Only the reserve is normalized.
- Each player retains five starting workers and personal gold income. The mine change does not alter worker identity, worker count, bounty ownership, or race build menus.

## Unanimous next-wave vote

- Add a non-pausing owner-local `Ready` control during each wave-free preparation interval, including the initial preparation before wave 1.
- A player's vote is scoped to the current next wave and may be toggled off before unanimity. The next wave starts immediately only when every active player has voted ready.
- If the existing preparation timer reaches zero first, start the wave normally. Keep ordinary preparation at 50 seconds and pre-boss preparation at 180 seconds.
- Hide or disable the control while a wave is active. Clear votes when a new wave starts and when the next preparation interval begins. A solo player's vote starts the next wave immediately.
- All vote data and wave transitions are synchronized. Local frames may display or accept input, but `GetLocalPlayer()` must never determine the vote result or spawn timing.

## Architecture and data flow

- Keep synchronized match state in `source/game.j`: selected difficulty, per-player difficulty votes, per-player current-wave ready votes, and wave transitions. Put reusable difficulty/tally/scaling helpers in `source/match_rules.j` before the modules that consume them; put the Ready callback after `KLS_Spawn` to satisfy JASS declaration order.
- Keep hero-level handling in `source/combat.j` and `source/heroes.j`. Remove automatic-stat state and use the existing local stat controls and Warcraft skill points.
- Keep item eligibility, rarity limits, rarity reward selection, item stats/effects/recipes, and effect-power components in `tools/equipment_catalog.py` and `tools/wave_rosters.py`, generated into the existing runtime. Keep mine reserve setup in `source/heroes.j`.
- Add `tools/power_curve.py` as a read-only report generator and `docs/STAT-POWER-CURVE.md` as its generated, checked-in output.
- Reuse the current frame/sync-event conventions for owner-local controls. Do not introduce globally pausing dialogs for difficulty or skip voting.
- Update the approved gameplay/design docs, agent guidance, progress ledger, and per-build changelog with the final implementation and exact evidence.

## Failure and fallback behavior

- No difficulty votes or a tied result selects Normal.
- No unanimous skip vote falls back to the existing countdown.
- Invalid, repeated, late, or out-of-range sync messages do not change state. Each player may only change their own vote while the relevant phase is open.
- Equipment reward creation follows the existing safe personal-reward flow. Failed reward delivery is logged and follows that flow's retry/queue behavior; it must not create a second copy.
- Existing enemy spawn failure handling remains unchanged.

## Acceptance criteria

1. Each selectable hero is logged at level 1 and 0 XP when chosen. No automatic attribute growth occurs; spending one skill point on a stat grants exactly the chosen +3, and spending it on a spell does not also grant stats.
2. Every hero's spell ranks can be learned with normal skill points through their supported rank cap; ranks 4–5 retain the generated 10% safe effect scaling and do not auto-rank on hero-level gain.
3. Each difficulty can be selected before the first wave, ties/defaults resolve to Normal, HUD/diagnostics report the result, and the four enemy scaling profiles apply to regular waves, bosses, and boss reinforcements without changing compositions.
4. Standard enemies cannot produce equipment; elites cannot produce Rare-or-higher items; boss awards are personal and follow the milestone rarity schedule. Consumable drops and player-specific gold remain independent.
5. All four races start with the same 1,000,000 reserve; Undead/Elf mine models remain race-specific, Human/Orc remain neutral mines, and worker counts/income ownership remain personal.
6. The power-curve report deterministically covers 25 heroes × 50 levels, chosen stat points, all three fifth-level talent paths, optional tomes/loadout, and all general/racial/crafted item tiers. Catalog outliers include Grudgebreaker and Worldrend Standard until their budgets are corrected.
7. No racial item makes the general same-slot catalog obsolete; recipe effects are included in the item-power report and each item's budget.
8. A Ready vote is local to its owner, does not pause the match, visibly reflects progress, starts only on unanimity, resets between waves, and leaves the existing 50/180-second fallback intact.
9. Package, source/object serialization, installed-editor JASS syntax, installed-map hash, power-curve report, and changelog/progress records are current. Gameplay, multiplayer, and balance acceptance still require human testing in Warcraft III and must not be claimed from static checks.

## Verification boundaries

Do not run or add automated tests unless the user asks. Build/package integrity checks and the installed editor's JASS syntax check are allowed. A successful Test Map already recorded for `KLS-D-fd638ddcf5` remains a pass for that build only; it does not clear gameplay or multiplayer checks for a new build. Keep the current build labeled Development and install only through the repository's existing current-build workflow.
