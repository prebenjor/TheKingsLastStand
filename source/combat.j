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
    framehandle array KLS_TalentStrengthButton
    framehandle array KLS_TalentAgilityButton
    framehandle array KLS_TalentIntelligenceButton
    framehandle array KLS_StatChoiceStrengthButton
    framehandle array KLS_StatChoiceAgilityButton
    framehandle array KLS_StatChoiceIntelligenceButton
    timer KLS_StatChoiceRefreshTimer = null
    boolean KLS_Debug = true
endglobals

// Follow the living objective wherever the authored layout places it.
// Attack-move retains ordinary pathing and lets invaders engage defenders en route.
function KLS_OrderInvader takes unit invader returns nothing
    if KLS_Ended or invader == null or KLS_King == null then
        return
    endif
    if GetWidgetLife(invader) <= 0.405 or GetWidgetLife(KLS_King) <= 0.405 then
        return
    endif
    call IssuePointOrder(invader,"attack",GetUnitX(KLS_King),GetUnitY(KLS_King))
endfunction

function KLS_StatChoiceRefresh takes nothing returns nothing
    local integer p = GetPlayerId(GetLocalPlayer())
    local unit hero
    local boolean showChoices = false
    local boolean showTalents = false
    if p >= 0 and p < 4 and KLS_Active[p] then
        set hero = KLS_Hero[p]
        if hero != null then
            set showChoices = not KLS_Ended and IsUnitSelected(hero,Player(p)) and GetHeroSkillPoints(hero) > 0
            set showTalents = not KLS_Ended and IsUnitSelected(hero,Player(p)) and KLS_TalentPoints[p] > 0
        endif
        if GetLocalPlayer() == Player(p) then
            if KLS_StatChoiceStrengthButton[p] != null then
                call BlzFrameSetVisible(KLS_StatChoiceStrengthButton[p],showChoices)
                call BlzFrameSetVisible(KLS_StatChoiceAgilityButton[p],showChoices)
                call BlzFrameSetVisible(KLS_StatChoiceIntelligenceButton[p],showChoices)
                call BlzFrameSetVisible(KLS_TalentStrengthButton[p],showTalents)
                call BlzFrameSetVisible(KLS_TalentAgilityButton[p],showTalents)
                call BlzFrameSetVisible(KLS_TalentIntelligenceButton[p],showTalents)
                call BlzFrameSetText(KLS_TalentStrengthButton[p],"+ STR ["+I2S(KLS_TalentPoints[p])+"]")
                call BlzFrameSetText(KLS_TalentAgilityButton[p],"+ AGI ["+I2S(KLS_TalentPoints[p])+"]")
                call BlzFrameSetText(KLS_TalentIntelligenceButton[p],"+ INT ["+I2S(KLS_TalentPoints[p])+"]")
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
    local integer p = GetPlayerId(GetTriggerPlayer())
    local framehandle clicked = BlzGetTriggerFrame()
    if p < 0 or p >= 4 or GetLocalPlayer() != GetTriggerPlayer() then
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
    call KLS_StatChoiceRefresh()
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

function KLS_TalentChoiceApplySync takes nothing returns nothing
    local integer p = GetPlayerId(GetTriggerPlayer())
    local string payload = BlzGetTriggerSyncData()
    local integer choice = S2I(payload)
    local unit hero
    if p < 0 or p >= 4 or not KLS_Active[p] or KLS_Ended or choice < 0 or choice > 2 or payload != I2S(choice) then
        return
    endif
    set hero = KLS_Hero[p]
    if hero != null and GetOwningPlayer(hero) == Player(p) and KLS_TalentPoints[p] > 0 then
        set KLS_TalentPoints[p] = KLS_TalentPoints[p]-1
        call KLS_TalentApply(p,choice)
    endif
    call KLS_StatChoiceRefresh()
    set hero = null
endfunction

function KLS_TalentChoiceClick takes nothing returns nothing
    local integer p = GetPlayerId(GetTriggerPlayer())
    local framehandle clicked = BlzGetTriggerFrame()
    if p < 0 or p >= 4 or GetLocalPlayer() != GetTriggerPlayer() then
        return
    endif
    if clicked == KLS_TalentStrengthButton[p] then
        call BlzSendSyncData("KLSTALENT","0")
    elseif clicked == KLS_TalentAgilityButton[p] then
        call BlzSendSyncData("KLSTALENT","1")
    elseif clicked == KLS_TalentIntelligenceButton[p] then
        call BlzSendSyncData("KLSTALENT","2")
    endif
    set clicked = null
endfunction

function KLS_TalentLevel takes nothing returns nothing
    local unit u = GetTriggerUnit()
    local integer p = GetPlayerId(GetOwningPlayer(u))
    local integer milestone
    local integer heroLevel
    if p >= 0 and p < 4 and u == KLS_Hero[p] and KLS_HeroChoice[p] >= 0 then
        set heroLevel = GetHeroLevel(u)
        call KLS_NativeSignatureRefresh(u)
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
    if p >= 0 and p < 4 and victim == KLS_Hero[p] and KLS_TalentAgilityRank[p] > 0 and BlzGetEventIsAttack() and GetEventDamage() > 0.0 then
        if GetRandomInt(1,100) <= KLS_TalentAgilityRank[p]*2 then
            call BlzSetEventDamage(0.0)
        endif
    endif
    set victim = null
endfunction

function KLS_ProgressionInit takes nothing returns nothing
    local integer p = 0
    local trigger talentClicks = CreateTrigger()
    local trigger talentSync = CreateTrigger()
    local trigger statClicks = CreateTrigger()
    local trigger statSync = CreateTrigger()
    local framehandle gameUI
    local framehandle firstCommandButton
    loop
        exitwhen p == 4
        if KLS_Active[p] then
            call BlzTriggerRegisterPlayerSyncEvent(talentSync,Player(p),"KLSTALENT",false)
            call BlzTriggerRegisterPlayerSyncEvent(statSync,Player(p),"KLSSTAT",false)
            // Frame creation and registration must run on every client.
            // KLS_StatChoiceRefresh alone controls owner-local visibility.
            if KLS_Active[p] then
                set gameUI = BlzGetOriginFrame(ORIGIN_FRAME_GAME_UI,0)
                set firstCommandButton = BlzGetOriginFrame(ORIGIN_FRAME_COMMAND_BUTTON,0)
                set KLS_StatChoiceStrengthButton[p] = KLS_StatChoiceCreateButton("KLSStatChoiceStrength","+3 STR",gameUI,firstCommandButton,FRAMEPOINT_TOPLEFT,0.0,0.003)
                call BlzTriggerRegisterFrameEvent(statClicks,KLS_StatChoiceStrengthButton[p],FRAMEEVENT_CONTROL_CLICK)
                set KLS_StatChoiceAgilityButton[p] = KLS_StatChoiceCreateButton("KLSStatChoiceAgility","+3 AGI",gameUI,KLS_StatChoiceStrengthButton[p],FRAMEPOINT_BOTTOMRIGHT,0.002,0.0)
                call BlzTriggerRegisterFrameEvent(statClicks,KLS_StatChoiceAgilityButton[p],FRAMEEVENT_CONTROL_CLICK)
                set KLS_StatChoiceIntelligenceButton[p] = KLS_StatChoiceCreateButton("KLSStatChoiceIntelligence","+3 INT",gameUI,KLS_StatChoiceAgilityButton[p],FRAMEPOINT_BOTTOMRIGHT,0.002,0.0)
                call BlzTriggerRegisterFrameEvent(statClicks,KLS_StatChoiceIntelligenceButton[p],FRAMEEVENT_CONTROL_CLICK)
                set KLS_TalentStrengthButton[p] = KLS_StatChoiceCreateButton("KLSTalentStrength","+ STR",gameUI,KLS_StatChoiceStrengthButton[p],FRAMEPOINT_TOPLEFT,0.0,0.003)
                call BlzTriggerRegisterFrameEvent(talentClicks,KLS_TalentStrengthButton[p],FRAMEEVENT_CONTROL_CLICK)
                set KLS_TalentAgilityButton[p] = KLS_StatChoiceCreateButton("KLSTalentAgility","+ AGI",gameUI,KLS_TalentStrengthButton[p],FRAMEPOINT_BOTTOMRIGHT,0.002,0.0)
                call BlzTriggerRegisterFrameEvent(talentClicks,KLS_TalentAgilityButton[p],FRAMEEVENT_CONTROL_CLICK)
                set KLS_TalentIntelligenceButton[p] = KLS_StatChoiceCreateButton("KLSTalentIntelligence","+ INT",gameUI,KLS_TalentAgilityButton[p],FRAMEPOINT_BOTTOMRIGHT,0.002,0.0)
                call BlzTriggerRegisterFrameEvent(talentClicks,KLS_TalentIntelligenceButton[p],FRAMEEVENT_CONTROL_CLICK)
                set firstCommandButton = null
                set gameUI = null
            endif
        endif
        set p = p+1
    endloop
    call TriggerAddAction(talentClicks,function KLS_TalentChoiceClick)
    call TriggerAddAction(talentSync,function KLS_TalentChoiceApplySync)
    call TriggerAddAction(statClicks,function KLS_StatChoiceClick)
    call TriggerAddAction(statSync,function KLS_StatChoiceApplySync)
    set KLS_StatChoiceRefreshTimer = CreateTimer()
    call TimerStart(KLS_StatChoiceRefreshTimer,0.25,true,function KLS_StatChoiceRefresh)
    set talentClicks = null
    set talentSync = null
    set statClicks = null
    set statSync = null
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
            // Keep the exact handle delivered by Warcraft. Never create a
            // replacement while the native backpack still owns the purchase.
            if UnitHasItemEquipped(buyer,gear) then
                call KLS_Log("Shop purchase already equipped:"+KLS_MarketEquipContext(buyer,gear,attempt))
            elseif GetItemUserData(gear) != p+1 or not (UnitHasItem(buyer,gear) or UnitHasItemBagged(buyer,gear)) then
                call KLS_Log("Shop auto-equip cancelled: purchase no longer owned/carried by buyer:"+KLS_MarketEquipContext(buyer,gear,attempt))
            elseif UnitEquipItem(buyer,gear) then
                call KLS_Log("Shop purchase equipped using original handle:"+KLS_MarketEquipContext(buyer,gear,attempt))
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
    if buyer == null or gear == null or rawcode == 0 then
        return
    endif
    if KLS_CompanyServiceIndex(rawcode) >= 0 then
        call KLS_CompanyResearchBuy(shop,buyer,gear)
    elseif shop == KLS_Castle then
        if rawcode == 'KHE1' then
            call KLS_KingContribute(GetOwningPlayer(buyer),false,KLS_KingTier,true)
            // Native KHE1 stock regeneration is one second; do not refill immediately.
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
        call RemoveItemFromStock(shop, rawcode)
        call AddItemToStock(shop, rawcode, 99, 99)
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
    local real damage = (80 + KLS_Wave * 7)*KLS_DifficultyDamageScale()
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
    local integer count = 0
    local integer spawned = 0
    local integer kind = 'uske'
    local unit summon
    local real hp
    local boolean spawnFailed = false
    if KLS_Players <= 0 or KLS_Ended then
        return
    endif
    set count = KLS_DifficultyScaledCount(KLS_Players*2)
    set hp = (180 + KLS_Wave * 55 + KLS_Players * 35)*KLS_DifficultyHealthScale()
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
            call BlzSetUnitBaseDamage(summon,R2I(I2R(6+KLS_Wave*2)*KLS_DifficultyDamageScale()+0.5),0)
            call SetUnitAcquireRange(summon,900)
            call GroupAddUnit(KLS_Enemies,summon)
            set KLS_Alive = KLS_Alive+1
            set spawned = spawned+1
            call KLS_OrderInvader(summon)
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
