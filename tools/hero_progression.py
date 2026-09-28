"""Rank the selected Warcraft hero skills through level 100 using installed data."""
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
MAX_HERO_LEVEL = 100
MAX_SPELL_RANK = 10
MAX_NATIVE_DATA_RANK = 6

# Hero types and the four native Warcraft skills shown by the selector. The
# Priest is the map's custom human hero, with the spell set from its tooltip.
HERO_ABILITIES = {
    'Hpal': ('AHhb', 'AHds', 'AHad', 'AHre'),
    'Hmkg': ('AHtb', 'AHtc', 'AHbh', 'AHav'),
    'H000': ('AHhb', 'AHab', 'AHds', 'AHre'),
    'Hblm': ('AHfs', 'AHbn', 'AHdr', 'AHpx'),
    'Obla': ('AOwk', 'AOmi', 'AOcr', 'AOww'),
    'Ofar': ('AOcl', 'AOfs', 'AOsf', 'AOeq'),
    'Otch': ('AOsh', 'AOws', 'AOae', 'AOre'),
    'Oshd': ('AOhw', 'AOhx', 'AOsw', 'AOvd'),
    'Edem': ('AEmb', 'AEim', 'AEev', 'AEme'),
    'Ekee': ('AEer', 'AEfn', 'AEah', 'AEtq'),
    'Emoo': ('AEst', 'AHfa', 'AEar', 'AEsf'),
    'Ewar': ('AEfk', 'AEbl', 'AEsh', 'AEsv'),
    'Udea': ('AUdc', 'AUdp', 'AUau', 'AUan'),
    'Ulic': ('AUfn', 'AUfu', 'AUdr', 'AUdd'),
    'Nbrn': ('ANsi', 'ANba', 'ANdr', 'ANch'),
    # Forsaken Kingdom campaign heroes verified against installed Definitive
    # Edition UnitAbilities.slk and UnitUI.slk data.
    'Hjsm': ('AHas', 'AHsf', 'AHmc', 'AHsl'),
    'Npal': ('AHcr', 'ANcp', 'AHpa', 'AHcl'),
}

_DATA_LETTERS = 'ABCDEFGHIJKLMNOPQRST'
_FIELD_TYPE = {
    'unreal': 2,
    'real': 2,
    'int': 0,
    'bool': 0,
    'string': 3,
    'targetList': 3,
    'unitList': 3,
    'buffList': 3,
    'effectList': 3,
    'modelList': 3,
}


def _slk(path):
    rows = {}
    y = 0
    for line in path.read_text().splitlines():
        if not line.startswith('C;'):
            continue
        match = re.search(r';Y(\d+)', line)
        if match:
            y = int(match.group(1))
        x = re.search(r';X(\d+)', line)
        value = re.search(r';K(.*)', line)
        if x and value:
            rows.setdefault(y, {})[int(x[1])] = value[1].strip('"')
    return rows


def _ability_tables():
    folder = ROOT / 'tools/reference/installed'
    data_rows = _slk(folder / 'AbilityData.slk')
    metadata_rows = _slk(folder / 'AbilityMetaData.slk')
    data_headers = data_rows[1]
    data = {row.get(1): row for row in data_rows.values() if row.get(1)}
    metadata = [row for row in metadata_rows.values() if row.get(1)]
    return data_headers, data, metadata


def _median_native_slope(previous):
    steps = []
    for index in range(1, len(previous)):
        before_rank, before_value = previous[index - 1]
        rank, current_value = previous[index]
        try:
            step = (float(current_value) - float(before_value)) / (rank - before_rank)
        except (TypeError, ValueError, ZeroDivisionError):
            continue
        if step != 0:
            steps.append(step)
    if not steps:
        return 0.0
    steps.sort()
    middle = len(steps) // 2
    if len(steps) % 2:
        return steps[middle]
    return (steps[middle - 1] + steps[middle]) * 0.5


def _rank_value(value, previous, kind, row, column_base, level, native_max_rank):
    """Continue a numeric curve after its actual last installed rank."""
    numeric = kind in ('unreal', 'real', 'int')
    if not numeric or len(previous) < 2:
        return previous[-1][1] if previous else value
    last_rank, last_value = previous[-1]
    try:
        last = float(last_value)
    except (TypeError, ValueError):
        return last_value
    slope = _median_native_slope(previous)
    if slope == 0:
        return last_value
    # Preserve every installed value, then continue the most recent changing
    # native step at half strength. This also handles native curves that plateau
    # for one or more ranks before their actual final rank.
    extended = last + slope * (level - native_max_rank) * 0.5
    if column_base in ('Cool', 'Dur', 'HeroDur'):
        extended = max(1.0, extended)
    elif column_base == 'Cost':
        extended = max(0.0, extended)
    elif column_base == 'Area' or column_base == 'Rng':
        extended = max(0.0, extended)
    if kind == 'int':
        return str(max(0, round(extended)))
    return str(extended)


def _modification_fields(ability_id, data_row, headers, metadata):
    fields = [('alev', 0, 0, 0, MAX_SPELL_RANK)]
    seen = {('alev', 0, 0)}
    column_by_name = {name: index for index, name in headers.items()}
    code_column = column_by_name.get('code')
    ability_codes = {ability_id}
    if code_column is not None and data_row.get(code_column):
        ability_codes.add(data_row[code_column])
    levels_column = column_by_name.get('levels')
    try:
        declared_levels = int(float(data_row.get(levels_column, MAX_NATIVE_DATA_RANK)))
    except (TypeError, ValueError):
        declared_levels = MAX_NATIVE_DATA_RANK
    declared_levels = max(1, min(MAX_NATIVE_DATA_RANK, declared_levels))
    for entry in metadata:
        field_id = entry[1]
        if field_id == 'alev' or entry.get(3) != 'AbilityData':
            continue
        allowed = entry.get(23, '')
        if allowed and ability_codes.isdisjoint(allowed.split(',')):
            continue
        value_kind = entry.get(10, '')
        typ = _FIELD_TYPE.get(value_kind)
        if typ is None:
            continue
        column_base = entry.get(2, '')
        pointer = int(entry.get(6, '0') or 0)
        if column_base == 'Data':
            if pointer < 1 or pointer > len(_DATA_LETTERS):
                continue
            column_base = 'Data' + _DATA_LETTERS[pointer - 1]
        if not any(name.startswith(column_base) and name[len(column_base):].isdigit()
                   for name in headers.values()):
            continue
        native_values = []
        for rank in range(1, declared_levels + 1):
            raw = data_row.get(column_by_name.get(column_base + str(rank), -1), '').strip()
            if raw not in ('', '-'):
                native_values.append((rank, raw))
        if not native_values:
            continue
        native_max_rank = native_values[-1][0]
        previous = []
        for rank in range(1, MAX_SPELL_RANK + 1):
            if rank <= native_max_rank:
                raw = data_row.get(column_by_name.get(column_base + str(rank), -1), '').strip()
                if raw in ('', '-'):
                    if not previous:
                        continue
                    raw = previous[-1][1]
            else:
                raw = _rank_value(previous[-1][1], previous, value_kind,
                                  data_row, column_base, rank, native_max_rank)
            if value_kind in ('unreal', 'real'):
                try:
                    value = float(raw)
                except (TypeError, ValueError):
                    continue
            elif value_kind in ('int', 'bool'):
                try:
                    value = int(float(raw))
                except (TypeError, ValueError):
                    continue
            else:
                value = raw
            key = (field_id, rank, pointer)
            if key not in seen:
                fields.append((field_id, typ, rank, pointer, value))
                seen.add(key)
            if rank <= native_max_rank:
                previous.append((rank, raw))
    return fields


def hero_ability_records(ability_builder):
    """Return base-object overrides that extend every selectable skill to 10."""
    headers, data, metadata = _ability_tables()
    records = []
    ability_ids = sorted({spell for spells in HERO_ABILITIES.values() for spell in spells})
    missing = [spell for spell in ability_ids if spell not in data]
    if missing:
        raise ValueError('Hero spell IDs absent from installed AbilityData.slk: ' + ', '.join(missing))
    for spell in ability_ids:
        row = data[spell]
        fields = _modification_fields(spell, row, headers, metadata)
        if len(fields) < 2:
            raise ValueError('No installed per-rank ability data found for ' + spell)
        # The stock strings cover only the original spell ranks. Give ranks
        # 7–10 explicit tooltips rather than leaving blank level cards.
        name = row.get(3, spell).split(' - ', 1)[-1]
        for rank in range(MAX_NATIVE_DATA_RANK + 1, MAX_SPELL_RANK + 1):
            fields.append(('atp1', 3, rank, 0, name + ' - Rank ' + str(rank)))
            fields.append(('aub1', 3, rank, 0,
                           'Rank ' + str(rank) + ' of this hero ability. Its installed spell values continue to scale for the extended defense.'))
        records.append(ability_builder(spell, '\0' * 4, fields))
    return records


def spell_script():
    headers, data, _ = _ability_tables()
    lines = [
        'function KLS_RankHeroSpell takes unit hero, integer spellId, integer heroLevel, integer unlockLevel returns nothing',
        '    local integer rank',
        '    if heroLevel < unlockLevel then',
        '        return',
        '    endif',
        '    set rank = IMinBJ(10, 1 + (heroLevel - unlockLevel) / 10)',
        '    if GetUnitAbilityLevel(hero, spellId) == 0 then',
        '        call UnitAddAbility(hero, spellId)',
        '        call UnitMakeAbilityPermanent(hero, true, spellId)',
        '    endif',
        '    if GetUnitAbilityLevel(hero, spellId) < rank then',
        '        call SetUnitAbilityLevel(hero, spellId, rank)',
        '    endif',
        'endfunction',
        'function KLS_ApplySpellRanks takes unit hero returns nothing',
        '    local integer heroType = GetUnitTypeId(hero)',
        '    local integer heroLevel = GetHeroLevel(hero)',
    ]
    for index, (hero_type, abilities) in enumerate(HERO_ABILITIES.items()):
        branch = 'if' if index == 0 else 'elseif'
        lines.append("    " + branch + " heroType == '" + hero_type + "' then")
        for spell in abilities:
            row = data[spell]
            unlock = max(1, int(float(row.get(12, '1') or 1)))
            lines.append("        call KLS_RankHeroSpell(hero, '" + spell + "', heroLevel, " + str(unlock) + ')')
    lines += ['    endif', 'endfunction']
    return '\n'.join(lines)
