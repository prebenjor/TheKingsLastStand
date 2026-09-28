# Hero-themed armies and Forsaken Kingdom expansion

**Status: design draft for approval.** This is the proposed next content system for The King's Last Stand. The existing 40-wave design remains in force. The map runtime has not yet been changed for this expansion.

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

## Recommended implementation: Oathbound Companies

Each selected hero unlocks a personal company that only that player's Barracks can train. The company has one clear battlefield role and one signature ability. A new **Hall of Banners** researches the hero's company doctrine and chapter upgrades. A new **Royal Foundry** upgrades company weapons/armor and unlocks the campaign's veteran variants. A new **Siege Yard** trains the matching tactical support unit: a ranged, control, healer, scout, or siege counter chosen to complement the hero rather than duplicate their damage role.

The existing buildings keep their jobs and gain connected, hero-aware options:

- **Barracks:** the hero's signature company, alongside the normal Human army.
- **Hall of Banners:** one company doctrine and three chapter upgrades; effects are owner-specific.
- **Blacksmith / Royal Foundry:** shared Human troop upgrades plus company-specific armor and weapon branches.
- **Workshop / Siege Yard:** the hero's tactical support unit and its counter-siege upgrade.
- **Arcane Sanctum:** hero-matched support research, available to every hero archetype.
- **Altar of Kings:** hero selection, revival, and the campaign hero's correctly named abilities.

All new structures remain buildable within the owner's plot and use the same footprint, refund, resource, and upgrade validation as existing buildings. No new structure or army unit may block the King's Road or gate.

## Hero company concepts

Names below are working names. The long-term table includes the Undead Ilastar candidate; its recruit remains gated on the missing campaign-specific skill data. Final base damage, armor, cost, cooldowns, and rank curves must be generated from one catalog and tuned against recorded playtests.

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

Company units use current selectable-hero ownership, can be controlled only by their owner, retain their current orders when the owner leaves, and do not count as wave enemies. Their special summons must have explicit expiry and cleanup. Enemy-kill gold uses the existing personal split and roster bounty source; company units do not generate gold merely for being summoned.

## Other approaches considered

1. **One Hall and one custom company unit per hero.** Lowest footprint and easiest to tune, but does not deliver the requested new building/unit ecosystem.
2. **Oathbound Companies (recommended).** Three new structures connect the Barracks, Blacksmith, Workshop, and Arcane Sanctum to each hero. Strong hero identity with a controlled, reusable architecture; it requires careful plot-space and 2/4-player balance testing.
3. **Eighteen separate racial/hero building trees.** Maximum visual uniqueness, but it replaces the approved Human kingdom economy, consumes plot space, multiplies object data, and makes multiplayer balance and maintenance much harder.

## Integration and implementation gates

1. Use the extended local installed-data extractor for `UnitBalance.slk`, `UnitUI.slk`, `UnitAbilities.slk`, and `UnitWeapons.slk`, without committing machine-local tables. Resolve hero stats, ability lists, portraits, command icons, model paths, and the worker portrait issue from these records. Human Ilastar and Forsaken Paladin have global hero skill lists; Undead Ilastar does not in the global list and needs campaign-specific skill data.
2. Extend the hero catalog to verified campaign identities; Human Ilastar and the Forsaken Paladin are implemented in the current development source. Preserve all original choices and confirm each added hero's native skill behavior in game.
3. Generate company/support unit object data, prices, training buttons, tooltips, upgrades, and bounty policy from one catalog. Use native Definitive Edition art and avoid rawcode collisions.
4. Add the Hall of Banners, Royal Foundry, and Siege Yard to the Human build menu with validated prerequisites, footprint, costs, refund behavior, and plot-only construction.
5. Add focused regressions for object records, catalogs, unlocks, costs, ownership, wave accounting, and GUI source parity; then package under a new development build ID and add its SHA-256/changelog entry.
6. Verify portraits, training, abilities, upgrade effects, pathing, gold, and no shared control in the editor and a live 2-player session before expanding to four players or recording balance conclusions.
