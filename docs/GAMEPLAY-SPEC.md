# Gameplay specification

This document preserves the approved gameplay target. Code presence is tracked separately from live verification in ROADMAP-AND-ACCEPTANCE.md.

## Match state and opening

Authoritative match states:

    INITIALIZING → HERO_SELECTION → PREPARATION → WAVE_ACTIVE → WON or LOST

- Create gameplay only for occupied player slots. Diagnostic packages may run solo; release packages support 2–4 defenders.
- Defenders are allied and share vision. Shared unit control is disabled. Undead invaders have a distinct hostile owner.
- Each active player sees a 45-second hero selection. The fallback for a player who does not confirm is Paladin.
- Players choose one of seventeen hero previews: the original fifteen plus Human Ilastar and the Forsaken Paladin verified in installed Definitive Edition data. Duplicate choices are allowed. Create the selected hero once; do not leave or replace a usable placeholder hero.
- After every active player selects, start the initial 45-second preparation period. Beginning troops stay held until the selection phase ends.
- Normal cleared-wave breaks are 50 seconds. Breaks before waves 10, 20, 30, and 40 are 180 seconds. The 50-second ordinary break supersedes the earlier 90-second decision; the longer boss break remains.
- Terminal victory/defeat stops spawns, timers, damage, rewards, and revival. King death takes precedence if it resolves in the same step as final-boss death.
- If a player leaves, remove their control and stop scaling them into future waves. Do not transfer their living army to another player; let its current orders continue.

## Player ownership and economy

- Each player controls their hero, Human workers, trained units, and structures.
- The team shares the battlefield, neutral vendors, enemy waves, boss encounter, king, and outcome; players do not share unit control or personal resources.
- Workers use standard Warcraft mine and lumber gathering. Put an accessible mine and harvestable tree grove by every active plot. Trees must not block routes to the mine, Altar, buildable pad, or road.
- A defender player's kill pays the full role bounty to that killer's owner only. A kill credited to King Aldric pays 25% of the bounty to each active defender. Show each recipient the exact amount credited. Boss participation gold and gear remain personal rewards for every active participant.
- Every active defender hero within 1,200 world units of a tracked enemy's death receives the full Warcraft unit-level XP award. The same full value is applied to each nearby hero; it is not divided. Hero race and current life state do not filter the recipients. Native shared/kill XP is disabled in map data so the custom award cannot split or double-count; verify dead-hero XP behavior in the engine.
- Boss gear is personal. If the inventory cannot accept the reward, preserve an entitlement or safely place a retrievable personal item; never destroy it or make it public/lootable by another defender.
- The market is one shared set of neutral shops accessible to all players. A purchase, tome, recipe, or castle contribution charges the buyer's personal resources.

## Hero growth

- Start player heroes at level 3. Cap them at level 100.
- Each hero retains four recognizable native Warcraft skills. Each can reach ten ranks: preserve all installed native rank data, then conservatively extend the values beyond the maximum installed rank.
- Keep the original skill unlock levels. Once a spell is unlocked, the current extension adds one rank every ten hero levels, capped at rank 10. At level 100 all four skills have reached rank 10 when their native unlock permits it.
- Each of the 17 heroes also has one automatically granted Z signature ability. The custom spell scales with hero level and uses a 700 cast range, 350 effect radius, 70 mana, and 30-second cooldown.
- Hero talents are selected by chat shortcut in the diagnostic: Power (+12 attack damage), Vitality (+300 maximum health), or Wisdom (+10 intelligence) per point. Award talent points at five-level milestones. Count every milestone crossed when a hero gains multiple levels at once. Replace the diagnostic-only shortcuts with visible controls for release.
- Revive a dead hero after 20 seconds at their own Altar of Kings, preserving equipment and backpack contents.
- Support abilities and ally targeting must work across all allied hero races. Keeper's custom Grove Awakening summons Treants on open ground; it must not require harvestable trees. Death Knight effects must not assume every target is living/undead incorrectly.

## Base building

The four plots are independent, free-placement Human kingdom construction zones beside the central road. Each plot has enough area for a Town Hall, resource access, training/support buildings, three tower roles, and late-wave reinforcement without overlapping the lane.

Required building families:

- Town Hall — base anchor, worker production, and economic progression.
- Farm — food capacity for recruited armies.
- Barracks — frontline melee recruitment.
- Altar of Kings — hero selection/revival identity. Do not represent it as a Chapel or train a Sorceress from it.
- Workshop — siege and specialized late-game units.
- Blacksmith — defensive and army upgrades.
- Three tower roles — distinct anti-swarm, anti-armor, and support/utility coverage.
- Repairable and upgradeable structures where the building role supports it.

Construction rules:

- Enforce ownership and validate the full footprint inside the owning player's plot.
- Reject a building or upgrade whose footprint intersects the central unbuildable road, leaves the owner's plot, overlaps prohibited structures, or blocks the only enemy route.
- An invalid placement is completely refunded and leaves no abandoned construction site.
- Place tower frontage facing the road. Prove coverage of the road before scenery decoration.
- Confirm worker pathing to the mine and trees and enemy pathing from northern spawns through the open gate to King Aldric before adding decorative blocking objects.
- The north wall must have the requested long runs on both sides and a permanent central opening. It is visual fortification, not a closed AI path.

## King Aldric and his castle

King Aldric is the shared survival objective at the central castle. His castle is an invulnerable native shop-style interaction building with readable native command-card buttons for healing and royal upgrades; do not put long overflowing prose in a framed dialog.

- Starting maximum health: 15,000; base damage: 80.
- Heal: 150 personal gold + 50 personal lumber; restore up to 2,000 HP. Full health is rejected and refunded.
- Five one-at-a-time royal tiers. Cost is 400 + 200 × existing tier gold and 150 lumber. Each gives +4,000 maximum/current HP and +30 damage.
- Reject maximum tier, stale tier price, dead king, invalid owner, insufficient resources, and full-health repair without charge.
- Contribution must be atomic: either apply the complete health/tier/damage change and debit the exact personal cost, or refund everything.
- King health/tier must appear in the persistent top HUD.

## Waves, enemies, and difficulty

- Exactly forty waves in four chapters. Chapter roles accumulate as described in WAVES-AND-BOSSES.md.
- Every spawn and summon joins the tracked enemy set exactly once. Death, removal, debug cleanup, and boss summons must decrement the live count once.
- Enemy movement targets the king. Issue pathing recovery only when an enemy has no valid order or is demonstrably stuck; do not override ordinary combat repeatedly.
- Every tracked enemy death pays the killer's defender owner one role-based bounty, plus the current wave number for normal units; no kill gold is shared. Bosses pay `100 + 5 × wave` for the killing defender. If King Aldric makes the killing blow, every active defender gets 25% of the bounty. See `WAVES-AND-BOSSES.md` for starting role values; tune from recorded matches.
- Every active defender hero within 1,200 world units receives the full kill XP value individually. Do not divide XP among heroes. The runtime computes the Warcraft normal-unit sequence and hero-kill table, disables native XP grants, and applies the value to each nearby hero regardless of race or life state.
- Keep enemy types varied: undead foot soldiers, ranged support, durable elites, necromancers, siege attackers, demons, and escorts. The user's feedback specifically asks for a more visible undead/demon mix than repeated identical ghouls.
- Recalculate scaling for later waves after a defender departs.
- Show the current wave and chapter, prep countdown, enemy count, king health/tier, personal revival countdown, and persistent boss warnings.
- Boss warning remains visible through the telegraph and action. Boss summons are tracked as enemies.

## Recovery, shops, and progression spaces

- King's Restoring Spring is below/south-west of the castle and outside the road. Within 450 range, restore 1% of maximum health and 1% of maximum mana to active living defender heroes every second, capped at their maximums. This is quiet regeneration: no healing effect, floating text, or per-tick notification.
- Six quality vendors (Common/Quartermaster, Uncommon/Veteran, Rare/Master Forge, Epic/Runic Reliquary, Legendary/Royal Vault, and Field Apothecary) are visible in the southern market. The implementation has separate shop objects for the five gear tiers' Arms & Armor and Apparel & Relics categories. Sage's Archive sits next to the Apothecary and sells personal permanent Strength/Agility/Intelligence tomes.
- Gold alone gates equipment quality; all shop tiers are available from the beginning.
- A shop must use an actual clickable item stock/window with icon, item identity, price, slot, stats, and special effect tooltip. A text-only page or empty list is a user-reported failure to resolve.
- The Altar of Kings and selection courtyard are before wave 1. It must match the familiar hero-building role and show the user's chosen hero flow rather than an unrelated unit/model.
