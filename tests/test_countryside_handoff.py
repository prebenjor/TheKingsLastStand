"""Regressions for targeted shop import and native editor grouping."""
import math
import struct
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'tools'))
import editor_layout
from editor_workshop import decode_units
from layout_catalog import market_placements


class CountrysideHandoff(unittest.TestCase):
    def test_new_market_facing_helper_precedes_shop_constructor(self):
        script=('function KLS_CreateShops takes nothing returns nothing\nendfunction\n'
                'function KLS_CrownlandsBuildTowns takes nothing returns nothing\nendfunction\n')
        helper='function KLS_MarketFacing takes integer index returns real\n return 90.0\nendfunction'
        changed=editor_layout.replace_runtime_functions(script,{'KLS_MarketFacing':helper})
        self.assertLess(changed.index('function KLS_MarketFacing'),changed.index('function KLS_CreateShops'))

    def test_group_repair_preserves_optional_native_payloads(self):
        record=editor_layout.unit_record('kInv',0,7680,0,11,146)
        record=(record[:63]+struct.pack('<2I',1,1)+b'phea'+struct.pack('<I',50)
                +record[67:91]+struct.pack('<2I',1,0)+b'pman'
                +struct.pack('<I',1)+b'AInv'+struct.pack('<2I',0,1)
                +record[99:127]+struct.pack('<I',1)+bytes(range(36)))
        grouped=bytearray(record)
        struct.pack_into('<i',grouped,40,0)
        data=b'W3do'+struct.pack('<3I',13,11,1)+bytes(grouped)
        repaired=editor_layout.ungroup_forest_units(data)
        self.assertEqual(repaired[:56],data[:56])
        expected=bytearray(data)
        struct.pack_into('<i',expected,56,-1)
        self.assertEqual(repaired,bytes(expected))

    def test_new_land_props_follow_final_terrain_and_partial_replay_is_refused(self):
        import forge_countryside
        self.assertTrue(hasattr(forge_countryside,'drape_land_props'), 'final-ground prop placement is missing')
        terrain=bytearray(69+193*193*8)
        struct.pack_into('<IIff',terrain,53,193,193,-12288,-12288)
        for i in range(193*193):
            struct.pack_into('<H',terrain,69+i*8,8192-400)
            terrain[69+i*8+7]=2
        plan={'props':[{'type_id':'LRrk','x':-6000,'y':-4000,'z':0},
                       {'type_id':'LPlp','x':-6000,'y':-4000,'z':-22}]}
        draped=forge_countryside.drape_land_props(plan,bytes(terrain))
        self.assertEqual(draped['props'][0]['z'],-100)
        self.assertEqual(draped['props'][1]['z'],-22)
        self.assertTrue(hasattr(forge_countryside,'validate_checkpoint'),'safe checkpoint validation is missing')
        with self.assertRaises(ValueError):
            forge_countryside.validate_checkpoint({'active':'props','next':4,'session_pid':1},1)

    def test_lookout_plateau_remains_walkable_away_from_cliff_edge(self):
        import inspect
        from countryside_catalog import countryside_pathing
        self.assertIn('terrain',inspect.signature(countryside_pathing).parameters,
                      'hill pathing must follow actual native cliff cells')
        terrain=bytearray(69+193*193*8)
        struct.pack_into('<IIff',terrain,53,193,193,-12288,-12288)
        for row in range(193):
            for col in range(193):
                off=69+(row*193+col)*8
                struct.pack_into('<H',terrain,off,8192)
                x,y=col*128-12288,row*128-12288
                terrain[off+7]=3 if abs(x+6000)<=512 and abs(y+4000)<=512 else 2
        original=b'MP3W'+struct.pack('<III',0,768,768)+bytes([64])*(768*768)
        plan={'ponds':[],'hills':[{'x':-6000,'y':-4000,'radius':576,'ramp_width':640}],'props':[]}
        changed=countryside_pathing(original,plan,bytes(terrain))
        idx=16+int((-3750+12288)//32)*768+int((-6240+12288)//32)
        self.assertFalse(changed[idx]&2)
        # DE W3E stores ramp as bit 0x40 in the 16-bit texture/flag word.
        for i in range(193*193):terrain[69+i*8+4]|=64
        ramped=countryside_pathing(original,plan,bytes(terrain))
        edge=16+int((-3984+12288)//32)*768+int((-6496+12288)//32)
        self.assertFalse(ramped[edge]&2)

    def test_native_water_flags_cover_the_rendered_pond_quad(self):
        from countryside_catalog import countryside_pathing
        terrain=bytearray(69+193*193*8)
        struct.pack_into('<IIff',terrain,53,193,193,-12288,-12288)
        for i in range(193*193):
            struct.pack_into('<H',terrain,69+i*8,7792)
            terrain[69+i*8+5]=1  # Native DE water bit is 0x0100.
            terrain[69+i*8+7]=2
        original=b'MP3W'+struct.pack('<III',0,768,768)+bytes([64])*(768*768)
        plan={'ponds':[{'x':-6000,'y':-4000,'radius':320,'surface':-24}],'hills':[],'props':[]}
        changed=countryside_pathing(original,plan,bytes(terrain))
        pixel=16+int((-4000+12288)//32)*768+int((-6400+12288)//32)
        self.assertTrue(changed[pixel]&2)

    def test_countryside_geometry_protects_castle_plots_and_northern_forest(self):
        import importlib.util
        self.assertIsNotNone(importlib.util.find_spec('countryside_catalog'),
                             'countryside catalog is missing')
        from countryside_catalog import protected, countryside_pathing
        self.assertTrue(protected(0, -500))
        self.assertTrue(protected(6000, -500))
        self.assertTrue(protected(4800, 8200))
        self.assertFalse(protected(-6000, -4000))
        original = b'MP3W'+struct.pack('<III',0,768,768)+bytes([64])*(768*768)
        changed = countryside_pathing(original, {'ponds':[{'x':-6000,'y':-4000,'radius':320}], 'hills':[]})
        self.assertEqual(changed[16:16+768],original[16:16+768])
        index=16+int((-4000+12288)//32)*768+int((-6000+12288)//32)
        self.assertTrue(changed[index]&2)
        self.assertTrue(changed[index]&8)
        self.assertFalse(changed[index]&64)
    def test_group_repair_changes_only_13_native_group_fields(self):
        self.assertTrue(hasattr(editor_layout, 'ungroup_forest_units'),
                        'targeted native group repair is missing')
        original = (ROOT / 'tests/fixtures/editor-unit-13-11.bin').read_bytes()
        records = []
        for identity, raw in ((20, 'htow'), (146, 'kInv'), (147, 'kL00')):
            r = bytearray(original)
            r[:4] = r[36:40] = raw.encode()
            struct.pack_into('<I', r, 115, identity)
            struct.pack_into('<i', r, 40, -1 if identity == 20 else 0)
            records.append(bytes(r))
        data = b'W3do' + struct.pack('<3I', 13, 11, 3) + b''.join(records)
        repaired = editor_layout.ungroup_forest_units(data)
        expected = bytearray(data)
        for i in (1, 2):
            struct.pack_into('<i', expected, 16+i*131+40, -1)
        self.assertEqual(repaired, bytes(expected))
        self.assertEqual(editor_layout.ungroup_forest_units(repaired), repaired)

    def test_shop_import_maps_creation_identity_not_record_order(self):
        self.assertTrue(hasattr(editor_layout, 'market_coordinates_from_units'),
                        'native shop coordinate importer is missing')
        records = [editor_layout.unit_record('hS02' if i == 18 else 'hS00',
                   i*128, -i*256, 0, 26, i, angle=math.pi/2)
                   for i in reversed(range(7, 20))]
        data = b'W3do' + struct.pack('<3I', 13, 11, 13) + b''.join(records)
        points = editor_layout.market_coordinates_from_units(data)
        self.assertEqual(points, tuple((i*128., -i*256., 90.) for i in range(7,20)))
        with self.assertRaises(ValueError):
            editor_layout.market_coordinates_from_units(data[:-131])


if __name__ == '__main__':
    unittest.main()
