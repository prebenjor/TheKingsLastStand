# Market square — 2026-10-01

Moved the existing market references 7–19 through Forge MCP, retaining rawcodes, ownership and scale. Four shops line the north side; three each line west, east and south. Cardinal facing points inward. Centre is (-576, -5760), perimeter spans X -1728..576 and Y -6912..-4608. No doodad or terrain mutation API was called.

Current editor artifact: `build/KLS-D-68303d69bf-Development-Forge-20261001-Market.w3m`.
SHA-256: `9897e6f63e3154904e03fd33effd0b1f0b2b85a8b228fdfbc0a0874d207241e1`.

Saved unit comparison proves only IDs 7–19 changed, with 102 total records retained. Terrain/pathing match the preserved human save. However saved doodad count is 1021 versus 1100 in the older preserved map. Switching to a pre-move extraction was blocked by automatic review because of unsaved changes; the live session was retained instead. No assumption is made that the 79 missing doodads were deliberately removed by the user; confirmation requested. Preserve all historical maps and do not transfer these doodad changes into authored source until resolved.

`tools/layout_catalog.py` records positions and generated `KLS_MarketFacing`; `source/shops.j` uses that facing for future runtime spawns. These source changes are not yet packaged into gameplay. Current editing artifact still has the prior runtime placement script. Full authored-layout integration remains pending.

Generated candidate JASS compiled with installed declarations and PJASS. No tests run. Visual entrance orientation and Warcraft navigation remain unverified; camera positioned over the square for human review.
