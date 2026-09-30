// The King's Last Stand: native JASS development runtime.
globals
    // GENERATED_LAYOUT_GLOBALS
    unit KLS_King = null
    unit array KLS_Hero
    unit array KLS_FirstWorker
    unit array KLS_BaseTownHall
    rect array KLS_Plot
    real array KLS_X
    real array KLS_Y
    boolean array KLS_Active
    integer KLS_Players = 0
    integer KLS_Wave = 0
    integer KLS_Alive = 0
    integer KLS_Prep = 45
    integer KLS_NormalPrep = 50
    integer KLS_BossPrep = 180
    integer KLS_XPShareRange = 1200
    boolean KLS_Ended = false
    integer KLS_Difficulty = 1
    boolean KLS_DifficultyLocked = false
    integer array KLS_DifficultyVote
    integer KLS_ReadyEpoch = 0
    boolean array KLS_ReadyVote
    framehandle array KLS_DifficultyButton
    framehandle array KLS_ReadyButton
    framehandle array KLS_DifficultyTitle
    timer KLS_VoteUITimer = null
    timer KLS_Clock = null
    group KLS_Enemies = null
    integer array KLS_Respawn
    integer KLS_KingTier = 0
    integer KLS_Seconds = 0
endglobals

function KLS_Message takes string s returns nothing
    call DisplayTimedTextToForce(bj_FORCE_ALL_PLAYERS, 8.0, s)
endfunction

function KLS_DifficultyVoteSync takes nothing returns nothing
    local integer p = GetPlayerId(GetTriggerPlayer())
    local integer choice = S2I(BlzGetTriggerSyncData())
    if p < 0 or p >= 4 or not KLS_Active[p] or not KLS_Selecting or KLS_DifficultyLocked then
        return
    endif
    if choice < 0 or choice > 3 then
        return
    endif
    set KLS_DifficultyVote[p] = choice
    call KLS_Log("Difficulty vote player="+I2S(p+1)+" choice="+KLS_DifficultyName(choice))
    call KLS_HUDUpdate()
endfunction

function KLS_DifficultyClick takes nothing returns nothing
    local integer p = GetPlayerId(GetTriggerPlayer())
    local integer choice = 0
    local framehandle clicked = BlzGetTriggerFrame()
    if p >= 0 and p < 4 and GetLocalPlayer() == GetTriggerPlayer() then
        loop
            exitwhen choice == 4
            if clicked == KLS_DifficultyButton[p*4+choice] then
                call BlzSendSyncData("KLSDIFF",I2S(choice))
                exitwhen true
            endif
            set choice = choice+1
        endloop
    endif
    set clicked = null
endfunction

function KLS_ReadyClick takes nothing returns nothing
    local integer p = GetPlayerId(GetTriggerPlayer())
    local framehandle clicked = BlzGetTriggerFrame()
    if p >= 0 and p < 4 and GetLocalPlayer() == GetTriggerPlayer() and clicked == KLS_ReadyButton[p] then
        if KLS_ReadyVote[p] then
            call BlzSendSyncData("KLSREADY",I2S(KLS_ReadyEpoch)+":0")
        else
            call BlzSendSyncData("KLSREADY",I2S(KLS_ReadyEpoch)+":1")
        endif
    endif
    set clicked = null
endfunction

function KLS_VoteUIRefresh takes nothing returns nothing
    local integer p = GetPlayerId(GetLocalPlayer())
    local integer choice = 0
    local boolean showReady
    if p < 0 or p >= 4 or not KLS_Active[p] then
        return
    endif
    if GetLocalPlayer() == Player(p) and KLS_DifficultyTitle[p] != null then
        call BlzFrameSetVisible(KLS_DifficultyTitle[p],KLS_Selecting and not KLS_DifficultyLocked)
        call BlzFrameSetText(KLS_DifficultyTitle[p],"Choose difficulty: "+KLS_DifficultyTallyText())
        loop
            exitwhen choice == 4
            call BlzFrameSetVisible(KLS_DifficultyButton[p*4+choice],KLS_Selecting and not KLS_DifficultyLocked)
            if KLS_DifficultyVote[p] == choice then
                call BlzFrameSetText(KLS_DifficultyButton[p*4+choice],"> "+KLS_DifficultyName(choice)+" <")
            else
                call BlzFrameSetText(KLS_DifficultyButton[p*4+choice],KLS_DifficultyName(choice))
            endif
            set choice = choice+1
        endloop
        set showReady = not KLS_Selecting and not KLS_Ended and KLS_Alive == 0 and KLS_Prep > 0
        call BlzFrameSetVisible(KLS_ReadyButton[p],showReady)
        if KLS_ReadyVote[p] then
            call BlzFrameSetText(KLS_ReadyButton[p],"Ready! "+I2S(KLS_ReadyCount())+"/"+I2S(KLS_Players)+" (click to undo)")
        else
            call BlzFrameSetText(KLS_ReadyButton[p],"Start next wave "+I2S(KLS_ReadyCount())+"/"+I2S(KLS_Players))
        endif
    endif
endfunction

function KLS_VoteUICreateButton takes string name, string label, framehandle parent, framepointtype point, real x, real y, real width returns framehandle
    local framehandle choiceFrame = BlzCreateFrameByType("GLUETEXTBUTTON",name,parent,"ScriptDialogButton",0)
    call BlzFrameSetSize(choiceFrame,width,0.032)
    call BlzFrameSetText(choiceFrame,label)
    call BlzFrameSetPoint(choiceFrame,point,parent,point,x,y)
    call BlzFrameSetVisible(choiceFrame,false)
    set parent = null
    return choiceFrame
endfunction

function KLS_GoldToast takes integer p, integer amount returns nothing
    local texttag rewardTag
    if p >= 0 and p < 4 and amount > 0 then
        // The timed message can be lost among simultaneous wave text. Add a
        // recipient-only combat number above that player's hero as well.
        set rewardTag = CreateTextTag()
        call SetTextTagText(rewardTag, "+"+I2S(amount)+" gold", 0.020)
        call SetTextTagColor(rewardTag,255,214,64,255)
        if KLS_Hero[p] != null then
            call SetTextTagPosUnit(rewardTag,KLS_Hero[p],65.0)
        else
            call SetTextTagPos(rewardTag,0,0,0)
        endif
        call SetTextTagVelocity(rewardTag,0,0.028)
        call SetTextTagPermanent(rewardTag,false)
        call SetTextTagLifespan(rewardTag,2.5)
        call SetTextTagFadepoint(rewardTag,1.8)
        if GetLocalPlayer() != Player(p) then
            call SetTextTagVisibility(rewardTag,false)
        endif
        call DisplayTimedTextToPlayer(Player(p),0,0.22,2.5,"|cffffcc00+"+I2S(amount)+" gold|r")
    endif
    set rewardTag = null
endfunction

function KLS_End takes boolean won returns nothing
    local integer i = 0
    if KLS_Ended then
        return
    endif
    set KLS_Ended = true
    set KLS_Won = won
    call KLS_Log("Match ended at wave " + I2S(KLS_Wave))
    call KLS_HUDUpdate()
    call PauseTimer(KLS_Clock)
    loop
        exitwhen i == 4
        if KLS_Active[i] then
            if won then
                call CustomVictoryBJ(Player(i), true, true)
            else
                call CustomDefeatBJ(Player(i), "The king has fallen.")
            endif
        endif
        set i = i + 1
    endloop
endfunction

function KLS_BossReward takes nothing returns nothing
    local integer i = 0
    local integer gear
    if KLS_Wave == 10 then
        set gear = 'I010'
    elseif KLS_Wave == 20 then
        set gear = 'I011'
    elseif KLS_Wave == 30 then
        set gear = 'I012'
    elseif KLS_Wave == 40 then
        set gear = 'I013'
    elseif KLS_Wave >= 40 then
        set gear = KLS_RandomCatalogDrop(4)
    elseif KLS_Wave >= 30 then
        set gear = KLS_RandomCatalogDrop(3)
    elseif KLS_Wave >= 20 then
        set gear = KLS_RandomCatalogDrop(2)
    else
        set gear = KLS_RandomCatalogDrop(1)
    endif
    loop
        exitwhen i == 4
        if KLS_Active[i] then
            call SetPlayerState(Player(i), PLAYER_STATE_RESOURCE_GOLD, GetPlayerState(Player(i), PLAYER_STATE_RESOURCE_GOLD) + 250 + KLS_Wave * 10)
            call KLS_GoldToast(i,250 + KLS_Wave * 10)
            call KLS_PersonalRewardEnqueue(i,gear,"Boss")
        endif
        set i = i + 1
    endloop
endfunction

function KLS_AwardBounty takes unit killer, integer bounty returns nothing
    local integer i = 0
    local integer p = -1
    local integer payout = 0
    if KLS_Ended or killer == null or bounty <= 0 then
        return
    endif
    if killer == KLS_King then
        set payout = R2I(I2R(bounty)*0.25)
        if payout < 1 then
            set payout = 1
        endif
        loop
            exitwhen i == 4
            if KLS_Active[i] then
                call SetPlayerState(Player(i),PLAYER_STATE_RESOURCE_GOLD,GetPlayerState(Player(i),PLAYER_STATE_RESOURCE_GOLD)+payout)
                call KLS_GoldToast(i,payout)
            endif
            set i = i+1
        endloop
        call KLS_Log("King Aldric kill bounty: each active defender receives 25 percent")
    else
        set p = GetPlayerId(GetOwningPlayer(killer))
        if p >= 0 and p < 4 and KLS_Active[p] then
            call SetPlayerState(Player(p),PLAYER_STATE_RESOURCE_GOLD,GetPlayerState(Player(p),PLAYER_STATE_RESOURCE_GOLD)+bounty)
            call KLS_GoldToast(p,bounty)
        endif
    endif
endfunction

function KLS_UnitKillXP takes unit dead returns integer
    local integer level = GetUnitLevel(dead)
    local integer xp = 25
    if level <= 0 then
        return 0
    endif
    if IsUnitType(dead,UNIT_TYPE_HERO) then
        if level <= 1 then
            return 100
        elseif level == 2 then
            return 120
        elseif level == 3 then
            return 160
        elseif level == 4 then
            return 220
        elseif level == 5 then
            return 300
        elseif level == 6 then
            return 400
        elseif level == 7 then
            return 500
        elseif level == 8 then
            return 600
        elseif level == 9 then
            return 700
        endif
        return 800
    endif
    // Warcraft's default normal-unit XP sequence: F(1)=25,
    // F(x)=F(x-1)+5*x+5. Native kill XP is disabled in Misc.txt below.
    set level = level - 1
    loop
        exitwhen level <= 0
        set xp = xp + 5*level + 5
        set level = level - 1
    endloop
    return xp
endfunction

function KLS_AwardKillXP takes unit dead returns nothing
    local integer i = 0
    local integer xp = KLS_UnitKillXP(dead)
    local unit hero
    local real dx
    local real dy
    if xp > 0 then
        loop
            exitwhen i == 4
            set hero = KLS_Hero[i]
            // Intentionally do not require a living unit or a specific race:
            // an active player's nearby hero receives the full award.
            if KLS_Active[i] and hero != null then
                set dx = GetUnitX(hero)-GetUnitX(dead)
                set dy = GetUnitY(hero)-GetUnitY(dead)
                if dx*dx+dy*dy <= I2R(KLS_XPShareRange*KLS_XPShareRange) then
                    call AddHeroXP(hero,xp,false)
                endif
            endif
            set i = i + 1
        endloop
    endif
    set hero = null
endfunction

function KLS_Death takes nothing returns nothing
    local unit dead = GetTriggerUnit()
    local integer i = 0
    if KLS_Ended then
        return
    endif
    if dead == KLS_King then
        call KLS_End(false)
    elseif dead == KLS_StoryCart then
        call KLS_StoryEscortFailed()
    elseif IsUnitInGroup(dead,KLS_StoryEnemies) then
        call KLS_StoryEnemyKilled(dead)
    elseif IsUnitInGroup(dead, KLS_Enemies) then
        call GroupRemoveUnit(KLS_Enemies, dead)
        set KLS_Alive = KLS_Alive - 1
        call KLS_AwardKillXP(dead)
        call KLS_AwardBounty(GetKillingUnit(),KLS_EnemyBounty(dead))
        call KLS_EnemyDrop(dead,dead == KLS_Boss)
        if dead == KLS_Boss then
            set KLS_Boss = null
            if GetWidgetLife(KLS_King) <= 0.405 then
                call KLS_End(false)
            else
                call KLS_BossReward()
                call KLS_Message("Boss defeated! Clear the remaining enemies.")
            endif
        endif
        if not KLS_Ended and KLS_Alive == 0 then
            call KLS_ResetReadyVotes()
            if ModuloInteger(KLS_Wave + 1, 10) == 0 then
                set KLS_Prep = KLS_BossPrep
            else
                set KLS_Prep = KLS_NormalPrep
            endif
            call KLS_Message("Wave cleared. " + I2S(KLS_Prep) + " seconds to prepare for the next assault.")
        endif
    else
        loop
            exitwhen i == 4
            if dead == KLS_Hero[i] then
                set KLS_Respawn[i] = 20
            endif
            set i = i + 1
        endloop
    endif
    set dead = null
endfunction

function KLS_Spawn takes nothing returns nothing
    local integer count = 0
    local integer n = 0
    local integer rosterWave = 1
    local integer kind = 'ugho'
    local unit u
    local real hp
    local boolean spawnFailed = false
    if KLS_Ended or KLS_Selecting or KLS_Alive > 0 then
        return
    endif
    set KLS_Prep = 0
    call KLS_ResetReadyVotes()
    set KLS_Wave = KLS_Wave + 1
    call KLS_CompanyResearchRefresh()
    set KLS_Boss = null
    set KLS_BossCast = 0
    set KLS_BossMechanic = 0
    call KLS_Log("Wave spawn started: " + I2S(KLS_Wave)+" difficulty="+KLS_DifficultyName(KLS_Difficulty))
    set count = KLS_DifficultyScaledCount(7 + KLS_Wave * 2 + KLS_Players * 3)
    set rosterWave = KLS_RosterSourceWave(KLS_Wave)
    loop
        exitwhen n == count or spawnFailed or KLS_Ended
        set kind = KLS_Roster[rosterWave*20+ModuloInteger(n,KLS_RosterSize[rosterWave])]
        set u = KLS_CreateUnit(Player(11), kind, I2R(ModuloInteger(n, 5) - 2) * 140, 6200 + I2R(n / 5) * 40, 270)
        if u != null then
            set hp = (180 + KLS_Wave * 55 + KLS_Players * 35)*KLS_DifficultyHealthScale()
            call BlzSetUnitMaxHP(u, R2I(hp))
            call SetWidgetLife(u, hp)
            call BlzSetUnitBaseDamage(u, R2I(I2R(6 + KLS_Wave * 2)*KLS_DifficultyDamageScale()+0.5), 0)
            if kind == 'unec' then
                call IssueImmediateOrder(u, "raisedeadon")
            elseif kind == 'oshm' then
                call IssueImmediateOrder(u, "bloodluston")
            endif
            call SetUnitAcquireRange(u, 900)
            call GroupAddUnit(KLS_Enemies, u)
            call IssuePointOrder(u, "attack", 0, 350)
            set KLS_Alive = KLS_Alive + 1
        else
            set spawnFailed = true
            call KLS_AbortForSpawnFailure("wave enemy", kind)
        endif
        set n = n + 1
    endloop
    if not spawnFailed and not KLS_Ended and ModuloInteger(KLS_Wave, 10) == 0 then
        set kind = KLS_BossUnitForWave(KLS_Wave)
        set u = KLS_CreateUnit(Player(11), kind, 0, 6800, 270)
        if u != null then
            set KLS_Boss = u
            set KLS_BossMechanic = KLS_BossMechanicForWave(KLS_Wave)
            set KLS_BossCast = 0
            call SetHeroLevel(u, KLS_Wave / 2, false)
            set hp = KLS_Wave * 550 * (1 + KLS_Players * 0.3)*KLS_DifficultyHealthScale()
            call BlzSetUnitMaxHP(u, R2I(hp))
            call SetWidgetLife(u, hp)
            call BlzSetUnitBaseDamage(u, R2I(I2R(KLS_Wave * 5)*KLS_DifficultyDamageScale()+0.5), 0)
            call SetUnitScale(u, 1.6, 1.6, 1.6)
            call GroupAddUnit(KLS_Enemies, u)
            set KLS_Alive = KLS_Alive + 1
            call IssuePointOrder(u, "attack", 0, 350)
            call KLS_Message("|cffff4444BOSS WAVE " + I2S(KLS_Wave) + "!|r")
        else
            set spawnFailed = true
            call KLS_AbortForSpawnFailure("wave boss", kind)
        endif
    elseif not spawnFailed and not KLS_Ended then
        set KLS_Boss = null
        call KLS_Message("Mixed invasion wave " + I2S(KLS_Wave) + " is approaching.")
    endif
    set u = null
endfunction

function KLS_ReadyCheck takes nothing returns nothing
    if KLS_Ended or KLS_Selecting or KLS_Alive != 0 or KLS_Prep <= 0 or KLS_Players <= 0 then
        return
    endif
    if KLS_ReadyCount() >= KLS_Players then
        set KLS_Prep = 0
        call KLS_Log("Unanimous ready vote; starting wave "+I2S(KLS_Wave+1))
        call KLS_Spawn()
    endif
endfunction

function KLS_ReadyVoteSync takes nothing returns nothing
    local integer p = GetPlayerId(GetTriggerPlayer())
    local string payload = BlzGetTriggerSyncData()
    if p < 0 or p >= 4 or not KLS_Active[p] or KLS_Ended or KLS_Selecting or KLS_Alive != 0 or KLS_Prep <= 0 then
        return
    endif
    if payload == I2S(KLS_ReadyEpoch)+":1" then
        set KLS_ReadyVote[p] = true
    elseif payload == I2S(KLS_ReadyEpoch)+":0" then
        set KLS_ReadyVote[p] = false
    else
        return
    endif
    call KLS_Log("Wave ready vote player="+I2S(p+1)+" ready="+I2S(KLS_ReadyCount())+"/"+I2S(KLS_Players))
    call KLS_ReadyCheck()
    call KLS_HUDUpdate()
endfunction

function KLS_VoteUIInit takes nothing returns nothing
    local integer p = 0
    local integer choice = 0
    local trigger difficultyClicks = CreateTrigger()
    local trigger difficultySync = CreateTrigger()
    local trigger readyClicks = CreateTrigger()
    local trigger readySync = CreateTrigger()
    local framehandle gameUI
    local real x
    loop
        exitwhen p == 4
        call BlzTriggerRegisterPlayerSyncEvent(difficultySync,Player(p),"KLSDIFF",false)
        call BlzTriggerRegisterPlayerSyncEvent(readySync,Player(p),"KLSREADY",false)
        // Allocate frames and event handles in the same order on every client.
        // Only KLS_VoteUIRefresh changes their visibility for the local owner.
        if KLS_Active[p] then
            set gameUI = BlzGetOriginFrame(ORIGIN_FRAME_GAME_UI,0)
            set KLS_DifficultyTitle[p] = BlzCreateFrameByType("TEXT","KLSDifficultyTitle",gameUI,"",0)
            call BlzFrameSetSize(KLS_DifficultyTitle[p],0.55,0.024)
            call BlzFrameSetPoint(KLS_DifficultyTitle[p],FRAMEPOINT_TOP,gameUI,FRAMEPOINT_TOP,0.0,-0.008)
            call BlzFrameSetVisible(KLS_DifficultyTitle[p],false)
            set choice = 0
            loop
                exitwhen choice == 4
                set x = -0.15+I2R(choice)*0.10
                set KLS_DifficultyButton[p*4+choice] = KLS_VoteUICreateButton("KLSDifficulty"+I2S(choice),KLS_DifficultyName(choice),gameUI,FRAMEPOINT_TOP,x,-0.036,0.09)
                call BlzTriggerRegisterFrameEvent(difficultyClicks,KLS_DifficultyButton[p*4+choice],FRAMEEVENT_CONTROL_CLICK)
                set choice = choice+1
            endloop
            set KLS_ReadyButton[p] = KLS_VoteUICreateButton("KLSReadyWave","Start next wave",gameUI,FRAMEPOINT_TOP,0.0,-0.014,0.20)
            call BlzTriggerRegisterFrameEvent(readyClicks,KLS_ReadyButton[p],FRAMEEVENT_CONTROL_CLICK)
            set gameUI = null
        endif
        set p = p+1
    endloop
    call TriggerAddAction(difficultyClicks,function KLS_DifficultyClick)
    call TriggerAddAction(difficultySync,function KLS_DifficultyVoteSync)
    call TriggerAddAction(readyClicks,function KLS_ReadyClick)
    call TriggerAddAction(readySync,function KLS_ReadyVoteSync)
    set KLS_VoteUITimer = CreateTimer()
    call TimerStart(KLS_VoteUITimer,0.25,true,function KLS_VoteUIRefresh)
    set difficultyClicks = null
    set difficultySync = null
    set readyClicks = null
    set readySync = null
endfunction

function KLS_Reorder takes nothing returns nothing
    if GetUnitCurrentOrder(GetEnumUnit()) == 0 then
        call IssuePointOrder(GetEnumUnit(), "attack", 0, 350)
    endif
endfunction

function KLS_Tick takes nothing returns nothing
    local integer i = 0
    if KLS_Ended then
        return
    endif
    if KLS_Selecting then
        call KLS_SelectionTick()
        call KLS_HUDUpdate()
        return
    endif
    set KLS_Seconds = KLS_Seconds + 1
    call KLS_PersonalRewardTick()
    loop
        exitwhen i == 4
        if KLS_Respawn[i] > 0 then
            set KLS_Respawn[i] = KLS_Respawn[i] - 1
            if KLS_Respawn[i] == 0 then
                if KLS_Altar[i] != null and GetWidgetLife(KLS_Altar[i]) > 0.405 then
                    call ReviveHero(KLS_Hero[i], GetUnitX(KLS_Altar[i]), GetUnitY(KLS_Altar[i]) - 250, true)
                else
                    call ReviveHero(KLS_Hero[i], KLS_X[i], KLS_Y[i], true)
                endif
            endif
        endif
        set i = i + 1
    endloop
    if KLS_Alive == 0 then
        if KLS_Prep > 0 then
            set KLS_Prep = KLS_Prep - 1
            if KLS_Prep <= 0 then
                call KLS_ResetReadyVotes()
                call KLS_Spawn()
            endif
        endif
    elseif ModuloInteger(KLS_Seconds, 8) == 0 then
        call ForGroup(KLS_Enemies, function KLS_Reorder)
    endif
    call KLS_CombatTick()
    call KLS_HUDUpdate()
endfunction

function KLS_Construct takes nothing returns nothing
    local unit u = GetConstructingStructure()
    local integer i = GetPlayerId(GetOwningPlayer(u))
    if i < 4 and not RectContainsCoords(KLS_Plot[i], GetUnitX(u), GetUnitY(u)) then
        call IssueImmediateOrder(u, "cancel")
        call DisplayTimedTextToPlayer(Player(i), 0, 0, 6, "Build inside your marked personal plot. Keep the King's Road clear.")
    endif
    set u = null
endfunction

function KLS_DebugRemove takes nothing returns nothing
    call RemoveUnit(GetEnumUnit())
endfunction

function KLS_Chat takes nothing returns nothing
    local player p = GetTriggerPlayer()
    local integer i = GetPlayerId(p)
    local string s = GetEventPlayerChatString()
    local integer gold = GetPlayerState(p, PLAYER_STATE_RESOURCE_GOLD)
    local integer wood = GetPlayerState(p, PLAYER_STATE_RESOURCE_LUMBER)
    if s == "-diag" then
        call KLS_ShowDiagnostics(p)
        return
    elseif s == "-gear" then
        call KLS_ShowGearDiagnostics(p)
        return
    endif
    if KLS_Ended then
        return
    endif
    if s == "-repair" then
        call KLS_KingContribute(p,false,KLS_KingTier,false)
    elseif s == "-upgrade" then
        call KLS_KingContribute(p,true,KLS_KingTier,false)
    elseif (s == "-power" or s == "-vitality" or s == "-wisdom") and i >= 0 and i < 4 then
        call KLS_ProgressionShow(i)
    elseif s == "-gold" and KLS_Debug then
        call SetPlayerState(p, PLAYER_STATE_RESOURCE_GOLD, gold+5000)
        call SetPlayerState(p, PLAYER_STATE_RESOURCE_LUMBER, wood+5000)
    elseif SubString(s, 0, 6) == "-wave " and KLS_Debug then
        if S2I(SubString(s, 6, StringLength(s))) >= 1 and S2I(SubString(s, 6, StringLength(s))) <= 1000 then
            call ForGroup(KLS_Enemies, function KLS_DebugRemove)
            call GroupClear(KLS_Enemies)
            set KLS_Alive = 0
            set KLS_Wave = S2I(SubString(s, 6, StringLength(s)))-1
            call KLS_Spawn()
        endif
    elseif s == "-help" then
        call DisplayTimedTextToPlayer(p, 0, 0, 30, "Defend King Aldric through the 40-wave Crownlands campaign, then face endless crossover waves. The King's death ends the run. Development commands: -diag, -gear, -wave 1–1000. The optional Crownlands story remains separate from wave counts.")
    endif
    set p = null
endfunction

function KLS_AddTree takes real x, real y returns nothing
    local destructable tree = KLS_CreateDestructableOptional('LTlt', x, y, 0, 1.0, 0, "base harvest tree")
    if tree == null then
        return
    endif
    call SetDestructableMaxLife(tree, 1500)
    call SetDestructableLife(tree, 1500)
    set tree = null
endfunction

function KLS_BuildLandscape takes nothing returns nothing
    local real x = -7640
    local real y = -6500
    local integer i = 0
    local integer j = 0
    local destructable gate
    // Extend the existing gate runs to both map edges at unchanged spacing.
    // The stone gateway spans the northern approach while leaving a broad
    // permanent opening on the central road.
    loop
        exitwhen x > -1450
        set gate = KLS_CreateDestructable('LTg1', x, 5200, 0, 2.0, 0)
        if gate == null then
            return
        endif
        call SetDestructableInvulnerable(gate, true)
        set x = x + 620
    endloop
    set x = 1450
    loop
        exitwhen x > 7650
        set gate = KLS_CreateDestructable('LTg1', x, 5200, 0, 2.0, 0)
        if gate == null then
            return
        endif
        call SetDestructableInvulnerable(gate, true)
        set x = x + 620
    endloop
    call KLS_Log("Northern barrier: 10 left sections, 11 right sections; central opening unchanged")
    set gate = KLS_CreateDestructable('BTsk', -1250, 5200, 0, 1.5, 0)
    if gate == null then
        return
    endif
    call SetDestructableInvulnerable(gate, true)
    set gate = KLS_CreateDestructable('BTsk', 1250, 5200, 0, 1.5, 0)
    if gate == null then
        return
    endif
    call SetDestructableInvulnerable(gate, true)
    // Keep the entire playable area visibly green and frame it with harvestable
    // tree belts. The central gate opening stays clear.
    set x = -7800
    loop
        exitwhen x > 7800
        if x < -1800 or x > 1800 then
            call KLS_AddTree(x, 7600)
            if KLS_Ended then
                return
            endif
            call KLS_AddTree(x, 7200)
            if KLS_Ended then
                return
            endif
        endif
        set x = x + 400
    endloop
    loop
        exitwhen y > 6800
        call KLS_AddTree(-7800, y)
        if KLS_Ended then
            return
        endif
        call KLS_AddTree(7800, y)
        if KLS_Ended then
            return
        endif
        set y = y + 480
    endloop
    // Ground textures are authored in W3E (or generated by the fallback).
    // Keep resource stands, but never repaint edited player plot borders.
    loop
        exitwhen i == 4
        // Bring each harvest stand closer while keeping the town-hall core,
        // north-side mine route, worker line, and western altar approach open.
        set j = 0
        loop
            exitwhen j == 4
            call KLS_AddTree(KLS_X[i]+150+j*150,KLS_Y[i]-500)
            if KLS_Ended then
                return
            endif
            call KLS_AddTree(KLS_X[i]+150+j*150,KLS_Y[i]-700)
            if KLS_Ended then
                return
            endif
            set j = j+1
        endloop
        set i = i + 1
    endloop
    // Preserve the authored road, courtyard and market textures at startup.
    set gate = null
endfunction

function KLS_PlayerLeft takes nothing returns nothing
    local player departing = GetTriggerPlayer()
    local integer p = GetPlayerId(departing)
    local integer i = 0
    if p < 4 and KLS_Active[p] then
        set KLS_Active[p] = false
        set KLS_Players = KLS_Players-1
        loop
            exitwhen i == 4
            if i != p then
                call SetPlayerAlliance(Player(i),departing,ALLIANCE_SHARED_XP,false)
                call SetPlayerAlliance(departing,Player(i),ALLIANCE_SHARED_XP,false)
            endif
            set i = i+1
        endloop
        call KLS_Log("Defender left; active players=" + I2S(KLS_Players))
        call KLS_Message(GetPlayerName(departing) + " has left the defense. Their army keeps its current orders.")
        if KLS_Selecting then
            call KLS_FinishSelection()
        endif
        if KLS_Players == 0 then
            call KLS_End(false)
        else
            if not KLS_Selecting then
                call KLS_ReadyCheck()
            endif
            call KLS_HUDUpdate()
        endif
    endif
    set departing = null
endfunction

// Neutral Extra is reserved for disposable World Editor layout references.
// World Editor creates preplaced units before the initialization trigger.
function KLS_ClearEditorPreviews takes nothing returns nothing
    local group previews = CreateGroup()
    local unit preview
    call GroupEnumUnitsOfPlayer(previews,Player(bj_PLAYER_NEUTRAL_EXTRA),null)
    loop
        set preview = FirstOfGroup(previews)
        exitwhen preview == null
        call GroupRemoveUnit(previews,preview)
        call RemoveUnit(preview)
    endloop
    call DestroyGroup(previews)
    set previews = null
    set preview = null
endfunction

function KLS_Init takes nothing returns nothing
    local integer i = 0
    local integer j = 0
    local integer hero = 'Hpal'
    local unit u
    local trigger deaths = CreateTrigger()
    local trigger builds = CreateTrigger()
    local trigger chats = CreateTrigger()
    local trigger talents = CreateTrigger()
    local trigger evasion = CreateTrigger()
    local trigger market = CreateTrigger()
    local trigger leaves = CreateTrigger()
    local real x
    local real y
    local destructable tree
    call KLS_ClearEditorPreviews()
    set KLS_Enemies = CreateGroup()
    call KLS_PersonalRewardInit()
    call KLS_Log("Initialization entered")
    // GENERATED_PLOT_COORDINATES
    call KLS_BuildLandscape()
    if KLS_Ended then
        return
    endif
    call KLS_Log("Landscape creation completed")
    call SetPlayerAlliance(Player(PLAYER_NEUTRAL_PASSIVE), Player(11), ALLIANCE_PASSIVE, false)
    call SetPlayerAlliance(Player(11), Player(PLAYER_NEUTRAL_PASSIVE), ALLIANCE_PASSIVE, false)
    // The keep is centered on the marked defense row. King Aldric holds the
    // northern face so incoming undead reach him before the castle.
    set u = KLS_CreateUnit(Player(PLAYER_NEUTRAL_PASSIVE), 'hC01', KLS_CastleX, KLS_CastleY, 270)
    if u == null then
        return
    endif
    set KLS_Castle = u
    call BlzSetUnitName(u, "King Aldric's Castle")
    call SetUnitInvulnerable(u, true)
    call UnitAddAbility(u,'Apit')
    call UnitAddAbility(u,'Asid')
    call UnitAddAbility(u,'Asud')
    call AddItemToStock(u,'KHE1',1,1)
    call AddItemToStock(u,'KUP1',1,1)
    call SetUnitAcquireRange(u, 0)
    set KLS_King = KLS_CreateUnit(Player(PLAYER_NEUTRAL_PASSIVE), 'Hpal', KLS_KingX, KLS_KingY, 270)
    if KLS_King == null then
        return
    endif
    call BlzSetUnitName(KLS_King, "King Aldric")
    call BlzSetHeroProperName(KLS_King, "King Aldric")
    call SetHeroLevel(KLS_King, 10, false)
    call BlzSetUnitMaxHP(KLS_King, 15000)
    call SetWidgetLife(KLS_King, 15000)
    call BlzSetUnitBaseDamage(KLS_King, 80, 0)
    call SetUnitAcquireRange(KLS_King, 900)
    call SetUnitMoveSpeed(KLS_King, 0)
    // Six tiered gear vendors are placed around the southern market plaza.
    call KLS_CreateShops()
    if KLS_Ended then
        return
    endif
    loop
        exitwhen i == 4
        call TriggerRegisterPlayerEvent(leaves,Player(i),EVENT_PLAYER_LEAVE)
        set x = KLS_X[i]
        set y = KLS_Y[i]
        set KLS_Plot[i] = Rect(x - 1024, y - 1024, x + 1024, y + 1024)
        set KLS_Active[i] = GetPlayerSlotState(Player(i)) == PLAYER_SLOT_STATE_PLAYING and GetPlayerController(Player(i)) == MAP_CONTROL_USER
        set KLS_DifficultyVote[i] = 1
        set KLS_ReadyVote[i] = false
        if KLS_Active[i] then
            set KLS_Players = KLS_Players + 1
            call SetPlayerState(Player(i), PLAYER_STATE_RESOURCE_GOLD, 700)
            call SetPlayerState(Player(i), PLAYER_STATE_RESOURCE_LUMBER, 300)
            call SetPlayerState(Player(i), PLAYER_STATE_RESOURCE_FOOD_CAP, 30)
            call SetPlayerAlliance(Player(i), Player(PLAYER_NEUTRAL_PASSIVE), ALLIANCE_PASSIVE, true)
            call SetPlayerAlliance(Player(PLAYER_NEUTRAL_PASSIVE), Player(i), ALLIANCE_PASSIVE, true)
            set j = 0
            loop
                exitwhen j == 4
                call SetPlayerAlliance(Player(i), Player(j), ALLIANCE_PASSIVE, true)
                call SetPlayerAlliance(Player(i), Player(j), ALLIANCE_SHARED_VISION, true)
                call SetPlayerAlliance(Player(i), Player(j), ALLIANCE_SHARED_CONTROL, false)
                set j = j + 1
            endloop
            set KLS_BaseMine[i] = KLS_CreateUnit(Player(PLAYER_NEUTRAL_PASSIVE), 'ngol', x + KLS_MineOffsetX, y + KLS_MineOffsetY, 270)
            if KLS_BaseMine[i] == null then
                return
            endif
            call SetResourceAmount(KLS_BaseMine[i], 1000000)
            set u = KLS_CreateUnit(Player(i), 'htow', x, y, 270)
            if u == null then
                return
            endif
            set KLS_BaseTownHall[i] = u
            set KLS_Altar[i] = KLS_CreateUnit(Player(i), 'h000', x + KLS_AltarOffsetX, y + KLS_AltarOffsetY, 270)
            if KLS_Altar[i] == null then
                return
            endif
            set j = 0
            loop
                exitwhen j == 5
                set u = KLS_CreateUnit(Player(i), 'hpea', x + KLS_WorkerOffsetX + j * 90, y + KLS_WorkerOffsetY, 270)
                if u == null then
                    return
                endif
                if j == 0 then
                    set KLS_FirstWorker[i] = u
                endif
                set j = j + 1
            endloop
            call TriggerRegisterPlayerChatEvent(chats, Player(i), "-", false)
        endif
        set i = i + 1
    endloop
    // Disable native sharing; the kill handler awards full XP to each nearby
    // active player's hero, rather than splitting one pool between heroes.
    set i = 0
    loop
        exitwhen i == 4
        if KLS_Active[i] then
            set j = 0
            loop
                exitwhen j == 4
                if KLS_Active[j] and i != j then
                    call SetPlayerAlliance(Player(i),Player(j),ALLIANCE_SHARED_XP,false)
                endif
                set j = j+1
            endloop
        endif
        set i = i+1
    endloop
    call KLS_CompanyInit()
    call KLS_MiningInit()
    call KLS_CrownlandsInit()
    call KLS_ProgressionInit()
    call KLS_VoteUIInit()
    call TriggerAddAction(leaves,function KLS_PlayerLeft)
    call TriggerRegisterAnyUnitEventBJ(deaths, EVENT_PLAYER_UNIT_DEATH)
    call TriggerAddAction(deaths, function KLS_Death)
    call TriggerRegisterAnyUnitEventBJ(builds, EVENT_PLAYER_UNIT_CONSTRUCT_START)
    call TriggerAddAction(builds, function KLS_Construct)
    call TriggerAddAction(chats, function KLS_Chat)
    call TriggerRegisterAnyUnitEventBJ(talents, EVENT_PLAYER_HERO_LEVEL)
    call TriggerAddAction(talents, function KLS_TalentLevel)
    call TriggerRegisterAnyUnitEventBJ(evasion, EVENT_PLAYER_UNIT_DAMAGED)
    call TriggerAddAction(evasion, function KLS_TalentAvoidDamage)
    call TriggerRegisterAnyUnitEventBJ(market, EVENT_PLAYER_UNIT_SELL_ITEM)
    call TriggerAddAction(market, function KLS_MarketBuy)
    call KLS_HUDInit()
    call KLS_InventoryInit()
    call KLS_GearInit()
    call KLS_WaveEnvironmentInit()
    if KLS_Ended then
        return
    endif
    call KLS_SignatureInit()
    call KLS_SelectionInit()
    if KLS_Ended then
        return
    endif
    call KLS_Log("Startup completed; hero selection active")
    set KLS_Clock = CreateTimer()
    call TimerStart(KLS_Clock, 1, true, function KLS_Tick)
    call FogMaskEnable(false)
    call FogEnable(false)
    call KLS_Message("The King's Last Stand: defend King Aldric! Choose your hero first; preparation starts when everyone is ready. Type -help for commands.")
    set tree = null
    set u = null
    set deaths = null
    set builds = null
    set chats = null
    set talents = null
    set evasion = null
    set market = null
    set leaves = null
endfunction
