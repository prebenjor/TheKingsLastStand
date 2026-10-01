# Authored layout integration review — 1 October 2026

## Preserved input

Immutable saved map: `backups/wc3-forge/20261001-f9c9276256ed/KLS-D-68303d69bf-Development-Terrain.w3m`.
SHA-256: `f9c9276256edd2531f37efa9a029e0334bb1f71dfa3ac7c297a98cff26ea55da`. Build identity: KLS-D-68303d69bf. This is an already edited human save, not a clean Chapter 0 baseline. The active Forge copy is separate; no map was saved or modified during this review.

## Placement findings

- 102 native records, including four start markers.
- 64 original references retain their type but have moved.
- 12 original reference IDs now carry different types. These are replacements/reused IDs, not safely identifiable original objects.
- 13 additional placement IDs contain new units, buildings and mines.
- The eight Redtusk reference IDs now contain different objects. Do not restore the removed village.
- Four original new-hero preview IDs now contain buildings. Preserve those buildings; hero selection must retain all 25 functional choices without assuming these replacement records are the old heroes.
- Added camp units include Neutral Hostile (24); added homes include Neutral Extra (26), and mines/farm objects include Neutral Passive (27). A blanket Neutral Extra cleanup or art-only capture would lose authored objects.

Full machine-local report: `build/layout-review/saved-placement-audit.json`. It compares the immutable save to generated reference metadata; it does not import anything or classify native object/trigger serialization as intentional gameplay edits.

## Reused placement identities

| Creation ID | Original role | Saved type |
|---|---|---|
| 28 | Redtusk Hold / ogre | `kT20` |
| 29 | Redtusk Hold / obar | `emow` |
| 30 | Redtusk Hold / otrb | `emow` |
| 31 | Redtusk Hold / ofor | `nfoh` |
| 32 | Redtusk Hold / kA01 | `nmoo` |
| 33 | Redtusk Hold / hS00 | `ngno` |
| 34 | Redtusk Hold / kQ01 | `ngnw` |
| 35 | Redtusk Hold / kT10 | `ngnv` |
| 73 | Hero choice 22 | `h001` |
| 74 | Hero choice 23 | `h001` |
| 75 | Hero choice 24 | `h001` |
| 76 | Hero choice 25 | `hhou` |

## Safe next integration steps

1. Port the 64 unambiguous moved references by role, including facing and dependent gameplay coordinates. The castle is now (0, -704), spring (-1536, -1728); Aldric remains (0, 350). Markets are clustered south-west rather than the old spread-out grid.
2. Preserve replacements and additions in a dedicated authored placement catalog; retain their existing owner, rawcode, scale and facing. Separate disposable references from authored Neutral Extra buildings before changing cleanup.
3. Disable Redtusk town spawns, relocate its services to existing market/contact objects, and guard absent town sites in restoration/garrison logic. Keep four playable race indices.
4. Reconcile Crownshire, Moonbark and Crown Ritual Service contacts, encounters and escort waypoints with their moved placements. Do not infer navigation from XY positions alone.
5. Capture all six art layers from this immutable saved revision. Port reviewed unit/object changes separately before packaging; no art-only package is acceptable because it would omit the additions.
6. Remove procedural gate spawns so they cannot overlay the authored cliffs. Preserve the 25-choice selection system without putting functional previews on replacement buildings.
7. Build a new versioned copy only after authored unit/reference dispositions are complete. Never overwrite the currently open Forge file. Verify pathing and visual placement in Warcraft separately.

## AI source correction completed this pass

Wave troops, bosses and boss reinforcements now use `KLS_OrderInvader` to attack-move to the living king's actual position. Idle redirection retains its eight-second cadence and does not interrupt an active attack/spell. Missing/dead objectives, null/dead invaders and ended matches do not receive new orders. This changes source behavior only; the currently installed package remains KLS-D-68303d69bf until the full preserved-layout integration is ready.
