"""Acceptance contracts for the Crownlands expansion content catalogs."""
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'tools'))
sys.path.insert(0, str(ROOT / 'tests'))

from equipment_catalog import CUSTOM_RACE_ITEMS, item_catalog
from hero_catalog import HERO_COUNT, HERO_RACES, NEW_HEROES
from faction_catalog import FACTIONS
from hero_progression import HERO_ABILITIES
from recipes import recipe_catalog
from signature_spells import SIGNATURES
from pipeline import runtime_script
from test_equipment import decode, slk
from objects import units, items


class CrownlandsExpansion(unittest.TestCase):
    def test_eight_new_heroes_have_racial_identity_skills_models_and_signatures(self):
        self.assertEqual(HERO_COUNT, 25)
        self.assertEqual(len(HERO_RACES), HERO_COUNT)
        self.assertEqual(len(NEW_HEROES), 8)
        self.assertEqual({entry['race'] for entry in NEW_HEROES},
                         {'Human', 'Orc', 'Night Elf', 'Undead'})
        self.assertEqual(len(HERO_ABILITIES), HERO_COUNT)
        self.assertEqual(len(SIGNATURES), HERO_COUNT)
        unit_data = slk('UnitData.slk')
        records = decode(units())
        for entry in NEW_HEROES:
            with self.subTest(hero=entry['name']):
                self.assertIn(entry['unit_id'], records)
                self.assertIn(entry['base'], unit_data)
                self.assertEqual(records[entry['unit_id']][0], entry['base'])
                self.assertEqual(entry['signature_index'], HERO_COUNT - 8 + NEW_HEROES.index(entry))

    def test_twenty_race_items_have_exact_names_rarities_stats_and_equipment_data(self):
        self.assertEqual(len(CUSTOM_RACE_ITEMS), 20)
        self.assertEqual(len({entry['name'] for entry in CUSTOM_RACE_ITEMS}), 20)
        self.assertEqual({entry['quality'] for entry in CUSTOM_RACE_ITEMS},
                         {'Common', 'Uncommon', 'Rare', 'Epic', 'Legendary'})
        catalog = item_catalog()
        by_name = {entry['name']: entry for entry in catalog}
        expected = {
            'Human': ('Watchman’s Token', 'Lionroad Mantle', 'Aldric’s Aegis', 'Crownward Pennant', 'Last King’s Oath'),
            'Orc': ('Redtusk Fetish', 'Ashen War Drum', 'Stormscar Bracers', 'Grudgebreaker', 'Worldrend Standard'),
            'Night Elf': ('Moonbark Charm', 'Starleaf Quiver', 'Duskwatch Longbow', 'Briarheart Mantle', 'Silvermoon Vigil'),
            'Undead': ('Crypt-Iron Band', 'Wraithsilk Cape', 'Soulreaper’s Fang', 'Mourning Reliquary', 'Night’s Covenant'),
        }
        for race, names in expected.items():
            self.assertEqual(tuple(entry['name'] for entry in CUSTOM_RACE_ITEMS if entry['race'] == race), names)
            self.assertEqual([by_name[name]['quality'] for name in names],
                             ['Common', 'Uncommon', 'Rare', 'Epic', 'Legendary'])
            for name in names:
                self.assertTrue(by_name[name]['stats'])
                self.assertTrue(by_name[name]['abilities'])
                self.assertIn('|c', by_name[name]['colored_name'])
        objects = decode(items())
        for item in CUSTOM_RACE_ITEMS:
            self.assertIn(item['rawcode'], objects)

    def test_four_faction_recipes_resolve_to_their_legendary_catalog_items(self):
        recipes = recipe_catalog(item_catalog())
        faction = [recipe for recipe in recipes if recipe['rawcode'] in {'RCP4', 'RCP5', 'RCP6', 'RCP7'}]
        self.assertEqual(len(faction), 4)
        self.assertEqual({recipe['output'] for recipe in faction},
                         {item['rawcode'] for item in CUSTOM_RACE_ITEMS if item['quality'] == 'Legendary'})
        self.assertTrue(all(len(recipe['components']) == 2 and recipe['price'] > 0 for recipe in faction))

    def test_selected_hero_race_drives_workers_and_working_build_menus(self):
        self.assertEqual([faction['race'] for faction in FACTIONS],
                         ['Human', 'Orc', 'Night Elf', 'Undead'])
        self.assertEqual([faction['worker'] for faction in FACTIONS],
                         ['hpea', 'opeo', 'ewsp', 'uaco'])
        self.assertTrue(all(len(faction['build_menu']) <= 12 for faction in FACTIONS))
        for faction in FACTIONS:
            self.assertEqual(set(('hall','foundry','siege_yard')),
                             set(faction['company_buildings']))
            self.assertEqual(len(set(faction['build_menu'])), len(faction['build_menu']))
        runtime = runtime_script('FACTION-TEST')
        self.assertIn('KLS_ReplaceStartingFaction(p,n)', runtime)
        self.assertIn('local integer raceId = KLS_HeroRace[heroIndex]', runtime)
        self.assertIn('KLS_FactionWorkerId[2] = \'ewsp\'', runtime)


    def test_towns_and_story_are_in_runtime_without_affecting_wave_counts(self):
        from town_catalog import TOWNS, QUEST_RAWCODES, town_placements
        self.assertEqual(len(TOWNS), 4)
        self.assertEqual([town['race'] for town in TOWNS], ['Human', 'Orc', 'Night Elf', 'Undead'])
        self.assertEqual(len(QUEST_RAWCODES), 4)
        towns = decode(units())
        self.assertTrue(set(QUEST_RAWCODES).issubset(towns))
        self.assertTrue(all(abs(position) <= 11520 for _, _, x, y in town_placements() for position in (x,y)))
        runtime = runtime_script('TOWN-TEST')
        for function in ('KLS_CrownlandsInit', 'KLS_StoryBegin', 'KLS_StoryComplete', 'KLS_StoryCartTick'):
            self.assertIn('function '+function+' takes', runtime)
        death = runtime[runtime.index('function KLS_Death takes'):runtime.index('function KLS_Spawn takes')]
        self.assertIn('IsUnitInGroup(dead,KLS_StoryEnemies)', death)
        self.assertNotIn('set KLS_Alive = KLS_Alive - 1', death[:death.index('elseif IsUnitInGroup(dead, KLS_Enemies)')])
        self.assertIn('KLS_TownShop[', runtime)
        story_begin = runtime[runtime.index('function KLS_StoryBegin takes'):runtime.index('function KLS_StoryStartSync takes')]
        self.assertNotIn('KLS_Alive', story_begin)
        self.assertNotIn('KLS_Prep', story_begin)
        self.assertNotIn('PauseTimer', story_begin)

    def test_second_defender_can_join_an_active_supply_escort(self):
        runtime = runtime_script('ESCORT-TEST')
        story_begin = runtime[runtime.index('function KLS_StoryBegin takes'):runtime.index('function KLS_StoryStartSync takes')]
        active_caravan = story_begin[story_begin.index('if KLS_StoryStage == 1 then'):story_begin.index('elseif KLS_StoryStage == 2 then')]
        self.assertIn('if KLS_StoryCart != null then', active_caravan)
        self.assertIn('set KLS_StoryContributor[KLS_StoryStage*4+p] = true', active_caravan)
        self.assertIn('You joined the Northwatch supply escort.', active_caravan)

    def test_each_hero_level_offers_three_attribute_points_and_fifth_levels_offer_talents(self):
        runtime = runtime_script('LEVEL-TEST')
        hero_records = decode(units())
        for hero_id in HERO_ABILITIES:
            learned_choices = hero_records[hero_id][1][('uhab', 0)][0].split(',')
            self.assertEqual(learned_choices, list(HERO_ABILITIES[hero_id]), hero_id)
        for choice in ('KLS_TalentStrengthButton','KLS_TalentAgilityButton',
                       'KLS_TalentIntelligenceButton'):
            self.assertIn(choice,runtime)
        self.assertNotIn('KLS_StatPending', runtime)
        self.assertNotIn('DialogAddButton(KLS_ProgressionDialog[p],"+3 Strength"', runtime)
        self.assertIn('set milestone = GetHeroLevel(u) / 5', runtime)
        self.assertIn('KLS_TalentApply(p,', runtime)
        self.assertIn('UNIT_RF_HIT_POINTS_REGENERATION_RATE,current+2.0', runtime)
        self.assertIn('UNIT_RF_MANA_REGENERATION,current+2.0', runtime)
        self.assertIn('KLS_TalentAgilityRank[p]*2', runtime)


if __name__ == '__main__':
    unittest.main()
