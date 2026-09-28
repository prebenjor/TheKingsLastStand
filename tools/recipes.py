"""Personal, atomic equipment crafting for the Master Forge."""

_RECIPES = (
    {
        'rawcode': 'RCP1',
        'name': 'Oathforged Kingswrath',
        'components_by_name': ('Gravebreaker', 'Ring of Conquest'),
        'output_name': 'Oathforged Kingswrath',
        'price': 5000,
        'description': 'Combine Rare Gravebreaker and Rare Ring of Conquest. Costs 5,000 gold. Ingredients are consumed only when the crafted weapon can be delivered.',
    },
    {
        'rawcode': 'RCP2',
        'name': 'Stormheart Prism',
        'components_by_name': ('Wintercall', 'Spellwell'),
        'output_name': 'Stormheart Prism',
        'price': 7000,
        'description': 'Combine Rare Wintercall and Rare Spellwell. Costs 7,000 gold. Ingredients are consumed only when the crafted focus can be delivered.',
    },
    {
        'rawcode': 'RCP3',
        'name': 'Sovereign’s Mantle',
        'components_by_name': ('Dawnguard Helm', 'Royal Bulwark'),
        'output_name': "Sovereign's Mantle",
        'price': 12000,
        'description': "Combine Epic Dawnguard Helm and Epic Royal Bulwark. Costs 12,000 gold. Ingredients are consumed only when the crafted cape can be delivered.",
    },
    {
        'rawcode': 'RCP4', 'name': 'Crownward Foundry Pattern',
        'components_by_name': ('Aldric’s Aegis','Lionroad Mantle'),
        'component_tiers': (2,1), 'output_name': 'Last King’s Oath', 'price': 9000,
        'description': 'Forge the Last King’s Oath from Aldric’s Aegis and Lionroad Mantle. Costs 9,000 gold; ingredients are consumed only after the personal output is delivered.',
    },
    {
        'rawcode': 'RCP5', 'name': 'Redtusk Foundry Pattern',
        'components_by_name': ('Stormscar Bracers','Ashen War Drum'),
        'component_tiers': (2,1), 'output_name': 'Worldrend Standard', 'price': 9000,
        'description': 'Forge the Worldrend Standard from Stormscar Bracers and Ashen War Drum. Costs 9,000 gold; ingredients are consumed only after the personal output is delivered.',
    },
    {
        'rawcode': 'RCP6', 'name': 'Moonbark Foundry Pattern',
        'components_by_name': ('Duskwatch Longbow','Starleaf Quiver'),
        'component_tiers': (2,1), 'output_name': 'Silvermoon Vigil', 'price': 9000,
        'description': 'Forge Silvermoon Vigil from the Duskwatch Longbow and Starleaf Quiver. Costs 9,000 gold; ingredients are consumed only after the personal output is delivered.',
    },
    {
        'rawcode': 'RCP7', 'name': 'Wraith Foundry Pattern',
        'components_by_name': ('Soulreaper’s Fang','Wraithsilk Cape'),
        'component_tiers': (2,1), 'output_name': 'Night’s Covenant', 'price': 9000,
        'description': 'Forge Night’s Covenant from Soulreaper’s Fang and Wraithsilk Cape. Costs 9,000 gold; ingredients are consumed only after the personal output is delivered.',
    },
)


def recipe_catalog(catalog):
    """Resolve recipe component and output rawcodes from the shared item catalog."""
    exact = {(entry['name'], entry['tier']): entry for entry in catalog}
    outputs = {entry['name']: entry for entry in catalog
               if entry.get('crafted') or entry.get('craft_output')}
    resolved = []
    for recipe in _RECIPES:
        default_tier = 3 if recipe['rawcode'] == 'RCP3' else 2
        tiers = recipe.get('component_tiers', (default_tier, default_tier))
        components = [exact[(name, tier)] for name, tier in zip(recipe['components_by_name'], tiers)]
        output = outputs[recipe['output_name']]
        resolved.append({
            'rawcode': recipe['rawcode'],
            'name': recipe['name'],
            'components': tuple(item['rawcode'] for item in components),
            'output': output['rawcode'],
            'output_slot': output['slot'],
            'price': recipe['price'],
            'description': recipe['description'],
        })
    return resolved


def plan_recipe_craft(recipe, hero_items, owner, gold, output_slot_available):
    """Plan one craft without mutating inputs; any failure leaves them untouched."""
    original = list(hero_items)
    if gold < recipe['price']:
        return {'success': False, 'gold': gold, 'remaining_items': original,
                'output': None, 'reason': 'insufficient gold'}
    if not output_slot_available:
        return {'success': False, 'gold': gold, 'remaining_items': original,
                'output': None, 'reason': 'no output space'}
    selected = []
    for component in recipe['components']:
        match = next((index for index, item in enumerate(original)
                      if index not in selected and item.get('id') == component
                      and item.get('owner') == owner), None)
        if match is None:
            return {'success': False, 'gold': gold, 'remaining_items': original,
                    'output': None, 'reason': 'missing or unowned component'}
        selected.append(match)
    remaining = [item for index, item in enumerate(original) if index not in selected]
    return {'success': True, 'gold': gold - recipe['price'],
            'remaining_items': remaining, 'output': recipe['output'], 'reason': ''}


def recipe_script():
    """Emit recipe lookup, shop stock and delayed all-or-nothing craft runtime."""
    from equipment_catalog import item_catalog

    recipes = recipe_catalog(item_catalog())
    lines = [
        'function KLS_IsRecipe takes integer itemCode returns boolean',
        '    return false',
    ]
    for recipe in recipes:
        lines[-1] += f" or itemCode == '{recipe['rawcode']}'"
    lines += [
        'endfunction',
        'function KLS_RecipeOutput takes integer itemCode returns integer',
        '    if false then',
        "        return 'I128'",
    ]
    for recipe in recipes:
        lines += [f"    elseif itemCode == '{recipe['rawcode']}' then",
                  f"        return '{recipe['output']}'"]
    lines += ['    endif', "    return 'I128'", 'endfunction',
              'function KLS_RecipeFirst takes integer itemCode returns integer',
              '    if false then', "        return 'I11A'"]
    for recipe in recipes:
        lines += [f"    elseif itemCode == '{recipe['rawcode']}' then",
                  f"        return '{recipe['components'][0]}'"]
    lines += ['    endif', "    return 'I11A'", 'endfunction',
              'function KLS_RecipeSecond takes integer itemCode returns integer',
              '    if false then', "        return 'I11A'"]
    for recipe in recipes:
        lines += [f"    elseif itemCode == '{recipe['rawcode']}' then",
                  f"        return '{recipe['components'][1]}'"]
    lines += ['    endif', "    return 'I11A'", 'endfunction',
              'function KLS_RecipePrice takes integer itemCode returns integer',
              '    if false then', '        return 0']
    for recipe in recipes:
        lines += [f"    elseif itemCode == '{recipe['rawcode']}' then",
                  f"        return {recipe['price']}"]
    lines += ['    endif', '    return 0', 'endfunction',
              'function KLS_StockRecipes takes nothing returns nothing']
    for recipe in recipes:
        lines.append(f"    call AddItemToStock(KLS_Shops[4], '{recipe['rawcode']}', 1, 1)")
    lines += ['endfunction',
              'function KLS_RecipeFindOwned takes unit hero, integer wanted, integer ownerMark returns item',
              '    local integer slot = 0',
              '    local item candidate',
              '    loop',
              '        exitwhen slot == 9',
              '        set candidate = UnitItemInEquipmentSlot(hero, ConvertLoadoutSlot(slot))',
              '        if candidate != null and GetItemTypeId(candidate) == wanted and GetItemUserData(candidate) == ownerMark then',
              '            return candidate',
              '        endif',
              '        set slot = slot + 1',
              '    endloop',
              '    set slot = 0',
              '    loop',
              '        exitwhen slot == 6',
              '        set candidate = UnitItemInSlot(hero, slot)',
              '        if candidate != null and GetItemTypeId(candidate) == wanted and GetItemUserData(candidate) == ownerMark then',
              '            return candidate',
              '        endif',
              '        set slot = slot + 1',
              '    endloop',
              '    set slot = 0',
              '    loop',
              '        exitwhen slot == 30',
              '        set candidate = UnitItemInBagSlot(hero, slot)',
              '        if candidate != null and GetItemTypeId(candidate) == wanted and GetItemUserData(candidate) == ownerMark then',
              '            return candidate',
              '        endif',
              '        set slot = slot + 1',
              '    endloop',
              '    return null',
              'endfunction',
              'function KLS_RecipeHasDeliverySpace takes unit hero, item scroll, item first, item second returns boolean',
              '    local integer slot = 0',
              '    local item candidate',
              '    loop',
              '        exitwhen slot == 6',
              '        set candidate = UnitItemInSlot(hero, slot)',
              '        if candidate == null or candidate == scroll or candidate == first or candidate == second then',
              '            return true',
              '        endif',
              '        set slot = slot + 1',
              '    endloop',
              '    set slot = 0',
              '    loop',
              '        exitwhen slot == 30',
              '        set candidate = UnitItemInBagSlot(hero, slot)',
              '        if candidate == null or candidate == scroll or candidate == first or candidate == second then',
              '            return true',
              '        endif',
              '        set slot = slot + 1',
              '    endloop',
              '    return false',
              'endfunction',
              'function KLS_RecipeRestoreIngredients takes unit buyer, item first, item second returns nothing',
              '    call UnitAddItem(buyer, first)',
              '    call UnitAddItem(buyer, second)',
              '    if GetItemTypeId(first) != 0 then',
              '        call UnitEquipItem(buyer, first)',
              '    endif',
              '    if GetItemTypeId(second) != 0 then',
              '        call UnitEquipItem(buyer, second)',
              '    endif',
              'endfunction',
              'function KLS_RecipeRefund takes unit buyer, item scroll returns nothing',
              '    local integer itemCode = GetItemTypeId(scroll)',
              '    local integer p = GetPlayerId(GetOwningPlayer(buyer))',
              '    if p >= 0 and p < 4 then',
              '        call SetPlayerState(Player(p), PLAYER_STATE_RESOURCE_GOLD, GetPlayerState(Player(p), PLAYER_STATE_RESOURCE_GOLD) + KLS_RecipePrice(itemCode))',
              '    endif',
              '    call RemoveItem(scroll)',
              "    call AddItemToStock(KLS_Shops[4], itemCode, 1, 1)",
              '    call KLS_Log("No components consumed; recipe fee refunded")',
              '    if p >= 0 and p < 4 then',
              '        call DisplayTimedTextToPlayer(Player(p), 0, 0, 8, "Craft failed. Your components remain yours and the recipe fee was refunded.")',
              '    endif',
              'endfunction',
              'function KLS_RecipeComplete takes nothing returns nothing',
              '    local timer craftTimer = GetExpiredTimer()',
              '    local integer key = GetHandleId(craftTimer)',
              '    local unit buyer = LoadUnitHandle(KLS_GearData, key, 30)',
              '    local item scroll = LoadItemHandle(KLS_GearData, key, 31)',
              '    local integer itemCode = GetItemTypeId(scroll)',
              '    local integer p = GetItemUserData(scroll) - 1',
              '    local item first = null',
              '    local item second = null',
              '    local item output = null',
              '    if not KLS_Ended and p >= 0 and p < 4 and KLS_Active[p] and buyer == KLS_Hero[p] and GetWidgetLife(buyer) > 0.405 then',
              '        set first = KLS_RecipeFindOwned(buyer, KLS_RecipeFirst(itemCode), p + 1)',
              '        set second = KLS_RecipeFindOwned(buyer, KLS_RecipeSecond(itemCode), p + 1)',
              '        if first != null and second != null and first != second and KLS_RecipeHasDeliverySpace(buyer, scroll, first, second) then',
              '            call UnitRemoveItem(buyer, scroll)',
              '            call UnitRemoveItem(buyer, first)',
              '            call UnitRemoveItem(buyer, second)',
              '            set output = CreateItem(KLS_RecipeOutput(itemCode), GetUnitX(buyer), GetUnitY(buyer))',
              '            if output == null then',
              '                call KLS_RecipeRestoreIngredients(buyer, first, second)',
              '                call KLS_RecipeRefund(buyer, scroll)',
              '            else',
              '                call SetItemPlayer(output, Player(p), false)',
              '                call SetItemUserData(output, p + 1)',
              '                if UnitAddItem(buyer, output) then',
              '                    call RemoveItem(first)',
              '                    call RemoveItem(second)',
              '                    call RemoveItem(scroll)',
              '                    call AddItemToStock(KLS_Shops[4], itemCode, 1, 1)',
              '                    if LoadInteger(KLS_GearData, GetItemTypeId(output), 0) > 0 then',
              '                        call UnitEquipItem(buyer, output)',
              '                    endif',
              '                    call DisplayTimedTextToPlayer(Player(p), 0, 0, 10, "Craft complete: " + GetItemName(output) + ". Your new item is personal.")',
              '                    call KLS_Log("Recipe completed: " + GetItemName(output) + " owner=p" + I2S(p + 1))',
              '                else',
              '                    call RemoveItem(output)',
              '                    call KLS_RecipeRestoreIngredients(buyer, first, second)',
              '                    call KLS_RecipeRefund(buyer, scroll)',
              '                endif',
              '            endif',
              '        else',
              '            call KLS_RecipeRefund(buyer, scroll)',
              '        endif',
              '    else',
              '        call KLS_RecipeRefund(buyer, scroll)',
              '    endif',
              '    call FlushChildHashtable(KLS_GearData, key)',
              '    call PauseTimer(craftTimer)',
              '    call DestroyTimer(craftTimer)',
              '    set craftTimer = null',
              '    set buyer = null',
              '    set scroll = null',
              '    set first = null',
              '    set second = null',
              '    set output = null',
              'endfunction',
              'function KLS_RecipeBegin takes unit buyer, item scroll returns nothing',
              '    local integer p = GetPlayerId(GetOwningPlayer(buyer))',
              '    local timer craftTimer = CreateTimer()',
              '    local integer key = GetHandleId(craftTimer)',
              '    call SetItemUserData(scroll, p + 1)',
              '    call SaveUnitHandle(KLS_GearData, key, 30, buyer)',
              '    call SaveItemHandle(KLS_GearData, key, 31, scroll)',
              '    call TimerStart(craftTimer, 0.05, false, function KLS_RecipeComplete)',
              '    set craftTimer = null',
              'endfunction']
    return '\n'.join(lines)
