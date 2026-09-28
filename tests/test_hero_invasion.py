"""Installed-data and allocation checks for the invasion and signature additions."""
import unittest
from test_equipment import slk,decode,ROOT
from equipment_catalog import abilities
from signature_spells import SIGNATURES,spell_id
from wave_rosters import wave_rosters

class HeroAndInvasionData(unittest.TestCase):
    def test_signature_spells_are_visible_point_casts_and_summons_exist(self):
        records=decode(abilities(),True)
        installed=slk('UnitData.slk')
        self.assertEqual(len(SIGNATURES),25)
        self.assertEqual(len({e[0] for e in SIGNATURES}),25)
        for index,entry in enumerate(SIGNATURES):
            base,fields=records[spell_id(index)]
            self.assertEqual(base,'ANcl')
            self.assertEqual(fields[('Ncl2',1)][0],2) # Ground target, not tree/unit target.
            self.assertEqual(fields[('Ncl3',1)][0]&1,1) # Visible command card button.
            self.assertEqual(fields[('aher',0)][0],0) # Bonus ability needs no skill point.
            self.assertEqual(fields[('amcs',1)][0],70)
            icon=fields[('aart',0)][0]
            self.assertTrue(icon.startswith('ReplaceableTextures\\CommandButtons\\BTN'),entry[0])
            self.assertTrue(icon.endswith('.dds'),entry[0])
            installed_icons={line.strip().lower() for line in (ROOT/'tools/reference/installed/commandbuttons.txt').read_text().splitlines()}
            self.assertIn(icon.lower(),installed_icons,entry[0])
            if entry[5]:self.assertIn(entry[5],installed,entry[0])
        keeper=SIGNATURES[9]
        self.assertEqual((keeper[5],keeper[6]),('efon',3))

    def test_all_waves_resolve_to_installed_units_and_retain_living_targets(self):
        installed=slk('UnitData.slk')
        rosters=wave_rosters()
        self.assertEqual(len(rosters),40)
        for wave,roster in enumerate(rosters,1):
            self.assertLessEqual(len(roster),20)
            self.assertLess(wave*20+len(roster)-1,820)
            self.assertIn('hfoo',roster)
            self.assertLessEqual(roster.count('hfoo')/len(roster),0.125)
            self.assertIn('nfel',roster)
            self.assertIn('ugho',roster)
            for kind in roster:self.assertIn(kind,installed)
        self.assertNotIn('ninf',rosters[0])
        self.assertIn('ninf',rosters[30])
        self.assertIn('umtw',rosters[20])
