# Gameplay specification

This document preserves the approved gameplay target. Code presence is tracked separately from live verification in ROADMAP-AND-ACCEPTANCE.md.

## September 30 authored layout decision

The user removed Redtusk Hold entirely, replaced gates with cliffs and placed a troll camp. Preserve that authored terrain/doodad/unit composition after the saved-map handoff. The three surviving settlements are Crownshire, Moonbark Glade and Wraithfall; all four playable races and personal bases remain. The optional four-stage story relocates Northwatch's contact and restores three extant refuges, with no prerequisite on a deleted Orc town. Troll-camp behavior is undecided. Exact positions, camp ownership and cliff-route validation remain pending; see [EDITOR-LAYOUT-REVISION.md](EDITOR-LAYOUT-REVISION.md). Current runtime still creates four towns and old gates and must be reconciled before the next integrated build.

## Match state and opening

Authoritative match states:

    INITIALIZING → HERO_SELECTION → PREPARATION ↔ WAVE_ACTIVE → KING_DEFEATED

- Create gameplay only for occupied player slots. Diagnostic packages may run solo; release packages support 2–4 defenders.
- Defenders are allied and share vision. Shared unit control is disabled. Undead invaders have a distinct hostile owner.
- Each active player sees a 45-second hero selection. The fallback for a player who does not confirm is Paladin.
- Players choose one of 25 hero previews: the original seventeen plus the eight race-themed heroes. Duplicate choices are allowed. The selected hero's race independently determines that player's starting worker and building menu. Create the selected hero once; do not leave or replace a usable placeholder hero.
- After every active player selects, start the initial 45-second preparation period. Beginning troops stay held until the selection phase ends.
- Normal cleared-wave breaks are 50 seconds. Breaks before each boss wave (10, 20, 30, 40, 50, and every ten waves after) are 180 seconds. The 50-second ordinary break supersedes the earlier 90-second decision; the longer boss break remains.
- The Wave 40 boss no longer ends the match. After Wave 40 clears, spawning continues automatically. King Aldric's death ends the run and the HUD shows the highest wave reached; terminal defeat stops spawns, timers, damage, rewards, and revival.
- If a player leaves, remove their control and stop scaling them into future waves. Do not transfer their living army to another player; let its current orders continue.

## Player ownership and economy

- Each player controls their hero, race-matched workers, trained units, and structures.
- The team shares the battlefield, neutral vendors, enemy waves, boss encounter, king, and outcome; players do not share unit control or personal resources.
- Workers use standard Warcraft mine and lumber gathering. Put an accessible mine and harvestable tree grove by every active plot. The generated base lumber stand has eight trees in two compact rows 500 and 700 map units south of the hall, offset to its eastern side. Trees must not block routes to the mine, Altar, buildable pad, or road. After hero confirmation, each Undead player starts with an owned Haunted Gold Mine and each Night Elf with an owned Entangled Gold Mine; Human and Orc players keep a neutral Gold Mine. Every starting mine holds 1,000,000 gold.
- A defender player's kill pays the full role bounty to that killer's owner only. A kill credited to King Aldric pays 25% of the bounty to each active defender. Show each recipient the exact amount credited. Boss participation gold and gear remain personal rewards for every active participant.
- Every active defender hero within 1,200 world units of a tracked enemy's death receives the full Warcraft unit-level XP award. The same full value is applied to each nearby hero; it is not divided. Hero race and current life state do not filter the recipients. Native shared/kill XP is disabled in map data so the custom award cannot split or double-count; verify dead-hero XP behavior in the engine.
- Boss gear is personal. If the inventory cannot accept the reward, preserve an entitlement or safely place a retrievable personal item; never destroy it or make it public/lootable by another defender.
- The market is one shared set of neutral shops accessible to all players. A purchase, tome, recipe, or castle contribution charges the buyer's personal resources.
- Gear rarity base prices are 300 / 1,000 / 3,000 / 8,000 / 20,000 gold from Common to Legendary. Blade, Bow and Staff cost 1.5 times the tier base; recipes and stat tomes use their higher listed prices. Healing and mana potions keep their current cost.

## Hero growth

- Start player heroes at level 1. Cap them at level 50.
- Each hero retains four recognizable native Warcraft skills. Preserve every installed native rank. Extend only abilities whose installed power fields are explicitly registered in `tools/hero_progression.py`; see HEROES-AND-ABILITIES.md for the mapping.
- Preserve the original skill unlock levels. Players learn spell ranks manually with normal hero skill points; ranks do not advance automatically on level milestones. Supported rank 4–5 data adds 10% of the final authored power field per added rank, while cost, cooldown, duration, range, targeting and untagged fields copy from the final native rank. Unsupported effects stay capped at their installed maximum.
- Each of the 25 heroes has one custom signature ability and a hero-specific company/support pair.
- Every gained hero level grants one normal skill point. Spend it on one native spell rank or choose one of three repeatable, unranked +3 STR/AGI/INT buttons. There is no automatic attribute growth. Every fifth level grants a separate talent choice: Strength adds health/health regeneration; Agility adds attack speed/evasion; Intelligence adds mana/mana regeneration.
- Optional Crownlands recovery objectives are shared within the match and remain available during waves; they never pause wave timing or change the wave enemy count. See CROWNLANDS-EXPANSION.md for all four steps and personal rewards.
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
- Tier-two Town Hall upgrades must require the matching race's custom Altar, Barracks and upgrade structure rawcodes so Castle, Stronghold, Tree of Ages and Halls of the Dead remain reachable from every race's build menu.

Construction rules:

- Enforce ownership and validate the full footprint inside the owning player's plot.
- Reject a building or upgrade whose footprint intersects the central unbuildable road, leaves the owner's plot, overlaps prohibited structures, or blocks the only enemy route.
- An invalid placement is completely refunded and leaves no abandoned construction site.
- Place tower frontage facing the road. Prove coverage of the road before scenery decoration.
- Confirm worker pathing to the mine and trees and enemy pathing from northern spawns through the authored cliff passages to King Aldric before adding blocking objects.
- Preserve the user's cliff-based frontier instead of restoring deleted gates. Leave a navigable invasion route wide enough for bosses and siege units.

## King Aldric and his castle

King Aldric is the shared survival objective at the central castle. His castle is an invulnerable native shop-style interaction building with readable native command-card buttons for healing and royal upgrades; do not put long overflowing prose in a framed dialog.

- Starting maximum health: 15,000; base damage: 80.
- Heal: 150 personal gold + 50 personal lumber; restore up to 2,000 HP. Full health is rejected and refunded.
- Five one-at-a-time royal tiers. Cost is 400 + 200 × existing tier gold and 150 lumber. Each gives +4,000 maximum/current HP and +30 damage.
- Reject maximum tier, stale tier price, dead king, invalid owner, insufficient resources, and full-health repair without charge.
- Contribution must be atomic: either apply the complete health/tier/damage change and debit the exact personal cost, or refund everything.
- King health/tier must appear in the persistent top HUD.

## Waves, enemies, and difficulty

- At hero selection, every active player votes Easy, Normal, Hard, or Very Hard; votes start on Normal and remain changeable until selection closes. Highest vote wins; no votes or a tie resolves to Normal. The final difficulty is synchronized, shown in the HUD and `-diag`, and scales enemies after wave/player scaling:

| Difficulty | Enemy health | Enemy base damage | Regular wave count |
|---|---:|---:|---:|
| Easy | 0.75× | 0.80× | 0.90× |
| Normal | 1.00× | 1.00× | 1.00× |
| Hard | 1.30× | 1.20× | 1.10× |
| Very Hard | 1.60× | 1.40× | 1.20× |

- During every wave-free preparation interval, each player may toggle a Ready vote. The next wave starts immediately only after every active player votes Ready; otherwise the 50-second normal / 180-second pre-boss countdown remains. The control is owner-local and never pauses the match.
- Preserve waves 1-40 as the four-chapter Crownlands story. Waves 41 onward reuse the generated ten-row campaign crossover roster with a bounded source index while count, health, damage, bounty, XP, and boss scaling continue to use the live wave number. See WAVES-AND-BOSSES.md.
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
- Five rarity vendors (Common/Quartermaster, Uncommon/Veteran, Rare Arms & Armor and Rare Apparel & Relics, Epic/Runic Reliquary, and Legendary/Royal Vault) sell general gear in the southern market. The Master Forge stocks three general recipes; each player's constructed race-themed Foundry sells one copy of that race's Legendary pattern. The three surviving town shops sell their four themed relics and potions. Move the removed Orc shop's four relics to existing matching-rarity market vendors, preserving recipe component access and checking capacity. Legendary race relics remain recipe outputs. Sage's Archive sits next to the Apothecary and sells personal permanent Strength/Agility/Intelligence tomes. All stock fits the native 12-slot shop command card. Revised sources remain pending integration.
- Gold alone gates equipment quality; all shop tiers are available from the beginning.
- A shop must use an actual clickable item stock/window with icon, item identity, price, slot, stats, and special effect tooltip. A text-only page or empty list is a user-reported failure to resolve.
- The Altar of Kings and selection courtyard are before wave 1. It must match the familiar hero-building role and show the user's chosen hero flow rather than an unrelated unit/model.
