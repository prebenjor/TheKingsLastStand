# Racial building access matrix — 2026-10-02

Captured from the saved R2 baseline and the reopened racial repair map through Forge MCP. Rawcodes identify native prerequisites, training, research and upgrade products. A dash means no product in that field; inherited native fields retain their baseline values. This is object evidence, not native gameplay acceptance.

The failure was the replacement of native worker build lists with mixed standard/custom buildings, including twelve entries and overlapping command positions. Native production definitions remained present but several were unreachable. Undead tier-two prerequisites also referenced the Slaughterhouse as a blacksmith; Graveyard is restored.

Installed data supplies field definitions and native inheritance; [Blizzard’s Night Elf building reference](https://classic.battle.net/war3/nightelf/buildingstats.shtml) cross-checks the native roster. Wisps gather lumber from trees without a Lumber Mill. Native town-hall and tower upgrades remain in their original chains.

## Human

Worker `hpea`; standard menu contains 11 buildings plus native Cancel. Expansion worker `rW00` is prototype-only until native acceptance.

| Building | Construction access before → after | Prerequisites | Upgrades | Recruits | Research | Harvesting / utility | Position |
|---|---|---|---|---|---|---|---|
| Town Hall `htow` | available → standard | — | hkee | hpea | Rhpm | native gold/lumber economy | 0,0 |
| Farm `hhou` | available → standard | — | — | — | — | food | 1,0 |
| Barracks `hbar` | available → standard | — | — | hfoo,hrif,hkni | Rhde,Rhan,Rhri,Rhsb | production / service | 2,0 |
| Altar of Kings `h000` | available → standard | — | — | — | — | production / service | 3,0 |
| Lumber Mill `hlum` | absent → standard | — | — | — | Rhac,Rhlh | lumber drop-off | 0,1 |
| Blacksmith `hbla` | available → standard | htow | — | — | Rhme,Rhar,Rhla,Rhra | production / service | 1,1 |
| Workshop `harm` | absent → standard | hkee,hbla | — | hgyr,hmtm,hmtt,hrtt | Rhgb,Rhfl,Rhrt,Rhfc,Rhfs | production / service | 2,1 |
| Arcane Sanctum `hars` | absent → standard | hkee | — | hmpr,hsor,hspt | Rhpt,Rhst,Rhse,Rhss | production / service | 3,1 |
| Gryphon Aviary `hgra` | absent → standard | hkee,hlum | — | hgry,hdhw | Rhhb,Rhcd | production / service | 0,2 |
| Scout Tower `hwtw` | absent → standard | — | hgtw,hctw,hatw | — | — | production / service | 1,2 |
| Arcane Vault `hvlt` | absent → standard | — | — | — | — | production / service | 2,2 |
| Hall of Banners `kH00` | available → expansion (gated) | hbar | — | rU00 | — | production / service | 0,0 |
| Royal Foundry `kF00` | available → expansion (gated) | hbar | — | — | — | production / service | 1,0 |
| Siege Yard `kY00` | available → expansion (gated) | hbar | — | rU01 | — | production / service | 2,0 |
| Guard Tower `h001` | available → expansion (gated) | — | — | — | — | production / service | 3,0 |
| Cannon Tower `h002` | available → expansion (gated) | — | — | — | — | production / service | 0,1 |
| Sanctuary Tower `h003` | available → expansion (gated) | — | — | — | — | production / service | 1,1 |
| Arcane Sanctum `h004` | available → upgrade / legacy | — | — | hmpr,hsor | Rhpt,Rhst | production / service | 2,1 |
| Keep `hkee` | absent → upgrade / legacy | — | hcas | hpea | Rhpm | production / service | 0,2 |

## Orc

Worker `opeo`; standard menu contains 10 buildings plus native Cancel. Expansion worker `rW01` is prototype-only until native acceptance.

| Building | Construction access before → after | Prerequisites | Upgrades | Recruits | Research | Harvesting / utility | Position |
|---|---|---|---|---|---|---|---|
| Great Hall `ogre` | available → standard | — | ostr | opeo | Ropg,Ropm | native gold/lumber economy | 0,0 |
| Burrow `otrb` | available → standard | — | — | — | — | food | 1,0 |
| Barracks `obar` | available → standard | — | — | ogru,ohun,otbk,ocat | Robs,Rotr,Robk,Robf | production / service | 2,0 |
| Orc Hero Shrine `kA01` | available → standard | — | — | — | — | production / service | 3,0 |
| War Mill `ofor` | available → standard | — | — | — | Rome,Roar,Rora,Rosp,Rorb | lumber drop-off | 0,1 |
| Watch Tower `owtw` | absent → standard | ofor | — | — | — | production / service | 1,1 |
| Beastiary `obea` | absent → standard | ostr | — | orai,okod,owyv,otbr | Roen,Rovs,Rwdm,Rolf | production / service | 2,1 |
| Spirit Lodge `osld` | absent → standard | ostr | — | oshm,odoc | Rowd,Rost | production / service | 3,1 |
| Tauren Totem `otto` | absent → standard | ostr | — | otau,ospm | Rows,Rowt | production / service | 0,2 |
| Voodoo Lounge `ovln` | absent → standard | — | — | — | — | production / service | 1,2 |
| Redtusk Banner Hall `kH01` | available → expansion (gated) | obar | — | rU02 | — | production / service | 0,0 |
| Ashen War Forge `kF01` | available → expansion (gated) | obar | — | — | — | production / service | 1,0 |
| War Drummer Lodge `kY01` | available → expansion (gated) | obar | — | rU03 | — | production / service | 2,0 |
| Watch Tower `kT10` | available → expansion (gated) | — | — | — | — | production / service | 3,0 |
| War Drum Tower `kT11` | available → expansion (gated) | — | — | — | — | production / service | 0,1 |
| Spirit Ward `kT12` | available → expansion (gated) | — | — | — | — | production / service | 1,1 |
| Spirit Lodge `kR01` | available → upgrade / legacy | — | — | oshm,odoc | Rowd,Rost | production / service | 2,1 |
| Stronghold `ostr` | absent → upgrade / legacy | obar,ofor,kA01 | ofrt | opeo | Ropg,Ropm | production / service | 0,2 |

## Night Elf

Worker `ewsp`; standard menu contains 10 buildings plus native Cancel. Expansion worker `rW02` is prototype-only until native acceptance.

| Building | Construction access before → after | Prerequisites | Upgrades | Recruits | Research | Harvesting / utility | Position |
|---|---|---|---|---|---|---|---|
| Tree of Life `etol` | available → standard | — | etoa | ewsp | Renb,Repm | native gold/lumber economy | 0,0 |
| Moon Well `emow` | available → standard | — | — | — | — | food | 1,0 |
| Ancient of War `eaom` | available → standard | — | — | earc,esen,ebal | Reib,Remk,Resc,Remg,Repb | production / service | 2,0 |
| Night Elf Hero Shrine `kA02` | available → standard | — | — | — | — | production / service | 3,0 |
| Hunter's Hall `edob` | available → standard | etol | — | — | Resm,Rema,Resw,Rerh,Reuv,Rews | production / service | 0,1 |
| Ancient Protector `etrp` | absent → standard | edob | — | — | — | production / service | 1,1 |
| Ancient of Lore `eaoe` | absent → standard | etoa,edob | — | edry,edoc,emtg | Resi,Redc,Rers,Rehs,Reeb | production / service | 2,1 |
| Ancient of Wind `eaow` | absent → standard | etoa | — | ehip,edot,efdr | Redt,Reec | production / service | 3,1 |
| Chimaera Roost `edos` | absent → standard | etoe | — | echm | Recb | production / service | 0,2 |
| Ancient of Wonders `eden` | absent → standard | — | — | — | — | production / service | 1,2 |
| Moonlit Banner Hall `kH02` | available → expansion (gated) | eaom | — | rU04 | — | production / service | 0,0 |
| Moonbark Runeforge `kF02` | available → expansion (gated) | eaom | — | — | — | production / service | 1,0 |
| Sentinel War Grove `kY02` | available → expansion (gated) | eaom | — | rU05 | — | production / service | 2,0 |
| Ancient Protector `kT20` | available → expansion (gated) | — | — | — | — | production / service | 3,0 |
| Moonfire Spire `kT21` | available → expansion (gated) | — | — | — | — | production / service | 0,1 |
| Moonwell Sentinel `kT22` | available → expansion (gated) | — | — | — | — | production / service | 1,1 |
| Tree of Ages `etoa` | absent → upgrade / legacy | eaom,edob,kA02 | etoe | ewsp | Renb,Repm | production / service | 0,2 |
| Ancient Lore Grove `kR02` | available → upgrade / legacy | — | — | edry,edoc,emtg | Resi,Redc,Rers,Rehs,Reeb | production / service | 2,1 |

## Undead

Worker `uaco`; standard menu contains 11 buildings plus native Cancel. Expansion worker `rW03` is prototype-only until native acceptance.

| Building | Construction access before → after | Prerequisites | Upgrades | Recruits | Research | Harvesting / utility | Position |
|---|---|---|---|---|---|---|---|
| Necropolis `unpl` | available → standard | — | unp1 | uaco | Rupm | native gold/lumber economy | 0,0 |
| Ziggurat `uzig` | available → standard | — | uzg1,uzg2 | — | — | food | 1,0 |
| Crypt `usep` | available → standard | — | — | ugho,ucry,ugar | Ruwb,Rugf,Rusf,Rubu,Ruac | production / service | 2,0 |
| Undead Hero Shrine `kA03` | available → standard | — | — | — | — | production / service | 3,0 |
| Graveyard `ugrv` | absent → standard | — | — | — | Rume,Ruar,Rura,Rucr | lumber drop-off | 0,1 |
| Slaughterhouse `uslh` | available → standard | unp1,ugrv | — | umtw,uabo,uobs | Rupc,Rusp,Ruex | production / service | 1,1 |
| Temple of the Damned `utod` | absent → standard | unp1,ugrv | — | unec,uban | Rune,Ruba,Rusm | production / service | 2,1 |
| Sacrificial Pit `usap` | absent → standard | unp1 | — | — | — | production / service | 3,1 |
| Boneyard `ubon` | absent → standard | unp2 | — | ufro | Rufb | production / service | 0,2 |
| Tomb of Relics `utom` | absent → standard | — | — | — | — | production / service | 1,2 |
| Haunted Gold Mine `ugol` | absent → standard | — | — | — | — | production / service | 2,2 |
| Bone Banner Hall `kH03` | available → expansion (gated) | usep | — | rU06 | — | production / service | 0,0 |
| Wraithforged Smithy `kF03` | available → expansion (gated) | usep | — | — | — | production / service | 1,0 |
| Graveyard of Arms `kY03` | available → expansion (gated) | usep | — | rU07 | — | production / service | 2,0 |
| Ziggurat Tower `kT30` | available → expansion (gated) | — | uzg1,uzg2 | — | — | production / service | 3,0 |
| Frost Tower `kT31` | available → expansion (gated) | — | — | — | — | production / service | 0,1 |
| Soulwell Spire `kT32` | available → expansion (gated) | — | uzg1,uzg2 | — | — | production / service | 1,1 |
| Temple of the Damned `kR03` | available → upgrade / legacy | — | — | unec,uban | Rune,Ruba,Rusm | production / service | 2,1 |
| Halls of the Dead `unp1` | absent → upgrade / legacy | usep,ugrv,kA03 | unp2 | uaco | Rupm | production / service | 0,2 |

## Command card acceptance

Specialist training is at (0,0), hero-company purchases at (3,0); construction pages have explicit row-major positions. Native rally, research, sale stock, Cancel, hotkeys and each complete prerequisite path require engine checks. Foundries retain upgrades/recipes and do not train specialists. Native item-stock button placement is inherited and must be visually tested.
