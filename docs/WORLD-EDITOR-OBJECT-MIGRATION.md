# Standard World Editor object migration — 2026-10-01

The user superseded Forge editing: use the latest standard World Editor layout. Confirmed saved and closed input is `build/KLS-D-68303d69bf-Development-Terrain.w3m`.

Immutable archive: `backups/editor-handoff/20261001-8813c8955931/KLS-D-68303d69bf-Development-Terrain.w3m`.
SHA-256: `8813c8955931e8cacb695e4ec9bdb46504884810d8031bfe8118f6f5313a3dfc`.

## Source candidate prepared

- All eight new hero objects list their signature in normal abilities, retaining their installed parent's normal ability list. The runtime no longer adds signatures to these eight; the seventeen older choices retain their existing assignment path.
- User approved native single-wave impact timing for Selyra. AK21 now derives from ANrf, with one wave, 350 radius, 700 range, 70 mana and 30 seconds cooldown. Native base damage is 300, with no lingering burn. Its live damage retains +20 per hero level through a small synchronized ability-field update using the Object Editor base value. It remains one signature rank, not fifty learnable ranks.
- AK21 exits the scripted signature handler before damage, healing, summons or visual callbacks. This avoids two damage implementations firing together.
- Native impact art currently inherits Rain of Fire; matching moonfire art requires editor review. Native targeting, damage-field updates and duration need Warcraft validation. Do not claim identical instantaneous impact or complete native migration of mixed-effect signatures.

Generated native definitions inspected; Selyra retains `Ashm,AInv,Ault,AK21`. Candidate JASS compiled with PJASS (8,018 generated lines). No tests were run. No new gameplay package was generated or installed; these changes are not in the user's saved map yet.

## Unresolved blockers and next work

Computer Use initialization failed again with `failed to write kernel assets: The system cannot find the path specified. (os error 3)`. No standard World Editor controls were operated. File generation remains possible, but cannot substitute for engine/editor acceptance.

The user's unknown AbilityData database-column warnings remain unresolved. Extracted installed AbilityData includes the reported columns, so an outdated editor/version conclusion is not established. Compare native ability/skin records, editor-load database provenance and actual editor reopen before choosing a correction. Do not suppress the warning with speculative imported global tables.

Review and reconcile all new saved layout/object/trigger changes before a full rebuild. Preserve new placements and the removed Orc town; do not install a build which restores procedural gates or loses authored units. The new saved layout supersedes the earlier Forge market suggestion. Do not automatically reapply the square over the user's latest layout.

Continue with editor-native research/menu/tome/healing candidates only where gameplay contracts can be preserved. Ownership, transactions, quests and multiplayer UI logic still require editable triggers. Purchase original-handle source repair remains pending packaging and live checks; backpack and rank warnings remain open.


## Forge MCP assignment pass — 2026-10-01

The user reauthorized Forge MCP against the newest standard World Editor save. All 25 selected heroes now explicitly list AK00–AK24 in Object Editor normal abilities, preserving each current normal ability list. The four learnable skills are unchanged. Matching source generation covers all 25 and no longer adds signatures during hero selection.

Final editing copy: `build/KLS-D-68303d69bf-WorldEditor-20261001-HeroObjects-Preserved.w3m`.
SHA-256: `261da9078b64ee617c292c24a203323a823123763be5220315a6e86b1805c610`.
Input remains `8813c8955931e8cacb695e4ec9bdb46504884810d8031bfe8118f6f5313a3dfc`.

Archive inspection found only war3map.w3u changed: 25 added uabi fields and two required original-object base records (Hjsm/Npal). All other content members, including unit/doodad placements, terrain, items, abilities, skins, triggers and JASS, are byte-identical. Report: `build/forge-session/20261001-hero-objects-preservation.json`.

Initial Forge export rewrote integral real fields as integers. That export (`HeroObjects-Assigned.w3m`, SHA 50151c597d7286e29ca6a2a17eeb48d81930f07cc09b55a03067c866684884cf) is superseded and must not be used. Repaired the Forge parser/writer to retain authored flat and leveled wire types, compiled wc3-forge-types-fixed.exe, selected its MCP session, and repeated edits from untouched input. Supplemental source patch: tools/wc3-forge/object-wire-types.patch. New numeric fields without original type information still require metadata-aware encoding review.

The final map retains existing scripted signature effects and runtime code. It does not contain the native Selyra conversion or purchase repair. Those source candidates must be packaged with matching runtime changes after latest layout integration. Generated all-hero definitions were inspected and candidate JASS compiled with PJASS; no gameplay tests were run. Computer Use initialization remains unavailable. Next human check: open the final editing copy in standard World Editor and inspect hero Normal Abilities alongside unchanged Hero Abilities, then report any load warnings. Development status remains.
