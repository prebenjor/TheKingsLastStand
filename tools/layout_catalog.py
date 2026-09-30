"""Shared runtime coordinates and editor-only layout references."""
from map_info import PLOTS
from hero_catalog import HERO_TYPES, NEW_HEROES
from faction_catalog import FACTIONS
from town_catalog import TOWNS, town_placements

POINTS = {
    'Castle': (0.0, -500.0), 'King': (0.0, 350.0),
    'Spring': (-900.0, -1600.0), 'HeroHub': (-10800.0, -10800.0),
}
HUB_COLUMNS = 5
HUB_SPACING = 450.0
MINE_OFFSET = (0.0, 1200.0)
ALTAR_OFFSET = (-650.0, -500.0)
WORKER_OFFSET = (-250.0, -300.0)


def market_placements():
    quality = ('Common', 'Uncommon', 'Rare', 'Epic', 'Legendary')
    result = [('hS00', -2300.0 + tier * 1150, -3900.0 - category * 560,
               quality[tier] + ' ' + ('Arms & Armor', 'Apparel & Relics')[category])
              for tier in range(5) for category in range(2)]
    return result + [('hS00', 3450.0, -3900.0, 'Field Apothecary'),
                     ('hS02', 4100.0, -3900.0, "Sage's Archive"),
                     ('hS00', 4850.0, -3900.0, 'Master Forge')]


def layout_globals():
    lines = []
    for name, (x, y) in POINTS.items():
        lines += [f'    real KLS_{name}X = {x:.1f}', f'    real KLS_{name}Y = {y:.1f}']
    for name, (x, y) in (('MineOffset', MINE_OFFSET), ('AltarOffset', ALTAR_OFFSET), ('WorkerOffset', WORKER_OFFSET)):
        lines += [f'    real KLS_{name}X = {x:.1f}', f'    real KLS_{name}Y = {y:.1f}']
    return '\n'.join(lines + [f'    integer KLS_HubColumns = {HUB_COLUMNS}',
                              f'    real KLS_HubSpacing = {HUB_SPACING:.1f}'])


def plot_script():
    return '\n'.join(f'    set KLS_{axis}[{i}] = {value:g}'
                     for axis, coordinate in (('X', 0), ('Y', 1))
                     for i, point in enumerate(PLOTS) for value in (point[coordinate],))


def market_script():
    lines = []
    for axis, coordinate in (('X', 1), ('Y', 2)):
        lines += [f'function KLS_Market{axis} takes integer index returns real']
        for i, placement in enumerate(market_placements()):
            lines += [f'    if index == {i} then', f'        return {placement[coordinate]:.1f}', '    endif']
        lines += ['    return 0.0', 'endfunction']
    return '\n'.join(lines)


def editor_placements():
    """(type, x, y, label) previews; ownership reserved to Neutral Extra."""
    result = [(raw, *POINTS[name], label) for raw, name, label in (
        ('hC01', 'Castle', "King Aldric's Castle"), ('Hpal', 'King', 'King Aldric'),
        ('nfoh', 'Spring', "King's Restoring Spring"))]
    result += market_placements()
    faction_by_race = {f['race']: f for f in FACTIONS}
    for race, rawcode, x, y in town_placements():
        rawcode = {'shop': 'hS00', 'tower': faction_by_race[race]['towers'][0]}.get(rawcode, rawcode)
        town = next(t for t in TOWNS if t['race'] == race)
        result.append((rawcode, x, y, town['name'] + ' / ' + rawcode))
    heroes = list(HERO_TYPES) + [h['unit_id'] for h in NEW_HEROES]
    hx, hy = POINTS['HeroHub']
    result += [(raw, hx + (i % HUB_COLUMNS) * HUB_SPACING,
                hy + (i // HUB_COLUMNS) * HUB_SPACING, 'Hero choice ' + str(i + 1))
               for i, raw in enumerate(heroes)]
    for i, (x, y) in enumerate(PLOTS):
        label = f'Player {i + 1} provisional base (race set by hero choice)'
        result += [('htow', x, y, label),
                   ('ngol', x + MINE_OFFSET[0], y + MINE_OFFSET[1], label + ' / mine'),
                   ('h000', x + ALTAR_OFFSET[0], y + ALTAR_OFFSET[1], label + ' / altar')]
    return result
