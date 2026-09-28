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
- One hero per player, chosen from seventeen distinct heroes (the original fifteen plus Human Ilastar and the Forsaken Paladin); duplicate selections allowed.
- Free construction inside personal plots; the main road cannot be built on.
- Repairable/upgradable buildings, tower defense, a worker-accessible mine and nearby harvestable trees at every plot.
- Altar of Kings is the player's hero-selection/revival building. The Chapel/sorceress presentation was reported as wrong.
- Native Forsaken Kingdom backpack/equipment UI: 30 storage slots, nine equipment positions, six normal inventory spaces including the backpack item.
- Multiple quality-tier shops with inspectable icon stock/tooltips and distinct armor/weapons/rings/trinkets/capes plus stat items.
- Add permanent Strength, Agility and Intelligence tomes in a separate Sage's Archive beside the Apothecary.
- Enemy kills grant combat gold. Each roster role has a generated base bounty plus the current wave; chapter bosses have a higher formula. The killing defender's player gets the full bounty. King Aldric's kills grant 25% of that bounty to each active player. Values remain initial tuning pending live playtests; see `WAVES-AND-BOSSES.md`.
- Every active hero within 1,200 world units gets the full XP value for each enemy kill. Nearby heroes do not split XP; all hero races and life states are included. Native XP grants are disabled in map data and the runtime awards XP individually.
- Add recipes, boss relics, long hero progression, and a health/mana restoration pool below the castle. The previous rank-10 extension has been superseded after live reports and source inspection showed generated higher spell ranks could break abilities; current spells stop at their installed native rank limits until safer scaling is designed and verified.
- Breaks: 50 seconds after ordinary waves, 180 seconds before boss waves; keep 45-second hero selection and initial preparation. The 50-second normal break supersedes the earlier 90-second choice.
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
11. **Combat gold feedback and ownership:** Source now awards full normal kill gold only to the owner of a defender killing unit. King Aldric awards 25% of a kill bounty to each active player. Recipient-only floating text and a timed notification display credited gold. Verify popups/resources for both kill paths in game.
12. **XP award behavior:** Source disables native shared XP (which divides XP among heroes) and grants the full unit/hero kill XP independently to every active hero within 1,200 range, including heroes regardless of race or life state. Verify recipient range, full per-hero amount, and dead-hero handling in game.
13. **Restoring Spring cadence:** The source restores capped 1% max HP and mana each second within 450 range, with no healing effect or floating/timed text. The native fountain prop is optional, so its spawn failure cannot suppress the coordinate-based timer. Verify exact regeneration, quiet presentation, full-resource behavior, and range in game.
13. **Hero/building/unit expansion:** The user approved Oathbound Companies. The new source catalog adds Hall of Banners, Royal Foundry, Siege Yard, and a personal Barracks company plus support recruit for each of the 17 currently selectable heroes. Recruitment, doctrine effects, owner checks, and the one-time foundry bonus are package/source checks only; actual building access and purchases remain unverified. Human Ilastar (`Hjsm`) and Forsaken Paladin (`Npal`) are selectable. Undead Ilastar (`Ujsm`) still lacks a verified global skill list; Aurrrius the Pure remains unresolved in the global installed tables. Do not invent either hero's rawcode/kit.
14. **Spell ranks above native limits:** The earlier rank-10 generator extrapolated every numeric field and made Warden Blink's 50/10/10 mana costs become zero at rank 4; stale campaign data also caused 500% Sacred Aura resistance. Build `KLS-D-b5ae4ab2fe` caps heroes at level 50 and extends only spells with explicitly registered installed power fields through rank 5. Each added rank adds 10% of the final authored power value; all other fields copy the final native rank. Unregistered spells remain at their native cap. Sacred Aura is 38.5%/42% resistance at ranks 4/5. The 79-test suite and package/API checks pass; exact-build gameplay remains pending.
15. **Recipe delivery feedback:** A screenshot showed “Craft complete” followed by “Craft failed” for Oathforged Kingswrath. Source inspection found an unconditional fee refund after the delivery `if/else`, in addition to the failure-branch refund. Build `KLS-D-a2dae2be8c` removes the extra call and has a regression check. Confirm one successful recipe and the full-bag failure/refund path in Warcraft III before closing the live behavior report.
16. **Hero starting level and stat growth:** The level-50 cap is implemented in `KLS-D-b5ae4ab2fe`. Heroes still start at level 3, and the earlier requests to start at level 1 and gain +3 Strength/Agility/Intelligence per invested hero ability point remain open. The requested Warcraft III talent system with Strength/Intelligence/Agility secondary stats also remains open; the current +12 damage/+300 health/+10 Intelligence milestone buttons do not satisfy that request.

## Process choices made for this repository

- The current artifact is a development map, not a release claim.
- Preserve the user's starter as backups/Blank-DE.w3m and the exact diagnostic map in dist/.
- Machine-local installed Warcraft API/object files stay out of Git; regenerate them from a supported installed edition.
- Store the complete player vision, mechanics, code/build contract, all 17 hero skill/signature and company details, item catalog, and acceptance plan as Markdown so future agents do not need conversation history to know the target.
- Keep one current development map in `dist/` and one installed copy in the dedicated Warcraft III test folder. Archive replaced builds outside that folder and preserve the existing open World Editor document.
- Use the progress ledger to append dated/build-tagged evidence. Never overwrite historical observations.
