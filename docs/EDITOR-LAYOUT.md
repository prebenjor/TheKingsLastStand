# Editor-visible terrain work copy

The shops, towns, quest sites, castle, starting bases and hero hub are created by the runtime. They are absent from an ordinary package's native unit placement file. Terrain authors need visible footprints to shape roads, grass, scenery and clearings.

## Supported workflow

Run `python -X utf8 -B tools/build_map.py --prepare-editor` from the repository. The supported builder produces the normal Development package and one `build/<current-build>-Development-Terrain.w3m` work copy. It refuses to overwrite an existing work copy with that name.

The work copy contains 85 disposable unit references: 13 market buildings, 32 settlement structures/shops/quest sites, 25 hero choices, 12 starting hall/mine/altar references, and castle/king/spring. Four native start markers match the source plot positions. The provisional Human base references show footprints before race selection; selected heroes still determine their actual race independently in play.

Use this copy for terrain editing. Reference units belong to **Neutral Extra**, a reserved owner. Their model and unit type come from the normal generated object catalog. Labels and coordinates are listed in local `build/editor-layout.json`. The generated preview units have native object names in World Editor; gameplay names are applied by the runtime.

Save and close the work copy, then capture it with `tools/capture_authored_map.py --map <path>`. The normal six-layer capture retains terrain, pathing, doodads/destructables, shadows, minimap markers and map preview. It excludes unit placement data and gameplay objects. Archive the saved original before capture. Do not create new working copies from older build IDs or overwrite a map still open in the editor.

## Placement ownership

- `tools/layout_catalog.py` owns the shared market, castle, king, spring, hero grid and base offsets; plot centers come from `tools/map_info.py`.
- `tools/town_catalog.py` owns settlement placements. Towers resolve through `tools/faction_catalog.py`; hero types come from `tools/hero_catalog.py`.
- Both compiled JASS and editable trigger export use these generated coordinates.
- Moving a reference unit in World Editor does **not** move the gameplay building. To move gameplay, update the relevant placement catalog, rebuild, and prepare a new current work copy. Tell the user this limitation before asking them to reposition references.
- Units manually added to the editor are not imported by art capture. Put decorative scenery in the Doodad Palette. Functional units and buildings require a source/catalog change.

## Runtime and format safeguards

`KLS_Init` removes all Neutral Extra references before creating landscape/gameplay objects. The function survives the WCT trigger export, so an editor-generated Test Map also carries the cleanup. Reserve Neutral Extra exclusively for these references; do not put gameplay units under that owner.

The installed/normal Development package contains only the four native start markers, with no layout references. The work copy changes only `war3mapUnits.doo`; all six art members are compared byte-for-byte against the package after packing.

`tools/editor_layout.py` emits the installed editor's 13.11 fixed unit record format. The 131-byte compatibility fixture in `tests/fixtures/editor-unit-13-11.bin` came from the user's own saved map (SHA-256 `ebb2f449b5363b16daf4a23a5e193754df438cc3252cbb3ddaaf9d04c1db3a82`). Its classic fields align with the [mdx-m3-viewer unit serializer](https://github.com/flowtsohg/mdx-m3-viewer/blob/master/src/parsers/w3x/unitsdoo/unit.ts); DE-specific reserved fields are preserved from the native save. Do not extend this fixed-record writer to inventory/drop/ability tables without a new verified format fixture.

## Pending engine checks

Open the current Terrain work copy in World Editor and confirm all shops, four settlements, hero hub and castle render in the expected locations. Save/reopen, then Test Map: references should disappear and the normal objects should appear once. Check placement collision and pathing after editor save, including reference-building footprints, resource access, gate and boss clearance. The editor connection is currently unavailable, so no visual open/reopen pass is claimed. Keep DEVELOPMENT and carry the earlier successful Test Map `KLS-D-fd638ddcf5` forward as a historical pass.
