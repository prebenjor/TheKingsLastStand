"""Shared map/report attribute conversions verified in installed MiscGame.txt.

The base and custom_v1 tables agree. Pin them in the map so projections cannot
silently drift with a future default balance table.
"""
ATTRIBUTE_CONSTANTS = {
    'StrAttackBonus': 1.0, 'StrHitPointBonus': 25.0, 'StrRegenBonus': 0.05,
    'IntManaBonus': 15.0, 'IntRegenBonus': 0.05,
    'AgiDefenseBonus': 0.30, 'AgiDefenseBase': -2.0,
    'AgiAttackSpeedBonus': 0.02,
}


def misc_attribute_data():
    return ''.join(f'{key}={value:g}\n' for key, value in ATTRIBUTE_CONSTANTS.items()).encode()


def attribute_secondary_delta(base, final):
    strength = final['strength'] - base['strength']
    intelligence = final['intelligence'] - base['intelligence']
    agility = final['agility'] - base['agility']
    return {
        'hp': strength * ATTRIBUTE_CONSTANTS['StrHitPointBonus'],
        'mana': intelligence * ATTRIBUTE_CONSTANTS['IntManaBonus'],
        'hp_regen': strength * ATTRIBUTE_CONSTANTS['StrRegenBonus'],
        'mana_regen': intelligence * ATTRIBUTE_CONSTANTS['IntRegenBonus'],
        'armor': agility * ATTRIBUTE_CONSTANTS['AgiDefenseBonus'],
        'attack_speed_bonus': agility * ATTRIBUTE_CONSTANTS['AgiAttackSpeedBonus'],
    }
