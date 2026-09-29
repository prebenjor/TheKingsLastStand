# Crownlands expansion: design and implementation contract

This document is the current detailed design for the kingdom expansion. It incorporates the approved race identity, settlement, hero, equipment, story and progression decisions. Read it with [GAME-VISION.md](GAME-VISION.md), [HEROES-AND-ABILITIES.md](HEROES-AND-ABILITIES.md), [COMPANIES-AND-BUILDINGS.md](COMPANIES-AND-BUILDINGS.md), [ITEMS-AND-EQUIPMENT.md](ITEMS-AND-EQUIPMENT.md), and [TECHNICAL-ARCHITECTURE.md](TECHNICAL-ARCHITECTURE.md). Source catalogs live in `tools/town_catalog.py`, `tools/faction_catalog.py`, `tools/hero_catalog.py`, `tools/company_catalog.py`, `tools/equipment_catalog.py`, and `tools/recipes.py`.

## Player promise

Players choose one of 25 heroes. That hero's race independently sets the owner's worker, Altar, Town Hall and build menu. Every player has a personal base and army, while all four allied communities help King Aldric hold the King's Road. Heroes grow from level 1 to a temporary cap of 50. Every level grants a choice to place three stat points; every five levels grants a separate talent choice. An optional four-part town-recovery story can be advanced during live waves without pausing or changing their enemy count.

The product remains a 2-4 player co-op defense RPG. Preserve the original 40-wave Crownlands story and bosses on waves 10, 20, 30 and 40, then continue automatically through the bounded ten-wave campaign crossover. Bosses recur every ten waves; only King Aldric's death ends the run, and the HUD shows the highest wave reached. Normal intermissions are 50 seconds and every pre-boss intermission is 180 seconds.

## Crownlands map and settlements

- Battlefield: 192 × 192 terrain cells (24,576 Warcraft world units square), map bounds ±12,288, playable/camera bounds ±11,520. Terrain, pathing, W3I bounds, camera and minimap must describe the same battlefield.
- Player plots stay at `(-6000,-500)`, `(-3300,-500)`, `(3300,-500)`, `(6000,-500)`. The north-to-south paved King's Road, open central gate, defensive row, castle and southern market remain readable and clear.
- Town centers sit at Human Crownshire `(0,-9000)`, Orc Redtusk Hold `(-9000,0)`, Night Elf Moonbark Glade `(9000,0)`, and Undead Wraithfall `(0,9000)`. Branch roads connect the east and west settlements to the central avenue; town plazas connect to their branch. Keep structures off the clear lane.
- Each town shows its native-race Town Hall, Altar, food building, Barracks, Blacksmith, one watch tower, a named neutral shop and a race-matched quest-giver. The four settlements are allied to Aldric's defenders and use installed Warcraft models.
- Town shops sell their race's four Common-through-Epic universally equippable relics plus healing and mana potions. The Legendary relic is not sold directly; its Foundry pattern combines the listed racial components into the Legendary output, and the item remains eligible for the existing enemy-drop rules. Generic rarity vendors exclude all race-themed relics. Item definitions, stats, rarity colors, stock IDs and drops come from the shared item catalog.
- The separate Master Forge in the southern market stocks the three general recipe patterns. Each player's race-themed Royal Foundry stocks one copy of its matching racial Legendary pattern after construction. Racial patterns can only be bought from an owned matching Foundry; scrolls return to the seller after success or failure, with the Master Forge as a fallback if the seller is destroyed during crafting. Generic rarity shops hold at most nine items, the Archive nine tomes, the Apothecary four consumables, each town relic shop six entries, the Master Forge three recipes, and each Foundry one recipe, within Warcraft's twelve-slot shop command card.

For hand-authored terrain dressing, see [TERRAIN-DRESSING-GUIDE.md](TERRAIN-DRESSING-GUIDE.md). Its four-panel visual is a reference for road shoulders, branch paths, rocky passes, settlement edges, and the undead frontier; preserve the navigable defense route and resource access while editing.

### Settlement identity

| Town | Race | Worker | Town Hall / Barracks / Altar | Shop | Story character |
|---|---|---|---|---|---|
| Crownshire | Human | Peasant `hpea` | `htow` / `hbar` / `h000` | Crownshire Provisioner | Crownshire Supplymaster |
| Redtusk Hold | Orc | Peon `opeo` | `ogre` / `obar` / `kA01` | Redtusk Quartermaster | Northwatch Vanguard |
| Moonbark Glade | Night Elf | Wisp `ewsp` | `etol` / `eaow` / `kA02` | Moonbark Curator | Moonbark Warden |
| Wraithfall | Undead | Acolyte `uaco` | `unpl` / `usep` / `kA03` | Wraithfall Broker | Wraithfall Keeper |

## Race identity and player companies

The native tier-two town-hall upgrades must recognize those custom Altars. Their required-structure lists use each race's reachable Tier One Barracks, upgrade building, and altar rawcodes: Human Castle hcas requires hbar, hbla, h000; Orc Stronghold ostr requires obar, ofor, kA01; Night Elf Tree of Ages etoa requires eaom (Ancient of War), edob (Hunter's Hall), kA02; Undead Halls of the Dead unp1 requires usep, uslh, kA03. Do not require eaow (Ancient of Wind) or eaoe (Ancient of Lore) to upgrade to Tree of Ages: both require Tree of Ages themselves and would create a deadlock. The Night Elf build menu uses Ancient of War as its Barracks, Hunter's Hall as its upgrade building, and the separate Ancient Lore Grove as its arcane structure.

Race is assigned per selected hero and per owner. It must not be inferred from another player's hero or a fixed Human lobby preference. The map starts with race preference set to Random; confirming a Human, Orc, Night Elf or Undead hero sets only that player's Warcraft race preference and replaces their starting Town Hall, altar and five workers with the matching faction. In mixed-race matches, each build menu and constructed role stays matched to its owner.

When a hero is confirmed, the Undead player's starting neutral mine is replaced with an owner-controlled Haunted Gold Mine, and the Night Elf player's with an owner-controlled Entangled Gold Mine. Both retain the full 1,000,000-gold reserve and the same plot location. Human and Orc players keep a neutral Gold Mine. The Undead order handler also recognizes Warcraft's native `hauntgoldmine` order for any additional neutral mine; the Night Elf Tree of Life's native Entangle range is 1,450. Confirm these native mine types and worker routes in Warcraft; source checks do not prove engine harvesting behavior.

The custom Undead Temple of the Damned (`kR03`, parent `utod`) explicitly uses `ReplaceableTextures\CommandButtons\BTNTempleOfTheDamned.dds`. Keep the icon override: the user reported the inherited command button displaying the Meat Wagon icon even though the building inherited the correct Temple parent. The object-data regression checks both parent and icon path.

| Role | Human | Orc | Night Elf | Undead |
|---|---|---|---|---|
| Worker | Peasant `hpea` | Peon `opeo` | Wisp `ewsp` | Acolyte `uaco` |
| Hall of Banners | Hall of Banners `kH00` | Redtusk Banner Hall `kH01` | Moonlit Banner Hall `kH02` | Bone Banner Hall `kH03` |
| Foundry | Royal Foundry `kF00` | Ashen War Forge `kF01` | Moonbark Runeforge `kF02` | Wraithforged Smithy `kF03` |
| Siege Yard | Siege Yard `kY00` | War Drummer Lodge `kY01` | Sentinel War Grove `kY02` | Graveyard of Arms `kY03` |
| Arcane/support | Arcane Sanctum `h004` | Spirit Lodge `kR01` | Ancient Lore Grove `kR02` | Temple of the Damned `kR03` |
| Three towers | Guard / Cannon / Sanctuary | Watch / War Drum / Spirit Ward | Protector / Moonfire / Moonwell Sentinel | Ziggurat / Frost / Soulwell Spire |

Hall, Foundry and Siege Yard roles have shared costs across races: 240 gold/100 lumber, 360/150, and 300/125 respectively. The Hall unlocks that hero's Barracks company and doctrine. The Foundry grants company and support recruits +20% maximum health and base damage once; it applies to existing and future recruits. The Siege Yard trains the hero's personal support recruit. Company units are defender-owned; never count them as wave enemies or bounty sources. Full 12-slot worker menus and catalog entries are defined in `tools/faction_catalog.py` and `tools/company_catalog.py`.

This is a focused race-flavored base system, not a request to reproduce every classic tech-tree building. Keep common construction validation, role behavior and costs shared.

## Selectable heroes

There are 25 choices; duplicate choices remain allowed. The original 17 are documented in [HEROES-AND-ABILITIES.md](HEROES-AND-ABILITIES.md). Eight new choices use verified installed parent heroes for their model, portrait and animations. Each has four native skills, a custom signature spell, a matching company recruit and a matching support recruit.

| Rawcode | Hero / race | Combat identity | Signature | Company / support |
|---|---|---|---|---|
| `Havl` | Aveline Ashford — Human | Banner defender; protects allies and turns rallies into counterattacks | Crownward Rally | Lionguard / Banner Chaplain |
| `Htor` | Toren Flintlock — Human | Siege artificer; disrupts clustered attackers | Flintlock Barrage | Powderwrights / Field Engineer |
| `Okrg` | Korgal Redtusk — Orc | Cleaving front line | Redtusk Earthshatter | Redtusk Breakers / Bloodfire Drummer |
| `Omor` | Morgra Ashcaller — Orc | Spirit caster and hunter | Ashen Spiritpack | Ashcallers / Spirit Guide |
| `Esly` | Selyra Moonlance — Night Elf | Precision huntress | Moonlance Volley | Moonlance Sentinels / Moonwell Keeper |
| `Efal` | Faelor Briarward — Night Elf | Thorn-control sentinel; nature powers do not require nearby trees | Briarward Stand | Briarward Guard / Thornmender |
| `Uvyr` | Veyra Wraithveil — Undead | Curse-focused banshee | Wraithveil Curse | Veilbound Wraiths / Grave Cantor |
| `Utha` | Tharos Bonecrown — Undead | Gravewarden and bone-guard summoner | Bonecrown Guard | Bonecrown Wardens / Crypt Acolyte |

The generated hero object inherits its model, portrait, animation and four native skills from the listed parent. AK17–AK24 use the shared signature runtime: 700 cast range, 350 effect radius, 70 mana, 30-second cooldown; authored damage gains 20 per hero level, authored healing gains 15 per hero level, and summoned creatures have 300 + 30 health and 12 + 2 damage per hero level for 25 seconds.

| Hero rawcode | Native parent / four native ability IDs | Signature rawcode and base behavior | Matching recruits |
|---|---|---|---|
| `Havl` | Human Paladin `Hpal`; `AHhb`, `AHds`, `AHad`, `AHre` | `AK17` Crownward Rally — Holy Bolt effect; 100 area damage, 250 allied HP healing and 80 allied mana restoration | `kC17` Lionguard / `kS17` Banner Chaplain |
| `Htor` | Human Mountain King `Hmkg`; `AHtb`, `AHtc`, `AHbh`, `AHav` | `AK18` Flintlock Barrage — Thunder Clap effect; 320 area damage and 3-second slow | `kC18` Powderwrights / `kS18` Field Engineer |
| `Okrg` | Orc Tauren Chieftain `Otch`; `AOsh`, `AOws`, `AOae`, `AOre` | `AK19` Redtusk Earthshatter — War Stomp effect; 380 area damage and 150 caster healing | `kC19` Redtusk Breakers / `kS19` Bloodfire Drummer |
| `Omor` | Orc Shadow Hunter `Oshd`; `AOhw`, `AOhx`, `AOsw`, `AOvd` | `AK20` Ashen Spiritpack — Spirit Wolf effect; 180 area damage, restores 60 mana to allied units, summons three `osw1` wolves | `kC20` Ashcallers / `kS20` Spirit Guide |
| `Esly` | Night Elf Priestess of the Moon `Emoo`; `AEst`, `AHfa`, `AEar`, `AEsf` | `AK21` Moonlance Volley — Starfall effect; 300 area damage | `kC21` Moonlance Sentinels / `kS21` Moonwell Keeper |
| `Efal` | Night Elf Keeper of the Grove `Ekee`; `AEer`, `AEfn`, `AEah`, `AEtq` | Runtime removes tree-dependent `AEfn`; `AK22` Briarward Stand summons three `efon` treants without needing trees while dealing 180 area damage, healing allies for 100 HP and restoring 40 allied mana | `kC22` Briarward Guard / `kS22` Thornmender |
| `Uvyr` | Undead Dark Ranger `Nbrn`; `ANsi`, `ANba`, `ANdr`, `ANch` | `AK23` Wraithveil Curse — Fan of Knives effect; 260 area damage, drains up to 40 mana from each enemy hit and transfers drained mana to Veyra | `kC23` Veilbound Wraiths / `kS23` Grave Cantor |
| `Utha` | Undead Death Knight `Udea`; `AUdc`, `AUdp`, `AUau`, `AUan` | `AK24` Bonecrown Guard — Death Coil effect; 120 area damage, 80 allied HP healing, summons three `uske` skeletons | `kC24` Bonecrown Wardens / `kS24` Crypt Acolyte |

Matching recruit models, gold/lumber prices, base health, base damage and banner doctrines are recorded in [COMPANIES-AND-BUILDINGS.md](COMPANIES-AND-BUILDINGS.md) and `tools/company_catalog.py`. Every selector portrait must match the created hero unit. Faelor's nature abilities do not require tree destructables. The standard Keeper hero uses the same tree-free signature approach; its native tree-consuming `AEfn` is removed. Dark/Necromantic spells and heals must work with both living and undead defenders, as appropriate.

## Leveling, attributes and safe spell ranks

- The selected hero starts at level 1. Temporary maximum is 50. King Aldric and wave-owned hero enemies retain their separately authored levels.
- On every gained hero level, automatically add +3 to that hero's primary damage attribute and +1 to each other attribute. Zero the installed native hero-growth fields for selectable hero records to avoid duplicate growth; apply this increment once for every crossed level, including a multi-level award. Independently, keep the hero's four normal learnable skills and show three owner-only buttons above the command-card ability grid when the hero has an unspent skill point: `+3 STR`, `+3 AGI`, and `+3 INT`. Clicking one spends one normal skill point and adds exactly +3 to the named stat. These are repeatable unranked choices: do not make them levelled abilities or show rank numbers. Normal spell `+` upgrades remain available and spend the same points. The buttons are non-modal, appear only while the owning hero is selected with unspent points, and must not pause the game for any player.
- Grant a separate talent point for every crossed five-level milestone (levels 5, 10, …, 50). A visible dialog offers:
  - **Vanguard / Strength:** +5 Strength, +200 maximum/current health and +2 health regeneration per second per talent.
  - **Skirmisher / Agility:** +5 Agility (therefore native attack-speed growth) and +2 percentage points evasion per talent.
  - **Sage / Intelligence:** +5 Intelligence, +100 maximum/current mana and +2 mana regeneration per second per talent.
- Talent award bookkeeping is per hero owner, preserves points earned across multi-level jumps, and presents the option visibly. Do not spend a point until the player selects an option.
- The five-level Vanguard/Skirmisher/Sage specialty remains its own dialog and needs a live multiplayer check; it is separate from per-level primary-stat choices.
- Native skill ranks retain authored values through the installed maximum. For skills with explicitly registered scalable power fields only, rank 4 and 5 add 10% of the rank-3 value per rank; range, cooldown, mana cost, duration, targeting and unrelated fields stay at the last authored value. Unsupported skills retain their native cap.
- Sacred Aura learned descriptions for both `AHas` and `AHpa` show the actual current rank and actual values. Learn descriptions separate current and next rank and show all five values. Rank 4 is 38.5% magic resistance / 27.5% increased healing; rank 5 is 42% / 30%. Generated descriptions and effect data must be produced together.

## Optional Crownlands recovery story

The story is shared, optional and persistent through one match. Site interactions stay available during waves. No objective pauses the match, changes the normal/boss countdown, delays a spawn, enters objective enemies into `KLS_Enemies`, or increments/decrements `KLS_Alive`. Missed objectives do not expire or block victory. The player who starts, funds, escorts or defeats threats is a personal contributor; each contributor receives personal gold and a bound catalog item when that shared chapter completes.

1. **Reclaim Northwatch:** accept from the Northwatch Vanguard at Redtusk Hold; defeat its four attackers. Its attackers are tracked in a separate story group.
2. **Escort the supplies:** start at the Crownshire Supplymaster. A visible supply caravan follows the King's Road south-to-center while waves continue. A second defender may join an escort already underway.
3. **Restore Moonbark's quarter:** contribute 250 personal gold and 100 personal lumber at the Moonbark Warden. The payment is charged only on acceptance; the story unlock is shared.
4. **Break the Wraithfall ritual:** accept from the Wraithfall Keeper and defeat four undead/demon ritual guards.

Each completion gives every recorded contributor personal gold and one ownership-bound item from the common/uncommon/rare progression. Story enemy kills also pay the credited killer a personal 25 gold; they do not share kill gold. Stage progress is match-scoped only and has no between-match save.

## Rarity item catalog and recipes

Use standard item-name and tooltip colors: Common white `|cffffffff`, Uncommon green `|cff1eff00`, Rare blue `|cff0070dd`, Epic purple `|cffa335ee`, Legendary gold `|cffff8000`. Every listed item is equippable by any hero, and every entry has an installed icon, one or more stat effects, item tooltip, shop stock, and drop eligibility from the shared catalog.

| Race theme | Rarity and item | Current catalog stats |
|---|---|---|
| Human | Common — Watchman’s Token | +120 health, +2 Strength |
| Human | Uncommon — Lionroad Mantle | +8 Strength, +360 health |
| Human | Rare — Aldric’s Aegis | +20 armor, +20 Strength |
| Human | Epic — Crownward Pennant | +42 Strength, +2,100 health |
| Human | Legendary — Last King’s Oath | +88 Strength, +220 damage, +5,500 health |
| Orc | Common — Redtusk Fetish | +3 Strength, +3 damage |
| Orc | Uncommon — Ashen War Drum | +6 Strength, +10% attack speed |
| Orc | Rare — Stormscar Bracers | +16 Strength, +28% attack speed |
| Orc | Epic — Grudgebreaker | +168 damage, +28 Strength |
| Orc | Legendary — Worldrend Standard | +220 damage, +99 Strength |
| Night Elf | Common — Moonbark Charm | +2 Agility, +100 health |
| Night Elf | Uncommon — Starleaf Quiver | +6 Agility, +10% attack speed |
| Night Elf | Rare — Duskwatch Longbow | +60 damage, +16 Agility |
| Night Elf | Epic — Briarheart Mantle | +42 Agility, +1,750 health |
| Night Elf | Legendary — Silvermoon Vigil | +88 Agility, +88% attack speed |
| Undead | Common — Crypt-Iron Band | +2 Intelligence, +1 armor |
| Undead | Uncommon — Wraithsilk Cape | +6 Intelligence, +200 mana |
| Undead | Rare — Soulreaper’s Fang | +36 damage, +20 Intelligence |
| Undead | Epic — Mourning Reliquary | +42 Intelligence, +2,100 mana |
| Undead | Legendary — Night’s Covenant | +88 Intelligence, +2,750 health, +4,400 mana |

| Foundry recipe | Components | Result | Recipe price |
|---|---|---|---:|
| Crownward Foundry Pattern `RCP4` | Aldric's Aegis + Lionroad Mantle | Last King's Oath | 9,000 gold |
| Redtusk Foundry Pattern `RCP5` | Stormscar Bracers + Ashen War Drum | Worldrend Standard | 9,000 gold |
| Moonbark Foundry Pattern `RCP6` | Duskwatch Longbow + Starleaf Quiver | Silvermoon Vigil | 9,000 gold |
| Wraith Foundry Pattern `RCP7` | Soulreaper's Fang + Wraithsilk Cape | Night's Covenant | 9,000 gold |

### Native item object and equipment-slot IDs

Each custom item object uses the listed native parent for its installed icon/art and click behavior. Generated per-item stat abilities apply the catalog bonuses while equipped; `tools/equipment_catalog.py` owns the amounts and ability records. Rawcodes are case-sensitive. Purchase prices are personal gold; each racial settlement stocks its own five themed items.

| Race | Rarity item | Item rawcode / native parent | Slot | Price | Stat ability rawcodes |
|---|---|---|---|---:|---|
| Human | Common Watchman’s Token | `I23C` / `elmt` | Trinket | 300 | `A03C`, `A13C` |
| Human | Uncommon Lionroad Mantle | `I23G` / `emoh` | Chest | 1,000 | `A03G`, `A13G` |
| Human | Rare Aldric’s Aegis | `I23K` / `eosc` | Offhand | 3,000 | `A03K`, `A13K` |
| Human | Epic Crownward Pennant | `I23O` / `ebdf` | Trinket | 8,000 | `A03O`, `A13O` |
| Human | Legendary Last King’s Oath | `I23S` / `erdr` | Ring | 20,000 | `A03S`, `A13S`, `A23S` |
| Orc | Common Redtusk Fetish | `I23D` / `elmt` | Trinket | 300 | `A03D`, `A13D` |
| Orc | Uncommon Ashen War Drum | `I23H` / `etkj` | Trinket | 1,000 | `A03H`, `A13H` |
| Orc | Rare Stormscar Bracers | `I23L` / `eggn` | Gloves | 3,000 | `A03L`, `A13L` |
| Orc | Epic Grudgebreaker | `I23P` / `efpb` | Primary | 12,000 | `A03P`, `A13P` |
| Orc | Legendary Worldrend Standard | `I23T` / `ehls` | Offhand | 20,000 | `A03T`, `A13T` |
| Night Elf | Common Moonbark Charm | `I23E` / `ebdf` | Trinket | 300 | `A03E`, `A13E` |
| Night Elf | Uncommon Starleaf Quiver | `I23I` / `epsb` | Primary | 1,500 | `A03I`, `A13I` |
| Night Elf | Rare Duskwatch Longbow | `I23M` / `epsb` | Primary | 4,500 | `A03M`, `A13M` |
| Night Elf | Epic Briarheart Mantle | `I23Q` / `emoh` | Chest | 8,000 | `A03Q`, `A13Q` |
| Night Elf | Legendary Silvermoon Vigil | `I23U` / `ejjr` | Ring | 20,000 | `A03U`, `A13U` |
| Undead | Common Crypt-Iron Band | `I23F` / `ecav` | Ring | 300 | `A03F`, `A13F` |
| Undead | Uncommon Wraithsilk Cape | `I23J` / `edsm` | Chest | 1,000 | `A03J`, `A13J` |
| Undead | Rare Soulreaper’s Fang | `I23N` / `epbs` | Primary | 4,500 | `A03N`, `A13N` |
| Undead | Epic Mourning Reliquary | `I23R` / `eege` | Trinket | 8,000 | `A03R`, `A13R` |
| Undead | Legendary Night’s Covenant | `I23V` / `ehls` | Offhand | 20,000 | `A03V`, `A13V`, `A23V` |

Recipes consume components only when crafting succeeds. Failed craft attempts preserve every component and refund the full recipe fee. Ordinary enemy gear drops total 3%, durable/elite role drops total 10%, and bosses total 50%, with the higher tiers weighted toward better rarities. Potion chances are separate rolls: 4% for ordinary enemies, 8% for elites, and 18% for bosses. Since the gear and potion rolls are independent, one death can drop both; the second item is placed beside the first. Ordinary drops belong to the killing defender, while story rewards are bound to contributors. See [WAVES-AND-BOSSES.md](WAVES-AND-BOSSES.md) for the exact rarity table and enemy-tier mapping.

## Build, evidence and maintenance

- Edit modular files in `source/` and deterministic generators/catalogs in `tools/`. `tools/pipeline.py` is the explicit module order. `source/war3map.j` and `build/` outputs are generated and must not be hand-edited.
- Build only with `python -B tools/build_map.py`. Keep one current map in `dist/`, named `<build-id>-Development.w3m`; archive the previous development artifact under `backups/development-builds/`. Do not create ad hoc map copies.
- The earlier user-reported Test Map remains a **pass for its own build ID**. It does not prove a later package. Each new package stays DEVELOPMENT until its own editor save/reopen, Custom Game, live feature, multiplayer and endurance gates pass.
- Each package receives an immutable `CHANGELOG.md` section with date, build ID, package SHA-256, feature summary and exact check evidence. Update [PROGRESS-LEDGER.md](PROGRESS-LEDGER.md) and [ROADMAP-AND-ACCEPTANCE.md](ROADMAP-AND-ACCEPTANCE.md) for each build. Never state an engine test passed without current-build evidence.
- Automated tests prove source/catalog/archive relationships and JASS syntax. They do not prove Warcraft rendering, input dialogs, object instantiation, pathfinding, inventory behavior or network synchronization. Preserve those as explicit human-run acceptance checks.
