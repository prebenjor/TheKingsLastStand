"""Regression contracts for racial mine access and faction building roles."""
import sys
import unittest
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'tools'))
sys.path.insert(0, str(ROOT / 'tests'))

from faction_catalog import FACTIONS
from equipment_catalog import abilities
from objects import units
from pipeline import runtime_script
from test_equipment import decode, slk
from hero_progression import HERO_ABILITIES, STAT_ABILITY_IDS
from hero_catalog import NEW_HEROES


def function_body(script, name):
    match = re.search(r'^function ' + re.escape(name) + r' takes [\s\S]*?^endfunction$', script, re.M)
    if not match:
        raise AssertionError('Missing runtime function ' + name)
    return match.group()


class RaceMiningAndBuildings(unittest.TestCase):
    def test_undead_arcane_building_uses_temple_parent_and_keeps_native_stock(self):
        undead = FACTIONS[3]
        self.assertEqual(undead['arcane_parent'], 'utod')
        base, fields = decode(units())[undead['arcane']]
        self.assertEqual(base, 'utod')
        self.assertNotIn(('utra', 0), fields)
        self.assertNotIn(('ures', 0), fields)
        self.assertNotIn(('urev', 0), fields)
        self.assertIn('Necromancers', fields[('utub', 0)][0])
        self.assertIn('Banshees', fields[('utub', 0)][0])
        self.assertEqual(fields[('uico', 0)][0],
                         r'ReplaceableTextures\CommandButtons\BTNTempleOfTheDamned.dds')

    def test_each_racial_worker_menu_and_custom_building_role_is_serialized(self):
        records = decode(units())
        for faction in FACTIONS:
            menu = records[faction['worker']][1][('ubui', 0)][0].split(',')
            self.assertEqual(menu, faction['build_menu'], faction['race'])
            self.assertEqual(len(menu), 12)
            for role, entry in faction['company_buildings'].items():
                base, fields = records[entry['rawcode']]
                self.assertEqual(base, entry['parent'], (faction['race'], role))
                self.assertEqual(fields[('utub', 0)][0], entry['tooltip'])

    def test_custom_building_tooltips_name_race_and_explain_their_real_roles(self):
        records = decode(units())
        for role in ('hall', 'foundry', 'siege_yard'):
            descriptions = [faction['company_buildings'][role]['tooltip'] for faction in FACTIONS]
            self.assertEqual(len(set(descriptions)), 4, role)
            self.assertTrue(all('Race-themed' not in description for description in descriptions))
        for faction in FACTIONS:
            race = faction['race']
            arcane = records[faction['arcane']][1][('utub', 0)][0]
            self.assertIn(race, arcane)
            self.assertNotIn('same role as the Human', arcane)
            for rawcode in faction['towers']:
                tooltip = records[rawcode][1].get(('utub', 0), ('',))[0]
                self.assertTrue(tooltip, (race, rawcode))
                self.assertNotIn('Race-themed', tooltip)
                self.assertIn(race, tooltip)
        self.assertIn('15 health', records['h003'][1][('utub', 0)][0])
        runtime = runtime_script('TOWER-ROLE-TEST')
        for faction in FACTIONS:
            self.assertIn("rawcode == '"+faction['towers'][2]+"'", runtime)
        self.assertIn('GroupEnumUnitsInRange(targets,GetUnitX(tower),GetUnitY(tower),650,null)', runtime)
        self.assertIn('GetWidgetLife(u)+15', runtime)
        self.assertIn('ModuloInteger(KLS_Seconds,3) == 0', runtime)

    def test_race_choice_sets_native_race_and_undead_workers_can_haunt_a_mine(self):
        runtime = runtime_script('MINING-TEST')
        self.assertIn('SetPlayerRacePreference(Player(p),racePreference)', runtime)
        self.assertIn('EVENT_PLAYER_UNIT_ISSUED_TARGET_ORDER', runtime)
        self.assertIn("GetUnitTypeId(worker) == 'uaco'", runtime)
        self.assertIn("GetUnitTypeId(mine) == 'ngol'", runtime)
        mining = function_body(runtime, 'KLS_HauntGoldMine')
        self.assertIn("KLS_CreateUnitOptional(Player(p),'ugol',GetUnitX(mine),GetUnitY(mine),GetUnitFacing(mine),\"Undead gold mine haunt\")", mining)
        self.assertIn('SetResourceAmount(haunted,amount)', runtime)
        self.assertIn('IssueTargetOrder(worker,"harvest",haunted)', runtime)
        self.assertNotIn("CreateUnit(Player(p),'ugol'", mining)
        checked = function_body(runtime, 'KLS_CreateUnitChecked')
        optional = function_body(runtime, 'KLS_CreateUnitOptional')
        self.assertIn('KLS_CreateUnitChecked(owner,kind,x,y,facing,false,context)', optional)
        self.assertNotIn('KLS_DiagFailureEvents', checked)
        self.assertIn('optional unit spawn failed context=', checked)
        self.assertIn('SetPlayerRacePreference(Player(0), RACE_PREF_RANDOM)', runtime)
        self.assertNotIn('RACE_PREF_HUMAN)', runtime[runtime.index('function config takes'):])

    def test_selected_undead_and_night_elf_start_with_owned_mines_at_full_reserve(self):
        runtime = runtime_script('STARTING-MINE-TEST')
        init = function_body(runtime, 'KLS_Init')
        self.assertIn("KLS_BaseMine[i] = KLS_CreateUnit(Player(PLAYER_NEUTRAL_PASSIVE), 'ngol'", init)
        self.assertIn('SetResourceAmount(KLS_BaseMine[i], 1000000)', init)
        self.assertIn('function KLS_ConfigureStartingMine takes', runtime)
        configure = function_body(runtime, 'KLS_ConfigureStartingMine')
        self.assertIn("set mineType = 'egol'", configure)
        self.assertIn("set mineType = 'ugol'", configure)
        self.assertIn('GetResourceAmount(KLS_BaseMine[p])', configure)
        self.assertIn('KLS_CreateUnitChecked(Player(p),mineType', configure)
        self.assertIn('SetResourceAmount(ownedMine,amount)', configure)
        self.assertIn('RemoveUnit(KLS_BaseMine[p])', configure)
        self.assertIn('KLS_ConfigureStartingMine(p,raceId)', function_body(runtime, 'KLS_ReplaceStartingFaction'))

    def test_tier_two_town_hall_upgrades_accept_the_selected_races_custom_altar(self):
        records = decode(units())
        expected = {
            'hcas': ('hbar', 'hbla', 'h000'),
            'ostr': ('obar', 'ofor', 'kA01'),
            'etoa': ('eaow', 'eaoe', 'kA02'),
            'unp1': ('usep', 'uslh', 'kA03'),
        }
        installed_units = slk('UnitData.slk')
        for hall, requirements in expected.items():
            with self.subTest(town_hall_upgrade=hall):
                self.assertIn(hall, installed_units)
                self.assertIn(hall, records)
                actual = records[hall][1][('ureq', 0)][0].split(',')
                self.assertEqual(actual, list(requirements))

    def test_diagnostics_report_expected_and_actual_starting_mine_state(self):
        runtime = runtime_script('STARTING-MINE-DIAGNOSTIC-TEST')
        expected = function_body(runtime, 'KLS_ExpectedStartingMine')
        diagnostics = function_body(runtime, 'KLS_ShowDiagnostics')
        self.assertIn('return "Entangled Gold Mine (egol)"', expected)
        self.assertIn('return "Haunted Gold Mine (ugol)"', expected)
        self.assertIn('return "Gold Mine (ngol)"', expected)
        self.assertIn('if mine != null then', diagnostics)
        self.assertIn('actual=MISSING', diagnostics)
        for observed_state in ('expected=', 'actual=', 'owner=', 'gold=', 'at='):
            self.assertIn(observed_state, diagnostics)
        self.assertIn('GetUnitTypeId(mine)', diagnostics)
        self.assertIn('GetOwningPlayer(mine)', diagnostics)
        self.assertIn('GetResourceAmount(mine)', diagnostics)
        self.assertIn('GetUnitX(mine)', diagnostics)
        self.assertIn('GetUnitY(mine)', diagnostics)

    def test_racial_mine_spawn_failure_has_specific_required_spawn_context(self):
        runtime = runtime_script('STARTING-MINE-SPAWN-DIAGNOSTIC-TEST')
        configure = function_body(runtime, 'KLS_ConfigureStartingMine')
        self.assertIn('KLS_CreateUnitChecked(Player(p),mineType,x,y,facing,true,"starting racial gold mine")', configure)

    def test_acolyte_haunt_handler_accepts_the_native_haunting_order(self):
        runtime = runtime_script('NATIVE-HAUNT-ORDER-TEST')
        mining = runtime[runtime.index('function KLS_HauntGoldMine takes'):runtime.index('function KLS_MiningInit takes')]
        self.assertIn('OrderId("hauntgoldmine")', mining)

    def test_night_elf_tree_entangle_reaches_the_starting_mine(self):
        _, fields = decode(abilities(), extended=True)['Aent']
        self.assertGreaterEqual(fields[('aran', 1)][0], 1400)
        self.assertEqual(FACTIONS[2]['town_hall'], 'etol')

    def test_all_racial_company_units_remain_connected_to_their_runtime_roles(self):
        runtime = runtime_script('BUILDING-ROLES-TEST')
        for fragment in ('EVENT_PLAYER_UNIT_CONSTRUCT_FINISH', 'KLS_IsFactionHall',
                         'KLS_IsFactionFoundry', 'KLS_IsFactionSiegeYard',
                         'AddUnitToStock(barracks,KLS_CompanyUnitId[KLS_HeroChoice[p]],99,99)',
                         'AddUnitToStock(building,KLS_CompanySupportId[KLS_HeroChoice[p]],99,99)',
                         'KLS_CompanyApplyFoundry'):
            self.assertIn(fragment, runtime)

    def test_each_hero_has_three_native_plus_button_stat_skills_and_no_stat_dialog(self):
        unit_records = decode(units())
        custom_heroes = {entry['unit_id'] for entry in NEW_HEROES} | {'H000'}
        for hero_id, _skills in HERO_ABILITIES.items():
            if hero_id in custom_heroes:
                fields = unit_records[hero_id][1]
            else:
                fields = unit_records[hero_id][1]
            choices = fields[('uhab', 0)][0].split(',')
            self.assertTrue(set(STAT_ABILITY_IDS) <= set(choices), hero_id)
        ability_records = decode(abilities(), extended=True)
        for code in STAT_ABILITY_IDS:
            base, fields = ability_records[code]
            self.assertEqual(base, 'Aamk')
            self.assertEqual(fields[('alev', 0)][0], 50)
        runtime = runtime_script('SKILL-TEST')
        self.assertNotIn('KLS_StatPending', runtime)
        self.assertNotIn('DialogAddButton(KLS_ProgressionDialog[p],"+3 Strength"', runtime)


if __name__ == '__main__':
    unittest.main()
