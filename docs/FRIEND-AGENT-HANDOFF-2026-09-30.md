# The King's Last Stand — friend-agent handoff

**Snapshot: 30 September 2026. Repository:** <https://github.com/prebenjor/TheKingsLastStand>

This is a portable copy of the current plan, preservation rules, source map and unfinished work. Read this first, then the required documents below. The owner's latest decisions override older plans. Code presence and passing automated checks do not establish that a feature works in Warcraft.

## 1. Brief to give the receiving agent

> Continue The King's Last Stand, a cooperative Warcraft III Definitive Edition defense RPG with personal heroes, armies, economy and equipment. Preserve the owner's manually edited map before rebuilding anything. The owner removed Redtusk Hold, replaced gates with cliffs, added a troll camp and made further terrain/doodad/unit edits. Do not remove their additions or regenerate the deleted village/gates. Integrate deliberate editor changes into the source catalogs and runtime, including actual building positions and facing. Reconcile towns/story/AI with the authored layout. Check reported gameplay issues against the exact current build, carry forward working systems, and document each result. Preserve all four playable races, 25 heroes, personal companies, scarce loot, manual progression and multiplayer independence. Follow this document's reading order, visual boundaries, integration sequence and acceptance gates. Ask about genuinely ambiguous new camp/object behavior while continuing independent work. Do not invent inspection or gameplay results.

## 2. What the owner must send

1. This document and access to the repository. The companion documentation ZIP contains the Markdown plans and existing visual reference images; it does **not** contain the latest edited map or a source checkout.
2. The **latest saved and closed Terrain `.w3m`**, sent separately. Its original path is `C:/Users/asphy/Documents/Warcraft3Maps/kings-last-stand/build/KLS-D-68303d69bf-Development-Terrain.w3m`. `build/` and local backups are ignored by Git. Cloning GitHub alone will not retrieve these latest edits.
3. An overview and close-ups of the castle, cliff passages, moved buildings and troll camp where possible. Screenshots supplement the saved archive; they do not replace it.
4. Any actual native comparison baseline/review report, if one exists. Do not invent one or substitute an older map.

The latest screenshot shows the Terrain file in World Editor. There is **no fresh saved-and-closed confirmation for the latest revision** in this handoff. Earlier save confirmations refer to earlier work. Preserve the open file and wait for the current handoff before capture, replacement or integration.

### Artifact provenance

| Artifact | Status |
|---|---|
| `dist/build-manifest.json` | Authority for the currently packaged build and hashes |
| `dist/KLS-D-68303d69bf-Development.w3m` | Current gameplay package; Development, engine acceptance pending |
| Gameplay SHA-256 | `baa024fd2b23ec03ef0ccbb6de5a2345a292fe82a4a03f9345b73c95b4d0b1c3` |
| `build/KLS-D-68303d69bf-Development-Terrain.w3m` | Human editing copy; latest contents must be supplied separately |
| Original generated Terrain SHA-256 | `89e91629ddaa0c1534114f0a2d033cdb00da02924d644129bd5b02d5ed0b48c1`; **before** subsequent human edits, not their current hash |
| `source/authored-map/editor-layer.zip` | Tracked six-layer capture of the preceding saved terrain; does not yet contain the latest village/cliff/camp revision |
| Installed gameplay copy | `C:/Users/asphy/Documents/Warcraft III/Maps/TheKingsLastStand/KLS-D-68303d69bf-Development.w3m` on the owner's computer |
| Repository immediately before this handoff | `main`, commit `e5088ca`; later documentation commits may supersede it |

The original generated Terrain copy contained 85 disposable Neutral Extra references plus four starting markers. Those counts are historical reference evidence, **not** a requirement to restore objects the owner deleted.

## 3. Required `.md` reading order

Paths below are relative to the repository root. In the documentation ZIP they retain the same paths. Read documents' latest decisions before historical package sections.

### Read before any edit

| Order | File | Purpose |
|---:|---|---|
| 1 | `AGENTS.md` | Project invariants, preservation and engineering rules |
| 2 | `README.md` and `BUILDING.md` | Repository, build/install/capture workflow and prerequisites |
| 3 | `docs/EDITOR-LAYOUT-REVISION.md` | Latest manual changes; removed Orc town, cliff defenses, preserved camp, pending integration |
| 4 | `docs/GAME-VISION.md` and `docs/GAMEPLAY-SPEC.md` | Intended complete game and approved gameplay rules |
| 5 | `docs/DECISIONS-AND-OPEN-ISSUES.md` | Later decisions override earlier proposals |
| 6 | `docs/PROGRESS-LEDGER.md`, `docs/ROADMAP-AND-ACCEPTANCE.md`, `CHANGELOG.md` | What was implemented, which exact build was checked, and what remains pending |
| 7 | `docs/TECHNICAL-ARCHITECTURE.md` | Runtime modules, generators, installed API provenance and archive format |

### Read before work in that area

| Area | Required files |
|---|---|
| Terrain, placement and handoff | `docs/EDITOR-LAYOUT.md`, `docs/EDITOR-WORKSHOP.md`, `docs/EDITOR-WORKSHOP-HANDOFF.md`, `docs/TERRAIN-DRESSING-GUIDE.md`, `docs/WORLD-EDITOR-POLISH-HANDOFF.md` |
| Towns and story | `docs/CROWNLANDS-EXPANSION.md` **together with** `docs/EDITOR-LAYOUT-REVISION.md` |
| Heroes and spells | `docs/HEROES-AND-ABILITIES.md`, `docs/HERO-THEMED-EXPANSION.md`, `docs/AUDIT-COMPLETION.md` |
| Buildings, recruits and research | `docs/COMPANIES-AND-BUILDINGS.md`, `docs/COMPANY-RESEARCH-AND-POWERS.md` |
| Items, recipes and balance | `docs/ITEMS-AND-EQUIPMENT.md`, `docs/ITEM-CATALOG.md`, `docs/STAT-POWER-CURVE.md` |
| Backpack and multiplayer UI | `docs/BACKPACK-PANEL-REPAIR.md`, `docs/MULTIPLAYER-UI-REPAIR.md`, current acceptance/ledger |
| Waves, enemy behavior and checks | `docs/WAVES-AND-BOSSES.md`, `docs/WAVE-ROSTER-CATALOG.md`, `docs/PLAYER-GUIDE.md` |
| Alternative authoring tooling | `docs/WC3-FORGE-ASSESSMENT.md` before proposing wc3-forge adoption |

For decision history, read `docs/superpowers/specs/2026-09-29-progression-difficulty-loot-wave-vote-design.md` and the relevant dated plans in `docs/superpowers/plans/`. The September 28 plan's level-100 spells, older timing and automatic-growth proposals are superseded. Some older document sections name obsolete builds or inflated item values. Use the current manifest for package identity, the newest decisions for design, and the generated item/company catalogs for actual current values.

## 4. Strict visual and authoring boundaries

### Preserve the owner's work

- Preserve **all** manually added terrain, height changes, cliffs, trees, rocks, doodads, units, paths and building moves. Archive the complete saved map before interpreting any changes.
- Redtusk Hold was removed entirely. Do not reconstruct its buildings, shop, scenery or invisible story dependency. Orc playable content remains.
- Gates were replaced by cliffs. Do not spawn the old gate runs or gateway pieces over those cliffs. The invasion route must pass through the actual authored openings.
- Preserve the troll camp's placed units and composition. Allegiance, respawns, rewards and story involvement are undecided; do not silently turn it into a replacement Orc village or mandatory objective.
- The owner is personally fixing grass and terrain. Do not restore procedural square grass/dirt islands, diagonal repeated patches, plot texture stamping, or automatic road/hero-hub repainting.
- Use the owner's actual saved map and screenshots as the visual reference. Existing concept images are suggestions, not instructions to replace their composition.
- Do not flatten hills, remove blocking scenery, move the camp, replace models, or change authored ownership just because a generator previously expected something else. Identify the affected object and resolve its intended treatment explicitly.

### Functional space that must remain accessible

- Keep the broad north–south King's Road clear of construction and navigable for ordinary enemies and large bosses. Cliffs can frame a passage; they must not seal the required route.
- Keep four personal player bases across one horizontal defense row. Preserve plot ownership and expansion room; decoration must not prevent building, mine access, lumber gathering or exits.
- Keep castle, King Aldric, spring and market as one understandable connected town. Leave enough accessible space for several heroes at the spring and around shops.
- Building entrances and quest contacts must face reachable ground. Connect settlement entrances to the road with usable paths. Preserve room for caravan travel without disabling pathing to force it through scenery.
- The three surviving settlements are Crownshire, Moonbark Glade and Wraithfall. Wraithfall decoration must leave the northern invasion approach open.
- The hero-selection hub must remain usable and distinct from the battlefield; preview moves must also update selection/camera logic and labels.
- Maintain the 192×192 terrain, pathing, camera bounds, playable area and minimap together. Current world extents are approximately ±12,288 and playable/camera extents ±11,520. Do not resize the map casually.

### Existing coordinate anchors — reference only

These are **pre-handoff source coordinates**, not orders to undo human moves. Extract actual moved positions and facing from the saved map and update dependent scripts.

| Landmark | Existing source location |
|---|---|
| Castle / King | `(0, -500)` / `(0, 350)` |
| Restoring Spring | `(-900, -1600)` |
| Main market | Around `Y=-3900`; Apothecary and Sage's Archive are adjacent services |
| Four plot centers | `(-6000,-500)`, `(-3300,-500)`, `(3300,-500)`, `(6000,-500)` |
| Hero hub | Starts near `(-10800,-10800)`, five columns |
| Crownshire / Moonbark / Wraithfall | Approximately `(0,-9000)` / `(9000,0)` / `(0,9000)` |
| Former gate line / invasion spawns | Approximately `Y=5200` / `Y=6200`; reconcile with authored cliffs |

Natural dressing should use irregular transitions, coherent roads, clustered scenery, modest hills and readable open space. The castle should feel like a castle town; smaller settlements should feel like villages. Do not impose a new visual layout without showing how it preserves the owner's additions.

## 5. Gameplay contract to keep intact

### Match, waves and difficulty

- 2–4 allied defenders with shared vision and independent units/resources. Solo is permitted for development diagnostics.
- King Aldric's death is the only run-ending condition. Preserve the original 40 waves and chapter/boss identity. After wave 40, continue through the bounded repeating 41–50 roster with live-wave scaling; bosses recur every ten waves. HUD shows highest wave reached.
- Hero selection lasts up to 45 seconds, permits duplicates and falls back to Paladin. Initial preparation is 45 seconds, ordinary breaks 50 seconds, pre-boss breaks 180 seconds.
- During preparation, start early only when **every active player** votes Ready. Votes reset per preparation, support withdrawal and never pause the game. Use preparation-epoch/desired-state synchronization.
- Difficulty is selected during hero selection. The choice with the most votes wins; ties or no votes select Normal. It is not automatically the hardest choice someone selected.

| Difficulty | Enemy health | Damage | Count |
|---|---:|---:|---:|
| Easy | 0.75× | 0.80× | 0.90× |
| Normal | 1.00× | 1.00× | 1.00× |
| Hard | 1.30× | 1.20× | 1.10× |
| Very Hard | 1.60× | 1.40× | 1.20× |

### Heroes, skill points and talents

- Exactly level 1 / 0 XP at hero confirmation, cap 50. One normal skill point initially and one per gained level.
- Spend that same point pool on **one spell rank OR one repeatable, unranked +3 STR/AGI/INT choice**. Buttons need distinct labels/tooltips. Keep four learnable skills available. There is **no automatic +3 main/+1 secondary growth**; native attribute growth fields remain zero.
- Fifth-level talents are separate, nonmodal choices; one player's choice must not pause or interrupt anyone else's controls.
- Current talent investments: Vanguard +5 STR, +200 health, +2 health regeneration; Skirmisher +5 AGI and +2 percentage points of attack-only evasion; Sage +5 INT, +100 mana and +2 mana regeneration. Review actual installed secondary-stat constants when projecting power.
- Every hero has a separate signature and company/support pair. Keep the tree-free `AKfn` Briar Host for Keeper/Faelor beside three other learnable skills; no nearby trees required.
- Preserve native authored spell ranks. Only explicitly tagged power fields extend to ranks 4–5 at **110% / 120% of the final authored rank**, without compounding. Untagged fields copy the final authored rank; unsupported abilities keep native caps.
- Revive at the player's own altar after 20 seconds, preserving equipment and backpack state.

### Sacred Aura: exact tooltip/effect contract

Both `AHas` and `AHpa` require actual-current-rank learned descriptions and learn descriptions distinguishing current versus next rank and documenting all five ranks.

| Rank | Magic resistance | Increased healing received |
|---:|---:|---:|
| 1 | 15% | 15% |
| 2 | 25% | 20% |
| 3 | 35% | 25% |
| 4 | 38.5% | 27.5% |
| 5 | 42% | 30% |

Resistance storage is a fraction: rank 4 uses `0.385`, while its healing field uses `27.5`. Do not enter `38.5` into resistance. Description changes alone do not change scripted effects.

### Economy, XP and restoration

- Defender kills pay the killer's player only. King kills pay **25% of the bounty to each active player**. Show credited gold in game; no shared defender-kill bounty.
- Every active defender hero within 1,200 range gets the **full** enemy XP award, without dividing it or filtering by race/life state. Native XP is disabled to prevent duplicate/sharing behavior. Dead-hero XP still needs an engine check.
- Five race-matched starting workers; every starting mine has 1,000,000 gold. Human/Orc use neutral regular mines; Night Elf/Undead get owned Entangled/Haunted mines from the start.
- Restoring Spring quietly restores 1% maximum HP and mana per second within 450 range, capped at maximum. No forced healing animation, floating heal numbers or repeated spell effects.
- Castle purchases use the acting player's personal gold/lumber with validation/refunds. Current heal service costs 150 gold/50 lumber, restoring up to 2,000 HP; five upgrade tiers cost `400 + 200 × existing tier` gold and 150 lumber, adding 4,000 maximum HP and 30 damage per tier. Starting King has 15,000 HP and 80 damage.

## 6. Heroes, racial structures and fighting units

The selector has 25 choices: seventeen established heroes plus these eight additions. Use verified installed models/icons; do not assume an arbitrary campaign screenshot supplies a valid rawcode.

| Race | Hero / rawcode | Signature / rawcode | Identity |
|---|---|---|---|
| Human | Aveline Ashford `Havl` | Crownward Rally `AK17` | Banner defender |
| Human | Toren Flintlock `Htor` | Flintlock Barrage `AK18` | Siege artificer |
| Orc | Korgal Redtusk `Okrg` | Redtusk Earthshatter `AK19` | Cleaving frontline fighter |
| Orc | Morgra Ashcaller `Omor` | Ashen Spiritpack `AK20` | Spirit caster |
| Night Elf | Selyra Moonlance `Esly` | Moonlance Volley `AK21` | Precision huntress |
| Night Elf | Faelor Briarward `Efal` | Briarward Stand `AK22` | Tree-independent thorn control |
| Undead | Veyra Wraithveil `Uvyr` | Wraithveil Curse `AK23` | Curse-focused banshee |
| Undead | Tharos Bonecrown `Utha` | Bonecrown Guard `AK24` | Gravewarden / bone guards |

Established hero rawcodes: `Hpal`, `Hmkg`, `H000`, `Hblm`, `Obla`, `Ofar`, `Otch`, `Oshd`, `Edem`, `Ekee`, `Emoo`, `Ewar`, `Udea`, `Ulic`, `Nbrn`, `Hjsm`, `Npal`. Case matters. Hero proper names can be assigned by scripts.

Confirmed hero choice determines **that player's** race. Retain all four races even though the Orc settlement was removed. All supported building roles, towers, workers, companies and support units need race-appropriate models, icons and world-facing flavor text, with shared functional rules and balanced costs. This is not a request to implement every classic Warcraft tech tree.

| Role | Human | Orc | Night Elf | Undead |
|---|---|---|---|---|
| Banner Hall | `kH00` | `kH01` | `kH02` | `kH03` |
| Royal Foundry counterpart | `kF00` | `kF01` | `kF02` | `kF03` |
| Siege/support building | `kY00` | `kY01` | `kY02` | `kY03` |
| Hero altar | `h000` | `kA01` | `kA02` | `kA03` |
| Worker | Peasant `hpea` | Peon `opeo` | Wisp `ewsp` | Acolyte `uaco` |
| Starting mine | `ngol` | `ngol` | `egol` | `ugol` |

- A completed Hall unlocks the chosen hero's company at their Barracks, their support recruit at the Siege Yard, and their personal doctrine. It must have an actual gameplay role beyond a renamed Keep.
- A Foundry stocks the owner's racial Legendary pattern and applies a one-time +20% health/base-damage veteran upgrade to existing and future company troops. It must expose working services.
- All 25 company/support pairs and **50 authored recruit powers / 11 personal research services** are listed in `docs/COMPANY-RESEARCH-AND-POWERS.md`, generated from `tools/company_catalog.py`. This is the full unit/power specification to follow; do not substitute generic stock troops for these companies.
- New eight company/support IDs are `kC17`–`kC24` and `kS17`–`kS24`. Confirm names, abilities, costs, food and upgrades against the generated table.
- Never add allied companies to tracked wave enemies or award enemy bounties for their deaths. Fresh purchases clear recycled-handle bookkeeping; ordinary death retains data needed for resurrection. Upgrade existing units by deltas so they do not stack repeatedly.
- Keep valid building prerequisites. Current Castle requires Human Barracks/Blacksmith/altar; Night Elf Tree of Ages uses Ancient of War `eaom`, Hunter's Hall `edob` and `kA02`, avoiding the Wind/Lore circular dependency. Review all race equivalents after Object Editor changes.
- The Undead support Temple uses the actual Temple of the Damned parent/icon, not Meat Wagon. Tooltips should explain the building's purpose in the world, not say it is equivalent to a Human building.

## 7. Towns, story and troll camp

### Surviving settlement targets

| Settlement | Direction | Character / requirements |
|---|---|---|
| Crownshire | South | Homes, farms, supply trade, public square, worn connected roads |
| Moonbark Glade | East | Curving paths, groves, moonwell clearings, reachable services |
| Wraithfall | North | Crypts, worn stone, sparse vegetation, ritual site, open invasion approach |
| Troll camp | Owner's authored location | Preserve composition and units; exact gameplay role awaits clarification |

**Redtusk Hold no longer exists.** Keep playable Orc identity and gear, relocating necessary services rather than reconstructing the town. Separate town presence from stable four-race indices. Guard missing town/site handles in every consumer.

### Four-stage optional recovery arc

Objectives remain available during active waves, never pause/block spawning or change wave completion counts, and share permanent unlocks for this match. Contributors receive personal rewards. No between-match save system is required.

1. **Reclaim Northwatch:** relocate the former Orc contact to reachable surviving allied/frontier ground. Keep four threats and restored watchpost unlocks; port encounter/watchpost positions to the cliff layout.
2. **Escort Crownshire supplies:** reconcile the caravan route/destination with authored roads. Current caravan has 1,800 HP, speed 140, normal pathing, a nearby living escort within 900 range, two ghoul ambushes and retry after destruction. Completion unlocks Greater potion stock at extant vendors.
3. **Restore surviving quarters:** retain the Moonbark contribution, currently 250 gold/100 lumber. Activate refuges at **three** surviving settlements; quiet 1% HP/mana regeneration per second in 650 range. No deleted Orc refuge.
4. **Break Wraithfall's invasion ritual:** preserve four ritual guards and existing restoration-potion/garrison completion perks. Move contacts/guards as required; place racial garrisons at surviving sites without assuming a fourth town exists.

Quest-site rawcodes remain `kQ00`–`kQ03`. The former Northwatch site identity can be retained while moving its host; stable IDs do not require the removed village. Troll camp allegiance, respawns, loot and story participation must be recorded once agreed. Keep independent camp/story enemies outside wave accounting unless deliberately integrated.

## 8. Equipment, rarity, shops and crafting

- Use the native **generic Backpack `ebac`**, with 30 storage slots, nine equipment slots and the backpack carried in normal inventory. Do not restore Anya-specific `ebua` / Forsaken Field Pack or a custom 18-slot dialog.
- Each player's panel, contents and controls are independent. Buying, crafting, selling, equipping and transferring into normal inventory must preserve ownership, create exactly one item and handle full inventory safely.
- One generated catalog owns item values, colors, tooltips, shop stock, drops and recipes: `tools/equipment_catalog.py`, with `tools/recipes.py`. Read all rawcodes/stats/prices in `docs/ITEM-CATALOG.md` rather than duplicating stale balance values here.
- Preserve 80 general items, 20 racial items and three general crafted variants; four racial recipes produce the existing racial Legendary items, not four extra unspecified items. Equipment is universally usable; race identity comes from theme/source/effects.
- Keep a stat-book shop beside the Apothecary, with +5/+10/+20 STR/AGI/INT tomes priced 1,000/3,000/8,000. Tome and gear stacking must be included in power projections.

| Rarity | Color | Base equipment price |
|---|---|---:|
| Common | White `#FFFFFF` | 300 |
| Uncommon | Green `#1EFF00` | 1,000 |
| Rare | Blue `#0070DD` | 3,000 |
| Epic | Purple `#A335EE` | 8,000 |
| Legendary | Gold/orange `#FF8000` | 20,000 |

General Blade/Bow/Staff prices are 1.5× the rarity base; crafted fees follow the current recipe catalog. Name **and** tooltip colors must agree.

| Race | Common | Uncommon | Rare | Epic | Legendary |
|---|---|---|---|---|---|
| Human | Watchman's Token | Lionroad Mantle | Aldric's Aegis | Crownward Pennant | Last King's Oath |
| Orc | Redtusk Fetish | Ashen War Drum | Stormscar Bracers | Grudgebreaker | Worldrend Standard |
| Night Elf | Moonbark Charm | Starleaf Quiver | Duskwatch Longbow | Briarheart Mantle | Silvermoon Vigil |
| Undead | Crypt-Iron Band | Wraithsilk Cape | Soulreaper's Fang | Mourning Reliquary | Night's Covenant |

Racial patterns `RCP4`–`RCP7` combine that race's Rare + Uncommon relic, currently with a 9,000-gold fee. General patterns `RCP1`–`RCP3` produce Oathforged Kingswrath, Stormheart Prism and Sovereign's Mantle. Read exact components in `ITEM-CATALOG.md`.

Removing Redtusk's vendor must not make Orc ingredients unobtainable. Move its Common-through-Epic stock to appropriate existing market vendors, checking native shop capacity (at most twelve stocked entries). Keep the Orc Foundry recipe.

### Loot restrictions

- Normal enemies: **0% equipment**, separate 4% potion roll.
- Elite enemies: **1% total equipment**, evenly Common/Uncommon only; separate 8% potion roll.
- Bosses: **0% random world equipment**, separate 18% potion roll, plus one personal milestone gear entitlement per active player: Uncommon/Rare/Epic/Legendary at waves 10/20/30/40 and Legendary thereafter.
- No random wave-1 Rare/Epic/Legendary gear. Preserve full-inventory/null-item retry behavior and owner-bound fallback rewards.
- The reported old +168 Epic Grudgebreaker / +220 damage and +99 STR Worldrend values are historical inflation reports, not the target. Current catalogs use shared rarity/slot component budgets. Regenerate `docs/STAT-POWER-CURVE.md` after changes, including manual allocations, talents, tomes, equipment effects and slot collisions.

## 9. Enemy AI and behavior work

Waves are controlled by JASS triggers, not an AI Editor profile. Inspect `source/game.j`: `KLS_Spawn`, `KLS_Reorder`, `KLS_Tick`; inspect boss/combat behavior in `source/combat.j`, rosters in `tools/wave_rosters.py`, and story encounters in `source/crownlands.j`.

### Confirmed source gaps after placement edits

- `KLS_Spawn` and `KLS_Reorder` currently issue attacks toward hard-coded `(0,350)`. They must target the **actual King unit position** when the owner moves him. In runtime source use `GetUnitX(KLS_King)` / `GetUnitY(KLS_King)`; generated editor script globals use the `udg_` prefix.
- Keep the existing idle-order condition in `KLS_Reorder`. Reissuing attack orders continuously can cancel movement, casts and target choices.
- Old gate pieces still spawn from `KLS_BuildLandscape`; remove their source spawns after preserving the cliff handoff.
- Reconcile spawn lanes, rally/order points, boss collision clearance and caravan destinations with actual cliffs/paths. Do not fix stuck units by removing the owner's landscape or making units ignore pathing.

### Behavior checks and constraints

1. Observe an ordinary melee wave, ranged/caster wave and large boss through every required passage. Record stuck locations and current orders before changing recovery behavior.
2. Check initial orders and bounded idle recovery; avoid perpetual order spam. Keep spellcasts and autocasts functional. Existing Raise Dead/Bloodlust autocast orders should still operate.
3. Check boss telegraphs, phases, summons, target selection, damage and cleanup. Track enemies exactly once across death/summon/removal, without including allied/story/camp units accidentally.
4. Town recovery and caravan threats must run concurrently with waves while keeping their own accounting.
5. Ensure all gameplay state is deterministic across clients. `GetLocalPlayer()` may control presentation/camera only, never decide unit creation, damage, resources, drops or synchronized state.
6. Stop spawning, combat timers, rewards and revival correctly on King's death; do not end at wave 40.
7. The AI Editor can later support an autonomous faction, but do not start a second controller on the invasion owner during this pass. Any AI profile needs explicit startup/import integration and separate acceptance.

## 10. Bug and missing-work register

**Status key:** "source gap" means an identifiable pending source change; "repair present" means code/static evidence exists, while exact-build engine behavior remains unverified. Reproduce reported defects before replacing working systems. This is not a claim that every historical bug still reproduces.

| Priority / issue | Current status | Required next action / source |
|---|---|---|
| P0 Latest human additions could be lost on rebuild | Latest revision not archived/integrated; six-layer capture excludes units/objects/triggers | Save/close handoff, complete immutable archive, semantic disposition for every change; workshop tools/catalogs |
| P1 Deleted Redtusk / replaced gates return in game | **Source gap:** four-town/gate spawning remains | Remove actual Redtusk runtime placements and old gates; `town_catalog.py`, `game.j` |
| P1 Story references removed town | **Source gap:** site-1 contact and four-site loops remain | Relocate Northwatch; three-refuge/missing-site-safe unlock/vendor/garrison handling; `crownlands.j` |
| P1 Camp and moved buildings not reflected at runtime | **Source gap:** art capture does not import units; original source positions remain | Port creation identities, ownership, XYZ/facing and dependencies; placement catalogs; don't clean up new gameplay units as previews |
| P1 Enemies attack old King coordinate | **Source gap:** hard-coded `(0,350)` | Actual-position orders with existing idle guard; `game.j`; test cliff/boss routes |
| P1 Multiplayer backpack opens/closes with another player | Repair present: generic pack and owner-local panel preference | Two players open/close, switch selection, equip and shop simultaneously; `backpack.j`, UI repair docs |
| P1 Purchases/crafts duplicate items or show both success/failure | Repair present: transfer detachment / duplicate craft-start guards | One purchase/output, one fee/component transaction, correct refund/restock; also full inventory; `shops.j`, `equipment.j`, `recipes.py` |
| P1 Purchased equipment cannot transfer/equip/sell | Repair present: gear drop/pawn flags and native transfer logic | Test normal inventory, bag, equipment and buyback without loss/duplication; `equipment_catalog.py`, `objects.py`, shop/backpack runtime |
| P1 Level-2 start / unwanted automatic attributes | Repair present: level 1/0 XP, zero growth, manual point pool | Fresh selections, XP suppression, spell vs stat choice, repeated +3 buttons; `heroes.j`, `hero_progression.py` |
| P1 Stat choices have same text, levels, wrong stat, or hide spells | Repair present: separate unranked owner controls | All three labels/effects, shared point consumption, all four learnable spells; `heroes.j` |
| P1 Ranks beyond 3–4 break spells / aura reads 500% or rank 3 | Repair present: tagged safe scaling and generated descriptions | All supported rank effects and both aura IDs at ranks 1–5; `hero_progression.py` |
| P1 All players get Human workers / race or portrait mismatch | Repair present: independent hero-to-race catalogs | Mixed-race ownership, actual worker rawcode/model/icon/build menu; `hero_catalog.py`, `faction_catalog.py`, `heroes.j` |
| P1 Undead/Elf cannot mine; mines have unequal reserves | Repair present: owned Haunted/Entangled starts, all one million | Gathering, capacity, ownership, replacement and reserve parity; `mining.j`, `faction_catalog.py` |
| P1 Circular prerequisites / altar doesn't unlock Castle | Repair present: custom altar requirements and Elf prerequisite repair | Build and upgrade each race in a fresh match; `faction_catalog.py`, `company_catalog.py` |
| P1 Empty Hall/Foundry or missing custom troops/services | Repair present: companies, doctrine, veteran/pattern services, research/powers | Construction completion, correct owner's recruits, 50 powers/11 services and existing/future upgrade deltas; `companies.j` |
| P1 Ready/stat/talent UI affects others or pauses everyone | Repair present: synchronized clicks, deterministic frame setup, nonmodal controls, Ready epoch | Player 2 initiates/votes last; simultaneous controls; stale/repeated messages and player leave; `heroes.j`, `game.j`, `match_rules.j` |
| P2 Rarity colors missing / early Legendary drops / racial gear outclasses general | Repair present: standard colors, restricted loot, component budget/power report | Shop/item tooltip/effect checks, boss entitlements, recipe tier order, fresh power projections; item catalog/`combat.j`/`rewards.j` |
| P2 Bounty invisible or shared; XP divided/wrong recipients | Repair present: personal gold feedback, King 25%-each, full range XP | Actual balances/messages and nearby/dead hero XP; `combat.j` |
| P2 Spring emits heal animation or restores in chunks | Repair present: quiet percentage tick | Observe 1-second HP/mana changes and no forced visuals; `wave_environment.j` |
| P2 Temple uses Meat Wagon icon / building descriptions are generic technical text | Repair present: explicit Temple icon and racial descriptions | Inspect all race build buttons/models/flavor text; `faction_catalog.py` |
| P2 Editor references invisible/unselectable / disappear in package | Terrain copy has editor-only references; Unit selection layer required | Unit Palette then Space/Selection Brush; distinguish disposable references from runtime spawns; do not infer missing runtime from editor previews |
| P2 Current exact-build engine/network/endurance evidence missing | **Pending acceptance**, not a recorded failure | Required checks below, build/hash-tagged findings; never mark Development as Production prematurely |
| P2 Friend's clean checkout cannot build immediately | Known local extraction/bootstrap prerequisites | Follow `BUILDING.md` / architecture; installed CASC/API data and extractor paths are machine-local; do not copy old installed tables blindly |

## 11. Technical source navigation

Change authoritative modules/catalogs, not generated `source/war3map.j`, package members or a one-off patch copy. `tools/pipeline.py` defines explicit module order and generates compiled JASS and editable trigger sources from the same runtime.

| Area | Owning source |
|---|---|
| Overall initialization, waves, enemy orders, landscape/build validation | `source/game.j` |
| Difficulty / Ready helpers | `source/match_rules.j` |
| Hero selection, manual progression, talents, revival | `source/heroes.j`; `tools/hero_catalog.py`, `tools/hero_progression.py` |
| Signatures and effects | `source/signatures.j`; `tools/signature_spells.py` |
| Personal companies, upgrades, powers | `source/companies.j`; `tools/company_catalog.py` |
| Race structures, workers, roles, icons, menus | `tools/faction_catalog.py` |
| Mining | `source/mining.j` |
| Native pack / vendor transfer / item transactions | `source/backpack.j`, `source/shops.j`, `source/equipment.j` |
| Equipment and recipes | `tools/equipment_catalog.py`, `tools/recipes.py`, inherited object definitions in `tools/objects.py` |
| Boss/story reward queue | `source/rewards.j` |
| Bounties, XP, battle/boss events | `source/combat.j` |
| Spring/environment / castle purchases | `source/wave_environment.j`, `source/castle.j` |
| Towns, caravan, refuges and recovery story | `source/crownlands.j`; `tools/town_catalog.py` |
| Castle/market/hub/base references and coordinates | `tools/layout_catalog.py`; `tools/map_info.py` for plots/starts/bounds |
| Wave compositions | `tools/wave_rosters.py` |
| HUD / diagnostic state | `source/hud.j`, `source/diagnostics.j` |
| Editor archive preservation and semantic review | `tools/editor_workshop.py` |
| Six-layer art capture | `tools/capture_authored_map.py`, `tools/authored_map.py` |
| Editable trigger export | `tools/gui_sources.py` |

Native Object Editor fields, GUI triggers and source-generated runtime are related but distinct. Port object deltas by rawcode/field/rank to their generator; translate deliberate trigger changes into appropriate source modules. Preserve authored trace/lesson triggers and disabled status deliberately. Do not paste the entire editor-generated script over source or initialize systems twice.

## 12. Ordered implementation and preservation plan

1. **Receive/preserve:** obtain current save-and-close confirmation; copy the complete `.w3m` into an immutable archive; record SHA-256 and all members. Never overwrite the only edited file. Inspect editor/native data and user additions before build.
2. **Establish comparison limits:** use a real pre-edit native baseline if available. These edits may predate Chapter 0. An already-edited save is not a clean baseline, and the baseline tool may correctly reject changed/deleted references. Do not recreate deleted units to satisfy it. Compare conservatively against generated reference identities and known native format evidence, preserving unresolved changes for review.
3. **Review all changes:** use existing creation identities for moved references, not nearest coordinates. Record every unit addition/deletion/replacement/ownership/facing change, object field/rank change, art change, trigger/script change and unknown member. Archive bytes even when a decoder cannot interpret them.
4. **Integrate authored art and gameplay separately:** capture six art layers; port placements and new gameplay units through catalogs/runtime. Update Neutral Extra cleanup so it only disposes of intended previews. Ensure moved refs produce exactly one gameplay instance at the authored location.
5. **Reconcile geography/story:** remove Redtusk/gate source spawns, relocate contact/vendor stock, guard absent sites, preserve camp, and port King/spring/shops/plots/hub/quest/escort/refuge dependencies. Add individual position/facing overrides where shared offsets cannot represent a move.
6. **Repair AI/routes:** actual King targeting, invasion/boss/worker/caravan passages, spell/autocast behavior, idle recovery and enemy accounting. Preserve authored scenery.
7. **Check heroes/ranks/races and companies:** reproduce historical reports on the current integrated candidate; repair actual failures and preserve source fixes already working. Check all 25 choices, four races, signatures, stat points, talents, mines, prerequisites, recruits and services.
8. **Check gear/loot/transactions and multiplayer:** independent native panels, purchase/craft/sale atomicity, scarcity, owner rewards, recipe budgets and source-generated power curve. Obtain actual two-player and mixed-race evidence.
9. **Package once and document:** supported builder only; one current Development gameplay package, one working Terrain copy, old versions archived elsewhere. Add changelog, manifest/hash, delta dispositions, results and next human check.

### Supported commands — from repository root

Only use capture/review/build against the appropriate **closed** copy after preservation. These are future workflow instructions; no map capture/build/testing was performed to produce this handoff.

```powershell
# Capture visual layers only; current build identity is validated.
python -X utf8 -B tools/capture_authored_map.py --map "<saved-current-Terrain.w3m>"

# Baseline only for a genuinely clean native save before that chapter's edits.
python -X utf8 -B tools/editor_workshop.py baseline --chapter 1 --map "<native-saved-map.w3m>" --closed

# Requires an actual compatible baseline; substitute its returned real path.
python -X utf8 -B tools/editor_workshop.py review --chapter 1 --map "<edited-map.w3m>" --baseline "<real-baseline.json>" --closed

# After reviewed source integration, build/install the one current package.
python -X utf8 -B tools/build_map.py --install-test-map

# Prepare the next editing copy only after archiving the prior closed copy.
python -X utf8 -B tools/build_map.py --prepare-editor

# Regenerate documentation after relevant catalog changes.
python -X utf8 -B tools/render_item_catalog.py
python -X utf8 -B tools/power_curve.py
python -X utf8 -B tools/render_company_catalog.py
```

The art allowlist is `war3map.w3e`, `war3map.wpm`, `war3map.doo`, `war3map.shd`, `war3map.mmp`, `war3mapMap.blp`. It excludes `war3mapUnits.doo`, objects and triggers. Keep their full original archive and integrate them explicitly.

Do not scatter many map versions into different live folders. The owner's local test path is `Documents/Warcraft III/Maps/TheKingsLastStand/`. Historical maps belong under local backups outside that folder, with build-tagged names. Development remains the label until required acceptance passes; use Test/Production only when justified.

## 13. Finite Editor Workshop to continue with the owner

The approved full instructions are in `docs/EDITOR-WORKSHOP.md`; follow them one area at a time, using the **latest** geography decisions and honest baseline limitations above.

| Chapter | Focus / result |
|---:|---|
| 0 | Preserve a native save and comparison baseline where valid; current already-edited revision needs conservative integration, not a false clean baseline |
| 1 | Castle, courtyard, market and spring; authored paths/scenery and actual source placement updates |
| 2 | One personal base, then all four races; mining, menus, buildings, prerequisites and room to build |
| 3 | Three surviving villages and their roads, plus preserved troll camp inspection; no restored Redtusk |
| 4 | Eight new heroes, then seventeen established choices; models, attributes, four learnable skills, signatures and companies |
| 5 | Spells/ranks/descriptions, starting with both Sacred Aura IDs; data units and safe scaling |
| 6 | Trigger trace and wave behavior; inspect `KLS_Init`, spawn/reorder/tick and AI Editor responsibilities |
| 7 | Focused gameplay check, including two-player backpack/controls, recorded issues; workshop ends here |

World Editor: Module → Terrain Editor with Terrain/Doodad/Unit/Region palettes; Module → Object Editor for Units/Abilities/Items/Upgrades; Trigger Editor for events/JASS; AI Editor for a future independent faction. Select units in the **Unit layer** before Space/Selection Brush. Use Object Editor raw-data display for IDs; script-applied names may differ. Doodads are scenery; placed gameplay units need source integration. Keep disposable reference ownership distinct from actual camp/story units.

## 14. Required checks and honest completion criteria

Historical evidence: the packaged build passed installed-API JASS syntax/readback and 188 source/layout tests; subsequent workshop tooling reached **200 tests passed**. These are historical recorded checks, not fresh tests run by this handoff and not proof of engine compatibility. Earlier user-reported successful Test Map remains credited to **KLS-D-fd638ddcf5**; never describe it as a failed step.

Current edited revision and its future integrated successor still require:

- Editor open/save/reopen; authored additions retained, intentional deletions retained, references visible, no duplicated runtime units, coherent minimap/bounds.
- Custom Game startup with visible **exact build ID**, 25-choice selection and fresh level-1 hero.
- Castle/market/spring and all three villages/camp accessible; main road, cliff passages, bosses, mines, lumber and caravan routes usable.
- Mixed-race workers/owned mines, build menus, all supported structures/towers, prerequisites, companies, research, powers and ownership.
- Every new hero's signatures, four learnable skills, manual stat/spell point competition and separate fifth-level talents; all 25 hero choices recorded.
- Supported spell ranks and exact Sacred Aura current/next labels and effects at ranks 1–5.
- Independent backpack panels and controls with two players; Player 2 acts first and last; purchase, equipment, sell and all seven recipes, including full inventory/failure/refund/restock and duplication checks.
- Gold/XP recipients and feedback, potions/loot scarcity, boss milestone rewards and balanced catalogs.
- Difficulty multipliers, 45/50/180-second phases, unanimous Ready/withdrawal/leave handling, ordinary and boss AI.
- Four-stage optional story during waves, shared once-per-match unlocks, personal contributor rewards, caravan loss/retry and missing-site safety.
- Two-/three-/four-player initialization and actual two-/four-player sessions; no desynchronization or cross-player UI/control interference.
- Normal-speed 40-wave progression, transition into endless, later bosses and King-death termination; forced development waves are targeted checks, not endurance evidence.

Use documented `-diag`, `-gear` and development `-wave N` controls where applicable. For rank tests use documented diagnostics or a temporary test trigger; do not invent unsupported commands. Record exact build ID/hash, reproduction, expected/actual result and pass/pending status. A syntax pass is not a gameplay pass.

### Reporting template

```text
Chapter / work area:
Input saved map / SHA-256:
Saved and closed confirmation:
Archive / comparison baseline and limitations:
Preserved additions / intentional deletions:
Moved buildings and dependent coordinates ported:
Hero, ability, item, building and trigger deltas ported:
Unresolved or unknown changes retained:
New Development build / map path / SHA-256:
Automated/package checks actually run:
Editor/game/multiplayer checks actually run:
Bugs reproduced / repaired / still pending:
Changelog and ledger entries:
One next human check:
```

## 15. Tooling limits and wc3-forge

### Verified editor version — do not confuse versions

Read-only inspection on 30 September found `C:/Program Files (x86)/Warcraft III/_retail_/x86_64/World Editor.exe` with product version **`3.0.0.24268 (ede670caa6)`**. The active installed `.build.info` also reports `3.0.0.24268`. This matches Blizzard's [Forsaken Kingdom 3.0 release notes](https://us.forums.blizzard.com/en/warcraft3/t/warcraft-iii-reforged-forsaken-kingdom-patch-notes/38400). Blizzard separately lists [PTR build 24306](https://us.forums.blizzard.com/en/warcraft3/t/new-300-ptr-build-24306/39295); a PTR build is not evidence of four missed production updates.

The friend reports that their agent says the owner's editor is "four versions behind". The exact message/comparison target has not yet been supplied, so that claim is **unverified**. Distinguish editor product/build number, Retail versus PTR, and individual archive schema versions. This project uses W3I metadata version 39, native unit records 13.11 and native Object Editor data version 3; these numbers are not editor release numbers. Request the actual compared versions/tool output before prescribing an update, downgrade or conversion. Any game update requires fresh API extraction and a preservation/compatibility check, not automatic conversion of the only edited copy.

### Computer use and alternative authoring

Live computer-use observation previously failed during helper initialization (`failed to write kernel assets`, OS error 3). No current live editor inspection occurred. Do not claim that the last map was watched or visually verified; obtain actual screenshots or working supported computer use.

The owner asked whether <https://github.com/StephenSHorton/wc3-forge> could help. It is a potential separate MCP-enabled authoring editor, **not a control bridge for the already-open Blizzard World Editor**. It has not been installed, connected or tested with this exact map here. Read `docs/WC3-FORGE-ASSESSMENT.md`. If adopting later, preserve the complete map and try a separate archived copy first; compare a no-change save for terrain, unit/object/trigger format preservation before making it part of the supported build workflow. Keep source integration and human additions intact.

**First receiving-agent action:** read the required files, receive the latest saved/closed map, archive it, and report the exact preservation/comparison plan. The next gameplay build must incorporate that handoff rather than restore the older generated landscape.
