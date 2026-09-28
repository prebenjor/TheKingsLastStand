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


if __name__ == '__main__':
    unittest.main()
