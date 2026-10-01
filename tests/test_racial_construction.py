import sys
import unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'tools'))
from faction_catalog import FACTIONS
from editor_workshop import decode_objects
from objects import units

class RacialConstruction(unittest.TestCase):
    def test_complete_standard_menu_and_native_limit(self):
        expected=( {'htow','hhou','hbar','h000','hlum','hbla','harm','hars','hgra','hwtw','hvlt'},
                   {'ogre','otrb','obar','kA01','ofor','owtw','obea','osld','otto','ovln'},
                   {'etol','emow','eaom','kA02','edob','etrp','eaoe','eaow','edos','eden'},
                   {'unpl','uzig','usep','kA03','ugrv','uslh','utod','usap','ubon','utom','ugol'} )
        for faction,wanted in zip(FACTIONS,expected):
            self.assertEqual(set(faction['standard_menu']),wanted)
            self.assertLessEqual(len(faction['standard_menu']),11)
            self.assertEqual(len(set(faction['expansion_menu'])),6)
            self.assertEqual(faction['build_menu'],faction['standard_menu'])

    def test_specialists_have_training_and_food_and_collision_free_ids(self):
        from racial_catalog import SPECIALISTS
        data=decode_objects(units())
        ids=[key.rsplit('/',1)[0] for key in data if key.endswith('/base')]
        self.assertEqual(len(SPECIALISTS),8)
        self.assertEqual(SPECIALISTS[6]['parent'],'uske')
        self.assertEqual(len({s['id'] for s in SPECIALISTS}),8)
        for s in SPECIALISTS:
            self.assertEqual(s['food'],3)
            self.assertEqual(s['train_time'],25 if s['role']=='hall' else 30)
        self.assertEqual(len(ids),len(set(ids)))

    def test_runtime_reconciles_stock_and_trained_units(self):
        source=(Path(__file__).resolve().parents[1]/'source/companies.j').read_text()
        self.assertIn('EVENT_PLAYER_UNIT_TRAIN_FINISH',source)
        self.assertIn('function KLS_CompanyReconcile',source)
        self.assertIn("call UnitAddAbility(barracks,'Asud')",source)
        self.assertIn('KLS_SpecialistIndex',source)

if __name__=='__main__':unittest.main()
