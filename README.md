# The King's Last Stand

## Sharing the current plan with another agent

Start with the [September 30 friend-agent handoff](docs/FRIEND-AGENT-HANDOFF-2026-09-30.md). It includes required Markdown reading, strict visual/preservation boundaries, the latest town/story decisions, gameplay contracts, hero/building IDs, AI work, reported bugs and their evidence status, source navigation and ordered acceptance checks. Send the latest **saved and closed Terrain map separately**: the current human edits in `build/` are not included in a Git checkout or the documentation bundle.

## World Editor workshop

The [wc3-forge MCP connection](docs/WC3-FORGE-CONNECTION.md) is now configured and responds with 153 tools. Opening the archived trial map fails on its native W3I-39 metadata; a forge compatibility fix is required before editing through it. The latest saved Terrain map is fully preserved and unchanged.

Latest authored [layout/story revision](docs/EDITOR-LAYOUT-REVISION.md): Orc village removed, gates replaced by cliffs, troll camp added. Documentation is updated; runtime integration awaits the saved/closed editor handoff. See the [wc3-forge assessment](docs/WC3-FORGE-ASSESSMENT.md) for the potential MCP authoring workflow.

Follow the approved [eight-chapter Editor Workshop](docs/EDITOR-WORKSHOP.md), starting with Chapter 0 on the current Terrain copy. The [handoff protocol](docs/EDITOR-WORKSHOP-HANDOFF.md) preserves a native baseline and reports terrain, reference moves, object/rank fields and trigger changes before source integration. Chapter 0 awaits the user's save/close; the gameplay package remains KLS-D-68303d69bf.

## Saved terrain and editor layout — 2026-09-30

Current DEVELOPMENT package: **KLS-D-68303d69bf**.

- Artifact: `dist/KLS-D-68303d69bf-Development.w3m`; SHA-256: `baa024fd2b23ec03ef0ccbb6de5a2345a292fe82a4a03f9345b73c95b4d0b1c3`. Installed copy matches in the established Warcraft III test folder.
- The user's saved terrain is captured in `source/authored-map/editor-layer.zip`, with the original archived locally. No runtime grass, road, plot or hero-hub texture painting overwrites it.
- Open `build/KLS-D-68303d69bf-Development-Terrain.w3m` for terrain editing: it includes 85 visible layout references for shops, towns, quest sites, hero hub, castle/spring and provisional bases. References use Neutral Extra and are removed before runtime gameplay spawns. Moving a reference does not change source-controlled gameplay coordinates.
- 188 automated tests passed; installed-API JASS syntax, archive readback and installed/package hashes passed.
- See [editor layout workflow](docs/EDITOR-LAYOUT.md). All six captured art layers are identical in both packages. Current editor visual/round-trip and game/multiplayer/endurance checks remain pending; retain the earlier successful Test Map record.

## Historical audit completion Development build — 2026-09-30

Historical DEVELOPMENT package: **KLS-D-8048eea39b**.

- Artifact: `dist/KLS-D-8048eea39b-Development.w3m`; SHA-256: `6759047254a8fd3bef830e32af7af4f8804fe732237a25b87957004138664247`.
- Installed in `Documents/Warcraft III/Maps/TheKingsLastStand/` with a matching hash; previous builds archived outside the test folder.
- Completed the seven source audit gaps: tree-free ranked summons, nonmodal talents, preparation-scoped Ready votes, participating/retryable escort, persistent town perks, personal company research and 50 recruit powers, plus corrected power projections.
- 181 automated tests passed. Installed-API JASS syntax and MPQ readback passed. Independent review findings were fixed and rechecked.
- Current-build engine, multiplayer and endurance checks remain pending. Earlier successful Test Map `KLS-D-fd638ddcf5` remains credited.
- Details and next exact-build check: [audit completion](docs/AUDIT-COMPLETION.md); full generated [company powers/research](docs/COMPANY-RESEARCH-AND-POWERS.md).


## Previous backpack repair candidate — 2026-09-30

Historical DEVELOPMENT package: **KLS-D-2aac020fb1**.
- Artifact: `dist/KLS-D-2aac020fb1-Development.w3m`.
- SHA-256: `0b71c26a3353d088cedb376d0d27d597039b9662687d475c60569c732fcb3a9d`.
- Installed in `Documents/Warcraft III/Maps/TheKingsLastStand/`; prior package archived.
- Ready, difficulty and stat-choice frames/events now initialize on every client in identical player order. Only visibility is local; only the triggering player sends a synchronized click.
- New static UI safety regressions passed 3/3 after failing on both original initialization paths. Installed-API syntax and archive readback passed. Full suite: 113 tests, 7 failures and 4 errors; see `docs/MULTIPLAYER-UI-REPAIR.md`. No multiplayer fix is claimed verified.
- Next check: in a two-player game, have Player 2 vote first, undo, then let both players vote to start one wave. Repeat with Player 2 casting the final vote. Check stat choices and difficulty on both clients.
- Backpack panel visibility now follows an owner-only local open preference; native item use and the 30-slot bag/nine equipment slots remain active. Eight script-boundary regressions pass. Native frame binding, selection refresh, panel contents and simultaneous multiplayer interaction remain unverified. See docs/BACKPACK-PANEL-REPAIR.md.

**A cooperative Warcraft III Definitive Edition defense RPG with a 40-wave campaign and endless crossover assaults.**

Players command distinct heroes and their own race-matched workers, buildings, and armies, build and upgrade four personal bases, and hold the King's Road against a changing undead and demonic invasion. King Aldric and his castle are the shared objective. The game combines hero progression and equipment with worker economy, construction, towers, boss fights, and personal boss rewards.

## Previous package status — superseded by the candidate above

Previous development build: **KLS-D-4e6ae863df**.

- Map: `dist/KLS-D-4e6ae863df-Development.w3m`
- SHA-256: `aa6276d4f1c2b4ca1b8f97562fee8c1a7bf52169300e7cca3f406036829de6d6`
- Installed as the sole project map in `Documents/Warcraft III/Maps/TheKingsLastStand/`; installed hash matches the package. Editor Test Map, Custom Game, purchase/crafting behavior, gameplay, multiplayer and endurance checks remain pending.
- Build manifest: dist/build-manifest.json

World Editor terrain and map dressing are preserved in `source/authored-map/editor-layer.zip`. After editing and saving the current build in World Editor, capture its six supported visual layers with `python -B tools/capture_authored_map.py --map "<saved-map.w3m>"`; the capture rejects a map with a different build ID. See `BUILDING.md` for the workflow and limitations.

This package carries the Crownlands settlements, four-race companies, hero progression and custom content forward. Heroes start at level 1 with one skill point per gained level; they choose a spell rank or one unranked +3 STR/AGI/INT option, with no automatic attribute growth or spell-rank advancement. A match-wide Easy/Normal/Hard/Very Hard vote resolves before wave 1, and each next wave can start early only after every active player votes Ready. The 50-second normal and 180-second boss countdowns remain the fallback. All four starting mines hold 1,000,000 gold while Undead and Night Elf keep their Haunted/Entangled mine identity. Enemy equipment drops are intentionally scarce: Normal waves have no gear roll; elites have a 1% Common/Uncommon chance; bosses grant personal rarity-milestone equipment. The generated item/slot power report currently has no rarity outliers or tier-order warnings. See the latest build section in CHANGELOG.md for package hash, checks and pending engine verification.

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
