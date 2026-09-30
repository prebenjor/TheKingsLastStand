# The King's Last Stand: Editor Workshop

Approved 2026-09-30. Eight chapters, numbered **0–7**. Finish one chapter, save and close, then hand it back before starting the next. This workshop ends after Chapter 7; full endurance acceptance is separate.

## Start here — Chapter 0 only

Current working map: `C:\Users\asphy\Documents\Warcraft3Maps\kings-last-stand\build\KLS-D-68303d69bf-Development-Terrain.w3m`.

1. Open that **Terrain** copy in World Editor using **File → Open Map**.
2. Look for the castle, shops, four villages/quest sites and the 25 hero previews. These are disposable layout references; the installed gameplay map creates its real units at startup.
3. Use **File → Save Map**, without making more changes. Allow the editor to finish saving.
4. Close the map. Send: **“Chapter 0 baseline saved and closed.”** Mention any missing references or save warnings.

The agent will archive this native save and confirm the file for Chapter 1. **Chapter 0 remains pending until that handoff.** We cannot use the older saved map as this baseline because its build differs.

World Editor converts generated object and trigger formats when saving. A clean native baseline prevents those conversions from being mistaken for your edits. When a later chapter receives a newly generated copy, save/close it once before making edits so the agent can establish its new native baseline. Reopening the same unchanged native copy does not need another baseline.

## How each chapter works

1. Find the area or objects listed below.
2. Make only that chapter's small group of related changes.
3. Check the result and record specific failures.
4. Save and close the map.
5. Send the [handoff form](EDITOR-WORKSHOP-HANDOFF.md).
6. Wait for the agent's integration and current working-copy path before continuing.

Keep one current Development gameplay map and one current Terrain editing copy. Archived originals live outside Warcraft's test folder. Do not overwrite the installed map with the Terrain copy or change the build ID in Map Description.

## Your editor toolbox

Open tools through **Module**. See Blizzard's [editor introduction](https://news.blizzard.com/en-us/article/23395649/revisiting-the-warcraft-iii-editor) for their general roles.

| Tool | Use it for |
|---|---|
| Terrain Editor → Terrain Palette | Grass, dirt, stone, terrain blending and gentle raised/lowered ground |
| Terrain Editor → Doodad Palette | Houses, rocks, trees, fences, lamps, barrels and scenery |
| Terrain Editor → Unit Palette | Select/move existing building and hero references |
| Terrain Editor → Region Palette | Areas for future trigger behavior |
| Object Editor → Units | Heroes, workers, structures and recruits |
| Object Editor → Abilities | Rank data, targets, costs, icons and descriptions |
| Object Editor → Items / Upgrades | Equipment fields, research and requirements |
| Trigger Editor | Events, conditions, actions and custom JASS |
| AI Editor | An autonomous computer faction's economy, army and attacks |

### Finding things without guessing

- For shops/buildings/heroes, first switch the Tool Palette dropdown to **Unit Palette** (or choose **Layer → Units**), then press **Space** for the Selection Brush. Space changes the brush on the active layer; a Terrain/Doodad brush cannot select unit references. Click an existing unit to select it, drag it to move it, or double-click to inspect it. Use the minimap to reach the quarter of the map you need, then zoom in.
- In Object Editor, enable **View → Display Values As Raw Data**. Find by name and rawcode. Custom objects may be listed under the parent race/category; runtime proper names may differ.
- Write down a rawcode before editing. A spelling change is harmless to the rawcode; deleting/recreating an object can break scripts that reference its ID.
- Existing references belong to **Neutral Extra**. Leave that owner intact: startup removes them before real units spawn. The base references look Human before play; hero confirmation decides the actual race.
- **Move the existing unit** when relocating a shop, quest site or hero preview. Deleting it and placing another loses its creation identity and requires manual matching.
- Use doodads for decorative houses/scenery. Decorative units are excluded from the six-layer art capture; additional interactive units require a source spawning rule.
- Terrain textures change appearance. Cliffs, trees, rocks and building footprints can block movement. Use raised/lowered terrain for gentle hills, and leave routes around cliff edges.
- Save related changes in small batches. Screenshots help explain intention; the saved map supplies precise coordinates and field values.

## Chapter 1 — Castle, courtyard and market

**Goal:** one connected castle town. **Tools:** Terrain, Doodad and Unit palettes.

| Landmark | Approximate coordinates |
|---|---|
| Castle | `(0, -500)` |
| King Aldric | `(0, 350)` |
| Restoring Spring | `(-900, -1600)` |
| Market | Around `Y = -3900`; a second row is farther south |
| Northern gate | Around `Y = 5200` |

Do these in order:

1. Leave the broad north–south defense road open.
2. Paint a stone courtyard around the castle. Use a large brush for its center, then a smaller brush for irregular grass/dirt transitions.
3. Connect the courtyard to the spring and market with readable side paths.
4. Select and move the existing shops into a market street or square. Include Field Apothecary, Sage's Archive and Master Forge.
5. Add small residential **doodads** along side streets. Keep their doorways facing usable ground.
6. Add a few clusters of lamps, fences, barrels and rocks around edges. Avoid evenly repeated arrangements.
7. Raise/lower town edges gently. Keep entrances, the king's approach and player plots usable.

Check:

- [ ] Shops have accessible entrances and space for several heroes.
- [ ] Houses leave streets rather than sealing alleys.
- [ ] Aldric remains approachable from the invasion lane.
- [ ] Spring has room for several heroes.
- [ ] Decoration leaves all player plots and the defense road clear.

**Stop when:** castle, market and spring feel connected. Save/close and hand off Chapter 1.

Agent integration: transfer each existing reference's X/Y and facing into the placement generators, then check king attack targets, castle service ranges and spring regeneration center. The current generators mostly use fixed facing; they must gain per-placement facing support when the first facing change is ported. Art capture alone does not move runtime units.

## Chapter 2 — One base, then all four races

**Goal:** usable layouts and racial building functions. Start with Player 1 near **`(-6000, -500)`**. Other plot centers are `(-3300, -500)`, `(3300, -500)` and `(6000, -500)`.

Terrain pass:

1. Inspect the Town Hall, altar and mine footprints.
2. Leave clear routes between hall, mine and lumber.
3. Leave building space for Barracks, Banner Hall, Foundry, siege/support building and towers.
4. Connect the base entrance to the main road.
5. Apply the same practical checks to the other plots. Layouts can vary; economy and functional costs stay balanced.

In **Object Editor → Units**, inspect these custom families:

| Role | Human | Orc | Night Elf | Undead |
|---|---|---|---|---|
| Banner Hall | `kH00` | `kH01` | `kH02` | `kH03` |
| Foundry | `kF00` | `kF01` | `kF02` | `kF03` |
| Siege/support | `kY00` | `kY01` | `kY02` | `kY03` |

For each object, review:

- **Art:** model, icon, selection size and command-card button position.
- **Text:** name, description and tooltip. Write race-specific world flavor and explain its service; avoid implementation text such as “same as the Human counterpart.”
- **Techtree:** requirements, trained units, research and upgrade paths. Check for circular requirements: a hall must not require a building that itself requires that hall upgrade.
- **Stats:** gold/lumber cost, food, build time and health.
- **Pathing:** footprint fits its plot and doors have clear ground.

Some stock, company unlocks and Foundry effects are scripted. Empty native training fields alone do not prove failure. The Hall enables the chosen hero's company; the Foundry applies the authored veteran upgrade and exposes its services.

Gameplay checks: choose one hero of **each race**, inspect worker/mine/build menu, build Hall and Foundry, buy recruits and inspect research. Human/Orc use regular mines; Night Elf uses an owned Entangled mine; Undead uses an owned Haunted mine. **All four start with 1,000,000 gold** and five matching workers. Test actual gathering, not just the mine model.

**Stop when:** every race has a pass or an individually described failure. Save/close and hand off Chapter 2. Moving one base must not accidentally shift all bases that currently share mine/altar offsets; the agent will introduce individual placement overrides as needed and review plot bounds, start markers and camera positions.

## Chapter 3 — Four villages and their roads

**Goal:** four recognizable, reachable settlements. Complete them in this order:

| Settlement | Approximate location | Direction |
|---|---|---|
| Crownshire | `(0, -9000)` | Homes, farms, market activity, worn roads |
| Redtusk Hold | `(-9000, 0)` | Timber, hides, training space, rough paths |
| Moonbark Glade | `(9000, 0)` | Curving paths, groves, moonwell space, clearings |
| Wraithfall | `(0, 9000)` | Crypts, broken stone, sparse vegetation, dark ground |

For each village:

1. Find the existing hall, shop and quest-site references.
2. Move them around a modest public space.
3. Connect entrances with paths; connect the village to the kingdom road.
4. Cluster scenery around edges instead of scattering identical pieces uniformly.
5. Make its quest site noticeable and reachable.
6. Check the route with several units. Leave Wraithfall's invasion approach and gate opening clear.

Quest-site rawcodes are `kQ00`–`kQ03` in race order Human, Orc, Night Elf, Undead. Use these identities when reporting moves.

**Stop when:** all villages have connected routes and distinct scenery. Save/close and hand off Chapter 3. Agent reviews moved buildings, quest sites, escort destination/routes, encounter positions and refuge ranges together. Story remains optional, shared and persistent for that match; waves keep running.

## Chapter 4 — Heroes and their companies

**Goal:** a recorded inspection of all 25 choices. Start with Aveline, then the other additions.

| Race | Hero | Rawcode | Signature shell |
|---|---|---|---|
| Human | Aveline Ashford | `Havl` | `AK17` Crownward Rally |
| Human | Toren Flintlock | `Htor` | `AK18` |
| Orc | Korgal Redtusk | `Okrg` | `AK19` |
| Orc | Morgra Ashcaller | `Omor` | `AK20` |
| Night Elf | Selyra Moonlance | `Esly` | `AK21` |
| Night Elf | Faelor Briarward | `Efal` | `AK22` |
| Undead | Veyra Wraithveil | `Uvyr` | `AK23` |
| Undead | Tharos Bonecrown | `Utha` | `AK24` |

**Object Editor → Units**, one hero at a time:

1. Inspect model, portrait, icon and proper names.
2. Check primary attribute and starting STR/AGI/INT.
3. Keep growth fields `ustp`, `uagp`, `uinp` **zero**. There is no automatic +3/+1 growth.
4. Inspect **Abilities → Hero** (`uhab`): four learnable spells.
5. Inspect normal abilities and inventory support; a signature can be assigned at runtime.
6. Inspect attack type, projectile, attack range and movement.
7. Find company/support units using [the company catalog](COMPANY-RESEARCH-AND-POWERS.md). Inspect their visuals, descriptions and powers too.

Check in play:

- Starts at level **1**, caps at **50**.
- Four regular spells remain learnable.
- Repeatable **+3 STR / +3 AGI / +3 INT** choices spend the **same normal skill point** as a spell. They are unranked choices, not three native Attribute Bonus abilities.
- Independent talents arrive every five levels without pausing everyone.
- Signature works; Hall, company, doctrine and support match the hero.

Then review the seventeen existing choices with the same checklist:
`Hpal`, `Hmkg`, `H000`, `Hblm`, `Obla`, `Ofar`, `Otch`, `Oshd`, `Edem`, `Ekee`, `Emoo`, `Ewar`, `Udea`, `Ulic`, `Nbrn`, `Hjsm`, `Npal`.

Use [HEROES-AND-ABILITIES.md](HEROES-AND-ABILITIES.md) to match displayed names; scripts may assign names after selection. Keeper/Faelor's `AKfn` summon must work without trees.

**Stop when:** all 25 have a pass or a specific issue. Save/close and hand off Chapter 4. Do not remove inventory or runtime-support abilities to make the command card look cleaner without checking their role.

## Chapter 5 — Spells, ranks and descriptions

**Goal:** effect values and descriptions agree. **Object Editor → Abilities**. Begin with Sacred Aura, both **`AHas` and `AHpa`**.

| Rank | Resistance | Increased healing received |
|---|---:|---:|
| 1 | 15% | 15% |
| 2 | 25% | 20% |
| 3 | 35% | 25% |
| 4 | 38.5% | 27.5% |
| 5 | 42% | 30% |

**Units matter:** `hsa1` stores resistance as a fraction, so rank 4 is **0.385**. `hsa2` stores healing as **27.5**. Entering 38.5 in the resistance field would be wrong.

For each supported spell:

1. Check number of ranks and required hero levels.
2. Expand and inspect **every rank's** effect fields, costs, cooldown, duration, range and targets.
3. Check learned tooltip (`atp1`/`aub1`) and learn-menu tooltip (`aret`/`arut`). Learned text must show the actual current rank; learn text distinguishes current from next and describes supported ranks.
4. Check icon and command-card position.
5. Test rank 4 and rank 5 where supported. Do not assume a good tooltip proves the effect.

Keep authored ranks intact. Supported extensions use **110% and 120% of final authored power**, without compounding. Untagged fields retain their final authored values; unsupported spells retain their native caps. Read [hero progression](../tools/hero_progression.py) before changing a field's scaling policy.

Editing a shared spell affects every hero using it. A private variation needs a new custom rawcode plus generator/catalog and runtime registration. Name it and report the new ID in the handoff.

**Scripting lesson:** signature shells define the button/cost/targeting. [signature_spells.py](../tools/signature_spells.py) and [signatures.j](../source/signatures.j) define scripted effects. Editing only the tooltip does not alter damage, healing or summons.

**Stop when:** reviewed values match descriptions and current/next labels. Save/close and hand off Chapter 5. Use a temporary test trigger or an agent-provided diagnostic method for rank checks; there is no documented `-level` command.

## Chapter 6 — Triggers and enemy behavior

**Goal:** understand object-to-script connections. **Module → Trigger Editor**.

1. Open **Initialize Kingdom Defense**. It calls `KLS_Init()`.
2. Inspect the map's global custom script/header. The repository generates this from runtime modules; generated editor variables carry the `udg_` prefix.
3. Create a category `Workshop`, then a GUI trigger **`Workshop_SpellTrace`**.
4. Set its event to **A unit starts the effect of an ability**.
5. Set a condition: **Ability being cast equals Crownward Rally (`AK17`)**.
6. Add an action displaying a short message: `Workshop: Crownward Rally fired`.
7. Test Aveline's cast. The message confirms the event only; do not add duplicate damage/healing.
8. Disable the trace after testing. Report that it is disabled; the agent will preserve its lesson purpose explicitly.

Next find these functions in the custom script, or open [game.j](../source/game.j):

| Function | Responsibility |
|---|---|
| `KLS_Spawn` | Create wave units and initial orders |
| `KLS_Reorder` | Redirect idle enemies |
| `KLS_Tick` | Schedule recurring work |

For a moved king, an editor-script attack order uses his actual unit position:

```jass
call IssuePointOrder(GetEnumUnit(), "attack", GetUnitX(udg_KLS_King), GetUnitY(udg_KLS_King))
```

In repository modules the variable is `KLS_King`; the GUI export adds `udg_`. Apply the change to the matching order context, not to every unit in the map. Keep the existing **idle-order check**. Reissuing orders continuously can interrupt movement/spells. Record each changed function so the agent can port it to the runtime source.

**AI Editor introduction:** open **Module → AI Editor** and inspect army, building and attack settings. Those describe an autonomous computer faction. Our invasion waves use triggers. During this workshop, improve their orders in those triggers. Do not start a second AI controller on the invasion player. A future profile needs an explicit import/startup integration and separate testing.

Gameplay state must run deterministically for all players. Use owner-local display only for UI; never use `GetLocalPlayer()` to decide gold, damage, items or unit creation.

**Stop when:** the spell event is traced, wave orders are located, and trigger versus AI responsibilities are clear. Save/close and hand off Chapter 6. GUI trigger binaries are archived/reported; their intentional behavior is reviewed and translated into source, rather than overwriting the runtime with the complete editor-generated script.

## Chapter 7 — Focused gameplay check and finish

**Goal:** actionable workshop results. Record **pass / fail / not checked** against the exact build.

- [ ] Hero selection; level 1; manual spell/stat spending; separate fifth-level talent.
- [ ] Worker gathering; equal mine reserves; building prerequisites.
- [ ] Hall/company; support recruit; Foundry services/research.
- [ ] Shops: buying, equipping, selling and one recipe; no duplicate items.
- [ ] Rarity colors and reasonable tier progression.
- [ ] Quiet spring regeneration, 1% maximum HP/mana each second.
- [ ] Normal 50-second breaks; 180-second pre-boss preparation.
- [ ] Unanimous Ready voting, including changing a vote.
- [ ] One village objective during active waves; shared unlock, personal reward.
- [ ] One boss encounter with accessible routes.
- [ ] Two-player independent backpacks/controls and both players spending skill points.

Use documented development commands `-diag`, `-gear` and `-wave N` where helpful. A forced wave checks that encounter; it does not prove ordinary progression or endurance. For every failure, record hero/race, wave, object/ability, actions, expected result and actual result. Add a screenshot if useful.

**Stop when:** every checklist line has a result and failures are reproducible. Save/close, hand off Chapter 7. **The workshop is finished.** Full endurance remains a separate acceptance task. Keep DEVELOPMENT until all current-build editor, Custom Game, multiplayer and endurance gates pass. The earlier successful Test Map remains credited to `KLS-D-fd638ddcf5`; it is not a failed step or proof for a later build.

## What happens to your changes

The agent follows [the integration protocol](EDITOR-WORKSHOP-HANDOFF.md). Your archived map retains every member, including changes the comparison tool cannot decode. Six-layer art capture stays separate from semantic unit/object/trigger review.

Moved references are matched by their **creation identity**, then rawcode and ownership are checked. Replacements, duplicates, deletions and unknown objects require an explicit resolution. Runtime positions/facing and dependent gameplay coordinates are ported before rebuilding. Intentional Object Editor fields go into generators; trigger behavior goes into source modules. The next changelog records actual edits and checks, not unperformed chapter work.

## Where code and data live

| Change | Source to update after handoff |
|---|---|
| Castle, spring, market, hub references | `tools/layout_catalog.py`; consumers in `source/game.j`, `heroes.j`, `wave_environment.j`, `shops.j` |
| Player plot centers/bounds and start positions | `tools/map_info.py`, `layout_catalog.py`, `source/game.j`, `mining.j`, `heroes.j` |
| Village buildings/quest sites | `tools/town_catalog.py`; dependent story coordinates in `source/crownlands.j` |
| Terrain, pathing, doodads, shadows, minimap | `source/authored-map/editor-layer.zip`, through the capture CLI |
| Hero identity/company | `tools/hero_catalog.py`, `company_catalog.py`, `source/heroes.j`, `companies.j` |
| Racial workers/buildings/recruits | `tools/faction_catalog.py`, `objects.py`, `source/mining.j`, `companies.j` |
| Native spells/ranks/tooltips | `tools/hero_progression.py`, object generators |
| Signature abilities | `tools/signature_spells.py`, `source/signatures.j` |
| Items, colors, stats, stock, recipes | `tools/equipment_catalog.py`, `recipes.py`; regenerate item/power documentation |
| Skill/stat/talent UI | `source/heroes.j`; shared skill budget rules in progression helpers |
| Waves/orders/rewards | `source/game.j`, `match_rules.j`, `rewards.j`, `tools/wave_rosters.py` |
| GUI export | `tools/gui_sources.py`; runtime modules are authoritative |

Never edit generated `source/war3map.j` as the persistent fix. Build through `tools/build_map.py`. See [BUILDING.md](../BUILDING.md), [game vision](GAME-VISION.md) and [progress ledger](PROGRESS-LEDGER.md) for the wider contract.
