# Racial construction execution ledger

Approved plan: restore standard/expansion construction pages, repair 50 company recruits, add eight timed specialists and re-audit 25 heroes. Preserve the R2 saved native map and publish DEVELOPMENT artifacts/source/README updates.

- Baseline: Hero-Market-Repairs-R2 SHA256 `4048e415d03d920b2c258b4e78fbaa46d5153a13b4d3927bea425aa524bfc4ea`.
- Existing changes preserved in commit d193f1f, including four earlier unpushed commits. R2 prerelease published from the repair branch.
- Publication: automatic review rejected a direct main push; publication proceeds on the repair branch and the README update will be presented in a pull request. No default-branch update without explicit approval.
- Ruling: continue in the existing checkout on a new repair branch, preserving the prior saved-map workflow and all uncommitted source work. No duplicate worktree or regenerated terrain.
- Native engine gate: Forge inspection cannot demonstrate worker handle/cargo preservation. Expansion switching remains a separate prototype until actual native acceptance evidence exists. No alternate menu architecture substituted.
- Red: missing standard-menu catalog, missing specialist catalog and missing trained-unit/reconciliation registration reproduce the construction/recruitment gaps.
- 2026-10-02: catalogs, source/runtime, MCP per-race undo groups, 50-company reconciliation and eight specialist definitions/powers implemented. Reopened readback: 137 units, 148 abilities, 25 heroes. Regular build KLS-D-1f003ecdb7 and prototype KLS-D-5ec0710adf compile and preserve protected content; 243 tests, 241 passed, two baseline failures.
- Review fixes: removed-unit timer links, Skeleton Warrior parent, native air/ground root buffs, immediate issued-order switching guard and shield ownership validation. Red/green regressions cover runtime fixes. Native-format records round-trip byte-identically.
- Native acceptance: user reported no Undead page change in obsolete Prototype R2. Incorrect Chaos parent corrected in R5; retest requested. Production switching remains false, with expansion facilities unavailable in the regular handoff until acceptance. See docs/RACIAL-CONSTRUCTION-20261002.md for the complete pending checklist.
