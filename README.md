# The King's Last Stand

**A cooperative, 40-wave Warcraft III Definitive Edition defense RPG.**

Players command distinct heroes and their own human kingdom armies, build and upgrade four personal bases, and hold the King's Road against a changing undead and demonic invasion. King Aldric and his castle are the shared objective. The game combines hero progression and equipment with worker economy, construction, towers, boss fights, and personal boss rewards.

## Project status

Current development build: **KLS-D-2780b4380e**.

- Map: `dist/KLS-D-2780b4380e-Development.w3m`
- SHA-256: `30e1fa1a9c5e6415131f2aea1f200046504e93dbe3dab9de504482eb24641a33`
- Build manifest: dist/build-manifest.json

Package inventory/readback, JASS syntax against the installed editor API, and 66 source-level regression tests pass for the current build. It adds Human Ilastar and the Forsaken Paladin to the 15 existing hero choices, with installed-data-verified skill ranks and custom signatures. It uses the native `ebua` Forsaken backpack record and retains visible combat gold rewards, movable/sellable normal gear, and one-second percentage spring healing. These in-game interactions remain pending. The user-reported World Editor Test Map pass applies to the earlier build `KLS-D-fd638ddcf5`; it remains a pass for that build. The current build still needs its own editor/game checks, live feature proof, 2/3/4-player sessions, and 40-wave endurance runs, so it remains a development build.

The current map is installed at `Documents/Warcraft III/Maps/TheKingsLastStand/KLS-D-2780b4380e-Development.w3m`. Warcraft III process PID 61400 is open, but the current build has not yet been launched. The UI-control helper failed before it could inspect the game window; see the roadmap for the one requested manual check.

The user has reported that shop windows can appear empty or as text lists, purchased gear cannot be equipped/sold, and UI panels can overflow. This build uses the native backpack object identity and current gear flags, but those interactions are not considered fixed until tested with this exact build in Warcraft III.

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
