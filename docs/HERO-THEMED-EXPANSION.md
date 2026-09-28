# Hero-themed armies and Forsaken Kingdom expansion

**Status: approved architecture; initial source implementation added.** The original 40-wave Crownlands story remains intact and is followed by the approved endless campaign crossover. Exact build/package and engine acceptance remain separate gates.

## Design goal

Make each hero choice change how that player's kingdom army develops. Keep one shared Human building tree, while giving each player a distinct recruit, tactical support unit, and building research path tied to their hero. Add official Forsaken Kingdom campaign heroes only where their unit, ability, portrait, and icon records can be verified from the installed Definitive Edition data.

## Campaign records verified locally

The installed edition's `UnitData.slk`, `AbilityData.slk`, and `WorldEditStrings.txt` include these campaign identities:

| Proposed selector entry | Installed unit rawcode | Verified campaign abilities |
|---|---|---|
| Ilastar, Human | `Hjsm` | `AHsf` Light's Mercy; `AHmc` Mind Control; `AHas` Sacred Aura; `AHsl` Surge of Light |
| Ilastar, Undead | `Ujsm` | Installed base object has no `heroAbilList`; audit the campaign-provided skill data and target rules before making it selectable |
| Forsaken Paladin | `Npal` | `ANcp` Righteous Fury; `AHcr` Consecration; `AHcl` Cleansing Fire; `AHpa` Sacred Aura |

Keep the original fifteen choices, duplicate picks, level-3 start, Human workers/buildings, and player ownership rules. Human Ilastar (`Hjsm`) and the Forsaken Paladin (`Npal`) are now included as two additional selectable campaign heroes, with native ability ranks and custom signature abilities generated from the installed Definitive Edition data. Their selector descriptions use the installed ability names. Convert `Npal` into a proper selectable hero record rather than spawning the neutral creep template unchanged if testing confirms its global unit record lacks a required hero property. Add Undead Ilastar only after the campaign-specific ability list is found and audited; the global `Ujsm` record alone is not a complete hero definition.

The user's screenshot names **Aurrrius the Pure**. That exact name was not present in the installed global unit and ability tables checked for this draft; it may be a campaign-map-specific object. Do not fabricate a rawcode or copy a protected map. If the campaign's editor data exposes Aurrrius as an object, add that native record after verifying its portrait, model, abilities, and attribution.

## Approved architecture: Oathbound Companies

Each selected hero unlocks a personal company that only that player's Barracks can train. The company has one clear battlefield role and one signature ability. A new **Hall of Banners** researches the hero's company doctrine and chapter upgrades. A new **Royal Foundry** upgrades company weapons/armor and unlocks the campaign's veteran variants. A new **Siege Yard** trains the matching tactical support unit: a ranged, control, healer, scout, or siege counter chosen to complement the hero rather than duplicate their damage role.

The existing buildings keep their jobs and gain connected, hero-aware options:

- **Barracks:** the hero's signature company, alongside the normal Human army.
- **Hall of Banners:** one company doctrine and three chapter upgrades; effects are owner-specific.
- **Blacksmith / Royal Foundry:** shared Human troop upgrades plus company-specific armor and weapon branches.
- **Workshop / Siege Yard:** the hero's tactical support unit and its counter-siege upgrade.
- **Arcane Sanctum:** hero-matched support research, available to every hero archetype.
- **Altar of Kings:** hero selection, revival, and the campaign hero's correctly named abilities.

All new structures remain buildable within the owner's plot and use the same footprint, refund, resource, and upgrade validation as existing buildings. No new structure or army unit may block the King's Road or gate.

## Current source baseline

The implemented first slice is documented in `COMPANIES-AND-BUILDINGS.md` and generated from `tools/company_catalog.py`:

- Hall of Banners (`kH00`, installed Castle parent `hcas`) grants the selected hero one installed doctrine aura and unlocks only their personal recruit stock in owned Barracks.
- Royal Foundry (`kF00`, installed Blacksmith parent `hbla`) gives that player's current and future company/support recruits +20% maximum HP and +20% base damage, applied once per unit.
- Siege Yard (`kY00`, installed Workshop parent `harm`) stocks the hero-specific support recruit.
- Seventeen selected heroes have distinct custom company and support rawcodes. They inherit native race-appropriate unit models/icons/abilities and receive catalog-defined names, costs, HP, and damage.
- The Altar is preplaced at each base. It does not consume a redundant worker build-card button. The Peasant construction menu has twelve or fewer choices.
- Purchases from a mismatched player's company shop are removed and refunded. Company recruits stay out of the wave enemy group, accounting, and bounty system.

The initial code does not yet include the architecture's planned three chapter researches, multiple weapon/armor branches, or a newly authored active ability for each recruit. Keep those items in the future scope; do not claim they are implemented. The unit catalog, class-to-stock pairing, doctrine aura, foundry upgrade, ownership, and stock purchase all require exact-build Warcraft verification.

## Hero company concepts

Names below are working names. The long-term table includes the Undead Ilastar candidate; its recruit remains gated on the missing campaign-specific skill data. Implemented base damage, health, and prices live in one catalog and remain initial tuning values until recorded playtests.

| Hero | Barracks company | Tactical support | Doctrine identity |
|---|---|---|---|
| Paladin | Oathguard | Dawn Chaplain | Protect the line; nearby allied units recover health |
| Mountain King | Rune-Breakers | Siege Sappers | Heavy impact and anti-armor pressure |
| Priest | Dawnweavers | Beacon Acolyte | Healing and mana recovery |
| Blood Mage | Emberguard | Phoenix Sentry | Area spell pressure and controlled fire |
| Blademaster | Windcutters | Shadow Scout | Flanking and brief evasion |
| Far Seer | Stormcallers | Spirit Wolf | Ranged magic and target marking |
| Tauren Chieftain | Ancestral Guard | War Drummer | Durable frontline and rally aura |
| Shadow Hunter | Serpent Wardens | Field Witch Doctor | Healing, hex, and ward control |
| Demon Hunter | Felbreakers | Warden Seeker | Anti-magic and demon hunting |
| Keeper of the Grove | Thornwatch | Grove Warden | Rooting and tree-line defense |
| Priestess of the Moon | Moonstriders | Starfall Ballista | Precision volleys and night-sky support |
| Warden | Gloomblades | Shadow Trapwright | Ambush, traps, and pursuit |
| Death Knight | Graveguard | Bone Cavalier | Sustain from combat and frontline pressure |
| Lich | Frostbound | Rime Mortar | Slow fields and ranged spell support |
| Dark Ranger | Black Arrow Company | Forsaken Marksman | Attrition, silence, and ranged focus fire |
| Ilastar, Human | Light's Vanguard | Mercy Bearer | Campaign light magic and allied rescue |
| Ilastar, Undead | Duskbound | Soul Lantern | Campaign shadow/light hybrid and control |
| Forsaken Paladin | Argent Revenants | Cleansing Pyre | Consecration, fire, and undead-counterplay |

Company units use current selectable-hero ownership, can be controlled only by their owner, retain their current orders when the owner leaves, and do not count as wave enemies. Their special summons must have explicit expiry and cleanup. Enemy-kill gold follows the personal-killer / King Aldric quarter-bounty rule in `GAMEPLAY-SPEC.md`; company units do not generate gold merely for being summoned.

## Other approaches considered

1. **One Hall and one custom company unit per hero.** Lowest footprint and easiest to tune, but does not deliver the requested new building/unit ecosystem.
2. **Oathbound Companies (recommended).** Three new structures connect the Barracks, Blacksmith, Workshop, and Arcane Sanctum to each hero. Strong hero identity with a controlled, reusable architecture; it requires careful plot-space and 2/4-player balance testing.
3. **Eighteen separate racial/hero building trees.** Maximum visual uniqueness, but it replaces the approved Human kingdom economy, consumes plot space, multiplies object data, and makes multiplayer balance and maintenance much harder.

## Integration and implementation gates

1. Use installed `UnitBalance.slk`, `UnitUI.slk`, `UnitAbilities.slk`, and `UnitWeapons.slk` for stats, models, abilities, portraits, and icons. Keep these tables machine-local.
2. Human Ilastar and the Forsaken Paladin are selectable. Undead Ilastar and Aurrrius remain gated on verified hero/skill records; do not fabricate either identity.
3. The initial company/support objects and three structures are generated from one catalog with collision/object-record regressions.
4. Complete the in-engine proof for worker build cards, structure placement, Hall unlock, matching Barracks/Siege Yard purchases, ability behavior, one-time Foundry upgrades, and ownership/refunds.
5. Implement the remaining chapter upgrades, company gear/armor branches, and further unique unit abilities from the approved design after the current recruitment gate passes.
6. Test actual two-player synchronization first, then three- and four-player setup and full-match progression. Tune only from recorded playtests.
# Current implementation supersedes the original proposal

The approved and current expansion is documented in [CROWNLANDS-EXPANSION.md](CROWNLANDS-EXPANSION.md). It adds eight rather than merely proposing additional heroes, gives race selection matching workers/buildings/companies, places four settlements and optional story sites, and specifies the shared item/rank catalogs. Older exploratory notes in this file are historical ideas, not instructions to restore the level-3 start or Human-only worker rule.

\n
