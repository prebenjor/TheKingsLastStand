globals
    trigger KLS_MiningOrders = null
    unit array KLS_BaseMine
endglobals

function KLS_HauntGoldMine takes nothing returns nothing
    local unit worker = GetTriggerUnit()
    local unit mine = GetOrderTargetUnit()
    local unit haunted = null
    local integer p = GetPlayerId(GetOwningPlayer(worker))
    local integer amount
    local integer orderId = GetIssuedOrderId()
    if p >= 0 and p < 4 and KLS_Active[p] and KLS_PlayerRace[p] == 3 and GetUnitTypeId(worker) == 'uaco' then
        if mine != null and GetUnitTypeId(mine) == 'ngol' and (orderId == OrderId("smart") or orderId == OrderId("harvest") or orderId == OrderId("hauntgoldmine")) then
            set amount = GetResourceAmount(mine)
            set haunted = KLS_CreateUnitOptional(Player(p),'ugol',GetUnitX(mine),GetUnitY(mine),GetUnitFacing(mine),"Undead gold mine haunt")
            if haunted == null or GetUnitTypeId(haunted) != 'ugol' then
                if haunted != null then
                    call RemoveUnit(haunted)
                endif
                call KLS_Log("ERROR Undead mine conversion failed for p"+I2S(p+1)+"; neutral mine preserved")
                call DisplayTimedTextToPlayer(Player(p),0,0,5,"The Acolytes could not claim that mine. Its gold is safe; try again.")
            else
                call SetResourceAmount(haunted,amount)
                call RemoveUnit(mine)
                call IssueTargetOrder(worker,"harvest",haunted)
                call KLS_Log("Undead mine haunted: player="+I2S(p+1)+" gold="+I2S(amount))
                call DisplayTimedTextToPlayer(Player(p),0,0,5,"The Acolytes have haunted the gold mine. Your workers can now harvest it.")
            endif
        endif
    endif
    set worker = null
    set mine = null
    set haunted = null
endfunction

function KLS_MiningInit takes nothing returns nothing
    set KLS_MiningOrders = CreateTrigger()
    call TriggerRegisterAnyUnitEventBJ(KLS_MiningOrders,EVENT_PLAYER_UNIT_ISSUED_TARGET_ORDER)
    call TriggerAddAction(KLS_MiningOrders,function KLS_HauntGoldMine)
endfunction
