import re
import struct
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'tools'))
sys.path.insert(0, str(ROOT / 'tests'))
from pipeline import runtime_script
from equipment_catalog import item_catalog,catalog_script
from objects import items, units
from test_equipment import decode


def function_body(script, name):
    match = re.search(r'^function ' + re.escape(name) + r' takes [\s\S]*?^endfunction$', script, re.M)
    if not match:
        raise AssertionError('Missing generated function ' + name)
    return match.group()


def custom_unit_fields(data, target):
    offset = 0

    def uint():
        nonlocal offset
        value = struct.unpack_from('<I', data, offset)[0]
        offset += 4
        return value

    if uint() != 2:
        raise AssertionError('Unexpected unit object format')
    result = None
    for section in range(2):
        for _ in range(uint()):
            base = data[offset:offset + 4]
            custom = data[offset + 4:offset + 8]
            offset += 8
            fields = {}
            for _ in range(uint()):
                field = data[offset:offset + 4].decode()
                offset += 4
                kind = uint()
                if kind == 3:
                    end = data.index(b'\0', offset)
                    value = data[offset:end].decode()
                    offset = end + 1
                else:
                    value = struct.unpack_from('<i', data, offset)[0]
                    offset += 4
                offset += 4  # Object ID attached to this field.
                fields[field] = value
            if section == 1 and custom.decode() == target:
                result = fields
    if result is None:
        raise AssertionError('Missing custom unit ' + target)
    return result


class NativeMarketControls(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.script = runtime_script('KLS-D-TEST')

    def test_gear_purchase_waits_for_shop_transfer_before_native_equip(self):
        market = function_body(self.script, 'KLS_MarketBuy')
        equip = function_body(self.script, 'KLS_MarketEquipPurchased')
        self.assertNotIn('UnitEquipItem(buyer,gear)', market)
        self.assertRegex(market, r'TimerStart\([^,]+,0\.25,false,function KLS_MarketEquipPurchased\)')
        self.assertIn('UnitEquipItem(buyer,gear)', equip)
        self.assertIn('KLS_MovePurchaseToRegularInventory(buyer,gear)', equip)
        self.assertIn('LoadInteger(KLS_GearData,key,22)', equip)
        self.assertIn('TimerStart(equipTimer,0.25,false,function KLS_MarketEquipPurchased)', equip)
        self.assertIn('KLS_Log("ERROR native equip rejected shop item after transfer:', equip)
        self.assertIn('equipment slot id="+I2S(LoadInteger(KLS_GearData,rawcode,2))', equip)
        self.assertIn('SetItemUserData(gear,p+1)', market)

    def test_purchase_fallback_places_a_backpack_item_in_a_real_free_inventory_slot(self):
        move = function_body(self.script, 'KLS_MovePurchaseToRegularInventory')
        self.assertIn('UnitItemInSlot(buyer,slot)', move)
        self.assertIn('UnitAddItemToSlotById(buyer,rawcode,emptySlot)', move)
        self.assertIn('SetItemUserData(moved,GetItemUserData(gear))', move)
        self.assertIn('SetItemCharges(moved,GetItemCharges(gear))', move)
        self.assertIn('RemoveItem(gear)', move)

    def test_native_successful_pawn_is_logged_and_confirmed_to_the_player(self):
        pawn = function_body(self.script, 'KLS_GearPawned')
        init = function_body(self.script, 'KLS_GearInit')
        self.assertIn('GetManipulatedItem()', pawn)
        self.assertNotIn('GetSoldItem()', pawn)
        self.assertIn('Native pawn event: item=', pawn)
        self.assertIn('Sold "+GetItemName(gear)+" back to the market.', pawn)
        self.assertIn('EVENT_PLAYER_UNIT_PAWN_ITEM', init)

    def test_catalog_registers_the_real_equipment_slot_for_diagnostics(self):
        generated=catalog_script()
        for entry in item_catalog():
            with self.subTest(item=entry['rawcode']):
                self.assertIn(f"SaveInteger(KLS_GearData, '{entry['rawcode']}', 2, {entry['slot']})",generated)

    def test_each_castle_upgrade_button_has_exact_native_cost_and_next_tier_stock(self):
        records = decode(items())
        for tier in range(5):
            rawcode = 'KUP' + str(tier + 1)
            fields = records[rawcode][1]
            self.assertEqual(fields[('igol', 0)][0], 400 + 200 * tier)
            self.assertEqual(fields[('ilum', 0)][0], 150)
            self.assertIn('Tier ' + str(tier + 1) + ' costs ' + str(400 + 200 * tier) + ' gold', fields[('utub', 0)][0])

        market = function_body(self.script, 'KLS_MarketBuy')
        self.assertNotIn("'KUP'+I2S", market)
        self.assertIn("AddItemToStock(shop,'KUP2',1,1)", market)
        self.assertIn("AddItemToStock(shop,'KUP3',1,1)", market)
        self.assertIn("AddItemToStock(shop,'KUP4',1,1)", market)
        self.assertIn("AddItemToStock(shop,'KUP5',1,1)", market)
        self.assertNotIn('DialogAddButton', function_body(self.script, 'KLS_CastleInit'))

    def test_gear_merchants_are_native_icon_stock_not_text_dialogs(self):
        shops = function_body(self.script, 'KLS_CreateShops')
        self.assertNotIn('DialogAddButton', shops)
        self.assertIn('KLS_StockCatalog()', shops)
        self.assertIn('KLS_Log("Sixteen gear families stocked', shops)

    def test_neutral_market_and_castle_retain_select_hero_shop_ability(self):
        for rawcode in ('hS00', 'hC01'):
            with self.subTest(shop=rawcode):
                abilities = set(custom_unit_fields(units(), rawcode)['uabi'].split(','))
                self.assertTrue({'Aneu', 'Apit', 'Asid'} <= abilities, abilities)


if __name__ == '__main__':
    unittest.main()

