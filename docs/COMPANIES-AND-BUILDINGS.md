# Hero companies and kingdom buildings

**Status:** implemented in source for development builds; editor/shop use, company combat, foundry bonuses, and multiplayer ownership still need exact-build engine checks.

## Buildings

All prices are personal resources. All three structures require the player's Barracks (`hbar`) and use the normal plot and full-footprint validation. The Altar of Kings is preplaced at each base; the player no longer needs a redundant Altar build button.

| Name | Rawcode / native parent | Cost | Build time / HP | Function |
|---|---|---:|---:|---|
| Hall of Banners | `kH00` / Castle `hcas` | 240 gold, 100 lumber | 35 s / 1,400 | Adds the selected hero's personal doctrine aura to this hall and unlocks that player's company at every owned Barracks. |
| Royal Foundry | `kF00` / Blacksmith `hbla` | 360 gold, 150 lumber | 45 s / 1,600 | Permanently grants the owner's company and support recruits +20% max HP and +20% base damage. Applies once to current units and automatically to later recruits. |
| Siege Yard | `kY00` / Workshop `harm` | 300 gold, 125 lumber | 40 s / 1,500 | Sells the hero-matched tactical support unit. Its stock belongs to the yard owner. |

The Altar (`h000`) is created beside each starting Town Hall. The worker build card has twelve or fewer entries; `kY00` uses the native Workshop art and replaces a second, redundant Altar/Workshop button. The other Human buildings and all three tower roles remain on the worker card.

## Hero company catalog

Each row is one selector choice in the same order as `tools/hero_progression.py`. `Company` recruits are stocked by the owner's Barracks only after their Hall is complete. `Support` recruits are stocked at that player's Siege Yard. Costs are gold/lumber; the Foundry upgrade is 20% HP and damage.

| Hero | Barracks company (ID / native model) | Cost; HP; damage | Siege Yard support (ID / native model) | Cost; HP; damage | Hall doctrine |
|---|---|---|---|---|---|
| Paladin | Oathguard (`kC00` / Footman `hfoo`) | 260/70; 900; 34 | Dawn Chaplain (`kS00` / Priest `hmpr`) | 320/100; 650; 22 | Devotion Aura (`AHad`) |
| Mountain King | Rune-Breakers (`kC01` / Footman `hfoo`) | 280/85; 1,000; 40 | Siege Sappers (`kS01` / Mortar Team `hmtm`) | 360/120; 680; 28 | Endurance Aura (`AOae`) |
| Priest | Dawnweavers (`kC02` / Priest `hmpr`) | 240/75; 720; 23 | Beacon Acolyte (`kS02` / Priest `hmpr`) | 300/100; 620; 18 | Brilliance Aura (`AHab`) |
| Blood Mage | Emberguard (`kC03` / Sorceress `hsor`) | 270/80; 760; 30 | Phoenix Sentry (`kS03` / Gryphon Rider `hgry`) | 400/140; 620; 34 | Brilliance Aura (`AHab`) |
| Blademaster | Windcutters (`kC04` / Grunt `ogru`) | 270/80; 850; 38 | Shadow Scout (`kS04` / Wolf Rider `orai`) | 340/110; 650; 30 | Endurance Aura (`AOae`) |
| Far Seer | Stormcallers (`kC05` / Shaman `oshm`) | 260/85; 750; 25 | Spirit Wolf (`kS05` / Wolf Rider `orai`) | 350/120; 700; 33 | Brilliance Aura (`AHab`) |
| Tauren Chieftain | Ancestral Guard (`kC06` / Tauren `otau`) | 320/110; 1,250; 44 | War Drummer (`kS06` / Kodo Beast `okod`) | 360/130; 850; 25 | Endurance Aura (`AOae`) |
| Shadow Hunter | Serpent Wardens (`kC07` / Headhunter `ohun`) | 250/80; 780; 31 | Field Witch Doctor (`kS07` / Shaman `oshm`) | 360/120; 700; 24 | Devotion Aura (`AHad`) |
| Demon Hunter | Felbreakers (`kC08` / Huntress `esen`) | 280/90; 850; 38 | Warden Seeker (`kS08` / Dryad `edry`) | 360/120; 720; 30 | Endurance Aura (`AOae`) |
| Keeper of the Grove | Thornwatch (`kC09` / Dryad `edry`) | 250/90; 760; 25 | Grove Warden (`kS09` / Ancient Protector `etrp`) | 380/130; 800; 28 | Devotion Aura (`AHad`) |
| Priestess of the Moon | Moonstriders (`kC10` / Huntress `esen`) | 270/85; 780; 35 | Starfall Ballista (`kS10` / Glaive Thrower `ebal`) | 420/150; 700; 38 | Trueshot Aura (`AEar`) |
| Warden | Gloomblades (`kC11` / Huntress `esen`) | 270/85; 800; 40 | Shadow Trapwright (`kS11` / Faerie Dragon `efdr`) | 400/140; 700; 30 | Endurance Aura (`AOae`) |
| Death Knight | Graveguard (`kC12` / Ghoul `ugho`) | 280/90; 900; 36 | Bone Cavalier (`kS12` / Abomination `uabo`) | 430/150; 1,050; 42 | Devotion Aura (`AHad`) |
| Lich | Frostbound (`kC13` / Crypt Fiend `ucry`) | 300/100; 850; 34 | Rime Mortar (`kS13` / Banshee `uban`) | 430/160; 740; 36 | Brilliance Aura (`AHab`) |
| Dark Ranger | Black Arrow Company (`kC14` / Skeletal Archer `nska`) | 270/90; 760; 35 | Forsaken Marksman (`kS14` / Fel Stalker `nfel`) | 390/135; 760; 38 | Trueshot Aura (`AEar`) |
| Ilastar, Human | Light’s Vanguard (`kC15` / Footman `hfoo`) | 300/90; 920; 36 | Mercy Bearer (`kS15` / Priest `hmpr`) | 380/120; 720; 26 | Devotion Aura (`AHad`) |
| Forsaken Paladin | Argent Revenants (`kC16` / Ghoul `ugho`) | 310/100; 1,000; 39 | Cleansing Pyre (`kS16` / Priest `hmpr`) | 400/135; 740; 30 | Devotion Aura (`AHad`) |

These custom unit records inherit their native parent model, portrait/icon, and ability set, then override the name, tooltip, cost, health, and base damage. They belong to their buyer's player and never join `KLS_Enemies`, so they cannot hold a wave open or generate enemy bounties. A mismatched-player Barracks/Siege Yard purchase is removed and refunded. The four banner doctrines use installed Warcraft abilities, not project-invented rawcodes.

## Engineering source of truth

- `tools/company_catalog.py` owns the hero-to-company pairing, all 17 unit stats/costs, banner choices, building models and prices.
- `tools/objects.py` serializes all 3 structures and 34 recruit unit records; `tools/pipeline.py` inserts the generated company runtime.
- `source/companies.j` handles Hall/Barracks/Siege Yard unlocks, owner checks, recruiting, stock replenishment, and the permanent Foundry upgrade.
- `source/heroes.j` stores the selector index on the player before company shops can unlock.
- Regression coverage is in `tests/test_company_expansion.py`. Tests prove catalog/metadata/package rules, not visual placement, shop UI, aura behavior, or multiplayer correctness in Warcraft III.

## Still to verify in game

Build one Barracks, Hall, Royal Foundry, and Siege Yard. Confirm the Hall adds only the correct hero's recruit to that player's Barracks, each Siege Yard sells its matching support recruit, a teammate cannot buy another player's company, and all recruits retain their current orders/control ownership. Build the Foundry before and after recruiting, and verify the +20% max HP/base damage applies once. Confirm none of the friendly recruits affects enemy counts or combat gold.
