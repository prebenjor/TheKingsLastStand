globals
    integer array KLS_Roster
    integer array KLS_RosterSize
    destructable array KLS_GroveTree
    integer array KLS_GroveDeadTime
    integer KLS_GroveCount = 0
    timer KLS_GroveClock = null
    unit KLS_RestorePool = null
    timer KLS_PoolClock = null
endglobals

// GENERATED_WAVES

function KLS_GroveTick takes nothing returns nothing
    local integer i = 0
    if KLS_Ended then
        call PauseTimer(KLS_GroveClock)
        return
    endif
    loop
        exitwhen i == KLS_GroveCount
        if GetDestructableLife(KLS_GroveTree[i]) <= 0.405 then
            set KLS_GroveDeadTime[i] = KLS_GroveDeadTime[i]+1
            if KLS_GroveDeadTime[i] >= 60 then
                call DestructableRestoreLife(KLS_GroveTree[i],GetDestructableMaxLife(KLS_GroveTree[i]),true)
                set KLS_GroveDeadTime[i] = 0
            endif
        else
            set KLS_GroveDeadTime[i] = 0
        endif
        set i = i+1
    endloop
endfunction

function KLS_GrovePlant takes real x, real y returns nothing
    set KLS_GroveTree[KLS_GroveCount] = KLS_CreateDestructableOptional('LTlt',x,y,0,1,0,"ability grove tree")
    if KLS_GroveTree[KLS_GroveCount] == null then
        return
    endif
    set KLS_GroveCount = KLS_GroveCount+1
endfunction

function KLS_EnemySummoned takes nothing returns nothing
    local unit u = GetSummonedUnit()
    if GetOwningPlayer(u) == Player(11) and not KLS_Ended and not IsUnitInGroup(u,KLS_Enemies) then
        call GroupAddUnit(KLS_Enemies,u)
        set KLS_Alive = KLS_Alive+1
        call IssuePointOrder(u,"attack",0,350)
    endif
    set u = null
endfunction

function KLS_PoolTick takes nothing returns nothing
    local integer p = 0
    local unit hero
    local real maxHP
    local real maxMana
    if KLS_Ended then
        call PauseTimer(KLS_PoolClock)
        return
    endif
    loop
        exitwhen p == 4
        set hero = KLS_Hero[p]
        if KLS_Active[p] and hero != null and GetWidgetLife(hero) > 0.405 and IsUnitInRangeXY(hero,-900,-1600,450.0) then
            set maxHP = BlzGetUnitMaxHP(hero)
            set maxMana = GetUnitState(hero,UNIT_STATE_MAX_MANA)
            if GetWidgetLife(hero) < maxHP or GetUnitState(hero,UNIT_STATE_MANA) < maxMana then
                call SetWidgetLife(hero,RMinBJ(maxHP,GetWidgetLife(hero)+maxHP*0.01))
                call SetUnitState(hero,UNIT_STATE_MANA,RMinBJ(maxMana,GetUnitState(hero,UNIT_STATE_MANA)+maxMana*0.01))
            endif
        endif
        set p = p+1
    endloop
    set hero = null
endfunction

function KLS_WaveEnvironmentInit takes nothing returns nothing
    local real y = 900
    local trigger summoned = CreateTrigger()
    call TriggerRegisterAnyUnitEventBJ(summoned,EVENT_PLAYER_UNIT_SUMMON)
    call TriggerAddAction(summoned,function KLS_EnemySummoned)
    set summoned = null
    call KLS_WaveRosterInit()
    // Thirty trees in small reachable groves, outside the central lane and plots.
    loop
        exitwhen y > 4500 or KLS_Ended
        call KLS_GrovePlant(-850,y)
        call KLS_GrovePlant(-1030,y)
        call KLS_GrovePlant(-940,y+160)
        call KLS_GrovePlant(850,y)
        call KLS_GrovePlant(1030,y)
        call KLS_GrovePlant(940,y+160)
        set y = y+900
    endloop
    if KLS_Ended then
        return
    endif
    // This visual prop is optional: its failure must not abort the match or
    // disable the coordinate-based restoration trigger.
    set KLS_RestorePool = CreateUnit(Player(PLAYER_NEUTRAL_PASSIVE),'nfoh',-900,-1600,270)
    if KLS_RestorePool != null then
        if GetUnitTypeId(KLS_RestorePool) == 'nfoh' then
            call BlzSetUnitName(KLS_RestorePool,"King's Restoring Spring")
            call SetUnitInvulnerable(KLS_RestorePool,true)
            call SetUnitPathing(KLS_RestorePool,false)
        else
            call KLS_Log("ERROR restoring spring expected nfoh but received type="+I2S(GetUnitTypeId(KLS_RestorePool)))
            call RemoveUnit(KLS_RestorePool)
            set KLS_RestorePool = null
        endif
    else
        // The restorative trigger is coordinate-based, so it can still work
        // if the visual fountain model cannot be created in this game build.
        call KLS_Log("ERROR restoring spring model unavailable; healing trigger retained at -900,-1600")
    endif
    set KLS_PoolClock = CreateTimer()
    call TimerStart(KLS_PoolClock,1.0,true,function KLS_PoolTick)
    set KLS_GroveClock = CreateTimer()
    call TimerStart(KLS_GroveClock,1,true,function KLS_GroveTick)
    call KLS_Log("30 combat-grove trees planted; King's Restoring Spring quietly restores 1% of maximum health and mana every second. Mixed wave rosters initialized.")
endfunction
