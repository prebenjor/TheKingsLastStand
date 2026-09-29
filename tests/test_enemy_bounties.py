"""Enemy combat gold is tiered by the installed wave-roster unit identity."""
import sys
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'tools'))

from pipeline import misc_data, runtime_script
from wave_rosters import BOSS_UNIT_CODES, BOUNTY_BY_UNIT, all_wave_rosters, bounty_script


def function_body(script, name):
    match = re.search(r'^function ' + re.escape(name) + r' takes [\s\S]*?^endfunction$', script, re.M)
    if not match:
        raise AssertionError('Missing runtime function ' + name)
    return match.group()


def generated_drop_rarity(script, loot_tier, roll):
    body = function_body(script, 'KLS_EnemyDropRarity')
    branches = re.findall(
        r'if tier == (\d+) then([\s\S]*?)(?=\n    elseif tier == \d+ then|\n    endif)',
        body,
    )
    branch = next((text for tier, text in branches if int(tier) == loot_tier), None)
    if branch is None:
        return -1
    for bound, rarity in re.findall(r'(?:if|elseif) roll <= (\d+) then\s+return (-?\d+)', branch):
        if roll <= int(bound):
            return int(rarity)
    return -1


class EnemyBounties(unittest.TestCase):
    def test_every_roster_unit_has_an_explicit_role_bounty(self):
        roster_units = {unit for roster in all_wave_rosters() for unit in roster}
        self.assertTrue(roster_units.issubset(BOUNTY_BY_UNIT))
        self.assertEqual(roster_units, set(BOUNTY_BY_UNIT))

        expected = {
            'uske': 5,       # basic skeleton
            'ugho': 8,       # ghoul
            'ucry': 12,      # crypt fiend
            'nfel': 18,      # fel stalker
            'unec': 22,      # necromancer
            'nfgu': 24,      # felguard
            'uabo': 32,      # abomination
            'umtw': 36,      # meat wagon
            'ninf': 45,      # infernal
        }
        for unit, bounty in expected.items():
            self.assertEqual(BOUNTY_BY_UNIT[unit], bounty, unit)
        tiers = ('uske', 'ugho', 'ucry', 'nfel', 'unec', 'nfgu', 'uabo', 'umtw', 'nbal', 'ninf')
        self.assertEqual(sorted(BOUNTY_BY_UNIT[unit] for unit in tiers),
                         [BOUNTY_BY_UNIT[unit] for unit in tiers])

    def test_generated_runtime_awards_role_bounty_plus_wave_scaling_once_on_tracked_death(self):
        script = runtime_script('KLS-D-TEST')
        self.assertIn(bounty_script(), script)
        bounty = function_body(script, 'KLS_EnemyBounty')
        self.assertIn("if unitCode == 'ninf' then\n        return 45 + KLS_Wave", bounty)
        self.assertIn("if unitCode == 'umtw' then\n        return 36 + KLS_Wave", bounty)
        self.assertIn("if unitCode == 'uske' then\n        return 5 + KLS_Wave", bounty)
        death = function_body(script, 'KLS_Death')
        self.assertIn('call KLS_AwardBounty(GetKillingUnit(),KLS_EnemyBounty(dead))', death)

    def test_personal_player_gold_and_king_quarter_bounty_have_separate_routes(self):
        script = runtime_script('KLS-D-TEST')
        award = function_body(script, 'KLS_AwardBounty')
        self.assertIn('if killer == KLS_King then', award)
        self.assertIn('R2I(I2R(bounty)*0.25)', award)
        self.assertIn('GetPlayerId(GetOwningPlayer(killer))', award)
        self.assertIn('call KLS_GoldToast(p,bounty)', award)
        self.assertNotIn('activeCount', award)
        self.assertNotIn('share = bounty /', award)

    def test_each_nearby_active_hero_receives_full_kill_xp_without_native_splitting(self):
        script = runtime_script('KLS-D-TEST')
        init = function_body(script, 'KLS_Init')
        leave = function_body(script, 'KLS_PlayerLeft')
        death = function_body(script, 'KLS_Death')
        award = function_body(script, 'KLS_AwardKillXP')
        self.assertIn('call KLS_AwardKillXP(dead)', death)
        self.assertIn('call AddHeroXP(hero,xp,false)', award)
        self.assertIn('dx*dx+dy*dy <= I2R(KLS_XPShareRange*KLS_XPShareRange)', award)
        self.assertIn('if KLS_Active[i] and hero != null then', award)
        self.assertNotIn('GetWidgetLife', award)
        self.assertNotIn('IsUnitType(KLS_Hero', award)
        self.assertIn('SetPlayerAlliance(Player(i),Player(j),ALLIANCE_SHARED_XP,false)', init)
        self.assertIn('ALLIANCE_SHARED_XP,false', leave)
        self.assertIn('SetUnitAcquireRange(KLS_King, 900)', init)
        self.assertIn(b'HeroExpRange=0\n', misc_data())
        self.assertIn(b'GrantNormalXP=0\n', misc_data())
        self.assertIn(b'GrantHeroXP=0,0,0,0,0,0,0,0,0,0\n', misc_data())

    def test_custom_kill_xp_preserves_warcraft_unit_and_hero_award_values(self):
        script = runtime_script('KLS-D-TEST')
        xp = function_body(script, 'KLS_UnitKillXP')
        self.assertIn('if IsUnitType(dead,UNIT_TYPE_HERO) then', xp)
        self.assertIn('return 100', xp)
        self.assertIn('return 800', xp)
        self.assertIn('set xp = xp + 5*level + 5', xp)
        self.assertIn('integer KLS_XPShareRange = 1200', script)

    def test_bosses_and_boss_summons_use_strength_based_bounty(self):
        script = runtime_script('KLS-D-TEST')
        bounty = function_body(script, 'KLS_EnemyBounty')
        boss_condition = ' or '.join("unitCode == '" + code + "'" for code in BOSS_UNIT_CODES)
        self.assertIn('if ' + boss_condition + ' then\n        return 100 + KLS_Wave * 5', bounty)
        self.assertIn("if unitCode == 'nfgu' then\n        return 24 + KLS_Wave", bounty)
        self.assertIn("if unitCode == 'uske' then\n        return 5 + KLS_Wave", bounty)

    def test_failed_random_item_drops_are_logged_with_item_enemy_and_position(self):
        script = runtime_script('KLS-D-TEST')
        delivery = function_body(script, 'KLS_DropEnemyItem')
        self.assertIn('CreateItem(itemCode,GetUnitX(enemy)+offsetX,GetUnitY(enemy))', delivery)
        self.assertIn('GetItemName(drop)+" dropped nearby."', delivery)
        self.assertIn('ERROR enemy item drop creation failed', delivery)
        self.assertIn('enemy="+GetObjectName(GetUnitTypeId(enemy))', delivery)
        self.assertIn('enemyXY="+R2S(GetUnitX(enemy))+","+R2S(GetUnitY(enemy))', delivery)
        self.assertIn('killerPlayerId="+I2S(p)', delivery)

    def test_enemy_loot_uses_explicit_elite_tiers_and_preserves_probability_bands(self):
        script = runtime_script('KLS-D-TEST')
        tier_body = function_body(script, 'KLS_EnemyLootTier')
        expected_elites = {
            'hbew', 'nbal', 'nbee', 'nbel', 'nchg', 'nchr', 'nchw', 'nckb',
            'ndqn', 'nfel', 'nfgu', 'nhyc', 'ninf', 'nmyr', 'nnmg', 'nnrg',
            'nnsw', 'nvdw', 'nwgs', 'uabo', 'ucry', 'umtw', 'unec',
        }
        self.assertIn('if boss then\n        return 2', tier_body)
        for unit_code in BOUNTY_BY_UNIT:
            expected_tier = 1 if unit_code in expected_elites else 0
            self.assertRegex(
                tier_body,
                rf"unitCode == '{unit_code}' then\s+return {expected_tier}",
                unit_code,
            )

        # Check generated JASS outcomes at every rarity boundary.
        expected_rolls = (
            (0, 160, 0), (0, 161, 1), (0, 250, 1), (0, 251, 2),
            (0, 290, 2), (0, 291, 3), (0, 298, 3), (0, 299, 4),
            (0, 300, 4), (0, 301, -1),
            (1, 350, 0), (1, 351, 1), (1, 650, 1), (1, 651, 2),
            (1, 850, 2), (1, 851, 3), (1, 950, 3), (1, 951, 4),
            (1, 1000, 4), (1, 1001, -1),
            (2, 1500, 0), (2, 1501, 1), (2, 2800, 1), (2, 2801, 2),
            (2, 4100, 2), (2, 4101, 3), (2, 4800, 3), (2, 4801, 4),
            (2, 5000, 4), (2, 5001, -1),
        )
        for tier, roll, expected_rarity in expected_rolls:
            self.assertEqual(generated_drop_rarity(script, tier, roll), expected_rarity,
                             (tier, roll))

    def test_equipment_and_potion_rolls_can_deliver_two_personal_drops(self):
        script = runtime_script('KLS-D-TEST')
        drops = function_body(script, 'KLS_EnemyDrop')
        self.assertIn('set rarity = KLS_EnemyDropRarity(tier,roll)', drops)
        self.assertIn('if potionRoll <= KLS_EnemyPotionThreshold(tier) then', drops)
        self.assertIn('call KLS_DropEnemyItem(enemy,gearCode,p,0.0)', drops)
        self.assertIn('call KLS_DropEnemyItem(enemy,potionCode,p,48.0)', drops)
        self.assertIn('local integer potionRoll = GetRandomInt(1,1000)', drops)

        potion = function_body(script, 'KLS_EnemyPotionThreshold')
        self.assertIn('if tier == 2 then\n        return 180', potion)
        self.assertIn('elseif tier == 1 then\n        return 80', potion)
        self.assertIn('return 40', potion)

        delivery = function_body(script, 'KLS_DropEnemyItem')
        self.assertIn('call SetItemPlayer(drop,Player(p),false)', delivery)
        self.assertIn('call SetItemUserData(drop,p+1)', delivery)
        self.assertIn('CreateItem(itemCode,GetUnitX(enemy)+offsetX,GetUnitY(enemy))', delivery)
        self.assertIn('enemy item drop creation failed', delivery)

        pickup = function_body(script, 'KLS_BindPickup')
        self.assertIn('elseif owner == 0 and LoadInteger(KLS_GearData,GetItemTypeId(gear),0) > 0 then', pickup)
        self.assertIn('set owner = GetPlayerId(GetOwningPlayer(u))+1', pickup)
        self.assertIn('call SetItemUserData(gear,owner)', pickup)


if __name__ == '__main__':
    unittest.main()
