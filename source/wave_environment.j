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
    set KLS_GroveTree[KLS_GroveCount] = KLS_CreateDestructable('LTlt',x,y,0,1,0)
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
    if KLS_Ended then
        call PauseTimer(KLS_PoolClock)
        return
    endif
    loop
        exitwhen p == 4
        set hero = KLS_Hero[p]
        if KLS_Active[p] and hero != null and GetWidgetLife(hero) > 0.405 and IsUnitInRangeXY(hero,-900,-1600,450.0) then
            call SetWidgetLife(hero,RMinBJ(BlzGetUnitMaxHP(hero),GetWidgetLife(hero)+200.0))
            call SetUnitState(hero,UNIT_STATE_MANA,RMinBJ(GetUnitState(hero,UNIT_STATE_MAX_MANA),GetUnitState(hero,UNIT_STATE_MANA)+120.0))
            call DestroyEffect(AddSpecialEffectTarget("Abilities\\Spells\\Human\\HolyBolt\\HolyBoltSpecialArt.mdl",hero,"origin"))
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
    set KLS_RestorePool = KLS_CreateUnit(Player(PLAYER_NEUTRAL_PASSIVE),'nfoh',-900,-1600,270)
    if KLS_RestorePool == null then
        return
    endif
    call BlzSetUnitName(KLS_RestorePool,"King's Restoring Spring")
    call SetUnitInvulnerable(KLS_RestorePool,true)
    call SetUnitPathing(KLS_RestorePool,false)
    set KLS_PoolClock = CreateTimer()
    call TimerStart(KLS_PoolClock,5.0,true,function KLS_PoolTick)
    set KLS_GroveClock = CreateTimer()
    call TimerStart(KLS_GroveClock,1,true,function KLS_GroveTick)
    call KLS_Log("30 combat-grove trees planted; King's Restoring Spring at -900,-1600 pulses every 5 seconds. Mixed wave rosters initialized.")
endfunction
