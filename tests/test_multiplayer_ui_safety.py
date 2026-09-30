"""Reject client-local handle allocation in the generated UI call graph.

This is a static multiplayer safety check, not a Warcraft engine simulation.
Moving event registration (including through a helper) under a local-player
branch must fail even when the generated JASS still compiles.
"""
import re
import unittest
from test_market_controls import function_body, runtime_script


def local_allocations(script, entry):
    allocations = re.compile(r'\b(?:BlzCreateFrame\w*|BlzTriggerRegister\w*|CreateTrigger|CreateTimer|DialogCreate)\s*\(')
    violations = []

    def visit(name, inherited=False, chain=()):
        if name in chain:
            return
        stack = [inherited]
        for line in function_body(script, name).splitlines()[1:-1]:
            line = line.split('//', 1)[0].strip()
            if line.startswith('if '):
                stack.append(stack[-1] or 'GetLocalPlayer()' in line)
            elif line == 'endif':
                stack.pop()
            if stack[-1] and allocations.search(line):
                violations.append((name, line))
            for callee in re.findall(r'\b(KLS_\w+)\(', line):
                if re.search(r'^function ' + callee + r' takes', script, re.M):
                    visit(callee, stack[-1], chain + (name,))
    visit(entry)
    return violations


class MultiplayerUISafety(unittest.TestCase):
    def test_vote_registration_is_identical_on_all_clients(self):
        self.assertEqual(local_allocations(runtime_script('KLS-D-TEST'), 'KLS_VoteUIInit'), [])

    def test_stat_registration_is_identical_on_all_clients(self):
        self.assertEqual(local_allocations(runtime_script('KLS-D-TEST'), 'KLS_ProgressionInit'), [])

    def test_checker_follows_allocation_helpers(self):
        fixture = '''function KLS_Helper takes nothing returns nothing
call CreateTrigger()
endfunction
function KLS_Init takes nothing returns nothing
if GetLocalPlayer() == Player(0) then
call KLS_Helper()
endif
endfunction'''
        self.assertEqual(len(local_allocations(fixture, 'KLS_Init')), 1)

