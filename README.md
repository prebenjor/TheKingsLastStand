# The King's Last Stand

**A cooperative, 40-wave Warcraft III Definitive Edition defense RPG.**

Players command distinct heroes and their own human kingdom armies, build and upgrade four personal bases, and hold the King's Road against a changing undead and demonic invasion. King Aldric and his castle are the shared objective. The game combines hero progression and equipment with worker economy, construction, towers, boss fights, and personal boss rewards.

## Project status

This repository starts with development build **KLS-D-fd638ddcf5**. Its map is available at:

- dist/DIAGNOSTIC-KLS-D-fd638ddcf5.w3m
- SHA-256: 48c960e485bd9c81154c13c4ce73ec0b33ac21059572a81a3add8436a268aafd
- Build manifest: dist/build-manifest.json

The project passes 55 source-level regression tests, syntax compilation against declarations extracted from the installed Warcraft III, and MPQ package inventory/readback. This does **not** establish a verified release. The current build has not passed the required World Editor save/reopen/Test Map cycle, exact-build Custom Game startup, complete live gameplay, 2/3/4-player network checks, or 40-wave two- and four-player endurance runs.

The user has reported that shop windows can appear empty or as text lists, purchased gear cannot be equipped, and UI panels can overflow. Source stock/catalog logic exists, but those interactions are not considered fixed until tested with this exact build in Warcraft III.

## Start here

- AGENTS.md — instructions and invariants for future agents.
- docs/GAME-VISION.md — why the game exists and the experience to protect.
- docs/GAMEPLAY-SPEC.md — match, economy, buildings, landscape, and player systems.
- docs/HEROES-AND-ABILITIES.md — all 15 heroes, their native skills, and custom signature spells.
- docs/ITEMS-AND-EQUIPMENT.md — Forsaken Kingdom backpack, quality progression, effects, books, recipes, relics, and shops.
- docs/ITEM-CATALOG.md — all generated catalog entries with rawcodes, prices, slots, stats, and effects.
- docs/WAVES-AND-BOSSES.md — chapter plan, enemy roster, boss mechanics, and scaling.
- docs/WAVE-ROSTER-CATALOG.md — every generated wave's unit rawcodes, in spawn order.
- docs/TECHNICAL-ARCHITECTURE.md — source, build pipeline, Warcraft data provenance, packaging, and diagnostics.
- docs/ROADMAP-AND-ACCEPTANCE.md — required order and pass/pending evidence.
- docs/DECISIONS-AND-OPEN-ISSUES.md — preserved decisions and unresolved reports.
- docs/PROGRESS-LEDGER.md — chronological implementation and verification record.
- docs/PLAYER-GUIDE.md — current diagnostic controls and playtest flow.
- docs/superpowers/plans/2026-09-28-hero-items-progression-and-pool.md — approved recent scope for attributes, recipes, level-100 spells, healing pool, and longer breaks.

## Build and test

Use a Windows machine with Warcraft III: Reforged / Definitive Edition and its World Editor installed. A clean checkout must first prepare the API extractor prerequisites documented in docs/TECHNICAL-ARCHITECTURE.md, then extract the API declarations and object tables from that installation. Do not copy another editor version's API tables into the project. The CascLib DLL/listfile bootstrap and configurable game path are known clean-checkout setup gaps; this snapshot does not claim to be a one-command bootstrap.

From the repository root, run:

    python -B tools/extract_game_api.py
    python -B tools/build_map.py
    python -B -m unittest discover -s tests -v

To install the package-proven diagnostic into the local Custom Game map folder:

    python -B tools/build_map.py --install-diagnostic

Installation is local to that computer. Follow docs/PLAYER-GUIDE.md and docs/ROADMAP-AND-ACCEPTANCE.md for the exact human-run engine check.

## Repository contents

- source/ contains authoritative JASS runtime modules and the DE blank-map template.
- tools/ contains the deterministic map builder, data generators, packer, API extractor, and a licensed MPQ reader.
- tests/ contains focused regression tests.
- backups/Blank-DE.w3m is the pinned user-supplied blank starter map used by the builder.
- dist/ contains the specific development map handed off by this repository snapshot.

The user-installed API/object tables, generated builds, temporary test logs, old diagnostic maps, and compiled helper binaries are not checked in. A future builder extracts the required references from the installed game and records their provenance in the build manifest.
