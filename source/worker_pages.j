globals
    boolean KLS_WorkerPagesAccepted = false
    hashtable KLS_WorkerPageData = null
    integer array KLS_WorkerStandardId
    integer array KLS_WorkerExpansionId
    integer array KLS_WorkerToExpansion
    integer array KLS_WorkerToStandard
endglobals

// GENERATED_WORKER_PAGES

function KLS_WorkerPageCast takes nothing returns nothing
    local unit worker = GetTriggerUnit()
    local integer rawcode = GetUnitTypeId(worker)
    local integer raceIndex = 0
    local integer morph = 0
    local integer expected = 0
    local integer workerHandle = GetHandleId(worker)
    local player owner = GetOwningPlayer(worker)
    local real life = GetWidgetLife(worker)
    local real mana = GetUnitState(worker,UNIT_STATE_MANA)
    if GetSpellAbilityId() != 'rPg0' then
        set worker = null
        set owner = null
        return
    endif
    call DisplayTimedTextToPlayer(owner,0,0,6,"Construction page: button callback received.")
    // The production initializer does not grant the button until the native
    // acceptance gate is met. Only the dedicated prototype map grants it.
    if (LoadInteger(KLS_WorkerPageData,workerHandle,0) != 0 and LoadInteger(KLS_WorkerPageData,workerHandle,0) != OrderId("stop")) or (GetUnitCurrentOrder(worker) != 0 and GetUnitCurrentOrder(worker) != OrderId("channel")) then
        call DisplayTimedTextToPlayer(owner,0,0,5,"Finish harvesting, repair or construction before changing pages.")
        set worker = null
        set owner = null
        return
    endif
    if IsUnitLoaded(worker) or GetWidgetLife(worker) <= 0.405 then
        call DisplayTimedTextToPlayer(owner,0,0,6,"Construction page: worker is loaded or not alive.")
        set worker = null
        set owner = null
        return
    endif
    loop
        exitwhen raceIndex == 4
        if rawcode == KLS_WorkerStandardId[raceIndex] then
            set morph = KLS_WorkerToExpansion[raceIndex]
            set expected = KLS_WorkerExpansionId[raceIndex]
            exitwhen true
        elseif rawcode == KLS_WorkerExpansionId[raceIndex] then
            set morph = KLS_WorkerToStandard[raceIndex]
            set expected = KLS_WorkerStandardId[raceIndex]
            exitwhen true
        endif
        set raceIndex = raceIndex+1
    endloop
    if morph != 0 then
        call UnitAddAbility(worker,morph)
        call UnitRemoveAbility(worker,morph)
        call SetWidgetLife(worker,life)
        call SetUnitState(worker,UNIT_STATE_MANA,mana)
        call UnitAddAbility(worker,'rPg0')
        call UnitMakeAbilityPermanent(worker,true,'rPg0')
        if GetUnitTypeId(worker) == expected then
            call DisplayTimedTextToPlayer(owner,0,0,8,"Construction page switched. Handle "+I2S(workerHandle)+" -> "+I2S(GetHandleId(worker))+". Open Build (B) to view the changed buildings.")
        else
            call DisplayTimedTextToPlayer(owner,0,0,10,"Construction page FAILED: expected type "+I2S(expected)+", actual "+I2S(GetUnitTypeId(worker))+". Handle "+I2S(workerHandle)+" -> "+I2S(GetHandleId(worker))+".")
        endif
        call KLS_Log("Worker page prototype: same workerHandle="+I2S(GetHandleId(worker))+" original="+I2S(workerHandle)+" expected="+I2S(expected)+" actual="+I2S(GetUnitTypeId(worker))+" owner="+I2S(GetPlayerId(GetOwningPlayer(worker))))
    else
        call DisplayTimedTextToPlayer(owner,0,0,8,"Construction page FAILED: worker type is not registered.")
    endif
    set worker = null
    set owner = null
endfunction

function KLS_WorkerPageOrdered takes nothing returns nothing
    local unit worker = GetTriggerUnit()
    local integer rawcode = GetUnitTypeId(worker)
    local integer issued = GetIssuedOrderId()
    local integer raceIndex = 0
    loop
        exitwhen raceIndex == 4
        if rawcode == KLS_WorkerStandardId[raceIndex] or rawcode == KLS_WorkerExpansionId[raceIndex] then
            if issued != OrderId("channel") then
                call SaveInteger(KLS_WorkerPageData,GetHandleId(worker),0,issued)
                call BlzUnitDisableAbility(worker,'rPg0',issued != OrderId("stop"),false)
            elseif GetUnitAbilityLevel(worker,'rPg0') > 0 then
                call DisplayTimedTextToPlayer(GetOwningPlayer(worker),0,0,6,"Construction page: toggle order received.")
            endif
            exitwhen true
        endif
        set raceIndex = raceIndex+1
    endloop
    set worker = null
endfunction

function KLS_WorkerPageRefreshEnum takes nothing returns nothing
    local unit worker = GetEnumUnit()
    local integer raceIndex = 0
    local integer rawcode = GetUnitTypeId(worker)
    loop
        exitwhen raceIndex == 4
        if rawcode == KLS_WorkerStandardId[raceIndex] or rawcode == KLS_WorkerExpansionId[raceIndex] then
            if GetUnitCurrentOrder(worker) == 0 then
                call SaveInteger(KLS_WorkerPageData,GetHandleId(worker),0,0)
            endif
            if KLS_WorkerPagesAccepted then
                call UnitAddAbility(worker,'rPg0')
                call UnitMakeAbilityPermanent(worker,true,'rPg0')
            endif
            // Keep the button active through its own spell effect; disabling
            // it during the cast can cancel Channel before the callback.
            call BlzUnitDisableAbility(worker,'rPg0',(GetUnitCurrentOrder(worker) != 0 and GetUnitCurrentOrder(worker) != OrderId("channel")) or IsUnitLoaded(worker),false)
            exitwhen true
        endif
        set raceIndex = raceIndex+1
    endloop
    set worker = null
endfunction

function KLS_WorkerPageRefresh takes nothing returns nothing
    local group workers = CreateGroup()
    local integer p = 0
    loop
        exitwhen p == 4
        call GroupEnumUnitsOfPlayer(workers,Player(p),null)
        call ForGroup(workers,function KLS_WorkerPageRefreshEnum)
        set p = p+1
    endloop
    call DestroyGroup(workers)
    set workers = null
endfunction

function KLS_WorkerPagesInit takes nothing returns nothing
    local trigger casts = CreateTrigger()
    local trigger orders = CreateTrigger()
    set KLS_WorkerPageData = InitHashtable()
    call KLS_WorkerPagesCatalog()
    call TriggerRegisterAnyUnitEventBJ(casts,EVENT_PLAYER_UNIT_SPELL_EFFECT)
    call TriggerAddAction(casts,function KLS_WorkerPageCast)
    call TriggerRegisterAnyUnitEventBJ(orders,EVENT_PLAYER_UNIT_ISSUED_ORDER)
    call TriggerRegisterAnyUnitEventBJ(orders,EVENT_PLAYER_UNIT_ISSUED_POINT_ORDER)
    call TriggerRegisterAnyUnitEventBJ(orders,EVENT_PLAYER_UNIT_ISSUED_TARGET_ORDER)
    call TriggerAddAction(orders,function KLS_WorkerPageOrdered)
    call TimerStart(CreateTimer(),0.25,true,function KLS_WorkerPageRefresh)
    set casts = null
    set orders = null
endfunction
