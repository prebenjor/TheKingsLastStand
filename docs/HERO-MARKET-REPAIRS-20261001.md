# Hero and market DEVELOPMENT handoff — 2026-10-01

Continue with `build/KLS-D-68303d69bf-Hero-Market-Repairs-R2-20261001.w3m`.
SHA256: `4048e415d03d920b2c258b4e78fbaa46d5153a13b4d3927bea425aa524bfc4ea`.
This is an editor development revision, not an installed or gameplay-verified release.

## Implemented

- MCP audited and read back all 25 heroes and 90 unique abilities after reopening the final archive. Normal and skin ability lists agree, with four learnable skills and one signature per hero.
- Safely scalable skills reach ten ranks. Extra ranks add 10% of the final authored power per rank; authored power remains intact. Costs, cooldowns, duration and range retain their authored values. Unsupported mechanics retain native caps. Percentage limits are bounded. Manual skill spending, attributes, talents and level cap 50 remain.
- Healing signatures explicitly accept living allied King Aldric, clamp healing, and exclude structures and unrelated neutrals. King mana behavior remains unchanged.
- Purchased gear retries retain the original item handle, stop on completed equip or ownership loss, and never create replacement items. Saved JASS and editable trigger header contain the repair; the obsolete replacement helper was removed.
- Sage tomes have 99 stock and immediate refill, unchanged prices and instant attributes. Paid castle healing has a shared one-second cooldown, unchanged 2,000 healing and 150 gold/50 lumber cost, with refunds for refused prepaid purchases.
- Consumable rolls use 1% normal, 2% elite and 5% boss. Duplicate wave death callbacks process loot once. Guaranteed forest rewards, equipment rules and existing ground items are preserved.
- Briar summons use collision-free `bT06`–`bT10`; the existing `kT10` faction tower is preserved. Main and skin tooltips are synchronized.

## Preservation and workflow

Baseline: `KLS-D-68303d69bf-Castle-Countryside-Final-R4-20261001.w3m`, SHA256 `8d04cabf92ef4ddf68559a66636f80d6603645d08804c13528cc60d7bfe822d6`. Full baseline archive is retained under `build/backups/hero-market/20261001-8d04cabf92ef/`.

Supported `tools/build_map.py` prepare, refresh, apply, audit and package hero-market modes preserve baseline archive members and mirror source changes. The deterministic working catalog and MCP evidence are in `build/forge-session/20261001-hero-market-repairs/`. Only JASS, WCT and six main/skin unit/item/ability tables change. Other members, including countryside terrain, pathing, unit/doodad placements and vendor layout, are byte-identical. Adjacent final-map JSON records compilation and preservation evidence.

The candidate and initial unsuffixed Hero-Market-Repairs maps are superseded. The initial archive failed Forge reopening because new version-two object records lacked the version-three set header. R2 corrects that header and successfully reopens. Never use the superseded archives.

## Verification

- PJASS passes with installed common.j and blizzard.j: 8,913 map lines.
- Full suite: 232 tests, 230 passing, two existing failures: AK21 source-candidate native-base expectation and Human building race wording. The additional native-format regression subsequently passes with all nine targeted repair tests.
- Targeted harnesses execute JASS handlers for king target/health states, shared healing cooldown/payment/refunds, original-handle equip retries across inventory states, and repeated wave death callbacks. These are controlled harness checks, not native engine gameplay proof.
- Forge reopens R2 and MCP reads all 25 heroes and 90 abilities. Native format checks round-trip metadata and all 151 units and 1,870 doodads byte-identically. Extracted evidence is `build/hero-market-native-roundtrip-20261001/`.
- Extracted final payloads equal all six expected object tables; all 25 main/skin kits match. Every targeted JASS function matches its editable WCT counterpart. Deferred equipment contains no replacement creation, the obsolete helper is absent, and pawn diagnostics award no resources.
- Reviewer independently verified original ability effect fields at ranks 1–3 against the baseline and found no further important issue.

## Open checks

The native sale popup showing 1,200 despite a verified 12,000 credit is **unresolved**. Native payment is preserved, with no compensation. Sale diagnostics identify the item and print the full current gold balance; they do not claim to replace the native popup amount. A reproducible item name and purchase price are requested before determining the correct display fix.

Native gameplay checks for every hero, ranks 5–10, shops, tome purchases, crafting, simultaneous multiplayer transactions, full backpack/equipment transitions, sale deltas, and service timing remain pending. Native UI control is unavailable here; MCP inspection is not gameplay proof. The supplied construction command-card screenshot has not received a separate worker-menu audit. AK21's existing Channel/script delivery is preserved in this targeted map; the separate source native-ability candidate remains subject to its existing test failure.
