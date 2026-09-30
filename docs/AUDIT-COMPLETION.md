# Audit completion — 2026-09-30

Current Development build: **KLS-D-8048eea39b**. Package: `dist/KLS-D-8048eea39b-Development.w3m`. SHA-256: `6759047254a8fd3bef830e32af7af4f8804fe732237a25b87957004138664247`. Installed: `C:\Users\asphy\Documents\Warcraft III\Maps\TheKingsLastStand\KLS-D-8048eea39b-Development.w3m`. Package and installed bytes match; one current project map remains in each folder. Older maps are preserved under local `backups/development-builds/` and `backups/installed-diagnostics/`, outside the test folder. Captured authored terrain remains in the build provenance.

## Implemented and checked

| Audit finding | Change | Evidence |
|---|---|---|
| Power report omitted secondary stats/collisions and individual cross-tier checks | Shared installed attribute constants, normalized general/racial slots, STR/INT/AGI secondary values, initial level-1 point, per-item component checks | Behavioral projection/slot/tier tests; regenerated STAT-POWER-CURVE.md |
| Tree-dependent summon remained learnable | Keeper/Faelor learn native instant `AKfn` with five explicit Treant ranks beside three other spells | Decoded ability/unit records and installed field metadata |
| Fifth-level talents paused play; evasion affected spells | Owner-local synchronized talent buttons; attack-only positive-damage evasion | Actual JASS handlers executed through native-boundary harness; identical-client allocation checks |
| Ready messages unscoped/non-idempotent | Preparation epoch plus canonical desired state | Stale, malformed and repeated-message behavioral tests |
| Caravan automatic; town unlocks lacked effects | Nearby living escort, normal pathing, two ambushes, vulnerable cart, death/retry; once-per-match watchposts/shop stock/refuges/garrisons | Escort presence/ambush/arrival/death handlers; unlock source/catalog checks |
| Company research and recruit powers missing | 11 personal research services, 50 authored company/support powers, mobile support parents | Decoded object/ability metadata; ownership/refund/order/idempotence tests; generated COMPANY-RESEARCH-AND-POWERS.md |
| Regression suite red and status stale | Superseded expectations updated to approved current rules; full suite repaired; docs and current package synchronized | 181 tests passed; installed-API JASS compile and MPQ archive readback passed |

The baseline was 121 tests with 6 failures and 4 errors. New failing audit cases were observed before fixes. Old expectations for Anya's backpack, auto ranks, automatic stat growth, widespread world loot and deadlocked Night Elf prerequisites were corrected to the approved rules; failed checks were not merely disabled.

Independent read-only review found two Important defects: Counter-Siege did not hit mobile invading siege roles, and recycled handles could inherit stale upgrade bookkeeping. Both received failing regressions and fixes, followed by reviewer recheck. Counter-Siege now covers the shared `umtw`/`hbew`/`nhyc` roster. Fresh recruits/construction starts clear bookkeeping; ordinary death retains totals for native resurrection. No further reachable issue was identified in the fixes by that review.

Commands: `python -X utf8 -B -m unittest discover -s tests -v`, `python -X utf8 -B tools/build_map.py --install-test-map`, and `git diff --check`. Local raw suite evidence: `test-results/audit-finish-final.txt`. Future agents can rerun the command; local test logs/installed Blizzard tables are intentionally excluded from Git.

## Current-build acceptance still pending

Automated handlers, serialization, syntax and package readback do not prove native game behavior. Keep DEVELOPMENT until these pass:

- Editor save/reopen, current-build Test Map and Custom Game startup. Preserve the user-reported successful earlier Test Map for `KLS-D-fd638ddcf5`; it is a pass, not a failed step.
- Mixed-race workers, mining, structure menus/icons, native queues, footprint/gathering access, town routes, open gate, minimap/bounds and boss clearance.
- All 25 heroes and eight new kits, level 1/0 XP/one point, manual spell/stat choices, safe ranks 4–5, Briar Host ranks 1–5 and Sacred Aura descriptions/effects.
- Company service stock, casts, personal refunds and stat deltas, later recruits and resurrection; all four Legendary recipes, shops/colors/gear/equipment/selling/full-inventory delivery without duplication.
- Escort movement, ambushes, loss/retry, shared permanent perks and personal contributor rewards during active waves.
- Independent multiplayer backpack panels, every client's difficulty/Ready/stat/talent controls, personal gold, full nearby XP and quiet regeneration.
- Normal-speed 2/3/4-player sessions and full Crownlands/endless endurance, including player departure and King death.

Next human-run check: launch the installed **KLS-D-8048eea39b** in a two-player Custom Game, confirm both displayed build IDs, choose different-race heroes, and open both backpacks simultaneously. Confirm each retains its own contents and Player 2 can vote Ready and spend a stat/talent point without affecting or pausing Player 1. Record screenshots/full `-diag` output on this exact build, then use the broader [acceptance register](ROADMAP-AND-ACCEPTANCE.md).

## Repository handoff

The source, generated catalogs, design decisions, tests, current Development map and public manifest are included in the audit-completion commit for `prebenjor/TheKingsLastStand` on `main`. Local installed Blizzard data, test logs and archived maps remain excluded. Verify `HEAD` against `origin/main` for publication; use the exact package ID/hash above for engine results.
