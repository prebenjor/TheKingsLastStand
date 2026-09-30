"""Execute the straight-line JASS panel handlers with native UI boundaries.

The engine's global panel-hide symptom is injected between item events; this
checks our owner isolation and visibility repair, not native UI rendering.
"""
import re
import unittest
from types import SimpleNamespace
from test_market_controls import function_body, runtime_script
from test_multiplayer_ui_safety import local_allocations


def compile_handler(script, name, env):
    lines = function_body(script, name).splitlines()[1:-1]
    header = function_body(script, name).splitlines()[0]
    args = re.search(r' takes (.*?) returns ', header)[1]
    parameters = '' if args == 'nothing' else ', '.join(token.strip().split()[-1] for token in args.split(','))
    output = [f'def {name}({parameters}):']
    assigned = set(re.findall(r'^\s*set (KLS_\w+) =', '\n'.join(lines), re.M))
    if assigned:
        output.append('    global ' + ', '.join(sorted(assigned)))
    depth = 1
    for line in lines:
        line = line.split('//', 1)[0].strip()
        if not line:
            continue
        line = re.sub(r'\bnull\b', 'None', line)
        line = re.sub(r'\btrue\b', 'True', line)
        line = re.sub(r'\bfalse\b', 'False', line)
        line = re.sub(r'\bfunction (?=\w+)', '', line)
        if line in ('endif', 'endloop'):
            depth -= 1
            continue
        if line == 'loop':
            output.append('    ' * depth + 'while True:')
            depth += 1
            continue
        if line.startswith('exitwhen '):
            output.append('    ' * depth + 'if ' + line[9:] + ': break')
            continue
        if line.startswith(('elseif ', 'else')):
            depth -= 1
        line = re.sub(r'\bnull\b', 'None', line)
        line = re.sub(r'\btrue\b', 'True', line)
        line = re.sub(r'\bfalse\b', 'False', line)
        line = re.sub(r'^local \w+ (\w+)$', r'\1 = None', line)
        line = re.sub(r'^local \w+ ', '', line)
        line = re.sub(r'^(set|call) ', '', line)
        line = re.sub(r'^elseif ', 'elif ', line)
        if line.endswith(' then'):
            line = line[:-5] + ':'
        elif line == 'else':
            line = 'else:'
        output.append('    ' * depth + line)
        if line.endswith(':'):
            depth += 1
    exec('\n'.join(output), env)


class BackpackPanel(unittest.TestCase):
    def test_panel_initialization_does_not_allocate_client_local_handles(self):
        self.assertEqual(local_allocations(runtime_script('KLS-D-TEST'), 'KLS_PackPanelInit'), [])

    def clients(self):
        script = runtime_script('KLS-D-TEST')
        heroes = [SimpleNamespace(owner=p, selected=True, capacity=30) for p in range(4)]
        clients = []
        for p in range(4):
            panels = {'bag': False, 'gear': False, 'backdrop': False}
            env = dict(KLS_PackOpenLocal=False, KLS_PackFramesReady=True,
                       KLS_PackBagFrame='bag', KLS_PackEquipmentFrame='gear',
                       KLS_PackBackdropFrame='backdrop', KLS_Hero=heroes,
                       KLS_Active=[True]*4, KLS_Ended=False,
                       GetLocalPlayer=lambda p=p:p, GetPlayerId=lambda p:p,
                       Player=lambda p:p, GetOwningPlayer=lambda u:u.owner,
                       GetItemTypeId=lambda item:item,
                       IsUnitSelected=lambda u,p:u.selected,
                       UnitExtendedInventorySize=lambda u:u.capacity,
                       GetWidgetLife=lambda u:100,
                       BlzFrameSetVisible=lambda frame,value,panels=panels:panels.__setitem__(frame,value))
            compile_handler(script, 'KLS_PackPanelRefresh', env)
            compile_handler(script, 'KLS_PackPanelUsed', env)
            compile_handler(script, 'KLS_PackPanelEscape', env)
            clients.append((env, panels))
        return heroes, clients

    def use(self, clients, unit, item='ebac'):
        for env, panels in clients:
            env['GetManipulatingUnit'] = lambda:unit
            env['GetManipulatedItem'] = lambda:item
            env['KLS_PackPanelUsed']()
            # Reproduce the reported native close affecting every client.
            panels.update(dict.fromkeys(panels, False))
            env['KLS_PackPanelRefresh']()

    def test_four_players_open_and_close_independently(self):
        heroes, clients = self.clients()
        for p in range(4):
            self.use(clients, heroes[p])
            self.assertEqual([c[1]['bag'] for c in clients], [i <= p for i in range(4)])
        self.use(clients, heroes[1])
        self.assertEqual([c[1]['bag'] for c in clients], [True, False, True, True])
        for env, panels in clients:
            self.assertEqual(panels['gear'], panels['bag'])
            self.assertEqual(panels['backdrop'], panels['bag'])

    def test_other_items_and_nonhero_units_cannot_toggle_panel(self):
        heroes, clients = self.clients()
        self.use(clients, heroes[0], 'phea')
        self.use(clients, SimpleNamespace(owner=0))
        self.assertEqual([c[1]['bag'] for c in clients], [False]*4)

    def test_deselecting_hero_closes_only_that_clients_panel(self):
        heroes, clients = self.clients()
        self.use(clients, heroes[0])
        self.use(clients, heroes[1])
        heroes[0].selected = False
        for env, _ in clients:
            env['KLS_PackPanelRefresh']()
        self.assertEqual([c[1]['bag'] for c in clients], [False, True, False, False])

    def test_missing_native_frames_leaves_native_behavior_alone(self):
        heroes, clients = self.clients()
        env, panels = clients[0]
        env['KLS_PackFramesReady'] = False
        panels['bag'] = True
        env['KLS_PackPanelRefresh']()
        self.assertTrue(panels['bag'])

    def test_match_end_closes_all_panels(self):
        heroes, clients = self.clients()
        self.use(clients, heroes[2])
        for env, panels in clients:
            env['KLS_Ended'] = True
            env['KLS_PackPanelRefresh']()
            self.assertFalse(panels['bag'])
            self.assertFalse(env['KLS_PackOpenLocal'])

    def test_escape_closes_only_the_pressing_players_panel(self):
        heroes, clients = self.clients()
        self.use(clients, heroes[0])
        self.use(clients, heroes[1])
        for env, _ in clients:
            env['GetTriggerPlayer'] = lambda:1
            env['KLS_PackPanelEscape']()
            env['KLS_PackPanelRefresh']()
        self.assertEqual([c[1]['bag'] for c in clients], [True, False, False, False])

    def test_native_capacity_is_required_without_mutating_inventory(self):
        heroes, clients = self.clients()
        self.use(clients, heroes[0])
        heroes[0].capacity = 0
        clients[0][0]['KLS_PackPanelRefresh']()
        self.assertFalse(clients[0][1]['bag'])
        self.assertEqual(heroes[0].capacity, 0)

