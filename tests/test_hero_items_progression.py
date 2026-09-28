"""Regressions for the approved high-level gear, crafting and recovery features."""
import re
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'tools'))
sys.path.insert(0, str(ROOT / 'tests'))

from equipment_catalog import abilities, attribute_books, catalog_script, item_catalog
from hero_progression import (
    HERO_ABILITIES, MAX_HERO_LEVEL, _ability_tables, _modification_fields,
    spell_script,
)
from objects import items, units
from pipeline import misc_data, runtime_script
from recipes import plan_recipe_craft, recipe_catalog, recipe_script
from test_equipment import decode, slk


class AttributeEquipment(unittest.TestCase):
    def test_tiered_attribute_gear_is_in_the_native_catalog(self):
        catalog = item_catalog()
        attributes = [e for e in catalog if e['family'] in {
            'Might Chestplate', 'Windrunner Boots', 'Arcanist Focus'}]
        self.assertEqual(len(attributes), 15)
        self.assertEqual({e['tier'] for e in attributes}, set(range(5)))
        self.assertEqual({e['family'] for e in attributes}, {
            'Might Chestplate', 'Windrunner Boots', 'Arcanist Focus'})
        for family, stat in (('Might Chestplate', 'strength'),
                             ('Windrunner Boots', 'agility'),
                             ('Arcanist Focus', 'intelligence')):
            rows = sorted((e for e in attributes if e['family'] == family), key=lambda e:e['tier'])
            self.assertEqual([e['stats'][stat] for e in rows], [2, 4, 8, 14, 22])
            self.assertTrue(all(stat in e['stats'] for e in rows))
        object_data = decode(items())
        ability_data = decode(abilities(), extended=True)
        expected_field = {'strength':'Istr', 'agility':'Iagi', 'intelligence':'Iint'}
        for entry in attributes:
            item_fields = object_data[entry['rawcode']][1]
            self.assertIn('All heroes', item_fields[('utub', 0)][0])
            for ability_id in item_fields[('iabi', 0)][0].split(','):
                fields = ability_data[ability_id][1]
                stat = next(stat for stat in expected_field
                            if any(field == expected_field[stat] for field, level in fields))
                self.assertEqual(fields[(expected_field[stat], 1)][0], entry['stats'][stat])

    def test_sages_archive_sells_permanent_strength_agility_and_intellect_books(self):
        books = attribute_books()
        self.assertEqual(len(books), 9)
        self.assertEqual({b['stat'] for b in books}, {'strength','agility','intelligence'})
        self.assertEqual({b['amount'] for b in books}, {5,10,20})
        self.assertTrue(all(b['price'] > 0 for b in books))
        self.assertTrue(all(len(b['rawcode']) == 4 for b in books))
        installed_items = {row[1] for row in slk('ItemData.slk').values() if 1 in row}
        self.assertTrue({b['rawcode'] for b in books}.isdisjoint(installed_items))
        self.assertIn('KLS_Shops[11]', catalog_script())
        item_data = decode(items())
        for book in books:
            fields = item_data[book['rawcode']][1]
            self.assertIn('permanently', fields[('utub',0)][0].lower())
            self.assertEqual(fields[('igol',0)][0], book['price'])
        unit_data = decode(units())
        self.assertEqual(unit_data['hS02'][0], 'hars')
        self.assertIn('Aneu', unit_data['hS02'][1][('uabi',0)][0])
        runtime = runtime_script('BOOKSHOP')
        self.assertIn("KLS_CreateUnit(Player(PLAYER_NEUTRAL_PASSIVE),'hS02'", runtime)
        apothecary = re.search(r"set KLS_Shops\[10\] = .*?,(-?\d+),(-?\d+),270", runtime)
        archive = re.search(r"set KLS_Shops\[11\] = .*?,(-?\d+),(-?\d+),270", runtime)
        self.assertIsNotNone(apothecary)
        self.assertIsNotNone(archive)
        self.assertLessEqual(abs(int(apothecary[1]) - int(archive[1])), 750)
        self.assertLessEqual(abs(int(apothecary[2]) - int(archive[2])), 200)


class RecipeTransactions(unittest.TestCase):
    def test_master_forge_has_three_named_combinations_using_existing_gear(self):
        recipes = recipe_catalog(item_catalog())
        self.assertEqual(len(recipes), 3)
        names = {r['name'] for r in recipes}
        self.assertEqual(names, {'Oathforged Kingswrath','Stormheart Prism','Sovereign’s Mantle'})
        catalog_ids = {entry['rawcode'] for entry in item_catalog()}
        for recipe in recipes:
            self.assertEqual(len(recipe['components']), 2)
            self.assertTrue(set(recipe['components']) <= catalog_ids)
            self.assertIn(recipe['output'], catalog_ids)
            self.assertGreater(recipe['price'], 0)
        generated = recipe_script()
        for recipe in recipes:
            self.assertIn(f"'{recipe['rawcode']}'", generated)
            self.assertIn(f"'{recipe['output']}'", generated)
        self.assertIn('UnitItemInEquipmentSlot', generated)
        self.assertIn('UnitItemInBagSlot', generated)

    def test_failed_recipe_keeps_components_and_refunds_the_entire_fee(self):
        recipe = recipe_catalog(item_catalog())[0]
        hero_items = [{'id':recipe['components'][0], 'owner':1}]
        result = plan_recipe_craft(recipe, hero_items, owner=1,
                                   gold=recipe['price'], output_slot_available=True)
        self.assertFalse(result['success'])
        self.assertEqual(result['gold'], recipe['price'])
        self.assertEqual(result['remaining_items'], hero_items)
        self.assertIsNone(result['output'])

    def test_successful_recipe_consumes_owned_components_and_charges_once(self):
        recipe = recipe_catalog(item_catalog())[0]
        hero_items = [{'id':recipe['components'][0], 'owner':1, 'slot':'bag'},
                      {'id':recipe['components'][1], 'owner':1, 'slot':'equipment'}]
        result = plan_recipe_craft(recipe, hero_items, owner=1,
                                   gold=recipe['price']+50, output_slot_available=True)
        self.assertTrue(result['success'])
        self.assertEqual(result['gold'], 50)
        self.assertEqual(result['remaining_items'], [])
        self.assertEqual(result['output'], recipe['output'])

    def test_wrong_owner_insufficient_gold_or_full_output_space_never_consumes_items(self):
        recipe = recipe_catalog(item_catalog())[0]
        hero_items = [{'id':recipe['components'][0], 'owner':1},
                      {'id':recipe['components'][1], 'owner':2}]
        for owner, gold, output_space in ((1, recipe['price'], True),
                                           (1, recipe['price']-1, True),
                                           (1, recipe['price'], False)):
            result = plan_recipe_craft(recipe, hero_items, owner=owner,
                                       gold=gold, output_slot_available=output_space)
            self.assertFalse(result['success'])
            self.assertEqual(result['remaining_items'], hero_items)
        script = runtime_script('RECIPE-TRANSACTION')
        self.assertIn('KLS_RecipeComplete', script)
        self.assertIn('No components consumed', script)

    def test_failed_native_output_creation_restores_components_and_refunds_recipe(self):
        script = recipe_script()
        self.assertRegex(script, r'function KLS_RecipeRestoreIngredients[\s\S]*?UnitAddItem\(buyer, first\)[\s\S]*?UnitAddItem\(buyer, second\)[\s\S]*?UnitEquipItem\(buyer, first\)[\s\S]*?UnitEquipItem\(buyer, second\)')
        self.assertRegex(script, r'set output = CreateItem\([\s\S]*?if output == null then[\s\S]*?KLS_RecipeRestoreIngredients\(buyer, first, second\)[\s\S]*?KLS_RecipeRefund\(buyer, scroll\)[\s\S]*?else[\s\S]*?SetItemPlayer\(output')


class HeroProgressionAndRecovery(unittest.TestCase):
    def test_installed_spell_rank_values_are_preserved_before_continuation(self):
        records = decode(abilities(), extended=True)
        devotion_aura = records['AHad'][1]
        self.assertEqual(devotion_aura[('Had1', 4)][0], 4.5)
        self.assertGreater(devotion_aura[('Had1', 5)][0], devotion_aura[('Had1', 4)][0])

    def test_space_padded_missing_native_ranks_do_not_become_numeric_values(self):
        headers, data, metadata = _ability_tables()
        fields = _modification_fields('AEar', data['AEar'], headers, metadata)
        cast_ranks = {(rank, pointer): value for field, _, rank, pointer, value in fields
                      if field == 'acas'}
        self.assertEqual(cast_ranks[(1, 0)], 0.0)
        self.assertEqual(cast_ranks[(2, 0)], 0.0)

    def test_every_selectable_hero_spell_is_extended_to_ten_native_ranks(self):
        self.assertEqual(MAX_HERO_LEVEL, 100)
        self.assertEqual(len(HERO_ABILITIES), 17)
        installed = slk('AbilityData.slk')
        installed_ids = {row[1] for row in installed.values() if 1 in row}
        self.assertTrue(all(len(spells) == 4 for spells in HERO_ABILITIES.values()))
        self.assertTrue({spell for spells in HERO_ABILITIES.values() for spell in spells} <= installed_ids)
        records = decode(abilities(), extended=True)
        for spell in {spell for spells in HERO_ABILITIES.values() for spell in spells}:
            fields = records[spell][1]
            self.assertEqual(fields[('alev',0)][0], 10, spell)
            levels = {level for field, level in fields if level > 0}
            self.assertGreaterEqual(max(levels), 10, spell)
        holy_light = records['AHhb'][1]
        self.assertGreater(holy_light[('Hhb1',5)][0], holy_light[('Hhb1',4)][0])
        self.assertGreater(holy_light[('Hhb1',10)][0], holy_light[('Hhb1',9)][0])
        runtime = runtime_script('SPELL-RANKS')
        self.assertIn('KLS_ApplySpellRanks', runtime)
        self.assertGreaterEqual(runtime.count('call KLS_ApplySpellRanks('), 2)
        generated = spell_script()
        self.assertIn("if heroType == 'Hpal' then", generated)
        self.assertNotIn('if false then', generated)
        self.assertIn('GetHeroLevel(hero)', generated)
        self.assertIn('set rank = IMinBJ(10, 1 + (heroLevel - unlockLevel) / 10)', generated)
        self.assertEqual(min(10, 1 + (50 - 1) // 10), 5)
        self.assertEqual(min(10, 1 + (51 - 1) // 10), 6)
        self.assertEqual(min(10, 1 + (100 - 1) // 10), 10)
        self.assertIn(b'MaxHeroLevel=100', misc_data())

    def test_wave_breaks_are_longer_with_double_time_before_each_boss(self):
        runtime = runtime_script('LONGER-BREAKS')
        self.assertIn('set KLS_NormalPrep = 90', runtime)
        self.assertIn('set KLS_BossPrep = 180', runtime)
        self.assertRegex(runtime, r'if ModuloInteger\(KLS_Wave \+ 1, 10\) == 0 then\s+set KLS_Prep = KLS_BossPrep\s+else\s+set KLS_Prep = KLS_NormalPrep')

    def test_restore_pool_is_south_of_castle_and_off_the_central_route(self):
        runtime = runtime_script('RESTORE-POOL')
        self.assertIn("'nfoh'", runtime)
        self.assertIn('-900,-1600', runtime.replace(' ',''))
        self.assertIn('GetUnitState(hero,UNIT_STATE_MAX_MANA)', runtime)
        self.assertIn('SetWidgetLife(hero', runtime)
        self.assertIn('450.0', runtime)


if __name__ == '__main__':
    unittest.main()
