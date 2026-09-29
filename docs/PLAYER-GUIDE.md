# Player and human-test guide

## Install and test the current development build

1. Build the current map and install it to the dedicated test folder with:

       python -B tools/build_map.py --install-test-map

2. The installer archives old project maps and leaves one current map named `<build-id>-Development.w3m` in `Documents/Warcraft III/Maps/TheKingsLastStand/`. If Warcraft III or World Editor has an older map open, close it before installing so Windows releases the old file.
3. Test that installed map from the already-open World Editor when it points at the current map, or select the same build in Warcraft III → Single Player → Custom Game. Do not make another test copy.
4. Confirm the startup text includes the filename's build ID. Stop if a different or no build ID appears.
5. Select one of 25 hero previews, read role/abilities, and confirm. The chosen race determines your worker, Altar and build menu; duplicate heroes are allowed. If no choice is made within 45 seconds, the fallback is Paladin.
6. After all players confirm, the initial preparation timer is 45 seconds.

The current package is development build `KLS-D-2fd59dee88` at `dist/KLS-D-2fd59dee88-Development.w3m` (SHA-256 `90204c470bd78cfb9c31abb4bf9768af31aea420d7f9330a1887664231456f91`). It is installed at `Documents/Warcraft III/Maps/TheKingsLastStand/KLS-D-2fd59dee88-Development.w3m`; its SHA-256 matches the package manifest, and it is the only project map in that folder. Current-build Test Map and Custom Game checks remain pending; the user-reported Test Map success for earlier build `KLS-D-fd638ddcf5` remains a pass for that build only. Check ROADMAP-AND-ACCEPTANCE.md for current status.

All four Crownlands settlements are reachable by connected roads: Crownshire (Human, south), Redtusk Hold (Orc, west), Moonbark Glade (Night Elf, east) and Wraithfall (Undead, north). Each has a race-themed shop that stocks its five themed universal items and healing/mana potions. Talk to the settlement characters to start the optional four-chapter recovery story; it continues during active waves. The four Legendary Foundry patterns combine that race's Rare and Uncommon item into its Legendary item. When hero selection ends, Undead and Night Elf players already have their Haunted or Entangled Gold Mine at the base; Human and Orc players use a regular Gold Mine. Starting mines hold 1,000,000 gold.

On each level after 1, open the hero ability panel and spend the normal skill point on `+3 Strength`, `+3 Agility`, or `+3 Intelligence` (the plus buttons replace the old level-up stat dialog). Every fifth level also grants a Vanguard, Skirmisher or Sage talent. Four Crownlands objectives can be started from their settlement characters at any time; they do not pause active waves.

## Match

- Defend King Aldric. The original Crownlands story lasts waves 1-40, then crossover assaults continue automatically. King Aldric's death ends the run; the HUD shows the highest wave reached.
- Work your own race-matched base and command your own army. You cannot control a teammate's units.
- Hire/use workers to mine gold, harvest nearby trees, and build within your own plot.
- Build on your plot only. Keep the central road open for attackers, defenders, siege units, and bosses.
- Use the separate Altar of Kings to choose/revive your hero.
- The southern market offers gear tiers, priced from 300 gold for Common to 20,000 gold for Legendary; Blade, Bow and Staff cost 1.5 times their rarity's base price. Inspect each shop's item icon and tooltip before buying. If stock is empty or the shop only shows unlabeled text, record the build ID and stop that shop test.
- Click the Forsaken Field Pack in your hero's normal inventory to open the native backpack equipment panel. This build uses the installed `ebua` item identity. Confirm the panel shows 30 storage slots and nine equipment positions. If it does not open, keep the item and report the exact build ID with a screenshot.
- To move bought gear between the 30-slot backpack, the five other normal inventory slots, and the nine equipment slots, drag the item through the native Forsaken Kingdom inventory panel. Gear can be sold back to a market vendor for half its listed price; boss relics remain unsellable.
- A player-owned defender kill pays its full bounty only to that player's resources. King Aldric's kill pays 25% of the bounty to each active player. The exact amount should appear in a recipient-only gold popup. Stronger enemies pay larger bounties.
- Each active player's hero within 1,200 range of a tracked enemy death receives the full XP award individually. Nearby heroes do not divide the XP; race and life state do not filter recipients. This custom award is source/package checked and needs in-game confirmation.
- Use King Aldric's Castle for heal/upgrade buttons. Contributions cost personal resources.
- Keeper of the Grove and Faelor Briarward have tree-targeting `AEfn` suppressed; use their Grove Awakening or Briarward Stand signature on open ground to summon Treants without a nearby tree.
- Normal breaks: 50 seconds. Before every boss wave: 180 seconds.
- The Restoring Spring is below/south-west of the castle. Active living heroes within 450 range quietly recover 1% of maximum HP and 1% of maximum mana every second while missing either resource. It no longer produces a healing burst effect or per-tick text.

## Diagnostic-only shortcuts

These are for development/testing and must not be treated as release controls:

| Chat text | Purpose |
|---|---|
| -help | Show diagnostic help |
| -diag | Show build ID, recent runtime creation/error diagnostics, and each active player's expected/actual starting mine, owner, gold reserve and coordinates |
| -wave N | Start a diagnostic-selected wave 1-1000 |
| -gold | Add diagnostic gold/lumber |
| -repair | Exercise castle-heal transaction |
| -upgrade | Exercise castle-upgrade transaction |
| -power | Spend talent point on damage |
| -vitality | Spend talent point on maximum health |
| -wisdom | Spend talent point on intelligence |

## Reporting a problem

Include the exact on-screen build ID. For missing units/buildings/items, type -diag and provide its complete output plus a screenshot. The starting-mine line appears after hero confirmation and reports expected/actual mine, owner player ID, remaining gold and position. Required racial-mine spawn failures use the context `starting racial gold mine`. For engine or editor errors, run:

    python -B tools/collect_test_logs.py

Then provide the new snapshot folder name and note whether the game was launched through Custom Game or World Editor. Older logs may belong to earlier builds and must be kept separate.
