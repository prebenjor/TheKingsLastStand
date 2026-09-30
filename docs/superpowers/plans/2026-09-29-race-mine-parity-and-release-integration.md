# Race Mine Parity and Final Build Integration Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Give every race the approved equal starting gold reserve while preserving its mine identity, then document, package, install, and publish one coordinated Development build.

**Architecture:** Normalize reserve during each selected player's existing starting-mine setup. Human/Orc keep neutral mine objects; Undead/Night Elf keep Haunted/Entangled mine variants. After all source and catalog work, generate one current package, archive previous Development packages through the existing builder, install to the single configured Warcraft test path, and publish the coordinated changes.

**Tech Stack:** Warcraft III JASS; existing Python map builder and MPQ pipeline; Git/GitHub.

**Spec:** `docs/superpowers/specs/2026-09-29-progression-difficulty-loot-wave-vote-design.md`

## Global Constraints

- Each race receives a starting mine reserve of exactly 1,000,000 with five workers and personal income unchanged.
- Preserve the one current Development build naming/install workflow; do not create scattered intermediate maps.
- Update source-of-truth design docs and the build changelog with the exact final build ID and package SHA-256.
- Keep the build labeled Development until current-build editor, Custom Game, multiplayer, and endurance checks pass.
- Carry forward the successful Test Map result for `KLS-D-fd638ddcf5` as evidence for that build only.
- Push only after the final local package and docs are reviewable; previous user authorization to push applies.

## Review Focus

- A neutral Human/Orc mine must retain the normalized reserve without replacement.
- Recreated Haunted/Entangled mines must preserve location, ownership, and the same reserve.
- Missing starting-mine handles must not stop hero selection or corrupt other players' mine reserves.
- The builder must archive old Development maps once and leave only the current named package in `dist`.
- The installed test map and changelog hash must refer to the same final build artifact.

---

### Task 1: Normalize starting mine reserves

**Files:**
- Modify: `source/heroes.j`
- Modify: `tests/test_race_mining_buildings.py` only if separately requested

**Interfaces:**
- Keep `KLS_ConfigureStartingMine(integer p, integer raceId)`.
- Set `amount = 1000000` for all races. Replace the mine only for Night Elf (`egol`) and Undead (`ugol`); for Human/Orc set reserve on the existing neutral mine.

- [x] Read existing amount/coordinates/facing only when a race-specific replacement is needed.
- [x] For Human/Orc, call `SetResourceAmount` on the original mine and log the fixed reserve.
- [x] For Night Elf/Undead, preserve current replacement and fallback behavior, but assign exactly one-million reserve.
- [x] Update `docs/CROWNLANDS-EXPANSION.md` and mining section in `docs/GAMEPLAY-SPEC.md`.

### Task 2: Final docs, package, install, and push

**Files:**
- Modify: `AGENTS.md`
- Modify: `README.md`
- Modify: `docs/GAMEPLAY-SPEC.md`
- Modify: `docs/DECISIONS-AND-OPEN-ISSUES.md`
- Modify: `docs/ROADMAP-AND-ACCEPTANCE.md`
- Modify: `docs/PROGRESS-LEDGER.md`
- Modify: `docs/ITEMS-AND-EQUIPMENT.md`
- Modify: `docs/ITEM-CATALOG.md`
- Modify: `docs/CROWNLANDS-EXPANSION.md`
- Modify: `docs/WAVES-AND-BOSSES.md`
- Modify: root `CHANGELOG.md`
- Create/update: `docs/STAT-POWER-CURVE.md`

**Interfaces:**
- Sole supported build command: `python -B tools/build_map.py`.
- Install command: `python -B tools/build_map.py --install-test-map`.
- One current package path from `diagnostic_output_path(build_id)`; builder owns archival of older matching Development packages.

- [x] Update all current-state statements from source/catalog values, including race reserve, level choices, difficulty, readiness, loot, item budgets, and power report.
- [x] Package the final implementation only after the generated audit is clean; record the final build ID, SHA-256, serialization, and compiler output. (A preceding Development package was archived when its item audit surfaced remaining balance issues.)
- [x] Install that exact package into the configured Warcraft III test folder. Do not claim live gameplay or multiplayer acceptance without current-build evidence.
- [x] Add one immutable dated Development changelog section with the exact package ID/hash, user-visible changes, checks performed, and pending engine gates.
- [x] Update progress ledger and acceptance checklist; retain the prior successful Test Map result for its own exact build.
- [ ] Review `git diff`, commit the coordinated changes, and push the authorized branch to the existing GitHub repository.

---

