# Build changelog

Keep one entry for every packaged build. The entry names the exact immutable build ID, summarizes the user-visible changes, lists verification evidence, and leaves engine-only checks pending until a person tests that exact map. Add the entry in the same source change as the build; do not reuse an old build ID for changed map contents.

## KLS-D-1739daf903 - 2026-09-29

- Extended the local log collector to include warning-only lines and explicit spawn/load failures, and to serialize each finding with severity, event kind, file/line, nearest preceding build ID, and a correlation-only provenance label. `collection.json` now summarizes error, fatal, warning, failure, spawn/load, and total counts.
- Full source regression suite passed **142/142**. Installed-editor JASS syntax and MPQ package/readback passed. Package SHA-256: `807f84919dd59097d31157fd8aabfe8de1c11661b32951a4df028114a06d1940`.
- Fresh snapshot `test-results/20260929T053054106327Z-KLS-D-1739daf903` has no current-build references and does not confirm gameplay. It reports 8 spawn/load failures, all following older `KLS-D-1a040d638c` map-open lines; the raw lines identify model-creation failures. No warning/error/fatal lines were found in the captured logs.
- Later captures after opening the map in World Editor and attempting a direct game launch are recorded in `test-results/20260929T055307058783Z-KLS-D-1739daf903` and `test-results/20260929T055724787319Z-KLS-D-1739daf903`. The direct launch log records the current build path on its command line, but no `Opening map` line for this build; the client remained open and the second capture had zero diagnostics. Neither capture confirms an in-game build ID or gameplay.
- Package `dist/KLS-D-1739daf903-Development.w3m`; prior dist package archived under `backups/development-builds/20260929T053034101646Z-KLS-D-1739daf903/`. Installed at `Documents/Warcraft III/Maps/TheKingsLastStand/KLS-D-1739daf903-Development.w3m`; installed SHA-256 matches and it is the only project map in the test folder. The replaced map remains preserved under `backups/installed-diagnostics/20260929T051420166893Z-KLS-D-660b4bdeea/`.
- Editor save/reopen, Test Map, Custom Game, gameplay, multiplayer and endurance remain pending for this exact build. The earlier Test Map pass remains assigned to `KLS-D-fd638ddcf5` only.

## KLS-D-660b4bdeea - 2026-09-29

- Updated `tools/collect_test_logs.py` to extract build IDs from captured Warcraft/Editor logs, separate current-build references from other builds, and label errors with their nearest preceding build ID as correlation only. The output explicitly says a map-open reference is not proof of gameplay or causality.
- A fresh capture at `test-results/20260929T051531256402Z-KLS-D-660b4bdeea` contains only older `KLS-D-1a040d638c` references. The captured model-creation failures follow those older map-open lines; there are no references to this build and no evidence it was played.
- Full source regression suite passed **141/141**. Installed-editor JASS syntax and MPQ package/readback passed. Package SHA-256: `719de46b17be26b7165d59d3f47e6d13b98117af9b77de1270077e39e78f74eb`.
- Package: `dist/KLS-D-660b4bdeea-Development.w3m`; prior dist package archived under `backups/development-builds/20260929T051420156254Z-KLS-D-660b4bdeea/`. Installation was attempted after the user closed the visible editor, but Windows returned `WinError 32` while removing the prior installed `KLS-D-7951d852c3-Development.w3m`. Windows Restart Manager identified a remaining `World Editor.exe` process (PID 22184) as the lock holder. The prior map remains in the test folder; the installer preserved an additional copy under `backups/installed-diagnostics/20260929T051420166893Z-KLS-D-660b4bdeea/`. The current build is not installed.
- Editor save/reopen, Test Map, Custom Game, gameplay, multiplayer and endurance remain pending for this exact build. The earlier Test Map pass remains assigned to `KLS-D-fd638ddcf5` only.

## KLS-D-7951d852c3 - 2026-09-29

- Expanded failed gear-purchase/equip diagnostics with the buyer's unit type, owner and life state; free normal-inventory slots; backpack occupancy; item location (normal inventory, backpack, equipped or missing); item type/owner; catalog family and equipment slot; and the retry attempt. The equip behavior itself is unchanged pending a playtest that captures these states.
- Full source regression suite passed **139/139**. Installed-editor API syntax and MPQ package readback passed. Package SHA-256: `42922eb38fd46bd6f6071fef7df08f4329e4abd921d8773bdfc32286f9421b1c`.
- Installed at `Documents/Warcraft III/Maps/TheKingsLastStand/KLS-D-7951d852c3-Development.w3m`; installed SHA-256 matches the package and it is the only project map in the test folder. The previous development artifact was archived under `backups/development-builds/20260929T044600046703Z-KLS-D-7951d852c3/`; the replaced installed map was preserved under `backups/installed-diagnostics/20260929T044600056810Z-KLS-D-7951d852c3/`.
- Editor save/reopen, Test Map, Custom Game, live gear purchase/transfer/equip/sale, gameplay, multiplayer and endurance remain pending for this build. The earlier Test Map pass remains attributed to `KLS-D-fd638ddcf5` only.

## KLS-D-b1609a439c - 2026-09-29

- Moved each base's eight-tree lumber stand closer to its hall, from roughly 650/850 map units south to 500/700. The trees remain on the rear-right side, away from the north-side mine route and western Altar approach.
- Full source regression suite passed **138/138**, including the new base-tree placement check. Installed-editor API syntax and MPQ package readback passed. Package SHA-256: `a3fef077af70c0395591f5862e71f431ac4d394062ad2c526ec82787fabd4221`.
- Installed at `Documents/Warcraft III/Maps/TheKingsLastStand/KLS-D-b1609a439c-Development.w3m`; installed SHA-256 matches the package and it is the only project map in the test folder. The previous development artifact was archived under `backups/development-builds/20260929T042649668175Z-KLS-D-b1609a439c/`; the replaced installed map was preserved under `backups/installed-diagnostics/20260929T042649676236Z-KLS-D-b1609a439c/`.
- The user confirmed testing a build but did not identify its build ID or result. This build's editor save/reopen, Test Map, Custom Game, tree harvesting/path clearance, gameplay, multiplayer and endurance checks remain pending. The earlier Test Map pass remains attributed to `KLS-D-fd638ddcf5` only.

## KLS-D-0235a0878b - 2026-09-29

- Extended the development-only `-gear` audit to list occupied backpack positions through the installed `UnitItemInBagSlot` API, in addition to all six normal inventory and nine equipment slots. Rows include item name/type, catalog family and equipment slot, plus owner marker; the header reports backpack occupancy and capacity.
- Full source regression suite passed **137/137**. Installed-editor API syntax and MPQ package readback passed. Package SHA-256: `70bce2bdbb91cdfbc762a182022a6552cfd96a027ae06579fea610a0709c0608`.
- Installed at `Documents/Warcraft III/Maps/TheKingsLastStand/KLS-D-0235a0878b-Development.w3m`; its SHA-256 matches the package and it is the only project map in the test folder. The previous development artifact was archived under `backups/development-builds/20260929T035722408473Z-KLS-D-0235a0878b/`; the replaced installed map was preserved under `backups/installed-diagnostics/20260929T035722417789Z-KLS-D-0235a0878b/`.
- The user reported testing a build but did not include its visible build ID or result. This build’s editor save/reopen, Test Map, Custom Game, gear purchase/equip flow, gameplay, multiplayer and endurance remain pending. The earlier Test Map pass remains attributed to `KLS-D-fd638ddcf5` only.

## KLS-D-2e8d369d67 - 2026-09-29

- Added a development-only `-gear` audit. It reports all six normal inventory slots and nine native equipment slots, including item name/type, catalog family and equipment slot, owner marker, and backpack capacity. This distinguishes a transfer failure from a slot or ownership problem during the next playtest.
- Full source regression suite passed **137/137**. Installed-editor API syntax and MPQ package readback passed. Package SHA-256: `e4460019b48eb32ce11afafed4fa776259e14d99182d652c9aac60470b59434b`.
- Installed at `Documents/Warcraft III/Maps/TheKingsLastStand/KLS-D-2e8d369d67-Development.w3m`; its SHA-256 matches the package and it is the only project map in the test folder. The previous development artifact was archived under `backups/development-builds/20260929T035024781689Z-KLS-D-2e8d369d67/`; the replaced installed map was preserved under `backups/installed-diagnostics/20260929T035024790640Z-KLS-D-2e8d369d67/`.
- The user reported testing a build but did not include its visible build ID or result. This build’s editor save/reopen, Test Map, Custom Game, item purchase/equip flow, gameplay, multiplayer and endurance remain pending. The earlier Test Map pass remains attributed to `KLS-D-fd638ddcf5` only.

## KLS-D-5604bb3f70 - 2026-09-29

- Enemy loot now uses explicit Normal/Elite/Boss profiles. Gear chances are 3% / 10% / 50%, with higher rarity weights for stronger tiers. Independent potion chances are 4% / 8% / 18%; one death can drop both items. Active killers own their drops, and unbound catalog gear receives its owner marker when picked up so equipment stats apply.
- Full source regression suite passed **136/136**. Installed-editor API syntax and MPQ package readback passed. Package SHA-256: `8e80a85f14a289f61bbf23260423754f1d3fee0441fee0882dfddefa479576bd`.
- Installed at `Documents/Warcraft III/Maps/TheKingsLastStand/KLS-D-5604bb3f70-Development.w3m`; its SHA-256 matches the package and it is the only project map in the test folder. The previous development artifact was archived under `backups/development-builds/20260929T032904554623Z-KLS-D-5604bb3f70/`; the replaced installed map was preserved under `backups/installed-diagnostics/20260929T032904564518Z-KLS-D-5604bb3f70/`.
- The user reported testing a build but has not identified its visible build ID or outcome. This build's editor save/reopen, Test Map, Custom Game, live drop/pickup behavior, gameplay, multiplayer and endurance remain pending. The earlier Test Map pass remains attributed to `KLS-D-fd638ddcf5` only.

## KLS-D-f97ab841cb - 2026-09-29

- `-diag` now counts each logged `ERROR` once in its summary across unit, scenery, item, recipe and retry failures. The separate 32-entry ERROR/FATAL/WARN ring and recent-eight display remain in place.
- Full source regression suite passed **134/134**. Installed-editor JASS syntax and MPQ package readback passed. Package SHA-256: `0abf819494aa3829f972e89ddb5b4e8acd60f1432057fb7a77fd56ca196be8b5`.
- Installed at `Documents/Warcraft III/Maps/TheKingsLastStand/KLS-D-f97ab841cb-Development.w3m`; its SHA-256 matches the package and it is the only project map in the folder. The previous development artifact was archived under `backups/development-builds/20260929T025854076991Z-KLS-D-f97ab841cb/`; the replaced installed map was preserved under `backups/installed-diagnostics/20260929T025854085811Z-KLS-D-f97ab841cb/`.
- The user reported completing a test but did not give the visible build ID or result. Current-build Editor save/reopen, Test Map, Custom Game, error-count/`-diag` capture, gameplay, multiplayer and endurance remain pending. The earlier Test Map success remains a pass for `KLS-D-fd638ddcf5` only.

## KLS-D-6d3db36ecf - 2026-09-29

- Failed recipe output delivery now logs the recipe, item, owner, buyer and coordinates before cleanup. Failed queued boss/story reward creation and each retry log the item name/code, owner and base coordinates; queue/retry behavior remains unchanged.
- Full source regression suite passed **133/133**. Installed-editor JASS syntax and MPQ package readback passed. Package SHA-256: `4612c5a61bd95ee06ce46dec9bf67c2f01f413eca5771029c015de41b455a478`.
- Installed at `Documents/Warcraft III/Maps/TheKingsLastStand/KLS-D-6d3db36ecf-Development.w3m`; its SHA-256 matches the package and it is the only project map in the folder. The previous development artifact was archived under `backups/development-builds/20260929T025141544693Z-KLS-D-6d3db36ecf/`; the replaced installed map was preserved under `backups/installed-diagnostics/20260929T025141553541Z-KLS-D-6d3db36ecf/`.
- The user reported completing a test but did not give the visible build ID or result. Current-build Editor save/reopen, Test Map, Custom Game, injected failures, live `-diag` capture, gameplay, multiplayer and endurance remain pending. The earlier Test Map success remains a pass for `KLS-D-fd638ddcf5` only.

## KLS-D-ca295479e8 - 2026-09-29

- Recipe output delivery rejection now writes a contextual `ERROR` entry to `-diag` before removing the unaccepted item. The log includes recipe/output names, owner, buyer and coordinates; ingredients are restored and the recipe fee is refunded as before.
- Full source regression suite passed **132/132**. Installed-editor JASS syntax and MPQ package readback passed. Package SHA-256: `d18491eab2479068d3a46e3b6065956bc6d858ffeebd3df9e73d9023329d1697`.
- Installed at `Documents/Warcraft III/Maps/TheKingsLastStand/KLS-D-ca295479e8-Development.w3m`; its SHA-256 matches the package and it is the only project map in the folder. The previous development artifact was archived under `backups/development-builds/20260929T023958709775Z-KLS-D-ca295479e8/`; the replaced installed map was preserved under `backups/installed-diagnostics/20260929T023958717683Z-KLS-D-ca295479e8/`.
- The user reported completing a test but did not give the visible build ID or result. Current-build Editor save/reopen, Test Map, Custom Game, injected delivery failure, live `-diag` capture, gameplay, multiplayer and endurance remain pending. The earlier Test Map success remains a pass for `KLS-D-fd638ddcf5` only.

## KLS-D-69ca4b4a50 - 2026-09-29

- Failed recipe-output item creation now writes a contextual `ERROR` entry to `-diag` with the recipe pattern, expected output item/rawcode, owner, and buyer coordinates. The existing component restoration and full recipe-fee refund remain in the failure path.
- Full source regression suite passed **131/131**. Installed-editor JASS syntax and MPQ package readback passed. Package SHA-256: `e79ff920dba8f96dcab993b3b6f1e8fad487670f7cf86102580e5e8ec7423352`.
- Installed at `Documents/Warcraft III/Maps/TheKingsLastStand/KLS-D-69ca4b4a50-Development.w3m`; its SHA-256 matches the package and it is the only project map in the folder. The previous development artifact was archived under `backups/development-builds/20260929T022610362928Z-KLS-D-69ca4b4a50/`; the replaced installed map was preserved under `backups/installed-diagnostics/20260929T022610371251Z-KLS-D-69ca4b4a50/`.
- Current-build Editor save/reopen, Test Map, Custom Game, injected recipe-output failure, live `-diag` capture, gameplay, multiplayer, and endurance remain pending. The earlier user-reported Test Map success remains a pass for `KLS-D-fd638ddcf5` only.

## KLS-D-f873a5b24f - 2026-09-29

- `-diag` now records ERROR/FATAL/WARN messages in a separate 32-entry rolling buffer. The command displays the latest eight severity messages alongside the most recent 12 ordinary runtime events, so routine log traffic no longer pushes spawn and setup failures out of view.
- Full source regression suite passed **130/130**. Installed-editor JASS syntax and MPQ package readback passed. Package SHA-256: `30fd0594806fd7e2cf9294b6750bb6ecc6e3855d9261852e01ab03fbe51c6d6e`.
- Installed at `Documents/Warcraft III/Maps/TheKingsLastStand/KLS-D-f873a5b24f-Development.w3m`; the installed SHA-256 matches the package and it is the only project map in the folder. The prior development artifact was archived under `backups/development-builds/20260929T020518521798Z-KLS-D-f873a5b24f/`; the replaced installed map was preserved under `backups/installed-diagnostics/20260929T020518530798Z-KLS-D-f873a5b24f/`.
- Current-build editor save/reopen, Test Map, Custom Game, live inspection of retained spawn warnings, gameplay, multiplayer, and endurance remain pending. The earlier user-reported Test Map success remains a pass for `KLS-D-fd638ddcf5` only.

## KLS-D-87a1bcd5c4 - 2026-09-29

- Hardened recipe restocking for a destroyed Foundry: Warcraft may retain a unit type on a dead structure handle, so the transaction now checks that the seller is alive before restocking it and otherwise falls back to the Master Forge.
- Full source regression suite passed **129/129**. Installed-API syntax compilation and MPQ package readback passed. Package SHA-256: `018fb3e6874134451308b961ea969e7f8a45c42c0e9c7123d1a7526aa404a5c1`.
- Installed at `Documents/Warcraft III/Maps/TheKingsLastStand/KLS-D-87a1bcd5c4-Development.w3m`; installed SHA-256 matches the package and it is the only project map in the folder. Its predecessor was preserved in `backups/development-builds/20260929T012822061855Z-KLS-D-87a1bcd5c4/` and `backups/installed-diagnostics/20260929T012822070939Z-KLS-D-87a1bcd5c4/`.
- Exact-build Editor save/reopen, Test Map, Custom Game, Hall appearance, Foundry shop/crafting, multiplayer, and endurance checks remain pending. The earlier user-reported Test Map success remains assigned to `KLS-D-fd638ddcf5`.

## KLS-D-91a75a0cc8 - 2026-09-29

- Cleared native parent abilities, training stock, and upgrades from the custom Hall/Foundry/Siege Yard records before applying their intended runtime behavior; this prevents the distinct Hall models from exposing unrelated native buttons. Tightened race-specific Foundry flavor text to fit the building tooltip.
- Full source regression suite passed **129/129**. Package tests also confirmed all four Hall parents and Foundry shop abilities exist in installed Warcraft data.
- Installed-API syntax compilation and MPQ package readback passed. Package SHA-256: `678a5fdf6c3af59381e107589fbc0c598da0e91a6e497bc3e42e9f04cd958a77`.
- Installed at `Documents/Warcraft III/Maps/TheKingsLastStand/KLS-D-91a75a0cc8-Development.w3m`; installed SHA-256 matches the package and it is the only project map in the folder. The preceding Development package remains in the local archive.
- Exact-build Editor save/reopen, Test Map, Custom Game, Hall appearance, Foundry shop/crafting, multiplayer, and endurance checks remain pending. The earlier user-reported Test Map success remains assigned to `KLS-D-fd638ddcf5`.

## KLS-D-cd91ba0b91 - 2026-09-29

- Replaced the duplicate keep/Town Hall parents on the four Halls of Banners with distinct installed race buildings: Gryphon Aviary, Orc Bestiary, Hunter's Hall, and Tomb of Relics.
- The Master Forge now stocks only the three general recipes. Each constructed racial Foundry opens an item shop with its own owner's matching Legendary pattern; the existing +20% company/support troop upgrade remains. Recipes return to the vendor that sold them after success or failure, and a destroyed vendor falls back to the Master Forge.
- Added regressions first; they failed against the duplicate Hall models and central-only Foundry stock. Focused race-building, equipment, recipe, Crownlands, and mining suites passed **50/50**; full source suite passed **129/129**.
- Installed-API syntax compilation and MPQ package readback passed. Package SHA-256: `529f8f825be5bfb550113f310a946c9ee7f157e792841cab32a01b34e60636eb`.
- Installed at `Documents/Warcraft III/Maps/TheKingsLastStand/KLS-D-cd91ba0b91-Development.w3m`; installed SHA-256 matches the package and it is the only project map in the folder. Prior development and installed maps were preserved in `backups/development-builds/20260929T011713544264Z-KLS-D-cd91ba0b91/` and `backups/installed-diagnostics/20260929T011713552898Z-KLS-D-cd91ba0b91/`.
- Exact-build Editor save/reopen, Test Map, Custom Game, Hall appearance, Foundry shop/crafting, multiplayer, and endurance checks remain pending. The earlier user-reported Test Map success remains assigned to `KLS-D-fd638ddcf5`.

## KLS-D-3bc9fcaf25 - 2026-09-29

- Corrected vendor stock overflow that hid shop entries: generic rarity shops now stock only the sixteen general equipment families, each town vendor keeps its matching race relics, and all seven recipe patterns have a dedicated Master Forge vendor. Recipe scrolls return to the Forge after either successful or failed crafting.
- Racial town shops sell their four Common-through-Epic items and two potions; their Legendary item is no longer directly stocked and can be crafted through its race's Foundry recipe. Existing enemy-drop rules remain active. Every vendor remains at or below Warcraft's twelve stock-slot limit.
- The new regressions failed first against the mixed generic stock and overfilled Rare Arms vendor. Focused equipment/recipe/town/market tests passed **40/40**; full source regression suite passed **128/128**.
- Installed-API syntax compilation and MPQ package readback passed. Package SHA-256: `ad398a4b564882b25406a7dd0b75b4d8627b31d7f47a4995979afd0d45f576b3`.
- Installed at `Documents/Warcraft III/Maps/TheKingsLastStand/KLS-D-3bc9fcaf25-Development.w3m`; installed SHA-256 matches the package. Replaced package and test map are preserved in the local development and installed-map archives.
- Current-build editor save/reopen, Test Map, Custom Game, native shop windows, Legendary crafting, multiplayer and endurance remain pending. The earlier user-reported Test Map success remains assigned to `KLS-D-fd638ddcf5`.

## KLS-D-2fd59dee88 - 2026-09-29

- Undead Acolyte conversion of a neutral Gold Mine now uses the shared optional checked-spawn helper. A missing or wrong-type Haunted Gold Mine is recorded with context, counted by `-diag`, and leaves the original mine and its gold intact without aborting the match.
- The regression failed against the direct uncounted `CreateUnit` call, then passed after routing through the checked helper. Focused race-mining tests: **12/12 passed**; the full source suite was **125/125** when the map was packaged. A follow-up manifest-alignment regression keeps current-build references synchronized across the README and guides; the current source suite is **126/126 passed**.
- Package archive readback and installed-editor API syntax checks passed. Package SHA-256: `90204c470bd78cfb9c31abb4bf9768af31aea420d7f9330a1887664231456f91`.
- Installed at `Documents/Warcraft III/Maps/TheKingsLastStand/KLS-D-2fd59dee88-Development.w3m`; installed SHA-256 matches the package, and the test folder contains one project map.
- Current-build Editor save/reopen, Test Map, Custom Game, mine-haunting gameplay, multiplayer, and endurance checks remain pending. The earlier user-reported Test Map success remains assigned to `KLS-D-fd638ddcf5`.

## KLS-D-2aa1705c84 - 2026-09-29

- Tier-two town-hall upgrades now require each faction's custom Altar rawcode and matching Barracks/upgrade building: Castle (hcas), Stronghold (ostr), Tree of Ages (etoa), and Halls of the Dead (unp1). This makes the Altars available in the racial build menus satisfy the native upgrade requirements.
- The regression was added first and failed for all four native upgrade targets, then passed after the object-data fix. Full source suite: **125/125 passed**.
- Package archive readback and installed-editor API syntax checks passed. Package SHA-256: edd432c6f16f5c628f63c6956b842b97ab2e66faff9e531395e8b4012f84b5b0.
- Installed on 2026-09-29 at Documents/Warcraft III/Maps/TheKingsLastStand/KLS-D-2aa1705c84-Development.w3m; the installed SHA-256 matches the package and the test folder contains one project map.
- Editor save/reopen, current-build Test Map, Custom Game, town-hall upgrades in Warcraft, gameplay, multiplayer and endurance checks remain pending. The earlier user-reported Test Map success remains assigned to KLS-D-fd638ddcf5.

## KLS-D-fdee19fa63 - 2026-09-29

- `-diag` now reports the caller's currently selected units, including object name, unit name, raw type ID, owner and coordinates. It reports up to 12 units so the displayed selection can be compared with the race-assigned worker.
- Full source regression suite: **124/124 passed**. Package archive readback and installed-editor API syntax checks passed.
- Package SHA-256: `6e591f5af710a3c6654d65743c957bf3308902c291907f6fec6090361367fa14`.
- Installed on 2026-09-29 at `Documents/Warcraft III/Maps/TheKingsLastStand/KLS-D-fdee19fa63-Development.w3m`; installed SHA-256 matches the package manifest, and the folder contains one project map.
- Editor save/reopen, current-build Test Map, Custom Game, gameplay, multiplayer and endurance checks remain pending. The earlier user-reported Test Map success remains assigned to `KLS-D-fd638ddcf5`.

## KLS-D-4a67348b4e - 2026-09-29

- The optional King's Restoring Spring visual now uses the shared checked spawn wrapper with the `restoring spring visual` context. Failed creation is logged and counted in diagnostics without aborting the match or disabling the coordinate-based regeneration timer.
- Full source regression suite: **123/123 passed**. Package archive readback and installed-editor API syntax checks passed.
- Package SHA-256: `a013631ed88293b9d4c2610015152135eb3a7a9456e5b119cc2b8c211560aff4`.
- Installed on 2026-09-29 at `Documents/Warcraft III/Maps/TheKingsLastStand/KLS-D-4a67348b4e-Development.w3m`; the installed SHA-256 matches the package manifest, and the folder contains one project map.
- Editor save/reopen, current-build Test Map, Custom Game, gameplay, multiplayer, and endurance checks remain pending. The earlier user-reported Test Map success remains assigned to `KLS-D-fd638ddcf5`.

## KLS-D-81285a4cc0 - 2026-09-29

- `-diag` now reports each active player's expected and actual starting mine, actual owner player ID, remaining gold, and coordinates. Failure to create a race-specific starting mine now logs the specific required-spawn context `starting racial gold mine`.
- Full source regression suite: **122/122 passed**. Package archive readback and installed-editor API syntax checks passed.
- Package SHA-256: `21540054f1250628fa1095ad42ee68bb986982a2f421c89b421574de827398cc`.
- Installed on 2026-09-29 at `Documents/Warcraft III/Maps/TheKingsLastStand/KLS-D-81285a4cc0-Development.w3m`; the installed SHA-256 matches the package manifest, and the folder contains one project map.
- Editor save/reopen, current-build Test Map, Custom Game, actual starting mine ownership/mining, all other live gameplay, multiplayer, and endurance checks remain pending. The earlier user-reported Test Map success remains assigned to `KLS-D-fd638ddcf5`.

## KLS-D-dd3a53babf - 2026-09-28

- Removed the tree-targeted native `AEfn` spell from Keeper of the Grove and Faelor Briarward whenever hero spell ranks are applied. Their tree-free Grove Awakening/Briarward Stand signature spells remain available for summoning Treants on open ground.
- Full source regression suite: **120/120 passed**. Package archive readback and installed-editor API syntax checks passed.
- Package SHA-256: `f2d804924a18aaab17ff00ed8d61b321a7fda54278a08e77559c3fcf6ab666cf`.
- Installed on 2026-09-29 at `Documents/Warcraft III/Maps/TheKingsLastStand/KLS-D-dd3a53babf-Development.w3m`; the test-folder SHA-256 matches the package manifest, and the folder contains one project map. The prior map is retained in `backups/installed-diagnostics/20260928T192844325669Z-KLS-D-8669a44192/`.
- Re-ran the full source regression suite on 2026-09-29: **120/120 passed**. Current-build editor save/reopen, Test Map, Custom Game, Keeper/Faelor casting, mine ownership/mining, shop/economy behavior, multiplayer, and endurance checks remain pending. The earlier user-reported Test Map success remains assigned to `KLS-D-fd638ddcf5`.


## KLS-D-f5fd3c5993 - 2026-09-28

- Undead and Night Elf players now start with an already-owned Haunted or Entangled Gold Mine at their base. Both retain the full 1,000,000-gold reserve; Human and Orc mines remain neutral. Additional neutral Undead mine haunting now recognizes Warcraft's native `hauntgoldmine` order.
- Raised equipment base prices to Common 300, Uncommon 1,000, Rare 3,000, Epic 8,000 and Legendary 20,000 gold. Blade/Bow/Staff cost 1.5× base; the three original recipe fees doubled to 5,000/7,000/12,000, racial Legendary recipes cost 9,000, and attribute tomes cost 1,000/3,000/8,000. Consumables and item stats are unchanged.
- Full source regression suite: **119/119 passed**. Package archive readback and installed-editor API syntax checks passed.
- Package SHA-256: `490a89b9445bc1d7af961bb8374222ca2af9cd3dbd356c6e8e29d352bed89351`.
- The package remains in `dist/`; Warcraft III PID `36140` is still running with the older installed map, so this build was not installed. The user-reported Test Map success remains assigned to `KLS-D-fd638ddcf5`. Current-build editor save/reopen, Test Map, Custom Game, mine harvesting, shop/economy behavior, multiplayer and endurance checks remain pending.


## KLS-D-c6f02bf50d - 2026-09-28

- Optional spawn failures now include useful context in `-diag` while allowing the match to continue for scenery, ability effects, signature summons, boss reinforcements, and optional Crownlands encounters. Required map setup and wave enemy/boss spawns still stop the match if creation fails; a partially created optional story encounter is cleaned up and remains retryable.
- Preserved the hero-panel `+3 Strength`, `+3 Agility`, and `+3 Intelligence` skills for per-level stat selection. There is no per-level stat dialog in this package; the separate specialty talent dialog remains every fifth level.
- Full source regression suite: **116/116 passed**. Package archive readback and installed-editor API syntax checks passed.
- Package SHA-256: `0869d7fa5bb3f1f67744768648c7690e7365193a402777a23e878fee73637ad0`.
- The package remains in `dist/`; Warcraft III PID `36140` still holds the older installed map, so this build was not installed. Current-build editor save/reopen, Test Map, Custom Game, gameplay, multiplayer, and endurance remain pending. The user-reported Test Map success remains assigned to `KLS-D-fd638ddcf5`.

## KLS-D-25463efa09 - 2026-09-28

- Kept the requested level-up choices in the hero ability panel as native `+` skills: `KSTR`, `KAGI`, and `KINT` each grant +3 to one primary stat per level. The old global stat-choice dialog is absent from current source; only the separate fifth-level specialty talent uses a dialog.
- Failed random enemy item drops now log the item name/rawcode, enemy type and coordinates, and killer player ID, so missing loot-object creation is visible in the diagnostic log.
- Full source suite: **113/113 passed**. Package member readback and installed-editor JASS syntax checks passed.
- Package SHA-256: `d1a5d81cc66998f526103738d0164388b24467306bdc9b73e9d6ec02f087b03d`.
- Installation safely stopped because Warcraft III PID `36140` still holds the old `KLS-D-1a040d638c-Development.w3m`. The old test map and its verified archive remain intact; this build is packaged in `dist/` but not installed. Current-build editor save/reopen, Test Map, Custom Game, gameplay, multiplayer and endurance checks remain pending. The earlier user-reported Test Map pass remains assigned to `KLS-D-fd638ddcf5`.

## KLS-D-2f2397cf14 - 2026-09-28

- Boss relics and Crownlands story items now share a guarded personal-reward delivery path. Failed `CreateItem` calls retain the item rawcode in that owner's queue and retry every five seconds during the match; full inventory leaves a visible owner-bound item at the owner's base.
- Added source regressions for boss/story routing, null-handle guards, owner-bound fallback and retry bookkeeping. Full suite: **112/112 passed**. Installed-editor JASS compilation and package member readback passed.
- Package SHA-256: `e63d8c15d90458056887f056ac66d1194aa30326e20ec94847f5ac91e2d7310f`.
- Installation was attempted but safely stopped because Warcraft III still locks the older `KLS-D-1a040d638c-Development.w3m`; its original and one hash-verified archive copy remain intact. This current build remains packaged in `dist/` and is not installed. Editor save/reopen, current-build Test Map/Custom Game, live item delivery, gameplay, multiplayer and endurance remain pending. The earlier user-reported Test Map pass remains assigned to `KLS-D-fd638ddcf5`.


## KLS-D-0227009b20 - 2026-09-28

- Carries forward the gameplay content of `KLS-D-8669a44192`; no hero, wave, item, or race behavior changed. This package has a new build ID because the supported installer code changed and is part of the build fingerprint.
- Hardened Windows installation: old maps are copied and hash-verified before removal, an exact existing archive is reused on retry, and failed removal or new-map copy restores prior files when possible. A locked-map error leaves the running map untouched and does not leave a partial new install.
- Installer regressions: **6/6 passed**. Full source suite: **108/108 passed**. Package readback and installed-editor API syntax checks passed.
- Package SHA-256: `23a7887af12f726ddffe37ab4b9e817c021ba46a2842ced4ce80a53297f43a6c`.
- Installation safely stopped because Warcraft III still holds `KLS-D-1a040d638c-Development.w3m`. The original remains in the test folder and has one byte-identical archived recovery copy at `backups/installed-diagnostics/20260928T192844325669Z-KLS-D-8669a44192/KLS-D-1a040d638c-Development.w3m` (SHA-256 `eaee0e501b3e7ced381bda7c93c530d79499faad94f2bb80304a9aeb1340e362`). `KLS-D-0227009b20` remains packaged in `dist/`, not installed. The earlier user-reported Test Map pass remains assigned to `KLS-D-fd638ddcf5`; all checks for this exact build remain pending.

## KLS-D-8669a44192 - 2026-09-28

- Replaced the per-level stat dialog with three native hero `+` skills: `KSTR`, `KAGI`, and `KINT` each add three points to the chosen primary stat per rank. The separate every-fifth-level specialty choice remains.
- Corrected the Undead Temple parent to native `utod`, retaining the Temple model, icon, training and research data. Added race-specific descriptions for altars, arcane/support buildings, towers, Hall of Banners, Foundries and Siege Yards. Sanctuary-style towers share a 15 HP / 3-second / 650-range ally-heal hook.
- Added Undead Acolyte neutral-gold-mine haunting with gold preservation and owner harvest order. Extended Night Elf Tree of Life Entangle range to reach its starting mine. Default player race preference is Random; hero choice applies the selected race per player.
- Preserved the authored first 40 waves and added ten bounded, repeating campaign rosters for Naga, Blood Elf, Fel Orc, Burning Legion, and Scourge forces. Wave 49 converges all five factions; Wave 50 adds the installed campaign Lady Vashj boss. Later bosses recur every ten waves, rotate through installed campaign leader records, and reuse the telegraphed slam, summon, and tower suppression mechanics.
- Continued live-wave count, health, damage, bounty, XP, and tracked-enemy accounting through endless waves. Waves 50 and later grant each active player a personal Legendary item from the equipment catalog; waves 10-40 retain their existing relic rewards. Wave 40 continues automatically; King Aldric's death ends the run and the HUD records the highest wave.
- Kept campaign unit models, animations, movement, and armor sourced from the installed Definitive Edition tables. Added a generated 50-row roster catalog and synchronized the wave, gameplay, Crownlands, decisions, roadmap, and contributor documents.
- Full automated regression suite: **105/105 passed**. Build-manifest checks `archive_readback` and `syntax_installed_api` are recorded as passed; the packaged artifact hash matches the manifest.
- Package SHA-256: `b7d0b41039d0cd4d655daf97d40a0329d443f987c62e9a927c87a8fc7bb995a0`.
- Installation first archived a verified copy of prior map `KLS-D-1a040d638c` but could not move its original. A retry on 2026-09-28 confirmed a running Warcraft III process still locks that file. The original and archived copy both have SHA-256 `eaee0e501b3e7ced381bda7c93c530d79499faad94f2bb80304a9aeb1340e362`; no current-build file was installed. Exit Warcraft III completely and rerun `python -B tools/build_map.py --install-test-map`. Editor save/reopen, Test Map, Custom Game, plus-button behavior, race-specific mine orders, Temple UI, campaign-unit visuals and pathing, wave 40-50 and later-boss gameplay, multiplayer, and endurance checks remain pending. The earlier user-reported Test Map success remains a pass for `KLS-D-fd638ddcf5`.

## KLS-D-1a040d638c - 2026-09-28

- Carries forward the complete Crownlands expansion and Sacred Aura tooltip work described in the previous entry.
- Fixed supply-escort contribution tracking: any active defender who joins while the caravan is already travelling is now recorded for that chapter's personal story reward. The escort contributor is recorded only after its caravan successfully spawns.
- Added a regression for the second-player join path. Full automated regression suite: **88/88 passed**. Package member readback, installed-editor API syntax and archive verification passed.
- Package SHA-256: `eaee0e501b3e7ced381bda7c93c530d79499faad94f2bb80304a9aeb1340e362`. Installed at `C:\Users\asphy\Documents\Warcraft III\Maps\TheKingsLastStand\KLS-D-1a040d638c-Development.w3m`; installed hash matches.
- Supersedes `KLS-D-41d103f7cb`, which is archived locally. World Editor is now open on this exact installed map and the editor window is responsive; save/reopen, Test Map, Custom Game, in-game feature checks, multiplayer and endurance remain pending. The earlier user-reported Test Map success remains a pass for `KLS-D-fd638ddcf5`.

## KLS-D-41d103f7cb - 2026-09-28

- Expanded the battlefield to 192×192 and placed four connected allied settlements: Human Crownshire, Orc Redtusk Hold, Night Elf Moonbark Glade and Undead Wraithfall. Kept the defense road, gate, player plots and existing wave cadence; terrain, pathing, camera bounds and minimap were rebuilt together.
- Hero choice now sets each player's race independently, including the matching Peasant, Peon, Wisp or Acolyte, Town Hall, Altar, construction menu, towers and race-flavored Hall of Banners, Foundry and Siege Yard. Shared construction roles and costs remain catalog-driven.
- Added eight race-native heroes (two per race), custom signature abilities and matching company/support recruits. The roster now has 25 choices; heroes begin at level 1 and cap at 50, with a visible +3 primary-stat choice per level and a separate Strength/Agility/Intelligence talent choice at every fifth level.
- Added the four-stage optional Crownlands recovery story, which can progress during active waves without altering wave counts or timers. Shared unlocks and personal contributor rewards last through the match.
- Added 20 universal race-themed gear items (five standard rarity tiers per race), with item names/tooltips colored white, green, blue, purple and gold. Shop stock, stats, drops, icons and four race-specific Legendary Foundry recipes use the shared item catalog.
- Fixed Sacred Aura learned and learn-menu descriptions for both `AHas` and `AHpa`; rank 4 displays 38.5% resistance / 27.5% healing received, rank 5 displays 42% / 30%, and the learn menu distinguishes current from next rank.
- Full automated regression suite: **87/87 passed**. Package readback, installed-editor API syntax checks and archive verification passed. Package SHA-256: `67f363beac6ce79313916026016a34b8458b35c648e7d27db46f0af370308928`.
- Installed at `C:\Users\asphy\Documents\Warcraft III\Maps\TheKingsLastStand\KLS-D-41d103f7cb-Development.w3m`; installed SHA-256 matches the package. Previous development and installed maps were archived under `backups/development-builds/` and `backups/installed-diagnostics/`. Current-build editor save/reopen, Test Map, Custom Game, live feature checks, multiplayer and endurance remain pending. The earlier Test Map success remains a pass for `KLS-D-fd638ddcf5`.

## KLS-D-b5ae4ab2fe - 2026-09-28

- Added safe extended ranks through rank 5 and set the hero level cap to 50. Installed native ranks remain unchanged. Beyond a spell's native maximum, only its explicitly registered power fields grow by 10% of the last authored value per rank; every other field holds the final authored value. Warden Blink stays capped at its native three ranks. Sacred Aura rises from 35% magic resistance to 38.5% at rank 4 and 42% at rank 5, avoiding the stale 500% value.
- Checked all registered effect fields against the installed editor metadata. Covered damage, healing, armor, evasion, aura bonuses, and other direct effects. Skills without a safe registered effect stay at their native rank limit.
- Applied standard rarity colors to equipment and boss relic names, tooltip quality headings, and quality-shop names: white, green, blue, purple, and gold. Item tiers and full stat descriptions remain visible.
- Full source regression suite: **79/79 passed**. Package readback and installed-editor API syntax passed.
- Map SHA-256: `05a072b826318b5d40d9cacda0f9e3755c845093f618f7bfb227da3fd7ec5da7`.
- Installed at `C:\Users\asphy\Documents\Warcraft III\Maps\TheKingsLastStand\KLS-D-b5ae4ab2fe-Development.w3m`; installed hash matches the package. Current-build editor save/reopen, Test Map, Custom Game rank/color presentation, gameplay, multiplayer, and endurance checks remain pending. The earlier Test Map pass stays attributed to `KLS-D-fd638ddcf5`.

## KLS-D-8b5076c3eb - 2026-09-28

- Stopped extending regular hero spells beyond the `levels` count in the installed Warcraft ability data. The map now preserves each ability's authored native ranks and caps runtime rank-ups to that spell's own limit.
- Removed generic numeric extrapolation. It treated every numeric field as a scalable effect; for example, Warden Blink's native mana costs 50/10/10 became 0 at generated rank 4. Unsupported higher ranks are no longer emitted or assigned.
- Regression coverage checks native-rank caps for every selectable hero spell and the Blink mana-cost case. Full regression suite: **77/77 passed**.
- Package member readback and JASS syntax against the installed editor API passed.
- Map SHA-256: `10f6d56f3811cece7189633f8b840746f72c34583ec41e28752e2f50396545c3`.
- Installed at `C:\Users\asphy\Documents\Warcraft III\Maps\TheKingsLastStand\KLS-D-8b5076c3eb-Development.w3m`; installed hash matches the package. Current-build editor save/reopen, Test Map, Custom Game rank behavior, gameplay, multiplayer, and endurance checks remain pending. The earlier Test Map pass stays attributed to `KLS-D-fd638ddcf5`.

## KLS-D-a2dae2be8c - 2026-09-28

- Fixed recipe delivery so a successful craft no longer falls through into the failure refund path. If the output cannot be delivered, the failure notification and fee refund still run once.
- Added a regression check for the contradictory success/failure notification and duplicate-refund path.
- Focused recipe/progression regression tests: **14/14 passed**. Full regression suite: **77/77 passed**.
- Package member readback and JASS syntax against the installed editor API passed.
- Map SHA-256: `e86d0c0e1696897d8727d243bf6bc92bd6f5ce8ca6b6b39a8d24ae38668dbd9d`.
- Installed at `C:\Users\asphy\Documents\Warcraft III\Maps\TheKingsLastStand\KLS-D-a2dae2be8c-Development.w3m`; its SHA-256 matches the package. Current-build editor save/reopen, Test Map, Custom Game craft interaction, gameplay, multiplayer, and endurance checks remain pending. The earlier Test Map pass stays attributed to `KLS-D-fd638ddcf5`.

## KLS-D-1398318c4a - 2026-09-28

- Fixed the high-rank aura data that made Sacred Aura grant 500% magic resistance at rank 4. Installed campaign records declare these auras as three-rank abilities but contain stale fourth-rank values; rank generation now respects each record's declared level count and resolves fields through the internal ability code, including the Forsaken Paladin's `AHpa` alias.
- The same stale-rank handling was corrected for other native abilities, including Devotion Aura. Ranks 1–3 keep their installed values; later ranks continue from those declared values.
- Regression tests: **76/76 passed**. MPQ member readback and installed-editor API JASS syntax passed.
- Map SHA-256: `b7fe3601272d32c7d95e23fb7b50470ee6e39ca40bc914d0e9c2c14fa6016af2`.
- The package is at `dist/KLS-D-1398318c4a-Development.w3m`. Installing into the dedicated Warcraft III test folder stopped because the prior `KLS-D-5b63d38dc0-Development.w3m` is locked. A verified archive copy of the old map is preserved; the old file remains in the test folder until it is closed. Current-build in-game rank behavior and the editor Test Map remain pending; the earlier Test Map success remains attributed to `KLS-D-fd638ddcf5`.

## KLS-D-5b63d38dc0 - 2026-09-28

- Player-owned kills award the full role bounty only to the killing unit's player. King Aldric's kills award 25% of the bounty to every active player. Both use the recipient-only gold notification.
- Each active hero within 1,200 world units receives a full individual kill-XP award. Warcraft's native shared XP divides experience, so native normal/hero kill XP and native shared XP are disabled; the runtime awards the Warcraft default unit-level progression or hero-kill XP value to each nearby hero. Race and life state are not used as recipient filters.
- King Aldric's acquisition range is 900 to enable his attack bounty route. Ordinary wave breaks are now 50 seconds, while pre-boss breaks remain 180 seconds.
- Restoring Spring restores 1% maximum HP and mana every second within range without a healing effect, floating text, or timed notification.
- Shop-purchased gear is moved to an available normal inventory slot when possible. Vendor resale now obtains the manipulated/pawned item from the correct event native. Both behaviors still require live backpack/shop verification.
- Adds Hall of Banners, Royal Foundry, Siege Yard, and 34 hero-specific company/support unit records for the 17 selectable heroes. Their recruiting, doctrines, upgrade effect, placement, and multiplayer ownership remain engine-pending.
- Full source regression suite: **75/75 passed** after adding this build's changelog entry. Package member readback and installed-editor API JASS syntax passed. The earlier run's only failure was the changelog guard detecting that the newly generated ID was undocumented; this entry resolves it.
- Map SHA-256: `560b662379fb23969ad2528f53d2623667125760e89d050e6a2dd6c5e8781bc8`.
- Installed at `Documents/Warcraft III/Maps/TheKingsLastStand/KLS-D-5b63d38dc0-Development.w3m`; the installed hash matches the package. Editor save/reopen, current-build Test Map, Custom Game gameplay, XP/gold behavior, item UI, multiplayer, and endurance checks remain pending. The earlier Test Map pass stays attributed to `KLS-D-fd638ddcf5`.

## KLS-D-49ab762fcd - 2026-09-28 (superseded before installation)

- Intermediate package included personal player kill gold, King Aldric's 25% bounty for each active player, silent one-second spring regeneration, 50-second normal breaks, and the hero-company building/unit slice.
- Package inventory/readback and installed-editor API syntax passed. The XP-sharing audit then showed that the native alliance experience setting divides XP; the source was changed to award the full amount independently to each hero in range, producing the follow-up build `KLS-D-5b63d38dc0`.
- SHA-256: `612e9a0578749275d70ac3f72406ea32a97758fbbaa30485cc32a479974a4436`.
- This intermediate map was never installed or engine-tested; it is retained in `backups/development-builds/`.

## KLS-D-2780b4380e - 2026-09-28

- Added two installed-data-verified Forsaken Kingdom heroes, Human Ilastar and the Forsaken Paladin, bringing the selector to 17 choices. Their descriptions use the native skill names, their native abilities are extended through the same level-100/rank-10 progression generator, and each receives a new custom signature ability (`AK15`/`AK16`).
- Kept the visible personal gold payout, ordinary gear movement/sale flags, and one-second percentage-based Restoring Spring behavior in the same build.
- Full source regression suite: **66/66 passed**. Package inventory/readback and installed-editor API syntax checks passed. The two recent 15-roster assertions were updated after the 17-entry catalog was added.
- Map SHA-256: `30e1fa1a9c5e6415131f2aea1f200046504e93dbe3dab9de504482eb24641a33`.
- Current-build editor save/reopen, Test Map, Custom Game, live shop/backpack/reward/spring, multiplayer, and endurance checks remain pending. The prior user-reported Test Map pass remains attributed to `KLS-D-fd638ddcf5` only.

## KLS-D-2cd4884e7f - 2026-09-28

- Changed the Forsaken backpack from custom clone `Ibpk` to an in-place edit of installed item `ebua` (`EquipmentBackpackAnya`). This is an evidence-based fix for the reported click-to-open issue; actual interaction remains unverified. Kept `AIni`, `AEqu`, and `ASde`; omitted `ATua`, which installed data identifies as Undead Anya's talent ability.
- Retains personal on-screen gold bounty notifications, droppable and pawnable normal gear (boss relics remain unsellable), and the Restoring Spring's 1% max HP and mana restoration each second. These behaviors are package/source proven but remain pending in-game confirmation.
- The backpack identity regression failed against `Ibpk`, then passed against native `ebua`. Full suite: **65/65 passed**. Package inventory/readback and installed-editor JASS syntax passed.
- Map SHA-256: `fb8a6adede04d1475c5668c44d1b77616fbff19215ec712d7150cdf64502a2cd`.
- Current-build editor/UI/gameplay checks remain pending. Warcraft III PID 46920 still has the earlier installed map open, so this build is in `dist/` and the previous package is archived locally.

## KLS-D-3a0464e019 - 2026-09-28

- Diagnostic `-diag` now reports each active player's runtime race and actual first worker object/unit name, to distinguish the reported Acolyte portrait from an actual Acolyte spawn.
- Installed-data extraction/provenance now includes `UnitBalance.slk`, `UnitUI.slk`, `UnitAbilities.slk`, and `UnitWeapons.slk`. The additional global campaign hero records and worker identities are documented; the hero/building/unit gameplay expansion remains a separate reviewed design proposal.
- Regression suite: **65/65 passed**. Installed-editor JASS syntax and 23-member MPQ package/readback passed.
- Map SHA-256: `c0bb8275469ffb3a2165930fd7ccd62ca6716bc8203a6fc5cc366d5d732365be`.
- Current-build editor/game checks remain pending. Warcraft III PID 46920 still holds the older test map, so this new package remains in `dist/` and the older installed map was preserved.

## KLS-D-b9e9b9dd33 - 2026-09-28

- Baseline for this changelog: development map with the 40-wave co-op runtime, 15-hero selector, expanded battlefield, multi-tier shops, attribute books/recipes, and longer preparation breaks.
- Map SHA-256: `3bbcd7be9bb9d3f2ba02febd026b52c143f5ba28dfc9c52ef4ef1b52e149cc7a`.
- Package/MPQ readback, installed-editor JASS syntax check, and 59 source regressions passed for this build.
- The user's successful Test Map report applies to earlier build `KLS-D-fd638ddcf5`, not this baseline. Editor/gameplay and multiplayer checks for `KLS-D-b9e9b9dd33` were still pending.

## KLS-D-dddc30394a - 2026-09-28

- Enemy kills now show each active defender the exact gold amount added to their own resources. Boss participation gold uses the same visible notification.
- Ordinary equipment is droppable and pawnable, enabling native movement between the Forsaken backpack, normal inventory and equipment UI, and vendor buyback. Boss relics can be moved/equipped but remain unpawnable. These engine interactions still need live confirmation.
- King's Restoring Spring now restores 1% of maximum HP and mana each second within 450 range, capped at each maximum. It emits the restore effect only while the hero is missing HP or mana.
- Focused regression tests failed against the previous source, then passed for the corrected reward display, object flags, and spring cadence. Full suite: **63/63 passed**. Installed-editor API syntax and MPQ package readback passed.
- Map SHA-256: `d646a4a3de78b4e8cbeb1bed6ab5121344565227547dcca7c60c6255ee2d05ab`.
- Installing this build was blocked because Warcraft III PID 46920 held the older `KLS-D-f89f212a3a-Development.w3m` open. The original was preserved and a byte-identical archive copy was verified; the new build remains available in `dist/`.
- Editor save/reopen, Test Map, Custom Game startup, native item transfer/equipment/sale, visible combat rewards, spring behavior, multiplayer and endurance checks remain pending for this build. Keep it labelled development.

