// Shared synchronized match-rule helpers. The arrays and locked values remain
// in game.j; this module is first because JASS requires definitions before calls.
globals
endglobals

function KLS_DifficultyName takes integer choice returns string
    if choice == 0 then
        return "Easy"
    elseif choice == 2 then
        return "Hard"
    elseif choice == 3 then
        return "Very Hard"
    endif
    return "Normal"
endfunction

function KLS_DifficultyHealthScale takes nothing returns real
    if KLS_Difficulty == 0 then
        return 0.75
    elseif KLS_Difficulty == 2 then
        return 1.30
    elseif KLS_Difficulty == 3 then
        return 1.60
    endif
    return 1.0
endfunction

function KLS_DifficultyDamageScale takes nothing returns real
    if KLS_Difficulty == 0 then
        return 0.80
    elseif KLS_Difficulty == 2 then
        return 1.20
    elseif KLS_Difficulty == 3 then
        return 1.40
    endif
    return 1.0
endfunction

function KLS_DifficultyCountScale takes nothing returns real
    if KLS_Difficulty == 0 then
        return 0.90
    elseif KLS_Difficulty == 2 then
        return 1.10
    elseif KLS_Difficulty == 3 then
        return 1.20
    endif
    return 1.0
endfunction

function KLS_DifficultyScaledCount takes integer baseCount returns integer
    return IMaxBJ(1,R2I(I2R(baseCount)*KLS_DifficultyCountScale()+0.5))
endfunction

function KLS_DifficultyVoteTally takes integer choice returns integer
    local integer p = 0
    local integer count = 0
    loop
        exitwhen p == 4
        if KLS_Active[p] and KLS_DifficultyVote[p] == choice then
            set count = count+1
        endif
        set p = p+1
    endloop
    return count
endfunction

function KLS_DifficultyTallyText takes nothing returns string
    return "Easy "+I2S(KLS_DifficultyVoteTally(0))+" | Normal "+I2S(KLS_DifficultyVoteTally(1))+" | Hard "+I2S(KLS_DifficultyVoteTally(2))+" | Very Hard "+I2S(KLS_DifficultyVoteTally(3))
endfunction

function KLS_LockDifficulty takes nothing returns nothing
    local integer choice = 0
    local integer best = 0
    local integer votes = 0
    local boolean tied = false
    if KLS_DifficultyLocked then
        return
    endif
    loop
        exitwhen choice == 4
        set votes = KLS_DifficultyVoteTally(choice)
        if votes > best then
            set best = votes
            set KLS_Difficulty = choice
            set tied = false
        elseif votes > 0 and votes == best then
            set tied = true
        endif
        set choice = choice+1
    endloop
    if best == 0 or tied then
        set KLS_Difficulty = 1
    endif
    set KLS_DifficultyLocked = true
    call DisplayTimedTextToForce(bj_FORCE_ALL_PLAYERS,8.0,"Difficulty set to "+KLS_DifficultyName(KLS_Difficulty)+".")
endfunction

function KLS_ReadyCount takes nothing returns integer
    local integer p = 0
    local integer count = 0
    loop
        exitwhen p == 4
        if KLS_Active[p] and KLS_ReadyVote[p] then
            set count = count+1
        endif
        set p = p+1
    endloop
    return count
endfunction

function KLS_ResetReadyVotes takes nothing returns nothing
    local integer p = 0
    set KLS_ReadyEpoch = KLS_ReadyEpoch+1
    loop
        exitwhen p == 4
        set KLS_ReadyVote[p] = false
        set p = p+1
    endloop
endfunction
