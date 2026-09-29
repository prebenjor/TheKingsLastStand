# The King's Last Stand

**A cooperative Warcraft III Definitive Edition defense RPG with a 40-wave campaign and endless crossover assaults.**

Players command distinct heroes and their own race-matched workers, buildings, and armies, build and upgrade four personal bases, and hold the King's Road against a changing undead and demonic invasion. King Aldric and his castle are the shared objective. The game combines hero progression and equipment with worker economy, construction, towers, boss fights, and personal boss rewards.

## Project status

Current development build: **KLS-D-921cb74251**.

- Map: `dist/KLS-D-921cb74251-Development.w3m`
- SHA-256: `2f22ad15e2f82e2a68cc5c389dc3572d9eae495447883c014643920071f87568`
- Installed as the sole project map in `Documents/Warcraft III/Maps/TheKingsLastStand/`; installed hash matches the package. Editor Test Map, Custom Game, purchase/crafting behavior, gameplay, multiplayer and endurance checks remain pending.
- Build manifest: dist/build-manifest.json

World Editor terrain and map dressing are preserved in `source/authored-map/editor-layer.zip`. After editing and saving the current build in World Editor, capture its six supported visual layers with `python -B tools/capture_authored_map.py --map "<saved-map.w3m>"`; the capture rejects a map with a different build ID. See `BUILDING.md` for the workflow and limitations.

This package carries the Crownlands settlements, four-race companies, hero progression and custom content forward. Each gained hero level now adds +3 to that hero's installed primary damage stat and +1 to each other stat; the normal skill point still funds a spell upgrade or one of the three separate +3 stat buttons. Native hero growth is disabled for selectable heroes so the requested automatic values are not doubled. The Night Elf build menu now uses Ancient of War and Hunter's Hall as its Tier One Barracks and upgrade building, removing a circular prerequisite that blocked Tree of Ages. The four Halls use distinct race buildings, and each constructed Foundry exposes its own owner-only Legendary recipe while retaining the company upgrade. Crafted patterns return to their selling building. It also routes boss relics and story items through a guarded personal delivery service: failed item creation is queued per owner and retried, while full inventories receive a visible owner-bound item at their base. `-gear` audits six normal inventory slots, occupied backpack positions and nine equipment slots, showing item type, catalog slot and owner marker. If a market equip attempt fails, its diagnostic also records buyer type/owner/life state, free normal slots, backpack occupancy, where the item is, item owner/type, catalog family/slot, and retry attempt; use `-gear` and `-diag` together to capture the transaction. `-diag` retains ERROR/FATAL/WARN messages in a separate rolling buffer, displays the latest eight after routine logs roll over, and counts each logged ERROR once across unit, scenery, item, recipe, and retry failures. Optional scenery, effects, reinforcements, story spawns, and Undead mine conversion use contextual checked-spawn diagnostics; optional failures do not end the match. Core setup and wave spawns remain fatal. The Undead Temple explicitly uses Warcraft's Temple of the Damned icon, Undead and Night Elf players begin with their own Haunted or Entangled Gold Mine holding 1,000,000 gold, and per-base lumber stands are placed in closer rows south of each hall. Keeper of the Grove and Faelor use tree-free Treant signatures. Gear prices, rarity tiers, recipes, endless wave rosters, kill gold, XP, Sacred Aura rank values, and drop probabilities remain as previously documented. The last full regression run passed 147/147 for an earlier build; automated tests were not run for this change. The current package build/readback and installed-editor API syntax passed. The log collector includes severity-tagged engine warnings and spawn/load failures in both `findings.txt` and the structured JSON report.

The installed Warcraft III version is `3.0.0.24268`; the 13 pinned extracted API/object/icon data tables remain unchanged. The generic `ebac` Backpack now replaces Anya-specific `ebua`, keeping native storage and equipment abilities; the multiplayer panel interaction needs a two-player check. Editor save/reopen, Test Map, Custom Game, gameplay, multiplayer and endurance remain pending. The earlier Test Map pass remains attributed to `KLS-D-fd638ddcf5`. Use docs/ROADMAP-AND-ACCEPTANCE.md for current-build acceptance and docs/CROWNLANDS-EXPANSION.md for implementation details.

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
