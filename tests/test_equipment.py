"""Decode emitted object records independently and validate against installed data."""
import re
import struct
import sys
import unittest
from collections import Counter
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'tools'))
from equipment_catalog import abilities,item_catalog,catalog_script
from objects import items
from recipes import recipe_catalog,recipe_script

def decode(blob,extended=False):
    pos=0
    def uint():
        nonlocal pos
        value=struct.unpack_from('<I',blob,pos)[0];pos+=4
        return value
    assert uint()==2
    result={}
    for section in range(2):
        for _ in range(uint()):
            base=blob[pos:pos+4].decode();custom=blob[pos+4:pos+8].decode();pos+=8
            fields={}
            for _ in range(uint()):
                field=blob[pos:pos+4].decode();pos+=4
                typ=uint();level=uint() if extended else 0;pointer=uint() if extended else 0
                if typ==3:
                    end=blob.index(0,pos);value=blob[pos:end].decode();pos=end+1
                else:
                    value=struct.unpack_from('<f' if typ in (1,2) else '<i',blob,pos)[0];pos+=4
                marker=blob[pos:pos+4].decode();pos+=4
                assert marker in (base,custom,'\0'*4)
                fields[(field,level)]=(value,typ,pointer)
            result[custom if section else base]=(base,fields)
    assert pos==len(blob)
    return result

def slk(name):
    rows={};y=0
    for line in (ROOT/'tools/reference/installed'/name).read_text().splitlines():
        if not line.startswith('C;'):continue
        match=re.search(r';Y(\d+)',line)
        if match:y=int(match[1])
        x=re.search(r';X(\d+)',line);value=re.search(r';K(.*)',line)
        if x and value:rows.setdefault(y,{})[int(x[1])]=value[1].strip('"')
    return {row[1]:row for row in rows.values() if 1 in row}

class EquipmentRecords(unittest.TestCase):
    def test_backpack_preserves_native_identity_and_usable_flags(self):
        base,fields=decode(items())['ebac']
        self.assertEqual(base,'ebac')
        self.assertEqual(fields[('iusa',0)][0],1)
        self.assertEqual(fields[('iabi',0)][0],'AIni,AEqu,ASde')
        for field in ('idro','ipaw','isel','iper','iuse'):
            self.assertEqual(fields[(field,0)][0],0)
        installed_pack=slk('ItemData.slk')['ebac']
        self.assertEqual(installed_pack[3],'EquipmentBackpack')
        self.assertEqual(installed_pack[13],'1')
        heroes=(ROOT/'source/heroes.j').read_text()
        self.assertIn("UnitAddItemById(KLS_Hero[p], 'ebac')",heroes)
        self.assertNotIn("UnitAddItemById(KLS_Hero[p], 'Ibpk')",heroes)

    def test_every_emitted_ability_has_an_installed_parent_and_valid_fields(self):
        installed=slk('AbilityData.slk');metadata=slk('AbilityMetaData.slk')
        for custom,(base,fields) in decode(abilities(),True).items():
            self.assertIn(base,installed,custom)
            if custom!=base:self.assertNotIn(custom,installed,'Custom ability shadows installed data')
            for (field,level),(value,typ,pointer) in fields.items():
                self.assertIn(field,metadata)
                meta=metadata[field]
                if meta[10]=='unreal':self.assertEqual(typ,2,field)
                if meta.get(2)=='Data':self.assertEqual(pointer,int(meta[6]))

    def test_equipment_stats_are_serialized_not_merely_advertised(self):
        records=decode(abilities(),True);gear=decode(items())
        fields={'damage':'Iatt','health':'Ilif','mana':'Iman','armor':'Idef','strength':'Istr','agility':'Iagi','intelligence':'Iint','attack speed':'Isx1','movement speed':'Imvb'}
        for entry in item_catalog():
            object_fields=gear[entry['rawcode']][1]
            self.assertEqual(object_fields[('igol',0)][0],entry['price'])
            for ability,(stat,amount) in zip(object_fields[('iabi',0)][0].split(','),entry['stats'].items()):
                actual=records[ability][1][(fields[stat],1)][0]
                self.assertAlmostEqual(actual,amount/100 if stat=='attack speed' else amount,places=5)
        legendary_blade=next(e for e in item_catalog() if e['family']=='Blade' and e['tier']==4)
        self.assertEqual(legendary_blade['stats']['damage'],66)
        self.assertEqual(legendary_blade['price'],30000)

    def test_custom_equipment_inherits_the_installed_equipment_slot(self):
        gear=decode(items())
        installed=slk('ItemData.slk')
        metadata=slk('UnitMetaData.slk')['iequ']
        self.assertEqual(metadata[3],'ItemData')
        self.assertEqual(metadata[8],'equipmentType')
        self.assertEqual(metadata[20],'1')
        slot_names={1:'Head',2:'Chest',3:'Gloves',4:'Boots',5:'Ring',6:'Primary',7:'Offhand',8:'Trinket'}
        for entry in item_catalog():
            with self.subTest(item=entry['rawcode']):
                self.assertEqual(installed[entry['parent']][32],slot_names[entry['slot']])
                self.assertNotIn(('iequ',0),gear[entry['rawcode']][1])
                self.assertNotIn(('iico',0),gear[entry['rawcode']][1])

    def test_native_icon_shops_expose_all_catalog_items_by_tier_and_category(self):
        catalog=item_catalog();script=catalog_script()
        self.assertEqual(len(catalog),103)
        for item in catalog:
            tier=item['tier'];cat=0 if item['family_index']<7 else 1
            stock=f"AddItemToStock(KLS_Shops[{tier*2+cat}], '{item['rawcode']}', 1, 1)"
            if item.get('crafted') or item.get('race'):
                self.assertNotIn(stock,script)
            else:
                self.assertIn(stock,script)
            fields=decode(items())[item['rawcode']][1]
            self.assertEqual(fields[('utip',0)][0],item['colored_name'])
            self.assertIn('+' , fields[('utub',0)][0])
            self.assertEqual(fields[('igol',0)][0],item['price'])
        self.assertIn("KLS_Shops[10]",Path(ROOT/'source/shops.j').read_text())

    def test_race_relics_and_foundry_patterns_are_stocked_in_their_own_vendors(self):
        from town_catalog import town_script
        catalog=item_catalog()
        generic=catalog_script()
        towns=town_script()
        recipes=recipe_script()
        for item in catalog:
            if item.get('race'):
                tier=item['tier'];cat=0 if item['family_index']<7 else 1
                generic_stock=f"AddItemToStock(KLS_Shops[{tier*2+cat}], '{item['rawcode']}', 1, 1)"
                self.assertNotIn(generic_stock,generic)
        self.assertIn('exitwhen tier == 4',towns)
        for race_index in range(4):
            self.assertIn(f'KLS_TownShop[{race_index}],KLS_RaceItemId[{race_index}*5+tier]',towns)
        for recipe in recipe_catalog(catalog):
            if recipe['rawcode'] in {'RCP1', 'RCP2', 'RCP3'}:
                self.assertIn(f"AddItemToStock(KLS_Shops[12], '{recipe['rawcode']}', 1, 1)",recipes)
            else:
                self.assertNotIn(f"AddItemToStock(KLS_Shops[12], '{recipe['rawcode']}', 1, 1)",recipes)
        self.assertIn('SaveUnitHandle(KLS_GearData, key, 32, vendor)', recipes)
        self.assertIn('KLS_RecipeRestockVendor(vendor, itemCode)', recipes)
        self.assertIn('GetWidgetLife(vendor) > 0.405', recipes)
        self.assertIn('KLS_Shops[12] = KLS_CreateUnit',Path(ROOT/'source/shops.j').read_text())
        self.assertIn('AddItemToStock(shop, rawcode, 1, 1)',
                      Path(ROOT/'source/combat.j').read_text())
        self.assertIn('KLS_RecipeBegin(buyer, gear, shop)',Path(ROOT/'source/combat.j').read_text())

    def test_native_shop_stock_stays_within_twelve_command_card_slots(self):
        catalog=item_catalog()
        stock_by_shop=Counter()
        for shop,code in re.findall(r"AddItemToStock\(KLS_Shops\[(\d+)\], '([^']+)'",catalog_script()):
            stock_by_shop[int(shop)] += 1
        for shop,code in re.findall(r"AddItemToStock\(KLS_Shops\[(\d+)\], '([^']+)'",recipe_script()):
            stock_by_shop[int(shop)] += 1
        stock_by_shop[10] = 4
        stock_by_shop[11] = 9
        for race_index in range(4):
            stock_by_shop[20+race_index] = 4 + 2
        self.assertLessEqual(max(stock_by_shop.values()),12,
                             'Native shop stock exceeds the 12-slot command card: '+str(dict(stock_by_shop)))

