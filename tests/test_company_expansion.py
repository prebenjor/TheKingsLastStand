"""Contract tests for hero-specific companies and the new kingdom structures."""
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'tools'))
sys.path.insert(0, str(ROOT / 'tests'))

from company_catalog import COMPANY_BUILDINGS, HERO_COMPANIES
from equipment_catalog import abilities
from faction_catalog import FACTIONS
from hero_progression import HERO_ABILITIES
from objects import units
from pipeline import runtime_script
from test_equipment import decode, slk


class HeroCompanyExpansion(unittest.TestCase):
    def test_every_selectable_hero_has_personal_company_and_support_stock(self):
        self.assertEqual(len(HERO_COMPANIES), 25)
        self.assertEqual([entry['hero_type'] for entry in HERO_COMPANIES], list(HERO_ABILITIES))

        unit_ids = []
        for entry in HERO_COMPANIES:
            self.assertTrue(entry['company_name'])
            self.assertTrue(entry['support_name'])
            self.assertGreater(entry['company_gold'], 0)
            self.assertGreater(entry['support_gold'], 0)
            self.assertGreater(entry['company_hp'], 0)
            self.assertGreater(entry['support_hp'], 0)
            unit_ids.extend((entry['company_id'], entry['support_id']))
        self.assertEqual(len(set(unit_ids)), 50)

        installed_units = slk('UnitData.slk')
        self.assertTrue(set(unit_ids).isdisjoint(installed_units))
        building_ids = [entry['rawcode'] for entry in COMPANY_BUILDINGS.values()]
        self.assertEqual(len(set(unit_ids + building_ids)), 53)
        self.assertTrue(set(building_ids).isdisjoint(installed_units))
        installed_abilities = slk('AbilityData.slk')
        for ability_id in {entry['banner_ability'] for entry in HERO_COMPANIES}:
            self.assertIn(ability_id, installed_abilities)

    def test_three_custom_buildings_are_buildable_and_use_native_models(self):
        unit_objects = decode(units())
        worker = unit_objects['hpea'][1][('ubui', 0)][0].split(',')
        self.assertLessEqual(len(worker), 12)
        self.assertEqual(set(COMPANY_BUILDINGS), {'hall', 'foundry', 'siege_yard'})
        expected_parents = {'hall': 'hgra', 'foundry': 'hbla', 'siege_yard': 'harm'}
        for role, entry in COMPANY_BUILDINGS.items():
            with self.subTest(building=role):
                self.assertIn(entry['rawcode'], worker)
                base, fields = unit_objects[entry['rawcode']]
                self.assertEqual(base, expected_parents[role])
                self.assertEqual(fields[('unam', 0)][0], entry['name'])
                self.assertGreater(fields[('ugol', 0)][0], 0)
                self.assertGreater(fields[('ulum', 0)][0], 0)
                self.assertIn('hbar', fields[('ureq', 0)][0])

    def test_racial_halls_have_distinct_models_and_foundries_sell_their_legendary_pattern(self):
        records = decode(units())
        expected_halls = ('hgra', 'obea', 'edob', 'utom')
        expected_patterns = ('RCP4', 'RCP5', 'RCP6', 'RCP7')
        runtime = runtime_script('FOUNDRY-TEST')
        installed_units = slk('UnitData.slk')
        installed_abilities = slk('AbilityData.slk')

        for index, faction in enumerate(FACTIONS):
            hall = faction['company_buildings']['hall']
            foundry = faction['company_buildings']['foundry']
            with self.subTest(race=faction['race']):
                self.assertEqual(hall['parent'], expected_halls[index])
                self.assertIn(expected_halls[index], installed_units)
                self.assertEqual(records[hall['rawcode']][0], expected_halls[index])
                hall_fields = records[hall['rawcode']][1]
                self.assertEqual(hall_fields[('uabi', 0)][0], '')
                self.assertEqual(hall_fields[('utra', 0)][0], '')
                self.assertEqual(hall_fields[('uupt', 0)][0], '')
                foundry_fields = records[foundry['rawcode']][1]
                for ability in ('Aneu', 'Apit', 'Asid', 'Asud'):
                    self.assertIn(ability, foundry_fields[('uabi', 0)][0])
                    self.assertIn(ability, installed_abilities)
                self.assertIn(
                    f"KLS_FactionFoundryRecipeId[{index}] = '{expected_patterns[index]}'",
                    runtime,
                )

        self.assertIn("call AddItemToStock(building,KLS_FactionFoundryRecipeId[KLS_PlayerRace[p]],1,1)", runtime)
        self.assertIn("KLS_IsFactionFoundry(GetUnitTypeId(shop))", runtime)

    def test_company_units_are_serialized_and_recruited_only_after_matching_doctrine(self):
        unit_objects = decode(units())
        for entry in HERO_COMPANIES:
            for rawcode, name, hp, damage in (
                (entry['company_id'], entry['company_name'], entry['company_hp'], entry['company_damage']),
                (entry['support_id'], entry['support_name'], entry['support_hp'], entry['support_damage']),
            ):
                with self.subTest(unit=rawcode):
                    base, fields = unit_objects[rawcode]
                    self.assertIn(base, slk('UnitData.slk'))
                    self.assertEqual(fields[('unam', 0)][0], name)
                    self.assertEqual(fields[('uhpm', 0)][0], hp)
                    self.assertEqual(fields[('ua1b', 0)][0], damage)

        runtime = runtime_script('COMPANY-TEST')
        self.assertIn("KLS_CompanyUnitId[15] = 'kC15'", runtime)
        self.assertIn("KLS_CompanySupportId[24] = 'kS24'", runtime)
        self.assertIn('integer array KLS_HeroChoice', runtime)
        self.assertIn('KLS_HeroChoice[p] = n', runtime)
        self.assertIn('KLS_CompanyHall[p]', runtime)
        self.assertIn('AddUnitToStock(barracks,KLS_CompanyUnitId[KLS_HeroChoice[p]],99,99)', runtime)
        self.assertIn('AddUnitToStock(building,KLS_CompanySupportId[KLS_HeroChoice[p]],99,99)', runtime)
        self.assertIn('EVENT_PLAYER_UNIT_SELL', runtime)
        self.assertNotIn('EVENT_PLAYER_UNIT_SELL_UNIT', runtime)
        self.assertIn('KLS_CompanyApplyFoundry', runtime)
        self.assertIn('EVENT_PLAYER_UNIT_CONSTRUCT_FINISH', runtime)
        self.assertIn('UnitAddAbility(building,doctrine)', runtime)

    def test_banner_doctrines_use_installed_auras_and_foundry_bonus_is_persistent(self):
        ids = {entry['banner_ability'] for entry in HERO_COMPANIES}
        self.assertTrue(ids <= {'AHad', 'AOae', 'AEar', 'AHab', 'AUau'})
        runtime = runtime_script('COMPANY-TEST')
        self.assertIn('KLS_CompanyFoundry[p] = true', runtime)
        self.assertIn('KLS_CompanyApplyFoundry', runtime)
        self.assertNotIn('KLS_Enemies, sold', runtime)
        self.assertNotIn('GroupAddUnit(KLS_Enemies, sold)', runtime)

if __name__ == '__main__':
    unittest.main()
