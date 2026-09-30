# Waves, bosses, and invading forces

The Crownlands story lasts forty waves, divided into four ten-wave chapters. After Wave 40, the match automatically continues through an endless campaign crossover. Normal waves retain earlier enemy roles as new units are introduced. Demons supplement the undead rather than replacing them. Living mercenary/creature escorts appear because hero spells and effects that interact with living beings need valid combat targets too.

## Chapter roster progression

| Waves | Chapter | New pressure | Roles retained |
|---|---|---|---|
| 1–10 | The Broken Verge | Melee attackers and ranged support; introduce demons and living escorts early | Basic undead swarm plus support |
| 11–20 | The Grave March | Durable elites and necromancers | Earlier melee/ranged pressure plus demons and escorts |
| 21–30 | The Siege Tide | Siege pressure and mixed escorts | Earlier waves, elites, necromancers, ranged and demonic support |
| 31–40 | The Last Host | Endgame combinations and Infernals | Full prior roster with siege, elites, casters, demons, and escorts |

The generator stores the original 40 rows and one ten-row endless roster (waves 41-50). Endless waves resolve to source row `41 + ((wave - 41) % 10)`, so roster indexing stays bounded while the live wave number continues to scale difficulty. Spawn count grows as 7 + 2 × wave + 3 × active players. Ordinary wave enemies start from health 180 + 55 × wave + 35 × active players, and damage 6 + 2 × wave. Boss health scales from wave × 550 × (1 + 0.3 × active players), with boss base damage wave × 5. The group-selected difficulty applies after those values:

| Difficulty | Enemy health | Enemy base damage | Regular wave count |
|---|---:|---:|---:|
| Easy | 0.75× | 0.80× | 0.90× |
| Normal | 1.00× | 1.00× | 1.00× |
| Hard | 1.30× | 1.20× | 1.10× |
| Very Hard | 1.60× | 1.40× | 1.20× |

Boss count remains one. Boss reinforcement count, health, and damage also use the chosen difficulty. These are initial tuning formulas, not proven balanced values.

The crossover introduces installed campaign Naga (`nmyr`, `nnsw`, `nnmg`, `nnrg`, `nhyc`, `nwgs`), Blood Elf (`nbel`, `nbee`, `hbew`), Fel Orc / Chaos Orc (`nchg`, `nchr`, `nchw`, `nckb`), Burning Legion (`nfel`, `nfgu`, `nbal`, `ninf`), and Scourge (`uske`, `ugho`, `ucry`, `nska`, `unec`, `uabo`, `umtw`) forces. Wave 49 gathers all five factions. Wave 50's ordinary roster is followed by a separate Lady Vashj boss spawn. These unit IDs resolve to the locally installed Definitive Edition tables; their native campaign models, animations, and armor fields are inherited without custom unit replacements.

The complete ordered rawcode sequences for story and crossover waves are maintained in the generated [wave roster catalog](WAVE-ROSTER-CATALOG.md). Read unit names and campaign status from the installed game tables during builds; never invent a rawcode mapping from memory. Crossover units keep their installed Definitive Edition model, animation set, and armor data.

## Combat gold bounty (initial tuning)

Each tracked enemy death gives the role bounty to the defender player who owns the killing unit. Player kill gold is not shared. If King Aldric gets the killing blow, each active defender gets 25% of that enemy's bounty. A role's base bounty increases by the current wave number:

| Role / unit rawcode | Base bounty | Paid bounty formula |
|---|---:|---|
| Skeleton Warrior (`uske`) | 5 | base + live wave |
| Ghoul (`ugho`) | 8 | base + live wave |
| Footman escort (`hfoo`) | 9 | base + live wave |
| Crypt Fiend / Skeletal Archer (`ucry` / `nska`) | 12 | base + live wave |
| Satyr Trickster (`nsat`) | 14 | base + live wave |
| Succubus / Voidwalker (`ndqn` / `nvdw`) | 16 | base + live wave |
| Fel Stalker (`nfel`) | 18 | base + live wave |
| Necromancer (`unec`) | 22 | base + live wave |
| Felguard (`nfgu`) | 24 | base + live wave |
| Abomination (`uabo`) | 32 | base + live wave |
| Meat Wagon (`umtw`) | 36 | base + live wave |
| Doom Guard (`nbal`) | 40 | base + live wave |
| Infernal (`ninf`) | 45 | base + live wave |
| Naga Myrmidon / Siren / Mur'gul Reaver (`nmyr` / `nnsw` / `nnmg`) | 28 / 24 / 28 | base + live wave |
| Naga Royal Guard / Dragon Turtle / Couatl (`nnrg` / `nhyc` / `nwgs`) | 40 / 42 / 36 | base + live wave |
| Blood Elf Lieutenant / Engineer / Siege Wagon (`nbel` / `nbee` / `hbew`) | 25 / 22 / 36 | base + live wave |
| Fel Orc Grunt / Wolf Rider / Warlock / Kodo Beast (`nchg` / `nchr` / `nchw` / `nckb`) | 24 / 30 / 30 / 34 | base + live wave |
| Chapter / endless boss | - | 100 + 5 × live wave |

These are starting values for playtesting, not final balance. Bosses on waves 10-40 retain their existing per-defender gold reward and personal relic. Bosses from wave 50 onward grant one personal Legendary catalog item to each active player. Boss reinforcements use their own unit role's bounty when killed. The table is generated from `tools/wave_rosters.py`; every rawcode in the 50 generated roster rows must have exactly one bounty entry.

For each tracked enemy death, each active defender hero within 1,200 world units independently receives the full normal unit-level XP award. The runtime disables native XP sharing and applies each full award, so nearby heroes do not divide one total. Hero race and life state do not filter recipients. Verify behavior with a dead hero in the installed game before calling it engine-proven.

The full generated unit-code sequence for each of the 50 source rows, in order, is preserved in WAVE-ROSTER-CATALOG.md. At runtime, the spawn loop cycles through that row's sequence if the player-scaled count is larger than the sequence. Live wave 51 reuses row 41, wave 60 reuses row 50, and the ten-row pattern continues without growing the roster table.

Each wave enemy is registered once in the authoritative tracked group. The spawn loop aborts with a diagnostic error if a required unit cannot be created; it must not leave the match waiting forever for a unit that never spawned. Death, boss summons, cleanup, and wave completion need exactly-once accounting.

## Enemy gear and potion drops

The wave roster explicitly classifies every ordinary role as Normal or Elite. Loot does not use wave-scaled bounty to infer toughness: durable Crypt Fiends, elite/caster units, siege roles, and heavier campaign fighters receive the Elite profile; basic infantry, Ghouls, Satyrs, and Skeletal Archers use Normal. The active boss flag selects Boss regardless of the unit's ordinary role.

| Enemy tier | Common | Uncommon | Rare | Epic | Legendary | Total gear chance | Potion chance |
|---|---:|---:|---:|---:|---:|---:|---:|
| Normal | 0% | 0% | 0% | 0% | 0% | 0% | 4% |
| Elite | 0.5% | 0.5% | 0% | 0% | 0% | 1% | 8% |
| Boss world roll | 0% | 0% | 0% | 0% | 0% | 0% | 18% |

Normal and Boss enemy deaths never produce random catalog equipment. Elites have a 1% total gear chance, split evenly between Common and Uncommon. Bosses receive a guaranteed owner-bound personal item instead: Uncommon at wave 10, Rare at 20, Epic at 30, and Legendary at 40 and every later ten-wave boss. Waves 10–40 use their named personal relics; wave 50+ uses a random item from the milestone tier. Potion rolls are independent, so a potion may still accompany a boss reward. Consumables are chosen uniformly from Potion of Healing (phea), Potion of Mana (pman), Scroll of Town Portal (stwp), and Scroll of Healing (shea). Elite drops are personalized to the active killing defender. Boss/story completion rewards remain separate personal rewards.

## Four named bosses

| Wave | Boss | Current boss unit | Signature mechanic |
|---|---|---|---|
| 10 | Bonequake | Death Knight hero base | Three-second slam warning and marked-area attack |
| 20 | Grave Muster | Lich hero base | Summons reinforcements; count every summon |
| 30 | Siege Blight | Dreadlord hero base | Suppresses/pause defender towers for 8 seconds |
| 40 | The Last March | Crypt Lord hero base | Combines slam, summons, and tower blackout |
| 50 | Vashj Ascendant | Campaign Lady Vashj (`Hvsh`) | Convergence slam, summons, and tower blackout |

- Telegraph before action, keep the HUD and on-screen warning visible until resolution, and never hide a warning while its attack is pending.
- Bosses are tracked as enemies. Each active defender receives one personal reward on boss death, even if escorts remain.
- Bosses recur every ten waves. Waves 50, 60, 70, 80, and 90 rotate among the installed campaign leader records `Hvsh`, `Usyl`, `Uanb`, `Hjsm`, and `Ujsm`; the five-step leader cycle repeats.
- Wave 40 is not a victory point. Defeating its boss and clearing the remaining enemies starts the next preparation countdown and the automatic Wave 41 assault. The match ends only when King Aldric falls; the final HUD shows the highest wave reached.
- Waves 10-40 keep their personal relics (`I010`-`I013`). Each boss from Wave 50 onward grants each active player one personal Legendary catalog item. Existing owner binding, inventory delivery, fallback placement, bounty, XP, and ordinary boss-drop rules remain in effect.

## Composition and pathing guardrails

- Do not repeatedly send every enemy a fresh attack order; this interrupts combat. Recover only units that have no order or are genuinely stuck.
- Keep the road and gate open to normal units, siege units, escorts, boss footprints, and summons.
- Dreadlord/Necromancer/Satyr and other non-undead or living targets matter mechanically: do not make every attack target undead.
- Use the combat groves for native tree-target hero skills. Keep eight nearby lumber trees at each player plot as well, but leave worker access and the enemy lane clear.
- Preserve varied models and roles in every chapter. The user's original live feedback was that attacks looked like the same repeated mob; avoid a composition that visually collapses into one unit type.
