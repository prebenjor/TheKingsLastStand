"""Generate editor variables plus a GUI initialization trigger (WTG v7)."""
import re
import struct


def z(s):
    return s.encode() + b'\0'


def gui_sources(script):
    block = re.search(r'^globals\n(.*?)^endglobals\n', script, re.S | re.M)
    variables = []
    for line in block.group(1).splitlines():
        match = re.match(r'\s*(\w+)\s+(?:(array)\s+)?(KLS_\w+)(?:\s*=\s*(.*))?$', line)
        if match:
            typ, array, name, value = match.groups()
            variables.append((typ, bool(array), name, value))
    for typ, array, name, value in variables:
        script = re.sub(r'\b' + name + r'\b', 'udg_' + name, script)
    runtime = script[script.index('endglobals')+len('endglobals'):script.index('function main ')]
    wct = struct.pack('<I', 1) + z('The King\'s Last Stand runtime: generated from source modules.')
    code = runtime.encode()
    wct += struct.pack('<I', len(code)) + code + struct.pack('<II', 1, 0)
    wtg = bytearray(b'WTG!' + struct.pack('<III', 7, 1, 0) + z('Initialization') + struct.pack('<III', 0, 2, len(variables)))
    for typ, array, name, value in variables:
        initialized = value is not None and value != 'null'
        wtg.extend(z(name) + z(typ) + struct.pack('<IIII', 1, int(array), (820 if name == "KLS_Roster" else 72) if array else 1, int(initialized)) + z(value if initialized else ''))
    wtg.extend(struct.pack('<I', 1) + z('Initialize Kingdom Defense') + z('Start the custom RPG runtime.'))
    wtg.extend(struct.pack('<7I', 0, 1, 0, 0, 1, 0, 2))
    wtg.extend(struct.pack('<I', 0) + z('MapInitializationEvent') + struct.pack('<II', 1, 0))
    wtg.extend(struct.pack('<I', 2) + z('CustomScriptCode') + struct.pack('<I', 1))
    wtg.extend(struct.pack('<I', 3) + z('call KLS_Init()') + struct.pack('<III', 0, 0, 0))
    return script, bytes(wtg), wct
