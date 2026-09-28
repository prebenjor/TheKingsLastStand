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
    integer array KLS_StatPending
    integer array KLS_TalentStrengthRank
    integer array KLS_TalentAgilityRank
    integer array KLS_TalentIntelligenceRank
    dialog array KLS_ProgressionDialog
    button array KLS_StatStrengthButton
    button array KLS_StatAgilityButton
    button array KLS_StatIntelligenceButton
    button array KLS_TalentStrengthButton
    button array KLS_TalentAgilityButton
    button array KLS_TalentIntelligenceButton
    boolean KLS_Debug = true
endglobals

function KLS_ProgressionShow takes integer p returns nothing
    if p < 0 or p >= 4 or not KLS_Active[p] or KLS_ProgressionDialog[p] == null then
        return
    endif
    call DialogClear(KLS_ProgressionDialog[p])
    if KLS_StatPending[p] > 0 then
        call DialogSetMessage(KLS_ProgressionDialog[p],"Level-up stat investment: choose where to put this level's 3 points.")
        set KLS_StatStrengthButton[p] = DialogAddButton(KLS_ProgressionDialog[p],"+3 Strength",0)
        set KLS_StatAgilityButton[p] = DialogAddButton(KLS_ProgressionDialog[p],"+3 Agility",0)
        set KLS_StatIntelligenceButton[p] = DialogAddButton(KLS_ProgressionDialog[p],"+3 Intelligence",0)
    elseif KLS_TalentPoints[p] > 0 then
        call DialogSetMessage(KLS_ProgressionDialog[p],"Talent earned! Every 5 hero levels, choose one specialty.")
        set KLS_TalentStrengthButton[p] = DialogAddButton(KLS_ProgressionDialog[p],"Vanguard: Strength, health and regeneration",0)
        set KLS_TalentAgilityButton[p] = DialogAddButton(KLS_ProgressionDialog[p],"Skirmisher: Agility, attack speed and evasion",0)
        set KLS_TalentIntelligenceButton[p] = DialogAddButton(KLS_ProgressionDialog[p],"Sage: Intelligence, mana and regeneration",0)
    else
        return
    endif
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
    if clicked == KLS_StatStrengthButton[p] then
        call ModifyHeroStat(bj_HEROSTAT_STR,hero,bj_MODIFYMETHOD_ADD,3)
    elseif clicked == KLS_StatAgilityButton[p] then
        call ModifyHeroStat(bj_HEROSTAT_AGI,hero,bj_MODIFYMETHOD_ADD,3)
    elseif clicked == KLS_StatIntelligenceButton[p] then
        call ModifyHeroStat(bj_HEROSTAT_INT,hero,bj_MODIFYMETHOD_ADD,3)
    elseif clicked == KLS_TalentStrengthButton[p] and KLS_TalentPoints[p] > 0 then
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
    if KLS_StatPending[p] > 0 then
        set KLS_StatPending[p] = KLS_StatPending[p]-1
    endif
    call DialogDisplay(Player(p),KLS_ProgressionDialog[p],false)
    call KLS_ProgressionShow(p)
    set hero = null
endfunction

function KLS_TalentLevel takes nothing returns nothing
    local unit u = GetTriggerUnit()
    local integer p = GetPlayerId(GetOwningPlayer(u))
    local integer milestone
    if p >= 0 and p < 4 and u == KLS_Hero[p] then
        call KLS_ApplySpellRanks(u)
        set KLS_StatPending[p] = KLS_StatPending[p]+1
        set milestone = GetHeroLevel(u) / 5
        if milestone > KLS_LastTalentMilestone[p] then
            set KLS_TalentPoints[p] = KLS_TalentPoints[p] + milestone - KLS_LastTalentMilestone[p]
            set KLS_LastTalentMilestone[p] = milestone
            call DisplayTimedTextToPlayer(Player(p), 0, 0, 10, "Talent earned at level "+I2S(GetHeroLevel(u))+". Choose a primary-stat specialty after your stat investment.")
        endif
        call KLS_ProgressionShow(p)
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
    loop
        exitwhen p == 4
        if KLS_Active[p] then
            set KLS_ProgressionDialog[p] = DialogCreate()
            call TriggerRegisterDialogEvent(clicks,KLS_ProgressionDialog[p])
        endif
        set p = p+1
    endloop
    call TriggerAddAction(clicks,function KLS_ProgressionClick)
    set clicks = null
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
    if emptySlot >= 0 and UnitAddItemToSlotById(buyer,rawcode,emptySlot) then
        set moved = UnitItemInSlot(buyer,emptySlot)
        if moved != null and GetItemTypeId(moved) == rawcode then
            call SetItemUserData(moved,GetItemUserData(gear))
            call SetItemCharges(moved,GetItemCharges(gear))
            call RemoveItem(gear)
            set current = null
            return moved
        endif
    endif
    set current = null
    set moved = null
    return gear
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
                call KLS_Log("Shop purchase equipped after transfer: "+GetItemName(gear)+" owner=p"+I2S(p+1)+" equipment slot id="+I2S(LoadInteger(KLS_GearData,rawcode,2)))
            else
                if attempt < 8 then
                    set attempt = attempt+1
                    call SaveInteger(KLS_GearData,key,22,attempt)
                    call SaveItemHandle(KLS_GearData,key,21,gear)
                    call TimerStart(equipTimer,0.25,false,function KLS_MarketEquipPurchased)
                    set retry = true
                else
                    call KLS_Log("ERROR native equip rejected shop item after transfer: "+GetItemName(gear)+" item type="+I2S(rawcode)+" equipment slot id="+I2S(LoadInteger(KLS_GearData,rawcode,2)))
                    call DisplayTimedTextToPlayer(GetOwningPlayer(buyer),0,0,8,"Your gear is safe in your normal inventory or backpack, but Warcraft has not equipped it. Make room in the six inventory slots, then try the equipment panel again.")
                endif
            endif
        else
            call KLS_Log("ERROR purchased gear cannot equip: buyer is not the living owning hero; item="+GetItemName(gear)+" player="+I2S(p+1))
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
            call KLS_RecipeBegin(buyer, gear)
        else
            if p >= 0 and p < 4 then
                call SetPlayerState(Player(p), PLAYER_STATE_RESOURCE_GOLD, GetPlayerState(Player(p), PLAYER_STATE_RESOURCE_GOLD) + KLS_RecipePrice(rawcode))
                call DisplayTimedTextToPlayer(Player(p), 0, 0, 8, "Buy recipes with your living hero. The fee was refunded.")
            endif
            call RemoveItem(gear)
            call AddItemToStock(KLS_Shops[4], rawcode, 1, 1)
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
        set summon = KLS_CreateUnit(Player(11),kind,KLS_BossX+GetRandomReal(-250,250),KLS_BossY+GetRandomReal(-250,250),270)
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
            call KLS_AbortForSpawnFailure("boss reinforcement", kind)
        endif
        set n = n+1
    endloop
    if not spawnFailed then
        call KLS_Log("Boss reinforcements spawned: "+I2S(spawned)+"; wave enemies tracked once each")
    endif
    set summon = null
endfunction

function KLS_BossExecuteMechanic takes nothing returns nothing
    if KLS_BossMechanic == 1 or KLS_BossMechanic == 4 then
        call KLS_BossSlam()
    endif
    if KLS_BossMechanic == 2 or KLS_BossMechanic == 4 then
        call KLS_BossSummon()
    endif
    if KLS_BossMechanic == 3 or KLS_BossMechanic == 4 then
        set KLS_TowerSuppression = 8
        call KLS_SetTowersPaused(true)
        call DisplayTimedTextToForce(bj_FORCE_ALL_PLAYERS,8,"|cffff4444Siege Blight suppresses defender towers for 8 seconds!|r")
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
