# Build changelog

Keep one entry for every packaged build. The entry names the exact immutable build ID, summarizes the user-visible changes, lists verification evidence, and leaves engine-only checks pending until a person tests that exact map. Add the entry in the same source change as the build; do not reuse an old build ID for changed map contents.

## KLS-D-4a67348b4e - 2026-09-29

- The optional King's Restoring Spring visual now uses the shared checked spawn wrapper with the `restoring spring visual` context. Failed creation is logged and counted in diagnostics without aborting the match or disabling the coordinate-based regeneration timer.
- Full source regression suite: **123/123 passed**. Package archive readback and installed-editor API syntax checks passed.
- Package SHA-256: `a013631ed88293b9d4c2610015152135eb3a7a9456e5b119cc2b8c211560aff4`.
- Installed on 2026-09-29 at `Documents/Warcraft III/Maps/TheKingsLastStand/KLS-D-4a67348b4e-Development.w3m`; the installed SHA-256 matches the package manifest, and the folder contains one project map.
- Editor save/reopen, current-build Test Map, Custom Game, gameplay, multiplayer, and endurance checks remain pending. The earlier user-reported Test Map success remains assigned to `KLS-D-fd638ddcf5`.

## KLS-D-81285a4cc0 - 2026-09-29

- `-diag` now reports each active player's expected and actual starting mine, actual owner player ID, remaining gold, and coordinates. Failure to create a race-specific starting mine now logs the specific required-spawn context `starting racial gold mine`.
- Full source regression suite: **122/122 passed**. Package archive readback and installed-editor API syntax checks passed.
- Package SHA-256: `21540054f1250628fa1095ad42ee68bb986982a2f421c89b421574de827398cc`.
- Installed on 2026-09-29 at `Documents/Warcraft III/Maps/TheKingsLastStand/KLS-D-81285a4cc0-Development.w3m`; the installed SHA-256 matches the package manifest, and the folder contains one project map.
- Editor save/reopen, current-build Test Map, Custom Game, actual starting mine ownership/mining, all other live gameplay, multiplayer, and endurance checks remain pending. The earlier user-reported Test Map success remains assigned to `KLS-D-fd638ddcf5`.

## KLS-D-dd3a53babf - 2026-09-28

- Removed the tree-targeted native `AEfn` spell from Keeper of the Grove and Faelor Briarward whenever hero spell ranks are applied. Their tree-free Grove Awakening/Briarward Stand signature spells remain available for summoning Treants on open ground.
- Full source regression suite: **120/120 passed**. Package archive readback and installed-editor API syntax checks passed.
- Package SHA-256: `f2d804924a18aaab17ff00ed8d61b321a7fda54278a08e77559c3fcf6ab666cf`.
- Installed on 2026-09-29 at `Documents/Warcraft III/Maps/TheKingsLastStand/KLS-D-dd3a53babf-Development.w3m`; the test-folder SHA-256 matches the package manifest, and the folder contains one project map. The prior map is retained in `backups/installed-diagnostics/20260928T192844325669Z-KLS-D-8669a44192/`.
- Re-ran the full source regression suite on 2026-09-29: **120/120 passed**. Current-build editor save/reopen, Test Map, Custom Game, Keeper/Faelor casting, mine ownership/mining, shop/economy behavior, multiplayer, and endurance checks remain pending. The earlier user-reported Test Map success remains assigned to `KLS-D-fd638ddcf5`.


## KLS-D-f5fd3c5993 - 2026-09-28

- Undead and Night Elf players now start with an already-owned Haunted or Entangled Gold Mine at their base. Both retain the full 1,000,000-gold reserve; Human and Orc mines remain neutral. Additional neutral Undead mine haunting now recognizes Warcraft's native `hauntgoldmine` order.
- Raised equipment base prices to Common 300, Uncommon 1,000, Rare 3,000, Epic 8,000 and Legendary 20,000 gold. Blade/Bow/Staff cost 1.5× base; the three original recipe fees doubled to 5,000/7,000/12,000, racial Legendary recipes cost 9,000, and attribute tomes cost 1,000/3,000/8,000. Consumables and item stats are unchanged.
- Full source regression suite: **119/119 passed**. Package archive readback and installed-editor API syntax checks passed.
- Package SHA-256: `490a89b9445bc1d7af961bb8374222ca2af9cd3dbd356c6e8e29d352bed89351`.
- The package remains in `dist/`; Warcraft III PID `36140` is still running with the older installed map, so this build was not installed. The user-reported Test Map success remains assigned to `KLS-D-fd638ddcf5`. Current-build editor save/reopen, Test Map, Custom Game, mine harvesting, shop/economy behavior, multiplayer and endurance checks remain pending.


## KLS-D-c6f02bf50d - 2026-09-28

- Optional spawn failures now include useful context in `-diag` while allowing the match to continue for scenery, ability effects, signature summons, boss reinforcements, and optional Crownlands encounters. Required map setup and wave enemy/boss spawns still stop the match if creation fails; a partially created optional story encounter is cleaned up and remains retryable.
- Preserved the hero-panel `+3 Strength`, `+3 Agility`, and `+3 Intelligence` skills for per-level stat selection. There is no per-level stat dialog in this package; the separate specialty talent dialog remains every fifth level.
- Full source regression suite: **116/116 passed**. Package archive readback and installed-editor API syntax checks passed.
- Package SHA-256: `0869d7fa5bb3f1f67744768648c7690e7365193a402777a23e878fee73637ad0`.
- The package remains in `dist/`; Warcraft III PID `36140` still holds the older installed map, so this build was not installed. Current-build editor save/reopen, Test Map, Custom Game, gameplay, multiplayer, and endurance remain pending. The user-reported Test Map success remains assigned to `KLS-D-fd638ddcf5`.

## KLS-D-25463efa09 - 2026-09-28

- Kept the requested level-up choices in the hero ability panel as native `+` skills: `KSTR`, `KAGI`, and `KINT` each grant +3 to one primary stat per level. The old global stat-choice dialog is absent from current source; only the separate fifth-level specialty talent uses a dialog.
- Failed random enemy item drops now log the item name/rawcode, enemy type and coordinates, and killer player ID, so missing loot-object creation is visible in the diagnostic log.
- Full source suite: **113/113 passed**. Package member readback and installed-editor JASS syntax checks passed.
- Package SHA-256: `d1a5d81cc66998f526103738d0164388b24467306bdc9b73e9d6ec02f087b03d`.
- Installation safely stopped because Warcraft III PID `36140` still holds the old `KLS-D-1a040d638c-Development.w3m`. The old test map and its verified archive remain intact; this build is packaged in `dist/` but not installed. Current-build editor save/reopen, Test Map, Custom Game, gameplay, multiplayer and endurance checks remain pending. The earlier user-reported Test Map pass remains assigned to `KLS-D-fd638ddcf5`.

## KLS-D-2f2397cf14 - 2026-09-28

- Boss relics and Crownlands story items now share a guarded personal-reward delivery path. Failed `CreateItem` calls retain the item rawcode in that owner's queue and retry every five seconds during the match; full inventory leaves a visible owner-bound item at the owner's base.
- Added source regressions for boss/story routing, null-handle guards, owner-bound fallback and retry bookkeeping. Full suite: **112/112 passed**. Installed-editor JASS compilation and package member readback passed.
- Package SHA-256: `e63d8c15d90458056887f056ac66d1194aa30326e20ec94847f5ac91e2d7310f`.
- Installation was attempted but safely stopped because Warcraft III still locks the older `KLS-D-1a040d638c-Development.w3m`; its original and one hash-verified archive copy remain intact. This current build remains packaged in `dist/` and is not installed. Editor save/reopen, current-build Test Map/Custom Game, live item delivery, gameplay, multiplayer and endurance remain pending. The earlier user-reported Test Map pass remains assigned to `KLS-D-fd638ddcf5`.


## KLS-D-0227009b20 - 2026-09-28

- Carries forward the gameplay content of `KLS-D-8669a44192`; no hero, wave, item, or race behavior changed. This package has a new build ID because the supported installer code changed and is part of the build fingerprint.
- Hardened Windows installation: old maps are copied and hash-verified before removal, an exact existing archive is reused on retry, and failed removal or new-map copy restores prior files when possible. A locked-map error leaves the running map untouched and does not leave a partial new install.
- Installer regressions: **6/6 passed**. Full source suite: **108/108 passed**. Package readback and installed-editor API syntax checks passed.
- Package SHA-256: `23a7887af12f726ddffe37ab4b9e817c021ba46a2842ced4ce80a53297f43a6c`.
- Installation safely stopped because Warcraft III still holds `KLS-D-1a040d638c-Development.w3m`. The original remains in the test folder and has one byte-identical archived recovery copy at `backups/installed-diagnostics/20260928T192844325669Z-KLS-D-8669a44192/KLS-D-1a040d638c-Development.w3m` (SHA-256 `eaee0e501b3e7ced381bda7c93c530d79499faad94f2bb80304a9aeb1340e362`). `KLS-D-0227009b20` remains packaged in `dist/`, not installed. The earlier user-reported Test Map pass remains assigned to `KLS-D-fd638ddcf5`; all checks for this exact build remain pending.

## KLS-D-8669a44192 - 2026-09-28

- Replaced the per-level stat dialog with three native hero `+` skills: `KSTR`, `KAGI`, and `KINT` each add three points to the chosen primary stat per rank. The separate every-fifth-level specialty choice remains.
- Corrected the Undead Temple parent to native `utod`, retaining the Temple model, icon, training and research data. Added race-specific descriptions for altars, arcane/support buildings, towers, Hall of Banners, Foundries and Siege Yards. Sanctuary-style towers share a 15 HP / 3-second / 650-range ally-heal hook.
- Added Undead Acolyte neutral-gold-mine haunting with gold preservation and owner harvest order. Extended Night Elf Tree of Life Entangle range to reach its starting mine. Default player race preference is Random; hero choice applies the selected race per player.
- Preserved the authored first 40 waves and added ten bounded, repeating campaign rosters for Naga, Blood Elf, Fel Orc, Burning Legion, and Scourge forces. Wave 49 converges all five factions; Wave 50 adds the installed campaign Lady Vashj boss. Later bosses recur every ten waves, rotate through installed campaign leader records, and reuse the telegraphed slam, summon, and tower suppression mechanics.
- Continued live-wave count, health, damage, bounty, XP, and tracked-enemy accounting through endless waves. Waves 50 and later grant each active player a personal Legendary item from the equipment catalog; waves 10-40 retain their existing relic rewards. Wave 40 continues automatically; King Aldric's death ends the run and the HUD records the highest wave.
- Kept campaign unit models, animations, movement, and armor sourced from the installed Definitive Edition tables. Added a generated 50-row roster catalog and synchronized the wave, gameplay, Crownlands, decisions, roadmap, and contributor documents.
- Full automated regression suite: **105/105 passed**. Build-manifest checks `archive_readback` and `syntax_installed_api` are recorded as passed; the packaged artifact hash matches the manifest.
- Package SHA-256: `b7d0b41039d0cd4d655daf97d40a0329d443f987c62e9a927c87a8fc7bb995a0`.
- Installation first archived a verified copy of prior map `KLS-D-1a040d638c` but could not move its original. A retry on 2026-09-28 confirmed a running Warcraft III process still locks that file. The original and archived copy both have SHA-256 `eaee0e501b3e7ced381bda7c93c530d79499faad94f2bb80304a9aeb1340e362`; no current-build file was installed. Exit Warcraft III completely and rerun `python -B tools/build_map.py --install-test-map`. Editor save/reopen, Test Map, Custom Game, plus-button behavior, race-specific mine orders, Temple UI, campaign-unit visuals and pathing, wave 40-50 and later-boss gameplay, multiplayer, and endurance checks remain pending. The earlier user-reported Test Map success remains a pass for `KLS-D-fd638ddcf5`.

## KLS-D-1a040d638c - 2026-09-28

- Carries forward the complete Crownlands expansion and Sacred Aura tooltip work described in the previous entry.
- Fixed supply-escort contribution tracking: any active defender who joins while the caravan is already travelling is now recorded for that chapter's personal story reward. The escort contributor is recorded only after its caravan successfully spawns.
- Added a regression for the second-player join path. Full automated regression suite: **88/88 passed**. Package member readback, installed-editor API syntax and archive verification passed.
- Package SHA-256: `eaee0e501b3e7ced381bda7c93c530d79499faad94f2bb80304a9aeb1340e362`. Installed at `C:\Users\asphy\Documents\Warcraft III\Maps\TheKingsLastStand\KLS-D-1a040d638c-Development.w3m`; installed hash matches.
- Supersedes `KLS-D-41d103f7cb`, which is archived locally. World Editor is now open on this exact installed map and the editor window is responsive; save/reopen, Test Map, Custom Game, in-game feature checks, multiplayer and endurance remain pending. The earlier user-reported Test Map success remains a pass for `KLS-D-fd638ddcf5`.

## KLS-D-41d103f7cb - 2026-09-28

- Expanded the battlefield to 192×192 and placed four connected allied settlements: Human Crownshire, Orc Redtusk Hold, Night Elf Moonbark Glade and Undead Wraithfall. Kept the defense road, gate, player plots and existing wave cadence; terrain, pathing, camera bounds and minimap were rebuilt together.
- Hero choice now sets each player's race independently, including the matching Peasant, Peon, Wisp or Acolyte, Town Hall, Altar, construction menu, towers and race-flavored Hall of Banners, Foundry and Siege Yard. Shared construction roles and costs remain catalog-driven.
- Added eight race-native heroes (two per race), custom signature abilities and matching company/support recruits. The roster now has 25 choices; heroes begin at level 1 and cap at 50, with a visible +3 primary-stat choice per level and a separate Strength/Agility/Intelligence talent choice at every fifth level.
- Added the four-stage optional Crownlands recovery story, which can progress during active waves without altering wave counts or timers. Shared unlocks and personal contributor rewards last through the match.
- Added 20 universal race-themed gear items (five standard rarity tiers per race), with item names/tooltips colored white, green, blue, purple and gold. Shop stock, stats, drops, icons and four race-specific Legendary Foundry recipes use the shared item catalog.
- Fixed Sacred Aura learned and learn-menu descriptions for both `AHas` and `AHpa`; rank 4 displays 38.5% resistance / 27.5% healing received, rank 5 displays 42% / 30%, and the learn menu distinguishes current from next rank.
- Full automated regression suite: **87/87 passed**. Package readback, installed-editor API syntax checks and archive verification passed. Package SHA-256: `67f363beac6ce79313916026016a34b8458b35c648e7d27db46f0af370308928`.
- Installed at `C:\Users\asphy\Documents\Warcraft III\Maps\TheKingsLastStand\KLS-D-41d103f7cb-Development.w3m`; installed SHA-256 matches the package. Previous development and installed maps were archived under `backups/development-builds/` and `backups/installed-diagnostics/`. Current-build editor save/reopen, Test Map, Custom Game, live feature checks, multiplayer and endurance remain pending. The earlier Test Map success remains a pass for `KLS-D-fd638ddcf5`.

## KLS-D-b5ae4ab2fe - 2026-09-28

- Added safe extended ranks through rank 5 and set the hero level cap to 50. Installed native ranks remain unchanged. Beyond a spell's native maximum, only its explicitly registered power fields grow by 10% of the last authored value per rank; every other field holds the final authored value. Warden Blink stays capped at its native three ranks. Sacred Aura rises from 35% magic resistance to 38.5% at rank 4 and 42% at rank 5, avoiding the stale 500% value.
- Checked all registered effect fields against the installed editor metadata. Covered damage, healing, armor, evasion, aura bonuses, and other direct effects. Skills without a safe registered effect stay at their native rank limit.
- Applied standard rarity colors to equipment and boss relic names, tooltip quality headings, and quality-shop names: white, green, blue, purple, and gold. Item tiers and full stat descriptions remain visible.
- Full source regression suite: **79/79 passed**. Package readback and installed-editor API syntax passed.
- Map SHA-256: `05a072b826318b5d40d9cacda0f9e3755c845093f618f7bfb227da3fd7ec5da7`.
- Installed at `C:\Users\asphy\Documents\Warcraft III\Maps\TheKingsLastStand\KLS-D-b5ae4ab2fe-Development.w3m`; installed hash matches the package. Current-build editor save/reopen, Test Map, Custom Game rank/color presentation, gameplay, multiplayer, and endurance checks remain pending. The earlier Test Map pass stays attributed to `KLS-D-fd638ddcf5`.

## KLS-D-8b5076c3eb - 2026-09-28

- Stopped extending regular hero spells beyond the `levels` count in the installed Warcraft ability data. The map now preserves each ability's authored native ranks and caps runtime rank-ups to that spell's own limit.
- Removed generic numeric extrapolation. It treated every numeric field as a scalable effect; for example, Warden Blink's native mana costs 50/10/10 became 0 at generated rank 4. Unsupported higher ranks are no longer emitted or assigned.
- Regression coverage checks native-rank caps for every selectable hero spell and the Blink mana-cost case. Full regression suite: **77/77 passed**.
- Package member readback and JASS syntax against the installed editor API passed.
- Map SHA-256: `10f6d56f3811cece7189633f8b840746f72c34583ec41e28752e2f50396545c3`.
- Installed at `C:\Users\asphy\Documents\Warcraft III\Maps\TheKingsLastStand\KLS-D-8b5076c3eb-Development.w3m`; installed hash matches the package. Current-build editor save/reopen, Test Map, Custom Game rank behavior, gameplay, multiplayer, and endurance checks remain pending. The earlier Test Map pass stays attributed to `KLS-D-fd638ddcf5`.

## KLS-D-a2dae2be8c - 2026-09-28

- Fixed recipe delivery so a successful craft no longer falls through into the failure refund path. If the output cannot be delivered, the failure notification and fee refund still run once.
- Added a regression check for the contradictory success/failure notification and duplicate-refund path.
- Focused recipe/progression regression tests: **14/14 passed**. Full regression suite: **77/77 passed**.
- Package member readback and JASS syntax against the installed editor API passed.
- Map SHA-256: `e86d0c0e1696897d8727d243bf6bc92bd6f5ce8ca6b6b39a8d24ae38668dbd9d`.
- Installed at `C:\Users\asphy\Documents\Warcraft III\Maps\TheKingsLastStand\KLS-D-a2dae2be8c-Development.w3m`; its SHA-256 matches the package. Current-build editor save/reopen, Test Map, Custom Game craft interaction, gameplay, multiplayer, and endurance checks remain pending. The earlier Test Map pass stays attributed to `KLS-D-fd638ddcf5`.

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

