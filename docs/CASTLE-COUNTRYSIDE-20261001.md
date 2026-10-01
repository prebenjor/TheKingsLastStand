# Castle countryside handoff — 1 October 2026

Continue with `build/KLS-D-68303d69bf-Castle-Countryside-Final-R4-20261001.w3m`, SHA256 `8d04cabf92ef4ddf68559a66636f80d6603645d08804c13528cc60d7bfe822d6`. This DEVELOPMENT editor copy supersedes all earlier countryside candidates. It is open in the corrected Forge session. The installed release and canonical authored layer were not replaced.

The approved area is south of the existing hills, west and east of the castle and relocated market. Fourteen fitted routes and branches connect countryside destinations, pond shores and lookout approaches. Added scenery comprises three irregular lily ponds, two single-level lookout hills with broad ramps, roadside rests, an eastern pond overlook, a western broken cart, and 121 doodads: 47 trees, 18 lily pads, 12 crates, 12 shrubs, 10 lanterns, 10 rocks, seven signs, four benches and one cart. Existing encounters and rewards are unchanged.

## Placement fixes

Portal and forest monster creation IDs 146–158 now have native group ID -1 instead of 0. Every other property is preserved. Forge's creation defaults for units, start locations and doodads now use the ungrouped sentinel. The corrected executable is `../wc3-forge-compat/build/bin/wc3-forge-ungrouped.exe`, SHA256 `16fc5764c177fec22640864f6bd2d9a0eb157060e9fe2f771ae164f7e8168eaa`; the supplemental source patch is `tools/wc3-forge/native-group-default.patch`. Use the corrected session; the older Forge window contains a stale extracted working copy.

All 13 market vendors retain their roles, stock, recipes and services. Saved reference IDs 7–19 supply position and facing to `tools/layout_catalog.py`; runtime helpers and the editable trigger header are synchronized. Startup retains its existing preview-removal and one-vendor-per-role construction. Actual gameplay confirmation remains pending.

After moving shops, save the native map and run the import as a separate process before packaging:

```powershell
python -X utf8 -B tools/build_map.py --import-market-layout <saved-map-or-extracted-folder>
python -X utf8 -B tools/build_map.py --countryside-editor-map <saved-countryside-folder> --editor-baseline <archived-baseline-map> --editor-output <new-versioned-map>
python -X utf8 -B tools/build_map.py --verify-countryside <new-versioned-map> --countryside-folder <saved-countryside-folder> --editor-baseline <archived-baseline-map>
```

The import matches creation identities, not proximity or record order. Preserve those reference IDs. Existing output paths are refused. Terrain application uses `--dress-countryside <folder> --forge-lock <selected-lock>` through the same entry point. A partial checkpoint must be restored to its group boundary before replay; automatic partial replay is refused.

## Preservation and verification

The untouched original is `build/KLS-D-68303d69bf-Forest-Coves-Final-20261001.w3m`, SHA256 `c7d91e762808683fae708105b1d0fdda5cf21291cd4bcdc61e93b3a2db892929`. Its full archive and members are archived under `backups/countryside/20261001-c7d91e762808/`. The applied deterministic catalog and undo-group checkpoints are in `build/forge-session/20261001-castle-countryside/`.

The final `.preservation.json` confirms all 151 original unit records are unchanged except the 13 group fields; all 1,749 original doodad records and footer are unchanged. There are 1,454 changed terrain corners and 6,001 changed pathing pixels, confined to approved footprints, with zero protected terrain changes. All 2,193 sampled trail positions are walkable. Land props match saved ground, lilies use pond surface elevation, vendor coordinates and facings match the source, and unrelated runtime functions are preserved.

PJASS compilation passed. Native metadata, units and doodads round-trip byte-identically (151 units; 1,870 doodads). Five Forge test packages passed. Eight countryside handoff regressions passed. The complete Python suite ran 224 tests: 222 passed, with two existing failures in signature spell base IDs and a Human tower tooltip race label. Evidence is in `build/countryside-tests-final.log` and the final artifact's adjacent reports.

Static checks do not replace native playtesting. Still verify individual portal/monster selection in standard World Editor, all 13 shops appearing once with working inventories, and walking both routes, ramps and pond shores. Check entrances, floating props, flooding and cliff gaps, then run the existing gameplay smoke test. No native editor click test or Warcraft III gameplay run was available in this session.
