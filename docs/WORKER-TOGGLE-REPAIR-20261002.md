# Worker construction toggle repair — 2026-10-02

The user reported that the Night Elf toggle did nothing; the exact tested map is awaiting confirmation. Undead had previously failed in Prototype R2. Production expansion switching remains disabled until native acceptance; this revision does not claim either race has passed gameplay verification.

## Two reproduced defects

1. All eight forward/back Chaos morph records serialized `Cha1` at data pointer 1. Installed `AbilityMetaData.slk` defines `Cha1` as native `UnitID`, data pointer **0**. Correct both main and skin records to pointer 0, preserving field type 3, level 1, destination, parent, record extras and all surrounding bytes. The regression checked the actual installed metadata and failed before the fix, then passed for all eight definitions.
2. The 0.25-second idle refresh disabled the toggle while its own `channel` order was active. That can interrupt the button's cast before the spell-effect callback. The actual JASS handler regression reproduced disabling during Channel; it now remains active through that order. Gathering/repair/construction/transport restrictions remain.

The prototype now displays three diagnostic stages: toggle order received; button callback received; worker type changed or a failure with expected/actual types. On success it shows original/current handle and tells the player to open Build (B). The construction page itself changes inside the native Build menu, not the outer worker command card. The callback reports unregistered, busy or loaded/dead workers explicitly.

Forge's `value` represents the flat/base slot; leveled values are in `levels`. Earlier blank flat-value observations did not prove a missing target. Reopened level-one destinations are present for all eight morphs. Audit tooling now records per-level fields as well as flat fields. No new Forge compatibility patch or alternative construction menu is needed for these corrections.

## Current immutable artifacts

| Map | Build | SHA256 |
|---|---|---|
| KLS-Worker-Toggle-Repair-Gated-R2-20261002.w3m | KLS-D-768ef40c73 | e64e3901a574dba632653e38a9d1f792bfa4054992156cd1c3c0e0c00bce70b5 |
| KLS-Worker-Toggle-Prototype-R7-20261002.w3m | KLS-D-06e5f5f190 | 24a7017ee0517612426070e6a807944942f49dd264b60ce505a06d9a7f86f180 |

Baseline: latest saved racial repair map KLS-D-1f003ecdb7, SHA256 `2793d5d6f815709d46953568743864ccbf09b8ea55f3915206322158ca7b5c14`, archived with its contents. The supported `--racial-action worker-revision` creates a fresh folder, verifies the known malformed records and changes only the eight destination slots. MCP applies the corrections in its worker-definition undo group. Older prototypes including R5/R6 are superseded and must not be used for this retest.

## Verification

- Both maps compile against installed Warcraft JASS APIs (25,272 total lines including API files).
- Preservation comparison passes for main/skin typed records and archive contents: all 25 heroes, all 90 hero abilities, terrain/pathing/placements/items/countryside/economy/encounters remain unchanged. Exactly three runtime function bodies changed: worker cast, issued-order diagnostic and idle refresh. All other existing function bodies remain identical apart from build ID. Runtime and editable trigger bodies remain synchronized.
- Reopened MCP readback: 132 unit definitions, 148 abilities and 25 heroes, including per-level fields. Dedicated morph readback records all eight correct level-one destinations. This does not verify actual engine conversion.
- Native-format metadata v39, 151 units v13 and 1,870 doodads v13 round-trip byte-identically.
- Full suite: **245 tests, 243 pass, two known baseline failures** (AK21 source/native-parent expectation and Human tower tooltip). Both new regressions have recorded red/green runs.
- Native sale-popup discrepancy remains unresolved: 1,200 can display for the preserved actual 12,000 payment. No extra compensation and no inventory, healing, tome, loot or hero behavior changes are included.

## Required next native test

Open **Prototype R7**, build KLS-D-06e5f5f190. Use V on an idle Wisp, then press B to inspect the expansion construction page. Return to the outer card, use V again and press B for the standard page. Report the exact diagnostic messages if either step fails. Repeat with Acolyte, Peon and Peasant. Compare original/current handle, ownership, health, mana, food, abilities and carried resources; V must remain blocked during active work or loaded transport. Native construction, prerequisite paths, queue/refund/rally, specialist powers and multiplayer acceptance from the previous report are still pending.

If native switching fails again, use the stage messages to locate the failure before making another behavioral change. Keep production gated; do not silently replace the approved same-handle design.

[DEVELOPMENT prerelease and downloads](https://github.com/prebenjor/TheKingsLastStand/releases/tag/dev-20261002-worker-toggle-repair) include both maps, SHA/preservation manifests, morph readback, expanded audit and this verification report. Source and updated README/changelog are submitted through a follow-up PR; its main-page update awaits merge.
