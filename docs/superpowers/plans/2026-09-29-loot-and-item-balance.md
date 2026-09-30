# Loot and Item-Power Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Reserve high-rarity drops for boss milestones and bring general, racial, and crafted item power into one comparable rarity/slot budget.

**Architecture:** Keep all item definitions and enemy-drop policy in `tools/equipment_catalog.py`, existing recipes in `tools/recipes.py`, and guaranteed personal boss awards in `source/game.j`. The power-curve report from the progression plan consumes catalog stats and structured effect metadata.

**Tech Stack:** Python item catalog generators, JASS runtime generation, current shop/drop/recipe object pipeline.

**Spec:** `docs/superpowers/specs/2026-09-29-progression-difficulty-loot-wave-vote-design.md`

## Global Constraints

- Ordinary enemies drop no equipment; preserve their current potion/mana consumable behavior.
- Elites have a 1% total equipment chance, limited to Common and Uncommon.
- Remove the extra random boss world-gear roll; grant one personal boss reward to each active player.
- Boss milestone rewards: Uncommon wave 10; Rare wave 20; Epic wave 30; Legendary wave 40 and later ten-wave bosses.
- Preserve rarity colors, existing general/racial item names, race-neutral equipment eligibility, and player-specific kill gold/XP.
- General gear, twenty racial relics, and all recipe outputs share one tier/slot budget; a price increase alone is not a power fix.
- Use the report interface from `tools/power_curve.py`; final build generation occurs once at integration.

## Review Focus

- Boss death must not combine a world drop with a personal drop.
- Random drop selection must not leak Epic/Legendary items into the elite pool.
- Crafted items must be included in the same report with all recipe-provided stats/effects.
- Damage procs with different triggers/cooldowns must remain visible as separate effect terms.
- Potion odds and personal ownership must remain separate from equipment eligibility.

---

### Task 1: Enforce enemy equipment eligibility and milestone rewards

**Files:**
- Modify: `tools/equipment_catalog.py`
- Modify: `source/game.j`
- Modify: `docs/WAVES-AND-BOSSES.md`
- Modify: `docs/ITEMS-AND-EQUIPMENT.md`

**Interfaces:**
- Keep generated entry point `KLS_EnemyDrop(unit enemy, boolean boss)`.
- Normal tier never returns equipment. Elite tier makes a single 1-in-100 eligibility roll and can select only item rarity 0 or 1.
- Update `KLS_BossReward` for rarity by ten-wave milestone and leave gold/reward queue ownership personal.

- [x] Change the normal threshold table to no equipment, while leaving independent consumable thresholds untouched.
- [x] Limit elite reward selection to Common/Uncommon items and exactly 1% chance.
- [x] Make boss world gear ineligible; preserve potions and use personal milestone rewards only.
- [x] Select reward tier deterministically from the boss wave: wave 10 => tier 1, 20 => 2, 30 => 3, 40+ ten-wave milestones => 4.
- [x] Update loot/source docs and ensure old claims about random wave-one legendary drops are resolved.

### Task 2: One rarity/slot budget for all equipment

**Files:**
- Modify: `tools/equipment_catalog.py`
- Modify: `tools/recipes.py`
- Modify: `tools/power_curve.py` (created in progression plan)
- Update generated catalog docs listed by final integration task

**Interfaces:**
- Each catalog entry exposes explicit `tier`, `slot`, `stats`, and structured `effects` with magnitude, trigger, duration, and cooldown where applicable.
- Recipe outputs are normal catalog entries for comparison and inherit no undocumented bonus budget.

- [x] Generate a deterministic inventory of all general, racial, and crafted items grouped by rarity and equipment slot.
- [x] Compare each numeric component with its peer median; adjust the outliers from the approved spec, including `I23P` Grudgebreaker, `I23T` Worldrend Standard, and `I128` Oathforged Kingswrath.
- [x] Reduce raw stats or named-effect strength where needed; preserve rarity, naming, and intended race flavor.
- [x] Tune recipe inputs/fees only when needed for craft identity or economy; price cannot conceal an excessive power budget.
- [x] Run the report generator and inspect the grouped table and outlier list before the final build.

### Task 3: Update item reference docs

**Files:**
- Modify: `docs/ITEMS-AND-EQUIPMENT.md`
- Modify: `docs/ITEM-CATALOG.md`
- Modify: `docs/CROWNLANDS-EXPANSION.md`
- Modify: `docs/DECISIONS-AND-OPEN-ISSUES.md`

- [x] Refresh exact item component values, recipe output, elite/boss eligibility and power-report path from the source catalog.
- [x] Record any remaining effect comparisons that cannot be collapsed to a single numeric budget.

---

