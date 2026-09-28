# Decisions, history, and open issues

This file keeps design choices visible when implementation evolves. A newer explicit user direction supersedes older decisions; otherwise preserve the agreed target.

## Preserved user decisions

- Create a new RPG/defense map on the supplied blank map instead of deprotecting the original map considered at the start.
- Co-op defense: defenders hold the south-side kingdom and enemies attack down the road from the north toward the neutral king.
- Two to four players; solo allowed for diagnostic builds.
- Each player controls only their own hero, builders/workers, army, and base. No shared unit control.
- Human kingdom buildings/workers regardless of the race of the chosen hero.
- Choose one main route, four individual bases aligned horizontally across one horizontal defense row, broad northern wall with an open gate, King Aldric's castle centered on the defense row, and a shared market farther south.
- Forty escalating waves in four chapters, four bosses on waves 10/20/30/40.
- Human defenders against varied undead and demon forces; include living/other escorts so combat abilities that need living targets have valid targets.
- Classic worker economy, plus combat gold. Markets are shared structures; purchases and reward gear remain personal.
- One hero per player, chosen from fifteen distinct heroes; duplicate selections allowed.
- Free construction inside personal plots; the main road cannot be built on.
- Repairable/upgradable buildings, tower defense, a worker-accessible mine and nearby harvestable trees at every plot.
- Altar of Kings is the player's hero-selection/revival building. The Chapel/sorceress presentation was reported as wrong.
- Native Forsaken Kingdom backpack/equipment UI: 30 storage slots, nine equipment positions, six normal inventory spaces including the backpack item.
- Multiple quality-tier shops with inspectable icon stock/tooltips and distinct armor/weapons/rings/trinkets/capes plus stat items.
- Add permanent Strength, Agility and Intelligence tomes in a separate Sage's Archive beside the Apothecary.
- Enemy kills grant combat gold. Each roster role now has a generated base bounty plus the current wave; chapter bosses have a higher formula. Split among active defenders in slot order. Values remain initial tuning pending live playtests; see `WAVES-AND-BOSSES.md`.
- Add recipes, boss relics, long progression to hero level 100 / spell rank 10, and a health/mana restoration pool below the castle.
- Longer breaks: 90 seconds after ordinary waves, 180 seconds before boss waves; keep 45-second hero selection and initial preparation.
- Heal and upgrade King Aldric at his castle, with visible costs and feedback.

## Requirements history / precedence

The original accepted tier sketch called for 12 families and 60 items and the initial normal/boss break was shorter. Later explicit feedback added Cape, Might Chestplate, Windrunner Boots, Arcanist Focus, attribute books, recipes, level-100 skill ranks, restoration pool, and 90/180-second breaks. The current generator therefore has 16 families × 5 qualities = 80 ordinary items plus 3 craft outputs. See ITEM-CATALOG.md for current exact data.

The earlier Chapel/sorceress presentation is superseded by the explicit correction: use an Altar of Kings. The earlier single/mixed mob look is superseded by varied undead/demon/escort compositions.

## Open reported issues (must not be silently closed)

1. **Backpack click/UX:** The installed `ebua` record is `EquipmentBackpackAnya` and includes the native extended/equipment inventory abilities. A prior custom clone `Ibpk` inherited the 30-slot count but may not have retained the installed item's runtime behavior. The current build modifies `ebua` in place, removes `ATua` (Anya's talent ability), and grants that native item to each hero. Confirm click-to-open behavior in Warcraft III.
2. **Gear movement/equip/sale:** Catalog gear is droppable (`idro=1`) and pawnable (`ipaw=1`); boss relics are movable but remain unpawnable. The current build must still be checked live for backpack-to-normal-inventory transfer, equipping, and shop resale.
3. **Shop stock UI:** User reported empty shops and later saw list-only purchase pages without visible item icons/stats. The source contains catalog/stock code, but exact current-build live shop window is not proven.
4. **Castle panels:** Older screenshot showed overflowing dialog text. Current source uses castle native shop-card buttons; verify current layout, prices, refunds, and health/upgrade effects in game.
5. **Altar model/role:** User observed a Sorceress in a structure expected to be the Altar of Kings and clarified the Chapel should be the Altar. Current source uses a custom lowercase h000 building record and selector logic; verify displayed model, portrait, construction object, and selection/spawn role in current build.
6. **Landscape scale/decor:** User repeatedly reported a map too small, missing wall/gates/player spaces/castle/trees/rocks. The current source expands terrain and stamps plots, road, northern gates and scenery. Visual scale, full side wall, tree distance, and all object creation remain pending current-build proof.
7. **Hero spells and race targeting:** Keeper's built-in Force of Nature requires real trees; Death Knight spell semantics require appropriate living/undead targets. The custom Grove Awakening and mixed enemy roster address intent in code; all casts need in-engine tests.
8. **Missing models/icons/rawcodes:** Older logs included model creation failures while an older map was in Warcraft's log; the failures were not attributed to the current build. Always tie new log evidence to exact build ID/hash and installed API provenance.
9. **Shop/gameplay behavior after build changes:** Re-run acceptance against current build only. A screenshot from an old build is not evidence the latest fixed or introduced the issue.
10. **Starting worker portrait:** Source creates `hpea`; installed `UnitUI.slk` names it `peasant`, while `uaco` is `acolyte`, and `UnitAbilities.slk` shows different ability lists. The reported portrait still needs runtime evidence. Current `-diag` now prints each player's actual race and first worker's object/unit name so the next exact-build capture distinguishes a wrong spawn from a display/group-selection issue.
11. **Combat gold feedback:** Exact per-player ordinary and boss gold payouts now use a local timed notification in source; verify it is visible/readable during dense waves and matches credited resources in game.
12. **Restoring Spring cadence:** Source now restores 1% of maximum HP and mana per second within the spring radius; verify its visual tick, exact regen, full-resource behavior and range in game.
13. **Hero/building/unit expansion:** Installed data verifies Human and Undead Ilastar (`Hjsm`, `Ujsm`) and the Forsaken Paladin (`Npal`) plus their campaign ability IDs. `docs/HERO-THEMED-EXPANSION.md` proposes adding them and Oathbound Companies; this architecture still needs user approval before gameplay code is changed. Aurrrius the Pure remains unresolved in the global installed tables and must not be assigned an invented rawcode.

## Process choices made for this repository

- The current artifact is a development map, not a release claim.
- Preserve the user's starter as backups/Blank-DE.w3m and the exact diagnostic map in dist/.
- Machine-local installed Warcraft API/object files stay out of Git; regenerate them from a supported installed edition.
- Store the complete player vision, mechanics, code/build contract, all 15 hero skill/signature descriptions, catalog, and acceptance plan as Markdown so future agents do not need conversation history to know the target.
- Keep one current development map in `dist/` and one installed copy in the dedicated Warcraft III test folder. Archive replaced builds outside that folder and preserve the existing open World Editor document.
- Use the progress ledger to append dated/build-tagged evidence. Never overwrite historical observations.
