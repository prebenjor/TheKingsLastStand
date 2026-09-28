# Player and human-test guide

## Install and test the current development build

1. Build the current map and install it to the dedicated test folder with:

       python -B tools/build_map.py --install-test-map

2. The installer archives old project maps and leaves one current map named `<build-id>-Development.w3m` in `Documents/Warcraft III/Maps/TheKingsLastStand/`. If Warcraft III currently has an older map open, close the game before installing so Windows releases the old file.
3. Test that installed map from the already-open World Editor when it points at the current map, or select the same build in Warcraft III → Single Player → Custom Game. Do not make another test copy.
4. Confirm the startup text includes the filename's build ID. Stop if a different or no build ID appears.
5. Select a hero preview, read role/abilities, click Confirm. If no choice is made within 45 seconds, the fallback is Paladin.
6. After all players confirm, the initial preparation timer is 45 seconds.

The current artifact is a development build. The user reports Test Map succeeded on the earlier build `KLS-D-fd638ddcf5`; that pass is recorded for that build. The current map `KLS-D-3a0464e019` is not yet installed or run. Check the status in ROADMAP-AND-ACCEPTANCE.md.

## Match

- Defend King Aldric. Keep attackers off him; the final boss must die before the king.
- Work your own human base and command your own army. You cannot control a teammate's units.
- Hire/use workers to mine gold, harvest nearby trees, and build within your own plot.
- Build on your plot only. Keep the central road open for attackers, defenders, siege units, and bosses.
- Use the separate Altar of Kings to choose/revive your hero.
- The southern market offers gear tiers. Inspect each shop's item icon and tooltip before buying. If stock is empty or the shop only shows unlabeled text, record the build ID and stop that shop test.
- Use the Forsaken Kingdom backpack equipment panel to store/equip gear. If a purchase cannot be equipped, keep the item and report the full item name, slot, hero, build ID, and backpack screenshot.
- To move bought gear between the 30-slot backpack, the five other normal inventory slots, and the nine equipment slots, drag the item through the native Forsaken Kingdom inventory panel. Gear can be sold back to a market vendor for half its listed price; boss relics remain unsellable.
- Enemy kills show a gold popup for the personal share credited to each active defender. Stronger enemies pay larger bounties.
- Use King Aldric's Castle for heal/upgrade buttons. Contributions cost personal resources.
- Normal breaks: 90 seconds. Before waves 10, 20, 30, 40: 180 seconds.
- The Restoring Spring is below/south-west of the castle. Active living heroes within 450 range recover 1% of maximum HP and 1% of maximum mana every second while missing either resource.

## Diagnostic-only shortcuts

These are for development/testing and must not be treated as release controls:

| Chat text | Purpose |
|---|---|
| -help | Show diagnostic help |
| -diag | Show build ID and recent runtime creation/error diagnostics |
| -wave N | Start a diagnostic-selected wave 1–40 |
| -gold | Add diagnostic gold/lumber |
| -repair | Exercise castle-heal transaction |
| -upgrade | Exercise castle-upgrade transaction |
| -power | Spend talent point on damage |
| -vitality | Spend talent point on maximum health |
| -wisdom | Spend talent point on intelligence |

## Reporting a problem

Include the exact on-screen build ID. For missing units/buildings/items, type -diag and provide its complete output plus a screenshot. For engine or editor errors, run:

    python -B tools/collect_test_logs.py

Then provide the new snapshot folder name and note whether the game was launched through Custom Game or World Editor. Older logs may belong to earlier builds and must be kept separate.
