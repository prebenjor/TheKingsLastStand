"""Generate the approved access matrix from baseline and reopened MCP evidence."""
import json,sys
from pathlib import Path
from faction_catalog import FACTIONS

def generate(folder,target):
    folder=Path(folder)
    baseline=json.loads((folder/'building-matrix-before.json').read_text())
    final=json.loads((folder/'mcp-racial-readback.json').read_text())
    lines=['# Racial building access matrix — 2026-10-02','',
      'Captured from the saved R2 baseline and the reopened racial repair map through Forge MCP. Rawcodes identify native prerequisites, training, research and upgrade products. A dash means no product in that field; inherited native fields retain their baseline values. This is object evidence, not native gameplay acceptance.','',
      'The failure was the replacement of native worker build lists with mixed standard/custom buildings, including twelve entries and overlapping command positions. Native production definitions remained present but several were unreachable. Undead tier-two prerequisites also referenced the Slaughterhouse as a blacksmith; Graveyard is restored.','',
      'Installed data supplies field definitions and native inheritance; [Blizzard’s Night Elf building reference](https://classic.battle.net/war3/nightelf/buildingstats.shtml) cross-checks the native roster. Wisps gather lumber from trees without a Lumber Mill. Native town-hall and tower upgrades remain in their original chains.','']
    for f in FACTIONS:
        lines+=['## '+f['race'],'',
          'Worker `'+f['worker']+'`; standard menu contains '+str(len(f['standard_menu']))+' buildings plus native Cancel. Expansion worker `'+f['expansion_worker']+'` is prototype-only until native acceptance.','',
          '| Building | Construction access before → after | Prerequisites | Upgrades | Recruits | Research | Harvesting / utility | Position |',
          '|---|---|---|---|---|---|---|---|']
        old=baseline[f['worker']]['fields']['ubui'].split(',')
        identities=f['standard_menu']+f['expansion_menu']
        # Include captured upgrade definitions and legacy wrappers for context.
        identities+= [i for i,e in baseline.items() if i not in identities and (i in (f['town_hall'],f['arcane']) or e['fields'].get('urac')==f['race'].lower().replace('night elf','nightelf') and e['fields'].get('uupt'))]
        for identity in dict.fromkeys(identities):
            entry=baseline[identity];fields=dict(entry['fields']);fields.update(final['units'].get(identity,{}).get('fields',{}))
            page='standard' if identity in f['standard_menu'] else 'expansion (gated)' if identity in f['expansion_menu'] else 'upgrade / legacy'
            utility='lumber drop-off' if identity in ('hlum','ofor','ugrv') else 'native gold/lumber economy' if identity==f['town_hall'] else 'food' if identity==f['food'] else 'production / service'
            cell=lambda field: str(fields.get(field,'') or '—').replace('|','/')
            position=(f'{f["standard_menu"].index(identity)%4},{f["standard_menu"].index(identity)//4}' if identity in f['standard_menu'] else f'{f["expansion_menu"].index(identity)%4},{f["expansion_menu"].index(identity)//4}' if identity in f['expansion_menu'] else cell('ubpx'))
            lines.append('| '+entry['name']+' `'+identity+'` | '+('available' if identity in old else 'absent')+' → '+page+' | '+cell('ureq')+' | '+cell('uupt')+' | '+cell('utra')+' | '+cell('ures')+' | '+utility+' | '+position+' |')
        lines+=['']
    lines+=['## Command card acceptance','',
      'Specialist training is at (0,0), hero-company purchases at (3,0); construction pages have explicit row-major positions. Native rally, research, sale stock, Cancel, hotkeys and each complete prerequisite path require engine checks. Foundries retain upgrades/recipes and do not train specialists. Native item-stock button placement is inherited and must be visually tested.','']
    Path(target).write_text('\n'.join(lines),encoding='utf-8')

if __name__=='__main__':generate(*sys.argv[1:])
