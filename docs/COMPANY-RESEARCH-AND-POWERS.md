# Company powers and research

Generated from `tools/company_catalog.py`. These are current source values; Warcraft command-card rendering, pathing, native item purchase timing and multiplayer effects require exact-build acceptance.

## Authored recruit powers

Each power is an installed Channel (`ANcl`) clone: point target, 600 cast range, 250 effect radius, 40 mana, 20-second cooldown. Recruits have 180 initial/maximum mana and 1 native mana regeneration. Damage targets enemies; healing/mana target friendly living troops of any race, excluding structures and King Aldric. Optional slow is 20% for 2 seconds. Chapter research adds 15% potency per rank; Arcane adds 25% for supports, additively. Manual casts are required.

| Hero | Recruit / rawcode | Installed parent | Gold / lumber | Base HP / damage | Power / rawcode | Damage / heal / mana | Slow |
|---|---|---|---:|---:|---|---:|---|
| Paladin | Oathguard / `kC00` | `hfoo` | 260 / 70 | 900 / 34 | Dawn Ward / `Kc00` | 80 / 80 / 0 | No |
| Paladin | Dawn Chaplain / `kS00` | `hmpr` | 320 / 100 | 650 / 22 | Dawn Chaplain Accord / `Ks00` | 40 / 120 / 20 | No |
| Mountain King | Rune-Breakers / `kC01` | `hfoo` | 280 / 85 | 1000 / 40 | Rune Impact / `Kc01` | 140 / 0 / 0 | Yes |
| Mountain King | Siege Sappers / `kS01` | `hmtm` | 360 / 120 | 680 / 28 | Siege Sappers Accord / `Ks01` | 70 / 120 / 20 | Yes |
| Priest | Dawnweavers / `kC02` | `hmpr` | 240 / 75 | 720 / 23 | Dawn Renewal / `Kc02` | 30 / 140 / 30 | No |
| Priest | Beacon Acolyte / `kS02` | `hmpr` | 300 / 100 | 620 / 18 | Beacon Acolyte Accord / `Ks02` | 15 / 140 / 30 | No |
| Blood Mage | Emberguard / `kC03` | `hsor` | 270 / 80 | 760 / 30 | Emberburst / `Kc03` | 160 / 0 / 0 | No |
| Blood Mage | Phoenix Sentry / `kS03` | `hgry` | 400 / 140 | 620 / 34 | Phoenix Sentry Accord / `Ks03` | 80 / 120 / 20 | No |
| Blademaster | Windcutters / `kC04` | `ogru` | 270 / 80 | 850 / 38 | Windcut / `Kc04` | 150 / 0 / 0 | No |
| Blademaster | Shadow Scout / `kS04` | `orai` | 340 / 110 | 650 / 30 | Shadow Scout Accord / `Ks04` | 75 / 120 / 20 | No |
| Far Seer | Stormcallers / `kC05` | `oshm` | 260 / 85 | 750 / 25 | Stormcall / `Kc05` | 120 / 0 / 30 | Yes |
| Far Seer | Spirit Wolf / `kS05` | `orai` | 350 / 120 | 700 / 33 | Spirit Wolf Accord / `Ks05` | 60 / 120 / 30 | Yes |
| Tauren Chieftain | Ancestral Guard / `kC06` | `otau` | 320 / 110 | 1250 / 44 | Ancestor Pulse / `Kc06` | 90 / 100 / 0 | No |
| Tauren Chieftain | War Drummer / `kS06` | `okod` | 360 / 130 | 850 / 25 | War Drummer Accord / `Ks06` | 45 / 120 / 20 | No |
| Shadow Hunter | Serpent Wardens / `kC07` | `ohun` | 250 / 80 | 780 / 31 | Serpent Venom / `Kc07` | 130 / 0 / 0 | Yes |
| Shadow Hunter | Field Witch Doctor / `kS07` | `oshm` | 360 / 120 | 700 / 24 | Field Witch Doctor Accord / `Ks07` | 65 / 120 / 20 | Yes |
| Demon Hunter | Felbreakers / `kC08` | `esen` | 280 / 90 | 850 / 38 | Fel Rupture / `Kc08` | 150 / 0 / 0 | No |
| Demon Hunter | Warden Seeker / `kS08` | `edry` | 360 / 120 | 720 / 30 | Warden Seeker Accord / `Ks08` | 75 / 120 / 20 | No |
| Keeper of the Grove | Thornwatch / `kC09` | `edry` | 250 / 90 | 760 / 25 | Verdant Ward / `Kc09` | 60 / 120 / 0 | No |
| Keeper of the Grove | Grove Warden / `kS09` | `edry` | 380 / 130 | 800 / 28 | Grove Warden Accord / `Ks09` | 30 / 120 / 20 | No |
| Priestess of the Moon | Moonstriders / `kC10` | `esen` | 270 / 85 | 780 / 35 | Moon Volley / `Kc10` | 150 / 0 / 0 | No |
| Priestess of the Moon | Starfall Ballista / `kS10` | `ebal` | 420 / 150 | 700 / 38 | Starfall Ballista Accord / `Ks10` | 75 / 120 / 20 | No |
| Warden | Gloomblades / `kC11` | `esen` | 270 / 85 | 800 / 40 | Gloomstrike / `Kc11` | 150 / 0 / 0 | Yes |
| Warden | Shadow Trapwright / `kS11` | `efdr` | 400 / 140 | 700 / 30 | Shadow Trapwright Accord / `Ks11` | 75 / 120 / 20 | Yes |
| Death Knight | Graveguard / `kC12` | `ugho` | 280 / 90 | 900 / 36 | Grave Covenant / `Kc12` | 90 / 100 / 0 | No |
| Death Knight | Bone Cavalier / `kS12` | `uabo` | 430 / 150 | 1050 / 42 | Bone Cavalier Accord / `Ks12` | 45 / 120 / 20 | No |
| Lich | Frostbound / `kC13` | `ucry` | 300 / 100 | 850 / 34 | Rime Burst / `Kc13` | 130 / 0 / 0 | Yes |
| Lich | Rime Mortar / `kS13` | `uban` | 430 / 160 | 740 / 36 | Rime Mortar Accord / `Ks13` | 65 / 120 / 20 | Yes |
| Dark Ranger | Black Arrow Company / `kC14` | `nska` | 270 / 90 | 760 / 35 | Black Volley / `Kc14` | 150 / 0 / 0 | No |
| Dark Ranger | Forsaken Marksman / `kS14` | `nska` | 390 / 135 | 760 / 38 | Forsaken Marksman Accord / `Ks14` | 75 / 120 / 20 | No |
| Ilastar, Human | Light’s Vanguard / `kC15` | `hfoo` | 300 / 90 | 920 / 36 | Mercy Flare / `Kc15` | 70 / 120 / 30 | No |
| Ilastar, Human | Mercy Bearer / `kS15` | `hmpr` | 380 / 120 | 720 / 26 | Mercy Bearer Accord / `Ks15` | 35 / 120 / 30 | No |
| Forsaken Paladin | Argent Revenants / `kC16` | `ugho` | 310 / 100 | 1000 / 39 | Cleansing Brand / `Kc16` | 120 / 80 / 0 | No |
| Forsaken Paladin | Cleansing Pyre / `kS16` | `uban` | 400 / 135 | 740 / 30 | Cleansing Pyre Accord / `Ks16` | 60 / 120 / 20 | No |
| Aveline Ashford | Lionguard / `kC17` | `hfoo` | 290 / 80 | 980 / 36 | Crownward Pulse / `Kc17` | 80 / 120 / 0 | No |
| Aveline Ashford | Banner Chaplain / `kS17` | `hmpr` | 340 / 110 | 700 / 24 | Banner Chaplain Accord / `Ks17` | 40 / 120 / 20 | No |
| Toren Flintlock | Powderwrights / `kC18` | `hmtm` | 300 / 100 | 900 / 42 | Powderburst / `Kc18` | 160 / 0 / 0 | Yes |
| Toren Flintlock | Field Engineer / `kS18` | `hmpr` | 380 / 140 | 680 / 32 | Field Engineer Accord / `Ks18` | 80 / 120 / 20 | Yes |
| Korgal Redtusk | Redtusk Breakers / `kC19` | `otau` | 340 / 120 | 1320 / 48 | Bloodfire Break / `Kc19` | 160 / 0 / 0 | No |
| Korgal Redtusk | Bloodfire Drummer / `kS19` | `oshm` | 390 / 140 | 900 / 30 | Bloodfire Drummer Accord / `Ks19` | 80 / 120 / 20 | No |
| Morgra Ashcaller | Ashcallers / `kC20` | `oshm` | 290 / 95 | 820 / 34 | Ashen Communion / `Kc20` | 80 / 100 / 30 | No |
| Morgra Ashcaller | Spirit Guide / `kS20` | `orai` | 390 / 140 | 760 / 28 | Spirit Guide Accord / `Ks20` | 40 / 120 / 30 | No |
| Selyra Moonlance | Moonlance Sentinels / `kC21` | `esen` | 300 / 100 | 900 / 40 | Moonlance Salvo / `Kc21` | 160 / 0 / 0 | No |
| Selyra Moonlance | Moonwell Keeper / `kS21` | `edry` | 430 / 150 | 780 / 34 | Moonwell Keeper Accord / `Ks21` | 80 / 120 / 20 | No |
| Faelor Briarward | Briarward Guard / `kC22` | `edry` | 280 / 100 | 850 / 31 | Briar Renewal / `Kc22` | 80 / 120 / 0 | Yes |
| Faelor Briarward | Thornmender / `kS22` | `edry` | 410 / 145 | 840 / 29 | Thornmender Accord / `Ks22` | 40 / 120 / 20 | Yes |
| Veyra Wraithveil | Veilbound Wraiths / `kC23` | `uban` | 300 / 100 | 820 / 38 | Veil Dirge / `Kc23` | 100 / 80 / 30 | No |
| Veyra Wraithveil | Grave Cantor / `kS23` | `ucry` | 420 / 160 | 780 / 40 | Grave Cantor Accord / `Ks23` | 50 / 120 / 30 | No |
| Tharos Bonecrown | Bonecrown Wardens / `kC24` | `ugho` | 330 / 110 | 1150 / 46 | Boneward Pulse / `Kc24` | 100 / 100 / 0 | No |
| Tharos Bonecrown | Crypt Acolyte / `kS24` | `ucry` | 430 / 160 | 1050 / 39 | Crypt Acolyte Accord / `Ks24` | 50 / 120 / 20 | No |

## Personal research services

Buy services at your completed matching building with your living selected hero within 700 range. Native purchase charges the displayed gold/lumber once. Wrong ownership, invalid progression or an obsolete rank refunds both costs. Service items are removed; ranks apply to existing and future recruits. Completing a Foundry grants +20% base health/damage once, independently of these branches.

| Service | Rawcode | Building role | Rank | Gold / lumber | Effect / prerequisite |
|---|---|---|---:|---:|---|
| Chapter Research 1 | `KC01` | hall | 1 | 350 / 100 | +5% base health and damage; +15% company ability potency. Applies to existing and future company/support recruits. Unlock: story chapter 1 or wave 10. |
| Chapter Research 2 | `KC02` | hall | 2 | 700 / 200 | +5% base health and damage; +15% company ability potency. Applies to existing and future company/support recruits. Unlock: story chapter 2 or wave 20. |
| Chapter Research 3 | `KC03` | hall | 3 | 1400 / 350 | +5% base health and damage; +15% company ability potency. Applies to existing and future company/support recruits. Unlock: story chapter 3 or wave 30. |
| Weapon Research 1 | `KW01` | foundry | 1 | 350 / 100 | +10% base damage. Applies to existing and future company/support recruits. Requires the previous rank. |
| Weapon Research 2 | `KW02` | foundry | 2 | 700 / 200 | +10% base damage. Applies to existing and future company/support recruits. Requires the previous rank. |
| Weapon Research 3 | `KW03` | foundry | 3 | 1400 / 350 | +10% base damage. Applies to existing and future company/support recruits. Requires the previous rank. |
| Armor Research 1 | `KA01` | foundry | 1 | 350 / 100 | +10% base health and +2 armor. Applies to existing and future company/support recruits. Requires the previous rank. |
| Armor Research 2 | `KA02` | foundry | 2 | 700 / 200 | +10% base health and +2 armor. Applies to existing and future company/support recruits. Requires the previous rank. |
| Armor Research 3 | `KA03` | foundry | 3 | 1400 / 350 | +10% base health and +2 armor. Applies to existing and future company/support recruits. Requires the previous rank. |
| Counter Siege Research | `KS01` | siege_yard | 1 | 650 / 200 | Support attacks deal 50% extra damage to Meat Wagons, Blood Elf Siege Wagons, Dragon Turtles and enemy structures. Applies only to your company support units. |
| Arcane Research | `KT01` | arcane | 1 | 650 / 200 | Support active abilities gain 25% damage, healing and mana restoration. Applies only to your company support units. |

## Bookkeeping and siege targets

Company totals use additive deltas against the catalog base, preserving unrelated native effects. Fresh native stock purchases clear recycled handle bookkeeping before applying bonuses. Construction starts clear stale completion flags. Ordinary death retains totals so resurrection does not stack bonuses; later research adds only its new delta.

Counter-Siege affects positive attack damage from the owner’s matching support against enemy structures or these actual invasion siege roles: `umtw`, `hbew`, `nhyc`. It does not amplify spells or ordinary infantry damage.

Regenerate with `python -X utf8 -B tools/render_company_catalog.py`.
