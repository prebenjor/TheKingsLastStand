Current package and full-suite evidence have moved to [AUDIT-COMPLETION.md](AUDIT-COMPLETION.md). The repair snapshot below is historical; its original counts are retained.

# Multiplayer UI repair — 2026-09-29

## Multiplayer UI repair candidate — 2026-09-29

Current DEVELOPMENT package: **KLS-D-c98ba28f73**.
- Artifact: `dist/KLS-D-c98ba28f73-Development.w3m`.
- SHA-256: `41c1a2c4eee98833435cf22f57998e2eea75ae7128f7f8278c840a1c69158973`.
- Installed in `Documents/Warcraft III/Maps/TheKingsLastStand/`; prior package archived.
- Ready, difficulty and stat-choice frames/events now initialize on every client in identical player order. Only visibility is local; only the triggering player sends a synchronized click.
- New static UI safety regressions passed 3/3 after failing on both original initialization paths. Installed-API syntax and archive readback passed. Full suite: 113 tests, 7 failures and 4 errors; see `docs/MULTIPLAYER-UI-REPAIR.md`. No multiplayer fix is claimed verified.
- Next check: in a two-player game, have Player 2 vote first, undo, then let both players vote to start one wave. Repeat with Player 2 casting the final vote. Check stat choices and difficulty on both clients.
- Backpack cross-player panel closing remains unresolved. No native storage, equipment or shop-transfer behavior was changed in this repair.

## Findings and limits

The original vote and stat initialization allocated frames and event handles inside GetLocalPlayer branches. Player-indexed frame arrays consequently described different allocations on different machines; observers skipped those allocations entirely. Both paths now allocate identically. Click handlers use GetTriggerPlayer and send sync data only on that player's client. This corrects a concrete synchronization hazard; without an engine reproduction it is not proof of the user's reported crash cause.

Native backpack activation is handled by the installed ebac/AIni/AEqu/ASde system. KLS_PackUsed only logs storage size; no custom open/close implementation was found. The installed common.j exposes storage/equipment natives but no dedicated per-player panel open/close native. Do not change inventory or ability state inside GetLocalPlayer to try to hide the symptom. The backpack issue needs an exact-build multiplayer reproduction and investigation of the native UI before a supported workaround can be chosen.

Existing purchase transfers still run through synchronized shop events and deferred timers. No specific remaining shop symptom has yet been supplied beyond the backpack interaction; clarification is pending.

## Full suite failures

These checks are not waived. Several expect superseded progression APIs, Anya's backpack, loot values or old build documentation. The full suite is not green. Raw output: test-results/multiplayer-ui-regressions.txt.

- ERROR: test_crownlands_expansion (unittest.loader._FailedTest.test_crownlands_expansion)
- ERROR: test_backpack_preserves_native_identity_and_usable_flags (test_equipment.EquipmentRecords.test_backpack_preserves_native_identity_and_usable_flags)
- ERROR: test_hero_items_progression (unittest.loader._FailedTest.test_hero_items_progression)
- ERROR: test_race_mining_buildings (unittest.loader._FailedTest.test_race_mining_buildings)
- FAIL: test_generated_runtime_uses_boss_plan_and_keeps_warning_in_hud_until_resolution (test_boss_mechanics.BossMechanics.test_generated_runtime_uses_boss_plan_and_keeps_warning_in_hud_until_resolution)
- FAIL: test_current_package_acceptance_references_match_the_manifest (test_build_changelog.BuildChangelog.test_current_package_acceptance_references_match_the_manifest)
- FAIL: test_verified_campaign_heroes_have_native_skills_ranks_and_signatures (test_campaign_hero_expansion.CampaignHeroExpansion.test_verified_campaign_heroes_have_native_skills_ranks_and_signatures)
- FAIL: test_later_bosses_give_personal_legendary_catalog_items_but_old_relics_stay (test_endless_waves.EndlessCampaignWaves.test_later_bosses_give_personal_legendary_catalog_items_but_old_relics_stay)
- FAIL: test_wave_scaling_tracking_and_debug_reach_are_kept_for_endless_spawns (test_endless_waves.EndlessCampaignWaves.test_wave_scaling_tracking_and_debug_reach_are_kept_for_endless_spawns)
- FAIL: test_enemy_loot_uses_explicit_elite_tiers_and_preserves_probability_bands (test_enemy_bounties.EnemyBounties.test_enemy_loot_uses_explicit_elite_tiers_and_preserves_probability_bands)
- FAIL: test_backpack_uses_native_extended_inventory_abilities (test_pipeline.ArchiveRegression.test_backpack_uses_native_extended_inventory_abilities)

## Reproduction checklist

1. Confirm the same candidate build ID on all clients.
2. During preparation, P2 votes first, then cancels; countdown continues and vote tally changes once. P1 votes and P2 supplies the final vote; one wave starts. Reverse voting order next break.
3. Each player votes difficulty and spends a stat point independently; other players' choices and points remain unchanged.
4. P1 opens their backpack, then P2 opens theirs. Repeat with three/four players; record whether another panel closes or switches hero. Check whether ordinary hero selection triggers it as well.
5. Buy, equip and sell one ordinary item per player; check full six-slot inventory and full bag separately. Record the exact failing action and use -gear diagnostics.

No Editor automation or live multiplayer run occurred in this session.

Final focused verification: UI safety 3/3, existing shop controls 9/9, build/changelog references 2/2 passed. The full-suite build-reference failure is resolved by the documentation update; the other failures remain pending. Workspace and installed SHA-256 match.

Backpack follow-up: candidate KLS-D-d213c3b353 now contains a local native-panel visibility guard; see [BACKPACK-PANEL-REPAIR.md](BACKPACK-PANEL-REPAIR.md). Earlier unresolved notes above describe the prior candidate.
