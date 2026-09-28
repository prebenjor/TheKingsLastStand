# Crownlands expansion: design and implementation contract

This document is the current detailed design for the kingdom expansion. It incorporates the approved race identity, settlement, hero, equipment, story and progression decisions. Read it with [GAME-VISION.md](GAME-VISION.md), [HEROES-AND-ABILITIES.md](HEROES-AND-ABILITIES.md), [COMPANIES-AND-BUILDINGS.md](COMPANIES-AND-BUILDINGS.md), [ITEMS-AND-EQUIPMENT.md](ITEMS-AND-EQUIPMENT.md), and [TECHNICAL-ARCHITECTURE.md](TECHNICAL-ARCHITECTURE.md). Source catalogs live in `tools/town_catalog.py`, `tools/faction_catalog.py`, `tools/hero_catalog.py`, `tools/company_catalog.py`, `tools/equipment_catalog.py`, and `tools/recipes.py`.

## Player promise

Players choose one of 25 heroes. That hero's race independently sets the owner's worker, Altar, Town Hall and build menu. Every player has a personal base and army, while all four allied communities help King Aldric hold the King's Road. Heroes grow from level 1 to a temporary cap of 50. Every level grants a choice to place three stat points; every five levels grants a separate talent choice. An optional four-part town-recovery story can be advanced during live waves without pausing or changing their enemy count.

The product remains a 2–4 player co-op defense RPG: forty waves, bosses on waves 10, 20, 30 and 40, a 50-second ordinary intermission and a 180-second pre-boss intermission. New map content must preserve the gate, clear road, build plots, resource access, King Aldric and the team's ability to reach the invaders.

## Crownlands map and settlements

- Battlefield: 192 × 192 terrain cells (24,576 Warcraft world units square), map bounds ±12,288, playable/camera bounds ±11,520. Terrain, pathing, W3I bounds, camera and minimap must describe the same battlefield.
- Player plots stay at `(-6000,-500)`, `(-3300,-500)`, `(3300,-500)`, `(6000,-500)`. The north-to-south paved King's Road, open central gate, defensive row, castle and southern market remain readable and clear.
- Town centers sit at Human Crownshire `(0,-9000)`, Orc Redtusk Hold `(-9000,0)`, Night Elf Moonbark Glade `(9000,0)`, and Undead Wraithfall `(0,9000)`. Branch roads connect the east and west settlements to the central avenue; town plazas connect to their branch. Keep structures off the clear lane.
- Each town shows its native-race Town Hall, Altar, food building, Barracks, Blacksmith, one watch tower, a named neutral shop and a race-matched quest-giver. The four settlements are allied to Aldric's defenders and use installed Warcraft models.
- Town shops sell the five universally equippable items of their race's theme, plus healing and mana potions. Their item definitions, stats, rarity colors, stock IDs and drops come from the shared item catalog.

### Settlement identity

| Town | Race | Worker | Town Hall / Barracks / Altar | Shop | Story character |
|---|---|---|---|---|---|
| Crownshire | Human | Peasant `hpea` | `htow` / `hbar` / `h000` | Crownshire Provisioner | Crownshire Supplymaster |
| Redtusk Hold | Orc | Peon `opeo` | `ogre` / `obar` / `kA01` | Redtusk Quartermaster | Northwatch Vanguard |
| Moonbark Glade | Night Elf | Wisp `ewsp` | `etol` / `eaow` / `kA02` | Moonbark Curator | Moonbark Warden |
| Wraithfall | Undead | Acolyte `uaco` | `unpl` / `usep` / `kA03` | Wraithfall Broker | Wraithfall Keeper |

## Race identity and player companies

Race is assigned per selected hero and per owner. It must not be inferred from lobby race, another player's hero, or the default map start. Choosing a Human, Orc, Night Elf or Undead hero replaces only that player's starting Town Hall, altar and five workers with the matching faction. In mixed-race matches, each build menu and constructed role stays matched to its owner.

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
| `Efal` | Night Elf Keeper of the Grove `Ekee`; `AEer`, `AEfn`, `AEah`, `AEtq` | `AK22` Briarward Stand — Force of Nature effect; 180 area damage, 100 allied HP healing, 40 allied mana restoration, summons three `efon` treants without needing trees | `kC22` Briarward Guard / `kS22` Thornmender |
| `Uvyr` | Undead Dark Ranger `Nbrn`; `ANsi`, `ANba`, `ANdr`, `ANch` | `AK23` Wraithveil Curse — Fan of Knives effect; 260 area damage, drains up to 40 mana from each enemy hit and transfers drained mana to Veyra | `kC23` Veilbound Wraiths / `kS23` Grave Cantor |
| `Utha` | Undead Death Knight `Udea`; `AUdc`, `AUdp`, `AUau`, `AUan` | `AK24` Bonecrown Guard — Death Coil effect; 120 area damage, 80 allied HP healing, summons three `uske` skeletons | `kC24` Bonecrown Wardens / `kS24` Crypt Acolyte |

Matching recruit models, gold/lumber prices, base health, base damage and banner doctrines are recorded in [COMPANIES-AND-BUILDINGS.md](COMPANIES-AND-BUILDINGS.md) and `tools/company_catalog.py`. Every selector portrait must match the created hero unit. Faelor's nature abilities do not require tree destructables. Dark/Necromantic spells and heals must work with both living and undead defenders, as appropriate.

## Leveling, attributes and safe spell ranks

- The selected hero starts at level 1. Temporary maximum is 50. King Aldric and wave-owned hero enemies retain their separately authored levels.
- On each hero level gained, queue one stat investment. The player selects Strength, Agility or Intelligence; each selection adds +3 to that primary attribute. Queue investments rather than dropping choices when a hero gains multiple levels quickly.
- Grant a separate talent point for every crossed five-level milestone (levels 5, 10, …, 50). A visible dialog offers:
  - **Vanguard / Strength:** +5 Strength, +200 maximum/current health and +2 health regeneration per second per talent.
  - **Skirmisher / Agility:** +5 Agility (therefore native attack-speed growth) and +2 percentage points evasion per talent.
  - **Sage / Intelligence:** +5 Intelligence, +100 maximum/current mana and +2 mana regeneration per second per talent.
- Talent award bookkeeping is per hero owner, preserves points earned across multi-level jumps, and presents the option visibly. Do not spend a point until the player selects an option.
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
| Crownward Foundry Pattern `RCP4` | Aldric's Aegis + Lionroad Mantle | Last King's Oath | 4,500 gold |
| Redtusk Foundry Pattern `RCP5` | Stormscar Bracers + Ashen War Drum | Worldrend Standard | 4,500 gold |
| Moonbark Foundry Pattern `RCP6` | Duskwatch Longbow + Starleaf Quiver | Silvermoon Vigil | 4,500 gold |
| Wraith Foundry Pattern `RCP7` | Soulreaper's Fang + Wraithsilk Cape | Night's Covenant | 4,500 gold |

### Native item object and equipment-slot IDs

Each custom item object uses the listed native parent for its installed icon/art and click behavior. Generated per-item stat abilities apply the catalog bonuses while equipped; `tools/equipment_catalog.py` owns the amounts and ability records. Rawcodes are case-sensitive. Purchase prices are personal gold; each racial settlement stocks its own five themed items.

| Race | Rarity item | Item rawcode / native parent | Slot | Price | Stat ability rawcodes |
|---|---|---|---|---:|---|
| Human | Common Watchman’s Token | `I23C` / `elmt` | Trinket | 150 | `A03C`, `A13C` |
| Human | Uncommon Lionroad Mantle | `I23G` / `emoh` | Chest | 400 | `A03G`, `A13G` |
| Human | Rare Aldric’s Aegis | `I23K` / `eosc` | Offhand | 1,000 | `A03K`, `A13K` |
| Human | Epic Crownward Pennant | `I23O` / `ebdf` | Trinket | 2,500 | `A03O`, `A13O` |
| Human | Legendary Last King’s Oath | `I23S` / `erdr` | Ring | 6,000 | `A03S`, `A13S`, `A23S` |
| Orc | Common Redtusk Fetish | `I23D` / `elmt` | Trinket | 150 | `A03D`, `A13D` |
| Orc | Uncommon Ashen War Drum | `I23H` / `etkj` | Trinket | 400 | `A03H`, `A13H` |
| Orc | Rare Stormscar Bracers | `I23L` / `eggn` | Gloves | 1,000 | `A03L`, `A13L` |
| Orc | Epic Grudgebreaker | `I23P` / `efpb` | Primary | 3,750 | `A03P`, `A13P` |
| Orc | Legendary Worldrend Standard | `I23T` / `ehls` | Offhand | 6,000 | `A03T`, `A13T` |
| Night Elf | Common Moonbark Charm | `I23E` / `ebdf` | Trinket | 150 | `A03E`, `A13E` |
| Night Elf | Uncommon Starleaf Quiver | `I23I` / `epsb` | Primary | 600 | `A03I`, `A13I` |
| Night Elf | Rare Duskwatch Longbow | `I23M` / `epsb` | Primary | 1,500 | `A03M`, `A13M` |
| Night Elf | Epic Briarheart Mantle | `I23Q` / `emoh` | Chest | 2,500 | `A03Q`, `A13Q` |
| Night Elf | Legendary Silvermoon Vigil | `I23U` / `ejjr` | Ring | 6,000 | `A03U`, `A13U` |
| Undead | Common Crypt-Iron Band | `I23F` / `ecav` | Ring | 150 | `A03F`, `A13F` |
| Undead | Uncommon Wraithsilk Cape | `I23J` / `edsm` | Chest | 400 | `A03J`, `A13J` |
| Undead | Rare Soulreaper’s Fang | `I23N` / `epbs` | Primary | 1,500 | `A03N`, `A13N` |
| Undead | Epic Mourning Reliquary | `I23R` / `eege` | Trinket | 2,500 | `A03R`, `A13R` |
| Undead | Legendary Night’s Covenant | `I23V` / `ehls` | Offhand | 6,000 | `A03V`, `A13V`, `A23V` |

Recipes consume components only when crafting succeeds. Failed craft attempts preserve every component and refund the full recipe fee. Drops use the same catalog: ordinary gear chance is 3% distributed across rarities; bosses use 50%, with higher-tier weights. Potions roll independently (4% ordinary enemy, 18% boss). Killer owns drops; story rewards are bound to contributors.

## Build, evidence and maintenance

- Edit modular files in `source/` and deterministic generators/catalogs in `tools/`. `tools/pipeline.py` is the explicit module order. `source/war3map.j` and `build/` outputs are generated and must not be hand-edited.
- Build only with `python -B tools/build_map.py`. Keep one current map in `dist/`, named `<build-id>-Development.w3m`; archive the previous development artifact under `backups/development-builds/`. Do not create ad hoc map copies.
- The earlier user-reported Test Map remains a **pass for its own build ID**. It does not prove a later package. Each new package stays DEVELOPMENT until its own editor save/reopen, Custom Game, live feature, multiplayer and endurance gates pass.
- Each package receives an immutable `CHANGELOG.md` section with date, build ID, package SHA-256, feature summary and exact check evidence. Update [PROGRESS-LEDGER.md](PROGRESS-LEDGER.md) and [ROADMAP-AND-ACCEPTANCE.md](ROADMAP-AND-ACCEPTANCE.md) for each build. Never state an engine test passed without current-build evidence.
- Automated tests prove source/catalog/archive relationships and JASS syntax. They do not prove Warcraft rendering, input dialogs, object instantiation, pathfinding, inventory behavior or network synchronization. Preserve those as explicit human-run acceptance checks.
