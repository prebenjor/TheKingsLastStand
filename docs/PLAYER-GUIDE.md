# Player and human-test guide

Current DEVELOPMENT build **KLS-D-68303d69bf**: `dist/KLS-D-68303d69bf-Development.w3m`; SHA-256: `baa024fd2b23ec03ef0ccbb6de5a2345a292fe82a4a03f9345b73c95b4d0b1c3`. Installed bytes match the package. Saved user terrain is captured; the editor-layout work copy is prepared. Editor/game/multiplayer/endurance checks remain pending. See [EDITOR-LAYOUT.md](EDITOR-LAYOUT.md).


## Historical backpack repair candidate — 2026-09-30

Historical DEVELOPMENT package: **KLS-D-2aac020fb1**.
- Artifact: `dist/KLS-D-2aac020fb1-Development.w3m`.
- SHA-256: `0b71c26a3353d088cedb376d0d27d597039b9662687d475c60569c732fcb3a9d`.
- Installed in `Documents/Warcraft III/Maps/TheKingsLastStand/`; prior package archived.
- Ready, difficulty and stat-choice frames/events now initialize on every client in identical player order. Only visibility is local; only the triggering player sends a synchronized click.
- New static UI safety regressions passed 3/3 after failing on both original initialization paths. Installed-API syntax and archive readback passed. Full suite: 113 tests, 7 failures and 4 errors; see `docs/MULTIPLAYER-UI-REPAIR.md`. No multiplayer fix is claimed verified.
- Next check: in a two-player game, have Player 2 vote first, undo, then let both players vote to start one wave. Repeat with Player 2 casting the final vote. Check stat choices and difficulty on both clients.
- Backpack panel visibility now follows an owner-only local open preference; native item use and the 30-slot bag/nine equipment slots remain active. Eight script-boundary regressions pass. Native frame binding, selection refresh, panel contents and simultaneous multiplayer interaction remain unverified. See docs/BACKPACK-PANEL-REPAIR.md.

## Install and test the current development build

1. Build the current map and install it to the dedicated test folder with:

       python -B tools/build_map.py --install-test-map

2. The installer archives old project maps and leaves one current map named `<build-id>-Development.w3m` in `Documents/Warcraft III/Maps/TheKingsLastStand/`. The game/editor may remain open if the map itself is closed; Windows must release the old file before replacement.
3. Test that installed map from the already-open World Editor when it points at the current map, or select the same build in Warcraft III → Single Player → Custom Game. Do not make another test copy.
4. Confirm the startup text includes the filename's build ID. Stop if a different or no build ID appears.
5. Select one of 25 hero previews, read role/abilities, and confirm. The chosen race determines your worker, Altar and build menu; duplicate heroes are allowed. If no choice is made within 45 seconds, the fallback is Paladin.
6. During hero selection, vote for Easy, Normal, Hard or Very Hard. Highest vote wins; ties and missing votes use Normal. After all players confirm, the initial preparation timer is 45 seconds.

The current package is development build `KLS-D-4e6ae863df` at `dist/KLS-D-4e6ae863df-Development.w3m` (SHA-256 `aa6276d4f1c2b4ca1b8f97562fee8c1a7bf52169300e7cca3f406036829de6d6`). It is installed in the dedicated test folder. Editor save/reopen, current-build Test Map, Custom Game, gameplay, purchase/crafting behavior, backpack multiplayer behavior and endurance remain pending. The earlier Test Map pass remains attributed to `KLS-D-fd638ddcf5` only. Check ROADMAP-AND-ACCEPTANCE.md for current status.

All four Crownlands settlements are reachable by connected roads: Crownshire (Human, south), Redtusk Hold (Orc, west), Moonbark Glade (Night Elf, east) and Wraithfall (Undead, north). Each has a race-themed shop that stocks its four Common-through-Epic universal items and healing/mana potions. Build your race's Foundry to buy one copy of its Legendary recipe, which combines that race's Rare and Uncommon items. The recipe pattern returns to your Foundry after success or failure. The Master Forge in the southern market stocks the three general recipes. Talk to settlement characters to start the optional four-chapter recovery story; it continues during active waves. Each starting mine holds 1,000,000 gold; Undead and Night Elf bases use owned Haunted or Entangled mines while Human and Orc bases use neutral Gold Mines.

Each gained hero level grants one skill point. Choose either a standard spell `+` upgrade or one of the `+3 STR`, `+3 AGI`, or `+3 INT` buttons above the ability grid. There is no automatic stat growth; each button spends that level's point, is repeatable and unranked, and adds exactly three points to its named stat. Every fifth level also offers a separate Vanguard, Skirmisher or Sage talent. Four Crownlands objectives can be started from their settlement characters at any time; they do not pause active waves.

## Match

- Defend King Aldric. The original Crownlands story lasts waves 1-40, then crossover assaults continue automatically. King Aldric's death ends the run; the HUD shows the highest wave reached.
- Work your own race-matched base and command your own army. You cannot control a teammate's units.
- Hire/use workers to mine gold, harvest nearby trees, and build within your own plot.
- Build on your plot only. Keep the central road open for attackers, defenders, siege units, and bosses.
- Use the separate Altar of Kings to choose/revive your hero.
- The southern market offers gear tiers, priced from 300 gold for Common to 20,000 gold for Legendary; Blade, Bow and Staff cost 1.5 times their rarity's base price. Inspect each shop's item icon and tooltip before buying. If stock is empty or the shop only shows unlabeled text, record the build ID and stop that shop test.
- Click Backpack in your hero's normal inventory to open the native equipment panel. It uses generic installed item `ebac`, with 30 storage slots and nine equipment positions. Multiplayer open/close independence still needs a two-player check. If the panel does not open, keep the item and report the exact build ID with a screenshot.
- To move bought gear between the 30-slot backpack, the five other normal inventory slots, and the nine equipment slots, drag the item through the native Forsaken Kingdom inventory panel. Gear can be sold back to a market vendor for half its listed price; boss relics remain unsellable. If a purchased item reports that it cannot equip, type `-gear` and `-diag` before trying again and send the complete output. The failed-purchase log now records the buyer unit/type/owner/life state, available normal slots, backpack occupancy, item location and owner, catalog family/equipment slot, and retry attempt. This gathers evidence for the still-unverified live equipment issue; it does not confirm that equip behavior is fixed.
- A player-owned defender kill pays its full bounty only to that player's resources. King Aldric's kill pays 25% of the bounty to each active player. The exact amount should appear in a recipient-only gold popup. Stronger enemies pay larger bounties.
- Each active player's hero within 1,200 range of a tracked enemy death receives the full XP award individually. Nearby heroes do not divide the XP; race and life state do not filter recipients. This custom award is source/package checked and needs in-game confirmation.
- Use King Aldric's Castle for heal/upgrade buttons. Contributions cost personal resources.
- Keeper of the Grove and Faelor Briarward have tree-targeting `AEfn` suppressed; use their Grove Awakening or Briarward Stand signature on open ground to summon Treants without a nearby tree.
- Normal breaks: 50 seconds. Before every boss wave: 180 seconds.
- During a preparation timer, vote Ready to start the next wave early. Everyone must vote; your vote can be toggled off while waiting. The existing timer starts the wave if the group is not unanimous.
- Normal enemies drop no equipment. Elites have a 1% chance of a Common or Uncommon item. Bosses grant personal milestone items; potion drops remain independent.
- The Restoring Spring is below/south-west of the castle. Active living heroes within 450 range quietly recover 1% of maximum HP and 1% of maximum mana every second while missing either resource. It no longer produces a healing burst effect or per-tick text.

## Diagnostic-only shortcuts

These are for development/testing and must not be treated as release controls:

| Chat text | Purpose |
|---|---|
| -help | Show diagnostic help |
| -gear | Report the hero’s six normal inventory slots, occupied backpack positions and nine equipment slots, showing each item’s catalog family/slot and owner marker. Failed market equip transactions additionally log buyer state, inventory capacity, item location and retry attempt; use `-diag` to capture those transaction lines |
| -diag | Show build ID, the latest 12 runtime events, the latest 8 ERROR/FATAL/WARN entries from a separate rolling buffer, each active player's expected/actual starting mine, owner, gold reserve and coordinates, plus difficulty/readiness state |
| -wave N | Start a diagnostic-selected wave 1-1000 |
| -gold | Add diagnostic gold/lumber |
| -repair | Exercise castle-heal transaction |
| -upgrade | Exercise castle-upgrade transaction |
| -power | Spend talent point on damage |
| -vitality | Spend talent point on maximum health |
| -wisdom | Spend talent point on intelligence |

## Reporting a problem

Include the exact on-screen build ID. For gear that will not transfer or equip, type `-gear` and provide its complete output plus `-diag`; occupied backpack slots are listed too. For missing units/buildings/items, type `-diag` and provide its complete output plus a screenshot. Error and warning entries are retained separately from routine messages, so recent spawn failures remain visible even after later gameplay logs fill the ordinary event window. The starting-mine line appears after hero confirmation and reports expected/actual mine, owner player ID, remaining gold and position. Required racial-mine spawn failures use the context `starting racial gold mine`. For engine or editor errors, run:

    python -B tools/collect_test_logs.py

Then provide the new snapshot folder name and note whether the game was launched through Custom Game or World Editor. `collection.json` lists build IDs and structured diagnostic severity/kind counts; `findings.txt` includes warning-only lines and explicit spawn/load failures with the nearest preceding build ID labeled as correlation only. If the current build ID is absent, copied errors cannot be attributed to it. Even a current map-open reference does not prove that the map was played; confirm the visible in-game identifier. Older logs may belong to earlier builds and must be kept separate.

## Town recovery and company research

Select the currently marked town contact to show its Begin/contribute button. Bring your living hero within 1,000 range. Northwatch clears four enemies; Crownshire sends a vulnerable supply caravan; Moonbark accepts 250 gold/100 lumber; Wraithfall offers the ritual encounter. The caravan moves only with a living escort within 900 range and can be restarted if lost. Objectives remain available while waves run. Attacking story threats, escorting, starting or funding records personal reward participation.

Town completions add watchposts, Greater Healing/Mana stock, four restoring refuges, then Restoration potions and racial garrisons. These shared unlocks last for the match. Refuges quietly regenerate 1% maximum HP/mana each second within 650 range.

Build your race’s Hall, Foundry, Siege Yard and arcane structure. Your hero buys personal research from their native item cards: three Company Chapters (unlocked through story or waves 10/20/30), three weapon ranks, three armor ranks, Counter-Siege and Spiritcraft Accord. Bring your living hero within 700 range; wrong-owner or obsolete purchases refund gold/lumber. Company recruits and supports have manual point-target powers costing 40 mana, with a 20-second cooldown. Full numbers: [company catalog](COMPANY-RESEARCH-AND-POWERS.md).

A level-1 hero has one normal skill point. Spell ranks and the three +3 stat buttons spend the same points. Every five levels, a separate talent row offers +5 STR/+200 HP/+2 HP regeneration, +5 AGI/+2% attack evasion, or +5 INT/+100 mana/+2 mana regeneration. These choices never pause the game.
