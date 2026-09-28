# Waves, bosses, and invading forces

The invasion lasts forty waves, divided into four ten-wave chapters. Normal waves retain earlier enemy roles as new units are introduced. Demons supplement the undead rather than replacing them. Living mercenary/creature escorts appear because hero spells and effects that interact with living beings need valid combat targets too.

## Chapter roster progression

| Waves | Chapter | New pressure | Roles retained |
|---|---|---|---|
| 1–10 | The Broken Verge | Melee attackers and ranged support; introduce demons and living escorts early | Basic undead swarm plus support |
| 11–20 | The Grave March | Durable elites and necromancers | Earlier melee/ranged pressure plus demons and escorts |
| 21–30 | The Siege Tide | Siege pressure and mixed escorts | Earlier waves, elites, necromancers, ranged and demonic support |
| 31–40 | The Last Host | Endgame combinations and Infernals | Full prior roster with siege, elites, casters, demons, and escorts |

The code stores forty explicit generated rosters in tools/wave_rosters.py. Spawn count grows as 7 + 2 × wave + 3 × active players. Ordinary wave enemies start from health 180 + 55 × wave + 35 × active players, and damage 6 + 2 × wave. Boss health scales from wave × 550 × (1 + 0.3 × active players), with boss base damage wave × 5. These are initial tuning formulas, not proven balanced values.

Current roster rawcodes include: ugho, uske, ucry, nska, nfel, hfoo, nfgu, unec, nsat, uabo, ndqn, nvdw, umtw, nbal, and ninf. Read names from the installed game table during builds; never invent a rawcode mapping from memory. The rawcode roster is intentionally maintained against installed DE object data.

## Combat gold bounty (initial tuning)

Each tracked enemy death grants one team bounty, then divides it equally among active defenders; remainder gold follows player-slot order. The final blow does not take the whole payout. A role's base bounty increases by the current wave number:

| Role / unit rawcode | Base gold | Example at wave 1 |
|---|---:|---:|
| Skeleton Warrior (`uske`) | 5 | 6 |
| Ghoul (`ugho`) | 8 | 9 |
| Footman escort (`hfoo`) | 9 | 10 |
| Crypt Fiend / Skeletal Archer (`ucry` / `nska`) | 12 | 13 |
| Satyr Trickster (`nsat`) | 14 | 15 |
| Succubus / Voidwalker (`ndqn` / `nvdw`) | 16 | 17 |
| Fel Stalker (`nfel`) | 18 | 19 |
| Necromancer (`unec`) | 22 | 23 |
| Felguard (`nfgu`) | 24 | 25 |
| Abomination (`uabo`) | 32 | 33 |
| Meat Wagon (`umtw`) | 36 | 37 |
| Doom Guard (`nbal`) | 40 | 41 |
| Infernal (`ninf`) | 45 | 46 |
| Chapter boss | 100 + 5 × wave | 150 |

These are starting values for playtesting, not final balance. Bosses also retain their existing per-defender chapter reward and personal relic. Boss reinforcements use their own unit role's bounty when killed. The table is generated from `tools/wave_rosters.py`; every rawcode in the 40 wave rosters must have exactly one bounty entry.

The full generated unit-code sequence for every wave, in order, is preserved in WAVE-ROSTER-CATALOG.md. At runtime, the spawn loop cycles through that wave's listed sequence if the player-scaled count is larger than the sequence.

Each wave enemy is registered once in the authoritative tracked group. The spawn loop aborts with a diagnostic error if a required unit cannot be created; it must not leave the match waiting forever for a unit that never spawned. Death, boss summons, cleanup, and wave completion need exactly-once accounting.

## Four named bosses

| Wave | Boss | Current boss unit | Signature mechanic |
|---|---|---|---|
| 10 | Bonequake | Death Knight hero base | Three-second slam warning and marked-area attack |
| 20 | Grave Muster | Lich hero base | Summons reinforcements; count every summon |
| 30 | Siege Blight | Dreadlord hero base | Suppresses/pause defender towers for 8 seconds |
| 40 | The Last March | Crypt Lord hero base | Combines slam, summons, and tower blackout |

- Telegraph before action, keep the HUD and on-screen warning visible until resolution, and never hide a warning while its attack is pending.
- Bosses are tracked as enemies. Each active defender receives one personal reward on boss death, even if escorts remain.
- Defeating the final boss while the king is alive is the wave-40 victory condition. The king's death takes precedence if both resolve together. Wave-40 escorts cannot delay victory forever.
- The design calls for one unique, unsellable relic per boss, awarded to every participating player. Current rawcodes are I010–I013; see ITEMS-AND-EQUIPMENT.md for the documented gap in names/effects and full-storage entitlement handling.

## Composition and pathing guardrails

- Do not repeatedly send every enemy a fresh attack order; this interrupts combat. Recover only units that have no order or are genuinely stuck.
- Keep the road and gate open to normal units, siege units, escorts, boss footprints, and summons.
- Dreadlord/Necromancer/Satyr and other non-undead or living targets matter mechanically: do not make every attack target undead.
- Use the combat groves for native tree-target hero skills. Keep eight nearby lumber trees at each player plot as well, but leave worker access and the enemy lane clear.
- Preserve varied models and roles in every chapter. The user's original live feedback was that attacks looked like the same repeated mob; avoid a composition that visually collapses into one unit type.
