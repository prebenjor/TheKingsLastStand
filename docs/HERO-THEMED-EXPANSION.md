# Hero-themed armies and Forsaken Kingdom expansion

**Status: historical exploration, superseded by the current four-race plan.** The authoritative roster and gameplay rules are in [GAMEPLAY-SPEC.md](GAMEPLAY-SPEC.md), [CROWNLANDS-EXPANSION.md](CROWNLANDS-EXPANSION.md), and [HEROES-AND-ABILITIES.md](HEROES-AND-ABILITIES.md). Keep the original 40-wave Crownlands story followed by the approved endless campaign crossover; exact build/package and engine acceptance remain separate gates.

The current roster has 25 selectable heroes: the original fifteen, Human Ilastar, the Forsaken Paladin, and eight original race-themed heroes. Heroes start at level 1 and cap at 50. Confirming a hero independently selects that player's Human, Orc, Night Elf, or Undead worker and matching building/recruit tree. The older Human-only army and level-3-start proposal below is retained only as design history and must not be reintroduced.

## Design goal

Make each hero choice change both that player's race-flavored kingdom army and their personal company. Use shared role rules and catalog-backed costs while matching workers, structures, recruits, and support units to Human, Orc, Night Elf, or Undead identity. Add official Forsaken Kingdom campaign heroes only where their unit, ability, portrait, and icon records can be verified from the installed Definitive Edition data.

## Campaign records verified locally

The installed edition's `UnitData.slk`, `AbilityData.slk`, and `WorldEditStrings.txt` include these campaign identities:

| Proposed selector entry | Installed unit rawcode | Verified campaign abilities |
|---|---|---|
| Ilastar, Human | `Hjsm` | `AHsf` Light's Mercy; `AHmc` Mind Control; `AHas` Sacred Aura; `AHsl` Surge of Light |
| Ilastar, Undead | `Ujsm` | Installed base object has no `heroAbilList`; audit the campaign-provided skill data and target rules before making it selectable |
| Forsaken Paladin | `Npal` | `ANcp` Righteous Fury; `AHcr` Consecration; `AHcl` Cleansing Fire; `AHpa` Sacred Aura |

**Historical proposal, superseded:** preserve fifteen choices, start at level 3, and use Human workers/buildings for everyone. The current design instead has 25 choices, level-1 starts, and independently race-matched workers/buildings/companies. Human Ilastar (`Hjsm`) and the Forsaken Paladin (`Npal`) are selectable campaign heroes, with native ability ranks and signature abilities generated from installed Definitive Edition data. Their selector descriptions use installed ability names. The global Undead Ilastar (`Ujsm`) record lacks a verified campaign skill list, so Undead Ilastar is a research candidate and is not one of the 25 selectable heroes. Do not invent its rawcode or kit.

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
- All 25 selected heroes have distinct custom company and support rawcodes. They inherit native race-appropriate unit models/icons/abilities and receive catalog-defined names, costs, HP, and damage.
- The Altar is preplaced at each base. It does not consume a redundant worker build-card button. The Peasant construction menu has twelve or fewer choices.
- Purchases from a mismatched player's company shop are removed and refunded. Company recruits stay out of the wave enemy group, accounting, and bounty system.

The September 30 audit completion adds three Company Chapter researches, three weapon and three armor ranks, support Counter-Siege and Arcane research, and an authored active for all 50 company/support recruits. Exact values and rawcodes are generated in [COMPANY-RESEARCH-AND-POWERS.md](COMPANY-RESEARCH-AND-POWERS.md). These are implemented in source; engine acceptance remains pending. The unit catalog, class-to-stock pairing, doctrine aura, foundry upgrade, ownership, and stock purchase all require exact-build Warcraft verification.

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
| Ilastar, Undead (research candidate; not selectable) | Duskbound (proposal only) | Soul Lantern (proposal only) | Campaign shadow/light hybrid and control |
| Forsaken Paladin | Argent Revenants | Cleansing Pyre | Consecration, fire, and undead-counterplay |

Company units use current selectable-hero ownership, can be controlled only by their owner, retain their current orders when the owner leaves, and do not count as wave enemies. Their special summons must have explicit expiry and cleanup. Enemy-kill gold follows the personal-killer / King Aldric quarter-bounty rule in `GAMEPLAY-SPEC.md`; company units do not generate gold merely for being summoned.

## Other approaches considered

1. **One Hall and one custom company unit per hero.** Lowest footprint and easiest to tune, but does not deliver the requested building/unit ecosystem.
2. **Four-race Oathbound Companies (current design).** Hero selection determines race-specific workers/buildings/units; the Hall, Foundry, and Siege Yard connect each hero to their company. Shared catalog rules keep roles and costs aligned while preserving faction identity. This requires careful plot-space and 2/4-player balance testing.
3. **A complete classic tech tree for every race and hero.** Maximum breadth, but it consumes plot space, multiplies object data, and makes multiplayer balance and maintenance much harder. The current request is for the specified custom buildings, workers, companies, towers, support units and upgrades, not every classic tech-tree building.

## Integration and implementation gates

1. Use installed `UnitBalance.slk`, `UnitUI.slk`, `UnitAbilities.slk`, and `UnitWeapons.slk` for stats, models, abilities, portraits, and icons. Keep these tables machine-local.
2. Human Ilastar and the Forsaken Paladin are selectable. Undead Ilastar and Aurrrius remain gated on verified hero/skill records; do not fabricate either identity.
3. The initial company/support objects and three structures are generated from one catalog with collision/object-record regressions.
4. Complete the in-engine proof for worker build cards, structure placement, Hall unlock, matching Barracks/Siege Yard purchases, ability behavior, one-time Foundry upgrades, and ownership/refunds.
5. Verify the implemented chapter, weapon/armor and support research branches and all 50 unit powers against the current build.
6. Test actual two-player synchronization first, then three- and four-player setup and full-match progression. Tune only from recorded playtests.
# Current implementation supersedes the original proposal

The approved and current expansion is documented in [CROWNLANDS-EXPANSION.md](CROWNLANDS-EXPANSION.md). It adds eight rather than merely proposing additional heroes, gives race selection matching workers/buildings/companies, places four settlements and optional story sites, and specifies the shared item/rank catalogs. Older exploratory notes in this file are historical ideas, not instructions to restore the level-3 start or Human-only worker rule.

\n
