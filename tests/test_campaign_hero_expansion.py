"""Regressions for the two installed-data-verified Forsaken campaign heroes."""
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'tools'))
sys.path.insert(0, str(ROOT / 'tests'))

from equipment_catalog import abilities
from hero_progression import HERO_ABILITIES
from pipeline import runtime_script
from signature_spells import SIGNATURES, spell_id
from test_equipment import decode, slk


class CampaignHeroExpansion(unittest.TestCase):
    def test_verified_campaign_heroes_have_native_skills_ranks_and_signatures(self):
        self.assertEqual(len(HERO_ABILITIES), 25)
        self.assertEqual(HERO_ABILITIES['Hjsm'], ('AHas', 'AHsf', 'AHmc', 'AHsl'))
        self.assertEqual(HERO_ABILITIES['Npal'], ('AHcr', 'ANcp', 'AHpa', 'AHcl'))

        unit_names = slk('UnitUI.slk')
        unit_abilities = slk('UnitAbilities.slk')
        ability_data = slk('AbilityData.slk')
        self.assertEqual(unit_names['Hjsm'][5], 'Ilastar')
        self.assertEqual(unit_names['Npal'][5], 'Forsaken Paladin')
        for hero, spells in (('Hjsm', HERO_ABILITIES['Hjsm']),
                             ('Npal', HERO_ABILITIES['Npal'])):
            self.assertEqual(tuple(unit_abilities[hero][6].split(',')), spells)
            for spell in spells:
                self.assertIn(spell, ability_data)
        self.assertIn('Sacred Aura', ability_data['AHas'][3])
        self.assertIn('Sacred Flame', ability_data['AHsf'][3])
        self.assertIn('Mind Control', ability_data['AHmc'][3])
        self.assertIn('Surge of Light', ability_data['AHsl'][3])
        self.assertEqual(ability_data['AHcr'][3], 'Consecration')
        self.assertEqual(ability_data['ANcp'][3], 'Righteous Fury')
        self.assertIn('Sacred Aura', ability_data['AHpa'][3])
        self.assertEqual(ability_data['AHcl'][3], 'Cleansing Fire')

        command_buttons = (ROOT / 'tools/reference/installed/commandbuttons.txt').read_text().lower()
        self.assertIn('replaceabletextures\\commandbuttons\\btnholybolt.dds', command_buttons)
        self.assertIn('replaceabletextures\\commandbuttons\\btndispelmagic.dds', command_buttons)

        self.assertEqual(len(SIGNATURES), 25)
        self.assertEqual(SIGNATURES[15][0], "Ilastar's Last Light")
        self.assertEqual(SIGNATURES[16][0], 'Cleansing Pyre')
        object_records = decode(abilities(), extended=True)
        self.assertIn(spell_id(15), object_records)
        self.assertIn(spell_id(16), object_records)

        runtime = runtime_script('KLS-HERO17-TEST')
        from objects import units
        heroes = decode(units())
        for hero in ('Hjsm','Npal'):
            self.assertEqual(heroes[hero][1][('uhab',0)][0], ','.join(HERO_ABILITIES[hero]))
        self.assertNotIn('KLS_ApplySpellRanks',runtime)
        self.assertIn("KLS_HeroType[15] = 'Hjsm'", runtime)
        self.assertIn("KLS_HeroType[16] = 'Npal'", runtime)
        self.assertIn('exitwhen n == KLS_HeroCount', runtime)
        self.assertIn('n >= KLS_HeroCount', runtime)
        self.assertIn('25 hero previews', runtime)


if __name__ == '__main__':
    unittest.main()
