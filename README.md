# The King's Last Stand

**A cooperative, 40-wave Warcraft III Definitive Edition defense RPG.**

Players command distinct heroes and their own human kingdom armies, build and upgrade four personal bases, and hold the King's Road against a changing undead and demonic invasion. King Aldric and his castle are the shared objective. The game combines hero progression and equipment with worker economy, construction, towers, boss fights, and personal boss rewards.

## Project status

Current development build: **KLS-D-a2dae2be8c**.

- Map: `dist/KLS-D-a2dae2be8c-Development.w3m`
- SHA-256: `e86d0c0e1696897d8727d243bf6bc92bd6f5ce8ca6b6b39a8d24ae38668dbd9d`
- Installed test map: `C:\Users\asphy\Documents\Warcraft III\Maps\TheKingsLastStand\KLS-D-a2dae2be8c-Development.w3m` (hash matches).
- Build manifest: dist/build-manifest.json

This build fixes the recipe delivery branch that showed both “Craft complete” and “Craft failed” and could refund the fee after a successful craft. Package readback and installed-editor API syntax passed; the full regression suite is recorded in CHANGELOG.md. The prior test map was closed and archived before this build was installed. The earlier user-reported World Editor Test Map pass remains attributed only to `KLS-D-fd638ddcf5`. Save/reopen, this build's own Test Map and Custom Game checks, live recipe interaction, multiplayer, and 40-wave endurance remain pending, so this stays a development build.

Next human check: open the installed `KLS-D-a2dae2be8c-Development.w3m` in Custom Game, complete one recipe, and confirm it shows exactly one successful craft notification with no failure/refund message. Other previously reported shop, equipment, and UI behaviors still need exact-build gameplay checks.

## Start here

- AGENTS.md — instructions and invariants for future agents.
- docs/GAME-VISION.md — why the game exists and the experience to protect.
- docs/GAMEPLAY-SPEC.md — match, economy, buildings, landscape, and player systems.
- docs/HEROES-AND-ABILITIES.md — all 17 heroes, their native skills, and custom signature spells.
- docs/HERO-THEMED-EXPANSION.md — proposed Forsaken Kingdom heroes, personal retinues, and hero-linked buildings/army research.
- docs/ITEMS-AND-EQUIPMENT.md — Forsaken Kingdom backpack, quality progression, effects, books, recipes, relics, and shops.
- docs/ITEM-CATALOG.md — all generated catalog entries with rawcodes, prices, slots, stats, and effects.
- docs/WAVES-AND-BOSSES.md — chapter plan, enemy roster, boss mechanics, and scaling.
- docs/WAVE-ROSTER-CATALOG.md — every generated wave's unit rawcodes, in spawn order.
- docs/TECHNICAL-ARCHITECTURE.md — source, build pipeline, Warcraft data provenance, packaging, and diagnostics.
- docs/ROADMAP-AND-ACCEPTANCE.md — required order and pass/pending evidence.
- docs/DECISIONS-AND-OPEN-ISSUES.md — preserved decisions and unresolved reports.
- docs/PROGRESS-LEDGER.md — chronological implementation and verification record.
- CHANGELOG.md — one build-ID and SHA-tagged change record for each package.
- docs/PLAYER-GUIDE.md — current diagnostic controls and playtest flow.
- docs/superpowers/plans/2026-09-28-hero-items-progression-and-pool.md — approved recent scope for attributes, recipes, level-100 spells, healing pool, and longer breaks.

## Build and test

Use a Windows machine with Warcraft III: Reforged / Definitive Edition and its World Editor installed. A clean checkout must first prepare the API extractor prerequisites documented in docs/TECHNICAL-ARCHITECTURE.md, then extract the API declarations and object tables from that installation. Do not copy another editor version's API tables into the project. The CascLib DLL/listfile bootstrap and configurable game path are known clean-checkout setup gaps; this snapshot does not claim to be a one-command bootstrap.

From the repository root, run:

    python -B tools/extract_game_api.py
    python -B tools/build_map.py
    python -B -m unittest discover -s tests -v

To install the package-proven current development build into the local Custom Game test folder:

    python -B tools/build_map.py --install-test-map

Installation is local to that computer. Follow docs/PLAYER-GUIDE.md and docs/ROADMAP-AND-ACCEPTANCE.md for the exact human-run engine check.

## Repository contents

- source/ contains authoritative JASS runtime modules and the DE blank-map template.
- tools/ contains the deterministic map builder, data generators, packer, API extractor, and a licensed MPQ reader.
- tests/ contains focused regression tests.
- backups/Blank-DE.w3m is the pinned user-supplied blank starter map used by the builder.
- dist/ contains one current build-ID-named development map and its manifest. Replaced versions are archived locally under backups/development-builds/ and remain recoverable from Git history.

The user-installed API/object tables, generated builds, temporary test logs, old diagnostic maps, and compiled helper binaries are not checked in. A future builder extracts the required references from the installed game and records their provenance in the build manifest.
