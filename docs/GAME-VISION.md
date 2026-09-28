# Game vision — The King's Last Stand

## One-sentence promise

Two to four friends choose different Warcraft heroes, build their own kingdom outposts along one defended road, and cooperate to keep King Aldric alive through forty escalating undead and demon assaults.

## The experience

The opening is a hero-selection courtyard. Players inspect twenty-five hero choices, their roles, native skill sets, and signature ability before confirming. The roster includes the original fifteen Warcraft heroes, verified Forsaken Kingdom campaign heroes Ilastar and the Forsaken Paladin, and eight new race-themed heroes. A confirmed hero sets that player's Human, Orc, Night Elf, or Undead workers and build menu independently. The invasion gathers beyond the northern wall, a stone road descends through the open central gate, four player plots line the defense row, and King Aldric's castle holds the center. Four allied race-themed settlements connect to the road across the 192 × 192 battlefield.

Each player develops a personal base and race-matched army. Workers gather lumber and gold, construct and repair faction-flavored buildings, recruit hero-matched troops, and place defensive structures. The selected hero explores the frontline, earns full nearby shared experience while keeping kill gold personal, learns safe extended spell ranks, chooses level-up stats and talents, and builds equipment through a persistent campaign backpack. King Aldric's own kills contribute a quarter bounty to every active player. Between waves the team prepares, heals at the castle or restorative spring, shops, crafts, advances optional town-recovery objectives, and adjusts defenses. Bosses interrupt the wave cadence with visible mechanics and personal rewards.

The tension comes from complementary responsibilities: heroes must meet pressure before it reaches the king, builders and towers need a clear route and firing lane, and each player must balance personal growth against contributions to the shared royal defense.

## Design pillars

1. **Co-op with personal ownership.** Players share an alliance, vision, road, boss rewards, and victory condition. Each player's selected hero determines their worker, trained troops, buildings and hero identity. Each player commands only their own army; there is no shared unit control.
2. **A recognizable Warcraft RPG.** Use native heroes, abilities, campaign backpack/equipment presentation, item art, buildings, and Definitive Edition assets. Custom systems should feel like Warcraft rather than a detached menu simulator.
3. **A real defense line.** The king, castle, open gate, road, player plots, resource access, and towers must occupy a coherent, navigable battlefield. Terrain art never overrides pathing.
4. **Long-term character growth.** Twenty-five choices, signature powers, level-up stat investments, five-level talents, a level-50 cap, safe extended spell ranks, equipment combinations and boss rewards support builds beyond the first few waves.
5. **Readable pressure.** A persistent wave/chapter/countdown HUD, enemy count, king health and tier, boss warnings, and personal revival status keep the objective obvious.
6. **Honest shipping.** A package or simulated test is not a successful Warcraft match. The map remains a development build until current-build editor, engine, multiplayer, and endurance checks pass.

## The battlefield drawn from the user's annotated layout

The map uses Warcraft world coordinates where positive Y is north and the view's top is north.

    NORTH
    undead and demonic spawn approach
    hills / ruins / woods / corrupted ground
    ======================================================  fortified north wall
    -------------------- OPEN GATE -----------------------
                         │
                         │  wide, unbuildable King's Road
       Player 1 plot     │      Player 2 plot
    [mine / Town Hall]   │   [mine / Town Hall]
       Player 3 plot     │      Player 4 plot
    [mine / Town Hall]   │   [mine / Town Hall]
    ========== horizontal defense row / red line ==========
                         │
                 [King Aldric's Castle]
                         │
            royal courtyard / restoration pool
                         │
    Quartermaster • quality shops • Archive • Apothecary
    SOUTH

The sketch is conceptual; implement coordinates and object footprints in source. The current layout constants put four plot centers at X = -6000, -3300, 3300, 6000 and Y = -500. The castle centers on X = 0, Y = -500; King Aldric stands north of it at (0, 350). The northern gate wall is at Y = 5200, with its broad permanent opening around the central road. Enemies spawn north at Y = 6200 and attack toward the king. The shop plaza is south of the plots around Y = -3900. The Restoring Spring is at (-900, -1600), south-west of the castle and away from the road.

The current terrain target is a readable 192 × 192-cell battlefield. Connected paved branches reach Crownshire, Redtusk Hold, Moonbark Glade, and Wraithfall. The main road is broad enough for bosses, siege units, escort groups, and defenders to pass. Four separate plots are horizontally aligned along the user's red line. The user's green line is a long northern wall with a clearly open central gate; do not leave unfortified side stretches. Buildable areas, gates, castle, towns, market, mines, forests, camera bounds, pathing, and minimap must agree.

## Non-negotiable product choices

- This is a new RPG scenario using the user's blank DE map. It is not a deprotection or adaptation of the third-party map originally considered at the start.
- Each selected hero race controls that player's matching worker and race-themed building roles. All four factions remain allies under King Aldric.
- Hero level 1 is the starting point and 50 is the current cap. Gain a +3 primary-stat investment each level and a separate secondary-stat talent every fifth level.
- The optional four-part Crownlands recovery story is shared for one match. Contributions remain personal for rewards, objectives stay available during waves, and story enemies are tracked outside the wave count.
- The heroes may be Human, Orc, Night Elf, or Undead; their team is still the human kingdom.
- Heroes can be duplicated across players.
- The first match supports one active player for diagnostics; the intended release supports 2–4 active defenders.
- Resource contribution and equipment purchases use each player's own resources. Markets are shared neutral facilities; rewards and purchased items belong to their buyer.
- The king is one neutral shared objective. His castle is the actual place to heal and upgrade him.
- The Forsaken Kingdom's native backpack/equipment system is the intended inventory UX; keeping an item in a six-slot-only shop delivery must not make that item unusable.
- Waves do not attack until selection and preparation timers complete.
- Four bosses occur at the end of each ten-wave chapter: 10, 20, 30, and 40.
