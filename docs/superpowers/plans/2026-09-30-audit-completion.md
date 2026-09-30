# Finish the audited gameplay and expansion gaps

Scope: finish the seven findings from the September 30 audit, retain the full approved Crownlands design and personal multiplayer economy.

1. Correct power projections and catalog slot/tier validation with installed attribute conversions.
2. Replace tree-dependent learnable Force of Nature with a verified native summon clone and five explicit treant ranks.
3. Replace fifth-level talent dialogs with owner-visible synchronized controls; restrict evasion to positive attack damage.
4. Make Ready messages idempotent and preparation-specific.
5. Complete town recovery: real escort participation/threat/retry, persistent shared town unlocks and personal contributor rewards.
6. Complete chapter research, company weapon/armor branches and custom company/support abilities, with mobile recruit parents.
7. Repair superseded regression expectations, run the relevant/full suites, review, document, package and install one Development build. Preserve the earlier successful Test Map result; live current-build engine/multiplayer/endurance acceptance still requires evidence.

## Execution ledger

- Baseline: KLS-D-2aac020fb1. Full suite: 121 tests, 6 failures and 4 errors. Raw output: test-results/audit-finish-baseline.txt.
- Ruling: continue in the existing checkout containing the authorized uncommitted map work. A fresh worktree would omit the current implementation and recent backpack repairs.
- Ruling: use the existing approved plans and audit as the implementation brief. The user asked to finish these; no additional approval cycle is needed.
- Ruling: attribute conversions were read from installed Units/MiscGame.txt and custom_v1; both agree. Pin these conversions in generated map constants and use the same catalog in projections, avoiding assumptions about SLK display totals.
- Tasks 1–6 implemented. Initial failing audit regressions were observed before their fixes; coverage includes stale/idempotent Ready messages, talents, spell-vs-attack evasion, escort presence/arrival/death, research ownership/refunds/order and non-stacking upgrades.
- Independent read-only review found two Important defects: ineffective Counter-Siege against mobile invaders and stale recycled handle bonus totals. Both received failing regressions, fixes and a reviewer recheck; no remaining reachable issue was identified in those fixes.
- Ruling: retain bonus bookkeeping across ordinary death for native resurrection, but clear it on each fresh company stock purchase and construction start. Flushing at death would apply bonuses twice after resurrection and later research.
- Ruling: report includes the initial level-1 normal skill point; reset the selected hero to exactly one initial point. This uses the same spell-or-stat budget, not a free stat award.
- Task 7: final docs and package/install complete; KLS-D-8048eea39b installed with matching hash. Full suite: 181 passed. Source and package publication accompanies this snapshot; verify the final commit against `origin/main`. Current-build engine/multiplayer/endurance acceptance pending; no live acceptance claimed.
