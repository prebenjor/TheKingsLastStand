# Hero companies and kingdom buildings

**Status:** implemented in source for development builds; editor/shop use, company combat, foundry bonuses, and multiplayer ownership still need exact-build engine checks.

## Buildings

All prices are personal resources. Each structure requires the player's race-matched Barracks (Human `hbar`, Orc `obar`, Night Elf Ancient of War `eaom`, or Undead Crypt `usep`) and uses normal plot and full-footprint validation. The Altar of Kings is preplaced at each base; the player no longer needs a redundant Altar build button.

| Name | Rawcode / native parent | Cost | Build time / HP | Function |
|---|---|---:|---:|---|
| Hall of Banners | `kH00`–`kH03` / Gryphon Aviary `hgra`, Orc Bestiary `obea`, Hunter's Hall `edob`, Tomb of Relics `utom` | 240 gold, 100 lumber | 35 s / 1,400 | Uses a distinct race-native building model, adds the selected hero's personal doctrine aura to the Hall and unlocks that player's company at every owned Barracks. |
| Royal Foundry | `kF00`–`kF03` / race-native smiths | 360 gold, 150 lumber | 45 s / 1,600 | Permanently grants the owner's company and support recruits +20% max HP and +20% base damage. Also sells one stock of its race's 9,000-gold Legendary pattern. Applies the troop bonus once to current units and automatically to later recruits. |
| Siege Yard | `kY00` / Workshop `harm` | 300 gold, 125 lumber | 40 s / 1,500 | Sells the hero-matched tactical support unit. Its stock belongs to the yard owner. |

The Altar (`h000`) is created beside each starting Town Hall. The worker build card has twelve or fewer entries; `kY00` uses the native Workshop art and replaces a second, redundant Altar/Workshop button. The other Human buildings and all three tower roles remain on the worker card.

Hall models intentionally differ by race so none appears as a duplicate keep. Each built Foundry has the native item-shop command card and exposes only its matching recipe: Human Crownward (`RCP4`), Orc Redtusk (`RCP5`), Night Elf Moonbark (`RCP6`), or Undead Wraith (`RCP7`). The Master Forge keeps the three general recipes. Craft scrolls return to the vendor that sold them after success or failure; if that vendor has been destroyed, they return to the Master Forge. A Foundry's racial pattern remains personal to its owner.

### Race-specific support buildings and towers

| Race | Arcane/support building (ID / native parent) | Role and tooltip identity | Towers (IDs) |
|---|---|---|---|
| Human | Arcane Sanctum `h004` / Arcane Sanctum `hars` | Priests, Sorceresses, and their native research | Guard `h001`, Cannon `h002`, Sanctuary `h003` |
| Orc | Spirit Lodge `kR01` / Spirit Lodge `osld` | Shamans, Witch Doctors, Spirit Walkers, and their research | Watch `kT10`, War Drum `kT11`, Spirit Ward `kT12` |
| Night Elf | Ancient Lore Grove `kR02` / Ancient of Lore `eaoe` | Druids of the Claw, Dryads, Mountain Giants, and nature research | Protector `kT20`, Moonfire `kT21`, Moonwell Sentinel `kT22` |
| Undead | Temple of the Damned `kR03` / Temple of the Damned `utod` | Necromancers, Banshees, and dark-ritual research | Ziggurat `kT30`, Frost `kT31`, Soulwell Spire `kT32` |

Race-specific altars, company buildings, arcane shops, and towers now carry descriptions for their actual faction and function. The Undead Temple inherits the native Temple's model, icon, training and research orders; its previous Meat Wagon parent (`umtw`) was incorrect. Sanitarium towers share the Human Sanctuary runtime: they heal allied units for 15 HP every 3 seconds within 650 range. Object names/tooltips and source hooks are catalog-driven in `tools/faction_catalog.py`; check the native queue, icons, and healing in the editor/game.

The Night Elf build menu uses Ancient of War (`eaom`) as its Barracks and Hunter's Hall (`edob`) as its upgrade building. Its separate Ancient Lore Grove remains based on Ancient of Lore (`eaoe`). Tree of Ages (`etoa`) requires the Tier One Ancient of War, Hunter's Hall and Night Elf Hero Shrine (`kA02`); Ancient of Wind (`eaow`) and Ancient of Lore require Tree of Ages, so neither may be a prerequisite for that upgrade.

## Hero company catalog

| Hero | Company / installed parent | Gold / lumber; HP; base damage | Support / installed parent | Gold / lumber; HP; base damage | Doctrine |
|---|---|---:|---|---:|---|
| Paladin | Oathguard (`kC00` / `hfoo`) | 260/70; 900; 34 | Dawn Chaplain (`kS00` / `hmpr`) | 320/100; 650; 22 | `AHad` |
| Mountain King | Rune-Breakers (`kC01` / `hfoo`) | 280/85; 1000; 40 | Siege Sappers (`kS01` / `hmtm`) | 360/120; 680; 28 | `AOae` |
| Priest | Dawnweavers (`kC02` / `hmpr`) | 240/75; 720; 23 | Beacon Acolyte (`kS02` / `hmpr`) | 300/100; 620; 18 | `AHab` |
| Blood Mage | Emberguard (`kC03` / `hsor`) | 270/80; 760; 30 | Phoenix Sentry (`kS03` / `hgry`) | 400/140; 620; 34 | `AHab` |
| Blademaster | Windcutters (`kC04` / `ogru`) | 270/80; 850; 38 | Shadow Scout (`kS04` / `orai`) | 340/110; 650; 30 | `AOae` |
| Far Seer | Stormcallers (`kC05` / `oshm`) | 260/85; 750; 25 | Spirit Wolf (`kS05` / `orai`) | 350/120; 700; 33 | `AHab` |
| Tauren Chieftain | Ancestral Guard (`kC06` / `otau`) | 320/110; 1250; 44 | War Drummer (`kS06` / `okod`) | 360/130; 850; 25 | `AOae` |
| Shadow Hunter | Serpent Wardens (`kC07` / `ohun`) | 250/80; 780; 31 | Field Witch Doctor (`kS07` / `oshm`) | 360/120; 700; 24 | `AHad` |
| Demon Hunter | Felbreakers (`kC08` / `esen`) | 280/90; 850; 38 | Warden Seeker (`kS08` / `edry`) | 360/120; 720; 30 | `AOae` |
| Keeper of the Grove | Thornwatch (`kC09` / `edry`) | 250/90; 760; 25 | Grove Warden (`kS09` / `edry`) | 380/130; 800; 28 | `AHad` |
| Priestess of the Moon | Moonstriders (`kC10` / `esen`) | 270/85; 780; 35 | Starfall Ballista (`kS10` / `ebal`) | 420/150; 700; 38 | `AEar` |
| Warden | Gloomblades (`kC11` / `esen`) | 270/85; 800; 40 | Shadow Trapwright (`kS11` / `efdr`) | 400/140; 700; 30 | `AOae` |
| Death Knight | Graveguard (`kC12` / `ugho`) | 280/90; 900; 36 | Bone Cavalier (`kS12` / `uabo`) | 430/150; 1050; 42 | `AHad` |
| Lich | Frostbound (`kC13` / `ucry`) | 300/100; 850; 34 | Rime Mortar (`kS13` / `uban`) | 430/160; 740; 36 | `AHab` |
| Dark Ranger | Black Arrow Company (`kC14` / `nska`) | 270/90; 760; 35 | Forsaken Marksman (`kS14` / `nska`) | 390/135; 760; 38 | `AEar` |
| Ilastar, Human | Light’s Vanguard (`kC15` / `hfoo`) | 300/90; 920; 36 | Mercy Bearer (`kS15` / `hmpr`) | 380/120; 720; 26 | `AHad` |
| Forsaken Paladin | Argent Revenants (`kC16` / `ugho`) | 310/100; 1000; 39 | Cleansing Pyre (`kS16` / `uban`) | 400/135; 740; 30 | `AHad` |
| Aveline Ashford | Lionguard (`kC17` / `hfoo`) | 290/80; 980; 36 | Banner Chaplain (`kS17` / `hmpr`) | 340/110; 700; 24 | `AHad` |
| Toren Flintlock | Powderwrights (`kC18` / `hmtm`) | 300/100; 900; 42 | Field Engineer (`kS18` / `hmpr`) | 380/140; 680; 32 | `AHad` |
| Korgal Redtusk | Redtusk Breakers (`kC19` / `otau`) | 340/120; 1320; 48 | Bloodfire Drummer (`kS19` / `oshm`) | 390/140; 900; 30 | `AOae` |
| Morgra Ashcaller | Ashcallers (`kC20` / `oshm`) | 290/95; 820; 34 | Spirit Guide (`kS20` / `orai`) | 390/140; 760; 28 | `AOae` |
| Selyra Moonlance | Moonlance Sentinels (`kC21` / `esen`) | 300/100; 900; 40 | Moonwell Keeper (`kS21` / `edry`) | 430/150; 780; 34 | `AEar` |
| Faelor Briarward | Briarward Guard (`kC22` / `edry`) | 280/100; 850; 31 | Thornmender (`kS22` / `edry`) | 410/145; 840; 29 | `AEar` |
| Veyra Wraithveil | Veilbound Wraiths (`kC23` / `uban`) | 300/100; 820; 38 | Grave Cantor (`kS23` / `ucry`) | 420/160; 780; 40 | `AUau` |
| Tharos Bonecrown | Bonecrown Wardens (`kC24` / `ugho`) | 330/110; 1150; 46 | Crypt Acolyte (`kS24` / `ucry`) | 430/160; 1050; 39 | `AUau` |

These custom unit records inherit their native parent model, portrait/icon, then replace the ability set with its authored power and override the name, tooltip, cost, health, and base damage. They belong to their buyer's player and never join `KLS_Enemies`, so they cannot hold a wave open or generate enemy bounties. A mismatched-player Barracks/Siege Yard purchase is removed and refunded. The four banner doctrines use installed Warcraft abilities, not project-invented rawcodes.

## Engineering source of truth

- `tools/company_catalog.py` owns the hero-to-company pairing, all 25 unit stats/costs, banner choices and shared company building prices. `tools/faction_catalog.py` owns the race-specific Hall model parents and Foundry identities.
- `tools/objects.py` serializes all 12 race-flavored structures and 50 recruit unit records; `tools/pipeline.py` inserts the generated company runtime.
- `source/companies.j` handles Hall/Barracks/Siege Yard unlocks, owner checks, recruiting, stock replenishment, the racial Foundry recipe shop, and the permanent Foundry upgrade. `tools/recipes.py` generates recipe identities and stores each transaction's selling vendor so the pattern returns to the right stock.
- `source/heroes.j` stores the selector index on the player before company shops can unlock.
- Regression coverage is in `tests/test_company_expansion.py`. Tests prove catalog/metadata/package rules, not visual placement, shop UI, aura behavior, or multiplayer correctness in Warcraft III.

## Still to verify in game

Build one Barracks, Hall, Royal Foundry, and Siege Yard for each race. Confirm the four distinct Hall models appear, the Hall adds only the correct hero's recruit to that player's Barracks, each Siege Yard sells its matching support recruit, and a teammate cannot buy another player's company or racial Foundry pattern. Buy and craft each Foundry pattern; confirm the correct race's pattern appears, the +20% max HP/base damage applies once, and the scroll returns to that same Foundry after both successful and failed crafts. Confirm none of the friendly recruits affects enemy counts or combat gold.
# Current four-race implementation

The earlier Human-only company design is superseded by the user-approved mixed-race rule. Hero selection gives each player the corresponding Peasant, Peon, Wisp or Acolyte. Their Town Hall, altar, worker menu, three tower roles, Arcane/support building, Hall, Foundry and Siege Yard are race-themed while shared role costs and behavior stay aligned. The complete rawcode/catalog table is in [CROWNLANDS-EXPANSION.md](CROWNLANDS-EXPANSION.md) and tools/faction_catalog.py.

Company and support recruit pairs remain specific to all 25 heroes. The eight new hero pairs and signature descriptions are listed in the Crownlands document and generated from tools/hero_catalog.py and tools/company_catalog.py.

## September 30 audit completion

All four racial Halls sell three Company Chapters. Foundries sell three weapon and armor ranks beside their Legendary recipe; Siege Yards sell Counter-Siege Drill; arcane structures retain native training/research and add Spiritcraft Accord. All services are owner-specific, charge personal gold/lumber, require the matching living hero nearby, and refund invalid/obsolete purchases. Chapter gates are town recovery stages or waves 10/20/30. Effects apply once to current and future troops; revived troops retain their bonuses.

All 50 company/support recruits now have authored point-target powers and mobile native parents. The generated [company power and research catalog](COMPANY-RESEARCH-AND-POWERS.md) owns the complete IDs, numbers, costs and conditions. Verify native command-card stock, queue coexistence, casts, refunds and research stat deltas in a mixed-race match.
