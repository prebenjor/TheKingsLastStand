# Build changelog

Keep one entry for every packaged build. The entry names the exact immutable build ID, summarizes the user-visible changes, lists verification evidence, and leaves engine-only checks pending until a person tests that exact map. Add the entry in the same source change as the build; do not reuse an old build ID for changed map contents.

## KLS-D-2780b4380e - 2026-09-28

- Added two installed-data-verified Forsaken Kingdom heroes, Human Ilastar and the Forsaken Paladin, bringing the selector to 17 choices. Their descriptions use the native skill names, their native abilities are extended through the same level-100/rank-10 progression generator, and each receives a new custom signature ability (`AK15`/`AK16`).
- Kept the visible personal gold payout, ordinary gear movement/sale flags, and one-second percentage-based Restoring Spring behavior in the same build.
- Full source regression suite: **66/66 passed**. Package inventory/readback and installed-editor API syntax checks passed. The two recent 15-roster assertions were updated after the 17-entry catalog was added.
- Map SHA-256: `30e1fa1a9c5e6415131f2aea1f200046504e93dbe3dab9de504482eb24641a33`.
- Current-build editor save/reopen, Test Map, Custom Game, live shop/backpack/reward/spring, multiplayer, and endurance checks remain pending. The prior user-reported Test Map pass remains attributed to `KLS-D-fd638ddcf5` only.

## KLS-D-2cd4884e7f - 2026-09-28

- Changed the Forsaken backpack from custom clone `Ibpk` to an in-place edit of installed item `ebua` (`EquipmentBackpackAnya`). This is an evidence-based fix for the reported click-to-open issue; actual interaction remains unverified. Kept `AIni`, `AEqu`, and `ASde`; omitted `ATua`, which installed data identifies as Undead Anya's talent ability.
- Retains personal on-screen gold bounty notifications, droppable and pawnable normal gear (boss relics remain unsellable), and the Restoring Spring's 1% max HP and mana restoration each second. These behaviors are package/source proven but remain pending in-game confirmation.
- The backpack identity regression failed against `Ibpk`, then passed against native `ebua`. Full suite: **65/65 passed**. Package inventory/readback and installed-editor JASS syntax passed.
- Map SHA-256: `fb8a6adede04d1475c5668c44d1b77616fbff19215ec712d7150cdf64502a2cd`.
- Current-build editor/UI/gameplay checks remain pending. Warcraft III PID 46920 still has the earlier installed map open, so this build is in `dist/` and the previous package is archived locally.

## KLS-D-3a0464e019 - 2026-09-28

- Diagnostic `-diag` now reports each active player's runtime race and actual first worker object/unit name, to distinguish the reported Acolyte portrait from an actual Acolyte spawn.
- Installed-data extraction/provenance now includes `UnitBalance.slk`, `UnitUI.slk`, `UnitAbilities.slk`, and `UnitWeapons.slk`. The additional global campaign hero records and worker identities are documented; the hero/building/unit gameplay expansion remains a separate reviewed design proposal.
- Regression suite: **65/65 passed**. Installed-editor JASS syntax and 23-member MPQ package/readback passed.
- Map SHA-256: `c0bb8275469ffb3a2165930fd7ccd62ca6716bc8203a6fc5cc366d5d732365be`.
- Current-build editor/game checks remain pending. Warcraft III PID 46920 still holds the older test map, so this new package remains in `dist/` and the older installed map was preserved.

## KLS-D-b9e9b9dd33 - 2026-09-28

- Baseline for this changelog: development map with the 40-wave co-op runtime, 15-hero selector, expanded battlefield, multi-tier shops, attribute books/recipes, and longer preparation breaks.
- Map SHA-256: `3bbcd7be9bb9d3f2ba02febd026b52c143f5ba28dfc9c52ef4ef1b52e149cc7a`.
- Package/MPQ readback, installed-editor JASS syntax check, and 59 source regressions passed for this build.
- The user's successful Test Map report applies to earlier build `KLS-D-fd638ddcf5`, not this baseline. Editor/gameplay and multiplayer checks for `KLS-D-b9e9b9dd33` were still pending.

## KLS-D-dddc30394a - 2026-09-28

- Enemy kills now show each active defender the exact gold amount added to their own resources. Boss participation gold uses the same visible notification.
- Ordinary equipment is droppable and pawnable, enabling native movement between the Forsaken backpack, normal inventory and equipment UI, and vendor buyback. Boss relics can be moved/equipped but remain unpawnable. These engine interactions still need live confirmation.
- King's Restoring Spring now restores 1% of maximum HP and mana each second within 450 range, capped at each maximum. It emits the restore effect only while the hero is missing HP or mana.
- Focused regression tests failed against the previous source, then passed for the corrected reward display, object flags, and spring cadence. Full suite: **63/63 passed**. Installed-editor API syntax and MPQ package readback passed.
- Map SHA-256: `d646a4a3de78b4e8cbeb1bed6ab5121344565227547dcca7c60c6255ee2d05ab`.
- Installing this build was blocked because Warcraft III PID 46920 held the older `KLS-D-f89f212a3a-Development.w3m` open. The original was preserved and a byte-identical archive copy was verified; the new build remains available in `dist/`.
- Editor save/reopen, Test Map, Custom Game startup, native item transfer/equipment/sale, visible combat rewards, spring behavior, multiplayer and endurance checks remain pending for this build. Keep it labelled development.

