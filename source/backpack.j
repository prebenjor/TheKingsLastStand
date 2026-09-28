globals
    boolean array KLS_ClassChosen
    unit array KLS_Altar
    dialog array KLS_ClassDialog
endglobals

function KLS_BindPickup takes nothing returns nothing
    local item gear = GetManipulatedItem()
    local unit u = GetManipulatingUnit()
    local integer owner = GetItemUserData(gear)
    if owner != 0 and owner != GetPlayerId(GetOwningPlayer(u))+1 then
        call UnitRemoveItem(u, gear)
        call DisplayTimedTextToPlayer(GetOwningPlayer(u), 0, 0, 5, "That item belongs to another defender.")
    endif
    set gear = null
    set u = null
endfunction

function KLS_AltarSelected takes nothing returns nothing
    local integer p = GetPlayerId(GetTriggerPlayer())
    if p >= 4 or KLS_Ended then
        return
    endif
    if not KLS_IsFactionAltar(GetUnitTypeId(GetTriggerUnit())) or GetOwningPlayer(GetTriggerUnit()) != Player(p) then
        return
    endif
    if not KLS_ClassChosen[p] then
        call DialogDisplay(Player(p), KLS_ClassDialog[p], true)
    elseif KLS_Respawn[p] > 0 then
        call DisplayTimedTextToPlayer(Player(p), 0, 0, 6, "Hero returns in " + I2S(KLS_Respawn[p]) + " seconds.")
    else
        call DisplayTimedTextToPlayer(Player(p), 0, 0, 6, "Your hero has been chosen. Fallen heroes return automatically after 20 seconds.")
    endif
endfunction

function KLS_AltarCompleted takes nothing returns nothing
    local unit u = GetConstructedStructure()
    local integer p = GetPlayerId(GetOwningPlayer(u))
    if p < 4 and KLS_IsFactionAltar(GetUnitTypeId(u)) then
        set KLS_Altar[p] = u
    endif
    set u = null
endfunction

function KLS_InventoryInit takes nothing returns nothing
    local integer p = 0
    local trigger classes = CreateTrigger()
    local trigger pickup = CreateTrigger()
    local trigger altars = CreateTrigger()
    local trigger completed = CreateTrigger()
    loop
        exitwhen p == 4
        if KLS_Active[p] then
            set KLS_ClassDialog[p] = DialogCreate()
            call TriggerRegisterDialogEvent(classes, KLS_ClassDialog[p])
        endif
        set p = p + 1
    endloop
    call TriggerRegisterAnyUnitEventBJ(altars, EVENT_PLAYER_UNIT_SELECTED)
    call TriggerAddAction(altars, function KLS_AltarSelected)
    call TriggerRegisterAnyUnitEventBJ(completed, EVENT_PLAYER_UNIT_CONSTRUCT_FINISH)
    call TriggerAddAction(completed, function KLS_AltarCompleted)
    set altars = null
    set completed = null
    call TriggerAddAction(classes, function KLS_ClassClick)
    call TriggerRegisterAnyUnitEventBJ(pickup, EVENT_PLAYER_UNIT_PICKUP_ITEM)
    call TriggerAddAction(pickup, function KLS_BindPickup)
    set classes = null
    set pickup = null
endfunction
