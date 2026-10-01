# Racial construction and recruitment DEVELOPMENT handoff — 2026-10-02

This is a staged implementation. Standard construction rosters, company reconciliation and eight specialists are packaged; expansion switching has **not passed native acceptance** and remains disabled in the regular handoff. Consequently, new expansion facilities cannot yet be constructed from regular workers in that handoff. The separate prototype grants the page button for the required engine test. MCP inspection does not establish gameplay acceptance.

## Immutable artifacts

| Artifact | Build | SHA256 |
|---|---|---|
| KLS-Racial-Repairs-Native-Gate-Pending-R3-20261002.w3m | KLS-D-1f003ecdb7 | 2793d5d6f815709d46953568743864ccbf09b8ea55f3915206322158ca7b5c14 |
| KLS-Racial-Worker-Prototype-R5-20261002.w3m | KLS-D-5ec0710adf | a1aeeb10bb9352a940adc9369b954c58caafd36625e89ebbafb83db2d2ad2856 |

Both start from saved Hero-Market-Repairs-R2 (`4048e415d03d920b2c258b4e78fbaa46d5153a13b4d3927bea425aa524bfc4ea`), archived with its contents. Earlier racial prototypes and gate-pending revisions are superseded local intermediates; do not use them for acceptance. Neither map is automatically installed.

## Packaged repairs

- Restore native standard rosters with at most eleven buildings plus Cancel, explicit positions, native production definitions and preserved town-hall/tower upgrade chains. Custom altars satisfy native prerequisite references and retain the single-hero rule. Correct the Undead tier-two Graveyard prerequisite. The [building access matrix](BUILDING-ACCESS-20261002.md) records before/after access, requirements, upgrades, recruits, research, harvesting and positions.
- Reserve four expansion workers and Chaos conversions using installed native parent `Sca5`; switch by adding/removing Chaos on the original handle. Restore health/mana explicitly. Capture issued work orders immediately, disable switching while busy/loaded and reject a callback retaining a prior work order. Native cargo, abilities, ownership, food and handle preservation remain unverified.
- Reconcile the existing 50 hero-company products against completed, owned facilities; validate product/owner/prerequisites at purchase, refresh preplaced/rebuilt buildings and stock both completion orders. Preserve prices/powers and permanent Foundry participation. Register native training completion separately from instant company purchases.
- Banner Halls train defenders and support yards train supports through native queues and rally. Company services remain at (3,0); specialist training uses (0,0). Foundries retain research/recipes. Native stock/research/rally layout needs visual engine acceptance.
- Mirror changes in shared faction/specialist catalogs, source generators and runtime/editor trigger headers. Apply separate Forge undo groups for each race, recruitment, worker definitions and specialist units/powers. Typed main/skin records retain version-three headers; reserved IDs are checked against both baseline tables.

## Specialists

| Race | Defender | Support |
|---|---|---|
| Human | Royal Bulwark: +4 armor, 8 seconds | Field Engineer: allied non-King structure repair, 300 HP/5 seconds |
| Orc | Spiritguard: 60 damage, 20% slow/3 seconds | Storm Drummer: +15% attack speed/6 seconds |
| Night Elf | Thorn Sentinel: root 3 seconds; boss/hero 1 second | Moonwell Tender: 150 HP/30 mana; excludes King/buildings |
| Undead | Bone Warden: absorb 250 damage/8 seconds | Plague Artificer: 25 damage/second for 4 seconds, -3 armor |

Defenders cost 300 gold/100 lumber, 3 food, 25-second training, 900 HP and 28 base damage. Supports cost 350/125, 3 food, 30-second training, 650 HP and 18 base damage. All have 180 mana/1 regeneration; powers cost 40 mana with 20-second cooldown, radius 250 and cast range 600 where applicable. Parent racial models, attack and movement types remain. Bone Warden uses Skeleton Warrior `uske`, not the archer. Roots use both native air/ground Ensnare buff variants.

Timed buffs refresh without stacking and restore only their applied stat changes. Death, removal and ownership changes expire effects; shield damage callbacks independently reject changed caster ownership. Chapter potency applies to active powers and support research adds support potency. Company upgrades use existing idempotent upgrade bookkeeping.

## Hero and preservation evidence

Reopened MCP readback covers all 25 heroes, 137 unit definitions and 148 abilities including company and specialist powers. Existing hero main/skin kits and all 90 distinct learnable/signature records remain baseline-identical; their rank, targeting, descriptions, order IDs and requirements are in the readback attachment. No alternate signature-delivery mechanism replaces the R2 targeted healing repair. Automated king-healing checks now cover every healing signature, low/high hero levels, injured/full/dead king cases.

Read-only archive comparison preserves terrain, pathing, units, doodads, shops, encounters, player plots, economy, item tables and unrelated runtime. 198 existing runtime function bodies remain identical apart from the build identifier; 51 subsystem functions match editable trigger source. All baseline object fields outside the selected changes are preserved. Native-format round trips passed for metadata v39, units v13 (151) and doodads v13 (1,870), byte-identically. JASS compiles against the installed API (25,257 lines including API files).

Final full suite: **243 tests, 241 passed, two pre-existing failures**. Both remain visible:

1. AK21 source-generator native-parent expectation disagrees with the older test. The saved R2 scripted signature object/runtime is preserved here.
2. A Human sanctuary tower tooltip omits the word “Human.”

Regression tests execute the actual JASS handlers for timed repair, armor/slow/haste/plague refresh/expiry, shield absorption, ownership transfer, removed-unit cleanup and the issued-order/channel switching race. This is not engine proof.

**Known unresolved gameplay issue:** native sale popup can display 1,200 while actual credited gold is 12,000. Verified payment remains unchanged; no extra compensation is added. Inventory, tome, healing and loot repairs are preserved, but native acceptance of those earlier repairs remains pending.

## Required native acceptance

Observed native failure: the user tested Undead in Prototype R2 and V did not switch pages. That revision used an incorrect Chaos parent. R5 uses installed `Sca5`; its native result remains pending. The production gate remains closed and no working switching claim is made.

Use **Prototype R5**, not an earlier prototype. For each race, select an idle worker and use V to open expansion construction, then return to standard construction. Record build ID and debug original/current handle, worker type, owner, health, mana, food, abilities and carried resources before/after. V must be unavailable/rejected during harvesting, repair, construction and loaded transport activity. Test native construction targeting, hotkeys, Cancel/Back and every button. Do not enable production switching until all four races pass. A failure stops this subsystem for correction; do not replace it with a different menu design.

Then test every standard prerequisite path, training/research/town upgrades and racial gold/lumber collection/drop-off. Test both facility completion orders, prerequisites, destruction/rebuilding, queue cancellation/refunds, food limits, native rally, ownership changes and simultaneous purchases/training by different players. Test all eight powers, refresh/expiry, boss root limits, company/research upgrades and cleanup on death/removal/ownership changes. Recheck all 25 heroes and supported ranks 1–10, native caps, skill points, +3 attributes, talents, level cap 50 and every king-healing signature. Multiplayer synchronization, native inventories, sale text, tome repetition and duplicate death callbacks remain required.

No native engine control is available in this session. These checks are **pending**, not passed. A future accepted build must archive this exact result, enable the gate deliberately, repeat affected checks and publish another immutable handoff.

## Publication

R2 was published first as [a DEVELOPMENT prerelease](https://github.com/prebenjor/TheKingsLastStand/releases/tag/dev-20261001-hero-market-r2). This handoff is published as [the racial repairs prerelease](https://github.com/prebenjor/TheKingsLastStand/releases/tag/dev-20261002-racial-repairs), including both maps, SHA/preservation manifests, readback and this report. Source/README changes are on the repair branch with a pull request; updating shared main requires merge approval following automatic review rejection of the direct main push. Authentication works outside the restricted shell. No credentials, installed Blizzard tables, caches or map binaries are committed to source history.
