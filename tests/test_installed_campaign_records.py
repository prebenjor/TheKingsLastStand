"""Pin supported-edition Forsaken campaign and worker records used by the design."""
import unittest
from test_equipment import slk


class InstalledCampaignRecords(unittest.TestCase):
    def test_worker_and_campaign_hero_identity_and_ability_lists(self):
        ui = slk('UnitUI.slk')
        abilities = slk('UnitAbilities.slk')
        self.assertEqual(ui['hpea'][5], 'peasant')
        self.assertEqual(ui['uaco'][5], 'acolyte')
        self.assertEqual(abilities['hpea'][5], 'Ahar,Amil,Ahrp,Ahlh')
        self.assertEqual(abilities['uaco'][5], 'Aaha,Arst,Alam,Auns')
        self.assertEqual(ui['Hjsm'][5], 'Ilastar')
        self.assertEqual(abilities['Hjsm'][6], 'AHas,AHsf,AHmc,AHsl')
        self.assertEqual(ui['Ujsm'][5], 'Ilastar Undead')
        self.assertNotIn(6, abilities['Ujsm'])
        self.assertEqual(ui['Npal'][5], 'Forsaken Paladin')
        self.assertEqual(abilities['Npal'][6], 'AHcr,ANcp,AHpa,AHcl')


if __name__ == '__main__':
    unittest.main()
