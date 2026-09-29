# Current status — 2026-09-29

## Current package-proven build — KLS-D-8a93630281

- Artifact: `dist/KLS-D-8a93630281-Development.w3m`.
- SHA-256: `bd158009334e911f835d4b9c82d9f0068d89cf0bac9e6c218bd80f9bd97a56ec`.
- Added a validated, checksummed World Editor art-layer bundle at `source/authored-map/editor-layer.zip`, captured from the exact prior package `KLS-D-b0fccf974c` (SHA-256 `5228220725849985bb49d112665a1898a61acdc40b7e431fed2a16ae0dd69110`). It currently preserves the package's existing terrain, pathing, doodads, shadows, minimap markers and preview; it is ready to carry forward future map dressing.
- Added `tools/capture_authored_map.py --map <saved-map.w3m>` and pipeline support to preserve those six layers while continuing to generate all gameplay logic, object data and metadata from source. The capture refuses a different build ID or malformed map dimensions and keeps layer checksums/provenance in the bundle and build manifest.
- Source regression suite: **147/147 passed**. Authored-layer capture, tamper rejection and pipeline archive readback passed; installed-editor JASS syntax and package readback passed.
- `python -B tools/build_map.py --install-test-map` rebuilt this same package and tried installation. Windows returned `WinError 32` while removing the old test map. The installer left `KLS-D-b0fccf974c` intact as the sole map in the test folder and retained a verified archive at `backups/installed-diagnostics/20260929T111716941276Z-KLS-D-8a93630281/` (SHA-256 `5228220725849985bb49d112665a1898a61acdc40b7e431fed2a16ae0dd69110`). No new map was installed. Warcraft III PID 43560 still has the old file locked even though the map is closed; do not force-close it. Retry after the entire game process exits. Current-build editor, Test Map, Custom Game, gameplay, multiplayer and endurance remain pending; the earlier Test Map success remains a pass for `KLS-D-fd638ddcf5`.

## Previous package-proven build — KLS-D-b0fccf974c

## Previous package-proven build — KLS-D-9f529add40

- Artifact: `dist/KLS-D-9f529add40-Development.w3m`.
- SHA-256: `a1aa81f8ea2b3922226ea8dae49aa2d002759b63d1b79c749a10f783aaeb8297`.
- The custom Undead Temple of the Damned (`kR03`) now explicitly sets the installed `BTNTempleOfTheDamned.dds` icon path; parent `utod` and native building stock are preserved. The focused test failed before the change because the generated record omitted `uico`, then passed after the change.
- Focused race/building tests: **12/12 passed**. Full regression suite: **142/142 passed**. Installed-editor JASS syntax and MPQ package/readback passed.
- `py -B tools/build_map.py --install-test-map` built the map and archived the prior package, then failed during installation with `WinError 32`. The old map was restored and remains hash-matched as the only project map in the Warcraft test folder. The archive is under `backups/installed-diagnostics/20260929T062442988973Z-KLS-D-9f529add40/`; the prior dist package is under `backups/development-builds/20260929T062442979354Z-KLS-D-9f529add40/`.
- `World Editor.exe` PID 61288 and `Warcraft III.exe` PID 16152 still launch with the exact old installed map path. Do not force-close either app. The user confirmed a Custom Game start for the previous build, but no visible build ID/result or fresh log entry is available; that attempt does not verify this package.
- Log snapshot `test-results/20260929T064209868239Z-KLS-D-9f529add40` was collected at 06:42:09 UTC. It contains zero diagnostics and no reference to `KLS-D-9f529add40`; its only map launch reference is the old `KLS-D-1739daf903`. `War3Log.txt` was last modified at 07:57 local, before the snapshot, so the collection does not show whether the user's later Custom Game attempt ran or what happened in it.
- Editor round-trip, current-build Test Map/Custom Game, visible icon, gameplay, multiplayer and endurance remain pending. Retry installation when both applications release the old map; keep the build labeled Development.

## Previous package-proven build — KLS-D-1739daf903

- Artifact: `dist/KLS-D-1739daf903-Development.w3m`.
- SHA-256: `807f84919dd59097d31157fd8aabfe8de1c11661b32951a4df028114a06d1940`.
- The log collector now records severity-tagged warnings and explicit spawn/load failures in `collection.json`, with a concise `diagnostic_summary`; `findings.txt` shows each full line and nearest preceding build ID as timing correlation only.
- Full source regression suite: **142/142 passed**. Package readback and installed-editor API syntax checks passed.
- Fresh log snapshot: `test-results/20260929T053054106327Z-KLS-D-1739daf903`; zero references to this build, six old-build map references, and eight spawn/load failures all correlated with older `KLS-D-1a040d638c` lines. These logs do not prove the new build was played.
- Recaptured after opening the current map in Editor: `test-results/20260929T055307058783Z-KLS-D-1739daf903`. It still contains no current-build reference or new gameplay event; the eight spawn/load failures remain tied only by timing to older `KLS-D-1a040d638c` entries, and `War3EditorLog.txt` is empty. No error is attributed to the current build from this snapshot.
- World Editor PID 22184 closed normally. The exact installed `KLS-D-1739daf903` file is now open in World Editor PID 61288 (window title includes its full path). This confirms editor loading only; save/reopen and current-build Test Map remain pending. The map is installed at `Documents/Warcraft III/Maps/TheKingsLastStand/KLS-D-1739daf903-Development.w3m`; its SHA-256 matches the package and it is the only project map in the folder. The replaced map is preserved under `backups/installed-diagnostics/20260929T051420166893Z-KLS-D-660b4bdeea/`.
- The editor-only capture at `20260929T055307058783Z` has no current-build reference or shop/equip event. The eight recorded model-load failures follow older `KLS-D-1a040d638c` map-open entries and are not attributed to this build. The current purchase handler moves a backpack purchase into a free normal slot when possible, then retries native `UnitEquipItem` and logs buyer, location, item and slot context on final refusal; runtime root cause remains undetermined.
- Direct startup attempt: `Warcraft III.exe -launch -loadfile "C:\Users\asphy\Documents\Warcraft III\Maps\TheKingsLastStand\KLS-D-1739daf903-Development.w3m"` ran as PID 16152. The current log snapshot `test-results/20260929T055724787319Z-KLS-D-1739daf903` records that exact command line and has zero warning/error/fatal/failure/spawn-load diagnostics. After 15 seconds the client process was still open, but its log had no `Opening map` entry for this build, so the map/gameplay did not receive a confirmed startup result. Do not mark this as a failed Test Map; the game UI still needs an in-app start and visible build-ID check.
- The earlier Test Map pass remains assigned to `KLS-D-fd638ddcf5`; current-build editor save/reopen, Test Map, Custom Game, gameplay, multiplayer and endurance remain pending.

## Previous package-proven build — KLS-D-660b4bdeea

- Artifact: `dist/KLS-D-660b4bdeea-Development.w3m`.
- Manifest output path: `C:\Users\asphy\Documents\Warcraft3Maps\kings-last-stand\dist\KLS-D-660b4bdeea-Development.w3m`.
- SHA-256: `719de46b17be26b7165d59d3f47e6d13b98117af9b77de1270077e39e78f74eb`.
- Updated the log collector to list observed build IDs separately from the target manifest build, and label the nearest preceding ID on each matching diagnostic as timing correlation only. It explicitly refuses to treat map-open entries as proof of gameplay or causality.
- Full source regression suite: **141/141 passed**. Package archive/readback and installed-API JASS syntax checks passed.
- Fresh capture: `test-results/20260929T051531256402Z-KLS-D-660b4bdeea`. It contains six references to older `KLS-D-1a040d638c`, no references to `KLS-D-660b4bdeea`, and model-creation failures following the older map-open entries. The capture does not establish that the current build was played.
- The first editor/game process query used the wrong process-name filter. Windows Restart Manager identified a remaining `World Editor.exe` process, PID 22184, as the holder of the old map after the user had closed the visible editor window. `python -B tools/build_map.py --install-test-map` failed with `WinError 32` when attempting to remove prior installed `KLS-D-7951d852c3-Development.w3m`. The old map remains in the live test folder; the new artifact was retained at `dist/` and copied to `backups/installed-diagnostics/20260929T051420166893Z-KLS-D-660b4bdeea/`. Do not force-close the editor or delete the locked map; it may contain unsaved work. After the editor is saved and closed normally, retry the supported installer.
- The earlier user-reported Test Map success remains attached to `KLS-D-fd638ddcf5` only. Editor save/reopen, current-build Test Map, Custom Game startup, gameplay, multiplayer and endurance remain pending.

## Current package-proven build — KLS-D-7951d852c3

- Artifact: `dist/KLS-D-7951d852c3-Development.w3m`.
- SHA-256: `42922eb38fd46bd6f6071fef7df08f4329e4abd921d8773bdfc32286f9421b1c`.
- Expanded failed gear purchase/equip diagnostics with buyer type, owner and life state; normal inventory free slots; backpack occupancy; exact gear location; item type/owner; catalog family and equipment slot; and retry attempt. Equip behavior itself remains unverified and unchanged.
- Full source regression suite: **139/139 passed**. Installed-editor API syntax and MPQ archive readback passed.
- Installed at `C:\Users\asphy\Documents\Warcraft III\Maps\TheKingsLastStand\KLS-D-7951d852c3-Development.w3m`; package and installed SHA-256 match, and the folder contains one project map. The previous package and installed map were preserved under `backups/development-builds/20260929T044600046703Z-KLS-D-7951d852c3/` and `backups/installed-diagnostics/20260929T044600056810Z-KLS-D-7951d852c3/`.
- Editor save/reopen, Test Map, Custom Game, gear purchase/transfer/equip/sale, gameplay, multiplayer and endurance remain pending for this build. The earlier Test Map success remains assigned to `KLS-D-fd638ddcf5`.

## Previous package-proven build — KLS-D-b1609a439c

- Artifact: `dist/KLS-D-b1609a439c-Development.w3m`.
- SHA-256: `a3fef077af70c0395591f5862e71f431ac4d394062ad2c526ec82787fabd4221`.
- Moved each plot's eight-tree lumber stand closer: two rows are now 500/700 map units south of the hall on its rear-right side, with the north-side mine route and west-side Altar approach kept open.
- Full source regression suite: **138/138 passed**. Installed-editor API syntax and MPQ archive readback passed.
- Installed at `C:\Users\asphy\Documents\Warcraft III\Maps\TheKingsLastStand\KLS-D-b1609a439c-Development.w3m`; package and installed SHA-256 matched. The package and installed map were preserved when replaced by the current build.
- The earlier Test Map success remains assigned to `KLS-D-fd638ddcf5`; current-build gameplay checks were pending.

## Previous package-proven build — KLS-D-0235a0878b

- Artifact: `dist/KLS-D-0235a0878b-Development.w3m`.
- SHA-256: `70bce2bdbb91cdfbc762a182022a6552cfd96a027ae06579fea610a0709c0608`.
- The development-only `-gear` audit reports six normal inventory slots, occupied backpack positions, and nine equipment slots. It shows item ID/name, registered catalog family/slot, owner marker, and backpack occupancy/capacity.
- Full source regression suite: **137/137 passed**. Installed-editor API syntax and MPQ archive readback passed.
- Installed at `C:\Users\asphy\Documents\Warcraft III\Maps\TheKingsLastStand\KLS-D-0235a0878b-Development.w3m`; package and installed SHA-256 matched and the folder contained one project map. The package and installed map were preserved under `backups/development-builds/20260929T035722408473Z-KLS-D-0235a0878b/` and `backups/installed-diagnostics/20260929T035722417789Z-KLS-D-0235a0878b/`.
- The user confirmed running a test but did not provide its visible build ID or result. Its editor save/reopen, Test Map, Custom Game, gear purchase/transfer/equip/sale, gameplay, multiplayer and endurance remain unverified. The earlier Test Map success remains assigned to `KLS-D-fd638ddcf5`.

## Previous package-proven build — KLS-D-5604bb3f70

- Artifact: `dist/KLS-D-5604bb3f70-Development.w3m`.
- SHA-256: `8e80a85f14a289f61bbf23260423754f1d3fee0441fee0882dfddefa479576bd`.
- Enemy drops now classify every ordinary roster role as Normal or Elite and use a separate Boss profile. Gear chances are 3% / 10% / 50% with increasing rarity weight; independent potion chances are 4% / 8% / 18%. Both items can drop from one death. Active killers own their drops, and the pickup handler binds otherwise unowned catalog gear so equipped stats apply.
- Full source regression suite: **136/136 passed**. Installed-editor API syntax and MPQ archive readback passed; `git diff --check` passed.
- Installed at `C:\Users\asphy\Documents\Warcraft III\Maps\TheKingsLastStand\KLS-D-5604bb3f70-Development.w3m`; package and installed SHA-256 match and the folder contains one project map. The previous package and installed map were preserved under `backups/development-builds/20260929T032904554623Z-KLS-D-5604bb3f70/` and `backups/installed-diagnostics/20260929T032904564518Z-KLS-D-5604bb3f70/`.
- The user reported testing but has not identified the visible build ID or result. Editor save/reopen, Test Map, Custom Game, live drop/pickup, gameplay, multiplayer and endurance remain pending for this build. The earlier Test Map success remains assigned to `KLS-D-fd638ddcf5`.

## Previous package-proven build — KLS-D-f97ab841cb

- Artifact: `dist/KLS-D-f97ab841cb-Development.w3m`.
- SHA-256: `0abf819494aa3829f972e89ddb5b4e8acd60f1432057fb7a77fd56ca196be8b5`.
- `-diag` now counts each logged `ERROR` once in its summary across unit, scenery, item, recipe and retry failures, while retaining the separate recent-error/warning ring.
- Full source regression suite: **134/134 passed**. Installed-editor JASS syntax and MPQ archive readback passed.
- Installed at `C:\Users\asphy\Documents\Warcraft III\Maps\TheKingsLastStand\KLS-D-f97ab841cb-Development.w3m`; package and installed SHA-256 match, and the folder contains one project map. Previous package and installed map were preserved under `backups/development-builds/20260929T025854076991Z-KLS-D-f97ab841cb/` and `backups/installed-diagnostics/20260929T025854085811Z-KLS-D-f97ab841cb/`.
- The user reported completing a test but did not identify the tested build ID or observations. Current-build Editor save/reopen, Test Map, Custom Game, live error-count/`-diag` capture, gameplay, multiplayer and endurance therefore remain pending. The earlier Test Map success remains attributed to `KLS-D-fd638ddcf5`.

## Previous package-proven build — KLS-D-6d3db36ecf

- Artifact: `dist/KLS-D-6d3db36ecf-Development.w3m`.
- SHA-256: `4612c5a61bd95ee06ce46dec9bf67c2f01f413eca5771029c015de41b455a478`.
- Failed recipe output delivery and queued boss/story reward creation or retry failures now include item context, owner and coordinates in `-diag`. Craft failure still restores both components and refunds the fee; personal rewards remain queued for retry.
- Full source regression suite: **133/133 passed**. Installed-editor JASS syntax and MPQ archive readback passed.
- Installed at `C:\Users\asphy\Documents\Warcraft III\Maps\TheKingsLastStand\KLS-D-6d3db36ecf-Development.w3m`; package and installed SHA-256 match, and the folder contains one project map. Previous package and installed map were preserved under `backups/development-builds/20260929T025141544693Z-KLS-D-6d3db36ecf/` and `backups/installed-diagnostics/20260929T025141553541Z-KLS-D-6d3db36ecf/`.
- The user reported completing a test but did not identify the tested build ID or observations. Current-build Editor save/reopen, Test Map, Custom Game, live failure injection/`-diag`, gameplay, multiplayer and endurance therefore remain pending. The earlier Test Map success remains attributed to `KLS-D-fd638ddcf5`.

## Previous package-proven build — KLS-D-ca295479e8

- Artifact: `dist/KLS-D-ca295479e8-Development.w3m`.
- SHA-256: `d18491eab2479068d3a46e3b6065956bc6d858ffeebd3df9e73d9023329d1697`.
- Recipe output delivery rejection now writes an `ERROR` diagnostic with recipe, output item, player, buyer and coordinates before cleanup. Component restoration and the full recipe fee refund remain intact.
- Full source regression suite: **132/132 passed**. Installed-editor JASS syntax and MPQ archive readback passed.
- Installed at `C:\Users\asphy\Documents\Warcraft III\Maps\TheKingsLastStand\KLS-D-ca295479e8-Development.w3m`; package and installed SHA-256 match, and the folder contains one project map. Previous package and installed map were preserved under `backups/development-builds/20260929T023958709775Z-KLS-D-ca295479e8/` and `backups/installed-diagnostics/20260929T023958717683Z-KLS-D-ca295479e8/`.
- The user reported completing a test but did not identify the tested build ID or observations. Current-build Editor save/reopen, Test Map, Custom Game, live recipe-delivery failure injection/`-diag`, gameplay, multiplayer, and endurance therefore remain pending. The earlier Test Map success remains attributed to `KLS-D-fd638ddcf5`.

## Previous package-proven build — KLS-D-69ca4b4a50

- Artifact: `dist/KLS-D-69ca4b4a50-Development.w3m`.
- SHA-256: `e79ff920dba8f96dcab993b3b6f1e8fad487670f7cf86102580e5e8ec7423352`.
- Failed recipe output item creation now logs recipe pattern, expected item/rawcode, owner, and buyer coordinates through `KLS_Log`; component restoration and fee refund remain unchanged. The diagnostic ring surfaces this error after routine logs roll over.
- Full source regression suite: **131/131 passed**. Installed-API JASS syntax and MPQ archive readback passed.
- Installed at `C:\Users\asphy\Documents\Warcraft III\Maps\TheKingsLastStand\KLS-D-69ca4b4a50-Development.w3m`; package and installed SHA-256 match and the folder contains one project map. Previous versions were archived under `backups/development-builds/20260929T022610362928Z-KLS-D-69ca4b4a50/` and `backups/installed-diagnostics/20260929T022610371251Z-KLS-D-69ca4b4a50/`.
- Current-build Editor save/reopen, Test Map, Custom Game, live recipe failure injection/`-diag` capture, gameplay, multiplayer, and endurance remain pending. The earlier user-reported Test Map success remains assigned to `KLS-D-fd638ddcf5`.

## Previous package-proven build — KLS-D-f873a5b24f

- Artifact: `dist/KLS-D-f873a5b24f-Development.w3m`.
- SHA-256: `30fd0594806fd7e2cf9294b6750bb6ecc6e3855d9261852e01ab03fbe51c6d6e`.
- `-diag` stores ERROR/FATAL/WARN messages in a separate 32-entry rolling buffer and displays its latest eight entries alongside the latest 12 regular runtime events. A regression confirms important spawn/setup failures stay visible after routine messages roll over.
- Full source regression suite: **130/130 passed**. Installed-API JASS syntax and MPQ archive readback passed.
- Installed at `C:\Users\asphy\Documents\Warcraft III\Maps\TheKingsLastStand\KLS-D-f873a5b24f-Development.w3m`; package and installed SHA-256 match, and the test folder contains one project map. Previous versions were archived under `backups/development-builds/20260929T020518521798Z-KLS-D-f873a5b24f/` and `backups/installed-diagnostics/20260929T020518530798Z-KLS-D-f873a5b24f/`.
- Captured local engine logs in `test-results/20260929T021428483932Z-KLS-D-f873a5b24f/`. The snapshot's editor/game opening records name only older build `KLS-D-1a040d638c-Development.w3m`; the manifest correctly leaves `played_build_confirmed` false. Model-load warnings in those old-build logs are not evidence about `KLS-D-f873a5b24f`, and in-game `-diag` messages are not persisted to `War3Log.txt`.
- After installation, the user said they had opened the build. The captured editor/game logs do not corroborate the current build ID, so no runtime result can be tied to this artifact yet. The earlier user-reported Test Map success remains assigned to `KLS-D-fd638ddcf5`.
- Exact-build ID/result, Editor save/reopen, current-build Test Map, Custom Game, live inspection of retained spawn warnings, multiplayer, and endurance remain pending. Confirm which build ID appeared and what the user observed; then use `-diag` after any missing spawn to inspect the retained error/warning section.

## Previous package-proven build — KLS-D-87a1bcd5c4

- Artifact: `dist/KLS-D-87a1bcd5c4-Development.w3m`.
- SHA-256: `018fb3e6874134451308b961ea969e7f8a45c42c0e9c7123d1a7526aa404a5c1`.
- Gave each Hall of Banners a distinct installed race building model. The Master Forge now stocks the three general recipes; each constructed race Foundry stocks its owner's racial Legendary pattern. Recipe scrolls return to their selling Foundry or Forge after success/failure; a destroyed seller falls back to the Master Forge. The Foundry's existing company/support bonus remains.
- Full source regression suite: **129/129 passed**. Focused building, equipment, recipe, Crownlands and mine regressions: **50/50 passed**. Installed-API JASS syntax and MPQ archive readback passed.
- Installed at `C:\Users\asphy\Documents\Warcraft III\Maps\TheKingsLastStand\KLS-D-87a1bcd5c4-Development.w3m`; package and installed SHA-256 match. The test folder contains one project map. Previous versions were archived under `backups/development-builds/20260929T012822061855Z-KLS-D-87a1bcd5c4/` and `backups/installed-diagnostics/20260929T012822070939Z-KLS-D-87a1bcd5c4/`.
- After the user closed the prior World Editor session, `War3EditorLog.txt` confirms its last loaded map was the older `KLS-D-1a040d638c-Development.w3m` and records shutdown at 2026-09-29 00:18. The current `87a1bcd5c4` package and installed map still match byte-for-byte; the editor log has no subsequent open of this current build, so any screenshot from that closed session cannot verify its starting mines or other fixes.
- Exact-build Editor save/reopen, Test Map, Custom Game, Hall appearance, Foundry shop/crafting, gameplay, multiplayer, and endurance remain pending. The earlier user-reported Test Map success remains assigned to `KLS-D-fd638ddcf5`.

## Previous package-proven build — KLS-D-2aa1705c84

- Artifact: dist/KLS-D-2aa1705c84-Development.w3m.
- SHA-256: edd432c6f16f5c628f63c6956b842b97ab2e66faff9e531395e8b4012f84b5b0.
- Fixed native tier-two town-hall prerequisites to point at the selected race's custom Altar, Barracks and upgrade structure: Human Castle (hcas), Orc Stronghold (ostr), Night Elf Tree of Ages (etoa), and Undead Halls of the Dead (unp1).
- Added a regression that failed against all four upgrade targets before the fix and passed afterward. Full source suite: 125/125 passed. Package archive readback and installed-editor API syntax checks passed.
- Installed on 2026-09-29 at C:\Users\asphy\Documents\Warcraft III\Maps\TheKingsLastStand\KLS-D-2aa1705c84-Development.w3m; installed SHA-256 matches the package manifest, and the folder contains one project map. The replaced build was archived under backups/installed-diagnostics/20260928T233302983717Z-KLS-D-2aa1705c84/.
- Captured local engine logs under test-results/20260928T233351692935Z-KLS-D-2aa1705c84/. They show the older KLS-D-1a040d638c map opening and several model-creation warnings; the manifest marks played_build_confirmed false. Those warnings are not evidence about this build. In-game -diag text is not persisted in War3Log.txt.
- Current-build editor save/reopen, Test Map, Custom Game, faction town-hall upgrade behavior, general gameplay, multiplayer and endurance remain pending. The earlier user-reported Test Map success remains assigned to KLS-D-fd638ddcf5.

## Previous package-proven build — KLS-D-fdee19fa63

- Artifact: `dist/KLS-D-fdee19fa63-Development.w3m`.
- SHA-256: `6e591f5af710a3c6654d65743c957bf3308902c291907f6fec6090361367fa14`.
- `-diag` now reports the calling player's selected units with object name, unit name, numeric type ID, owner and position, up to 12 units. This distinguishes a wrong worker spawn from a different selected unit behind the Peon/Acolyte portrait report.
- Full source suite: **124/124 passed**. Package archive readback and installed-editor API syntax checks passed.
- Installed on 2026-09-29 at `Documents/Warcraft III/Maps/TheKingsLastStand/KLS-D-fdee19fa63-Development.w3m`; installed SHA-256 matches the manifest and the test folder contains one project map. The prior installed map remains preserved in the verified local archive.
- Current-build editor save/reopen, Test Map, Custom Game, gameplay, multiplayer and endurance checks remain pending in Warcraft. The earlier user-reported Test Map success remains assigned to `KLS-D-fd638ddcf5`.

## Previous package-proven build — KLS-D-4a67348b4e

- Artifact: `dist/KLS-D-4a67348b4e-Development.w3m`.
- SHA-256: `a013631ed88293b9d4c2610015152135eb3a7a9456e5b119cc2b8c211560aff4`.
- The optional King's Restoring Spring visual now uses the shared checked spawn wrapper with `restoring spring visual` context. Spawn failure is logged and counted by diagnostics without stopping the match or disabling coordinate-based regeneration.
- Full source suite: **123/123 passed**. Package archive readback and installed-editor API syntax checks passed.
- Installed on 2026-09-29 at `Documents/Warcraft III/Maps/TheKingsLastStand/KLS-D-4a67348b4e-Development.w3m`; installed SHA-256 matches the manifest and the test folder contains one project map. The prior installed map remains preserved in the verified local archive.
- Current-build editor save/reopen, Test Map, Custom Game, gameplay, multiplayer, and endurance checks remain pending in Warcraft. The earlier user-reported Test Map success remains assigned to `KLS-D-fd638ddcf5`.

## Previous package-proven build — KLS-D-81285a4cc0

- Artifact: `dist/KLS-D-81285a4cc0-Development.w3m`.
- SHA-256: `21540054f1250628fa1095ad42ee68bb986982a2f421c89b421574de827398cc`.
- Adds mine-specific startup diagnostics: `-diag` reports each active player's expected and actual starting mine type, mine owner, remaining gold, and coordinates. A missing mine is reported explicitly; required racial mine spawn failures include the `starting racial gold mine` context.
- Retains tree-free Keeper/Faelor signatures, pre-owned Undead Haunted and Night Elf Entangled starting mines with 1,000,000 gold, and the higher equipment price curve (300/1,000/3,000/8,000/20,000; hand weapons cost 1.5× base; racial recipes cost 9,000; tomes cost 1,000/3,000/8,000).
- Full source suite: **122/122 passed**. Package archive readback and installed-editor API syntax checks passed.
- Installed on 2026-09-29 at `Documents/Warcraft III/Maps/TheKingsLastStand/KLS-D-81285a4cc0-Development.w3m`; installed SHA-256 matches the manifest and the test folder contains one project map. The prior installed map remains preserved in the verified local archive.
- Current-build editor save/reopen, Test Map, Custom Game, starter mine ownership/mining, shops and prices, multiplayer, and endurance checks remain pending in Warcraft. The earlier user-reported Test Map success remains assigned to `KLS-D-fd638ddcf5`.

## Previous package-proven build — KLS-D-dd3a53babf

- Artifact: `dist/KLS-D-dd3a53babf-Development.w3m`.
- SHA-256: `f2d804924a18aaab17ff00ed8d61b321a7fda54278a08e77559c3fcf6ab666cf`.
- Keeper of the Grove and Faelor Briarward no longer receive the unusable tree-targeted native `AEfn` button when spell ranks are applied. Keeper's Grove Awakening and Faelor's Briarward Stand signatures summon Treants at an open target point without nearby tree destructables. `AEfn` is removed again after each hero-rank update.
- Undead and Night Elf starting heroes receive owned Haunted or Entangled Gold Mines at their base with 1,000,000 gold; the Undead handler also accepts the native `hauntgoldmine` order.
- Equipment rarity prices: 300/1,000/3,000/8,000/20,000; hand weapons cost 1.5× base, original recipe fees 5,000/7,000/12,000, racial recipes 9,000, and tomes 1,000/3,000/8,000. Consumable prices and item stats are unchanged.
- Full source suite: **120/120 passed**. Package archive readback and installed-editor API syntax checks passed.
- Installed on 2026-09-29 at `Documents/Warcraft III/Maps/TheKingsLastStand/KLS-D-dd3a53babf-Development.w3m`; the installed SHA-256 matches the manifest and the test folder contains one project map. The locked prior map was retained in the verified local installed-map archive.
- Current-build editor save/reopen, Test Map, Custom Game, Keeper/Faelor signature casting on clear ground, starter mine ownership/mining, shops and prices, multiplayer, and endurance checks remain pending. The earlier user-reported Test Map success remains assigned to `KLS-D-fd638ddcf5`.

## Previous package-proven build — KLS-D-2f2397cf14

- Artifact: `dist/KLS-D-2f2397cf14-Development.w3m`.
- SHA-256: `e63d8c15d90458056887f056ac66d1194aa30326e20ec94847f5ac91e2d7310f`.
- Added `source/rewards.j` as the shared delivery path for chapter-boss and Crownlands story items. The path checks null item creation before use, queues failed item codes for the correct owner and retries every five seconds while the match clock runs. A created item goes into the owner's hero inventory when possible; otherwise it remains visible, owner-bound and retrievable at that player's base.
- Removed direct `CreateItem` and unchecked `UnitAddItem` handling from both boss and story reward code. Reward gold, contributor eligibility, boss death counting and story stage progression are unchanged.
- Full source suite: **112/112 passed**. Package member readback and installed-editor JASS compilation passed. Regression tests cover routing, null-handle checks, queue retry bookkeeping and full-inventory fallback.
- Installation was attempted but did not proceed because Warcraft III still holds `KLS-D-1a040d638c-Development.w3m` open. The installer preserved its original and reused the matching archive under `backups/installed-diagnostics/20260928T192844325669Z-KLS-D-8669a44192/`; both have SHA-256 `eaee0e501b3e7ced381bda7c93c530d79499faad94f2bb80304a9aeb1340e362`. Current build remains only in `dist/`; no extra map was left in the test folder.
- Current-build editor save/reopen, Test Map, Custom Game, live reward ownership/pickup, gameplay, multiplayer and endurance remain pending. The earlier user-reported Test Map success remains a pass for `KLS-D-fd638ddcf5`.

## Previous package-proven build — KLS-D-0227009b20

- Current task: harden map installation and backup behavior while preserving the current Crownlands gameplay package.
- Build: **KLS-D-0227009b20**.
- Artifact: `dist/KLS-D-0227009b20-Development.w3m`.
- SHA-256: `23a7887af12f726ddffe37ab4b9e817c021ba46a2842ced4ce80a53297f43a6c`.
- Package member readback and installed-editor API syntax passed. Full source regression suite: **108/108 passed** (`python -B -m unittest discover -s tests -v`); installer-focused checks: **6/6 passed**.
- Gameplay content carries forward from `KLS-D-8669a44192`; the build ID changes because installer source is included in the build fingerprint.
- Implemented: the original 40 rows are unchanged; waves 41-50 add Naga, Blood Elf, Fel Orc, Burning Legion, and Scourge forces, with all five represented at Wave 49. The bounded ten-row cycle repeats while live-wave scaling continues. Campaign leaders rotate as bosses every ten waves; bosses from Wave 50 grant each active player a personal Legendary catalog item. Existing tracked enemy accounting, bounties, XP, summons, and relic rewards for waves 10-40 remain covered by regressions. Wave 40 continues, King Aldric's death ends the run, and the HUD shows the highest wave.
- Crossover units resolve against installed Definitive Edition tables and retain their native campaign models, animations, movement, and armor. The deterministic ordered roster catalog is `docs/WAVE-ROSTER-CATALOG.md`.
- The installer now creates and verifies a backup before removing old maps, reuses exact archived copies on retry, and restores prior files when a later install step fails. The actual retry stopped cleanly because the running Warcraft III process locks `KLS-D-1a040d638c-Development.w3m`; its untouched original and one retained archive copy have matching SHA-256 `eaee0e501b3e7ced381bda7c93c530d79499faad94f2bb80304a9aeb1340e362`. The new package is not installed. Exit Warcraft III completely and rerun `python -B tools/build_map.py --install-test-map`.
- Status: **development build**. Current-build editor save/reopen, Test Map, Custom Game, native plus-button behavior, mine orders, Temple UI, wave 40-50 and later-boss visuals/gameplay, multiplayer and endurance remain pending. The earlier user-reported Test Map success remains a pass for **KLS-D-fd638ddcf5**.

## 2026-09-28: endless campaign crossover and Crownlands runtime — KLS-D-8669a44192

### Changes and evidence

- Replaced the global per-level attribute Dialog with standard hero `+` skill choices for +3 Strength, +3 Agility, or +3 Intelligence. Every fifth level still awards the separate Vanguard/Skirmisher/Sage talent.
- Set map default race preference to Random and changed the confirmed hero's owner's race preference before spawning the matching race base.
- Corrected Undead Temple of the Damned rawcode `kR03` to inherit from `utod`; retained native Temple training/research fields so it uses the Temple's art and icon. Updated race-specific Altar, arcane/support, tower and company-building descriptions.
- Added Undead Acolyte conversion of a neutral gold mine into an owner-controlled Haunted Gold Mine, preserving remaining gold. Extended Night Elf Tree of Life `Aent` range to 1,450.
- Carried forward the user-requested first 40 waves and added ten bounded repeating post-40 campaign rosters, live-wave scaling, recurring installed-campaign bosses, and personal Legendary drops from Wave 50 onward. Wave 49 converges all five forces; Wave 40 continues; only King Aldric's death ends the run. The same package also contains the primary-stat plus skills and race-specific mine/building fixes listed above.
- Full regressions: **105/105 passed**. Supported package readback and installed-editor API syntax checks passed.
- Artifact SHA-256: `b7d0b41039d0cd4d655daf97d40a0329d443f987c62e9a927c87a8fc7bb995a0`.
- Installation is blocked only by the World Editor handle on the older map. The archive copy is verified; the original remains untouched. The exact current build is still available in `dist/`.

### Next human checks

- Exit Warcraft III completely, run the supported install command, open the newly installed build and check the startup ID. Verify the primary-stat plus buttons are visible and one selection increases only the matching attribute without a per-level dialog; also verify the separate fifth-level choice. Then play through waves 40-50 and one later boss to inspect the crossover campaign models/armor, warnings, summons, pathing and per-player reward.
- In mixed-race play, confirm `utod` Temple icon and queues, Undead Acolyte mine haunting/resource harvest, and Night Elf Entangle access. Continue to the broader gameplay, multiplayer and endurance checks. Do not mark earlier successful Test Map evidence as failed; it stays with `KLS-D-fd638ddcf5`.

## Previous build record — KLS-D-b5ae4ab2fe

- Its 79/79 automated suite, package readback and installed-editor API checks passed. Its SHA-256 was `05a072b826318b5d40d9cacda0f9e3755c845093f618f7bfb227da3fd7ec5da7`. It has been archived and superseded by the current expansion build above.

## 2026-09-28: fix contradictory recipe completion/refund — KLS-D-a2dae2be8c

- The craft output delivery branch already refunded the fee and reported failure when `UnitAddItem` failed. A second unconditional refund immediately after the branch caused the contradictory screenshot message after successful crafting and could charge/refund incorrectly on failed delivery. Removed that unconditional call while retaining the failure-branch refund.
- Added a regression asserting that success emits no refund, failed delivery refunds once, and there is no statement after the delivery conditional before its enclosing branch closes.
- Focused recipe/progression tests: **14/14 passed**. Full suite: **77/77 passed**. Package readback and installed API JASS syntax passed.
- SHA-256: `e86d0c0e1696897d8727d243bf6bc92bd6f5ce8ca6b6b39a8d24ae38668dbd9d`; installed map matches at the dedicated Custom Game path above.
- Exact next check: use this build to complete a single recipe and confirm one completion notification with no failure/refund notification. Broader current-build gameplay and multiplayer gates remain pending.

## 2026-09-28: correct extended hero-aura rank data — KLS-D-1398318c4a

- The installed Forsaken campaign ability data declares Sacred Aura as three ranks, with resistance values 0.15, 0.25, and 0.35. Its row also contains an unrelated fourth-rank value of `5`; setting the ability's max ranks to ten exposed that as 500% magic resistance.
- The Forsaken Paladin alias `AHpa` uses internal code `AHas`. The old generator filtered allowed metadata by alias only, so it did not emit Sacred Aura's resistance fields for `AHpa`; that variant also fell through to bad source data.
- Rank generation now uses both the alias and internal code for metadata filtering and limits native rank reads to the ability's declared number of levels. Later ranks continue from the last valid installed values. Regression coverage checks Ilastar's `AHas`, the Forsaken Paladin's `AHpa`, and Devotion Aura continuation.
- Focused progression tests and the full suite passed (**76/76**). Package inventory/readback and JASS syntax against the installed editor API passed.
- Package SHA-256: `b7fe3601272d32c7d95e23fb7b50470ee6e39ca40bc914d0e9c2c14fa6016af2`.
- The current build is not installed yet because the prior test map is held open/locked. The install attempt preserved a verified archive copy of the prior map but left its original in the test folder. Close the process holding that map and rerun the supported install command. Then check Sacred Aura rank 4 and later in the exact build. Do not treat the prior build's successful Test Map as evidence for this build.

## Previous installed build

- Build: **KLS-D-5b63d38dc0**.
- Artifact: `dist/KLS-D-5b63d38dc0-Development.w3m`.
- SHA-256: `560b662379fb23969ad2528f53d2623667125760e89d050e6a2dd6c5e8781bc8`.
- Installed test map: `C:\Users\asphy\Documents\Warcraft III\Maps\TheKingsLastStand\KLS-D-5b63d38dc0-Development.w3m` (hash matches the package).
- Manifest: `dist/build-manifest.json`.
- Package archive readback and JASS syntax against installed API: passed. Full source regression suite: **75/75 passed**.
- Status: **development build**. Current-build editor, Custom Game, gameplay, multiplayer, and endurance checks are pending.

## User-reported engine result

- World Editor Test Map succeeded on the earlier installed development build **KLS-D-fd638ddcf5**. This remains a pass for that build and is not listed as a failure.
- Save/reopen, current-build Test Map, current-build Custom Game, live systems, multiplayer and endurance checks remain pending for their respective builds.

## 2026-09-28: personal bounties, full-range XP, quiet spring, and Oathbound Companies — KLS-D-5b63d38dc0

### Current task and last proven build

- Current task: implement the approved RPG recovery plan and the user's latest reward, regeneration, gear-flow, building expansion, and wave-break feedback.
- Current development build: **KLS-D-5b63d38dc0**.
- Workspace artifact: `dist/KLS-D-5b63d38dc0-Development.w3m`.
- SHA-256: `560b662379fb23969ad2528f53d2623667125760e89d050e6a2dd6c5e8781bc8`.
- Installed version: `C:\Users\asphy\Documents\Warcraft III\Maps\TheKingsLastStand\KLS-D-5b63d38dc0-Development.w3m`; the installed copy matches this SHA-256.

### Changes and evidence

- Player-owned kills now pay the full role bounty only to that player's resources. King Aldric kills pay 25% of the bounty to each active defender. Visible recipient-only gold text remains on both routes.
- Warcraft's native experience-sharing behavior divides XP across heroes, so the map disables native XP awards and the runtime grants a full per-kill XP amount to each active hero inside 1,200 world units. Hero race and life state do not filter recipients. XP values use the normal unit-level progression and hero-kill table. Dead-hero XP, actual range behavior, and high-level progression still need engine proof.
- King Aldric's acquisition range is set to 900 so the stationary king can attempt to make the kills that use his quarter-bounty route.
- Restoring Spring heals 1% max health and mana every second with no Holy Bolt effect, floating text, or timed message.
- Normal between-wave preparation is 50 seconds; before boss waves it remains 180 seconds. Initial preparation remains 45 seconds.
- Bought equipment transfers toward an available normal-inventory slot after shop purchase. Vendor resale reads the pawn event's manipulated item instead of the unrelated sold-item event payload. Equipment/backpack/sale behavior remains engine-pending.
- Added Hall of Banners, Royal Foundry, Siege Yard, and 34 hero-linked company/support unit records. Company purchase, ownership, effects, and UI are still engine-pending.
- Focused reward/XP/timing tests passed. The first full-suite run reported only that this newly generated build ID had no changelog section yet; after documenting the ID, the full suite passed **75/75**.
- `python -B tools/build_map.py` passed MPQ readback and installed-editor API syntax checks. `python -B tools/build_map.py --install-test-map` archived older project test maps and installed the new version. The installed SHA-256 matches the package.
- The user-reported World Editor Test Map success remains credited only to **KLS-D-fd638ddcf5**. The current build has not been launched or tested in the editor yet.

### Exact next action and remaining checks

- Next human check: start the installed `KLS-D-5b63d38dc0-Development.w3m` through Warcraft III → Single Player → Custom Game, confirm its visible ID and that hero selection opens without a premature victory. Use this exact build in all subsequent checks.
- After startup proof, check killer-only gold feedback, XP to every nearby hero, King Aldric's quarter bounty, gear transfer/equip/resale, the silent one-second spring tick, and 50/180-second break timers.
- The 2/3/4-player, 40-wave, boss, building/company, current editor save/reopen, and endurance acceptance checks remain pending.

## 2026-09-28: campaign heroes and reward/inventory corrections — KLS-D-2780b4380e (historical)

### Current task and last package-proven build

- Current task: keep implementing the full approved defense RPG plan, record every packaged build, and address the latest combat-feedback and Forsaken inventory test reports.
- Current development build: **KLS-D-2780b4380e**.
- Workspace artifact: `dist/KLS-D-2780b4380e-Development.w3m`.
- SHA-256: `30e1fa1a9c5e6415131f2aea1f200046504e93dbe3dab9de504482eb24641a33`.
- Package changelog: `CHANGELOG.md`; manifest: `dist/build-manifest.json`.

### Changes and evidence

- Expanded the 15-hero selector to 17 with Human Ilastar (`Hjsm`) and the Forsaken Paladin (`Npal`). Their four skill IDs and display names were checked against the installed Definitive Edition tables. The same rank generator extends their native skills to ten ranks through hero level 100, and the selector provides the custom `AK15`/`AK16` signatures.
- Kept the 17 previews inside the existing selection camera bounds with a six-column grid. The user's actual selector readability test remains pending.
- Focused and full regression suite passed: **66/66**. This includes per-player kill/boss gold notifications, ordinary gear backpack/normal-inventory movement and pawnability, unsellable boss relics, and 1% HP/mana restoration each second.
- Package inventory/readback and JASS syntax against the installed editor API passed. The generated map is `dist/KLS-D-2780b4380e-Development.w3m`; previous build artifacts are archived outside `dist/`.
- The earlier user-reported World Editor Test Map success remains a pass for **KLS-D-fd638ddcf5** only. It has not been carried forward as evidence for this build.
- The current build was installed at `Documents/Warcraft III/Maps/TheKingsLastStand/KLS-D-2780b4380e-Development.w3m`; the installer archived the former test copy. Warcraft III PID 61400 is open, but the new map has not been launched. All engine, equipment, multiplayer, and endurance checks remain pending.
- Computer-use initialization failed twice with `failed to write kernel assets: The system cannot find the path specified`, including after resetting the UI session. No clicks or keyboard input were sent.

### Exact next action

- Exact next check: launch `KLS-D-2780b4380e` via Custom Game, choose a hero, use `-wave 1` if necessary, and confirm one enemy kill displays `+N gold` while resources increase. Then report the build ID and a screenshot. After startup/reward feedback is confirmed, ask for the backpack transfer/sell and spring tick checks.

## 2026-09-28: restore native backpack identity — KLS-D-2cd4884e7f (historical)

### Current task and last package-proven build

- Current task: resolve the Forsaken Field Pack click-to-open report, while keeping the user's gold feedback, transferable/resellable ordinary gear, and one-second spring healing in the same current package.
- Current development build: **KLS-D-2cd4884e7f**.
- Workspace artifact: `dist/KLS-D-2cd4884e7f-Development.w3m`.
- SHA-256: `fb8a6adede04d1475c5668c44d1b77616fbff19215ec712d7150cdf64502a2cd`.
- Changelog: `CHANGELOG.md`; package manifest: `dist/build-manifest.json`.

### Changes and evidence

- Installed `ItemData.slk` identifies native backpack `ebua` as `EquipmentBackpackAnya`, with `AIni,AEqu,ATua,ASde`; installed `AbilityData.slk` identifies `ATua` as Undead Anya's talent tree. The custom clone `Ibpk` was replaced with an in-place edit of native `ebua`, retaining `AIni,AEqu,ASde` and usability while omitting the unrelated talent ability. This is the best-supported explanation/fix for the click report, but the interaction remains unverified in the game.
- Hero initialization grants `ebua`; backpack activation diagnostics now match `ebua`. Source regression failed before the rawcode change and passed afterward.
- Current source still shows each active defender the gold amount actually credited on enemy/boss kills. Ordinary equipment flags permit movement and vendor resale; boss relics remain unsellable. The restoring spring uses a 1-second timer and restores 1% maximum HP and mana per tick. These require in-game confirmation.
- Full regression suite: **65/65 passed**. Package member inventory/readback and installed-editor JASS syntax passed for the build. `dist/` contains one current map; the previous development package is archived locally.
- The prior user-reported World Editor Test Map success remains a pass for `KLS-D-fd638ddcf5`. It is not treated as a failure or a current-build pass.
- Warcraft III PID 46920 still has an older project map open; `KLS-D-2cd4884e7f` was not installed or run.

### Exact next action and remaining checks

- After the user closes Warcraft III, run `python -B tools/build_map.py --install-test-map`. Open that exact build through the established editor/Test Map and Custom Game workflows.
- First live item check: click the native backpack; confirm its UI appears. Then buy Common Boots, transfer between backpack and normal inventory, equip, and sell them. In the same run, verify the visible kill-gold message and watch HP/mana restore at the spring for several consecutive one-second ticks.
- Remain a development build until current-build gameplay, editor round-trip, multiplayer and endurance gates pass.

## Changes since the previous build

- Each roster enemy has an explicit generated base bounty. Normal enemy gold equals the role's base value plus current wave number; bosses pay `100 + 5 × wave`. The existing equal team split and slot-order remainder remain in place. Boss summons use their own unit bounty.
- 59/59 focused regression tests passed, including roster coverage, role ordering, boss/reinforcement rewards and existing shared payout rules.
- One current map is kept in `dist/`; prior local map packages are archived under `backups/development-builds/`, and Git history preserves tracked versions.
- **Ruling:** keep 90-second ordinary breaks and 180-second pre-boss breaks. Revise only after a recorded pacing playtest.

## Test-folder and Editor state

- The live test folder currently contains the older `DIAGNOSTIC-KLS-D-fd638ddcf5.w3m` and the partially installed `KLS-D-f89f212a3a-Development.w3m`. The running Warcraft III process (PID 46920) holds the older map, so the new installer correctly refuses to move forward until that lock is released. It will archive old project copies and install only the current map after Warcraft III closes.
- The user's open World Editor document at `build/DIAGNOSTIC-TheKingsLastStand.w3m` was left untouched. UI automation could not attach in this session, so no live editor edits were sent and no round-trip copy was created.

## Next exact action and remaining checks

1. After Warcraft III is closed, run `python -B tools/build_map.py --install-test-map`. Confirm only `KLS-D-b9e9b9dd33-Development.w3m` remains in the dedicated test folder and its SHA-256 matches the manifest.
2. Test this ID in World Editor and through Custom Game. Record the user-reported earlier Test Map pass separately; do not treat the current exact-build check as failed or as passed until tried.
3. Continue the acceptance gates in ROADMAP-AND-ACCEPTANCE.md for inventory/shop use, construction/economy, all 40 waves, boss mechanics, actual 2/3/4-player sessions and two-/four-player endurance.

## Historic recovery notes

The following is the original detailed implementation ledger. Its build identifiers and test counts are historical; use the heading and status in each entry to place evidence in sequence.

---

# Recovery progress

Current feature plan: docs/superpowers/plans/2026-09-28-hero-items-progression-and-pool.md. The full recovery scope remains approved in the conversation and is tracked through this ledger.

## Current stage

Package and installed-API syntax checks pass; in-game verification remains pending.

Latest diagnostic: **KLS-D-64d7e969ab**.
Manifest: `build/diagnostic-manifest.json`.
Project map: `build/DIAGNOSTIC-TheKingsLastStand.w3m`.
Installed versioned copy: `C:\Users\asphy\Documents\Warcraft III\Maps\TheKingsLastStand\DIAGNOSTIC-KLS-D-64d7e969ab.w3m`. Its SHA-256 matches the build manifest.

Latest SHA-256: `cf77930ef80a5107c5ab7a3234dffa9eb30750d00b2cabf53ae1880acdd95369`.

## Evidence

- Added-file-list regression first failed because custom unit/item members were missing from the listfile; now passes.
- Packer updates listfile, hash/block tables, and per-block CRC attributes. Uses engine-style probing and exact payload read-back before writing output.
- Unmodified named editor members are preserved byte-for-byte.
- Installed common.j and blizzard.j extracted directly from Warcraft III CASC storage with locally compiled upstream CascLib. Provenance records build-info and API hashes; stale references are rejected.
- Current diagnostic compiles using installed API declarations and the installed pjass.
- Editable WTG/WCT data is independently parsed, reconstructed into a JASS script and compiled. This is a static check, not an actual editor round-trip.
- At the original startup stage, four focused package/editor-source regressions passed; the expanded battlefield stage now has eight tests passing. The current 128-cell terrain still requires an in-game visual/pathing check.
- Runtime receives explicit initial values and an initialization guard from the single assembly path. Build ID appears in metadata/config and the startup message.
- Old prototype and one-off scripts are preserved under backups. The original root blank map is still locked by World Editor; an identical backup exists at backups/Original-Blank-TheKingsLastStand.w3m. Do not terminate the editor or discard unsaved user work to remove it.

## Historical implementation — expanded battlefield and startup-gated systems (KLS-D-51f7f1f807)

- Terrain and pathing are now 128 × 128 cells (playable W3I bounds 116 × 116), with updated camera bounds and four east-to-west player starts at x = -6000, -3300, 3300 and 6000 on y = -500.
- The generated map paints a grassland, a stone north-to-south lane, four bordered build plots, a rocky northern approach, the king’s paved courtyard, and a southern market square.
- Runtime creates the open northern gate line, harvestable tree belts, four visible town halls and gold mines (neutral markers for vacant slots), King Aldric’s castle and the king in front, and the shared market south of the castle.
- Updated build ID **KLS-D-51f7f1f807** includes the corrected shop patron abilities, packages successfully, compiles against the installed API and is installed in the Custom Game map folder. Build SHA-256 matches the installed copy.
- Current focused regression suite passes: 29/29. The new shop-ability regression failed first for both market and castle (`Aneu` absent), then passed after restoring the ability.
- Warcraft launched the previous editor Test Map and its archived runtime script contains `KLS-D-f8fbeccb9f`. The separate current build `KLS-D-51f7f1f807` has not yet been opened in the engine.

**Historical next action:** the KLS-D-51f7f1f807 stock-panel check is superseded. Use the current build and exact next human check recorded in the latest dated section below.

## Prior build round-trip inspection — KLS-D-d4b1172aba (2026-09-26)

- Inspected `Editor-Roundtrip.w3m` saved at 18:05. It retains build identifier `KLS-D-d4b1172aba` in map metadata and runtime script.
- Its runtime JASS compiles successfully with the installed Warcraft III 3.0.0.24268 `common.j` and `blizzard.j` declarations (981 map-script lines; no compiler stderr).
- Runtime has one `KLS_Init` definition and one startup call, retains the initialization guard, and contains no melee initialization or melee victory/defeat trigger.
- World Editor serialized object data as format version 3, placing custom names/tooltips in `war3mapSkin.w3u` / `war3mapSkin.w3t` and `war3map.wts`. Custom hero/building IDs `H000`, `H001`, `h000`–`h003` and item IDs `I000`–`I003`, `I010`–`I013` remain present. Terrain (`war3map.w3e`) and pathing (`war3map.wpm`) match the diagnostic package byte-for-byte. Object data is present; the current legacy object verifier understands only version 2 and needs a version-3-aware semantic check before future round-trips can be automatically certified.
- The user's in-game screenshot shows a running match with a completed Barracks and a cleared wave. This is human evidence of single-player progression, but it does not identify whether the screenshot came from Test Map or Custom Game.

**Historical status:** the previous build compiled and retained its editor data; its direct Custom Game route was not proven. This record is superseded by the expanded battlefield build **KLS-D-104afc2935** above.

## Battlefield layout update — 2026-09-26

User's annotated layout supersedes the earlier generic plot arrangement:

- North is the top of the map. Undead approach down one central north-to-south lane (black mark).
- Place the northern gate line across the approach (green mark), leaving a broad permanent central passage for the lane; gate structures and hills funnel enemies without sealing the route.
- Align all four player plots east-to-west along the red line. Keep a clear central crossing/approach at the King’s Castle, centered on the yellow mark.
- Place the King’s Castle at the center of the defender row. Put the shared markets farther south, behind the castle.
- The 128-cell diagnostic implements this layout with separate plots, a clear central road, an open gate, courtyard and southern market; in-game pathing and visual checks remain pending.


## Battlefield verification request — 2026-09-26

The current artifact differs from the user's screenshot and needs an in-engine look. Please launch `DIAGNOSTIC-TheKingsLastStand.w3m` from the Warcraft III Custom Games menu, use the minimap to pan to the center if needed, and send one screenshot showing the northern gate, four aligned plot markers, King Aldric's castle and the southern market. Confirm enemies can pass through the central gate opening. No claim of in-game terrain/pathing success is made yet.

## Chapel correction — KLS-D-13c2f140bc

- Installed HumanUnitFunc.txt confirms Arcane Sanctum `hars`, Priest `hmpr`, Sorceress `hsor`; previous Chapel cloned `halt` and referenced invalid Priest ID `hpri`.
- Chapel now derives its model/icon and caster-building behavior from `hars`, trains `hmpr,hsor`, and offers only Priest/Sorceress research. Keeps 160 gold / 70 lumber, 30-second construction and 900 HP. Added role tooltip.
- Worker menu replaces redundant standard Arcane Sanctum with the intended Workshop (`harm`); Chapel remains the caster building.
- Sole build entry point rebuilt and installed diagnostic KLS-D-13c2f140bc. Package readback and installed-API syntax checks passed.
- Pending engine check: in this build, construct Chapel and confirm Arcane Sanctum appearance and both Priest/Sorceress recruitment buttons; recruit one of each.
- Broader terrain, native equipment, hero selection and multiplayer acceptance remain unfinished; this correction is not completion of the approved full plan.

## Altar / Sanctum separation — KLS-D-73c34cd3eb
- Supersedes Chapel correction: h000 now derives from native Altar of Kings halt, with correct name/icon/model and no caster recruitment. h004 is a separate Arcane Sanctum training hmpr/hsor and their upgrades. Workers build both.
- Each active defender starts with an altar. Selecting an owned altar reopens the initial class dialog until a choice is made; choice guard prevents repeated replacement. After selection it reports hero/revival status.
- Existing 20-second automatic revival returns heroes beside their altar. Completed replacement altars update the destination; destroyed altar falls back to the base. Native paid revival and extra hero recruitment are disabled to avoid duplicate revival/extra heroes.
- Built and installed via build_map.py --install-diagnostic. Package readback, installed-API syntax and all 8 existing regression tests passed. These do not prove engine behavior.
- Next human check: start KLS-D-73c34cd3eb, confirm the starting Altar of Kings and build an Arcane Sanctum with separate Priest/Sorceress buttons. Hero revival at the altar remains an additional pending engine check.
- Broader approved feature plan remains incomplete and development-labelled.

## Battlefield camera, approach and HUD — KLS-D-c72d6785ce
- Found old starter SetCameraBounds in compiled main despite enlarged W3E/W3I. Runtime camera now spans +/-7424; checks cover all four plots, market and staging area. Editable source retains matching generated runtime.
- Moved regular spawn rows to y6200 + floor(n/5)*40 and boss to y6800, inside playable bounds.
- WPM now blocks ground movement on northern gate flanks (|x|>=1100, y4800..5600), leaving central passage open; corresponding rocky surface extends across flanks. Pathing route checks pass but destructible collision still needs engine proof.
- Replaced old 64-cell shadow member with blank 512x512 shadow data matching enlarged pathing; editor may bake shadows on save. Minimap imagery still needs regeneration; not claimed complete.
- Replaced leaderboard title with top-right six-row multiboard: wave, chapter, prep clock/enemy count, king HP/tier, local hero revival time and terminal result. Local player affects text only.
- Idle enemy redirection no longer blanket-interrupts units with active orders. Stuck-path detection remains pending.
- Built/installed through sole build entry. Package readback, installed-API syntax, and 10/10 regression checks passed. SHA256: 01e3badee01257132c81e2f7e076a0dc2185bfb20179b82d1df8b7464845e257.
- Next engine check: launch this identifier and pan from the westernmost base across all four bases, then north to the gate; confirm camera is no longer clipped and the top-right panel is visible.
- Outstanding: native FK equipment, 15-hero portrait selector, six shops/catalog, full match-state/wave recovery, minimap regeneration, boss/selection HUD, editor round-trip, gameplay and multiplayer/endurance acceptance. Development label retained.

## Hero staging area — KLS-D-19e9bb94c6
- Added source/heroes.j to explicit module order. Fifteen native-model previews arranged in a labelled 5x3 selection court southwest of the battlefield. Preview selection opens role/ability description and Confirm/Back dialog; duplicate choices allowed.
- Removed player placeholder hero creation and old four-class dialog. Only guarded confirmation/timeout creates the owned level-3 hero, beside the player's Altar. Neutral invulnerable/paused previews are removed with labels when selection finishes.
- Starting armies pause during selection, including confirmed heroes. All active choices or 45-second timeout (Paladin fallback) releases armies and starts a fresh 45-second preparation period. Selection departure drops that slot from the ready requirement.
- Staging camera is local presentation; restored on confirmation/timeout. Hero creation and dialog confirmation use synchronized game events. Back clears local selection so the same preview can be selected again. HUD displays selection countdown.
- Package readback and installed API compilation passed. Existing 10 regression tests passed; they do not simulate selection gameplay.
- Exact next human check: launch KLS-D-19e9bb94c6, select Mountain King preview, choose Back, select it again and Confirm; verify one level-3 Mountain King appears at your Altar and preparation begins at 45 seconds in solo.
- Pending engine checks: all 15 models/abilities, timeout fallback, repeated/late confirmation, simultaneous duplicate picks, departure, staging camera visibility and multiplayer sync. Cross-race support spell adjustments remain part of the broader recovery plan.
- Build SHA256: b956574c2f9829a57b4d83fd8aa88b0f50b072dc0bbf2fb5a10303583897500f. Installed diagnostic remains development-labelled.

## Terrain encoding diagnosis — KLS-D-5cd9f6b28a
- User screenshots show black patches and silhouetted buildings. Found generator writes texture index at byte 5, setting W3E v12 water/boundary flags rather than uint16 low-six-bit texture at offset 4. Reference: https://github.com/ChiefOfGxBxL/WC3MapSpecification/blob/master/Terrain/12.md
- Corrected independent terrain decoding test and added flag validation: two checks failed before fix, all 11 passed after correcting uint16 encoding. Compiled/package readback passed.
- Standard install failed with WinError 32 (file in use). Verified identical copy installed under Maps/KLS-Terrain-Fix-5cd9f6b28a/Terrain-Fix-5cd9f6b28a.w3m.
- Native desktop control is unavailable; CUA initialization also failed with missing kernel assets. No live editor inspection performed.
- Terrain render recovery needs in-game proof. Trees/gates currently runtime-generated, not editor-placed; rock formations remain terrain paint/pathing rather than completed scenery. Do not claim finished landscape.
- Next check: launch this terrain-fix identifier and inspect courtyard/market for black boundary patches. Landscape placement/editor roundtrip and all prior pending acceptance remain outstanding.

## Testing diagnostics — KLS-D-3fd240478d
- Read local Logs/War3Log.txt, War3EditorLog.txt and enumerated Errors. Game log contains map enumeration; editor log last updated 17:31; selection.log empty. No current per-spawn evidence available. Old May crash/desync archives not attributed to current build.
- Added diagnostic wrappers to unit/destructable creation across runtime modules. Check null/type mismatch and unit displacement >256; count attempted creations/failures. Last 64 messages retained, -diag shows summary and last 12 with build identifier. Startup milestones, selections, prep transition, wave spawn and match-end recorded. KLS_Debug gates logging; no rendering correctness claim.
- Added tools/collect_test_logs.py: preserve engine logs + build manifest, source timestamps, hashes and filtered findings under test-results. Explicitly marks played-build unconfirmed; map enumeration alone is not launch proof. In-game ring buffer is not exported to disk.
- Build/API/package checks and 11 regressions passed. Installed unique Maps/KLS-Diagnostics-3fd240478d/Diagnostics-3fd240478d.w3m; verified checksum.
- Next check: start identifier 3fd240478d, type -diag after hero selection and capture output. After closing the game run collector to preserve flushed engine logs. Runtime checks remain pending.

## Complete gate flanks — KLS-D-f10ca3e628
- User screenshots show working grass/gate rendering but long empty strips outside original short gate runs. Extended existing left run outward from -3300 to -7640; right limit from 3300 to 7650. Same 620 spacing, models, scale and inward endpoints; central opening unchanged. 10 left / 11 right sections; outer sections overlap playable boundary at +/-7424. Existing flank pathing remains.
- Diagnostic startup logs barrier section counts. Build syntax/archive readback passed. Collected engine log snapshot; collection does not confirm build played.
- Installed unique Maps/KLS-Gate-Fix-f10ca3e628/Gate-Fix-f10ca3e628.w3m with checksum verification. Visual join/edge coverage pending game check; not a verified release.

## Native equipment, market tiers — KLS-D-9e894e39a9
- Read installed CASC ItemData.slk, UnitMetaData.slk, AbilityData.slk and AbilityMetaData.slk. Native FK pack ebua uses AIni/AEqu; installed equipment field IDs/slots and actual parents were checked. Removed Anya's ATua talent ability from copied pack; pack item Ibpk is unsellable/undroppable and is granted per hero. Removed hidden 18-slot dialog stash and chat transfers. Boss rewards now remain at owner's base if active inventory rejects them.
- Added five tier catalogs x 12 families = 60 unique object IDs. Catalog selects installed FK campaign equipment parents, retains those items' native abilities/models, explicitly maps equipment slot, sets tier prices 150/400/1000/2500/6000, and weapons cost 1.5x. Six separate Goblin Merchant units receive stock for each tier; Field Apothecary has four healing/utility consumables. In-game sale event binds purchases to buyer.
- Still missing from approved plan: exact baseline stat multipliers and scripted rare+ cleave/bleed/frost/absorb/mana/heal effects. Tier bases use authentic native FK items with their native effects; not yet balanced against promised stat table. Do not claim native equipment UI or effects work until engine test.
- Regression tests failed first as expected (catalog absent; custom bag lacks native ability), then passed after implementation. Full suite 13/13 pass. Installed API JASS compile and MPQ readback passed. Build ID KLS-D-9e894e39a9; SHA256 44a47968000f223914e9e66d9555d50caabe1e0e0fc2f4236c3f5fea7df03c76.
- Installed checksum-verified separate map at C:\Users\asphy\Documents\Warcraft III\Maps\KLS-Shops-9e894e39a9\KLS-Shops-9e894e39a9.w3m; previous locked copy left unchanged. Next human check: start this ID; verify Field Pack opens 30 slots/equipment UI; buy one item from each rarity shop and confirm effects/models; check a wrong-slot equip is rejected.
- Multiplayer/effects/endurance/editor acceptance pending. Development label retained.


## 2026-09-27: backpack click and equipment shops — KLS-D-f4eaf32a81

- User-reported failure: pack could not be clicked. Confirmed `iusa=0` in generated item; installed `ebua` has usable=1. Restored usable=1 and native AIni/AEqu/ASde, omitting campaign talents. Explicitly nonperishable, nondroppable, unsellable, zero charges. Equipment Level Threshold (`equ1`, confirmed installed editor string) is zero for all native AEqu levels.
- Replaced inherited tier stats with generated ability records and exact tooltips. One catalog generates all 65 objects, prices, descriptions and runtime catalog entries. Five capes added as chest-slot alternatives. Five paged equipment shops plus apothecary; removed inherited Goblin Merchant stock. Purchase checks range, living hero and gold, charging only on successful item insertion.
- Implemented equipped-gear effects: cleave, bleed, frost/slow, shield, mana-on-cast, healing pulse and cape spell resistance. Hero-owned cooldowns survive swaps; proc damage does not trigger offensive effects. Equip/unequip/use/purchase diagnostics added.
- Failures corrected during verification: generic ability code AIml/AIde/AImm is not a valid parent alias; replaced with installed AIlf/AId1/AImb. Compiler caught reserved local name and malformed callback edit; both corrected before final build.
- Proven: 17 automated checks; installed API compilation; archive lookup/readback including war3map.w3a; installed copy SHA equals manifest. Last engine-proven build remains unknown; this build has NO engine proof.
- Artifact: `C:\Users\asphy\Documents\Warcraft III\Maps\KLS-Equipment-f4eaf32a81\KLS-Equipment-f4eaf32a81.w3m`. SHA `7edd713159e67566b1e10e83c4a1f99904b92d9950bdfbeb736e7c674b330da6`.
- Exact next action: user opens this build, chooses a hero and clicks the pack; record whether native interface opens. No substitute custom storage dialog was added.
- Pending: engine equipment, sales, effects, multiplayer transactions, editor round-trip and the original 40-wave recovery acceptance. Do not publish release.


## 2026-09-27: king name and castle contributions — KLS-D-fcd13fad0a

- Screenshot showed Aurrius the Pure: BlzSetUnitName did not change the Paladin hero's proper name. Added BlzSetHeroProperName to set King Aldric.
- Castle selection now opens a personal synchronized management dialog. Heal: 150 gold/50 lumber for up to 2,000 health. Upgrade: 400+200 per current tier gold/150 lumber, five tiers, each +4,000 max/current HP and +30 base damage. HUD updates immediately.
- Castle buttons and -repair/-upgrade share one non-yielding transaction. Full health, dead king, ended match, inactive player, insufficient resources and max tier cannot charge resources. Stale upgrade quotes after a teammate contribution are rejected, then refreshed without charging the higher price.
- Verified: 17 existing regression checks, installed API compilation, archive readback and installed SHA match. These cover packaging and script generation, not engine behavior of the new menu. No new engine proof.
- Installed `C:\Users\asphy\Documents\Warcraft III\Maps\KLS-Castle-fcd13fad0a\KLS-Castle-fcd13fad0a.w3m` (SHA `941b1b228c99a83ed7a37ff7a70dcb0f6196163e5280d2efdc0f1fb41ea028d5`). Includes preceding backpack/catalog changes.
- Next human check: select the castle and confirm its management menu appears and the king's hover name reads King Aldric. Then test full-health rejection, damaged healing, all five upgrades and concurrent contributions. Backpack/equipment, multiplayer and full recovery acceptance remain pending.


## 2026-09-27: spell targets and mixed invasion — KLS-D-b2706f47e9

- Root cause: Force of Nature had no nearby trees (only distant border/resource belts). Added thirty destructible LTlt trees in ten small groves at x approximately +/-850..1030, y900..4660, beside the fighting lane. Dead grove trees regrow after 60 seconds; main road and player plots remain clear of these placements. Actual navigation and spell-cast acceptance pending.
- Root cause: spawner selected one type per ten-wave chapter. Replaced it with forty generated rosters retaining undead and living attackers in every wave: ghouls, skeletons/crypt fiends, footmen, riflemen and grunts; later abominations, knights, necromancers, shamans, meat wagons, demolishers and tauren. Wave count now uses the wave being spawned. Native Death Coil can damage living attackers; native living/undead ally-healing restrictions remain unchanged. No claim that all race-specific abilities are universally usable.
- Added tracking for undead-owner summons so summoned skeletons participate in wave cleanup. Added native raise-dead/bloodlust autocast orders; actual caster behavior pending. Boss types/mechanics unchanged.
- Verified: installed API compilation, archive readback, 17 existing regressions, all 40 rosters contain living and undead units and fit their allocated table stride, installed SHA match. No engine/multiplayer proof.
- Installed `C:\Users\asphy\Documents\Warcraft III\Maps\KLS-Invasion-b2706f47e9\KLS-Invasion-b2706f47e9.w3m`, SHA `24585785c1084fa83b06945d502d620b4bf63adb351042d0dd94ee4445edb6d7`. Includes castle, backpack and equipment work.
- Next human check: choose Keeper, move beside the road north of the castle and cast Force of Nature on a nearby grove. Then verify treants, tree regrowth and mixed waves; Death Coil targeting and complete wave cleanup remain pending.


## 2026-09-27: closer lumber, signatures and demonic invasion — KLS-D-9bc91a9c6a

- Moved base lumber from four distant trees (roughly 1,600 units from hall) to eight trees per base, in rear-right rows 650/850 units south. Nearest tree is approximately 675 units from hall and roughly 400 from initial workers. Native combat groves remain.
- Added 15 distinct bonus signatures via generated Channel object records and synchronized spell triggers. Automatically granted alongside native hero kits; descriptions in selector/tooltips, Z hotkey, 70 mana/30 sec, level-scaled effects. Includes tree-free Keeper summons and Death Knight support healing independent of living/undead race. Detailed list in HERO-SIGNATURES.md.
- Reweighted invasion: core undead plus increasingly diverse demons; retains one human infantry entry per roster for guaranteed living targets. Verified every unit/summon rawcode against extracted installed UnitData.slk. Added that reference to source hashes.
- Verified 19 tests including binary ability records, visible point-cast configuration, installed summon/enemy aliases and all 40 roster bounds. Full package/API checks passed; installed SHA match. Gameplay, spell icons, pathing and tuning remain unproven. No release claim.
- Installed `C:\Users\asphy\Documents\Warcraft III\Maps\KLS-Heroes-9bc91a9c6a\KLS-Heroes-9bc91a9c6a.w3m`, SHA `e0f0b9a6c2e5f015c9548770ab0e23a87948807171c7fa312726a0f1907f5504`.
- Next human check: Keeper signature Z on open ground should summon three Treants; confirm cast and cooldown. Subsequent pending: all signatures, tree harvesting routes, enemy abilities, new-wave balance, multiplayer and original recovery checklist.


## 2026-09-27: native gear and castle shops — KLS-D-87d1de4c9d

- Replaced custom list dialogs with Warcraft native shop inventory: ten gear stalls (two per tier, 7+6 stock capacity) plus apothecary. Native item icon art and hover tooltips use the same 65-item object catalog and generated prices/stock. Added tests proving all 65 items appear in correct native stock pages and preserve item description/prices.
- Investigated slots against installed common.j and ItemData.slk: native equipment enum is NONE=0, HEAD=1 through TRINKET=8; generated gear mappings match installed equipment parents, `icla=Equipment`, and the native 9-slot `AEqu` interface. The purchase path previously only gave items to normal inventory. It now marks personal owner then calls `UnitEquipItem` immediately; rejection logs rawcode/equipment type and leaves the item in inventory. This diagnoses any remaining game-side metadata issue. Actual engine equip success remains unverified.
- Replaced the castle overflow dialog with its native shop stock and two icon items. Castle purchase events call the shared king transaction, then remove and restock the command item. Short descriptions fit the native hover tooltip.
- Fixes confirmed along the way: restored the catalog generation insertion point so GearData initialization and all stock entries actually compile into runtime. Corrected module ordering for shop purchase calls into castle logic. Updated battlefield test for castle's custom unit alias.
- Verified 19 tests, editable source compile against installed APIs, object/data checks, package archive readback. Installed `C:\Users\asphy\Documents\Warcraft III\Maps\KLS-Native-Shops-87d1de4c9d\KLS-Native-Shops-87d1de4c9d.w3m` SHA `3c7d93a01199b940416c3d8463a356ded1faa522c1cd5020238cdace42e21435`. No live engine proof.
- Next human check: right-click a gear stall as a hero; confirm native icons/tooltips; buy one free-slot weapon and armor and confirm they immediately appear in their equipment slots. Then right-click castle to confirm icons/text and test healing/upgrade costs. If a gear purchase logs native equip rejection, capture `-diag` output before another edit.


## 2026-09-27: shop equip timing and castle tier stock — KLS-D-0d170dd0a7

- Screenshot audit: the item and castle windows shown by the user were the old text-dialog build. A fresh native-shop diagnostic was rebuilt and installed at `C:\Users\asphy\Documents\Warcraft III\Maps\TheKingsLastStand\DIAGNOSTIC-TheKingsLastStand.w3m`; its build manifest SHA-256 is `685bdc44ef4b5803f22c45d8dc86bb663994af1280de27cf1907fe9dde5bad83`. Exact player instructions are in `ITEM-SHOPS.md` and `CASTLE-CONTROLS.md`.
- Gear sale now queues `UnitEquipItem` for 0.05 seconds after the native sell event so Warcraft can finish transferring the sold item first. Successful equips and refusals are logged; on refusal, the owned item remains available and the diagnostic message names the expected equipment slot.
- Fixed castle upgrade stock to start with KUP1 and advance to one correctly priced next-tier item after a successful contribution. Tier item IDs map explicitly to quoted tiers so rejected/stale purchases refund the exact displayed gold and lumber; removed unsupported rawcode string concatenation and the generic unlimited restock that previously defeated progression. Normal merchants and the heal item restock one item after each sale.
- Regression suite: 22/22 passed. Installed API JASS compilation and MPQ component/listfile readback passed; installer verified the copied file against its manifest. The source pipeline contains native item-stock merchants and native castle item controls; the custom shop/castle text dialogs are absent from those controls.
- UI automation could not attach: the computer-use helper exited unexpectedly twice, including after a reset. No live editor/game claim is made. Next human-run check: load the exact map path above from **Single Player → Custom Game**, right-click a quality merchant and verify its icon/hover stat window; buy one weapon and one armor piece and confirm each enters its correct backpack equipment slot; then right-click the castle and verify its heal/next-tier controls and non-overflowing hover text. Record the result against KLS-D-0d170dd0a7. Editor round-trip, all item effects, multiplayer and normal-speed 40-wave acceptance remain pending.


## 2026-09-27: distinct bosses and persistent telegraphs — KLS-D-efdad65e20

- Added boss mechanics as data for waves 10/20/30/40: Bonequake telegraphed slam; Grave Muster skeleton/felguard summons; Siege Blight pauses all three defender tower roles for 8 seconds; The Last March combines all three. The HUD has a dedicated Boss warning row and data-derived, action-specific text that remains visible through the countdown and switches to the suppression timer after it resolves.
- Boss reinforcements use the existing installed skeleton/felguard rawcodes, receive wave-scaled HP/damage, enter the enemy group and alive count exactly once, and order down the central road to King Aldric at y=350. This corrects the previous summons order toward y=-2700, away from the king.
- Tower suppression pauses only completed living Watchtower, Bombard Tower and Sanctuary Tower units; it resumes them after eight ticks and also stops Sanctuary healing during suppression. Fixed Sanctuary group reuse so one player's tower group is cleared before enumerating the next player's units.
- Tests: all 26 regression checks passed, including data mapping, mechanic routing, countdown/HUD coverage, exactly-once summon tracking and kingward summon order. Build ID KLS-D-efdad65e20 compiled against the installed API and passed MPQ readback. Installed copy checksum equals output and manifest: `d9f9dceec35f365ae43553f861c56de62339bb48328ebb773f8679717809cdf6`.
- Installed at `C:\Users\asphy\Documents\Warcraft III\Maps\TheKingsLastStand\DIAGNOSTIC-TheKingsLastStand.w3m`; editor/game proof remains pending. Next precise human check: in this exact build, start wave 10 with the diagnostic `-wave 10` command and confirm the HUD shows Bonequake's countdown, then that the marked slam resolves. If it does not, type `-diag` and capture the full output. Boss waves 20/30/40, shops, equipment, castle transactions, editor round-trip, multiplayer and endurance remain pending.

## 2026-09-27: player departure flow — KLS-D-f8fbeccb9f

- Current task: complete the startup gate before further gameplay changes. Last package-proven build is KLS-D-f8fbeccb9f; this identifier does not yet have engine/editor proof. Earlier screenshots refer to older identifiers.
- Implemented `EVENT_PLAYER_LEAVE` handling for all four defender slots. The first active departure marks that slot inactive and decrements the active-player count, so it no longer affects later wave scaling or personal rewards. During hero selection, the remaining active slots are re-evaluated immediately. If nobody remains, the match ends and the match timer stops. No unit owner or alliance is changed; the departed army retains its current orders.
- Regression evidence: the two new focused checks failed before the implementation because the handler and event registrations were absent; both pass afterward. Full regression suite: 28/28. Installed API syntax compilation and MPQ archive readback pass.
- Build SHA-256: `3a41b79902afe5c8ed70bcd5b4c775c0f701fce5c6e7990d5d80f955c532fc8c`. Installed copy was copied and byte-verified at `C:\Users\asphy\Documents\Warcraft III\Maps\TheKingsLastStand\DIAGNOSTIC-TheKingsLastStand.w3m`.
- Exact next action: complete the World Editor round-trip first: open `build/DIAGNOSTIC-TheKingsLastStand.w3m`, Save As `build/Editor-Roundtrip.w3m`, close/reopen, and Test Map. Confirm the `KLS-D-f8fbeccb9f` identifier, hero selector, king/castle, custom resources, countdown, and no premature victory. Then repeat through Custom Game. The approved plan requires this startup gate before further gameplay changes.
- Still pending: World Editor save/reopen/Test Map for this identifier; live hero, equipment, market, castle, terrain and pathing checks; 2–4 player join/leave, synchronization, three-player scaling; boss waves 20/30/40; all 40 waves and normal-speed endurance. No release build is authorized by the current evidence.

## 2026-09-27: engine-log snapshot for startup gate — KLS-D-f8fbeccb9f

- Tried the Windows app-control initialization twice (reset once); both attempts failed before `list_apps` with `windows sandbox failed: helper_unknown_error: apply deny-read ACLs`. The initial process filter missed the spaced name `World Editor`; a later exact query found the stale editor process recorded below. No Warcraft game process is running.
- Ran `python -B kings-last-stand/tools/collect_test_logs.py`; snapshot: `test-results/20260927T210609783112Z-KLS-D-f8fbeccb9f`. The collector correctly records `played_build_confirmed: false` because its input logs can be stale.
- Current `War3Log.txt` contains no launch of KLS-D-f8fbeccb9f. Its latest map-open references are older KLS-Shops-9e894e39a9 and KLS-Heroes-9bc91a9c6a. It contains 34 `model creation failed` messages after those older opens (22 empty paths, 8 `.mdl`, and four legacy HumanBarracks/Blacksmith birth/death paths). These are leads to compare against a log captured after launching the current ID; they do not prove a current-build failure.
- `War3EditorLog.txt` is stale and points to an earlier editor launch of `build/DIAGNOSTIC-TheKingsLastStand.w3m`; `selection.log` is empty. No current startup, missing-spawn, or editor-roundtrip result can be inferred.
- Updated `PLAYTEST.md` with the exact editor-first startup check and log collector command. Next action is to preserve any needed edits from the existing stale editor session, reload the current on-disk KLS-D-f8fbeccb9f, Save As a round-trip copy, reopen it, and Test Map. Direct Custom Game launch follows the editor check. The current build remains development-labelled.

## 2026-09-27: World Editor launch attempt — KLS-D-f8fbeccb9f

- The `@oai/sky` Windows UI helper failed during initialization twice (including after a reset) with `windows sandbox failed: helper_unknown_error: apply deny-read ACLs`.
- Tried launching the installed World Editor executable with the same `-launch -loadfile` arguments recorded in the old editor log. That launch process started, opened `War3.w3mod`, then shut down normally (exit code 0) in under one second; it never logged opening the map. Repeating with the install root as working directory produced the same result. A separate stale editor process remained running, as recorded below.
- The direct launch was useful diagnosis only; no editor save/reopen or gameplay check passed. Switch the required human check to launching Editor from the Warcraft III launcher, then run the round-trip described in `PLAYTEST.md`. This restores the approved editor-first order before direct Custom Game testing.

## 2026-09-27: stale World Editor session found — KLS-D-f8fbeccb9f

- Read-only process inspection found an existing responsive `World Editor` window (PID 47232), titled `Warcraft III World Editor - [C:/Users/asphy/Documents/Warcraft3Maps/kings-last-stand/build/DIAGNOSTIC-TheKingsLastStand.w3m]`. It was started 2026-09-26 12:27 local; the diagnostic file on disk was rebuilt at 2026-09-27 20:57 UTC. The open process therefore predates and cannot prove the current file’s contents.
- Battle.net is already running. Do not replace, close, or save over this existing editor state automatically; it may contain user work. The UI-control helper still cannot initialize, so no editor UI action was taken.
- Updated `PLAYTEST.md` to warn that this existing in-memory map is stale and must be saved separately if needed, then reopened from disk before the editor round-trip. The exact startup gate remains pending.

## 2026-09-28: empty native shop panels — KLS-D-51f7f1f807

- User reported that the visible market stalls were empty. The prior `WorldEditTestMap.w3x` was inspected read-only; its runtime script contains the same `KLS-D-f8fbeccb9f` ID as `Editor-Roundtrip.w3m`, so the report matched the editor Test Map artifact rather than an unrelated downloaded map.
- Root cause in Object Editor data: custom merchant `hS00` and castle `hC01` each overrode their ability lists with `Avul,Apit,Asid,Asud`, omitting `Aneu` (Select Hero / Select User). Stock calls and all 65 custom item records were present in the runtime/package, but the native shop lacked its buyer-selection ability.
- Added a focused regression that parses the custom unit records and requires `Aneu`, `Apit`, and `Asid` on both `hS00` and `hC01`. It failed before the fix for both units, then passed after adding `Aneu` to their ability lists.
- Updated shop instructions: approach within 700, select the shop, use Select Hero if Warcraft has not assigned the buyer, then click an icon. Selecting King Aldric's Castle shows its native heal/upgrade stock.
- Full focused regression suite: 29/29 passed. Rebuilt through `python tools/build_map.py --install-diagnostic`. Installed-API syntax compilation and archive readback passed.
- New build **KLS-D-51f7f1f807**, SHA-256 `8bd8ef99780d04f72aa079bd2dc2a11e2edff2c1468bd38a6e7fc3bc9a946118`. Build and installed map hashes match. Manifest remains development-labelled with editor/game startup pending.
- The open World Editor process still has the separate `Editor-Roundtrip.w3m`; it was not changed. Exact next action: launch the newly installed build from Custom Game, select an Uncommon Arms & Armor stall, verify icons and a stat tooltip, buy one item, and confirm castle controls also appear. If empty, type `-diag` and send the complete command-card screenshot. Multiplayer and 40-wave acceptance remain pending.


## 2026-09-28: equipment slot and installed item ID audit — KLS-D-dab035c25e

- Current task: resolve the user's report that bought gear, including boots, cannot be equipped; audit custom item/hero spell IDs and missing icon assignments against the installed Forsaken Kingdom editor data.
- Updated native item parent assignments from the installed `ItemData.slk`. All 65 custom item rawcodes are unique and verified not to collide with installed item IDs. Every parent has the catalog's expected native equipment slot. All equipment fields inherit the slot and icon from a real parent item; test also verifies the installed shared metadata defines `iequ` as an item equipment type. Only two native equipment-class bow bases exist, so the bow tiers reuse those correct bow visuals rather than using sword/lance art. No separate installed `ItemMetaData.slk` was available by the editor data path; current item slot types are defined in ItemData and shared UnitMetaData.
- Existing deferred purchase handler still calls `UnitEquipItem` after Warcraft's shop-transfer event, logging native success/refusal. Object-generation regression confirms correct equipment slot inheritance, but no live game interaction has verified an equip. All 15 custom hero signatures have unique rawcodes with configured command-button paths; asset rendering itself remains a pending in-game/editor check.
- Verification: 31/31 regression tests passed. Installed API script compilation, MPQ inventory/readback and component comparison passed. Diagnostic was installed with a build-specific filename because the standard diagnostic file was locked by a running Warcraft process. Installed SHA-256 matches output and manifest.
- Last proven package build **KLS-D-dab035c25e**, output SHA-256 `80d05636b9d6dd948d295da4249815834c29ebfee4ce39d7e458b232df589b8b`. Playable copy: `C:\Users\asphy\Documents\Warcraft III\Maps\TheKingsLastStand\DIAGNOSTIC-KLS-D-dab035c25e.w3m`.
- Exact next action: test this exact copy via **Single Player → Custom Game**. Buy one Common Boots item from the Quartermaster, open the Forsaken Field Pack, move the boots from storage into the Boots equipment slot, and check that the item stays equipped and its movement bonus appears. If the stock is empty or equip is refused, send the command-card/inventory screenshot and complete `-diag` output. Keep this as a development build until the UI, editor round-trip, multiplayer and 40-wave checks pass.
- Failed check: overwriting the standard installed diagnostic path failed with Windows sharing violation because a Warcraft process is using it; the current versioned copy is byte-verified instead. No installed data extraction errors remain in the supported workflow. Editor round-trip and latest in-game startup/equip/spell icon checks are pending.


## 2026-09-28: build-specific diagnostic installation — KLS-D-85e2f5e290

- Current task: user reports that purchased gear including boots cannot be equipped; connect the item catalog and custom spell data to current installed Forsaken Kingdom editor references and make the updated map straightforward to test.
- Changed: all 65 custom gear rawcodes are collision-checked against installed `ItemData.slk`; equipment parents supply the matching native equipment slot and icon. All but the two bow tier variants use distinct native item parents; the native editor set has only two equipment bows. Tests confirm all item records retain their inherited slot/icon rather than overwriting those fields. Added path checks for all 15 custom signature ability button icons. The installed JASS API/object tables are pinned in `tools/reference/installed/provenance.json` and build manifest.
- Build/install workflow: diagnostic copies are now named `DIAGNOSTIC-{build_id}.w3m`. Re-running install for the same hash verifies and reuses the file; it will not overwrite a same-ID file with different bytes. This avoids collisions with maps currently open in Warcraft.
- Verification: 32/32 regressions passed. Installed API script compilation, archive inventory/readback, and all output/install/manifest SHA-256 comparisons passed. Build **KLS-D-85e2f5e290**, SHA-256 `4003beebaf535cbada2703a0882f3c19a7c806da8a09d2fa6e53e6950170a088`. Output: `C:\Users\asphy\Documents\Warcraft3Maps\kings-last-stand\build\DIAGNOSTIC-TheKingsLastStand.w3m`. Installed test map: `C:\Users\asphy\Documents\Warcraft III\Maps\TheKingsLastStand\DIAGNOSTIC-KLS-D-85e2f5e290.w3m`.
- Still pending: live test of shop stock visibility and native equip/unequip for each slot, in-game rendering of all signature icons, World Editor open/save/reopen/Test Map, full spell/effect acceptance, 2–4 player sync and normal-speed 40-wave matches. Static metadata and icon-path tests do not prove visual engine behavior.
- Exact next action: in Single Player → Custom Game, load the installed `DIAGNOSTIC-KLS-D-85e2f5e290.w3m`. Buy Common Boots from the Quartermaster, move them from the Forsaken Field Pack storage grid to the Boots slot, and confirm the movement bonus. If the shop or equip action fails, send a screenshot of the command card/backpack and the full `-diag` output. Keep the build labeled development.


## 2026-09-28: Definitive edition spell icon audit — KLS-D-570aba1f6f

- Current task: resolve the user's report that purchased equipment will not equip and their suspicion that new hero spells/items have missing IDs or icons.
- Confirmed item data: extracted current ItemData, UnitData, AbilityData and shared metadata from the installed Warcraft build. All 65 custom gear rawcodes avoid installed ItemData collisions; equipment parents map to the correct head/chest/gloves/boots/ring/primary/offhand/trinket slots. Item records inherit `iequ` and `iico` from their verified parents. The engine's `UnitEquipItem` purchase handler remains in place after the delayed shop transfer and logs refusals. The manual backpack transfer and bonus check still needs a game run.
- Confirmed spell icon defect: the prior signature records wrote image paths to `areq`, leaving `aart` unset, and all guessed `.blp` paths were wrong for this installed Definitive edition. CASC enumeration found the current command-button texture set (1,534 files), exposed four missing guessed names, and supplied valid `.dds` assets. Updated all 15 custom signatures to store a real installed path in `aart`, choosing these matches for the prior missing names: `HeroAvatarOfFlame`, `StormOfSteel`, `Frost`, and `TheBlackArrow`. Extraction now writes and hashes `tools/reference/installed/commandbuttons.txt`; build provenance pins it with the installed item/hero/ability tables.
- Installer now uses one map file per build identifier and reuses only identical bytes, avoiding the sharing violation when an older test map is open.
- Verification: 32/32 regressions passed. New checks verify every signature `aart` resolves in the installed asset index, ability IDs/fields are valid, item rawcodes do not collide, inherited item slots/icons are retained, and installer is idempotent. Installed API compilation, MPQ archive readback and output/install/manifest hash match passed.
- Last package-proven build **KLS-D-570aba1f6f**, SHA-256 `c137508ab02230536df40c680db388833bb0a84192f647f45dc93dfe3fc62000`. Output: `C:\Users\asphy\Documents\Warcraft3Maps\kings-last-stand\build\DIAGNOSTIC-TheKingsLastStand.w3m`. Installed Custom Game copy: `C:\Users\asphy\Documents\Warcraft III\Maps\TheKingsLastStand\DIAGNOSTIC-KLS-D-570aba1f6f.w3m`.
- Still pending: live purchase and boot-slot transfer/effect; visual rendering of signature textures and shop item icons; World Editor save/reopen/Test Map; all gear effects; multiplayer and 40-wave endurance. These remain development artifacts until passed.
- Exact next action: test this installed build via **Single Player → Custom Game**. Buy one Common Boots item from the Quartermaster, then move it from pack storage into the Boots slot and check the movement bonus. If either the stock or equip action fails, send the command-card/backpack screenshot and full `-diag` output. Next check after that: confirm a signature spell button renders, then continue the editor round-trip gate.


## 2026-09-28: accurate equipment failure diagnostics — KLS-D-b25af91597

- Added an expected equipment-slot value to generated catalog data and fixed equip logs to report that slot. The old log accidentally printed the item's family number as its equipment type, so a boot refusal could report the wrong value. Purchase success and failure now say `equipment slot id=...`; boots are slot 4.
- Verification: new regression reproduced the bad value (65 catalog entries lacked slot diagnostic data and equip log read family index), then passed after the fix. Full suite: 33/33. Installed API compile, MPQ package checks and installed file SHA match passed.
- Current package build **KLS-D-b25af91597**, SHA-256 `6376ddf918081e9ff13493cadc492a366ee9c5d722daff90a25fe2905f13350a`. Output: `C:\Users\asphy\Documents\Warcraft3Maps\kings-last-stand\build\DIAGNOSTIC-TheKingsLastStand.w3m`. Installed path: `C:\Users\asphy\Documents\Warcraft III\Maps\TheKingsLastStand\DIAGNOSTIC-KLS-D-b25af91597.w3m`.
- Current task and next proof: user tests this exact file by buying Common Boots at the Quartermaster, transferring them from backpack storage into Boots, and confirming movement bonus. If blocked, request the command-card/backpack screenshot and full `-diag` report, which now contains the right slot ID. Editor icon rendering, editor round-trip, multiplayer and 40-wave checks remain pending. Maintain development label.
## 2026-09-28: attribute gear, recipes, level-100 spell ranks and recovery systems — KLS-D-51960bfa2a

### Current task and last proven build

- Current task: add Strength, Agility and Intelligence equipment, craftable item variants, level-100 hero spell ranks, an attribute tome shop beside the Apothecary, a restoring pool south of the castle, and longer breaks before bosses.
- Last package-proven build: KLS-D-51960bfa2a. Output: build/DIAGNOSTIC-TheKingsLastStand.w3m.
- Output SHA-256: 92d3697fd8700750b5a3f4e4d7c8c6eca4a76ea3115c129f398fd25949ddb194.
- Installed copy: C:\Users\asphy\Documents\Warcraft III\Maps\TheKingsLastStand\DIAGNOSTIC-KLS-D-51960bfa2a.w3m. Its SHA-256 matches the output.
- This workspace has no Git repository, so no Git diff or branch state is available.

### Changed behavior

- Added Strength, Agility and Intelligence equipment families across five qualities. Gear bonuses serialize as actual native stat abilities and remain subject to native equipment slots.
- Added Sage's Archive (hS02) beside the Field Apothecary. Its nine personal tomes grant +5, +10 or +20 Strength, Agility or Intelligence on purchase.
- Added three Master Forge recipes. They require personally owned components and a fee; the transaction verifies component ownership and delivery space, and is intended to preserve components/refund the fee on failure.
- Set the map's maximum hero level to 100. All 15 selectable hero skill sets now expose ten ranks; ranks 7–10 extrapolate the final native rank curve with bounded growth. Ranks advance each ten hero levels after native unlock.
- Added King's Restoring Spring at (-900,-1600), south-west of the castle. It restores nearby active heroes by up to 200 health and 120 mana every five seconds within 450 range.
- Increased cleared-wave breaks to 60 seconds and breaks before waves 10, 20, 30 and 40 to 120 seconds.
- Updated README.md, ITEM-SHOPS.md and PLAYTEST.md with this diagnostic's location, features, limits and first human-run check.

### Evidence and failed checks

- The first generated-script compilation caught an invalid hero-rank conditional chain (first branch closed before subsequent elseif clauses). Reworked the generator to emit one valid if/elseif chain; added a regression for the first branch.
- Full focused suite: 42/42 passed. It includes object-data attribute serialization, book stocks, recipe failure safety, level-10 ability records and compilation of reconstructed editor sources.
- Installed Warcraft API syntax compilation passed. MPQ archive inventory contains 23 members and every component passed readback. Manifest status remains development: startup proof pending.
- Versioned diagnostic installed successfully; installed SHA matches. These results do not prove live shop display, tome purchase, item equip, pool behavior, timer accuracy or spell ranking in Warcraft.

### Exact next action and remaining checks

- First human-run check: launch DIAGNOSTIC-KLS-D-51960bfa2a through Single Player → Custom Game, verify its build ID, then select Sage's Archive and report whether tome icons/tooltips display. Buy one tome only if its icon and tooltip are visible and confirm the matching attribute changes. See PLAYTEST.md.
- If the Archive check passes, test gear transfer/equip, pool restoration, 60/120-second timers, all 15 hero rank curves and recipes.
- Still pending: open/save/close/reopen/Test Map in World Editor; direct Custom Game startup; all gameplay acceptance; actual 2-player and 4-player sync, 3-player initialization, and 2-/4-player 40-wave endurance. Keep the map development-labelled.



- Placement regression note: the first check measured 1,100 map units between the Archive and Apothecary, exceeding the 750-unit adjacency bound. Moved the Archive from x=4550 to x=4100 (650 units from the Apothecary at x=3450); the targeted check and full 42-test suite then passed. Final installed build is KLS-D-51960bfa2a.


## 2026-09-28: native spell rank preservation and regression recovery — KLS-D-2b91b30b7c

### Current task and last proven build

- Current task: continue the approved full recovery work and finish the added attribute gear/books, crafting recipes, level-100 hero progression, restoring pool and longer wave breaks.
- Current package-proven diagnostic: **KLS-D-2b91b30b7c**.
- Output: `build/DIAGNOSTIC-TheKingsLastStand.w3m`.
- Output and installed SHA-256: `8f447a6b47ada8de9979d0bc6d3637a22732b11a4297a9af6fcb2d4e7dac6eee`.
- Installed copy: `C:\Users\asphy\Documents\Warcraft III\Maps\TheKingsLastStand\DIAGNOSTIC-KLS-D-2b91b30b7c.w3m`.

### Changes and evidence

- Found and fixed an installed-data parsing failure: the editor's missing-rank sentinel appears as whitespace-padded ` - `. The rank generator now trims each cell before treating empty/dash values as missing. The new `AEar` regression failed first with `IndexError`, then passed; this also restored the tiered-attribute item regression and all hero ability record generation.
- Added a native-rank preservation regression. It failed because the previous generator changed Devotion Aura's installed rank 4 from 4.5 to 5.0. Removed that native-rank clamping; installed ability values are preserved and only extended ranks are extrapolated. The native-data test then passed.
- Added checks for generated rank scheduling at levels 50, 51 and 100. The cap is 100, all 15 selectable heroes retain four regular abilities configured for ten ranks, and the generated runtime caps ranks at ten.
- The feature set is statically present: five quality tiers of strength/agility/intelligence equipment, nine permanent attribute tomes in Sage's Archive beside the Apothecary, three personal Master Forge recipes, King's Restoring Spring south of the castle, 60-second ordinary breaks and 120-second boss breaks.
- Full regression suite: **45/45 passed**. Installed API syntax compilation and MPQ inventory/readback passed. Manifest records API syntax and archive readback as passed; editor round-trip, game startup and multiplayer remain pending.
- Output and installed map SHA-256 match exactly.
- Final review for this continuation: self-review of the changed generator, focused tests, build manifest and updated current-build docs; no additional issue found in that scope. This workspace has no Git repository, so a branch diff review is unavailable. This is not a review or acceptance of the unverified full game.

### Ruling

- Ruling: preserve every installed spell-rank value, even where a native curve dips, and use the median native slope only to extrapolate new ranks — the approved plan says to use installed ability data and continue it; rewriting an installed rank conflicts with that. Cost if wrong: an intentional native non-monotonic effect remains as authored by Warcraft rather than being smoothed.

### Logs and next action

- Log snapshot: `test-results/20260928T002735962671Z-KLS-D-2b91b30b7c`. It is linked to the package hash but records `played_build_confirmed: false`. `War3Log.txt` is an old map-catalogue scan with no current build ID; `War3EditorLog.txt` records the earlier 2026-09-27 editor open. Neither supplies current startup or spawn-error proof.
- Exact next human check: open `build/DIAGNOSTIC-TheKingsLastStand.w3m` in World Editor, Save As a separate `build/Editor-Roundtrip-KLS-D-2b91b30b7c.w3m`, close/reopen it and Test Map. Confirm the visible ID, hero selector, custom resources, king/castle, countdown and absence of premature victory. Then launch the installed version through Custom Game. Do not overwrite the diagnostic source map.
- After the startup gate: test the Archive icon/tooltips and tome stat increase, backpack equip, recipe transactions, restoring pool, spell ranks and wave timers. Still pending: full gameplay acceptance, all four bosses/wave cleanup, actual 2/3/4-player synchronization, and complete 2-/4-player 40-wave endurance. Keep development label.

## 2026-09-28: spawn-failure diagnostics and null-handle safety — KLS-D-3fe621c333

### Current task and last proven build

- Current task: continue the approved full recovery plan, including the latest attribute gear/books, item recipes, spell ranks above level 50, the restoring pool and longer wave breaks.
- Current package-proven diagnostic: **KLS-D-3fe621c333**.
- Output: `build/DIAGNOSTIC-TheKingsLastStand.w3m`.
- Installed copy: `C:\Users\asphy\Documents\Warcraft III\Maps\TheKingsLastStand\DIAGNOSTIC-KLS-D-3fe621c333.w3m`.
- Output and installed SHA-256: `8933404df95c150a015d9c2a88e48f13774f32daa48bd1f93f51d51a67786786`.

### Changes and evidence

- Spawn audit found that failed enemy and boss-summon creation could still be dereferenced and counted, risking a script error or wave stall. Added failure aborts and exactly-once group/count handling.
- Extended the same guard to startup gates, scenery trees, shops, mines, halls, Altars, workers, hero previews/selections, grove trees, the restoring spring and signature summons. Routed temporary slow-effect units through the shared diagnostic creation wrapper.
- The new callsite safety regression failed before the fixes; it now verifies null guards across startup and combat creation paths. The JASS helper had to move earlier in the explicit module order; editor-source compilation caught and verified both declaration-order fixes.
- Full regression suite: **49/49 passed**. Reconstructed editable sources compile against the installed API. The build passed installed-API syntax and MPQ readback checks; manifest inventories 23 packaged components. Output and installed map hashes match.
- Feature checks still pass statically: 15 selectable heroes, ten native ranks up to level 100, tiered stat equipment, nine attribute tomes, three crafting recipes, an off-route restoring spring, 60-second normal breaks and 120-second boss breaks.

### Logs and pending checks

- Log snapshot: `test-results/20260928T005456649287Z-KLS-D-3fe621c333`; `played_build_confirmed` is false. It has no current build ID in the game log; the editor log points to the earlier 2026-09-27 launch. No claim is made about current-build visual spawning or script errors.
- Exact next human check: preserve any edits in an older open World Editor session, then open `build/DIAGNOSTIC-TheKingsLastStand.w3m`, Save As `build/Editor-Roundtrip-KLS-D-3fe621c333.w3m`, close/reopen that copy and Test Map. Confirm the on-screen build ID, 15-hero selection court, custom resources, castle/king, first-wave countdown, and no automatic victory. If anything is missing, type `-diag` and send its full output plus a screenshot.
- After editor round-trip: launch the installed diagnostic via Custom Game. Still pending are every live shop item/equip/tome/recipe effect, pool and wave timers, all construction/king/boss systems, 2/3/4-player synchronization, and normal-speed 2-/4-player 40-wave endurance. Keep development label.

## 2026-09-28: occupied-slot setup, shared bounty and boss victory — KLS-D-64d7e969ab

### Current task and last proven build

- Current task: continue the approved full recovery plan and validate its multiplayer initialization, enemy reward sharing, boss reward timing and final victory rules.
- Current package-proven diagnostic: **KLS-D-64d7e969ab**.
- Output: `build/DIAGNOSTIC-TheKingsLastStand.w3m`.
- Installed copy: `C:\Users\asphy\Documents\Warcraft III\Maps\TheKingsLastStand\DIAGNOSTIC-KLS-D-64d7e969ab.w3m`.
- Output and installed SHA-256: `cf77930ef80a5107c5ab7a3234dffa9eb30750d00b2cabf53ae1880acdd95369`.

### Changes and evidence

- Removed neutral mines and reserved hall units from closed slots. Active players alone now receive a mine, Town Hall, Altar and five workers; all four terrain plots remain laid out for the 2–4 player map.
- Enemy bounties now divide equally among active defenders. Remainder gold goes to the lowest-numbered active slots first. A regression reproduced last-hitter-only payout before the change and checks odd splits, departed slots and solo payout.
- Boss rewards now fire once when the boss dies, even while escorts remain. Wave 40 ends immediately when its boss dies and King Aldric is alive; king death takes precedence. Previously the match waited for every escort.
- Recipe crafting now restores both components and refunds the fee if native output-item creation fails, before applying item ownership or inventory calls to the null output.
- Full regression suite: **53/53 passed**. Installed-API syntax, 23-component archive readback, source hashes and output/installed map SHA-256 all match.

### Logs and pending checks

- Log snapshot: `test-results/20260928T011005230629Z-KLS-D-64d7e969ab`; `played_build_confirmed` is false. Warcraft and editor logs are still from prior sessions and contain no evidence that this build was opened or played.
- Exact next human check remains the editor round-trip in `PLAYTEST.md`: preserve any older editor work, open `build/DIAGNOSTIC-TheKingsLastStand.w3m`, Save As `build/Editor-Roundtrip-KLS-D-64d7e969ab.w3m`, reopen it and Test Map. Confirm the build ID, selector, active-player base, King Aldric, countdown and no victory. If anything is missing, send a screenshot and full `-diag` output.
- Then launch the installed map in Custom Game. Still pending are live shop/backpack/recipe/tome checks, pool and timers, all structures and boss mechanics, 2-/3-/4-player sync, and full 40-wave matches with two and four players. Keep development label.

## 2026-09-28: longer preparation intervals — KLS-D-a37ac8c2fb

### Current task and last package-proven build

- Current task: carry the approved item/hero progression systems into the current diagnostic and lengthen normal and boss-wave preparation time.
- Current diagnostic build: **KLS-D-a37ac8c2fb**.
- Workspace output: `build/DIAGNOSTIC-TheKingsLastStand.w3m`.
- Installed Custom Game map: `C:\Users\asphy\Documents\Warcraft III\Maps\TheKingsLastStand\DIAGNOSTIC-KLS-D-a37ac8c2fb.w3m`.
- Workspace and installed SHA-256: `73acb5b29f0f045c9db5ebc5ecd62eda63589a6a3e4811f3c2b7786a8ba182cc`.

### Changes and evidence

- Increased normal cleared-wave preparation from 60 to 90 seconds and pre-boss preparation from 120 to 180 seconds. Hero selection and initial preparation remain 45 seconds.
- The current map source/package already includes five-tier Strength/Agility/Intelligence gear, three personal Master Forge combinations, level-100 heroes with ten-rank native spell data, a health/mana spring south of the castle, and Sage's Archive with nine attribute tomes beside the Field Apothecary. Their live in-game shop/equipment behavior remains unverified.
- Updated `PLAYTEST.md`, `ITEM-SHOPS.md` and `README.md` to identify the new diagnostic build and timer values.
- The timer regression failed first against the old 60/120 values, then passed after the change.
- Full regression suite: **53/53 passed**. Installed-API syntax compilation and complete MPQ inventory/readback passed. The installed map hash matches the workspace output hash.
- Manifest status remains `development: startup proof pending`; editor round-trip, current-build game startup, multiplayer, live gameplay and endurance checks remain pending.
- Fresh log snapshot: `test-results/20260928T012346690119Z-KLS-D-a37ac8c2fb`. It is hash-linked to this build but records `played_build_confirmed: false`. The cached Editor log's only matching entry is a Sep 27 command-line launch; `selection.log` is empty. No current-build spawn or script errors were available to assess.
- Attempted to open the map in World Editor visibly. The `-launch -loadfile` invocation opened `War3.w3mod` then logged shutdown 0.4 seconds later; a normal visible launch exited with code 0 and left no WorldEditor process. No usable editor window or Test Map result was produced in this session.

### Ruling

- Ruling: increase the previously approved post-wave waits from 60/120 to 90/180 seconds — the latest user direction asks for longer wave breaks, especially before bosses; this preserves 45-second selection/initial setup and doubles the normal-to-boss interval. Cost if wrong: the longer downtime may slow the match pacing.

### Next check

- Human-run startup gate: open `build/DIAGNOSTIC-TheKingsLastStand.w3m` from the desktop World Editor's File → Open, Save As `build/Editor-Roundtrip-KLS-D-a37ac8c2fb.w3m`, close/reopen that copy and Test Map. Confirm the ID, hero selector, resources, King Aldric and castle, countdown and no automatic victory; then launch the installed map through Custom Game. Continue with the shop/tome/gear/recipe/spring checks and later multiplayer/endurance acceptance. Keep the build labelled development.

## 2026-09-28: immutable diagnostic outputs and stale-map cleanup — KLS-D-fd638ddcf5

### Current task and last package-proven build

- Current task: remove diagnostic map ambiguity, preserve the open World Editor document, re-pin the installed API provenance, and resume the approved startup gate without additional gameplay changes.
- Current build: **KLS-D-fd638ddcf5**.
- Workspace artifact: `build/DIAGNOSTIC-KLS-D-fd638ddcf5.w3m`.
- Installed Custom Game artifact: `C:\Users\asphy\Documents\Warcraft III\Maps\TheKingsLastStand\DIAGNOSTIC-KLS-D-fd638ddcf5.w3m`.
- Workspace and installed SHA-256: `48c960e485bd9c81154c13c4ce73ec0b33ac21059572a81a3add8436a268aafd`.
- Manifest remains `development: startup proof pending`.

### Changes and evidence

- The live `War3Log.txt` showed the game opening the old unversioned `DIAGNOSTIC-TheKingsLastStand.w3m` three times. That installed file was 973,265 bytes with SHA-256 `8bd8ef99780d04f72aa079bd2dc2a11e2edff2c1468bd38a6e7fc3bc9a946118`; it did not match the then-current 1,241,341-byte build. The log's map-open entries may be menu scans, so this proves the old artifact was read, not that its match reached gameplay.
- Two `model creation failed - .mdl` lines occurred immediately after that old map's 01:06 log entries, followed later by blank-path and engine asset-path failures. These are recorded in `test-results/20260928T080427670954Z-KLS-D-fd638ddcf5/findings.txt`; their source is not proven and must not be attributed to the current build without a fresh test.
- Installer regression failed first because old diagnostic files remained visible beside the new one. It now archives prior project-named diagnostics under `backups/installed-diagnostics/<timestamp>-<build-id>`; the old copies remain recoverable. The live Custom Game folder now contains only `DIAGNOSTIC-KLS-D-fd638ddcf5.w3m`.
- The build pipeline now emits an immutable build-tagged workspace map. A regression that ran a real package build failed against the former shared filename, then passed while confirming an older file at that path remained unchanged.
- Windows Restart Manager identified the already-running World Editor (PID 47232) holding `build/DIAGNOSTIC-TheKingsLastStand.w3m`. Its window title still names that old fixed path. The failed rebuild did not alter it; the old workspace artifact still hashes to the previous `KLS-D-a37ac8c2fb` build. New builds use their own files, leaving the open editor document in place.
- A full test run initially caught changed installed `.build.info` provenance. Re-extraction updated the fingerprint to `9634415670e63868c82f3bc167dc8f8f127550382d817a63b561f99e77e1ffd4`; all referenced item, unit, ability, metadata and icon tables retained the same hashes. The focused API test passed after refreshing provenance.
- Full suite: **55/55 passed**. Installed-API syntax compilation, 23-member MPQ inventory/readback, and the workspace/installed map hash comparison passed.
- Current log snapshot: `test-results/20260928T080427670954Z-KLS-D-fd638ddcf5`; `played_build_confirmed` is false. It predates any opening of this new build. No current-build Editor round-trip, game startup, in-game spawn diagnostics, multiplayer or endurance evidence exists.

### Rulings

- Ruling: use immutable build-tagged workspace artifacts and archive previous diagnostic copies out of the Custom Game folder — the observed user test selected an old unversioned artifact, and the editor had the output locked. Preserve the old files so an open/older working copy is not destroyed. Cost if wrong: the Custom Game list will no longer offer earlier development diagnostics directly; they are recoverable from the project backup folder.
- Ruling: refresh installed API provenance after the `.build.info` change, even though relevant object tables are byte-identical — the builder correctly treats the installed game build as part of compatibility evidence. Cost if wrong: build IDs change when Blizzard updates installation metadata without changing declarations.

### Exact next action and remaining checks

- Preserve any edits in the existing World Editor tab before switching away from `build/DIAGNOSTIC-TheKingsLastStand.w3m`. Open `build/DIAGNOSTIC-KLS-D-fd638ddcf5.w3m`, Save As `build/Editor-Roundtrip-KLS-D-fd638ddcf5.w3m`, close/reopen that copy, and Test Map. Confirm the visible ID, 15-hero selector, custom resources, King Aldric/castle, countdown, and no victory. Then launch the sole installed map `DIAGNOSTIC-KLS-D-fd638ddcf5.w3m` through Custom Game.
- If any structure, shop or unit is missing, capture a screenshot and full `-diag` output, then collect fresh engine logs. Only after this startup gate should we resume live item/backpack, tome, recipe, pool, wave, multiplayer and 40-wave endurance checks. Keep the build labelled development.

## 2026-09-28: reward feedback, native gear movement, spring cadence — KLS-D-dddc30394a

### Current task and last package-proven build

- Current task: make per-kill gold visible, allow normal equipment to move between the native backpack/normal inventory and vendor buyback, make the restoration pool tick progressively, and maintain a per-build changelog.
- Current development build: **KLS-D-dddc30394a**.
- Workspace artifact: `dist/KLS-D-dddc30394a-Development.w3m`.
- SHA-256: `d646a4a3de78b4e8cbeb1bed6ab5121344565227547dcca7c60c6255ee2d05ab`.
- Changelog: `CHANGELOG.md`, section for this exact build. `tests/test_build_changelog.py` checks that the current manifest's build ID and hash are documented.
- The earlier user-reported Test Map pass remains attached to `KLS-D-fd638ddcf5`. It is not a failed check and is not evidence for this build.

### Changes and evidence

- `KLS_AwardBounty` now shows each active defender the exact personal gold share that was credited. Boss participation gold also shows a separate per-player amount. The UI message is presentation only; payout math remains synchronized.
- Installed `ItemData.slk` labels `idro` as `droppable` and `ipaw` as `Can Be Sold To Merchants`. Catalog gear changed from `idro=0` to `idro=1`; `ipaw=1` and `isel=1` remain. Boss relics became movable (`idro=1`) but stay unpawnable (`ipaw=0`, `isel=0`). Actual drag/equipment/sale behavior remains unverified in the engine.
- The Restoring Spring now ticks once per second, restoring 1% of maximum HP and mana, capped at each maximum. Its effect only emits while at least one resource is missing.
- Regression tests were added first and failed on the prior source (missing reward toast, droppable gear flags, and one-second percentage regeneration). After the source changes, the focused regressions passed.
- Full suite: **63/63 passed**. Build reports installed-editor JASS syntax and MPQ package/readback passed for this build.
- `build_map.py --install-test-map` could not install this build because Warcraft III PID 46920 held `KLS-D-f89f212a3a-Development.w3m` open. The installer preserved both prior map files. A byte-identical copy of `KLS-D-f89f212a3a-Development.w3m` exists under `backups/installed-diagnostics/20260928T102120988478Z-KLS-D-dddc30394a/`; both copies hash to `06ee04a3fb1cf5af35d27e0059d0b3cd33522ce93acc30f9914219188fa6f787`. No new build was copied into the live Warcraft III test folder.

### Exact next action and remaining checks

- After the user finishes and closes Warcraft III, rerun `python -B tools/build_map.py --install-test-map` from this repository. It should install `KLS-D-dddc30394a-Development.w3m` and archive prior project maps without overwriting them.
- Then run one focused in-game check on this exact build: kill one basic enemy and verify the visible gold toast matches the gold increase. Next, verify moving one purchased gear item into normal inventory and selling an ordinary item back; test the spring's HP/mana tick afterward. Record each result against this build ID.
- Keep editor round-trip/current-build Test Map, all gameplay, 2/3/4-player sessions, and 40-wave endurance pending until tested. Keep the map labelled development.

## 2026-09-28: verified campaign roster and hero-army expansion draft — prior build KLS-D-dddc30394a

### Evidence gathered

- At this research point, the development artifact was `dist/KLS-D-dddc30394a-Development.w3m`, SHA-256 `d646a4a3de78b4e8cbeb1bed6ab5121344565227547dcca7c60c6255ee2d05ab`.
- `UnitData.slk`, `UnitUI.slk`, `UnitAbilities.slk`, `UnitBalance.slk`, `AbilityData.slk`, and `WorldEditStrings.txt` from the installed Definitive Edition identify Human Ilastar (`Hjsm`), Undead Ilastar (`Ujsm`), and Forsaken Paladin (`Npal`), with ability IDs recorded in `docs/HERO-THEMED-EXPANSION.md`. The unit ability table gives Human Ilastar and the Forsaken Paladin hero skills; Undead Ilastar has no global hero-skill list.
- The screenshot name Aurrrius the Pure was not found in the installed global tables searched; the campaign-map object may be separate. No rawcode was invented and no campaign map was deprotected.
- The installed unit data names `hpea` as `peasant` and `uaco` as `acolyte`, with distinct ability lists. The starting-worker path creates `hpea`; this confirms the source and installed records but does not resolve the in-game Acolyte portrait. The diagnostic `-diag` output now includes the runtime player race and actual first-worker object/unit name so the next current-build capture can distinguish a wrong unit from a UI/group-selection issue.

### Current task and exact next action

- Current task: continue the complete approved gameplay plan, with the hero-themed army/building expansion as the next major design slice.
- Draft: `docs/HERO-THEMED-EXPANSION.md` proposes three campaign hero additions and the Oathbound Companies system. No code or map changes have been made for this new architecture pending user review.
- The installation still has Warcraft III PID 46920 holding the older installed map; the current build cannot be installed while it remains open. Source work and data research continue independently.
- Next independent action: after the user approves or redirects the expansion architecture, implement the hero/building/unit catalogs in phased, build-ID-tagged changes. The current-build live checklist remains pending separately.

## 2026-09-28: unit-data provenance and worker identity diagnostics — KLS-D-3a0464e019

### Current task and last package-proven build

- Current task: continue the approved game plan; extend installed metadata for the Forsaken Kingdom hero expansion and expose runtime evidence for the reported Peasant/Acolyte portrait mismatch.
- Current development build: **KLS-D-3a0464e019**.
- Workspace artifact: `dist/KLS-D-3a0464e019-Development.w3m`.
- SHA-256: `c0bb8275469ffb3a2165930fd7ccd62ca6716bc8203a6fc5cc366d5d732365be`.
- The per-build record is in `CHANGELOG.md`; the manifest and output hash match.

### Changes and evidence

- The local-only API extractor and build provenance now include installed `UnitBalance.slk`, `UnitUI.slk`, `UnitAbilities.slk`, and `UnitWeapons.slk`. These source tables remain git-ignored and are regenerated from the installed game.
- Runtime `-diag` prints each active player's actual runtime race and the object/unit name of that player's first spawned worker. The source still creates `hpea` workers.
- Installed unit records show `hpea` named `peasant`, with abilities `Ahar,Amil,Ahrp,Ahlh`; `uaco` is named `acolyte`, with abilities `Aaha,Arst,Alam,Auns`. This proves the base definitions differ but does not prove what the live screenshot selected or displayed.
- Installed data identifies `Hjsm` Human Ilastar with hero skills `AHas,AHsf,AHmc,AHsl`, `Npal` Forsaken Paladin with `AHcr,ANcp,AHpa,AHcl`, and `Ujsm` Undead Ilastar with no global hero-skill list. `Aurrrius the Pure` was not found in the searched global tables.
- Full regression suite: **65/65 passed**. Installed-editor JASS syntax and 23-member MPQ inventory/readback passed. Editor/game, current-build startup, and live worker portrait checks remain pending.
- The user-provided earlier Test Map pass remains on `KLS-D-fd638ddcf5`; this build has not yet been tried.
- Warcraft III PID 46920 continues to hold the older installed map. No current build was installed; the prior map was preserved and the current map remains the single artifact in `dist/`.

### Exact next actions

1. After Warcraft III closes, run `python -B tools/build_map.py --install-test-map` to replace the one test-folder copy while archiving the older map.
2. Open the installed `KLS-D-3a0464e019-Development.w3m`, run `-diag`, and capture the worker race/object identity lines. Confirm whether the selected worker portrait is Peasant or Acolyte.
3. Ask the user to approve or redirect `docs/HERO-THEMED-EXPANSION.md` before implementing that new architecture; continue the already approved 40-wave/building/equipment/gameplay work independently.
