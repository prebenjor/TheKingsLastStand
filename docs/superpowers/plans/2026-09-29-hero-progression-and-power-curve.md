# Hero Progression and Power-Curve Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Make every level a real choice between spell ranks and one +3 attribute button, remove automatic attribute growth, and generate an auditable hero/item power-curve report.

**Architecture:** Keep hero skill spending in the existing JASS progression module and use native Warcraft skill points for both native spells and synchronized stat buttons. Add a read-only Python report generator over existing hero/item catalogs and installed UnitBalance data; do not add another runtime subsystem.

**Tech Stack:** Warcraft III JASS, existing Python catalog/build pipeline, installed Definitive Edition API extraction.

**Spec:** `docs/superpowers/specs/2026-09-29-progression-difficulty-loot-wave-vote-design.md`

## Global Constraints

- Every selected hero starts at level 1 with 0 XP; selectable native attribute growth remains zeroed.
- Remove automatic +3 primary and +1 secondary attribute growth.
- +3 STR, +3 AGI, +3 INT are unranked repeatable choices; each consumes exactly one normal skill point.
- Spell ranks are learned by spending those same native skill points; never auto-rank on level gain.
- Preserve the separate fifth-level talent track and the 50-level cap.
- Use installed `UnitBalance.slk` provenance; fail with the existing extraction command when it is missing or stale.
- Respect the spec's verification boundary: do not add or run automated tests unless the user separately requests them. Build/package and JASS syntax checks are allowed.

## Review Focus

- Level-up events arriving at level 50 must not grant a stat or spell rank after the cap.
- Stat sync messages from inactive players or players without skill points must be ignored.
- Custom heroes must inherit the correct parent base stats without native zeroed growth being counted as base.
- Talent projections must not spend normal skill points or be included before the fifth-level milestone.
- Invalid item codes, duplicate equipment slots, or impossible stat-point budgets must produce clear report errors rather than plausible-looking results.

---

### Task 1: Restore single-point hero advancement

**Files:**
- Modify: `source/heroes.j`
- Modify: `source/combat.j`
- Modify: `tools/hero_progression.py`
- Modify: `tools/pipeline.py`
- Modify: `tools/hero_catalog.py` only if primary-stat metadata becomes unused at runtime
- Modify: `AGENTS.md`

**Interfaces:**
- Keep `KLS_StatChoiceApplySync` and its `KLSSTAT` payload values 0/1/2 for STR/AGI/INT.
- Remove the generated `KLS_ApplySpellRanks` interface and every call site; native ability leveling remains available through unit ability records.

- [x] Set level 1 and explicitly clear XP on selection; log both values.
- [x] Delete the automatic-growth array, growth function, level loop, and automatic spell-rank call. Keep talent milestone handling and owner-local stat controls.
- [x] Stop generating/injecting hero-level auto-rank JASS from `tools/hero_progression.py` and `tools/pipeline.py`; preserve safe ability object ranks and their descriptions.
- [x] Replace the stale agent rule describing automatic stat growth with the approved skill-point choice rule.
- [x] Run `python -B tools/build_map.py` only after all implementation plans are complete; inspect its generated JASS compile/package results.

### Task 2: Add deterministic power-curve report

**Files:**
- Create: `tools/power_curve.py`
- Create/update: `docs/STAT-POWER-CURVE.md`
- Read: `tools/hero_catalog.py`, `tools/equipment_catalog.py`, `tools/reference/installed/UnitBalance.slk`

**Interfaces:**
- CLI: `python -B tools/power_curve.py --level N --strength-points N --agility-points N --intelligence-points N --talents PATH --tomes RAWCODES --items RAWCODES`.
- Default mode writes the full deterministic 25-hero × 50-level report to `docs/STAT-POWER-CURVE.md`; custom mode prints the selected projection.
- Custom heroes use their declared parent hero's installed base stats. Normal stat allocations may spend at most `level - 1` skill points; talent selections are separate.

- [x] Parse the installed UnitBalance table through the existing verified extraction output and reject missing/stale provenance.
- [x] Calculate base stats, level, remaining normal points, stat allocations, one chosen talent per earned five-level milestone, tome effects, equipment stats, and named item effects separately.
- [x] Add catalog tables grouped by rarity and slot with damage, attributes, armor, HP, mana, speed, plus effect magnitude/trigger/duration/cooldown.
- [x] Flag shared tier-budget violations deterministically; reject unknown rawcodes and slot collisions.
- [x] After all plans are integrated, regenerate the full report and run the one final package build.

### Task 3: Source-of-truth documentation

**Files:**
- Modify: `docs/GAMEPLAY-SPEC.md`
- Modify: `docs/DECISIONS-AND-OPEN-ISSUES.md`
- Modify: `docs/PROGRESS-LEDGER.md`
- Modify: `docs/ROADMAP-AND-ACCEPTANCE.md`
- Modify: `docs/HEROES-AND-ABILITIES.md`

- [x] Update all current-state descriptions to say level 1 / zero XP, no automatic growth, stat buttons compete with spell points, level cap 50, and separate fifth-level talents.
- [x] Record the generated power-curve report path and its installed-data provenance requirements.
- [x] Keep engine, multiplayer, and gameplay checks pending until performed in Warcraft III.

---

