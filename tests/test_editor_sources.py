import re
import struct
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT/'tools'))
from pipeline import runtime_script, compile_script, check_objects
from gui_sources import gui_sources
from objects import units, items


class Reader:
    def __init__(self, data):
        self.data, self.pos = data, 0
    def integer(self):
        value = struct.unpack_from('<I', self.data, self.pos)[0]
        self.pos += 4
        return value
    def string(self):
        end = self.data.index(b'\0', self.pos)
        value = self.data[self.pos:end].decode()
        self.pos = end+1
        return value


class EditorSourceRegression(unittest.TestCase):
    def test_editable_sources_reconstruct_compilable_runtime(self):
        script, wtg, wct = gui_sources(runtime_script('TEST-BUILD'))
        r = Reader(wtg)
        self.assertEqual(r.integer(), int.from_bytes(b'WTG!', 'little'))
        self.assertEqual(r.integer(), 7)
        self.assertEqual(r.integer(), 1)
        r.integer(); r.string(); r.integer(); r.integer()
        declarations, initialization = [], []
        for _ in range(r.integer()):
            name, typ = r.string(), r.string()
            r.integer()
            array, size, initialized, value = r.integer(), r.integer(), r.integer(), r.string()
            declarations.append('    '+typ+(' array ' if array else ' ')+'udg_'+name)
            if initialized and not array:
                initialization.append('    set udg_'+name+' = '+value)
        self.assertEqual(r.integer(), 1)
        self.assertEqual(r.string(), 'Initialize Kingdom Defense')
        r.string()
        self.assertEqual([r.integer() for _ in range(7)], [0,1,0,0,1,0,2])
        self.assertEqual(r.integer(), 0)
        self.assertEqual(r.string(), 'MapInitializationEvent')
        self.assertEqual([r.integer(),r.integer()], [1,0])
        self.assertEqual(r.integer(), 2)
        self.assertEqual(r.string(), 'CustomScriptCode')
        self.assertEqual(r.integer(), 1)
        self.assertEqual(r.integer(), 3)
        self.assertEqual(r.string(), 'call KLS_Init()')
        self.assertEqual([r.integer() for _ in range(3)], [0,0,0])
        self.assertEqual(r.pos, len(wtg))
        c = Reader(wct)
        self.assertEqual(c.integer(), 1)
        c.string()
        length = c.integer()
        runtime = wct[c.pos:c.pos+length].decode()
        c.pos += length
        self.assertEqual([c.integer(),c.integer()], [1,0])
        self.assertEqual(c.pos, len(wct))
        self.assertNotRegex(runtime, r'(?m)^globals\s*$')
        self.assertNotIn('MeleeInitVictoryDefeat', runtime)
        self.assertIn('if udg_KLS_Initialized then', runtime)
        self.assertIn('set udg_KLS_Prep = 45', runtime)
        tail = script[script.index('function main '):]
        tail = tail.replace('    call KLS_Init()', '    call InitGlobals()\n    call KLS_Init()')
        generated = 'globals\n'+'\n'.join(declarations)+'\nendglobals\nfunction InitGlobals takes nothing returns nothing\n'+'\n'.join(initialization)+'\nendfunction\n'+runtime+tail
        with tempfile.TemporaryDirectory() as folder:
            path=Path(folder)/'editor-regenerated.j'
            path.write_bytes(generated.encode())
            self.assertIn('Parse successful', compile_script(path))

    def test_malformed_object_data_is_rejected(self):
        self.assertGreater(check_objects(units()), 0)
        self.assertGreater(check_objects(items()), 0)
        with self.assertRaises((ValueError, struct.error)):
            check_objects(items()[:-1])


if __name__ == '__main__':
    unittest.main()
