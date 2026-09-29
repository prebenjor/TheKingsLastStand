"""Runtime diagnostics for the reported Peasant/Acolyte identity mismatch."""
import unittest
from test_equipment import ROOT


class WorkerIdentityDiagnostics(unittest.TestCase):
    def test_debug_report_includes_runtime_race_and_actual_worker_type(self):
        game = (ROOT / 'source' / 'game.j').read_text()
        diagnostics = (ROOT / 'source' / 'diagnostics.j').read_text()
        self.assertIn("unit array KLS_FirstWorker", game)
        self.assertIn("KLS_CreateUnit(Player(i), 'hpea'", game)
        self.assertIn('set KLS_FirstWorker[i] = u', game)
        start = diagnostics.index('function KLS_ShowDiagnostics')
        end = diagnostics.index('endfunction', start)
        report = diagnostics[start:end]
        self.assertIn('KLS_RaceName(KLS_PlayerRace[i])', report)
        self.assertIn('GetUnitTypeId(KLS_FirstWorker[i])', report)
        self.assertIn('GetObjectName(GetUnitTypeId(KLS_FirstWorker[i]))', report)
        self.assertIn('GetUnitName(KLS_FirstWorker[i])', report)

    def test_debug_report_identifies_the_calling_players_selected_units(self):
        diagnostics = (ROOT / 'source' / 'diagnostics.j').read_text()
        start = diagnostics.index('function KLS_ShowDiagnostics')
        end = diagnostics.index('endfunction', start)
        report = diagnostics[start:end]
        self.assertIn('GetUnitsSelectedAll(p)', report)
        self.assertIn('GetObjectName(GetUnitTypeId(selectedUnit))', report)
        self.assertIn('GetUnitName(selectedUnit)', report)
        self.assertIn('GetPlayerId(GetOwningPlayer(selectedUnit))', report)
        self.assertIn('DestroyGroup(selectedUnits)', report)

    def test_diag_keeps_errors_and_warnings_visible_after_the_recent_log_window_rolls_over(self):
        diagnostics = (ROOT / 'source' / 'diagnostics.j').read_text()
        self.assertIn('string array KLS_DiagErrorLines', diagnostics)
        self.assertIn('integer KLS_DiagErrorCount = 0', diagnostics)

        start = diagnostics.index('function KLS_Log')
        end = diagnostics.index('endfunction', start)
        logger = diagnostics[start:end]
        for severity in ('ERROR', 'FATAL'):
            self.assertIn(f'SubString(message,0,5) == "{severity}"', logger)
        self.assertIn('SubString(message,0,4) == "WARN"', logger)
        self.assertIn('KLS_DiagErrorLines[ModuloInteger(KLS_DiagErrorCount, 32)]', logger)

        start = diagnostics.index('function KLS_ShowDiagnostics')
        end = diagnostics.index('endfunction', start)
        report = diagnostics[start:end]
        self.assertIn('Recent errors/warnings:', report)
        self.assertIn('KLS_DiagErrorLines[ModuloInteger(errorIndex, 32)]', report)
        self.assertIn('IMaxBJ(0, KLS_DiagErrorCount - 8)', report)

    def test_diag_error_total_counts_item_and_spawn_failures_once(self):
        diagnostics = (ROOT / 'source' / 'diagnostics.j').read_text()
        start = diagnostics.index('function KLS_Log')
        end = diagnostics.index('endfunction', start)
        logger = diagnostics[start:end]
        self.assertIn('if SubString(message,0,5) == "ERROR" then', logger)
        self.assertIn('set KLS_DiagFailureEvents = KLS_DiagFailureEvents + 1', logger)

        start = diagnostics.index('function KLS_CreateUnitChecked')
        end = diagnostics.index('endfunction', start)
        checked_unit = diagnostics[start:end]
        start = diagnostics.index('function KLS_CreateDestructableChecked')
        end = diagnostics.index('endfunction', start)
        checked_scenery = diagnostics[start:end]
        self.assertNotIn('KLS_DiagFailureEvents', checked_unit)
        self.assertNotIn('KLS_DiagFailureEvents', checked_scenery)

        start = diagnostics.index('function KLS_ShowDiagnostics')
        end = diagnostics.index('endfunction', start)
        report = diagnostics[start:end]
        self.assertIn('errors=" + I2S(KLS_DiagFailureEvents)', report)


if __name__ == '__main__':
    unittest.main()
