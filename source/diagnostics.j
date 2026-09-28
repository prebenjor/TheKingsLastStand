globals
    string array KLS_DiagLines
    integer KLS_DiagCount = 0
    integer KLS_DiagUnits = 0
    integer KLS_DiagDestructables = 0
    integer KLS_DiagFailures = 0
endglobals

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

function KLS_CreateUnit takes player owner, integer kind, real x, real y, real facing returns unit
    local unit u
    if KLS_Ended then
        return null
    endif
    set u = CreateUnit(owner, kind, x, y, facing)
    if u == null then
        if KLS_Debug then
            set KLS_DiagUnits = KLS_DiagUnits + 1
            set KLS_DiagFailures = KLS_DiagFailures + 1
            call KLS_Log("ERROR unit creation name=" + GetObjectName(kind) + " type=" + I2S(kind) + " owner=" + I2S(GetPlayerId(owner)) + " at " + R2S(x) + "," + R2S(y))
        endif
        call KLS_AbortForSpawnFailure("unit", kind)
        return null
    endif
    if GetUnitTypeId(u) != kind then
        if KLS_Debug then
            set KLS_DiagUnits = KLS_DiagUnits + 1
            set KLS_DiagFailures = KLS_DiagFailures + 1
            call KLS_Log("ERROR wrong unit type created name=" + GetObjectName(kind) + " type=" + I2S(kind) + " actual=" + I2S(GetUnitTypeId(u)))
        endif
        call KLS_AbortForSpawnFailure("wrong unit type", kind)
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

function KLS_CreateDestructable takes integer kind, real x, real y, real facing, real scale, integer variation returns destructable
    local destructable d
    if KLS_Ended then
        return null
    endif
    set d = CreateDestructable(kind, x, y, facing, scale, variation)
    if d == null then
        if KLS_Debug then
            set KLS_DiagDestructables = KLS_DiagDestructables + 1
            set KLS_DiagFailures = KLS_DiagFailures + 1
            call KLS_Log("ERROR destructable creation name=" + GetObjectName(kind) + " type=" + I2S(kind) + " at " + R2S(x) + "," + R2S(y))
        endif
        call KLS_AbortForSpawnFailure("destructable", kind)
        return null
    endif
    if GetDestructableTypeId(d) != kind then
        if KLS_Debug then
            set KLS_DiagDestructables = KLS_DiagDestructables + 1
            set KLS_DiagFailures = KLS_DiagFailures + 1
            call KLS_Log("ERROR wrong destructable type created name=" + GetObjectName(kind) + " type=" + I2S(kind) + " actual=" + I2S(GetDestructableTypeId(d)))
        endif
        call KLS_AbortForSpawnFailure("wrong destructable type", kind)
        return null
    endif
    if KLS_Debug then
        set KLS_DiagDestructables = KLS_DiagDestructables + 1
    endif
    return d
endfunction

function KLS_ShowDiagnostics takes player p returns nothing
    local integer n = IMaxBJ(0, KLS_DiagCount - 12)
    if not KLS_Debug then
        return
    endif
    call DisplayTimedTextToPlayer(p, 0, 0, 30, "KLS_BUILD_ID | units attempted=" + I2S(KLS_DiagUnits) + " scenery attempted=" + I2S(KLS_DiagDestructables) + " failures=" + I2S(KLS_DiagFailures))
    loop
        exitwhen n >= KLS_DiagCount
        call DisplayTimedTextToPlayer(p, 0, 0, 30, KLS_DiagLines[ModuloInteger(n, 64)])
        set n = n + 1
    endloop
endfunction
