# Hero gear, spell progression, recovery and wave breaks

## Approved design

- Raise the player hero cap to 100 and extend each selectable hero's four regular abilities to ten ranks. Rank 1 retains the hero's ordinary unlock rules; higher ranks arrive automatically at level milestones and use the installed Warcraft ability data through rank 6 plus a conservative continuation to rank 10. Existing custom signature spells continue scaling with hero level.
- Extend the tier catalog with Strength, Agility and Intelligence equipment. Add a Sage's Archive building beside the Field Apothecary with permanent +5, +10 and +20 attribute tomes for each attribute.
- Add three personal Master Forge recipes. Each consumes its named gear components from the hero's inventory, Forsaken backpack or equipment slots. The recipe fee, ingredient removal and crafted item delivery form one transaction; failure restores the fee and leaves components alone.
- Place a restorative fountain south of the castle, off the central route. It restores nearby living defender heroes' health and mana in timed pulses.
- Set normal post-wave preparation to 60 seconds and boss-wave preparation to 120 seconds. Keep the approved initial selection/preparation timers.

## Implementation sequence

1. Add focused failing regressions for attribute gear and books, recipe data and transactions, native spell rank records and level milestones, fountain placement/effect, shop object data, and revised timers.
2. Extend the single item catalog and object-data generator; preserve existing item rawcodes and existing item stats. Create the Sage's Archive shop object and stock the attribute books.
3. Implement post-purchase book handling and a delayed, atomic recipe transaction. Enumerate all native storage locations and equipment slots. Replenish unlimited stock and report transaction outcomes.
4. Generate native spell base-object modifications from the installed AbilityData and AbilityMetaData tables, set the map cap to 100, and apply spell ranks at hero creation and level milestones without removing the existing hero identities or spell buttons.
5. Add the southern health/mana fountain and longer preparation intervals. Update player/build documentation and append evidence to RECOVERY-PROGRESS.md.
6. Run the focused regression suite requested in the approved recovery plan, compile against the installed Warcraft API, build and read back the MPQ, compare its manifest and installed diagnostic hashes, and preserve the development label. Engine, editor round-trip, multiplayer and full 40-wave endurance checks remain pending until actually performed.

## Verification evidence

- Tests must parse the emitted item, unit, and ability object records rather than only search source text.
- Recipe tests must exercise success and failure with ingredients in storage/equipment, including the full-inventory boundary and item ownership.
- Spell tests must prove every selectable hero's skill IDs exist in the pinned installed table and each generated ability has ten rank values.
- Battlefield checks must prove fountain coordinates are inside playable bounds and do not lie on the unbuildable central road.
- Package success is static evidence only; live use of tomes, recipes, pool, and rank progression remains an in-game acceptance check.
