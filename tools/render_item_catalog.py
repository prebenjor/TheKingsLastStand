"""Render the human-readable item reference from the shared runtime catalog."""
from pathlib import Path
import json
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'tools'))

from equipment_catalog import (ENEMY_DROP_THRESHOLDS,
                               ENEMY_POTION_THRESHOLDS_PER_1000,
                               RARITY_COLORS, TIERS, attribute_books,
                               item_catalog)
from recipes import recipe_catalog


SLOTS = {1: 'Head', 2: 'Chest', 3: 'Gloves', 4: 'Boots', 5: 'Ring',
         6: 'Primary', 7: 'Offhand', 8: 'Trinket'}


def effect_text(item):
    effects = item.get('effects', [])
    if not effects:
        return item.get('effect', '') or '—'
    rendered = []
    for effect in effects:
        value = (f"{effect['name']}: {effect['magnitude']} {effect['unit']} "
                 f"on {effect['trigger']}")
        if effect.get('duration'):
            value += ', duration ' + effect['duration']
        if effect.get('cooldown'):
            value += ', cooldown ' + effect['cooldown']
        if effect.get('radius'):
            value += f", radius {effect['radius']}"
        rendered.append(value)
    return '; '.join(rendered)


def render():
    items = item_catalog()
    books = attribute_books()
    recipes = recipe_catalog(items)
    color_names = {
        'Common': '#FFFFFF', 'Uncommon': '#1EFF00', 'Rare': '#0070DD',
        'Epic': '#A335EE', 'Legendary': '#FF8000',
    }
    lines = [
        '# Generated item catalog', '',
        'Generated from `tools/equipment_catalog.py` and `tools/recipes.py`. '
        'Contains 80 shared equipment items, 20 race-themed universal relics, '
        'three additional crafted Legendary items, nine tomes and seven recipe '
        'scrolls. The source catalog owns names, rawcodes, slots, prices, stats, '
        'rarity colors, effects, shop/drop stock and recipe components. '
        'Regenerate with `python -B tools/render_item_catalog.py` after catalog '
        'changes. The boss relics are defined separately in `tools/objects.py` '
        'and summarized below.', '',
        '| Rarity | Race/theme | Family | Item | Rawcode | Slot | Gold | Numeric stats | Effect |',
        '|---|---|---|---|---|---|---:|---|---|',
    ]
    for item in items:
        quality = item.get('quality', TIERS[item['tier']][0])
        stats = ', '.join(f'+{value:g} {name}'
                          for name, value in item.get('stats', {}).items()) or '—'
        theme = item.get('race', 'General')
        if item.get('crafted'):
            theme = 'General crafted'
        lines.append(
            f"| {quality} ({color_names[quality]}) | {theme} | {item['family']} | "
            f"{item['name']} | {item['rawcode']} | "
            f"{item.get('slot_name', SLOTS.get(item.get('slot'), 'Unknown'))} | "
            f"{item['price']:,} | {stats} | {effect_text(item)} |"
        )

    lines.extend([
        '', '## Recipe catalog', '',
        '| Recipe | Rawcode | Components (rawcode) | Output | Cost |',
        '|---|---|---|---|---:|',
    ])
    item_by_code = {item['rawcode']: item for item in items}
    for recipe in recipes:
        component_names = ' + '.join(
            f"{item_by_code[code]['name']} ({code})"
            for code in recipe['components'])
        output = item_by_code[recipe['output']]
        lines.append(
            f"| {recipe['name']} | {recipe['rawcode']} | {component_names} | "
            f"{output['name']} ({recipe['output']}) | {recipe['price']:,} |"
        )

    lines.extend([
        '', '## Rarity palette and drop eligibility', '',
        '| Quality | Color | Base shop price |',
        '|---|---|---:|',
    ])
    for quality, price in TIERS:
        lines.append(f'| {quality} | `{color_names[quality]}` | {price:,} |')
    lines.extend([
        '', 'The general Blade, Bow and Staff families cost 1.5× their rarity '
        'base price. Other catalog equipment uses its rarity base; authored '
        'recipe and tome prices are listed above and below.', '',
        '| Enemy class | Common | Uncommon | Rare | Epic | Legendary | Total gear chance | Potion chance |',
        '|---|---:|---:|---:|---:|---:|---:|---:|',
    ])
    for key, label in (('normal', 'Normal'), ('elite', 'Elite'), ('boss', 'Boss')):
        thresholds = ENEMY_DROP_THRESHOLDS[key]
        per_rarity = [thresholds[0]] + [thresholds[n] - thresholds[n - 1]
                                        for n in range(1, len(thresholds))]
        chance = lambda rolls, denominator: f'{sum(rolls) / denominator:g}%'
        lines.append(
            f"| {label} | " + ' | '.join(f'{value / 100:g}%' for value in per_rarity) +
            f" | {chance(per_rarity, 100)} | "
            f"{ENEMY_POTION_THRESHOLDS_PER_1000[key] / 10:g}% |"
        )
    lines.extend([
        '', 'Normal and boss deaths never produce random catalog equipment. '
        'Elites have a 1% total equipment chance, split evenly between Common '
        'and Uncommon. Bosses instead grant one owner-bound milestone item '
        'per active player: Uncommon at wave 10, Rare at wave 20, Epic at wave '
        '30, and Legendary at wave 40 and every later boss milestone. The '
        'separate potion chance remains 4% / 8% / 18% for Normal / Elite / Boss.',
        '', '## Separate milestone boss relics', '',
        '| Boss wave | Rarity | Item | Rawcode | Slot | Authored numeric value/effect |',
        '|---:|---|---|---|---|---|',
        '| 10 | Uncommon | Gravetide Cleaver | I010 | Primary | +15 damage |',
        '| 20 | Rare | Heart of the Watch | I011 | Chest | Maximum-health bonus; numeric value is inherited from its native item parent |',
        '| 30 | Epic | Crown of Dawn | I012 | Trinket | Healing aura; numeric value is inherited from its native item parent |',
        '| 40 | Legendary | Oath of the Last King | I013 | Ring | +5 Strength, +5 Agility, +5 Intelligence |',
        '', 'The I011 and I012 bonuses are not numeric in the custom object description; '
        'do not infer their magnitude from rarity. Resolve the inherited ability '
        'values against installed item/ability data before including them in a '
        'numeric budget. Their current object definitions are in `tools/objects.py`.',
        '', '## Attribute tomes', '',
        '| Tome | Rawcode | Bonus | Price |',
        '|---|---|---:|---:|',
    ])
    for book in books:
        lines.append(
            f"| {book['name']} | {book['rawcode']} | +{book['amount']} "
            f"{book['stat']} | {book['price']:,} |"
        )
    manifest_path = ROOT / 'dist/build-manifest.json'
    if manifest_path.exists():
        manifest = json.loads(manifest_path.read_text(encoding='utf-8'))
        lines += ['', '## Current Development package', '',
                  'Build: `' + manifest['build_id'] + '`; package: `' + manifest['output_path'] + '`; SHA-256: `' + manifest['sha256'] + '`. Engine checks remain pending.']
    return '\n'.join(lines) + '\n'


if __name__ == '__main__':
    target = ROOT / 'docs/ITEM-CATALOG.md'
    target.write_text(render(), encoding='utf-8')
    print(target)
