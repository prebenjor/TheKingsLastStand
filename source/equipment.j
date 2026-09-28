globals
    hashtable KLS_GearData = null
    real KLS_GearTime = 0
    boolean KLS_GearDamage = false
    real array KLS_EffectReady
    timer KLS_GearClock = null
endglobals

function KLS_EquippedTier takes unit hero, integer family returns integer
    local integer slot = 0
    local integer best = -1
    local integer itemCode
    local item gear
    loop
        exitwhen slot == 9
        set gear = UnitItemInEquipmentSlot(hero,ConvertLoadoutSlot(slot))
        set itemCode = GetItemTypeId(gear)
        if LoadInteger(KLS_GearData,itemCode,0) == family and GetItemUserData(gear) == GetPlayerId(GetOwningPlayer(hero))+1 then
            set best = IMaxBJ(best,LoadInteger(KLS_GearData,itemCode,1))
        endif
        set slot = slot+1
    endloop
    set gear = null
    return best
endfunction

function KLS_EffectPower takes integer tier returns real
    if tier == 2 then
        return 40.0
    elseif tier == 3 then
        return 80.0
    endif
    return 140.0
endfunction

function KLS_ProcDamage takes unit source, unit target, real amount returns nothing
    if not KLS_Ended and GetWidgetLife(target) > 0.405 then
        set KLS_GearDamage = true
        call UnitDamageTarget(source,target,amount,false,false,ATTACK_TYPE_MAGIC,DAMAGE_TYPE_MAGIC,null)
        set KLS_GearDamage = false
    endif
endfunction

function KLS_BleedTick takes nothing returns nothing
    local timer t = GetExpiredTimer()
    local integer key = GetHandleId(t)
    local unit source = LoadUnitHandle(KLS_GearData,key,10)
    local unit target = LoadUnitHandle(KLS_GearData,key,11)
    local integer ticks = LoadInteger(KLS_GearData,key,12)
    if not KLS_Ended and GetWidgetLife(target) > 0.405 then
        call KLS_ProcDamage(source,target,LoadReal(KLS_GearData,key,13))
        set ticks = ticks-1
    else
        set ticks = 0
    endif
    if ticks == 0 then
        call FlushChildHashtable(KLS_GearData,key)
        call PauseTimer(t)
        call DestroyTimer(t)
    else
        call SaveInteger(KLS_GearData,key,12,ticks)
    endif
    set t = null
    set source = null
    set target = null
endfunction

function KLS_GearHit takes nothing returns nothing
    local unit target = GetTriggerUnit()
    local unit source = GetEventDamageSource()
    local integer p = GetPlayerId(GetOwningPlayer(source))
    local integer defender = GetPlayerId(GetOwningPlayer(target))
    local integer tier
    local real amount = GetEventDamage()
    local real cleave = 0
    local real frost = 0
    local timer bleed
    local group targets
    local unit u
    local unit dummy
    if KLS_Ended or amount <= 0 then
        return
    endif
    if defender < 4 and target == KLS_Hero[defender] then
        set tier = KLS_EquippedTier(target,13)
        if tier >= 2 and not BlzGetEventIsAttack() then
            set amount = amount*(1.0-0.05*(tier-1))
        endif
        set tier = KLS_EquippedTier(target,4)
        if tier >= 2 and KLS_GearTime >= KLS_EffectReady[defender*8+3] then
            set amount = RMaxBJ(0,amount-KLS_EffectPower(tier))
            set KLS_EffectReady[defender*8+3] = KLS_GearTime+8
            call DestroyEffect(AddSpecialEffectTarget("Abilities\\Spells\\Human\\ManaShield\\ManaShieldCaster.mdl",target,"origin"))
        endif
        call BlzSetEventDamage(amount)
    endif
    if KLS_GearDamage or p >= 4 or source != KLS_Hero[p] or not BlzGetEventIsAttack() or not IsUnitEnemy(target,Player(p)) then
        return
    endif
    set tier = KLS_EquippedTier(source,1)
    if tier >= 2 then
        set cleave = amount*(0.15+0.10*(tier-2))
    endif
    set tier = KLS_EquippedTier(source,2)
    if tier >= 2 and KLS_GearTime >= KLS_EffectReady[p*8+1] then
        set KLS_EffectReady[p*8+1] = KLS_GearTime+5
        set bleed = CreateTimer()
        call SaveUnitHandle(KLS_GearData,GetHandleId(bleed),10,source)
        call SaveUnitHandle(KLS_GearData,GetHandleId(bleed),11,target)
        call SaveInteger(KLS_GearData,GetHandleId(bleed),12,3)
        if tier == 2 then
            set amount = 30
        elseif tier == 3 then
            set amount = 60
        else
            set amount = 100
        endif
        call SaveReal(KLS_GearData,GetHandleId(bleed),13,amount/3)
        call TimerStart(bleed,1,true,function KLS_BleedTick)
    endif
    set tier = KLS_EquippedTier(source,3)
    if tier >= 2 and KLS_GearTime >= KLS_EffectReady[p*8+2] then
        set KLS_EffectReady[p*8+2] = KLS_GearTime+8
        set frost = KLS_EffectPower(tier)
        call DestroyEffect(AddSpecialEffectTarget("Abilities\\Spells\\Undead\\FrostNova\\FrostNovaTarget.mdl",target,"origin"))
    endif
    if cleave > 0 or frost > 0 then
        set targets = CreateGroup()
        call GroupEnumUnitsInRange(targets,GetUnitX(target),GetUnitY(target),250,null)
        loop
            set u = FirstOfGroup(targets)
            exitwhen u == null
            call GroupRemoveUnit(targets,u)
            if IsUnitEnemy(u,Player(p)) and GetWidgetLife(u) > 0.405 and not IsUnitType(u,UNIT_TYPE_STRUCTURE) then
                if u != target and cleave > 0 then
                    call KLS_ProcDamage(source,u,cleave)
                endif
                if frost > 0 then
                    call KLS_ProcDamage(source,u,frost)
                    set dummy = KLS_CreateUnit(Player(p),'hS01',GetUnitX(u),GetUnitY(u),0)
                    if dummy != null then
                        call IssueTargetOrder(dummy,"slow",u)
                        call UnitApplyTimedLife(dummy,'BTLF',3)
                    endif
                endif
            endif
        endloop
        call DestroyGroup(targets)
    endif
    set source = null
    set target = null
    set u = null
    set dummy = null
    set targets = null
    set bleed = null
endfunction

function KLS_GearCast takes nothing returns nothing
    local unit hero = GetTriggerUnit()
    local integer p = GetPlayerId(GetOwningPlayer(hero))
    local integer tier
    local real mana
    if p < 4 and hero == KLS_Hero[p] and not KLS_Ended then
        set tier = KLS_EquippedTier(hero,5)
        if tier >= 2 and KLS_GearTime >= KLS_EffectReady[p*8+4] then
            set mana = 15
            if tier == 3 then
                set mana = 30
            elseif tier == 4 then
                set mana = 50
            endif
            call SetUnitState(hero,UNIT_STATE_MANA,RMinBJ(GetUnitState(hero,UNIT_STATE_MAX_MANA),GetUnitState(hero,UNIT_STATE_MANA)+mana))
            set KLS_EffectReady[p*8+4] = KLS_GearTime+8
        endif
    endif
    set hero = null
endfunction

function KLS_GearTick takes nothing returns nothing
    local integer p = 0
    local integer tier
    local unit hero
    local unit u
    local group targets
    set KLS_GearTime = KLS_GearTime+0.25
    if KLS_Ended then
        call PauseTimer(KLS_GearClock)
        return
    endif
    loop
        exitwhen p == 4
        set hero = KLS_Hero[p]
        if KLS_Active[p] and hero != null and GetWidgetLife(hero) > 0.405 then
            set tier = KLS_EquippedTier(hero,12)
            if tier >= 2 and KLS_GearTime >= KLS_EffectReady[p*8+5] then
                set KLS_EffectReady[p*8+5] = KLS_GearTime+10
                set targets = CreateGroup()
                call GroupEnumUnitsInRange(targets,GetUnitX(hero),GetUnitY(hero),400,null)
                loop
                    set u = FirstOfGroup(targets)
                    exitwhen u == null
                    call GroupRemoveUnit(targets,u)
                    if IsUnitAlly(u,Player(p)) and IsUnitType(u,UNIT_TYPE_HERO) and GetWidgetLife(u) > 0.405 then
                        call SetWidgetLife(u,RMinBJ(BlzGetUnitMaxHP(u),GetWidgetLife(u)+KLS_EffectPower(tier)))
                        call DestroyEffect(AddSpecialEffectTarget("Abilities\\Spells\\Human\\HolyBolt\\HolyBoltSpecialArt.mdl",u,"origin"))
                    endif
                endloop
                call DestroyGroup(targets)
            endif
        endif
        set p = p+1
    endloop
    set hero = null
    set u = null
    set targets = null
endfunction

function KLS_GearEquip takes nothing returns nothing
    local unit u = GetTriggerUnit()
    local item gear = GetEquippedItem()
    local integer owner = GetItemUserData(gear)
    if owner != 0 and owner != GetPlayerId(GetOwningPlayer(u))+1 then
        call UnitUnequipItem(u,gear)
        call KLS_Log("Rejected equipment belonging to another defender")
    else
        call KLS_Log("Equipped "+GetItemName(gear)+" on "+GetUnitName(u))
    endif
    set u = null
    set gear = null
endfunction

function KLS_GearUnequip takes nothing returns nothing
    call KLS_Log("Unequipped "+GetItemName(GetUnequippedItem())+" from "+GetUnitName(GetTriggerUnit()))
endfunction

function KLS_GearPawned takes nothing returns nothing
    // Pawn-item uses the generic manipulated-item payload, not the sold-unit
    // or sold-item accessors used by the separate shop purchase events.
    local item gear = GetManipulatedItem()
    local unit seller = GetTriggerUnit()
    local integer p = GetPlayerId(GetOwningPlayer(seller))
    local integer rawcode = GetItemTypeId(gear)
    if p >= 0 and p < 4 and gear != null and LoadInteger(KLS_GearData,rawcode,0) > 0 then
        call KLS_Log("Native pawn event: item="+GetItemName(gear)+" seller=p"+I2S(p+1)+" item-owner="+I2S(GetItemUserData(gear)))
        call DisplayTimedTextToPlayer(Player(p),0,0,6,"Sold "+GetItemName(gear)+" back to the market.")
    endif
    set seller = null
    set gear = null
endfunction

function KLS_PackUsed takes nothing returns nothing
    if GetItemTypeId(GetManipulatedItem()) == 'ebua' then
        call KLS_Log("Pack activated: storage="+I2S(UnitExtendedInventorySize(GetTriggerUnit())))
    endif
endfunction

function KLS_GearInit takes nothing returns nothing
    local trigger damage = CreateTrigger()
    local trigger cast = CreateTrigger()
    local trigger equipped = CreateTrigger()
    local trigger used = CreateTrigger()
    local trigger unequipped = CreateTrigger()
    local trigger pawned = CreateTrigger()
    call TriggerRegisterAnyUnitEventBJ(damage,EVENT_PLAYER_UNIT_DAMAGED)
    call TriggerAddAction(damage,function KLS_GearHit)
    call TriggerRegisterAnyUnitEventBJ(cast,EVENT_PLAYER_UNIT_SPELL_EFFECT)
    call TriggerAddAction(cast,function KLS_GearCast)
    call TriggerRegisterAnyUnitEventBJ(equipped,EVENT_PLAYER_UNIT_EQUIP_ITEM)
    call TriggerAddAction(equipped,function KLS_GearEquip)
    call TriggerRegisterAnyUnitEventBJ(unequipped,EVENT_PLAYER_UNIT_UNEQUIP_ITEM)
    call TriggerAddAction(unequipped,function KLS_GearUnequip)
    call TriggerRegisterAnyUnitEventBJ(pawned,EVENT_PLAYER_UNIT_PAWN_ITEM)
    call TriggerAddAction(pawned,function KLS_GearPawned)
    call TriggerRegisterAnyUnitEventBJ(used,EVENT_PLAYER_UNIT_USE_ITEM)
    call TriggerAddAction(used,function KLS_PackUsed)
    set KLS_GearClock = CreateTimer()
    call TimerStart(KLS_GearClock,0.25,true,function KLS_GearTick)
    set damage = null
    set cast = null
    set equipped = null
    set used = null
    set unequipped = null
    set pawned = null
endfunction
