globals
    unit KLS_Boss = null
    integer KLS_BossCast = 0
    integer KLS_BossMechanic = 0
    integer KLS_TowerSuppression = 0
    boolean KLS_BossPauseState = false
    real KLS_BossX = 0
    real KLS_BossY = 0
    integer array KLS_TalentPoints
    integer array KLS_LastTalentMilestone
    integer array KLS_TalentStrengthRank
    integer array KLS_TalentAgilityRank
    integer array KLS_TalentIntelligenceRank
    integer array KLS_LastAutomaticStatLevel
    dialog array KLS_ProgressionDialog
    button array KLS_TalentStrengthButton
    button array KLS_TalentAgilityButton
    button array KLS_TalentIntelligenceButton
    framehandle array KLS_StatChoiceStrengthButton
    framehandle array KLS_StatChoiceAgilityButton
    framehandle array KLS_StatChoiceIntelligenceButton
    timer KLS_StatChoiceRefreshTimer = null
    boolean KLS_Debug = true
endglobals

function KLS_StatChoiceRefresh takes nothing returns nothing
    local integer p = GetPlayerId(GetLocalPlayer())
    local unit hero
    local boolean showChoices = false
    if p >= 0 and p < 4 and KLS_Active[p] then
        set hero = KLS_Hero[p]
        if hero != null then
            set showChoices = IsUnitSelected(hero,Player(p)) and GetHeroSkillPoints(hero) > 0
        endif
        if GetLocalPlayer() == Player(p) then
            if KLS_StatChoiceStrengthButton[p] != null then
                call BlzFrameSetVisible(KLS_StatChoiceStrengthButton[p],showChoices)
                call BlzFrameSetVisible(KLS_StatChoiceAgilityButton[p],showChoices)
                call BlzFrameSetVisible(KLS_StatChoiceIntelligenceButton[p],showChoices)
            endif
        endif
    endif
    set hero = null
endfunction

function KLS_StatChoiceApplySync takes nothing returns nothing
    local integer p = GetPlayerId(GetTriggerPlayer())
    local integer choice = S2I(BlzGetTriggerSyncData())
    local integer heroStat = -1
    local unit hero
    if choice == 0 then
        set heroStat = bj_HEROSTAT_STR
    elseif choice == 1 then
        set heroStat = bj_HEROSTAT_AGI
    elseif choice == 2 then
        set heroStat = bj_HEROSTAT_INT
    else
        return
    endif
    if p < 0 or p >= 4 or not KLS_Active[p] then
        return
    endif
    set hero = KLS_Hero[p]
    if hero != null and GetOwningPlayer(hero) == Player(p) and GetHeroSkillPoints(hero) > 0 then
        if UnitModifySkillPoints(hero,-1) then
            call ModifyHeroStat(heroStat,hero,bj_MODIFYMETHOD_ADD,3)
            if choice == 0 then
                call DisplayTimedTextToPlayer(Player(p),0,0,5,"+3 Strength selected.")
            elseif choice == 1 then
                call DisplayTimedTextToPlayer(Player(p),0,0,5,"+3 Agility selected.")
            else
                call DisplayTimedTextToPlayer(Player(p),0,0,5,"+3 Intelligence selected.")
            endif
        endif
    endif
    call KLS_StatChoiceRefresh()
    set hero = null
endfunction

function KLS_StatChoiceClick takes nothing returns nothing
    local integer p = GetPlayerId(GetLocalPlayer())
    local framehandle clicked = BlzGetTriggerFrame()
    if p < 0 or p >= 4 then
        return
    endif
    if clicked == KLS_StatChoiceStrengthButton[p] then
        call BlzSendSyncData("KLSSTAT","0")
    elseif clicked == KLS_StatChoiceAgilityButton[p] then
        call BlzSendSyncData("KLSSTAT","1")
    elseif clicked == KLS_StatChoiceIntelligenceButton[p] then
        call BlzSendSyncData("KLSSTAT","2")
    endif
    set clicked = null
endfunction

function KLS_StatChoiceCreateButton takes string name, string label, framehandle parent, framehandle relative, framepointtype relativePoint, real x, real y returns framehandle
    local framehandle choice = BlzCreateFrameByType("GLUETEXTBUTTON",name,parent,"ScriptDialogButton",0)
    call BlzFrameSetSize(choice,0.052,0.026)
    call BlzFrameSetText(choice,label)
    call BlzFrameSetPoint(choice,FRAMEPOINT_BOTTOMLEFT,relative,relativePoint,x,y)
    call BlzFrameSetVisible(choice,false)
    set relative = null
    set parent = null
    return choice
endfunction

function KLS_ProgressionShow takes integer p returns nothing
    if p < 0 or p >= 4 or not KLS_Active[p] or KLS_ProgressionDialog[p] == null then
        return
    endif
    if KLS_TalentPoints[p] <= 0 then
        return
    endif
    call DialogClear(KLS_ProgressionDialog[p])
    call DialogSetMessage(KLS_ProgressionDialog[p],"Talent earned! Every 5 hero levels, choose one specialty.")
    set KLS_TalentStrengthButton[p] = DialogAddButton(KLS_ProgressionDialog[p],"Vanguard: Strength, health and regeneration",0)
    set KLS_TalentAgilityButton[p] = DialogAddButton(KLS_ProgressionDialog[p],"Skirmisher: Agility, attack speed and evasion",0)
    set KLS_TalentIntelligenceButton[p] = DialogAddButton(KLS_ProgressionDialog[p],"Sage: Intelligence, mana and regeneration",0)
    call DialogDisplay(Player(p),KLS_ProgressionDialog[p],true)
endfunction

function KLS_TalentApply takes integer p, integer stat returns nothing
    local unit hero
    local integer maximum
    local real current
    if p < 0 or p >= 4 or KLS_Hero[p] == null then
        return
    endif
    set hero = KLS_Hero[p]
    if stat == 0 then
        set KLS_TalentStrengthRank[p] = KLS_TalentStrengthRank[p]+1
        call ModifyHeroStat(bj_HEROSTAT_STR,hero,bj_MODIFYMETHOD_ADD,5)
        set maximum = BlzGetUnitMaxHP(hero)
        call BlzSetUnitMaxHP(hero,maximum+200)
        call SetWidgetLife(hero,GetWidgetLife(hero)+200.0)
        set current = BlzGetUnitRealField(hero,UNIT_RF_HIT_POINTS_REGENERATION_RATE)
        call BlzSetUnitRealField(hero,UNIT_RF_HIT_POINTS_REGENERATION_RATE,current+2.0)
    elseif stat == 1 then
        set KLS_TalentAgilityRank[p] = KLS_TalentAgilityRank[p]+1
        call ModifyHeroStat(bj_HEROSTAT_AGI,hero,bj_MODIFYMETHOD_ADD,5)
    else
        set KLS_TalentIntelligenceRank[p] = KLS_TalentIntelligenceRank[p]+1
        call ModifyHeroStat(bj_HEROSTAT_INT,hero,bj_MODIFYMETHOD_ADD,5)
        set maximum = R2I(GetUnitState(hero,UNIT_STATE_MAX_MANA))
        call BlzSetUnitMaxMana(hero,maximum+100)
        call SetUnitState(hero,UNIT_STATE_MANA,GetUnitState(hero,UNIT_STATE_MANA)+100.0)
        set current = BlzGetUnitRealField(hero,UNIT_RF_MANA_REGENERATION)
        call BlzSetUnitRealField(hero,UNIT_RF_MANA_REGENERATION,current+2.0)
    endif
    call DisplayTimedTextToPlayer(Player(p),0,0,6,"Talent chosen. Its attribute and secondary bonuses are now active.")
    set hero = null
endfunction

function KLS_ProgressionClick takes nothing returns nothing
    local integer p = GetPlayerId(GetTriggerPlayer())
    local button clicked = GetClickedButton()
    local unit hero
    if p < 0 or p >= 4 or KLS_Hero[p] == null then
        return
    endif
    set hero = KLS_Hero[p]
    if clicked == KLS_TalentStrengthButton[p] and KLS_TalentPoints[p] > 0 then
        set KLS_TalentPoints[p] = KLS_TalentPoints[p]-1
        call KLS_TalentApply(p,0)
    elseif clicked == KLS_TalentAgilityButton[p] and KLS_TalentPoints[p] > 0 then
        set KLS_TalentPoints[p] = KLS_TalentPoints[p]-1
        call KLS_TalentApply(p,1)
    elseif clicked == KLS_TalentIntelligenceButton[p] and KLS_TalentPoints[p] > 0 then
        set KLS_TalentPoints[p] = KLS_TalentPoints[p]-1
        call KLS_TalentApply(p,2)
    else
        set hero = null
        return
    endif
    call DialogDisplay(Player(p),KLS_ProgressionDialog[p],false)
    call KLS_ProgressionShow(p)
    set hero = null
endfunction

function KLS_ApplyAutomaticHeroStatGrowth takes unit hero, integer primaryStat returns nothing
    // Native growth is zeroed for selectable hero records. Add a consistent
    // +1 to every attribute and two extra points to the hero's primary stat.
    call ModifyHeroStat(bj_HEROSTAT_STR,hero,bj_MODIFYMETHOD_ADD,1)
    call ModifyHeroStat(bj_HEROSTAT_AGI,hero,bj_MODIFYMETHOD_ADD,1)
    call ModifyHeroStat(bj_HEROSTAT_INT,hero,bj_MODIFYMETHOD_ADD,1)
    call ModifyHeroStat(primaryStat,hero,bj_MODIFYMETHOD_ADD,2)
endfunction

function KLS_TalentLevel takes nothing returns nothing
    local unit u = GetTriggerUnit()
    local integer p = GetPlayerId(GetOwningPlayer(u))
    local integer milestone
    local integer heroLevel
    local integer processedLevel
    if p >= 0 and p < 4 and u == KLS_Hero[p] and KLS_HeroChoice[p] >= 0 then
        set heroLevel = GetHeroLevel(u)
        set processedLevel = KLS_LastAutomaticStatLevel[p]
        loop
            exitwhen processedLevel >= heroLevel
            call KLS_ApplyAutomaticHeroStatGrowth(u,KLS_HeroPrimaryStat[KLS_HeroChoice[p]])
            set processedLevel = processedLevel+1
        endloop
        set KLS_LastAutomaticStatLevel[p] = heroLevel
        call KLS_ApplySpellRanks(u)
        set milestone = GetHeroLevel(u) / 5
        if milestone > KLS_LastTalentMilestone[p] then
            set KLS_TalentPoints[p] = KLS_TalentPoints[p] + milestone - KLS_LastTalentMilestone[p]
            set KLS_LastTalentMilestone[p] = milestone
            call DisplayTimedTextToPlayer(Player(p), 0, 0, 10, "Talent earned at level "+I2S(GetHeroLevel(u))+". Choose a primary-stat specialty.")
        endif
        call KLS_ProgressionShow(p)
        call KLS_StatChoiceRefresh()
    endif
    set u = null
endfunction

function KLS_TalentAvoidDamage takes nothing returns nothing
    local unit victim = GetTriggerUnit()
    local integer p = GetPlayerId(GetOwningPlayer(victim))
    if p >= 0 and p < 4 and victim == KLS_Hero[p] and KLS_TalentAgilityRank[p] > 0 then
        if GetRandomInt(1,100) <= KLS_TalentAgilityRank[p]*2 then
            call BlzSetEventDamage(0.0)
        endif
    endif
    set victim = null
endfunction

function KLS_ProgressionInit takes nothing returns nothing
    local integer p = 0
    local trigger clicks = CreateTrigger()
    local trigger statClicks = CreateTrigger()
    local trigger statSync = CreateTrigger()
    local framehandle gameUI
    local framehandle firstCommandButton
    loop
        exitwhen p == 4
        if KLS_Active[p] then
            set KLS_ProgressionDialog[p] = DialogCreate()
            call TriggerRegisterDialogEvent(clicks,KLS_ProgressionDialog[p])
            call BlzTriggerRegisterPlayerSyncEvent(statSync,Player(p),"KLSSTAT",false)
            if GetLocalPlayer() == Player(p) then
                set gameUI = BlzGetOriginFrame(ORIGIN_FRAME_GAME_UI,0)
                set firstCommandButton = BlzGetOriginFrame(ORIGIN_FRAME_COMMAND_BUTTON,0)
                set KLS_StatChoiceStrengthButton[p] = KLS_StatChoiceCreateButton("KLSStatChoiceStrength","+3 STR",gameUI,firstCommandButton,FRAMEPOINT_TOPLEFT,0.0,0.003)
                call BlzTriggerRegisterFrameEvent(statClicks,KLS_StatChoiceStrengthButton[p],FRAMEEVENT_CONTROL_CLICK)
                set KLS_StatChoiceAgilityButton[p] = KLS_StatChoiceCreateButton("KLSStatChoiceAgility","+3 AGI",gameUI,KLS_StatChoiceStrengthButton[p],FRAMEPOINT_BOTTOMRIGHT,0.002,0.0)
                call BlzTriggerRegisterFrameEvent(statClicks,KLS_StatChoiceAgilityButton[p],FRAMEEVENT_CONTROL_CLICK)
                set KLS_StatChoiceIntelligenceButton[p] = KLS_StatChoiceCreateButton("KLSStatChoiceIntelligence","+3 INT",gameUI,KLS_StatChoiceAgilityButton[p],FRAMEPOINT_BOTTOMRIGHT,0.002,0.0)
                call BlzTriggerRegisterFrameEvent(statClicks,KLS_StatChoiceIntelligenceButton[p],FRAMEEVENT_CONTROL_CLICK)
                set firstCommandButton = null
                set gameUI = null
            endif
        endif
        set p = p+1
    endloop
    call TriggerAddAction(clicks,function KLS_ProgressionClick)
    call TriggerAddAction(statClicks,function KLS_StatChoiceClick)
    call TriggerAddAction(statSync,function KLS_StatChoiceApplySync)
    set KLS_StatChoiceRefreshTimer = CreateTimer()
    call TimerStart(KLS_StatChoiceRefreshTimer,0.25,true,function KLS_StatChoiceRefresh)
    set clicks = null
    set statClicks = null
    set statSync = null
endfunction

function KLS_MovePurchaseToRegularInventory takes unit buyer, item gear returns item
    local integer slot = 0
    local integer emptySlot = -1
    local integer rawcode = GetItemTypeId(gear)
    local item current
    local item moved = null
    // Native shop purchases can land in the 30-slot Forsaken bag. If there is
    // a free six-slot inventory position, place the same catalog item there
    // first; this lets native equipment and merchant drag interactions work.
    loop
        exitwhen slot == 6
        set current = UnitItemInSlot(buyer,slot)
        if current == gear then
            set current = null
            return gear
        endif
        if current == null and emptySlot < 0 then
            set emptySlot = slot
        endif
        set slot = slot+1
    endloop
    if emptySlot >= 0 then
        // Remove the original handle from the extended backpack before asking
        // Warcraft to create its regular-inventory replacement. If the copy
        // cannot be placed, restore that same original item to the buyer.
        call UnitRemoveItem(buyer,gear)
        if UnitAddItemToSlotById(buyer,rawcode,emptySlot) then
            set moved = UnitItemInSlot(buyer,emptySlot)
            if moved != null and GetItemTypeId(moved) == rawcode then
                call SetItemUserData(moved,GetItemUserData(gear))
                call SetItemCharges(moved,GetItemCharges(gear))
                call RemoveItem(gear)
                set current = null
                return moved
            endif
        endif
        call UnitAddItem(buyer,gear)
    endif
    set current = null
    set moved = null
    return gear
endfunction

function KLS_MarketEquipContext takes unit buyer, item gear, integer attempt returns string
    local integer playerId = -1
    local integer slot = 0
    local integer bagSize = 0
    local integer normalFree = 0
    local integer itemType = 0
    local integer family = 0
    local integer equipmentSlot = 0
    local integer itemOwner = 0
    local item current = null
    local string buyerName = "NULL"
    local string buyerType = "NULL"
    local string buyerOwner = "unknown"
    local string alive = "unknown"
    local string backpack = "0/0"
    local string position = "not-on-buyer"
    local string itemName = "NONE"
    if buyer != null then
        set playerId = GetPlayerId(GetOwningPlayer(buyer))
        set buyerName = GetUnitName(buyer)
        set buyerType = GetObjectName(GetUnitTypeId(buyer))+"("+I2S(GetUnitTypeId(buyer))+")"
        set buyerOwner = "p"+I2S(playerId+1)
        set alive = R2S(GetWidgetLife(buyer))
        set bagSize = UnitExtendedInventorySize(buyer)
        set backpack = I2S(UnitExtendedInventoryCount(buyer))+"/"+I2S(bagSize)
        set slot = 0
        loop
            exitwhen slot == 6
            set current = UnitItemInSlot(buyer,slot)
            if current == null then
                set normalFree = normalFree+1
            elseif gear != null and current == gear then
                set position = "inventory-slot="+I2S(slot)
            endif
            set current = null
            set slot = slot+1
        endloop
        set slot = 0
        loop
            exitwhen slot >= bagSize
            set current = UnitItemInBagSlot(buyer,slot)
            if gear != null and current == gear then
                set position = "backpack-slot="+I2S(slot)
            endif
            set current = null
            set slot = slot+1
        endloop
        set slot = 0
        loop
            exitwhen slot == 9
            set current = UnitItemInEquipmentSlot(buyer,ConvertLoadoutSlot(slot))
            if gear != null and current == gear then
                set position = "equipment-slot="+I2S(slot)
            endif
            set current = null
            set slot = slot+1
        endloop
    endif
    if gear != null then
        set itemName = GetItemName(gear)
        set itemType = GetItemTypeId(gear)
        set family = LoadInteger(KLS_GearData,itemType,0)
        set equipmentSlot = LoadInteger(KLS_GearData,itemType,2)
        set itemOwner = GetItemUserData(gear)
    endif
    set current = null
    return " buyer="+buyerName+" buyer-type="+buyerType+" buyer-owner="+buyerOwner+" alive="+alive+" normal-free="+I2S(normalFree)+"/6 backpack="+backpack+" gear-position="+position+" item="+itemName+" item-type="+I2S(itemType)+" item-owner="+I2S(itemOwner)+" catalog-family="+I2S(family)+" equipment-slot="+I2S(equipmentSlot)+" attempt="+I2S(attempt)
endfunction

function KLS_MarketEquipPurchased takes nothing returns nothing
    local timer equipTimer = GetExpiredTimer()
    local integer key = GetHandleId(equipTimer)
    local unit buyer = LoadUnitHandle(KLS_GearData,key,20)
    local item gear = LoadItemHandle(KLS_GearData,key,21)
    local integer p
    local integer rawcode
    local integer attempt = LoadInteger(KLS_GearData,key,22)
    local boolean retry = false
    if buyer != null and gear != null then
        set p = GetPlayerId(GetOwningPlayer(buyer))
        set rawcode = GetItemTypeId(gear)
        if p >= 0 and p < 4 and buyer == KLS_Hero[p] and GetWidgetLife(buyer) > 0.405 and LoadInteger(KLS_GearData,rawcode,0) > 0 then
            set gear = KLS_MovePurchaseToRegularInventory(buyer,gear)
            if UnitEquipItem(buyer,gear) then
                call KLS_Log("Shop purchase equipped after transfer:"+KLS_MarketEquipContext(buyer,gear,attempt))
            else
                if attempt < 8 then
                    set attempt = attempt+1
                    call SaveInteger(KLS_GearData,key,22,attempt)
                    call SaveItemHandle(KLS_GearData,key,21,gear)
                    call TimerStart(equipTimer,0.25,false,function KLS_MarketEquipPurchased)
                    set retry = true
                else
                    call KLS_Log("ERROR native equip rejected shop item after transfer:"+KLS_MarketEquipContext(buyer,gear,attempt))
                    call DisplayTimedTextToPlayer(GetOwningPlayer(buyer),0,0,8,"Your gear is safe in your normal inventory or backpack, but Warcraft has not equipped it. Make room in the six inventory slots, then try the equipment panel again.")
                endif
            endif
        else
            call KLS_Log("ERROR purchased gear cannot equip: buyer is not the living owning hero"+KLS_MarketEquipContext(buyer,gear,attempt))
        endif
    else
        call KLS_Log("ERROR deferred equipment lost its buyer or item handle")
    endif
    if not retry then
        call FlushChildHashtable(KLS_GearData,key)
        call PauseTimer(equipTimer)
        call DestroyTimer(equipTimer)
    endif
    set equipTimer = null
    set buyer = null
    set gear = null
endfunction

function KLS_MarketBuy takes nothing returns nothing
    local unit shop = GetSellingUnit()
    local unit buyer = GetBuyingUnit()
    local item gear = GetSoldItem()
    local integer rawcode = GetItemTypeId(gear)
    local integer p = GetPlayerId(GetOwningPlayer(buyer))
    local integer quotedTier = -1
    local timer equipTimer = null
    if shop == KLS_Castle then
        if rawcode == 'KHE1' then
            call KLS_KingContribute(GetOwningPlayer(buyer),false,KLS_KingTier,true)
            call AddItemToStock(shop,'KHE1',1,1)
        elseif rawcode == 'KUP1' or rawcode == 'KUP2' or rawcode == 'KUP3' or rawcode == 'KUP4' or rawcode == 'KUP5' then
            if rawcode == 'KUP1' then
                set quotedTier = 0
            elseif rawcode == 'KUP2' then
                set quotedTier = 1
            elseif rawcode == 'KUP3' then
                set quotedTier = 2
            elseif rawcode == 'KUP4' then
                set quotedTier = 3
            else
                set quotedTier = 4
            endif
            call KLS_KingContribute(GetOwningPlayer(buyer),true,quotedTier,true)
            if KLS_KingTier > quotedTier then
                if KLS_KingTier == 1 then
                    call AddItemToStock(shop,'KUP2',1,1)
                elseif KLS_KingTier == 2 then
                    call AddItemToStock(shop,'KUP3',1,1)
                elseif KLS_KingTier == 3 then
                    call AddItemToStock(shop,'KUP4',1,1)
                elseif KLS_KingTier == 4 then
                    call AddItemToStock(shop,'KUP5',1,1)
                endif
            elseif KLS_KingTier == quotedTier then
                call AddItemToStock(shop,rawcode,1,1)
            endif
        endif
        call RemoveItem(gear)
    elseif KLS_IsRecipe(rawcode) then
        if p >= 0 and p < 4 and KLS_Active[p] and buyer == KLS_Hero[p] and GetWidgetLife(buyer) > 0.405 then
            if KLS_IsFactionFoundry(GetUnitTypeId(shop)) and GetOwningPlayer(shop) != GetOwningPlayer(buyer) then
                call SetPlayerState(Player(p), PLAYER_STATE_RESOURCE_GOLD, GetPlayerState(Player(p), PLAYER_STATE_RESOURCE_GOLD) + KLS_RecipePrice(rawcode))
                call DisplayTimedTextToPlayer(Player(p), 0, 0, 8, "Use your own faction's Foundry to buy its personal pattern. The fee was refunded.")
                call RemoveItem(gear)
                call KLS_RecipeRestockVendor(shop, rawcode)
            else
                call KLS_RecipeBegin(buyer, gear, shop)
            endif
        else
            if p >= 0 and p < 4 then
                call SetPlayerState(Player(p), PLAYER_STATE_RESOURCE_GOLD, GetPlayerState(Player(p), PLAYER_STATE_RESOURCE_GOLD) + KLS_RecipePrice(rawcode))
                call DisplayTimedTextToPlayer(Player(p), 0, 0, 8, "Buy recipes with your living hero. The fee was refunded.")
            endif
            call RemoveItem(gear)
            call KLS_RecipeRestockVendor(shop, rawcode)
        endif
    elseif KLS_BookAmount(rawcode) > 0 then
        if p >= 0 and p < 4 and KLS_Active[p] and buyer == KLS_Hero[p] and GetWidgetLife(buyer) > 0.405 then
            call ModifyHeroStat(KLS_BookStat(rawcode), buyer, bj_MODIFYMETHOD_ADD, KLS_BookAmount(rawcode))
            call DisplayTimedTextToPlayer(Player(p), 0, 0, 8, GetItemName(gear) + " permanently increased your attribute.")
            call KLS_Log("Attribute tome used at purchase: " + GetItemName(gear) + " owner=p" + I2S(p+1))
        else
            if p >= 0 and p < 4 then
                call SetPlayerState(Player(p), PLAYER_STATE_RESOURCE_GOLD, GetPlayerState(Player(p), PLAYER_STATE_RESOURCE_GOLD) + KLS_BookPrice(rawcode))
                call DisplayTimedTextToPlayer(Player(p), 0, 0, 8, "Attribute tomes require your living hero. The fee was refunded.")
            endif
        endif
        call RemoveItem(gear)
        call AddItemToStock(shop, rawcode, 1, 1)
    else
        if p >= 0 and p < 4 then
            call SetItemUserData(gear,p+1)
            if LoadInteger(KLS_GearData,rawcode,0) > 0 then
                set equipTimer = CreateTimer()
                call SaveUnitHandle(KLS_GearData,GetHandleId(equipTimer),20,buyer)
                call SaveItemHandle(KLS_GearData,GetHandleId(equipTimer),21,gear)
                call SaveInteger(KLS_GearData,GetHandleId(equipTimer),22,0)
                call TimerStart(equipTimer,0.25,false,function KLS_MarketEquipPurchased)
            endif
        endif
        call AddItemToStock(shop,rawcode,1,1)
    endif
    set shop = null
    set buyer = null
    set gear = null
    set equipTimer = null
endfunction

function KLS_BossPauseTower takes nothing returns nothing
    local unit tower = GetEnumUnit()
    local integer rawcode = GetUnitTypeId(tower)
    if GetWidgetLife(tower) > 0.405 and KLS_IsFactionTower(rawcode) then
        call PauseUnit(tower,KLS_BossPauseState)
    endif
    set tower = null
endfunction

function KLS_SetTowersPaused takes boolean paused returns nothing
    local group towers = CreateGroup()
    local integer p = 0
    set KLS_BossPauseState = paused
    loop
        exitwhen p == 4
        if KLS_Active[p] then
            call GroupEnumUnitsOfPlayer(towers,Player(p),null)
            call ForGroup(towers,function KLS_BossPauseTower)
            call GroupClear(towers)
        endif
        set p = p+1
    endloop
    call DestroyGroup(towers)
    set towers = null
endfunction

function KLS_BossSlam takes nothing returns nothing
    local group targets = CreateGroup()
    local unit victim
    local integer owner
    local real damage = 80 + KLS_Wave * 7
    call DestroyEffect(AddSpecialEffect("Abilities\\Spells\\Human\\Thunderclap\\ThunderClapCaster.mdl",KLS_BossX,KLS_BossY))
    call GroupEnumUnitsInRange(targets,KLS_BossX,KLS_BossY,550,null)
    loop
        set victim = FirstOfGroup(targets)
        exitwhen victim == null
        call GroupRemoveUnit(targets,victim)
        set owner = GetPlayerId(GetOwningPlayer(victim))
        if owner >= 0 and owner < 4 and KLS_Active[owner] and GetWidgetLife(victim) > 0.405 then
            call UnitDamageTarget(KLS_Boss,victim,damage,false,false,ATTACK_TYPE_MAGIC,DAMAGE_TYPE_MAGIC,null)
        endif
    endloop
    call DestroyGroup(targets)
    set targets = null
    set victim = null
endfunction

function KLS_BossSummon takes nothing returns nothing
    local integer n = 0
    local integer count = KLS_Players * 2
    local integer spawned = 0
    local integer kind = 'uske'
    local unit summon
    local real hp = 180 + KLS_Wave * 55 + KLS_Players * 35
    local boolean spawnFailed = false
    loop
        exitwhen n == count or spawnFailed or KLS_Ended
        if ModuloInteger(n,2) == 1 then
            set kind = 'nfgu'
        else
            set kind = 'uske'
        endif
        set summon = KLS_CreateUnitOptional(Player(11),kind,KLS_BossX+GetRandomReal(-250,250),KLS_BossY+GetRandomReal(-250,250),270,"boss reinforcement")
        if summon != null then
            call BlzSetUnitMaxHP(summon,R2I(hp))
            call SetWidgetLife(summon,hp)
            call BlzSetUnitBaseDamage(summon,6+KLS_Wave*2,0)
            call SetUnitAcquireRange(summon,900)
            call GroupAddUnit(KLS_Enemies,summon)
            set KLS_Alive = KLS_Alive+1
            set spawned = spawned+1
            call IssuePointOrder(summon,"attack",0,350)
        else
            set spawnFailed = true
            call KLS_Log("WARN boss reinforcement sequence stopped after a failed optional spawn; spawned="+I2S(spawned))
        endif
        set n = n+1
    endloop
    if not spawnFailed then
        call KLS_Log("Boss reinforcements spawned: "+I2S(spawned)+"; wave enemies tracked once each")
    endif
    set summon = null
endfunction

function KLS_BossExecuteMechanic takes nothing returns nothing
    if KLS_BossMechanic == 1 or KLS_BossMechanic == 4 or KLS_BossMechanic == 5 then
        call KLS_BossSlam()
    endif
    if KLS_BossMechanic == 2 or KLS_BossMechanic == 4 or KLS_BossMechanic == 5 then
        call KLS_BossSummon()
    endif
    if KLS_BossMechanic == 3 or KLS_BossMechanic == 4 or KLS_BossMechanic == 5 then
        set KLS_TowerSuppression = 8
        call KLS_SetTowersPaused(true)
        call DisplayTimedTextToForce(bj_FORCE_ALL_PLAYERS,8,"|cffff4444The boss suppresses defender towers for 8 seconds!|r")
    endif
    set KLS_BossCast = 0
endfunction

function KLS_Sanctuary takes nothing returns nothing
    local unit tower = GetEnumUnit()
    local group targets
    local unit u
    if KLS_IsFactionSanctuaryTower(GetUnitTypeId(tower)) and GetWidgetLife(tower) > 0.405 and KLS_TowerSuppression == 0 then
        set targets = CreateGroup()
        call GroupEnumUnitsInRange(targets,GetUnitX(tower),GetUnitY(tower),650,null)
        loop
            set u = FirstOfGroup(targets)
            exitwhen u == null
            call GroupRemoveUnit(targets,u)
            if IsUnitAlly(u,GetOwningPlayer(tower)) and not IsUnitType(u,UNIT_TYPE_STRUCTURE) and GetWidgetLife(u) > 0.405 then
                call SetWidgetLife(u,RMinBJ(BlzGetUnitMaxHP(u),GetWidgetLife(u)+15))
            endif
        endloop
        call DestroyGroup(targets)
    endif
    set targets = null
    set u = null
    set tower = null
endfunction

function KLS_CombatTick takes nothing returns nothing
    local group targets
    local integer p = 0
    if KLS_TowerSuppression > 0 then
        set KLS_TowerSuppression = KLS_TowerSuppression-1
        if KLS_TowerSuppression == 0 then
            call KLS_SetTowersPaused(false)
            call DisplayTimedTextToForce(bj_FORCE_ALL_PLAYERS,5,"|cff80ff80Defender towers are active again.|r")
        endif
    endif
    if ModuloInteger(KLS_Seconds,3) == 0 then
        set targets = CreateGroup()
        loop
            exitwhen p == 4
            if KLS_Active[p] then
                call GroupEnumUnitsOfPlayer(targets,Player(p),null)
                call ForGroup(targets,function KLS_Sanctuary)
                call GroupClear(targets)
            endif
            set p = p+1
        endloop
        call DestroyGroup(targets)
        set targets = null
    endif
    if KLS_Boss != null and GetWidgetLife(KLS_Boss) > 0.405 then
        if KLS_BossCast > 0 then
            set KLS_BossCast = KLS_BossCast-1
            if KLS_BossCast == 0 then
                call KLS_BossExecuteMechanic()
            endif
        elseif ModuloInteger(KLS_Seconds,18) == 0 then
            set KLS_BossX = GetUnitX(KLS_Boss)
            set KLS_BossY = GetUnitY(KLS_Boss)
            set KLS_BossCast = 3
            call DisplayTimedTextToForce(bj_FORCE_ALL_PLAYERS,3,"|cffff4444"+KLS_BossMechanicName(KLS_BossMechanic)+" in 3 seconds! Watch the Boss warning panel.|r")
            call DestroyEffect(AddSpecialEffect("Abilities\\Spells\\Other\\Doom\\DoomTarget.mdl",KLS_BossX,KLS_BossY))
        endif
    else
        set KLS_BossCast = 0
        set KLS_BossMechanic = 0
    endif
    set targets = null
endfunction
