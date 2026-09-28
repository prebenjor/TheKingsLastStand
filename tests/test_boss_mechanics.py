import re
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'tools'))
from wave_rosters import BOSS_MECHANICS, boss_mechanic_for_wave, boss_script
from pipeline import runtime_script


def function_body(script, name):
    match = re.search(r'^function ' + re.escape(name) + r' takes [\s\S]*?^endfunction$', script, re.M)
    if not match:
        raise AssertionError('Missing runtime function ' + name)
    return match.group()


class BossMechanics(unittest.TestCase):
    def test_boss_waves_map_to_their_approved_distinct_actions(self):
        expected = (
            (10, 1, ('slam',)),
            (20, 2, ('summon',)),
            (30, 3, ('tower_suppression',)),
            (40, 4, ('slam', 'summon', 'tower_suppression')),
            (50, 5, ('slam', 'summon', 'tower_suppression')),
        )
        actual = tuple((row['wave'], row['id'], row['actions']) for row in BOSS_MECHANICS)
        self.assertEqual(actual, expected)
        self.assertEqual(tuple(row['warning'] for row in BOSS_MECHANICS), (
            'Leave the marked circle.',
            'Skeletons and felguards are incoming.',
            'Defender towers will be suppressed.',
            'Dodge, then survive the horde and tower blackout.',
            'Dodge the slam, stop the reinforcements, and weather the tower blackout.',
        ))
        for wave, mechanic, _ in expected:
            self.assertEqual(boss_mechanic_for_wave(wave), mechanic)
        for wave in (1, 9, 11, 19, 21, 29, 31, 39, 41):
            self.assertEqual(boss_mechanic_for_wave(wave), 0)

    def test_generated_runtime_uses_boss_plan_and_keeps_warning_in_hud_until_resolution(self):
        script = runtime_script('KLS-D-TEST')
        self.assertIn(boss_script(), script)
        self.assertIn('set KLS_BossMechanic = KLS_BossMechanicForWave(KLS_Wave)', script)
        self.assertIn('call KLS_BossExecuteMechanic()', script)
        self.assertIn('call KLS_HUDRow(6, "Boss warning", KLS_BossThreatText())', script)
        self.assertIn('KLS_BossMechanicWarning(KLS_BossMechanic)', script)
        self.assertIn('MultiboardSetRowCount(KLS_HUD, 7)', script)
        self.assertIn('call KLS_SetTowersPaused(true)', script)
        self.assertIn('call KLS_SetTowersPaused(false)', script)

    def test_boss_summons_follow_the_king_route_and_are_counted_once(self):
        script = runtime_script('KLS-D-TEST')
        summon = function_body(script, 'KLS_BossSummon')
        self.assertIn("set kind = 'uske'", summon)
        self.assertIn("set kind = 'nfgu'", summon)
        self.assertEqual(summon.count('GroupAddUnit(KLS_Enemies,summon)'), 1)
        self.assertEqual(summon.count('set KLS_Alive = KLS_Alive+1'), 1)
        self.assertIn('IssuePointOrder(summon,"attack",0,350)', summon)
        self.assertNotIn('IssuePointOrder(summon,"attack",0,-2700)', summon)

    def test_failed_wave_enemy_creation_does_not_count_a_null_unit_or_finish_as_victory(self):
        script = runtime_script('KLS-D-TEST')
        spawn = function_body(script, 'KLS_Spawn')
        self.assertIn('local boolean spawnFailed = false', spawn)
        self.assertRegex(spawn, r'if u != null then[\s\S]*?GroupAddUnit\(KLS_Enemies, u\)[\s\S]*?set KLS_Alive = KLS_Alive \+ 1[\s\S]*?else\s+set spawnFailed = true')
        self.assertIn('call KLS_AbortForSpawnFailure("wave enemy", kind)', spawn)
        self.assertIn('call KLS_AbortForSpawnFailure("wave boss", kind)', spawn)
        self.assertIn('or spawnFailed', spawn)
        abort = function_body(script, 'KLS_AbortForSpawnFailure')
        self.assertIn('set KLS_Ended = true', abort)
        self.assertIn('call CustomDefeatBJ', abort)

    def test_failed_boss_reinforcement_is_not_counted_or_fatal_to_the_match(self):
        script = runtime_script('KLS-D-TEST')
        summon = function_body(script, 'KLS_BossSummon')
        self.assertRegex(summon, r'if summon != null then[\s\S]*?GroupAddUnit\(KLS_Enemies,summon\)[\s\S]*?set KLS_Alive = KLS_Alive\+1[\s\S]*?else\s+set spawnFailed = true')
        self.assertIn('KLS_CreateUnitOptional(Player(11),kind,', summon)
        self.assertIn('"boss reinforcement"', summon)
        self.assertNotIn('KLS_AbortForSpawnFailure', summon)

    def test_optional_spawn_failures_have_context_without_global_abort(self):
        script = runtime_script('KLS-D-TEST')
        for function, fatal_token in (
            ('KLS_CreateUnitOptional', 'KLS_AbortForSpawnFailure'),
            ('KLS_CreateDestructableOptional', 'KLS_AbortForSpawnFailure'),
        ):
            body = function_body(script, function)
            with self.subTest(function=function):
                self.assertIn('false', body)
                self.assertNotIn(fatal_token, body)
        checked_unit = function_body(script, 'KLS_CreateUnitChecked')
        checked_destructable = function_body(script, 'KLS_CreateDestructableChecked')
        for body in (checked_unit, checked_destructable):
            self.assertIn('if fatal then', body)
            self.assertRegex(body, r'KLS_AbortForSpawnFailure\(context,\s*kind\)')
            self.assertIn('ERROR optional', body)
            self.assertIn('context=', body)
            self.assertIn('GetObjectName(kind)', body)
            self.assertIn('R2S(x)', body)

    def test_optional_gameplay_callers_use_nonfatal_spawn_paths(self):
        script = runtime_script('KLS-D-TEST')
        expected = {
            'KLS_AddTree': "KLS_CreateDestructableOptional('LTlt', x, y, 0, 1.0, 0, \"base harvest tree\")",
            'KLS_GrovePlant': "KLS_CreateDestructableOptional('LTlt',x,y,0,1,0,\"ability grove tree\")",
            'KLS_SignatureCast': 'KLS_CreateUnitOptional(owner,\'hS01\'',
            'KLS_StorySpawnEncounter': 'KLS_CreateUnitOptional(Player(11),kind,',
            'KLS_StoryBegin': "KLS_CreateUnitOptional(Player(PLAYER_NEUTRAL_PASSIVE),'hpea'",
        }
        for function, fragment in expected.items():
            with self.subTest(function=function):
                self.assertIn(fragment, function_body(script, function))
        encounter = function_body(script, 'KLS_StorySpawnEncounter')
        self.assertIn('call KLS_StoryEncounterAbort()', encounter)
        abort = function_body(script, 'KLS_StoryEncounterAbort')
        self.assertIn('RemoveUnit(remaining)', abort)
        self.assertIn('set KLS_StoryRemaining = 0', abort)
        self.assertNotIn('KLS_AbortForSpawnFailure', abort)

    def test_required_spawn_path_still_aborts_and_wave_enemies_remain_required(self):
        script = runtime_script('KLS-D-TEST')
        for function in ('KLS_CreateUnit', 'KLS_CreateDestructable'):
            body = function_body(script, function)
            with self.subTest(function=function):
                self.assertIn('true', body)
        spawn = function_body(script, 'KLS_Spawn')
        self.assertIn('KLS_CreateUnit(Player(11), kind,', spawn)
        self.assertIn('call KLS_AbortForSpawnFailure("wave enemy", kind)', spawn)

    def test_boss_reward_is_once_on_death_and_wave_40_continues_without_victory(self):
        script = runtime_script('KLS-D-TEST')
        death = function_body(script, 'KLS_Death')
        self.assertEqual(death.count('call KLS_BossReward()'), 1)
        self.assertRegex(death, r'if dead == KLS_Boss then[\s\S]*?call KLS_BossReward\(\)[\s\S]*?call KLS_Message\("Boss defeated!')
        self.assertRegex(death, r'if GetWidgetLife\(KLS_King\) <= 0\.405 then\s+call KLS_End\(false\)[\s\S]*?else[\s\S]*?call KLS_BossReward\(\)')
        self.assertNotIn('call KLS_End(true)', death)
        self.assertNotRegex(death, r'if KLS_Alive == 0 then[\s\S]{0,180}call KLS_BossReward\(\)')
        self.assertIn('if not KLS_Ended and KLS_Alive == 0 then', death)
        self.assertIn('set KLS_Boss = null', death)

    def test_spawn_wrappers_name_failures_and_abort_before_callers_use_null_handles(self):
        script = runtime_script('KLS-D-TEST')
        create_unit = function_body(script, 'KLS_CreateUnit')
        create_destructable = function_body(script, 'KLS_CreateDestructable')
        self.assertIn('KLS_CreateUnitChecked(owner,kind,x,y,facing,true,"required unit")', create_unit)
        self.assertIn('KLS_CreateDestructableChecked(kind,x,y,facing,scale,variation,true,"required destructable")', create_destructable)
        checked_unit = function_body(script, 'KLS_CreateUnitChecked')
        checked_destructable = function_body(script, 'KLS_CreateDestructableChecked')
        self.assertIn('if fatal then', checked_unit)
        self.assertIn('if fatal then', checked_destructable)
        self.assertRegex(checked_unit, r'KLS_AbortForSpawnFailure\(context,\s*kind\)')
        self.assertRegex(checked_destructable, r'KLS_AbortForSpawnFailure\(context,\s*kind\)')
        self.assertIn('GetObjectName(kind)', checked_unit)
        self.assertIn('GetObjectName(kind)', checked_destructable)

    def test_startup_and_combat_callers_guard_handles_after_failed_creation(self):
        script = runtime_script('KLS-D-TEST')
        cases = {
            'KLS_AddTree': (r'if tree == null then\s+return\s+endif[\s\S]*?SetDestructableMaxLife',),
            'KLS_BuildLandscape': (
                r'set gate = KLS_CreateDestructable[\s\S]*?if gate == null then\s+return\s+endif[\s\S]*?SetDestructableInvulnerable',
            ),
            'KLS_CreateShops': (
                r'set KLS_Shops\[tier\*2\+i\] = KLS_CreateUnit[\s\S]*?if KLS_Shops\[tier\*2\+i\] == null then\s+return\s+endif[\s\S]*?BlzSetUnitName',
                r'set KLS_Shops\[10\] = KLS_CreateUnit[\s\S]*?if KLS_Shops\[10\] == null then\s+return\s+endif[\s\S]*?BlzSetUnitName',
                r'set KLS_Shops\[11\] = KLS_CreateUnit[\s\S]*?if KLS_Shops\[11\] == null then\s+return\s+endif[\s\S]*?BlzSetUnitName',
            ),
            'KLS_GrovePlant': (r'KLS_GroveTree\[KLS_GroveCount\] = KLS_CreateDestructable[\s\S]*?if KLS_GroveTree\[KLS_GroveCount\] == null then\s+return\s+endif[\s\S]*?set KLS_GroveCount',),
            'KLS_WaveEnvironmentInit': (r'set KLS_RestorePool = CreateUnit[\s\S]*?if KLS_RestorePool != null then[\s\S]*?BlzSetUnitName[\s\S]*?else[\s\S]*?ERROR restoring spring model unavailable[\s\S]*?set KLS_PoolClock = CreateTimer\(\)[\s\S]*?TimerStart\(KLS_PoolClock,1\.0,true,function KLS_PoolTick\)',),
            'KLS_ChooseHero': (r'set KLS_Hero\[p\] = KLS_CreateUnit[\s\S]*?if KLS_Hero\[p\] == null then\s+return\s+endif[\s\S]*?set KLS_ClassChosen\[p\] = true',),
            'KLS_SelectionInit': (r'set KLS_Preview\[n\] = KLS_CreateUnit[\s\S]*?if KLS_Preview\[n\] == null then\s+return\s+endif[\s\S]*?SetUnitInvulnerable',),
            'KLS_SignatureCast': (r'set u = KLS_CreateUnitOptional\(owner,KLS_SignatureSummon\[n\][\s\S]*?if u == null then\s+exitwhen true\s+endif[\s\S]*?SetUnitUseFood\(u,false\)',),
        }
        for name, patterns in cases.items():
            body = function_body(script, name)
            for pattern in patterns:
                with self.subTest(function=name, pattern=pattern):
                    self.assertRegex(body, pattern)
        init = function_body(script, 'KLS_Init')
        for pattern in (
            r'call KLS_BuildLandscape\(\)\s+if KLS_Ended then\s+return\s+endif',
            r"set u = KLS_CreateUnit\(Player\(PLAYER_NEUTRAL_PASSIVE\), 'hC01'[\s\S]*?if u == null then\s+return\s+endif[\s\S]*?set KLS_Castle = u[\s\S]*?BlzSetUnitName",
            r"set KLS_King = KLS_CreateUnit[\s\S]*?if KLS_King == null then\s+return\s+endif[\s\S]*?BlzSetUnitName",
            r"set u = KLS_CreateUnit\(Player\(PLAYER_NEUTRAL_PASSIVE\), 'ngol'[\s\S]*?if u == null then\s+return\s+endif[\s\S]*?SetResourceAmount",
            r"set KLS_Altar\[i\] = KLS_CreateUnit[\s\S]*?if KLS_Altar\[i\] == null then\s+return\s+endif",
            r'call KLS_SelectionInit\(\)\s+if KLS_Ended then\s+return\s+endif',
        ):
            with self.subTest(function='KLS_Init', pattern=pattern):
                self.assertRegex(init, pattern)
        self.assertEqual(len(re.findall(r'(?<!KLS_)CreateUnit\(', script)), 3,
                         'direct unit creation is limited to the optional spring visual and recoverable Undead mine conversion')

    def test_each_boss_action_is_limited_to_its_approved_wave_mechanics(self):
        script = runtime_script('KLS-D-TEST')
        execute = function_body(script, 'KLS_BossExecuteMechanic')
        self.assertIn('if KLS_BossMechanic == 1 or KLS_BossMechanic == 4 or KLS_BossMechanic == 5 then', execute)
        self.assertIn('if KLS_BossMechanic == 2 or KLS_BossMechanic == 4 or KLS_BossMechanic == 5 then', execute)
        self.assertIn('if KLS_BossMechanic == 3 or KLS_BossMechanic == 4 or KLS_BossMechanic == 5 then', execute)


if __name__ == '__main__':
    unittest.main()
