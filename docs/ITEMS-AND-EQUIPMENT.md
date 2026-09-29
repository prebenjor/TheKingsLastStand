# Items, equipment, backpack, crafting, and shops

The generated catalog and item rawcodes are documented in ITEM-CATALOG.md. tools/equipment_catalog.py is the implementation source of truth; update the catalog document whenever generator data changes.

## Forsaken Kingdom native backpack

The target is the backpack/equipment presentation used by the Forsaken Kingdom campaign:

- Thirty storage slots.
- Nine equipment slots: head, chest, gloves, boots, ring 1, ring 2, main hand, off hand, and trinket.
- Normal six-slot hero inventory, with one space reserved for the persistent backpack item.
- Native backpack/equipment UI and installed editor/game APIs, not a replacement 18-slot dialog.
- All 25 hero types may use the same equipment. Race-themed items remain universally equippable; descriptions can recommend a role but must not enforce class or level restrictions. The 20-item race catalog and four Legendary Foundry recipes are detailed in [CROWNLANDS-EXPANSION.md](CROWNLANDS-EXPANSION.md).
- Ordinary catalog gear is native-droppable and pawnable so the player can move it through the backpack, normal inventory, and equipment slots, and sell it to vendors for half its listed price. Boss relics are also movable/equippable, but remain unpawnable.

Buying an item must deliver it in a location from which the same native inventory service can equip it. Storage, equip, unequip, ownership, stat changes, sell, and crafting must be atomic. Never remove an old item or consume a recipe part until delivery and final state are guaranteed.

Backpacks cannot be dropped, sold, duplicated, or lost on hero death. Equipment and storage survive death/revival. Purchased items and boss drops are personal. A full backpack must create a pending personal entitlement or retrievable owner-bound delivery; it must not discard the reward.

This UI is a high-priority live acceptance area. The player has reported bought items, including boots, cannot be equipped and the backpack does not open like the campaign version. API syntax and object data alone do not resolve that report.

## Vendor layout and prices

All qualities are available immediately; gold gates affordability rather than shop unlocks. The base equipment prices are Common 300, Uncommon 1,000, Rare 3,000, Epic 8,000 and Legendary 20,000 gold. The three hand-weapon families Blade/Bow/Staff cost 1.5 times base; other families cost base. The three original Foundry recipe fees are 5,000/7,000/12,000 gold; each racial Legendary Foundry recipe costs 9,000. Tome prices are 1,000/3,000/8,000. The catalog is authoritative for individual item costs.

| Vendor quality | Shop name | Base equipment price |
|---|---|---:|
| Common | Quartermaster | 300 gold |
| Uncommon | Veteran Armorer | 1,000 gold |
| Rare | Rare Arms & Armor / Rare Apparel & Relics | 3,000 gold |
| Epic | Runic Reliquary | 8,000 gold |
| Legendary | Royal Vault | 20,000 gold |
| Recipes | Master Forge and built racial Foundries | Three original recipes at Master Forge; one race-matched Legendary pattern in each player's Foundry |
| Consumables | Field Apothecary | Existing Warcraft consumable prices |
| Attribute books | Sage's Archive | 1,000 / 3,000 / 8,000 gold by tome size |

Display item rarity with Warcraft color codes in item names, shop stock names, and tooltip headers: Common white (`#FFFFFF`), Uncommon green (`#1EFF00`), Rare blue (`#0070DD`), Epic purple (`#A335EE`), and Legendary gold (`#FF8000`). Boss relics use Rare for Gravetide Cleaver, Epic for Heart of the Watch and Crown of Dawn, and Legendary for Oath of the Last King. Keep the raw quality label and full stats in the tooltip so color is supplementary.

The five quality levels are implemented as two neutral units per level: Arms & Armor and Apparel & Relics. Generic vendors contain only the sixteen general equipment families, keeping each quality shop at seven Arms & Armor items and nine Apparel & Relics items. Matching Crownlands town shops sell their race's four Common-through-Epic relics plus health and mana potions. The racial Legendary relic is not directly stocked; its Foundry pattern crafts it from two racial components, and it remains eligible for the existing enemy-drop rules. The Master Forge in the southern market stocks three general recipe patterns. Each constructed race Foundry sells one copy of its own racial Legendary pattern to its owner. Recipe stock returns to the original vendor after successful or failed crafting; if the vendor was destroyed during crafting, stock returns to the Master Forge. The Field Apothecary has four consumables, and Sage's Archive has nine tomes. Keep every vendor at twelve or fewer stock entries so all items fit the native command card. Present the market vendors as recognizable buildings around the southern plaza, with the Archive beside the Apothecary. Shop windows must display icon buttons and stat-rich item tooltips, not a text-only list or an empty inventory.

## Equipment families, stats, and scaling

The current generated catalog has sixteen families × five qualities = eighty ordinary equipment items, plus three crafted legendary variants. Stats use multipliers Common 1, Uncommon 2, Rare 4, Epic 7, Legendary 11. Prices are tier base price, except Blade/Bow/Staff at 1.5×.

| Family | Common baseline | Native slot | Special effect family |
|---|---:|---|---|
| Blade | +6 damage | Main hand | Rare+: cleave |
| Bow | +6 damage | Main hand | Rare+: bleed |
| Staff | +3 intelligence | Main hand | Rare+: frost burst |
| Shield | +2 armor | Off hand | Rare+: single-hit absorption |
| Focus | +75 mana | Off hand | Rare+: mana return on cast |
| Helmet | +60 health | Head | Attributes/defense from item stats |
| Chest | +100 health | Chest | Attributes/defense from item stats |
| Gloves | +5% attack speed | Gloves | Attributes/defense from item stats |
| Boots | +10 movement speed | Boots | Attributes/defense from item stats |
| Offensive Ring | +3 damage | Ring | Two ring slots can coexist |
| Defensive Ring | +1 armor | Ring | Two ring slots can coexist |
| Trinket | +50 health, +50 mana | Trinket | Rare+: nearby allied hero healing |
| Cape | +50 health, +1 armor | Chest | Rare+: spell damage reduction |
| Might Chestplate | +2 Strength | Chest | Attribute specialization |
| Windrunner Boots | +2 Agility | Boots | Attribute specialization |
| Arcanist Focus | +2 Intelligence | Off hand | Attribute specialization |

Rare, Epic, and Legendary named procs:

| Family | Rare | Epic | Legendary | Cooldown/radius |
|---|---|---|---|---|
| Blade | 15% cleave | 25% | 35% | Secondary targets within 250 |
| Bow | 30 bleed damage over 3 s | 60 | 100 | 5 s cooldown |
| Staff | 40 burst damage | 80 | 140 | 250 radius; 20% slow for 2 s; 8 s cooldown |
| Shield | Absorb up to 40 damage | 80 | 140 | One incoming hit; 8 s cooldown |
| Focus | Restore 15 mana after a spell | 30 | 50 | 8 s cooldown |
| Trinket | Heal 40 | 80 | 140 | Every 10 s; owner and allied heroes within 400 |
| Cape | Reduce incoming spell damage by 5% | 10% | 15% | While equipped |

The strongest equipped copy of an identically named proc wins. Effects may not trigger themselves. Equipment swaps do not reset effect cooldowns. Normal equipment sells for 50% of its listed value. Boss relics are meant to be unsellable.

## Attribute books

Sage's Archive sells nine personal, permanent tomes. They apply immediately to the buyer's selected living hero; missing hero or failed purchase refunds the fee.

| Book | Rawcode | Bonus | Cost |
|---|---|---:|---:|
| Tome of Strength +5 | KS05 | +5 Strength | 1,000 |
| Tome of Strength +10 | KS10 | +10 Strength | 3,000 |
| Tome of Strength +20 | KS20 | +20 Strength | 8,000 |
| Tome of Agility +5 | KA05 | +5 Agility | 1,000 |
| Tome of Agility +10 | KA10 | +10 Agility | 3,000 |
| Tome of Agility +20 | KA20 | +20 Agility | 8,000 |
| Tome of Intelligence +5 | KI05 | +5 Intelligence | 1,000 |
| Tome of Intelligence +10 | KI10 | +10 Intelligence | 3,000 |
| Tome of Intelligence +20 | KI20 | +20 Intelligence | 8,000 |

## Recipes

The recipe scroll and fee are personal. Ingredients may be equipped or stored anywhere in the buyer's own native hero inventory/backpack. Validate both exact ingredients, ownership, alive buyer, and output space. Only then debit/consume and deliver. Any failure restores the fee and every item unchanged.

| Result | Ingredients | Fee | Result details |
|---|---|---:|---|
| Oathforged Kingswrath | Rare Gravebreaker + Rare Ring of Conquest | 5,000 | Legendary blade, +88 damage, +10 Strength, 35% cleave |
| Stormheart Prism | Rare Wintercall + Rare Spellwell | 7,000 | Legendary focus, +22 Intelligence, +550 mana, restores 50 mana per spell proc |
| Sovereign's Mantle | Epic Dawnguard Helm + Epic Royal Bulwark | 12,000 | Legendary chest/cape, +10 of each primary attribute, +800 HP, +10 armor, 15% spell damage reduction |

## Boss relics and completion rewards

Design intent: four distinct personal, unsellable relics are awarded by the four chapter bosses. Current object data defines:

| Wave | Name | Rawcode | Slot | Current tooltip |
|---|---|---|---|---|
| 10 | Gravetide Cleaver | I010 | Main hand | +15 damage |
| 20 | Heart of the Watch | I011 | Chest | Increases maximum health |
| 30 | Crown of Dawn | I012 | Trinket | Grants a healing aura |
| 40 | Oath of the Last King | I013 | Ring | +5 to all attributes |

These are personal, unsellable boss relics. Boss relics and Crownlands story items use the shared delivery service in `source/rewards.j`. It checks `CreateItem` before using the returned handle. If creation fails, the item rawcode stays in that owner's pending queue and is retried every five seconds while the match clock runs. If the hero cannot accept a successfully created item, it remains visible and owner-bound at that player's base. Both native item owner and the project owner marker are set so other players cannot claim the personal reward. Regression coverage checks boss/story routing, null-handle guards, full-inventory fallback and retry queue behavior; verify pickup, ownership and injected creation failures in Warcraft. Do not rename, replace, or rebalance the relics without updating this catalog and testing their actual native effects.

## Ordinary enemy drops

Enemy gear uses the shared general/racial catalog and explicit Normal, Elite, and Boss tiers from the wave roster. Normal enemies have a 3% gear chance, Elite roles 10%, and bosses 50%; Elite and Boss profiles give higher rarities greater weight. Potion chances are independent at 4% / 8% / 18% for Normal / Elite / Boss. Both rolls can succeed on one death, placing the gear and potion beside each other. Drops from an active defender's kill are owned by that killer; first pickup assigns the owner marker to any otherwise unbound catalog gear so its stats work when equipped. Boss and story completion rewards remain owner-bound through the reward queue.

See [WAVES-AND-BOSSES.md](WAVES-AND-BOSSES.md) for the per-rarity probability table and tiered roster.

## Player-facing interaction acceptance

For each shop: open the shop by clicking/approaching it, see icon stock, hover exact name/cost/slot/stat/effect, buy, find the buyer-owned item in the native backpack UI, move it between storage and normal inventory, equip it, verify stat/proc, unequip and verify removal, and sell ordinary gear back for half price. Confirm boss relics remain unpawnable. Repeat with full normal inventory/storage, two rings, two players buying simultaneously, and post-death revival. Test every shop, tier, recipe, tome, consumable, and reward. These native inventory interactions remain pending until this exact flow passes in game.
