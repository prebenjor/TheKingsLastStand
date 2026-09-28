# Build changelog

Keep one entry for every packaged build. The entry names the exact immutable build ID, summarizes the user-visible changes, lists verification evidence, and leaves engine-only checks pending until a person tests that exact map. Add the entry in the same source change as the build; do not reuse an old build ID for changed map contents.

## KLS-D-1398318c4a - 2026-09-28

- Fixed the high-rank aura data that made Sacred Aura grant 500% magic resistance at rank 4. Installed campaign records declare these auras as three-rank abilities but contain stale fourth-rank values; rank generation now respects each record's declared level count and resolves fields through the internal ability code, including the Forsaken Paladin's `AHpa` alias.
- The same stale-rank handling was corrected for other native abilities, including Devotion Aura. Ranks 1–3 keep their installed values; later ranks continue from those declared values.
- Regression tests: **76/76 passed**. MPQ member readback and installed-editor API JASS syntax passed.
- Map SHA-256: `b7fe3601272d32c7d95e23fb7b50470ee6e39ca40bc914d0e9c2c14fa6016af2`.
- The package is at `dist/KLS-D-1398318c4a-Development.w3m`. Installing into the dedicated Warcraft III test folder stopped because the prior `KLS-D-5b63d38dc0-Development.w3m` is locked. A verified archive copy of the old map is preserved; the old file remains in the test folder until it is closed. Current-build in-game rank behavior and the editor Test Map remain pending; the earlier Test Map success remains attributed to `KLS-D-fd638ddcf5`.

## KLS-D-5b63d38dc0 - 2026-09-28

- Player-owned kills award the full role bounty only to the killing unit's player. King Aldric's kills award 25% of the bounty to every active player. Both use the recipient-only gold notification.
- Each active hero within 1,200 world units receives a full individual kill-XP award. Warcraft's native shared XP divides experience, so native normal/hero kill XP and native shared XP are disabled; the runtime awards the Warcraft default unit-level progression or hero-kill XP value to each nearby hero. Race and life state are not used as recipient filters.
- King Aldric's acquisition range is 900 to enable his attack bounty route. Ordinary wave breaks are now 50 seconds, while pre-boss breaks remain 180 seconds.
- Restoring Spring restores 1% maximum HP and mana every second within range without a healing effect, floating text, or timed notification.
- Shop-purchased gear is moved to an available normal inventory slot when possible. Vendor resale now obtains the manipulated/pawned item from the correct event native. Both behaviors still require live backpack/shop verification.
- Adds Hall of Banners, Royal Foundry, Siege Yard, and 34 hero-specific company/support unit records for the 17 selectable heroes. Their recruiting, doctrines, upgrade effect, placement, and multiplayer ownership remain engine-pending.
- Full source regression suite: **75/75 passed** after adding this build's changelog entry. Package member readback and installed-editor API JASS syntax passed. The earlier run's only failure was the changelog guard detecting that the newly generated ID was undocumented; this entry resolves it.
- Map SHA-256: `560b662379fb23969ad2528f53d2623667125760e89d050e6a2dd6c5e8781bc8`.
- Installed at `Documents/Warcraft III/Maps/TheKingsLastStand/KLS-D-5b63d38dc0-Development.w3m`; the installed hash matches the package. Editor save/reopen, current-build Test Map, Custom Game gameplay, XP/gold behavior, item UI, multiplayer, and endurance checks remain pending. The earlier Test Map pass stays attributed to `KLS-D-fd638ddcf5`.

## KLS-D-49ab762fcd - 2026-09-28 (superseded before installation)

- Intermediate package included personal player kill gold, King Aldric's 25% bounty for each active player, silent one-second spring regeneration, 50-second normal breaks, and the hero-company building/unit slice.
- Package inventory/readback and installed-editor API syntax passed. The XP-sharing audit then showed that the native alliance experience setting divides XP; the source was changed to award the full amount independently to each hero in range, producing the follow-up build `KLS-D-5b63d38dc0`.
- SHA-256: `612e9a0578749275d70ac3f72406ea32a97758fbbaa30485cc32a479974a4436`.
- This intermediate map was never installed or engine-tested; it is retained in `backups/development-builds/`.

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

