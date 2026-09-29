"""Rank selected Warcraft hero skills through level 50 using installed data."""
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
MAX_HERO_LEVEL = 50
MAX_SPELL_RANK = 5
MAX_NATIVE_DATA_RANK = MAX_SPELL_RANK
EXTRA_RANK_POWER_STEP = 0.10
STAT_ABILITY_IDS = ('KSTR', 'KAGI', 'KINT')
STAT_ABILITY_NAMES = ('+3 Strength', '+3 Agility', '+3 Intelligence')

# Only fields whose installed meaning is a spell's power are extended. Every
# other field is copied from the final authored rank, preserving costs,
# cooldowns, duration, range, targeting, and mechanics. Abilities missing a
# registered nonzero power field keep their native rank cap.
SCALABLE_EFFECT_FIELDS = {
    'AHhb': ('Hhb1',),                    # Holy Light heal / damage
    'AHad': ('Had1',),                    # Devotion Aura armor
    'AHtb': ('Htb1',),                    # Storm Bolt damage
    'AHtc': ('Htc1',),                    # Thunder Clap damage
    'AHbh': ('Hbh1', 'Hbh3'),             # Bash proc chance / bonus damage
    'AHav': ('Hav1', 'Hav2', 'Hav3'),     # Avatar armor, health, damage
    'AHfs': ('Hfs1', 'Hfs3', 'Hfs6'),     # Flame Strike damage values
    'AHbn': ('Hbn1',),                    # Banish movement-speed reduction
    'AHpa': ('hsa1', 'hsa2'),             # Forsaken Paladin Sacred Aura
    'AHas': ('hsa1', 'hsa2'),             # Ilastar Sacred Aura
    'AHfa': ('Hfa1',),                    # Searing Arrows bonus damage
    'AOwk': ('Owk3',),                    # Wind Walk bonus damage
    'AOcr': ('Ocr2',),                    # Critical Strike multiplier
    'AOww': ('Oww1',),                    # Bladestorm damage
    'AOcl': ('Ocl1',),                    # Chain Lightning damage
    'AOsh': ('Osh1',),                    # Shockwave damage
    'AOws': ('Wrs1',),                    # War Stomp damage
    'AOae': ('Oae1', 'Oae2'),             # Endurance Aura move/attack speed
    'AOhw': ('Ocl1',),                    # Healing Wave amount
    'AEmb': ('Emb1',),                    # Mana Burn amount
    'AEim': ('Eim1',),                    # Immolation damage
    'AEev': ('Eev1',),                    # Evasion chance
    'AEer': ('Eer1',),                    # Entangling Roots damage
    'AEah': ('Eah1',),                    # Thorns Aura reflected damage
    'AEar': ('Ear1',),                    # Trueshot Aura damage bonus
    'AEfk': ('Efk1', 'Efk2'),             # Fan of Knives damage / total cap
    'AEsh': ('Esh1', 'Esh5'),             # Shadow Strike poison / initial damage
    'AEtq': ('Etq1',),                    # Tranquility healing
    'AEme': ('Eme5',),                    # Metamorphosis bonus health
    'AEsf': ('Esf1',),                    # Starfall damage
    'AUdc': ('Udc1',),                    # Death Coil damage / healing
    'AUau': ('Uau1', 'Uau2'),             # Unholy Aura speed / regeneration
    'AUdr': ('Udp1',),                    # Dark Ritual mana conversion
    'AUfn': ('Ufn1',),                    # Frost Nova damage
    'AUdd': ('Udd1',),                    # Death and Decay damage fraction
}

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

from hero_catalog import NEW_HEROES
HERO_ABILITIES.update({entry['unit_id']: entry['abilities'] for entry in NEW_HEROES})

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


def _native_level_cap(data_row, headers):
    column_by_name = {name: index for index, name in headers.items()}
    levels_column = column_by_name.get('levels')
    try:
        levels = int(float(data_row.get(levels_column, MAX_NATIVE_DATA_RANK)))
    except (TypeError, ValueError):
        levels = MAX_NATIVE_DATA_RANK
    return max(1, min(MAX_NATIVE_DATA_RANK, levels))


def _effect_field_entries(ability_id, data_row, headers, metadata, native_level_cap):
    """Find configured, numeric power fields actually present in this object."""
    column_by_name = {name: index for index, name in headers.items()}
    code_column = column_by_name.get('code')
    ability_codes = {ability_id}
    if code_column is not None and data_row.get(code_column):
        ability_codes.add(data_row[code_column])
    configured = set(SCALABLE_EFFECT_FIELDS.get(ability_id, ()))
    found = set()
    for entry in metadata:
        field_id = entry[1]
        if field_id not in configured or entry.get(3) != 'AbilityData':
            continue
        allowed = entry.get(23, '')
        if allowed and ability_codes.isdisjoint(allowed.split(',')):
            continue
        column_base = entry.get(2, '')
        pointer = int(entry.get(6, '0') or 0)
        if column_base == 'Data':
            if pointer < 1 or pointer > len(_DATA_LETTERS):
                continue
            column_base = 'Data' + _DATA_LETTERS[pointer - 1]
        values = []
        for rank in range(1, native_level_cap + 1):
            raw = data_row.get(column_by_name.get(column_base + str(rank), -1), '').strip()
            if raw in ('', '-'):
                continue
            try:
                values.append(float(raw))
            except (TypeError, ValueError):
                continue
        if values and max(values) > 0:
            found.add(field_id)
    return found


def _effective_level_cap(ability_id, data_row, headers, metadata):
    native_level_cap = _native_level_cap(data_row, headers)
    if _effect_field_entries(ability_id, data_row, headers, metadata, native_level_cap):
        return MAX_SPELL_RANK
    return native_level_cap


def _modification_fields(ability_id, data_row, headers, metadata):
    native_level_cap = _native_level_cap(data_row, headers)
    effect_field_ids = _effect_field_entries(
        ability_id, data_row, headers, metadata, native_level_cap)
    effective_level_cap = MAX_SPELL_RANK if effect_field_ids else native_level_cap
    fields = [('alev', 0, 0, 0, effective_level_cap)]
    seen = {('alev', 0, 0)}
    column_by_name = {name: index for index, name in headers.items()}
    code_column = column_by_name.get('code')
    ability_codes = {ability_id}
    if code_column is not None and data_row.get(code_column):
        ability_codes.add(data_row[code_column])
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
        for rank in range(1, native_level_cap + 1):
            raw = data_row.get(column_by_name.get(column_base + str(rank), -1), '').strip()
            if raw not in ('', '-'):
                native_values.append((rank, raw))
        if not native_values:
            continue
        previous = []
        for rank in range(1, effective_level_cap + 1):
            if rank <= native_level_cap:
                raw = data_row.get(column_by_name.get(column_base + str(rank), -1), '').strip()
            else:
                raw = ''
            if raw in ('', '-'):
                if not previous:
                    continue
                raw = previous[-1][1]
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
            if rank > native_level_cap and field_id in effect_field_ids and value_kind in ('unreal', 'real', 'int') and value > 0:
                scaled = value * (1.0 + EXTRA_RANK_POWER_STEP * (rank - native_level_cap))
                value = int(scaled + 0.5) if value_kind == 'int' else scaled
            key = (field_id, rank, pointer)
            if key not in seen:
                fields.append((field_id, typ, rank, pointer, value))
                seen.add(key)
            previous.append((rank, raw))
    return fields


def _sacred_aura_tooltips(fields):
    """Describe all safe Sacred Aura ranks in both learned and learn-menu tips."""
    rank_values = {}
    for field_id, _, rank, _, value in fields:
        if field_id in ('hsa1', 'hsa2') and rank:
            rank_values.setdefault(rank, {})[field_id] = value

    def percent(value):
        return f'{value:g}'

    result = []
    rank_summary = []
    for rank in range(1, MAX_SPELL_RANK + 1):
        values = rank_values.get(rank, {})
        resistance = round(float(values['hsa1']) * 100, 1)
        healing = round(float(values['hsa2']), 1)
        rank_summary.append(
            f'Rank {rank}: {percent(resistance)}% Magic Resistance, '
            f'{percent(healing)}% increased healing received.')

    for rank, summary in enumerate(rank_summary, start=1):
        values = rank_values[rank]
        resistance = percent(round(float(values['hsa1']) * 100, 1))
        healing = percent(round(float(values['hsa2']), 1))
        current = 'not learned' if rank == 1 else str(rank - 1)
        required_hero_level = 1 + (rank - 1) * 2
        normal_title = f'Sacred Aura - |cffffcc00Level {rank}|r'
        normal_text = (
            f'Current rank: {rank}|nGives {resistance}% Magic Resistance and '
            f'{healing}% increased healing received to nearby friendly units.')
        learn_title = f'Learn Sacred Aura - |cffffcc00Level {rank}|r'
        learn_text = (
            f'Current rank: {current}|nNext rank: {rank}|n'
            f'Requires hero level: {required_hero_level}|n'
            + '|n'.join(rank_summary))
        result.extend((
            ('atp1', 3, rank, 0, normal_title),
            ('aub1', 3, rank, 0, normal_text),
            ('aut1', 3, rank, 0, learn_title),
            ('auu1', 3, rank, 0, learn_text),
        ))
    return result


def hero_ability_records(ability_builder):
    """Return safe rank overrides for the selected heroes' native skills."""
    headers, data, metadata = _ability_tables()
    records = []
    ability_ids = sorted({spell for spells in HERO_ABILITIES.values() for spell in spells})
    missing = [spell for spell in ability_ids if spell not in data]
    if missing:
        raise ValueError('Hero spell IDs absent from installed AbilityData.slk: ' + ', '.join(missing))
    for spell in ability_ids:
        row = data[spell]
        fields = _modification_fields(spell, row, headers, metadata)
        if spell in ('AHas', 'AHpa'):
            fields.extend(_sacred_aura_tooltips(fields))
        if len(fields) < 2:
            raise ValueError('No installed per-rank ability data found for ' + spell)
        records.append(ability_builder(spell, '\0' * 4, fields))
    return records


def hero_choice_ability_records(ability_builder):
    """Create three distinct native + skills for repeatable single-stat choices."""
    records = []
    choices = zip(STAT_ABILITY_IDS, STAT_ABILITY_NAMES, (2, 0, 1))
    for code, name, selected in choices:
        label = name[3:]
        fields = [
            ('alev', 0, 0, 0, MAX_HERO_LEVEL),
            ('arlv', 0, 0, 0, 1),
            ('alsk', 0, 0, 0, 1),
            ('anam', 3, 0, 0, name),
            # The tooltip/name fields are Profile fields. They must be written
            # at level zero; attaching them to AbilityData rank indices leaves
            # every clone showing Aamk's identical default text in Warcraft.
            ('atp1', 3, 0, 0, f'Learn {name}'),
            ('aub1', 3, 0, 0,
             f'Choosing this skill permanently adds 3 {label}. It can be chosen again with a future hero skill point.'),
            ('aut1', 3, 0, 0, name),
            ('auu1', 3, 0, 0,
             f'Permanently adds 3 {label}. Choose it alongside your other hero abilities.'),
        ]
        for rank in range(1, MAX_HERO_LEVEL + 1):
            total = rank * 3
            fields.extend((
                ('Iagi', 0, rank, 1, total if selected == 0 else 0),
                ('Iint', 0, rank, 2, total if selected == 1 else 0),
                ('Istr', 0, rank, 3, total if selected == 2 else 0),
            ))
        records.append(ability_builder('Aamk', code, fields))
    return records


def spell_script():
    headers, data, metadata = _ability_tables()
    lines = [
        'function KLS_RankHeroSpell takes unit hero, integer spellId, integer heroLevel, integer unlockLevel, integer maxRank returns nothing',
        '    local integer rank',
        '    if heroLevel < unlockLevel then',
        '        return',
        '    endif',
        '    set rank = IMinBJ(maxRank, IMinBJ(5, 1 + (heroLevel - unlockLevel) / 10))',
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
            max_rank = _effective_level_cap(spell, row, headers, metadata)
            lines.append("        call KLS_RankHeroSpell(hero, '" + spell + "', heroLevel, " + str(unlock) + ', ' + str(max_rank) + ')')
    lines += [
        '    endif',
        "    if heroType == 'Ekee' or heroType == 'Efal' then",
        "        call UnitRemoveAbility(hero, 'AEfn')",
        '    endif',
        'endfunction',
    ]
    return '\n'.join(lines)
