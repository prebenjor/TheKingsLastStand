# Player and human-test guide

## Launch the checked-in diagnostic

1. Copy dist/DIAGNOSTIC-KLS-D-fd638ddcf5.w3m into the Warcraft III Custom Game maps folder or install a newly built diagnostic with:

       python -B tools/build_map.py --install-diagnostic

2. Launch Warcraft III → Single Player → Custom Game → TheKingsLastStand → DIAGNOSTIC-KLS-D-fd638ddcf5.
3. Confirm the startup text includes KLS-D-fd638ddcf5. Stop if a different or no build ID appears.
4. Select a hero preview, read role/abilities, click Confirm. If no choice is made within 45 seconds, the fallback is Paladin.
5. After all players confirm, the initial preparation timer is 45 seconds.

The artifact is a development build. Shop/backpack and live multiplayer behavior is not yet certified. Check the exact current status in ROADMAP-AND-ACCEPTANCE.md.

## Match

- Defend King Aldric. Keep attackers off him; the final boss must die before the king.
- Work your own human base and command your own army. You cannot control a teammate's units.
- Hire/use workers to mine gold, harvest nearby trees, and build within your own plot.
- Build on your plot only. Keep the central road open for attackers, defenders, siege units, and bosses.
- Use the separate Altar of Kings to choose/revive your hero.
- The southern market offers gear tiers. Inspect each shop's item icon and tooltip before buying. If stock is empty or the shop only shows unlabeled text, record the build ID and stop that shop test.
- Use the Forsaken Kingdom backpack equipment panel to store/equip gear. If a purchase cannot be equipped, keep the item and report the full item name, slot, hero, build ID, and backpack screenshot.
- Use King Aldric's Castle for heal/upgrade buttons. Contributions cost personal resources.
- Normal breaks: 90 seconds. Before waves 10, 20, 30, 40: 180 seconds.
- The Restoring Spring is below/south-west of the castle. Active living heroes within 450 range recover 200 HP and 120 mana every 5 seconds.

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
