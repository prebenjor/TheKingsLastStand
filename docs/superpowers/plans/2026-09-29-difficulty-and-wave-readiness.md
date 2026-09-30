# Difficulty and Wave-Readiness Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Let players choose match difficulty before wave 1 and unanimously start each next wave early through non-pausing owner-local controls.

**Architecture:** Keep all synchronized vote state, difficulty locks, wave timers, and spawn transitions in `source/game.j`. Put shared names, tallies, reset, and scaling helpers in the earlier-loaded `source/match_rules.j`, and keep Ready handlers after `KLS_Spawn` to satisfy JASS definition-before-call ordering. Frames only display or send the local player's vote; the existing HUD reports the resolved state.

**Tech Stack:** Warcraft III JASS, owner-local Blz frames, synchronized `BlzSendSyncData` events, existing multiboard HUD.

**Spec:** `docs/superpowers/specs/2026-09-29-progression-difficulty-loot-wave-vote-design.md`

## Global Constraints

- Difficulty options are Easy / Normal / Hard / Very Hard, default Normal, locked after hero selection.
- Presets are Easy .75 HP/.80 damage/.90 count; Normal 1/1/1; Hard 1.30/1.20/1.10; Very Hard 1.60/1.40/1.20.
- Apply difficulty after existing wave/player scaling; round counts to nearest and clamp normal wave count to at least 1. Boss count remains 1.
- Boss reinforcements use the selected difficulty for their relevant count, health, and damage values.
- Readiness is unanimous among active players, scoped to the next wave, toggleable before unanimity, and never pauses the game.
- Retain 50-second ordinary and 180-second pre-boss breaks, with timer expiration as fallback.
- `GetLocalPlayer()` may affect UI only, never votes, spawn timing, or enemy creation.

## Review Focus

- A disconnected/inactive player must not block unanimity or cast a valid vote.
- Multiple clicks or duplicate sync messages must not count as multiple votes.
- A vote arriving after selection closes, after wave start, or after the break changes must not alter state.
- Simultaneous last-ready and timer-expiry events must spawn exactly one wave.
- A difficulty tie or no votes must resolve to Normal on every client.

---

### Task 1: Match difficulty voting and scaling

**Files:**
- Modify: `source/game.j`
- Create: `source/match_rules.j`
- Modify: `source/heroes.j`
- Modify: `source/hud.j`
- Modify: `docs/GAMEPLAY-SPEC.md`
- Modify: `docs/WAVES-AND-BOSSES.md`

**Interfaces:**
- Add `integer array KLS_DifficultyVote`, `integer KLS_Difficulty`, and `boolean KLS_DifficultyLocked`.
- Add `KLS_LockDifficulty`, `KLS_DifficultyVoteSync`, `KLS_DifficultyHealthScale`, `KLS_DifficultyDamageScale`, `KLS_DifficultyScaledCount`, and Ready handlers in their ordered match-rule/game modules.
- Difficulty sync key/payload: `KLSDIFF`, sender-owned values 0..3. HUD displays the final resolved difficulty.

- [x] Create owner-local difficulty controls during selection; every active slot begins with vote 1 (Normal).
- [x] Register synchronized vote events for active slots. Reject invalid sender/value and any event after lock.
- [x] Lock on selection completion/timeout; count active votes, resolve plurality, ties/no votes to Normal, and log the result.
- [x] Apply exact health, damage, and count multipliers to normal spawns after wave/player scaling; preserve one boss while scaling its HP/damage.
- [x] Extend boss reinforcement calculations to include difficulty without changing named roster selection.
- [x] Add the difficulty to a multiboard field without using local frame text in gameplay decisions.

### Task 2: Unanimous Ready vote

**Files:**
- Modify: `source/game.j`
- Modify: `source/hud.j`
- Modify: `docs/GAMEPLAY-SPEC.md`
- Modify: `docs/WAVES-AND-BOSSES.md`

**Interfaces:**
- Add `boolean array KLS_ReadyVote`, `KLS_ReadyVoteSync`, `KLS_ReadyClick`, `KLS_ResetReadyVotes`, and `KLS_ReadyCount`.
- Ready sync key/payload: `KLSREADY`, payload `"toggle"`; sender is derived from `GetTriggerPlayer()`.
- `KLS_Spawn` consumes the resolved difficulty and clears current readiness exactly once.

- [x] Create one local Ready toggle visible during selection-complete intermissions, including before wave 1.
- [x] Toggle only the sender's vote, update visible vote count, and spawn immediately only when all active slots are ready and `KLS_Alive == 0`.
- [x] Reset on each spawn and on each new preparation interval; hide during active waves and after match end.
- [x] Preserve timer-based fallback, prevent duplicate spawns, and handle one-player readiness as immediate unanimity.
- [x] Update the HUD/docs after the implementation plans are integrated.

### Task 3: Final source/package verification

**Files:**
- Modify: `docs/PROGRESS-LEDGER.md`
- Modify: root `CHANGELOG.md` via the final integration plan only

- [x] Check synchronized state paths by code inspection; confirm only rendering/click routing uses local-player guards.
- [x] Run the final package/JASS compiler command once after all four plans are integrated; record exact result and pending live checks.

---

