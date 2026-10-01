# Countryside execution ledger — 1 October 2026

Approved plan: castle countryside, shop placement, and selection fixes.

Baseline archived: c7d91e762808683fae708105b1d0fdda5cf21291cd4bcdc61e93b3a2db892929. Original map remains untouched.

Ruling: preserve the existing in-place source changes; a fresh checkout would omit the prior uncommitted map integration. Terrain mutations use a dedicated extracted copy. No commits or installs are requested.

Task 1: native group regression failed for new units, start locations and doodads at group 0; sentinel defaults changed to 0xffffffff; regression passed.

Task 2: native group repair and identity-based market import regressions failed before implementation, then both passed.

Completed: deterministic countryside catalog, separate MCP undo groups for west/east terrain, ponds/hills and props, and targeted runtime/header packaging. Review identified floating land props and unsafe partial checkpoint replay; both were corrected and covered by regressions. Further verification corrected DE water/ramp flags, lookout approaches and a pond-shore bypass, and moved only new trees away from route/plot edges.

Final handoff: KLS-D-68303d69bf-Castle-Countryside-Final-R4-20261001.w3m, SHA256 8d04cabf92ef4ddf68559a66636f80d6603645d08804c13528cc60d7bfe822d6. Original 151 units and 1,749 doodads preserved except 13 intended unit group fields; 121 doodads added. Preservation checks passed with zero protected terrain changes and 2,193 walkable trail samples. PJASS and byte-identical native roundtrips passed. Python: 222/224 passed, two pre-existing failures. Forge: five packages passed. Native selection and gameplay checks remain pending. See CASTLE-COUNTRYSIDE-20261001.md for handoff instructions and evidence.
