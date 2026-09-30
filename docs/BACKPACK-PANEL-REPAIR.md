Current package and full-suite evidence have moved to [AUDIT-COMPLETION.md](AUDIT-COMPLETION.md). The repair snapshot below is historical; its original counts are retained.

# Backpack panel repair candidate — 2026-09-30

Current DEVELOPMENT package: **KLS-D-2aac020fb1**, `dist/KLS-D-2aac020fb1-Development.w3m`.
SHA-256: `0b71c26a3353d088cedb376d0d27d597039b9662687d475c60569c732fcb3a9d`.

## User-visible behavior and implementation

The reported symptom is that P1 using their backpack closes P2/P3/P4's backpack and vice versa. The map's former item-use handler only logged the action; panel behavior comes from native ebac/AIni/AEqu/ASde. This does not establish an engine root cause by itself.

The candidate adds a presentation-only client preference in `source/backpack.j`. Only the owning hero's ebac item-use event toggles that client's preference. A synchronized timer reapplies local visibility to three native frames every 0.03 seconds. A living selected own hero with 30 native storage slots is required; selecting away, Escape or match end clears the preference. No item/equipment mutation, unit order, selection forcing or sync message is issued by the guard. Trigger/timer allocation and event registration run on all clients.

Frame names were verified in the user's installed `UI/FrameDef/UI/InventoryBar.fdf`: SimpleEquipmentInventoryPanel, SimpleEquipmentPanel and EquipmentPanelBackdrop. Local diagnostic extraction resides under ignored `test-results/native-inventory-ui`; no Blizzard UI asset is bundled into the map. The installed common.j confirms the frame lookup and visibility natives. Native frame availability/context, whether the engine's panel controller accepts direct visibility restoration, and item/name/slot refresh after another client's action remain live-test assumptions. A missing core frame disables the guard and shows an owner-only message on backpack use; native inventory behavior remains active.

## Verification and limitations

- Eight regression checks passed: simulated four-client independent toggle/restoration, non-backpack/nonhero isolation, selection close, missing-frame fallback, match-end close, required capacity, and no local handle allocation in initialization.
- These tests execute the straight-line generated JASS handlers translated into Python with native UI boundaries. They inject the reported native hide behavior. They prove our script decisions, not the game's native UI implementation or binding.
- Installed-editor API syntax and package archive/readback passed; package installed. Live editor/gameplay/multiplayer/endurance gates remain pending.
- Full suite: 120 tests, six failures and four errors. Several checks still expect superseded backpack identity/progression APIs or earlier loot/scaling values. None is treated as passing. Raw output: `test-results/backpack-panel-regressions.txt`.

- ERROR: test_crownlands_expansion (unittest.loader._FailedTest.test_crownlands_expansion)
- ERROR: test_backpack_preserves_native_identity_and_usable_flags (test_equipment.EquipmentRecords.test_backpack_preserves_native_identity_and_usable_flags)
- ERROR: test_hero_items_progression (unittest.loader._FailedTest.test_hero_items_progression)
- ERROR: test_race_mining_buildings (unittest.loader._FailedTest.test_race_mining_buildings)
- FAIL: test_generated_runtime_uses_boss_plan_and_keeps_warning_in_hud_until_resolution (test_boss_mechanics.BossMechanics.test_generated_runtime_uses_boss_plan_and_keeps_warning_in_hud_until_resolution)
- FAIL: test_verified_campaign_heroes_have_native_skills_ranks_and_signatures (test_campaign_hero_expansion.CampaignHeroExpansion.test_verified_campaign_heroes_have_native_skills_ranks_and_signatures)
- FAIL: test_later_bosses_give_personal_legendary_catalog_items_but_old_relics_stay (test_endless_waves.EndlessCampaignWaves.test_later_bosses_give_personal_legendary_catalog_items_but_old_relics_stay)
- FAIL: test_wave_scaling_tracking_and_debug_reach_are_kept_for_endless_spawns (test_endless_waves.EndlessCampaignWaves.test_wave_scaling_tracking_and_debug_reach_are_kept_for_endless_spawns)
- FAIL: test_enemy_loot_uses_explicit_elite_tiers_and_preserves_probability_bands (test_enemy_bounties.EnemyBounties.test_enemy_loot_uses_explicit_elite_tiers_and_preserves_probability_bands)
- FAIL: test_backpack_uses_native_extended_inventory_abilities (test_pipeline.ArchiveRegression.test_backpack_uses_native_extended_inventory_abilities)

## Exact live check

Use this candidate on every client. With each player's hero selected: open P1's bag, open P2's bag, verify both display their own item/name data; close P2 and confirm P1 stays open. Buy/equip/sell one ordinary item per player; select a worker or shop and then reselect/reopen the hero; test normal inventory full and bag full. Repeat P1/P2/P3/P4 in varying order. If the guard-unavailable message appears, record it and do not mark the fix verified. If panels remain open but names/items switch to another hero, direct visibility is insufficient and this candidate needs revision before further gameplay acceptance.

Final review: independent reviewer found no synchronized gameplay mutation or local handle allocation. Escape close now clears only the triggering client's preference and has a regression check. Final package KLS-D-2aac020fb1 passed eight focused tests and compilation/archive/installation. Full suite before docs synchronization: 121 tests, 13 failures and four errors, including seven new-build record failures/subtests; build-record checks are rerun after updating docs. Other failures are listed above. Final raw output: test-results/backpack-panel-final-regressions.txt. Native panel rendering/binding remains unverified.

Live editor attempt, 2026-09-30: copied the exact package to ignored `build/Backpack-Test-KLS-D-2aac020fb1.w3m`; its SHA-256 matched the package above. World Editor opened it and Test Map launched Warcraft III. The editor requested automatic starting locations, accepted only in this disposable copy. The editor also displayed `Referencing unknown database field: 'netsafe' (UI/SkinMetaData.slk)`. Computer Use then returned `Computer Use app approval timed out` while attempting to inspect Warcraft III. No in-game backpack behavior or multiplayer result was observed. The versioned package was not edited. A focused rerun with `PYTHONPATH=tests` passed all 22 backpack, multiplayer UI safety, market control, and build-record tests; `git diff --check` passed.
