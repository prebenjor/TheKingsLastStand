# Editor workshop handoff and integration

## Human handoff

Copy this after each chapter. Names/rawcodes are enough; the saved map supplies field values and coordinates.

```text
Chapter:
Saved map:
Saved and closed: yes

Moved/deleted/added buildings:
Changed hero/building/item/ability objects:
Changed or added triggers:
Checks that passed:
Problems still present:
Screenshots, if useful:
```

For Chapter 0, “Chapter 0 baseline saved and closed” plus the current path is sufficient. Do not report a baseline save as a gameplay test.

## Agent protocol

### 1. Preserve a native baseline

Only after the human confirms **saved and closed**, run from the repository root:

```powershell
python -X utf8 -B tools/editor_workshop.py baseline --chapter 1 --map "build/KLS-D-68303d69bf-Development-Terrain.w3m" --closed
```

Chapter 0 establishes the **chapter-1** baseline. The command refuses an untouched generated package, stale build, changed reference identity/ownership or unsupported native unit format. It archives the exact map with SHA-256, member hashes and creation-ID labels under ignored `backups/editor-workshop/`. Record the returned `baseline.json` path in the progress ledger. Do not substitute the older native editor save.

Before a later chapter on a newly generated map, ask the human to save/close that copy once **before editing** and establish its chapter-specific native baseline. If the same native file is still being used, archive its integrated state as the next chapter baseline; keep the correct chapter number and original build provenance.

### 2. Review the chapter handoff

```powershell
python -X utf8 -B tools/editor_workshop.py review --chapter 1 --map "build/KLS-D-68303d69bf-Development-Terrain.w3m" --baseline "backups/editor-workshop/<baseline-folder>/baseline.json" --closed
```

Replace the placeholder with the returned real path. The report archives the complete edited map and writes `review.json`, readable `review.md`, and a full `script.diff` when JASS changed. It verifies baseline bytes, build identity and chapter. Output folders are immutable; an existing folder is not overwritten.

Review includes:

- All archive member additions, removals and byte changes, including unrecognized files.
- Coverage against active MPQ hash entries; unnamed/unlisted files are flagged for manual review even when unchanged. Their original bytes remain in the archived map.
- The six terrain/dressing members independently from gameplay data.
- DE 13.11 unit records, including optional inventory/ability/drop tables. Units match creation numbers, never nearest coordinates. Moves/facing/owner changes and replacements are reported.
- Object v2/v3 fields in units/items/abilities/destructables/doodads/buffs/upgrades, keyed by table, object rawcode, field, rank and data pointer. Version wrappers/order changes are normalized; unknown editor metadata remains visible.
- Trigger and custom script member hashes, changed JASS functions, and full script differences including globals/generated sections.

**Limits:** the tool does not translate GUI trigger binaries or automatically import gameplay. Unknown formats, replaced identities, added/deleted objects and trigger changes remain review tasks. The complete saved archive is preserved even if a decoder cannot interpret a member. Native default pruning during a later save can still occur; resolve reported deletions against installed data and human intention rather than assuming every byte change is deliberate.

### 3. Port deliberate changes

1. Review the human report together with semantic differences. Record a disposition for **every** changed member: ported, editor serialization only, intentionally disabled/deferred, or unresolved with explanation.
2. Capture the six art layers using the existing current-build `tools/capture_authored_map.py --map <saved-map>` command. This imports no units/objects/triggers.
3. Port unit positions and facing to the matching layout/town/base source. Add individual placement/facing support where the current shared offsets/formulas cannot represent a move. Do not shift all mines because one mine moved.
4. Review dependent king attack orders, spring range center, castle interactions, shop proximity, hero preview selection/camera, plot bounds, start locations, quest/refuge/escort/encounter coordinates and resource tree routes. Mark intentional deletion or replacement clearly.
5. Port Object Editor deltas to the owning catalog/generator. Account for rank units and shared spell users. Register new rawcodes and update runtime references. Regenerate item/company/power documentation when affected.
6. Translate approved GUI/custom-script behavior into the appropriate runtime module. Preserve user-authored lesson triggers deliberately, including disabled status; do not paste the whole compiled `war3map.j` over the runtime. Review variables, events, synchronization and initialization exactly once.
7. Add relevant regressions and run the approved checks. Build once through `tools/build_map.py`; archive the old editing copy before preparing the next. Use `--prepare-editor` for one current editing copy and `--install-test-map` when preparing the next gameplay check.
8. Check archive readback, art hashes, runtime coordinates/facing and duplicate prevention. Current engine results must be obtained separately; syntax/static tests do not prove multiplayer or pathing.
9. Add the new build's dated changelog entry and progress-ledger evidence: map/hash, imported changes, checks, unresolved deltas, next human chapter and exact new file path. Preserve earlier Test Map success.

Do not declare a chapter integrated while known changes have silently disappeared. If mapping is ambiguous, preserve/report it and ask a concise question about that object while continuing independent changes.

## Workshop progress

| Chapter | Status at workshop setup |
|---|---|
| 0 Native baseline | Awaiting human save/close of KLS-D-68303d69bf Terrain copy |
| 1 Castle/market | Not started |
| 2 Bases/races | Not started |
| 3 Villages | Not started |
| 4 Heroes | Not started |
| 5 Spells | Not started |
| 6 Triggers/AI introduction | Not started |
| 7 Gameplay/finish | Not started |

Update statuses only from actual handoffs and recorded checks. The workshop ends at Chapter 7; full endurance is a separate task.

## Decoder references

Object v3 per-object metadata and ranked field layout follow the primary [War3Net simple object reader](https://github.com/Drake53/War3Net/blob/master/src/War3Net.Build.Core/Serialization/Binary/Object/SimpleObjectModification.cs) and [ranked field reader](https://github.com/Drake53/War3Net/blob/master/src/War3Net.Build.Core/Serialization/Binary/Object/LevelObjectDataModification.cs). DE unit 13.11 layout is checked against our own installed-editor fixture. Native format changes must be investigated and covered by regression fixtures; do not guess offsets and discard bytes.
