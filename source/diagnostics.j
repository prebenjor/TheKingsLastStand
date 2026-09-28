globals
    string array KLS_DiagLines
    integer KLS_DiagCount = 0
    integer KLS_DiagUnits = 0
    integer KLS_DiagDestructables = 0
    integer KLS_DiagFailures = 0
endglobals

function KLS_RaceName takes integer raceId returns string
    if raceId == 0 then
        return "Human"
    elseif raceId == 1 then
        return "Orc"
    elseif raceId == 2 then
        return "Night Elf"
    endif
    return "Undead"
endfunction

function KLS_Log takes string message returns nothing
    if not KLS_Debug then
        return
    endif
    set KLS_DiagLines[ModuloInteger(KLS_DiagCount, 64)] = "[KLS_BUILD_ID] " + message
    set KLS_DiagCount = KLS_DiagCount + 1
endfunction

function KLS_AbortForSpawnFailure takes string context, integer kind returns nothing
    local integer p = 0
    if KLS_Ended then
        return
    endif
    set KLS_Ended = true
    set KLS_Won = false
    call KLS_Log("FATAL spawn failed context=" + context + " type=" + I2S(kind))
    call DisplayTimedTextToForce(bj_FORCE_ALL_PLAYERS, 8.0, "|cffff3333MAP ERROR: required object failed to spawn (" + context + "). The diagnostic match is stopping; type -diag.|r")
    if KLS_Clock != null then
        call PauseTimer(KLS_Clock)
    endif
    if KLS_GroveClock != null then
        call PauseTimer(KLS_GroveClock)
    endif
    if KLS_PoolClock != null then
        call PauseTimer(KLS_PoolClock)
    endif
    loop
        exitwhen p == 4
        if KLS_Active[p] or (GetPlayerSlotState(Player(p)) == PLAYER_SLOT_STATE_PLAYING and GetPlayerController(Player(p)) == MAP_CONTROL_USER) then
            call CustomDefeatBJ(Player(p), "A required map object failed to spawn in " + context + ". Type -diag for details.")
        endif
        set p = p + 1
    endloop
endfunction

function KLS_CreateUnitChecked takes player owner, integer kind, real x, real y, real facing, boolean fatal, string context returns unit
    local unit u
    if KLS_Ended then
        return null
    endif
    set u = CreateUnit(owner, kind, x, y, facing)
    if u == null then
        if KLS_Debug then
            set KLS_DiagUnits = KLS_DiagUnits + 1
            set KLS_DiagFailures = KLS_DiagFailures + 1
            if fatal then
                call KLS_Log("ERROR required unit spawn failed context="+context+" name="+GetObjectName(kind)+" type="+I2S(kind)+" owner="+I2S(GetPlayerId(owner))+" at "+R2S(x)+","+R2S(y))
            else
                call KLS_Log("ERROR optional unit spawn failed context="+context+" name="+GetObjectName(kind)+" type="+I2S(kind)+" owner="+I2S(GetPlayerId(owner))+" at "+R2S(x)+","+R2S(y))
            endif
        endif
        if fatal then
            call KLS_AbortForSpawnFailure(context, kind)
        endif
        return null
    endif
    if GetUnitTypeId(u) != kind then
        if KLS_Debug then
            set KLS_DiagUnits = KLS_DiagUnits + 1
            set KLS_DiagFailures = KLS_DiagFailures + 1
            if fatal then
                call KLS_Log("ERROR required unit has wrong type context="+context+" name="+GetObjectName(kind)+" expected="+I2S(kind)+" actual="+I2S(GetUnitTypeId(u))+" at "+R2S(x)+","+R2S(y))
            else
                call KLS_Log("ERROR optional unit has wrong type context="+context+" name="+GetObjectName(kind)+" expected="+I2S(kind)+" actual="+I2S(GetUnitTypeId(u))+" at "+R2S(x)+","+R2S(y))
            endif
        endif
        call RemoveUnit(u)
        if fatal then
            call KLS_AbortForSpawnFailure(context, kind)
        endif
        return null
    endif
    if KLS_Debug then
        set KLS_DiagUnits = KLS_DiagUnits + 1
        if RAbsBJ(GetUnitX(u) - x) > 256 or RAbsBJ(GetUnitY(u) - y) > 256 then
            call KLS_Log("WARN displaced " + GetUnitName(u) + " requested=" + R2S(x) + "," + R2S(y) + " actual=" + R2S(GetUnitX(u)) + "," + R2S(GetUnitY(u)))
        endif
    endif
    return u
endfunction

function KLS_CreateUnit takes player owner, integer kind, real x, real y, real facing returns unit
    return KLS_CreateUnitChecked(owner,kind,x,y,facing,true,"required unit")
endfunction

function KLS_CreateUnitOptional takes player owner, integer kind, real x, real y, real facing, string context returns unit
    return KLS_CreateUnitChecked(owner,kind,x,y,facing,false,context)
endfunction

function KLS_CreateDestructableChecked takes integer kind, real x, real y, real facing, real scale, integer variation, boolean fatal, string context returns destructable
    local destructable d
    if KLS_Ended then
        return null
    endif
    set d = CreateDestructable(kind, x, y, facing, scale, variation)
    if d == null then
        if KLS_Debug then
            set KLS_DiagDestructables = KLS_DiagDestructables + 1
            set KLS_DiagFailures = KLS_DiagFailures + 1
            if fatal then
                call KLS_Log("ERROR required destructable spawn failed context="+context+" name="+GetObjectName(kind)+" type="+I2S(kind)+" at "+R2S(x)+","+R2S(y))
            else
                call KLS_Log("ERROR optional destructable spawn failed context="+context+" name="+GetObjectName(kind)+" type="+I2S(kind)+" at "+R2S(x)+","+R2S(y))
            endif
        endif
        if fatal then
            call KLS_AbortForSpawnFailure(context, kind)
        endif
        return null
    endif
    if GetDestructableTypeId(d) != kind then
        if KLS_Debug then
            set KLS_DiagDestructables = KLS_DiagDestructables + 1
            set KLS_DiagFailures = KLS_DiagFailures + 1
            if fatal then
                call KLS_Log("ERROR required destructable has wrong type context="+context+" name="+GetObjectName(kind)+" expected="+I2S(kind)+" actual="+I2S(GetDestructableTypeId(d))+" at "+R2S(x)+","+R2S(y))
            else
                call KLS_Log("ERROR optional destructable has wrong type context="+context+" name="+GetObjectName(kind)+" expected="+I2S(kind)+" actual="+I2S(GetDestructableTypeId(d))+" at "+R2S(x)+","+R2S(y))
            endif
        endif
        call RemoveDestructable(d)
        if fatal then
            call KLS_AbortForSpawnFailure(context, kind)
        endif
        return null
    endif
    if KLS_Debug then
        set KLS_DiagDestructables = KLS_DiagDestructables + 1
    endif
    return d
endfunction

function KLS_CreateDestructable takes integer kind, real x, real y, real facing, real scale, integer variation returns destructable
    return KLS_CreateDestructableChecked(kind,x,y,facing,scale,variation,true,"required destructable")
endfunction

function KLS_CreateDestructableOptional takes integer kind, real x, real y, real facing, real scale, integer variation, string context returns destructable
    return KLS_CreateDestructableChecked(kind,x,y,facing,scale,variation,false,context)
endfunction

function KLS_ShowDiagnostics takes player p returns nothing
    local integer n = IMaxBJ(0, KLS_DiagCount - 12)
    local integer i = 0
    local string raceName
    if not KLS_Debug then
        return
    endif
    call DisplayTimedTextToPlayer(p, 0, 0, 30, "KLS_BUILD_ID | units attempted=" + I2S(KLS_DiagUnits) + " scenery attempted=" + I2S(KLS_DiagDestructables) + " failures=" + I2S(KLS_DiagFailures))
    loop
        exitwhen i == 4
        if KLS_Active[i] then
            set raceName = KLS_RaceName(KLS_PlayerRace[i])
            if KLS_FirstWorker[i] != null then
                call DisplayTimedTextToPlayer(p, 0, 0, 30, "Identity check player=" + I2S(i+1) + " race=" + raceName + " worker=" + GetObjectName(GetUnitTypeId(KLS_FirstWorker[i])) + " unit=" + GetUnitName(KLS_FirstWorker[i]))
            else
                call DisplayTimedTextToPlayer(p, 0, 0, 30, "Identity check player=" + I2S(i+1) + " race=" + raceName + " worker=NOT CREATED")
            endif
        endif
        set i = i + 1
    endloop
    loop
        exitwhen n >= KLS_DiagCount
        call DisplayTimedTextToPlayer(p, 0, 0, 30, KLS_DiagLines[ModuloInteger(n, 64)])
        set n = n + 1
    endloop
endfunction
