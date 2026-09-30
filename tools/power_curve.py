"""Render a deterministic hero and equipment power report from installed data."""
import argparse
import json
import statistics
from pathlib import Path

from equipment_catalog import item_catalog, attribute_books
from hero_catalog import HERO_TYPES, HERO_PRIMARY_STATS, HERO_PARENT_TYPES, HERO_BASE_HP_OVERRIDES, NEW_HEROES
from pipeline import check_api
from stat_rules import ATTRIBUTE_CONSTANTS, attribute_secondary_delta

SLOT_NAMES = {1: "Head", 2: "Chest", 3: "Gloves", 4: "Boots", 5: "Ring",
              6: "Primary", 7: "Offhand", 8: "Trinket"}

def equipment_slot(item):
    return SLOT_NAMES.get(item.get("slot"), item.get("slot_name", "Unknown"))

ROOT = Path(__file__).resolve().parents[1]
LEVEL_CAP = 50
ATTRIBUTES = ('strength', 'agility', 'intelligence')
DISPLAY = {'strength': 'STR', 'agility': 'AGI', 'intelligence': 'INT'}
UNIT_BALANCE = ROOT / 'tools/reference/installed/UnitBalance.slk'
UNIT_WEAPONS = ROOT / 'tools/reference/installed/UnitWeapons.slk'


def slk_table(path, id_field):
    rows = {}
    y = 0
    for line in path.read_text().splitlines():
        if not line.startswith('C;'):
            continue
        import re
        y_match = re.search(r';Y(\d+)', line)
        if y_match:
            y = int(y_match[1])
        x_match = re.search(r';X(\d+)', line)
        value_match = re.search(r';K(.*)', line)
        if x_match and value_match:
            rows.setdefault(y, {})[int(x_match[1])] = value_match[1].strip('"')
    if 1 not in rows:
        raise ValueError('Installed UnitBalance.slk has no header row.')
    headers = {name: index for index, name in rows[1].items()}
    return headers, {row.get(headers[id_field]): row for row in rows.values()
                     if row.get(headers[id_field])}


def hero_catalog():
    from company_catalog import HERO_COMPANIES
    names = {entry['hero_type']: entry['hero_name'] for entry in HERO_COMPANIES}
    return [
        {
            'unit_id': unit_id,
            'name': names[unit_id],
            'parent': HERO_PARENT_TYPES[unit_id],
            'primary': HERO_PRIMARY_STATS[unit_id],
        }
        for unit_id in HERO_TYPES + tuple(entry['unit_id'] for entry in NEW_HEROES)
    ]


def numeric(row, headers, name, required=False):
    index = headers.get(name)
    raw = row.get(index, '') if index is not None else ''
    try:
        return float(raw)
    except (TypeError, ValueError):
        if required:
            raise ValueError('Installed UnitBalance.slk is missing numeric field ' + name)
        return None


def load_heroes():
    provenance = check_api()
    headers, rows = slk_table(UNIT_BALANCE, 'unitBalanceID')
    weapon_headers, weapon_rows = slk_table(UNIT_WEAPONS, 'unitWeaponID')
    required = ('STR', 'AGI', 'INT', 'HP', 'realM', 'Primary')
    missing = [field for field in required if field not in headers]
    if missing:
        raise ValueError('Installed UnitBalance.slk is missing fields: ' + ', '.join(missing))
    result = {}
    for entry in hero_catalog():
        row = rows.get(entry['parent'])
        if row is None:
            raise ValueError('No installed UnitBalance row for hero ' + entry['unit_id'] +
                             ' parent ' + entry['parent'] +
                             '; extract installed APIs with python kings-last-stand/tools/extract_game_api.py')
        entry['base_stats'] = {stat: numeric(row, headers, DISPLAY[stat], True)
                               for stat in ATTRIBUTES}
        entry['base_hp'] = HERO_BASE_HP_OVERRIDES.get(entry['unit_id'], numeric(row, headers, 'HP', True))
        entry['base_hp'] += entry['base_stats']['strength'] * ATTRIBUTE_CONSTANTS['StrHitPointBonus']
        entry['base_mana'] = numeric(row, headers, 'manaN', True) + entry['base_stats']['intelligence'] * ATTRIBUTE_CONSTANTS['IntManaBonus']
        entry['hp_regen'] = numeric(row, headers, 'regenHP') or 0
        entry['mana_regen'] = numeric(row, headers, 'regenMana') or 0
        entry['hp_regen'] += entry['base_stats']['strength'] * ATTRIBUTE_CONSTANTS['StrRegenBonus']
        entry['mana_regen'] += entry['base_stats']['intelligence'] * ATTRIBUTE_CONSTANTS['IntRegenBonus']
        entry['base_armor'] = (numeric(row, headers, 'def', True) + ATTRIBUTE_CONSTANTS['AgiDefenseBase'] + entry['base_stats']['agility'] * ATTRIBUTE_CONSTANTS['AgiDefenseBonus'])
        entry['native_primary'] = row.get(headers['Primary'], '')
        weapon = weapon_rows.get(entry['parent'])
        if weapon is None:
            raise ValueError('No installed UnitWeapons.slk row for hero ' + entry['unit_id']+
                             ' parent ' + entry['parent']+
                             '; extract installed APIs with python kings-last-stand/tools/extract_game_api.py')
        entry['weapon_min'] = numeric(weapon, weapon_headers, 'mindmg1', True)
        entry['weapon_max'] = numeric(weapon, weapon_headers, 'maxdmg1', True)
        entry['provenance'] = provenance.get('build_info_sha256', 'unknown')
        result[entry['unit_id']] = entry
    return result, provenance


def add_projection(hero, level, points, talent_stat=''):
    stats = dict(hero['base_stats'])
    for stat, count in points.items():
        stats[stat] += count * 3
    milestones = level // 5
    hp = hero['base_hp']
    mana = hero['base_mana']
    hp_regen = hero['hp_regen']
    mana_regen = hero['mana_regen']
    if talent_stat == 'strength':
        stats['strength'] += milestones * 5
        hp += milestones * 200
        hp_regen += milestones * 2
    elif talent_stat == 'agility':
        stats['agility'] += milestones * 5
    elif talent_stat == 'intelligence':
        stats['intelligence'] += milestones * 5
        mana += milestones * 100
        mana_regen += milestones * 2
    secondary = attribute_secondary_delta(hero['base_stats'], stats)
    hp += secondary['hp']
    mana += secondary['mana']
    hp_regen += secondary['hp_regen']
    mana_regen += secondary['mana_regen']
    damage_min = hero['weapon_min'] + stats[hero['primary']]
    damage_max = hero['weapon_max'] + stats[hero['primary']]
    return stats, hp, mana, hp_regen, mana_regen, milestones, damage_min, damage_max


def fmt_stats(stats):
    return '/'.join(str(round(stats[stat], 2)).rstrip('0').rstrip('.')
                    if isinstance(stats[stat], float) else str(stats[stat])
                    for stat in ATTRIBUTES)


def fmt_projection(stats, damage_min, damage_max):
    return f'{fmt_stats(stats)} ({damage_min:g}–{damage_max:g} damage)'


def talent_summary(milestones):
    return (f'STR path +{5*milestones} STR, +{200*milestones} HP, +{2*milestones} HP regen; '
            f'AGI path +{5*milestones} AGI, +{2*milestones}% evasion; '
            f'INT path +{5*milestones} INT, +{100*milestones} mana, '
            f'+{2*milestones} mana regen')


def curve_report(heroes):
    lines = [
        '# Hero and Item Power Curve', '',
        'Attribute secondary effects are included using the same pinned MiscGame conversions as the map: +25 HP/+0.05 HP regen per STR; +15 mana/+0.05 mana regen per INT; +0.3 armor/+2% attack speed per AGI. Active buffs and procs remain separately listed, not estimated DPS.', '',
        'Generated from the current hero/item catalogs and the installed Definitive Edition UnitBalance data. ',
        'Selectable heroes have zero native attribute growth; these tables show base stats plus the stated manual allocation. Damage ranges use installed weapon rolls plus the hero primary attribute. ',
        'Normal skill points include one initial point at level 1 and one per level gained. The +3 stat buttons and spell ranks compete for those points. ',
        'Fifth-level talent offsets are shown separately from normal skill points.', '',
        '| Hero | Unit | Installed parent | Primary | Base STR/AGI/INT | Base damage | Base HP | Base mana |',
        '|---|---|---|---|---:|---:|---:|---:|',
    ]
    for hero in heroes.values():
        lines.append(f"| {hero['name']} | {hero['unit_id']} | {hero['parent']} | "
                     f"{DISPLAY[hero['primary']]} | {fmt_stats(hero['base_stats'])} | "
                     f"{hero['weapon_min'] + hero['base_stats'][hero['primary']]:g}–{hero['weapon_max'] + hero['base_stats'][hero['primary']]:g} | "
                     f"{hero['base_hp']:g} | {hero['base_mana']:g} |")
    lines.extend(['', '## Level projections', '',
                  'Each row is one hero at one level. STR/AGI/INT cells are final attributes before applying one of the listed talent paths; ',
                  'the talent column gives the exact separate STR, AGI, or INT path offsets for that level. Each stat-spend scenario spends all normal points on the named option.', '',
                  '| Hero | Lvl | Total normal point budget | No stat picks (spell/unspent) STR/AGI/INT + damage | All primary stat STR/AGI/INT + damage | All STR picks + damage | All AGI picks + damage | All INT picks + damage | Talent path offsets (choose one per milestone) |',
                  '|---|---:|---:|---|---|---|---|---|---|'])
    for hero in heroes.values():
        for level in range(1, LEVEL_CAP + 1):
            skill_points = level
            spell = add_projection(hero, level, {})
            primary = add_projection(hero, level, {hero['primary']: skill_points})
            str_projection = add_projection(hero, level, {'strength': skill_points})
            agi_projection = add_projection(hero, level, {'agility': skill_points})
            int_projection = add_projection(hero, level, {'intelligence': skill_points})
            lines.append(f"| {hero['name']} | {level} | {skill_points} | {fmt_projection(spell[0],spell[6],spell[7])} | "
                         f"{fmt_projection(primary[0],primary[6],primary[7])} | "
                         f"{fmt_projection(str_projection[0],str_projection[6],str_projection[7])} | "
                         f"{fmt_projection(agi_projection[0],agi_projection[6],agi_projection[7])} | "
                         f"{fmt_projection(int_projection[0],int_projection[6],int_projection[7])} | "
                         f"{talent_summary(level//5)} |")
    return lines


def item_effect_text(item):
    effects = item.get('effects', [])
    if not effects:
        return item.get('effect', '') or '—'
    return '; '.join(
        f"{effect['name']}: {effect['magnitude']} {effect['unit']} on {effect['trigger']}"
        + (f", duration {effect['duration']}" if effect.get('duration') else '')
        + (f", cooldown {effect['cooldown']}" if effect.get('cooldown') else '')
        + (f", radius {effect['radius']}" if effect.get('radius') else '')
        for effect in effects)


def item_report(items):
    slot_names = {1:'Head', 2:'Chest', 3:'Gloves', 4:'Boots', 5:'Ring',
                  6:'Primary', 7:'Offhand', 8:'Trinket'}
    lines = ['', '## Full item catalog', '',
             '| Rarity | Slot | Name | Rawcode | Numeric stats | Named effect components |',
             '|---|---|---|---|---|---|']
    comparable = {}
    for item in items:
        slot = equipment_slot(item)
        stats = item.get('stats', {})
        lines.append(f"| {item.get('quality', 'Legendary' if item.get('tier') == 4 else '')} | {slot} | "
                     f"{item['name']} | {item['rawcode']} | "
                     f"{', '.join(f'{name} +{value:g}' for name, value in stats.items()) or '—'} | "
                     f"{item_effect_text(item)} |")
        for component, value in stats.items():
            comparable.setdefault((item['tier'], slot, component), []).append((item['rawcode'], value))
    lines.extend(['', '## Tier/slot component audit', '',
                  'Outliers are flagged when a positive component is more than 25% below or above its rarity-and-slot median. ',
                  'Adjacent rarity medians must strictly increase when a component exists in both neighboring tiers; each lower-tier item component over 25% above the next tier median is also flagged. Effects remain separate components above.', '',
                  '| Rarity | Slot | Component | Median | Min–max | Items outside ±25% |',
                  '|---|---|---|---:|---:|---|'])
    tiers = sorted({item['tier'] for item in items})
    groups = {}
    for (tier, slot, component), values in comparable.items():
        median = statistics.median(value for _, value in values)
        outliers = [f'{rawcode} ({value:g})' for rawcode, value in values
                    if value < median * .75 or value > median * 1.25]
        low = min(value for _, value in values)
        high = max(value for _, value in values)
        quality = items[0].get('quality')
        from equipment_catalog import TIERS
        quality = TIERS[tier][0]
        lines.append(f'| {quality} | {slot} | {component} | {median:g} | {low:g}–{high:g} | '
                     f"{', '.join(outliers) or '—'} |")
        groups[(tier, slot, component)] = median
    for tier in tiers[:-1]:
        for slot in sorted({key[1] for key in groups if key[0] == tier}):
            components = sorted({key[2] for key in groups if key[0] == tier and key[1] == slot})
            for component in components:
                current = groups.get((tier, slot, component))
                next_value = groups.get((tier + 1, slot, component))
                if current is not None and next_value is not None and current >= next_value:
                    from equipment_catalog import TIERS
                    lines.append(f"| Tier-order warning | {slot} | {component} | {TIERS[tier][0]} median {current:g} "
                                 f"must be below {TIERS[tier+1][0]} median {next_value:g} | — | — |")
                if next_value is not None:
                    for rawcode, value in comparable[(tier, slot, component)]:
                        if value > next_value * 1.25:
                            lines.append(f'| Cross-tier item warning | {slot} | {component} | {rawcode} ({value:g}) > 1.25x next-tier median {next_value:g} | - | - |')
                if current is not None and next_value is not None and current > next_value * 1.25:
                    from equipment_catalog import TIERS
                    lines.append(f"| Cross-tier warning | {slot} | {component} | {TIERS[tier][0]} median {current:g} "
                                 f"> 1.25× {TIERS[tier+1][0]} median {next_value:g} | — | — |")
    return lines


def parse_item_options(rawcodes, items, max_per_slot=1):
    by_code = {entry['rawcode']: entry for entry in items}
    selected = []
    used_slots = {}
    for code in filter(None, (token.strip().upper() for token in rawcodes.split(','))):
        entry = by_code.get(code)
        if entry is None:
            raise ValueError('Unknown or non-equipment item rawcode: ' + code)
        slot = equipment_slot(entry)
        used_slots[slot] = used_slots.get(slot, 0) + 1
        slot_cap = 2 if slot in ('Ring', 5) else max_per_slot
        if used_slots[slot] > slot_cap:
            raise ValueError('Equipment slot collision: ' + str(slot))
        selected.append(entry)
    return selected


def parse_tomes(rawcodes):
    by_code = {entry['rawcode'].upper(): entry for entry in attribute_books()}
    totals = {stat: 0 for stat in ATTRIBUTES}
    for code in filter(None, (token.strip().upper() for token in rawcodes.split(','))):
        if code not in by_code:
            raise ValueError('Unknown attribute tome rawcode: ' + code)
        entry = by_code[code]
        totals[entry['stat']] += entry['amount']
    return totals


def custom_projection(args, heroes, items):
    hero_key = args.hero.strip().lower()
    hero = next((row for key, row in heroes.items()
                 if key.lower() == hero_key or row['name'].lower() == hero_key), None)
    if hero is None:
        raise ValueError('Unknown hero: ' + args.hero)
    if args.level < 1 or args.level > LEVEL_CAP:
        raise ValueError(f'Level must be between 1 and {LEVEL_CAP}.')
    allocations = {'strength': args.strength_points,
                   'agility': args.agility_points,
                   'intelligence': args.intelligence_points}
    if min(allocations.values()) < 0 or sum(allocations.values()) > args.level:
        raise ValueError('Stat allocations must be nonnegative and spend no more than level normal skill points (including the initial point).')
    talent_names = [token.strip().lower() for token in args.talents.split(',') if token.strip()]
    talent_names = [{'str':'strength','agi':'agility','int':'intelligence'}.get(value, value)
                    for value in talent_names]
    if any(value not in ATTRIBUTES for value in talent_names):
        raise ValueError('Talent choices must be STR, AGI, or INT.')
    if len(talent_names) > args.level // 5:
        raise ValueError('Talent choices cannot exceed the number of fifth-level milestones.')
    items_selected = parse_item_options(args.items, items)
    tome_stats = parse_tomes(args.tomes)
    stats = dict(hero['base_stats'])
    for stat in ATTRIBUTES:
        stats[stat] += allocations[stat] * 3 + tome_stats[stat]
    hp = hero['base_hp']
    mana = hero['base_mana']
    hp_regen = hero['hp_regen']
    mana_regen = hero['mana_regen']
    for talent in talent_names:
        if talent == 'strength':
            stats['strength'] += 5
            hp += 200
            hp_regen += 2
        elif talent == 'agility':
            stats['agility'] += 5
        else:
            stats['intelligence'] += 5
            mana += 100
            mana_regen += 2
    gear_components = {}
    for item in items_selected:
        for stat, value in item.get('stats', {}).items():
            gear_components[stat] = gear_components.get(stat, 0) + value
            if stat in stats:
                stats[stat] += value
            elif stat == 'health':
                hp += value
            elif stat == 'mana':
                mana += value
    secondary = attribute_secondary_delta(hero['base_stats'], stats)
    hp += secondary['hp']
    mana += secondary['mana']
    hp_regen += secondary['hp_regen'] + gear_components.get('hp_regen', 0)
    mana_regen += secondary['mana_regen'] + gear_components.get('mana_regen', 0)
    remaining = args.level - sum(allocations.values())
    damage_bonus = gear_components.get('damage', 0)
    damage_min = hero['weapon_min'] + stats[hero['primary']] + damage_bonus
    damage_max = hero['weapon_max'] + stats[hero['primary']] + damage_bonus
    result = {
        'hero': hero['name'], 'unit_id': hero['unit_id'], 'level': args.level,
        'primary': hero['primary'], 'skill_points_remaining_for_spells': remaining,
        'allocations': allocations, 'talents': talent_names,
        'stats': {key: round(value, 2) for key, value in stats.items()},
        'damage_range': [damage_min, damage_max],
        'hp': round(hp, 3), 'mana': round(mana, 3),
        'hp_regen': round(hp_regen, 3), 'mana_regen': round(mana_regen, 3),
        'armor': round(hero.get('base_armor', 0) + secondary['armor'] + gear_components.get('armor', 0), 3),
        'agility_attack_speed_bonus': round(stats['agility'] * ATTRIBUTE_CONSTANTS['AgiAttackSpeedBonus'], 3),
        'total_attack_speed_bonus': round(stats['agility'] * ATTRIBUTE_CONSTANTS['AgiAttackSpeedBonus'] + gear_components.get('attack speed', 0) / 100, 3),
        'talent_evasion_percent': 2 * talent_names.count('agility'),
        'tomes': tome_stats, 'items': [entry['rawcode'] for entry in items_selected],
        'equipped_item_components': gear_components,
        'effects': [item_effect_text(item) for item in items_selected
                    if item.get('effect') or item.get('effects')],
    }
    return json.dumps(result, indent=2)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--hero', help='Unit rawcode or display name for a custom projection')
    parser.add_argument('--level', type=int, default=1)
    parser.add_argument('--strength-points', type=int, default=0)
    parser.add_argument('--agility-points', type=int, default=0)
    parser.add_argument('--intelligence-points', type=int, default=0)
    parser.add_argument('--talents', default='', help='Comma-separated earned choices: STR, AGI, INT')
    parser.add_argument('--tomes', default='', help='Comma-separated purchased tome rawcodes')
    parser.add_argument('--items', default='', help='Comma-separated equipped item rawcodes')
    parser.add_argument('--output', type=Path, default=ROOT / 'docs/STAT-POWER-CURVE.md')
    args = parser.parse_args()
    try:
        heroes, provenance = load_heroes()
        items = item_catalog()
        if args.hero:
            print(custom_projection(args, heroes, items))
            return 0
        lines = curve_report(heroes) + item_report(items)
        lines.extend(['', '## Provenance', '',
                      f"- Warcraft installed build metadata SHA-256: `{provenance['build_info_sha256']}`",
                      f"- UnitBalance.slk SHA-256: `{provenance['files']['UnitBalance.slk']['sha256']}`",
                      f"- UnitWeapons.slk SHA-256: `{provenance['files']['UnitWeapons.slk']['sha256']}`",
                      '- Generated by `python -B tools/power_curve.py`.'])
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text('\n'.join(lines) + '\n', encoding='utf-8')
        print(args.output)
        return 0
    except (KeyError, OSError, ValueError) as error:
        parser.error(str(error))


if __name__ == '__main__':
    raise SystemExit(main())
