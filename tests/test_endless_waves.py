"""Regression coverage for the campaign crossover and endless wave loop."""
import hashlib
import json
import re
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'tools'))
sys.path.insert(0, str(ROOT / 'tests'))

import wave_rosters
from equipment_catalog import item_catalog
from objects import units
from pipeline import runtime_script
from test_equipment import decode, slk


def roster_rows(script):
    sizes = {int(wave): int(size) for wave, size in re.findall(
        r"set KLS_RosterSize\[(\d+)\] = (\d+)", script)}
    entries = {}
    for index, code in re.findall(r"set KLS_Roster\[(\d+)\] = '(.{4})'", script):
        wave, slot = divmod(int(index), 20)
        entries.setdefault(wave, {})[slot] = code
    return {wave: [entries[wave][i] for i in range(sizes[wave])] for wave in sizes}


class EndlessCampaignWaves(unittest.TestCase):
    def test_original_waves_one_to_forty_remain_byte_for_byte_equivalent_as_data(self):
        original = wave_rosters.wave_rosters()
        fingerprint = hashlib.sha256(
            json.dumps(original, separators=(',', ':')).encode()).hexdigest()
        self.assertEqual(len(original), 40)
        self.assertEqual(fingerprint, '1ffddcd7613c10f2ffebc09524e87cdf525e1826a2a535b871c0d52388b8ae3d')

    def test_generated_crossover_block_contains_all_five_campaign_forces_and_convergence(self):
        rows = roster_rows(wave_rosters.wave_script())
        self.assertEqual(set(rows), set(range(1, 51)))
        naga = {'nmyr', 'nnsw', 'nnmg', 'nnrg', 'nhyc', 'nwgs'}
        blood_elf = {'nbel', 'nbee', 'hbew'}
        fel_orc = {'nchg', 'nchr', 'nchw', 'nckb'}
        legion = {'nfel', 'nfgu', 'nbal', 'ninf'}
        scourge = {'uske', 'ugho', 'ucry', 'nska', 'unec', 'uabo', 'umtw'}
        factions = (naga, blood_elf, fel_orc, legion, scourge)
        crossover = [code for wave in range(41, 51) for code in rows[wave]]
        for faction in factions:
            self.assertTrue(faction.intersection(crossover), faction)
            self.assertTrue(faction.intersection(rows[49]), faction)
        self.assertLessEqual(max(map(len, rows.values())), 20)

    def test_endless_roster_source_index_stays_within_the_ten_generated_rows(self):
        resolver = getattr(wave_rosters, 'roster_source_wave', None)
        self.assertIsNotNone(resolver, 'generator needs a bounded endless roster resolver')
        rows = wave_rosters.wave_rosters()
        endless = getattr(wave_rosters, 'endless_wave_rosters', None)
        self.assertIsNotNone(endless)
        endless = endless()
        self.assertEqual(len(endless), 10)
        for wave in range(1, 10001):
            expected = wave if wave <= 40 else 41 + (wave - 41) % 10
            self.assertEqual(resolver(wave), expected)
            if wave > 40:
                self.assertEqual(resolver(wave), 41 + (wave - 41) % len(endless))
        self.assertEqual(resolver(51), 41)
        self.assertEqual(resolver(60), 50)
        self.assertEqual(resolver(61), 41)

    def test_new_wave_and_boss_units_resolve_to_installed_campaign_models_and_armor(self):
        rows = roster_rows(wave_rosters.wave_script())
        ui = slk('UnitUI.slk')
        balance = slk('UnitBalance.slk')
        data = slk('UnitData.slk')
        abilities = slk('UnitAbilities.slk')
        crossover_units = {code for wave in range(41, 51) for code in rows[wave]}
        campaign_units = {
            'nmyr', 'nnsw', 'nnmg', 'nnrg', 'nhyc', 'nwgs',
            'nbel', 'nbee', 'hbew', 'nchg', 'nchr', 'nchw', 'nckb',
        }
        for code in crossover_units | set(wave_rosters.ENDLESS_BOSS_UNITS):
            self.assertIn(code, ui, code)
            self.assertIn(code, balance, code)
            self.assertIn(code, data, code)
            self.assertIn(31, balance[code], 'installed armor for ' + code)
            self.assertIn(code, abilities, code)
        for code in campaign_units | set(wave_rosters.ENDLESS_BOSS_UNITS):
            self.assertEqual(ui[code].get(8), '1', 'not tagged as a campaign unit: ' + code)
            self.assertTrue(ui[code].get(5), 'campaign model is missing: ' + code)
            self.assertTrue(data[code].get(12), 'campaign movement data is missing: ' + code)
        emitted = decode(units())
        visual_and_armor_fields = {'umdl', 'uani', 'udef', 'udty'}
        for code in campaign_units | set(wave_rosters.ENDLESS_BOSS_UNITS):
            if code in emitted:
                fields = emitted[code][1]
                self.assertFalse(visual_and_armor_fields.intersection(
                    field for field, _level in fields),
                    'campaign model, animation, and armor must remain native: ' + code)
        self.assertEqual(ui['Hvsh'][5], 'ladyvashj')
        self.assertEqual(data['Hvsh'][12], 'amph')

    def test_original_bosses_stay_and_campaign_leaders_rotate_every_ten_waves(self):
        resolver = getattr(wave_rosters, 'boss_unit_for_wave', None)
        self.assertIsNotNone(resolver, 'generator needs to expose the boss rotation')
        expected = {
            10: 'Udea', 20: 'Ulic', 30: 'Udre', 40: 'Uanb',
            50: 'Hvsh', 60: 'Usyl', 70: 'Uanb', 80: 'Hjsm',
            90: 'Ujsm', 100: 'Hvsh',
        }
        for wave, code in expected.items():
            self.assertEqual(resolver(wave), code)
        for wave in (41, 49, 51, 59, 61, 69, 71):
            self.assertIsNone(resolver(wave))

    def test_boss_mechanics_repeat_from_wave_fifty(self):
        expected = {40: 4, 50: 5, 60: 1, 70: 2, 80: 3, 90: 5, 100: 1}
        for wave, mechanic in expected.items():
            self.assertEqual(wave_rosters.boss_mechanic_for_wave(wave), mechanic)
        for wave in (41, 49, 51, 59, 61, 69, 71):
            self.assertEqual(wave_rosters.boss_mechanic_for_wave(wave), 0)
        self.assertIn('function KLS_BossUnitForWave', wave_rosters.boss_script())

    def test_wave_scaling_tracking_and_debug_reach_are_kept_for_endless_spawns(self):
        script = runtime_script('KLS-D-TEST')
        spawn = re.search(r'^function KLS_Spawn takes[\s\S]*?^endfunction$', script, re.M).group()
        self.assertIn('set count = 7 + KLS_Wave * 2 + KLS_Players * 3', spawn)
        self.assertIn('180 + KLS_Wave * 55 + KLS_Players * 35', spawn)
        self.assertIn('6 + KLS_Wave * 2', spawn)
        self.assertIn('KLS_RosterSourceWave(KLS_Wave)', spawn)
        self.assertIn('call GroupAddUnit(KLS_Enemies, u)', spawn)
        self.assertIn('set KLS_Alive = KLS_Alive + 1', spawn)
        chat = re.search(r'^function KLS_Chat takes[\s\S]*?^endfunction$', script, re.M).group()
        self.assertRegex(chat, r'S2I\(SubString\(s, 6, StringLength\(s\)\)\) <= 1000')

    def test_later_bosses_give_personal_legendary_catalog_items_but_old_relics_stay(self):
        legendaries = {entry['rawcode'] for entry in item_catalog()
                       if entry['tier'] == 4 and not entry.get('crafted')}
        self.assertTrue(legendaries)
        script = runtime_script('KLS-D-TEST')
        reward = re.search(r'^function KLS_BossReward takes[\s\S]*?^endfunction$', script, re.M).group()
        for relic in ("'I010'", "'I011'", "'I012'", "'I013'"):
            self.assertIn(relic, reward)
        self.assertIn('KLS_Wave >= 50', reward)
        self.assertIn('KLS_RandomCatalogDrop(4)', reward)
        self.assertIn('call KLS_PersonalRewardEnqueue(i,gear,"Boss")', reward)
        self.assertNotIn('CreateItem(', reward)
        for code in legendaries:
            self.assertIn("return '" + code + "'", script)

    def test_wave_forty_continues_king_death_ends_and_hud_shows_highest_wave(self):
        script = runtime_script('KLS-D-TEST')
        death = re.search(r'^function KLS_Death takes[\s\S]*?^endfunction$', script, re.M).group()
        self.assertEqual(death.count('call KLS_BossReward()'), 1)
        self.assertNotRegex(death, r'if KLS_Wave == 40 then\s+call KLS_End\(true\)')
        self.assertIn('if dead == KLS_King then\n        call KLS_End(false)', death)
        self.assertIn('if not KLS_Ended and KLS_Alive == 0 then', death)
        self.assertIn('if IsUnitInGroup(dead,KLS_StoryEnemies) then', death)
        self.assertNotIn('KLS_StoryEnemies', death[death.index('elseif IsUnitInGroup(dead, KLS_Enemies)'):])
        hud = re.search(r'^function KLS_HUDUpdate takes[\s\S]*?^endfunction$', script, re.M).group()
        self.assertIn('King defeated at wave ', hud)
        self.assertIn('Endless', hud)
        self.assertIn('I2S(KLS_Wave)', hud)

    def test_roster_catalog_is_generated_from_the_same_fifty_source_rows(self):
        renderer = getattr(wave_rosters, 'roster_catalog_markdown', None)
        self.assertIsNotNone(renderer, 'wave roster catalog needs a deterministic generator')
        catalog = (ROOT / 'docs/WAVE-ROSTER-CATALOG.md').read_text()
        self.assertEqual(catalog, renderer())


if __name__ == '__main__':
    unittest.main()
