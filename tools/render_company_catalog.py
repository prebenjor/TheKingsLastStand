"""Generate the authored company powers and personal research reference."""
from pathlib import Path
from company_catalog import HERO_COMPANIES, company_research_catalog
from wave_rosters import SIEGE_UNIT_CODES


def render():
    lines = ['# Company powers and research', '',
             'Generated from `tools/company_catalog.py`. These are current source values; Warcraft command-card rendering, pathing, native item purchase timing and multiplayer effects require exact-build acceptance.', '',
             '## Authored recruit powers', '',
             'Each power is an installed Channel (`ANcl`) clone: point target, 600 cast range, 250 effect radius, 40 mana, 20-second cooldown. Recruits have 180 initial/maximum mana and 1 native mana regeneration. Damage targets enemies; healing/mana target friendly living troops of any race, excluding structures and King Aldric. Optional slow is 20% for 2 seconds. Chapter research adds 15% potency per rank; Arcane adds 25% for supports, additively. Manual casts are required.', '',
             '| Hero | Recruit / rawcode | Installed parent | Gold / lumber | Base HP / damage | Power / rawcode | Damage / heal / mana | Slow |',
             '|---|---|---|---:|---:|---|---:|---|']
    for entry in HERO_COMPANIES:
        for index, role in enumerate(('company', 'support')):
            power = entry['powers'][index]
            lines.append(f"| {entry['hero_name']} | {entry[role+'_name']} / `{entry[role+'_id']}` | `{entry[role+'_parent']}` | {entry[role+'_gold']} / {entry[role+'_lumber']} | {entry[role+'_hp']} / {entry[role+'_damage']} | {power['name']} / `{entry[role+'_ability']}` | {power['damage']} / {power['heal']} / {power['mana']} | {'Yes' if power['slow'] else 'No'} |")
    lines += ['', '## Personal research services', '',
              'Buy services at your completed matching building with your living selected hero within 700 range. Native purchase charges the displayed gold/lumber once. Wrong ownership, invalid progression or an obsolete rank refunds both costs. Service items are removed; ranks apply to existing and future recruits. Completing a Foundry grants +20% base health/damage once, independently of these branches.', '',
              '| Service | Rawcode | Building role | Rank | Gold / lumber | Effect / prerequisite |',
              '|---|---|---|---:|---:|---|']
    for entry in company_research_catalog():
        lines.append(f"| {entry['name']} | `{entry['rawcode']}` | {entry['role']} | {entry['rank']} | {entry['gold']} / {entry['lumber']} | {entry['description']} |")
    lines += ['', '## Bookkeeping and siege targets', '',
              'Company totals use additive deltas against the catalog base, preserving unrelated native effects. Fresh native stock purchases clear recycled handle bookkeeping before applying bonuses. Construction starts clear stale completion flags. Ordinary death retains totals so resurrection does not stack bonuses; later research adds only its new delta.', '',
              'Counter-Siege affects positive attack damage from the owner’s matching support against enemy structures or these actual invasion siege roles: '+', '.join('`'+code+'`' for code in SIEGE_UNIT_CODES)+'. It does not amplify spells or ordinary infantry damage.', '',
              'Regenerate with `python -X utf8 -B tools/render_company_catalog.py`.', '']
    return '\n'.join(lines)


if __name__ == '__main__':
    output = Path(__file__).resolve().parents[1] / 'docs/COMPANY-RESEARCH-AND-POWERS.md'
    output.write_text(render(), encoding='utf-8')
    print(output)
