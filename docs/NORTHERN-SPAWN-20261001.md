# Northern invasion site — 1 October 2026

Resumed the interrupted Find and adapt a Warcraft 3 RPG map request. The latest saved northern-origin Forge folder contains the user's layout plus the previously saved gate/forecourt work. The original Terrain and working archives remain preserved.

## Editing artifact

`build/KLS-D-68303d69bf-Northern-Spawn-Final-20261001.w3m`

SHA-256: `a3fb2bd5c4d36e234c66823f680bd11f08439a0cd85f9513e8174aed61b4b491`.

This is an immutable DEVELOPMENT editor handoff based on KLS-D-68303d69bf. The dedicated gameplay package, installed copy and dist manifest are unchanged. Do not confuse its new SHA with the old gameplay package. Opened successfully through Forge MCP with 139 placed units. Companion `.json` records compiler output and the exact updated functions.

## Behavior and preservation

- Northern Summoning Gate `kInv`, based on the installed Demon Gate model, at `(0,7680)`, owned by Player 12 (zero-based 11), faces south and has native `Avul`, no attacks and no training queue. Runtime also explicitly makes it invulnerable.
- Preserved the saved dirt/stone forecourt, side braziers and sparse ruins. Regular waves emerge 1,400 units south of the gate in a seven-column formation; bosses emerge 760 units south. Moving the gate in the editor moves both wave origins. A checked generated-map fallback creates one gate only when none is placed.
- Removed the retired northern settlement's runtime structures. Crown Ritual Warden and racial vendors remain accessible in the kingdom; four playable racial identities remain. The northern ritual now occurs beside the gate. Only actual surviving halls receive restoration refuges and garrisons.
- Removed runtime `LTg1`/`BTsk` barriers so they cannot reappear over the user's cliffs. Existing resource-tree behavior remains.
- The targeted runtime refresh changes `war3map.j` and the custom-script header in `war3map.wct`; every other map content member matches the saved Forge folder/staged native baseline byte-for-byte. Archive CRC attributes are regenerated. Native `main`, preplaced-unit creation, trigger table, terrain, doodads, units, object data and unrelated runtime functions remain preserved.
- The existing native signature and purchase candidates were not imported into this editing copy. No full authored-map capture or new installed gameplay package is claimed.

## Verification

- Installed-API PJASS passed: 8,784 map-script lines, 24,611 lines including native declarations.
- Content-member preservation/readback passed; final SHA rechecked; Forge MCP reopened the exact artifact and confirmed gate placement.
- Six northern-origin regressions pass: surviving settlement placements, restoration/garrison boundary, no recreated barriers, gate-relative wave origins/invulnerability, helper order/native-code preservation, duplicate-function rejection.
- Full suite: 211 tests, 209 passed, 2 failures. Remaining failures concern the earlier `ANrf` native signature candidate versus an `ANcl` expectation, and a Human tower tooltip that lacks the race word. Neither concerns this handoff. Log: `build/northern-continuation-tests-verified.log`.
- Static WPM footprint check: all 57 sampled regular/boss spawn positions are walkable in the saved 768×768 pathing grid. This does not prove native building collision, cliffs/doodad navigation or multiplayer behavior.

## Next human-run check

Open this exact copy in standard World Editor, save/reopen a new copy and run Test Map. Confirm the northern gate cannot take damage and one regular wave plus a boss wave can reach King Aldric through the authored cliff passage. Report the artifact name/SHA with any problem. Editor round-trip, gameplay, multiplayer and endurance remain pending.
