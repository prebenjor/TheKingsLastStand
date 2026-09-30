globals
    boolean array KLS_ClassChosen
    unit array KLS_Altar
    dialog array KLS_ClassDialog
    // Presentation-only state. Never use these values to decide item ownership,
    // equipment, unit orders, resources, or other synchronized gameplay.
    boolean KLS_PackOpenLocal = false
    boolean KLS_PackFramesReady = false
    framehandle KLS_PackBagFrame = null
    framehandle KLS_PackEquipmentFrame = null
    framehandle KLS_PackBackdropFrame = null
    timer KLS_PackViewTimer = null
endglobals

function KLS_PackPanelRefresh takes nothing returns nothing
    local integer p = GetPlayerId(GetLocalPlayer())
    local unit hero = null
    local boolean visible = false
    if not KLS_PackFramesReady then
        return
    endif
    if p >= 0 and p < 4 then
        set hero = KLS_Hero[p]
        if KLS_Active[p] and not KLS_Ended and hero != null then
            if IsUnitSelected(hero,Player(p)) and GetWidgetLife(hero) > 0.405 and UnitExtendedInventorySize(hero) == 30 then
                set visible = KLS_PackOpenLocal
            else
                set KLS_PackOpenLocal = false
            endif
        else
            set KLS_PackOpenLocal = false
        endif
    endif
    // Native item use can hide these singleton UI panels on another client.
    // Restore this client's own preference without reissuing an item order or
    // touching the native bag contents/equipment. Frame names come from the
    // installed UI/FrameDef/UI/InventoryBar.fdf, not a replacement inventory.
    call BlzFrameSetVisible(KLS_PackBagFrame,visible)
    call BlzFrameSetVisible(KLS_PackEquipmentFrame,visible)
    if KLS_PackBackdropFrame != null then
        call BlzFrameSetVisible(KLS_PackBackdropFrame,visible)
    endif
    set hero = null
endfunction

function KLS_PackPanelUsed takes nothing returns nothing
    local unit hero = GetManipulatingUnit()
    local integer p = GetPlayerId(GetOwningPlayer(hero))
    if GetItemTypeId(GetManipulatedItem()) == 'ebac' and p >= 0 and p < 4 then
        if hero == KLS_Hero[p] and GetLocalPlayer() == Player(p) then
            set KLS_PackOpenLocal = not KLS_PackOpenLocal
            if not KLS_PackFramesReady then
                call DisplayTimedTextToPlayer(Player(p),0,0,8,"Backpack UI guard unavailable: native panel handles were not found. Native inventory remains active.")
            endif
        endif
    endif
    set hero = null
endfunction

function KLS_PackPanelEscape takes nothing returns nothing
    if GetLocalPlayer() == GetTriggerPlayer() then
        set KLS_PackOpenLocal = false
    endif
endfunction

function KLS_PackPanelInit takes nothing returns nothing
    local trigger used = CreateTrigger()
    local trigger escape = CreateTrigger()
    local integer p = 0
    // Resolve the same native handles and register events on EVERY client.
    set KLS_PackBagFrame = BlzGetFrameByName("SimpleEquipmentInventoryPanel",0)
    set KLS_PackEquipmentFrame = BlzGetFrameByName("SimpleEquipmentPanel",0)
    set KLS_PackBackdropFrame = BlzGetFrameByName("EquipmentPanelBackdrop",0)
    set KLS_PackFramesReady = KLS_PackBagFrame != null and KLS_PackEquipmentFrame != null
    call TriggerRegisterAnyUnitEventBJ(used,EVENT_PLAYER_UNIT_USE_ITEM)
    call TriggerAddAction(used,function KLS_PackPanelUsed)
    loop
        exitwhen p == 4
        call TriggerRegisterPlayerEvent(escape,Player(p),EVENT_PLAYER_END_CINEMATIC)
        set p = p+1
    endloop
    call TriggerAddAction(escape,function KLS_PackPanelEscape)
    set KLS_PackViewTimer = CreateTimer()
    // Run after native event handling as well as across later UI refreshes.
    // Always start this timer on all clients, even if native frames are absent.
    call TimerStart(KLS_PackViewTimer,0.03,true,function KLS_PackPanelRefresh)
    set used = null
    set escape = null
endfunction

function KLS_BindPickup takes nothing returns nothing
    local item gear = GetManipulatedItem()
    local unit u = GetManipulatingUnit()
    local integer owner = GetItemUserData(gear)
    if owner != 0 and owner != GetPlayerId(GetOwningPlayer(u))+1 then
        call UnitRemoveItem(u, gear)
        call DisplayTimedTextToPlayer(GetOwningPlayer(u), 0, 0, 5, "That item belongs to another defender.")
    elseif owner == 0 and LoadInteger(KLS_GearData,GetItemTypeId(gear),0) > 0 then
        set owner = GetPlayerId(GetOwningPlayer(u))+1
        call SetItemUserData(gear,owner)
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
    call KLS_PackPanelInit()
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
