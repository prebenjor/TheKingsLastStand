# Heroes and abilities

All selectable heroes start at level 1 and belong to a defending player's ownership. The 25-choice roster preserves the original seventeen and adds eight race-themed heroes; their detailed signatures, company/support recruits and IDs are recorded in [CROWNLANDS-EXPANSION.md](CROWNLANDS-EXPANSION.md). A confirmed choice sets that player's worker and matching race build menu independently. Duplicate hero choices are valid.

## Selection roster

| Race | Hero | Role | Native four-skill set |
|---|---|---|---|
| Human | Paladin | Frontline healer/tank | Holy Light, Divine Shield, Devotion Aura, Resurrection |
| Human | Mountain King | Melee control | Storm Bolt, Thunder Clap, Bash, Avatar |
| Human | Priest | Healer/support | Holy Light, Brilliance Aura, Divine Shield, Resurrection |
| Human | Blood Mage | Ranged area caster | Flame Strike, Banish, Siphon Mana, Phoenix |
| Orc | Blademaster | Melee damage | Wind Walk, Mirror Image, Critical Strike, Bladestorm |
| Orc | Far Seer | Ranged caster/summoner | Chain Lightning, Far Sight, Spirit Wolves, Earthquake |
| Orc | Tauren Chieftain | Frontline control | Shockwave, War Stomp, Endurance Aura, Reincarnation |
| Orc | Shadow Hunter | Healer/utility | Healing Wave, Hex, Serpent Ward, Big Bad Voodoo |
| Night Elf | Demon Hunter | Anti-magic melee | Mana Burn, Immolation, Evasion, Metamorphosis |
| Night Elf | Keeper of the Grove | Nature control/support | Entangling Roots, Grove Awakening, Thorns Aura, Tranquility |
| Night Elf | Priestess of the Moon | Ranged support | Scout, Searing Arrows, Trueshot Aura, Starfall |
| Night Elf | Warden | Mobile area damage | Fan of Knives, Blink, Shadow Strike, Vengeance |
| Undead | Death Knight | Frontline support | Death Coil, Death Pact, Unholy Aura, Animate Dead |
| Undead | Lich | Ranged frost caster | Frost Nova, Frost Armor, Dark Ritual, Death and Decay |
| Undead | Dark Ranger | Ranged control | Silence, Black Arrow, Life Drain, Charm |
| Human | Ilastar | Campaign support caster | Sacred Aura, Sacred Flame - Light's Mercy, Mind Control, Surge of Light |
| Undead | Forsaken Paladin | Frontline purifier | Consecration, Righteous Fury, Sacred Aura, Cleansing Fire |

The custom Human Priest is based on the map's custom hero type and has the four-skill set above. Preserve that identity while verifying its portrait, order, icons, and native object IDs in the installed editor version.

## Per-level primary-stat choices

Every hero's learnable list contains its four native skills and three additional native `+` choices: `KSTR` adds only +3 Strength, `KAGI` adds only +3 Agility, and `KINT` adds only +3 Intelligence. A choice spends the same hero skill point as a normal ability and can be chosen again with a later point. Do not replace the hero's regular four-skill list with these choices, and do not show the former modal stat-allocation dialog. Each choice's learn and extended tooltips must name its one stat; do not reuse Attribute Bonus's all-stats description or list a separate stat progression ladder.

## Hero and native skill rawcodes

These are the IDs currently present in tools/hero_progression.py and the selector source. Validate every ID against the locally extracted supported-edition tables before changing or extending the roster.

| Hero | Hero unit rawcode | Four native ability rawcodes, in selector order |
|---|---|---|
| Paladin | Hpal | AHhb, AHds, AHad, AHre |
| Mountain King | Hmkg | AHtb, AHtc, AHbh, AHav |
| Priest | H000 | AHhb, AHab, AHds, AHre |
| Blood Mage | Hblm | AHfs, AHbn, AHdr, AHpx |
| Blademaster | Obla | AOwk, AOmi, AOcr, AOww |
| Far Seer | Ofar | AOcl, AOfs, AOsf, AOeq |
| Tauren Chieftain | Otch | AOsh, AOws, AOae, AOre |
| Shadow Hunter | Oshd | AOhw, AOhx, AOsw, AOvd |
| Demon Hunter | Edem | AEmb, AEim, AEev, AEme |
| Keeper of the Grove | Ekee | AEer, AEfn, AEah, AEtq |
| Priestess of the Moon | Emoo | AEst, AHfa, AEar, AEsf |
| Warden | Ewar | AEfk, AEbl, AEsh, AEsv |
| Death Knight | Udea | AUdc, AUdp, AUau, AUan |
| Lich | Ulic | AUfn, AUfu, AUdr, AUdd |
| Dark Ranger | Nbrn | ANsi, ANba, ANdr, ANch |
| Ilastar | Hjsm | AHas, AHsf, AHmc, AHsl |
| Forsaken Paladin | Npal | AHcr, ANcp, AHpa, AHcl |

The 17 custom signature ability IDs are AK00 through AK16 in the same order as the table above. Keep new user-defined abilities in a project-owned, collision-checked rawcode range; verify icons and all object fields against the installed editor before packaging. Do not confuse hero object IDs, ability IDs, item IDs, and building IDs.

## Custom signature abilities

Every hero receives one additional Z-key point-target signature spell. Shared values: 700 cast range, 350-area radius, 70 mana, 30-second cooldown. Damage generally equals the listed base plus 20 per hero level. Healing generally equals the listed base plus 15 per hero level. Summons last 25 seconds and scale to 300 + 30 HP and 12 + 2 base damage per hero level. Friendly target selection includes allied races. Signature effects never heal the king or buildings unless separately designed and tested.

| Hero | Spell (custom rawcode) | Current effect data |
|---|---|---|
| Paladin | Dawn Verdict (AK00) | 80 + 20/level area damage; heal allies for 100 + 15/level. |
| Mountain King | Runebreaker (AK01) | 180 + 20/level damage; slow enemies by 20% for 2 seconds. |
| Priest | Sanctuary of Hope (AK02) | Heal allies for 220 + 15/level and restore 60 mana per allied unit. |
| Blood Mage | Phoenix Flare (AK03) | 280 + 20/level area fire damage. |
| Blademaster | Steel Tempest (AK04) | 180 + 20/level area damage; heal self for 150. |
| Far Seer | Stormpack (AK05) | 90 + 20/level damage; summon two spirit wolves. |
| Tauren Chieftain | Ancestral Reckoning (AK06) | 120 + 20/level damage and 120 + 15/level allied healing. |
| Shadow Hunter | Serpent Communion (AK07) | Heal allies for 150 + 15/level; summon two serpent wards. |
| Demon Hunter | Fel Hunger (AK08) | 130 + 20/level damage; drain up to 40 mana from each target with mana and restore the amount drained to the caster. |
| Keeper of the Grove | Grove Awakening (AK09) | Summon three Treants on open ground. No tree target required. |
| Priestess of the Moon | Moonwell Convergence (AK10) | 120 + 20/level damage and 160 + 15/level allied healing. |
| Warden | Umbral Harvest (AK11) | 230 + 20/level area damage; heal self for 150. |
| Death Knight | Soul Covenant (AK12) | 150 + 20/level damage and 180 + 15/level allied healing, including undead allies. |
| Lich | Winter's Grasp (AK13) | 200 + 20/level frost damage; slow enemies by 20% for 2 seconds. |
| Dark Ranger | Black Hunt (AK14) | 100 + 20/level damage; summon two skeletal archers. |
| Ilastar | Ilastar's Last Light (AK15) | 240 + 20/level area damage and 200 + 15/level allied healing. |
| Forsaken Paladin | Cleansing Pyre (AK16) | 200 + 20/level area damage and 150 + 15/level allied healing. |

These effects are the current authored object/runtime values; visual assets, native action behavior, spell targeting and balance still require in-engine verification. The Z ability is the custom signature; it does not replace the familiar four Warcraft skills.

## Extended spell and talent progression

- Hero level cap: 50.
- Four regular hero skills use installed Warcraft ability records. Preserve ranks 1 through each record's declared `levels` count exactly, and preserve the installed unlock level.
- Safely extend only abilities with a registered, installed, nonzero power field in `tools/hero_progression.py`. Each rank beyond the installed maximum adds 10% of the final authored power value; the increase is relative to the authored value, not compounded (for a three-rank ability, ranks 4 and 5 are 110% and 120%). Every other field copies from the final authored rank, including mana cost, cooldown, duration, range, targeting and mechanics.
- The extension table is explicit and keyed by ability rawcode and AbilityData field ID: `AHhb/Hhb1`, `AHad/Had1`, `AHtb/Htb1`, `AHtc/Htc1`, `AHbh/Hbh1+Hbh3`, `AHav/Hav1+Hav2+Hav3`, `AHfs/Hfs1+Hfs3+Hfs6`, `AHbn/Hbn1`, `AHpa/hsa1+hsa2`, `AHas/hsa1+hsa2`, `AHfa/Hfa1`, `AOwk/Owk3`, `AOcr/Ocr2`, `AOww/Oww1`, `AOcl/Ocl1`, `AOsh/Osh1`, `AOws/Wrs1`, `AOae/Oae1+Oae2`, `AOhw/Ocl1`, `AEmb/Emb1`, `AEim/Eim1`, `AEev/Eev1`, `AEer/Eer1`, `AEah/Eah1`, `AEar/Ear1`, `AEfk/Efk1+Efk2`, `AEsh/Esh1+Esh5`, `AEtq/Etq1`, `AEme/Eme5`, `AEsf/Esf1`, `AUdc/Udc1`, `AUau/Uau1+Uau2`, `AUdr/Udp1`, `AUfn/Ufn1`, and `AUdd/Udd1`. These labels were checked against the installed editor's localized AbilityMetaData strings.
- Unregistered abilities remain at their installed rank cap rather than receiving guessed scaling. The runtime advances ranks at ten-level milestones, to rank 5 at most. The custom signature ability system keeps its separate per-hero-level effects.
- Each hero level queues one visible stat investment: +3 Strength, +3 Agility or +3 Intelligence. Every fifth level grants a separate talent choice; Strength adds health and health regeneration, Agility adds attack speed and evasion, and Intelligence adds mana and mana regeneration. The exact effects are listed in [CROWNLANDS-EXPANSION.md](CROWNLANDS-EXPANSION.md).
- Keep hero inventory/equipment through death and revive after 20 seconds at that player's Altar of Kings.

## Race-sensitive spell behavior

- Healing and ally detection must include all allied human, orc, night elf, and undead defenders and their friendly troops.
- Keeper of the Grove and Faelor Briarward have the native tree-targeting `AEfn` ability removed when hero ranks are applied. Their tree-free Grove Awakening/Briarward Stand signature spells provide the Treant summon on open ground, so this roster no longer leaves a dead tree-dependent Force of Nature button on either hero.
- Death Knight abilities must respect their ordinary living/undead target semantics, while the custom Soul Covenant must support the mixed allied party explicitly.
- Summoned signature units need ownership, target orders, cleanup/lifetime, and wave-accounting rules tested in live play.
