# The King's Last Stand

**A cooperative Warcraft III Definitive Edition defense RPG with a 40-wave campaign and endless crossover assaults.**

Players command distinct heroes and their own race-matched workers, buildings, and armies, build and upgrade four personal bases, and hold the King's Road against a changing undead and demonic invasion. King Aldric and his castle are the shared objective. The game combines hero progression and equipment with worker economy, construction, towers, boss fights, and personal boss rewards.

## Project status

Current development build: **KLS-D-f873a5b24f**.

- Map: `dist/KLS-D-f873a5b24f-Development.w3m`
- SHA-256: `30fd0594806fd7e2cf9294b6750bb6ecc6e3855d9261852e01ab03fbe51c6d6e`
- The package is installed at `Documents/Warcraft III/Maps/TheKingsLastStand/KLS-D-f873a5b24f-Development.w3m`; its SHA-256 matches and it is the only project map in the test folder.
- Build manifest: dist/build-manifest.json

This package carries the Crownlands settlements, four-race companies, hero progression and custom content forward. The four Halls now use distinct race buildings, and each constructed Foundry exposes its own owner-only Legendary recipe while retaining the company upgrade. Crafted patterns return to their selling building. It also routes boss relics and story items through a guarded personal delivery service: failed item creation is queued per owner and retried, while full inventories receive a visible owner-bound item at their base. Per-level +3 Strength, Agility, or Intelligence choices are native hero ability plus buttons; the global stat-choice dialog is removed. `-diag` now retains ERROR/FATAL/WARN messages in a separate rolling buffer and displays the latest eight even after ordinary recent logs roll over. Failed random item-drop creation writes item, enemy, position and killer details to the diagnostic log. Optional scenery, effects, reinforcements, story spawns, and Undead mine conversion use contextual checked-spawn diagnostics; optional failures do not end the match. Core setup and wave spawns remain fatal. The Undead Temple inherits the correct Temple parent, race building tooltips describe their actual roles, and Undead and Night Elf players now begin with their own Haunted or Entangled Gold Mine holding 1,000,000 gold. Keeper of the Grove and Faelor now use their tree-free Treant signatures without also showing the unusable tree-target spell. Gear prices now rise from 300 gold for Common to 20,000 for Legendary; hand weapons cost 1.5×, Foundry fees are doubled, and attribute tomes cost 1,000/3,000/8,000. Consumable prices and equipment stats are unchanged. After the preserved 40-wave story, ten installed campaign crossover rosters repeat with live-wave scaling, a five-force wave 49 convergence, a Lady Vashj wave 50 boss, rotating campaign leaders and personal Legendary catalog rewards. King Aldric's death ends the run. Sacred Aura ranks 4/5 retain the generated 38.5%/27.5% and 42%/30% effects for both ability IDs. The current source regression suite passes **130/130**; package readback and installed-editor API syntax pass.

This exact build still needs its own World Editor save/reopen, Test Map, Custom Game, gameplay, multiplayer and endurance checks, so it remains Development. The earlier user-reported Test Map success is a pass for `KLS-D-fd638ddcf5`. Use docs/ROADMAP-AND-ACCEPTANCE.md for current-build acceptance and docs/CROWNLANDS-EXPANSION.md for implementation details.

## Start here

- AGENTS.md — instructions and invariants for future agents.
- docs/GAME-VISION.md — why the game exists and the experience to protect.
- docs/GAMEPLAY-SPEC.md — match, economy, buildings, landscape, and player systems.
- docs/CROWNLANDS-EXPANSION.md — current expansion contract: 192-cell map, four settlements, race-matched workers/buildings, 25 heroes, progression, optional story, twenty-item catalog, and endless campaign waves.
- docs/TERRAIN-DRESSING-GUIDE.md — generated visual reference and practical World Editor guidance for natural paths, grass transitions, boulders, hills, settlement edges, and undead ground.
- docs/HEROES-AND-ABILITIES.md — hero roster, native skills, safe ranks, and signature spells.
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
