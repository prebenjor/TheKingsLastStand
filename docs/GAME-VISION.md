# Game vision — The King's Last Stand

## One-sentence promise

Two to four friends choose different Warcraft heroes, build their own kingdom outposts along one defended road, and cooperate to keep King Aldric alive through the forty-wave Crownlands campaign and endless cross-campaign assaults.

## The experience

The opening is a hero-selection courtyard. Players inspect twenty-five hero choices, their roles, native skill sets, and signature ability before confirming. The roster includes the original fifteen Warcraft heroes, verified Forsaken Kingdom campaign heroes Ilastar and the Forsaken Paladin, and eight new race-themed heroes. A confirmed hero sets that player's Human, Orc, Night Elf, or Undead workers and build menu independently. The invasion approaches through the user's cliff-based frontier passages, four player plots line the defense row, and King Aldric's castle holds the center. Crownshire, Moonbark Glade and Wraithfall connect to the road across the 192 × 192 battlefield. The user removed Redtusk Hold and added a troll camp; those authored choices supersede the old four-village/gate layout.

Each player develops a personal base and race-matched army. Workers gather lumber and gold, construct and repair faction-flavored buildings, recruit hero-matched troops, and place defensive structures. The selected hero explores the frontline, earns full nearby shared experience while keeping kill gold personal, learns safe extended spell ranks, chooses level-up stats and talents, and builds equipment through a persistent campaign backpack. King Aldric's own kills contribute a quarter bounty to every active player. Between waves the team prepares, heals at the castle or restorative spring, shops, crafts, advances optional town-recovery objectives, and adjusts defenses. Bosses interrupt the wave cadence with visible mechanics and personal rewards.

The tension comes from complementary responsibilities: heroes must meet pressure before it reaches the king, builders and towers need a clear route and firing lane, and each player must balance personal growth against contributions to the shared royal defense.

## Design pillars

1. **Co-op with personal ownership.** Players share an alliance, vision, road, boss rewards, and victory condition. Each player's selected hero determines their worker, trained troops, buildings and hero identity. Each player commands only their own army; there is no shared unit control.
2. **A recognizable Warcraft RPG.** Use native heroes, abilities, campaign backpack/equipment presentation, item art, buildings, and Definitive Edition assets. Custom systems should feel like Warcraft rather than a detached menu simulator.
3. **A real defense line.** The king, castle, cliff passages, road, player plots, resource access, and towers must occupy a coherent, navigable battlefield. Terrain art never overrides pathing. The user's hand-authored terrain, doodads and unit placements set the visual direction.
4. **Long-term character growth.** Twenty-five choices, signature powers, level-up stat investments, five-level talents, a level-50 cap, safe extended spell ranks, equipment combinations and boss rewards support builds beyond the first few waves.
5. **Readable pressure.** A persistent wave/chapter/countdown HUD, enemy count, king health and tier, boss warnings, and personal revival status keep the objective obvious.
6. **Honest shipping.** A package or simulated test is not a successful Warcraft match. The map remains a development build until current-build editor, engine, multiplayer, and endurance checks pass.

## The battlefield drawn from the user's annotated layout

The map uses Warcraft world coordinates where positive Y is north and the view's top is north.

    NORTH
    undead and demonic spawn approach
    hills / ruins / woods / corrupted ground
    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^  cliff frontier
    ---------------- NAVIGABLE PASSAGE -------------------
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

The sketch is conceptual; implement saved coordinates and footprints in source. The existing layout constants put four plot centers at X = -6000, -3300, 3300, 6000 and Y = -500. The castle centers on X = 0, Y = -500; King Aldric stands north of it at (0, 350). Former gate spawns at Y = 5200 must yield to the user's authored cliffs after handoff. Enemies currently spawn north at Y = 6200 and attack toward the king; review this route against the new passages. The shop plaza is around Y = -3900 and the Restoring Spring at (-900, -1600), subject to saved placement changes.

The terrain target is a readable 192 × 192-cell battlefield. Connected paths reach Crownshire, Moonbark Glade and Wraithfall; the removed Orc village must not be regenerated. The main route and cliff passages must accommodate bosses, siege units, escorts and defenders. Preserve four personal plots, the user's new troll camp and their authored composition. Buildable areas, cliffs, castle, settlements, market, mines, forests, bounds, pathing and minimap must agree. See [EDITOR-LAYOUT-REVISION.md](EDITOR-LAYOUT-REVISION.md) for the user decisions and pending source integration.

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
- Keep the original chapter bosses at waves 10, 20, 30, and 40. After the Crownlands story, continue automatically into endless waves with a boss every ten waves; King Aldric's death ends the run.
