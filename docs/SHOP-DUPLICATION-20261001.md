# Shop duplication report — 2026-10-01

Current 2026-10-01 policy and packaged evidence: safely scalable skills now allow ten ranks; unsupported mechanics keep native caps. Original-handle purchase retries, king healing, tome stock and consumable changes are in the R2 DEVELOPMENT handoff. Native sale popup and engine testing remain open. See [Hero/market repair report](HERO-MARKET-REPAIRS-20261001.md); this supersedes older five-rank or source-only repair status below.

User reports duplicate purchases in multiplayer. Screenshots additionally report a sale displaying 1,200 but crediting 12,000, and question escalating +5/+10 tome prices. The specific sold item and potion behaviour are not yet identified.

Source candidate repair: removed `KLS_MovePurchaseToRegularInventory`, which called `UnitAddItemToSlotById` to create a replacement for a native backpack purchase. Its failure branch could restore the original after creating an untracked replacement, and retries could revisit items already equipped. Auto-equip now retains the purchased handle, accepts already-equipped state without another operation, and cancels when ownership or regular/bag possession no longer matches. No purchase retry creates an item. This removes a demonstrated unsafe source path; it does not prove the reported engine symptom is resolved or explain duplication of consumables if that is also occurring.

Generated source candidate `build/layout-review/purchase-original-handle.j` compiled with installed common.j/blizzard.j and PJASS (7,951 generated lines). Existing regression assertions were updated to the new contract, but no tests were run in this turn. Live equipment/backpack, repeated purchases, full inventory, two-player and crafting checks remain pending.

The candidate is source-only. Neither the installed gameplay package nor the Forge editing map contains this repair. A full rebuild remains pending the authored-placement integration described in AUTHORED-LAYOUT-INTEGRATION-REVIEW.md; do not lose the user's edits to deploy this fix.

Sale payout is currently native, with no custom gold award in `KLS_GearPawned`. Do not add a second payout to compensate for a tooltip mismatch. Tome catalog prices currently deliberately escalate: +5 = 1,000; +10 = 3,000; +20 = 8,000. No pricing changes were made without identifying the discrepancy.
