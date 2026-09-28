# Instructions for future agents

This file is the first read for anyone continuing The King's Last Stand. Preserve the full co-op defense RPG in the linked design documents. Do not narrow it to a wave demo, a single-player toy, or a generic tower-defense map.

## Read before changing anything

1. README.md for repository status and quick commands.
2. docs/GAME-VISION.md and docs/GAMEPLAY-SPEC.md for the approved player experience and map layout.
3. docs/HEROES-AND-ABILITIES.md, docs/HERO-THEMED-EXPANSION.md, docs/ITEMS-AND-EQUIPMENT.md, docs/ITEM-CATALOG.md, and docs/WAVES-AND-BOSSES.md for feature detail. The expansion proposal is not approved until the user accepts its recommended direction.
4. docs/TECHNICAL-ARCHITECTURE.md for build provenance and supported workflow.
5. docs/ROADMAP-AND-ACCEPTANCE.md and docs/PROGRESS-LEDGER.md for what is actually proven.
6. docs/DECISIONS-AND-OPEN-ISSUES.md before changing a user-approved decision or resolving a reported bug.
7. docs/superpowers/plans/2026-09-28-hero-items-progression-and-pool.md for the latest approved attribute gear, crafting, spell-rank, fountain, and break-timing work.

## Product rules

- The game is a 2–4 player cooperative human-kingdom defense RPG with individual player armies and heroes. Players do not receive shared unit control.
- Preserve the 40-wave, four-chapter structure and the bosses on waves 10, 20, 30, and 40.
- Preserve the user's battlefield: a broad north-to-south road, the undead/demon approach from the north, an open central gate in the northern wall, four separate player plots aligned across one horizontal row, King Aldric's castle at the defense line, and the shared market farther south.
- Keep the 15-choice hero selector before the match proper. Duplicate choices are allowed. All heroes retain human workers and building access.
- The Forsaken Kingdom backpack is the intended native equipment system: 30 storage spaces, nine equipment slots, and one backpack carried in normal inventory. Never silently substitute a custom 18-slot dialog.
- Keep gear personal, preserve ownership, and make buying, equipping, crafting, and rewards safe when inventory is full.
- The king is a shared defense objective. Healing and upgrades are purchased at his castle with the acting player's personal gold and lumber.
- Keep Definitive Edition rendering and use native installed game objects, portraits, icons, abilities, and models where possible.
- Build stays labelled DEVELOPMENT until the editor save/reopen/Test Map, Custom Game startup, live gameplay, multiplayer, and endurance acceptance gates have actually passed.

## Source-of-truth order

1. A new explicit user decision takes precedence over earlier decisions.
2. Approved design requirements are in the design documents linked above.
3. Current implementation details are in source/ and tools/. Source is evidence of code, not proof of a working in-game feature.
4. docs/PROGRESS-LEDGER.md and the build manifest are evidence for the exact build and checks performed.
5. Screenshots and older build logs are observations tied to their specific build IDs. Never silently treat old screenshots as proof about a newer build.

If design and source differ, record the gap in docs/DECISIONS-AND-OPEN-ISSUES.md and docs/PROGRESS-LEDGER.md. Do not rewrite the design to match an incomplete implementation.

## Engineering rules

- The only supported build entry point is:

      python -B tools/build_map.py

- Use `python -B tools/build_map.py --install-test-map` to install the package-proven current development build in the dedicated Warcraft III test folder. The old `--install-diagnostic` option remains a compatibility alias only.
- The build derives compiled JASS and editable trigger data from the same runtime modules. Change source modules and generators, not generated source/war3map.j or build output.
- Keep the explicit module order in tools/pipeline.py. Do not reintroduce source-file auto-discovery or one-off patch scripts.
- Keep the known Definitive Edition blank starter unchanged. The builder verifies its pinned hash and metadata version and stops on unknown input.
- tools/reference/installed is machine-local output from the user's installed Warcraft III. Do not check in installed SLK/API tables or Blizzard script declarations. Documented extraction and provenance checks are part of the build contract.
- Do not deprotect or reuse a protected third-party map. This project is the user's new map based on the blank DE starter.
- All synchronized gameplay changes must be deterministic and run for all players. GetLocalPlayer() may change display/camera only; it must not decide resources, item ownership, damage, wave state, or unit creation.
- Add regression tests for changed archive, JASS, editor-source, hero, inventory, economy, wave, or multiplayer-state behavior. A passing syntax check is not engine compatibility proof.
- Use the captured diagnostic logs and full KLS diagnostic output to investigate missing objects. Tie each conclusion to the current immutable build ID and map hash.
- Keep output names versioned and preserve an editor-open file. Do not overwrite/delete the file World Editor currently has open.
- Update the docs and progress ledger in the same change as behavior changes. Record build ID, SHA-256, exact checks, failures, and the single next human-run check.
- Maintain root `CHANGELOG.md`: every newly packaged map gets one dated, immutable build-ID section with its package SHA-256, user-visible changes, verification evidence, and pending engine checks. Update the entry as part of that build's source change. A changelog section must never label a development map as a release.

## Pull request and handoff checklist

- Link the user-visible feature to the relevant requirements section.
- State which tests were run and which engine checks remain pending.
- Update catalog tables from tools/equipment_catalog.py when catalog data changes.
- Keep known issues visible until current-build evidence resolves them.
- Do not call any artifact a verified release while any release gate is pending.
