globals
    unit array KLS_TownSite
    group KLS_StoryEnemies = null
    timer KLS_StoryCartClock = null
    unit KLS_StoryCart = null
    framehandle array KLS_StoryStartButton
    timer KLS_StoryUIClock = null
    unit array KLS_TownHall
    boolean array KLS_StoryUnlock
    boolean array KLS_TownRestored
    integer array KLS_StorySiteChoice
    boolean array KLS_StoryContributor
    integer KLS_StoryStage = 0
    integer KLS_StoryRemaining = 0
    integer KLS_StoryCartSteps = 0
endglobals

// GENERATED_TOWN_PLACEMENTS

function KLS_StoryExpectedSite takes nothing returns integer
    if KLS_StoryStage == 0 then
        return 1
    elseif KLS_StoryStage == 1 then
        return 0
    elseif KLS_StoryStage == 2 then
        return 2
    elseif KLS_StoryStage == 3 then
        return 3
    endif
    return -1
endfunction

function KLS_StoryClearEncounter takes nothing returns nothing
    local unit enemy = FirstOfGroup(KLS_StoryEnemies)
    loop
        exitwhen enemy == null
        call GroupRemoveUnit(KLS_StoryEnemies,enemy)
        call RemoveUnit(enemy)
        set enemy = FirstOfGroup(KLS_StoryEnemies)
    endloop
    set KLS_StoryRemaining = 0
    set enemy = null
endfunction

function KLS_StoryApplyUnlock takes integer stage returns nothing
    local integer i = 0
    local unit guard
    local integer kind
    if stage < 0 or stage > 3 or KLS_StoryUnlock[stage] then
        return
    endif
    set KLS_StoryUnlock[stage] = true
    if stage == 0 then
        set guard = KLS_CreateUnitOptional(Player(PLAYER_NEUTRAL_PASSIVE),'hgtw',-7600,-650,270,"Northwatch restored watchpost")
        set guard = KLS_CreateUnitOptional(Player(PLAYER_NEUTRAL_PASSIVE),'hgtw',-7600,650,270,"Northwatch restored watchpost")
    endif
    loop
        exitwhen i == 4
        if stage == 1 and KLS_TownShop[i] != null then
            call AddItemToStock(KLS_TownShop[i],'pghe',1,99)
            call AddItemToStock(KLS_TownShop[i],'pgma',1,99)
        elseif stage == 2 then
            set KLS_TownRestored[i] = true
            if KLS_TownHall[i] != null then
                call BlzSetUnitName(KLS_TownHall[i],GetUnitName(KLS_TownHall[i])+" - Restored Quarter")
            endif
            if KLS_TownSite[i] != null then
                call BlzSetUnitName(KLS_TownSite[i],GetUnitName(KLS_TownSite[i])+" - Restoring Refuge")
            endif
        elseif stage == 3 then
            if KLS_TownShop[i] != null then
                call AddItemToStock(KLS_TownShop[i],'pres',1,99)
            endif
            if i == 0 then
                set kind = 'hfoo'
            elseif i == 1 then
                set kind = 'ogru'
            elseif i == 2 then
                set kind = 'edry'
            else
                set kind = 'ugho'
            endif
            set guard = KLS_CreateUnitOptional(Player(PLAYER_NEUTRAL_PASSIVE),kind,GetUnitX(KLS_TownSite[i])+200,GetUnitY(KLS_TownSite[i])+200,270,"restored town garrison")
        endif
        set i = i+1
    endloop
    set guard = null
endfunction

function KLS_StoryComplete takes nothing returns nothing
    local integer p = 0
    local integer rewardTier = KLS_StoryStage
    local integer itemCode
    if KLS_StoryStage >= 4 then
        return
    endif
    if rewardTier > 2 then
        set rewardTier = 2
    endif
    loop
        exitwhen p == 4
        if KLS_StoryContributor[KLS_StoryStage*4+p] and KLS_Active[p] and KLS_Hero[p] != null then
            call SetPlayerState(Player(p),PLAYER_STATE_RESOURCE_GOLD,GetPlayerState(Player(p),PLAYER_STATE_RESOURCE_GOLD)+150+KLS_StoryStage*100)
            set itemCode = KLS_RandomCatalogDrop(rewardTier)
            call KLS_PersonalRewardEnqueue(p,itemCode,"Crownlands story")
            call DisplayTimedTextToPlayer(Player(p),0,0,8,"Crownlands story reward: personal gold and a bound equipment item.")
        endif
        set p = p+1
    endloop
    call KLS_StoryApplyUnlock(KLS_StoryStage)
    set KLS_StoryStage = KLS_StoryStage+1
    call KLS_CompanyResearchRefresh()
    if KLS_StoryStage >= 4 then
        call DisplayTimedTextToForce(bj_FORCE_ALL_PLAYERS,10,"|cffFFD700The four Crownlands towns are restored. Their story rewards were personal to each contributor.|r")
    elseif KLS_StoryStage == 1 then
        call DisplayTimedTextToForce(bj_FORCE_ALL_PLAYERS,10,"|cffFFD700Northwatch is reclaimed. Escort its supply train from Crownshire when ready.|r")
    elseif KLS_StoryStage == 2 then
        call DisplayTimedTextToForce(bj_FORCE_ALL_PLAYERS,10,"|cffFFD700The supply train arrived. Restore Moonbark's quarter with 250 gold and 100 lumber.|r")
    else
        call DisplayTimedTextToForce(bj_FORCE_ALL_PLAYERS,10,"|cffFFD700Moonbark is restored. Break the Wraithfall invasion ritual when ready.|r")
    endif
    call KLS_Log("Crownlands story stage completed; shared unlock="+I2S(KLS_StoryStage))
endfunction

function KLS_StoryEscortFailed takes nothing returns nothing
    call PauseTimer(KLS_StoryCartClock)
    if KLS_StoryCart != null then
        call RemoveUnit(KLS_StoryCart)
        set KLS_StoryCart = null
    endif
    call KLS_StoryClearEncounter()
    set KLS_StoryCartSteps = 0
    call DisplayTimedTextToForce(bj_FORCE_ALL_PLAYERS,8,"The supply caravan was lost. Crownshire can send another; the story remains available and waves continue.")
endfunction

function KLS_StoryAmbush takes nothing returns nothing
    local integer n = 0
    local unit enemy
    loop
        exitwhen n == 2
        set enemy = KLS_CreateUnitOptional(Player(11),'ugho',GetUnitX(KLS_StoryCart)+320+I2R(n)*80,GetUnitY(KLS_StoryCart)+300,270,"caravan ambush")
        if enemy != null then
            call GroupAddUnit(KLS_StoryEnemies,enemy)
            set KLS_StoryRemaining = KLS_StoryRemaining+1
            call BlzSetUnitMaxHP(enemy,R2I(650.0*KLS_DifficultyHealthScale()))
            call SetWidgetLife(enemy,I2R(BlzGetUnitMaxHP(enemy)))
            call BlzSetUnitBaseDamage(enemy,R2I(18.0*KLS_DifficultyDamageScale()),0)
            call IssueTargetOrder(enemy,"attack",KLS_StoryCart)
        endif
        set n = n+1
    endloop
    set enemy = null
endfunction

function KLS_StoryCartTick takes nothing returns nothing
    local integer p = 0
    local unit hero
    local real dx
    local real dy
    local boolean escorted = false
    if KLS_StoryCart == null or KLS_Ended then
        call PauseTimer(KLS_StoryCartClock)
        return
    endif
    if GetWidgetLife(KLS_StoryCart) <= 0.405 then
        call KLS_StoryEscortFailed()
        return
    endif
    loop
        exitwhen p == 4
        set hero = KLS_Hero[p]
        if KLS_Active[p] and hero != null and GetWidgetLife(hero) > 0.405 then
            set dx = GetUnitX(hero)-GetUnitX(KLS_StoryCart)
            set dy = GetUnitY(hero)-GetUnitY(KLS_StoryCart)
            if dx*dx+dy*dy <= 810000.0 then
                set escorted = true
                set KLS_StoryContributor[4+p] = true
            endif
        endif
        set p = p+1
    endloop
    if not escorted then
        call IssueImmediateOrder(KLS_StoryCart,"stop")
        set hero = null
        return
    endif
    call IssuePointOrder(KLS_StoryCart,"move",0.0,-4800.0)
    set KLS_StoryCartSteps = KLS_StoryCartSteps+1
    if KLS_StoryCartSteps == 8 or KLS_StoryCartSteps == 16 then
        call KLS_StoryAmbush()
    endif
    if GetUnitY(KLS_StoryCart) >= -4950.0 then
        call RemoveUnit(KLS_StoryCart)
        set KLS_StoryCart = null
        call PauseTimer(KLS_StoryCartClock)
        call KLS_StoryClearEncounter()
        call KLS_StoryComplete()
    endif
    set hero = null
endfunction

function KLS_StoryEncounterAbort takes nothing returns nothing
    local unit remaining = FirstOfGroup(KLS_StoryEnemies)
    loop
        exitwhen remaining == null
        call GroupRemoveUnit(KLS_StoryEnemies,remaining)
        call RemoveUnit(remaining)
        set remaining = FirstOfGroup(KLS_StoryEnemies)
    endloop
    set KLS_StoryRemaining = 0
    call KLS_Log("ERROR Crownlands encounter cancelled after an optional spawn failure; stage remains="+I2S(KLS_StoryStage))
    call DisplayTimedTextToForce(bj_FORCE_ALL_PLAYERS,8,"A Crownlands patrol failed to muster. The story remains available to retry; waves continue.")
    set remaining = null
endfunction

function KLS_StorySpawnEncounter takes integer siteIndex, boolean ritual returns nothing
    local integer n = 0
    local integer kind = 'ugho'
    local unit enemy
    local boolean spawnFailed = false
    local real x = GetUnitX(KLS_TownSite[siteIndex])
    local real y = GetUnitY(KLS_TownSite[siteIndex])
    set KLS_StoryRemaining = 0
    loop
        exitwhen n == 4 or KLS_Ended
        if ritual then
            if n == 0 then
                set kind = 'nbal'
            elseif n == 1 then
                set kind = 'ninf'
            elseif n == 2 then
                set kind = 'uabo'
            else
                set kind = 'nfgu'
            endif
        else
            if n == 0 then
                set kind = 'ugho'
            elseif n == 1 then
                set kind = 'uske'
            elseif n == 2 then
                set kind = 'nfel'
            else
                set kind = 'nfgu'
            endif
        endif
        set enemy = KLS_CreateUnitOptional(Player(11),kind,x+I2R(n-2)*150,y+I2R(n-2)*90,270,"Crownlands story encounter")
        if enemy == null then
            set spawnFailed = true
        else
            call GroupAddUnit(KLS_StoryEnemies,enemy)
            set KLS_StoryRemaining = KLS_StoryRemaining+1
            call SetUnitAcquireRange(enemy,900)
            call IssuePointOrder(enemy,"attack",GetUnitX(KLS_King),GetUnitY(KLS_King))
        endif
        set n = n+1
    endloop
    if spawnFailed then
        call KLS_StoryEncounterAbort()
    elseif KLS_StoryRemaining > 0 and not KLS_Ended then
        call DisplayTimedTextToForce(bj_FORCE_ALL_PLAYERS,8,"A Crownlands story encounter is attacking during the current wave. It does not change the wave count.")
    endif
    set enemy = null
endfunction

function KLS_StoryBegin takes integer p, integer siteIndex returns nothing
    local integer gold
    local integer lumber
    local real dx
    local real dy
    if p < 0 or p >= 4 or not KLS_Active[p] or KLS_Hero[p] == null or KLS_Ended or KLS_Selecting or siteIndex < 0 or siteIndex >= 4 or GetWidgetLife(KLS_Hero[p]) <= 0.405 then
        return
    endif
    set dx = GetUnitX(KLS_Hero[p])-GetUnitX(KLS_TownSite[siteIndex])
    set dy = GetUnitY(KLS_Hero[p])-GetUnitY(KLS_TownSite[siteIndex])
    if dx*dx+dy*dy > 1000000.0 then
        call DisplayTimedTextToPlayer(Player(p),0,0,6,"Bring your hero within 1,000 range of this town contact.")
        return
    endif
    if siteIndex != KLS_StoryExpectedSite() then
        if KLS_StoryStage >= 4 then
            call DisplayTimedTextToPlayer(Player(p),0,0,6,"The Crownlands story is complete for this match.")
        else
            call DisplayTimedTextToPlayer(Player(p),0,0,6,"Visit the currently marked town objective to continue the shared story.")
        endif
        return
    endif
    if (KLS_StoryStage == 0 or KLS_StoryStage == 3) and KLS_StoryRemaining > 0 then
        call DisplayTimedTextToPlayer(Player(p),0,0,5,"This Crownlands encounter is already underway.")
        return
    endif
    if KLS_StoryStage == 1 then
        if KLS_StoryCart != null then
            set KLS_StoryContributor[KLS_StoryStage*4+p] = true
            call DisplayTimedTextToPlayer(Player(p),0,0,5,"You joined the Northwatch supply escort.")
            return
        endif
        set KLS_StoryCart = KLS_CreateUnitOptional(Player(PLAYER_NEUTRAL_PASSIVE),'kCar',0,-8400,270,"Northwatch supply caravan")
        if KLS_StoryCart == null then
            call DisplayTimedTextToPlayer(Player(p),0,0,6,"The caravan could not be created. No resources were spent; check -diag and try again.")
            return
        endif
        set KLS_StoryContributor[KLS_StoryStage*4+p] = true
        call BlzSetUnitName(KLS_StoryCart,"Northwatch Supply Caravan")
        call SetUnitInvulnerable(KLS_StoryCart,false)
        call SetUnitAcquireRange(KLS_StoryCart,0)
        set KLS_StoryCartSteps = 0
        call TimerStart(KLS_StoryCartClock,1.0,true,function KLS_StoryCartTick)
        call DisplayTimedTextToForce(bj_FORCE_ALL_PLAYERS,8,"Escort the Northwatch caravan along the King's Road. It moves with a living hero within 900 range; protect it from ambushers.")
    elseif KLS_StoryStage == 2 then
        set gold = GetPlayerState(Player(p),PLAYER_STATE_RESOURCE_GOLD)
        set lumber = GetPlayerState(Player(p),PLAYER_STATE_RESOURCE_LUMBER)
        if gold < 250 or lumber < 100 then
            call DisplayTimedTextToPlayer(Player(p),0,0,6,"Restoring Moonbark costs 250 personal gold and 100 personal lumber.")
            return
        endif
        call SetPlayerState(Player(p),PLAYER_STATE_RESOURCE_GOLD,gold-250)
        call SetPlayerState(Player(p),PLAYER_STATE_RESOURCE_LUMBER,lumber-100)
        set KLS_StoryContributor[KLS_StoryStage*4+p] = true
        call KLS_StoryComplete()
    else
        set KLS_StoryContributor[KLS_StoryStage*4+p] = true
        call KLS_StorySpawnEncounter(siteIndex,KLS_StoryStage == 3)
    endif
endfunction

function KLS_StoryStartSync takes nothing returns nothing
    local integer p = GetPlayerId(GetTriggerPlayer())
    local integer site = KLS_StoryExpectedSite()
    if site >= 0 and BlzGetTriggerSyncData() == I2S(KLS_StoryStage)+":"+I2S(site) then
        call KLS_StoryBegin(p,site)
    endif
endfunction

function KLS_StoryStartClick takes nothing returns nothing
    local integer p = GetPlayerId(GetTriggerPlayer())
    local integer site = KLS_StoryExpectedSite()
    if p >= 0 and p < 4 and GetLocalPlayer() == Player(p) and site >= 0 and BlzGetTriggerFrame() == KLS_StoryStartButton[p] then
        call BlzSendSyncData("KLSSTORY",I2S(KLS_StoryStage)+":"+I2S(site))
    endif
endfunction

function KLS_StoryUIRefresh takes nothing returns nothing
    local integer p = GetPlayerId(GetLocalPlayer())
    local integer site = KLS_StoryExpectedSite()
    local boolean visible = false
    if p >= 0 and p < 4 and KLS_Active[p] and KLS_StoryStartButton[p] != null then
        if site >= 0 and not KLS_Ended and not KLS_Selecting then
            set visible = IsUnitSelected(KLS_TownSite[site],Player(p))
        endif
        call BlzFrameSetVisible(KLS_StoryStartButton[p],visible)
    endif
endfunction

function KLS_StorySiteSelected takes nothing returns nothing
    local unit site = GetTriggerUnit()
    local integer p = GetPlayerId(GetTriggerPlayer())
    local integer index = GetUnitUserData(site)
    if p >= 0 and p < 4 and KLS_Active[p] and index >= 0 and index < 4 and site == KLS_TownSite[index] then
        call DisplayTimedTextToPlayer(Player(p),0,0,8,"Crownlands story: bring your hero close and choose Begin / contribute. This optional story continues during waves.")
    endif
    set site = null
endfunction

function KLS_StoryRecordDamage takes nothing returns nothing
    local unit victim = GetTriggerUnit()
    local unit attacker = GetEventDamageSource()
    local integer p = GetPlayerId(GetOwningPlayer(attacker))
    if KLS_StoryStage < 4 and p >= 0 and p < 4 and KLS_Active[p] and GetEventDamage() > 0.0 and IsUnitInGroup(victim,KLS_StoryEnemies) then
        set KLS_StoryContributor[KLS_StoryStage*4+p] = true
    endif
    set victim = null
    set attacker = null
endfunction

function KLS_StoryRefugesTick takes nothing returns nothing
    local integer i = 0
    local group nearby = CreateGroup()
    local unit target
    if KLS_Ended then
        call DestroyGroup(nearby)
        set nearby = null
        return
    endif
    loop
        exitwhen i == 4
        if KLS_TownRestored[i] and KLS_TownSite[i] != null then
            call GroupEnumUnitsInRange(nearby,GetUnitX(KLS_TownSite[i]),GetUnitY(KLS_TownSite[i]),650,null)
            loop
                set target = FirstOfGroup(nearby)
                exitwhen target == null
                call GroupRemoveUnit(nearby,target)
                if GetWidgetLife(target) > 0.405 and target != KLS_King and GetPlayerId(GetOwningPlayer(target)) < 4 and not IsUnitType(target,UNIT_TYPE_STRUCTURE) then
                    call SetWidgetLife(target,RMinBJ(I2R(BlzGetUnitMaxHP(target)),GetWidgetLife(target)+I2R(BlzGetUnitMaxHP(target))*0.01))
                    call SetUnitState(target,UNIT_STATE_MANA,RMinBJ(GetUnitState(target,UNIT_STATE_MAX_MANA),GetUnitState(target,UNIT_STATE_MANA)+GetUnitState(target,UNIT_STATE_MAX_MANA)*0.01))
                endif
            endloop
        endif
        set i = i+1
    endloop
    call DestroyGroup(nearby)
    set nearby = null
    set target = null
endfunction

function KLS_StoryEnemyKilled takes unit dead returns nothing
    local unit killer = GetKillingUnit()
    local integer p = 4
    if not IsUnitInGroup(dead,KLS_StoryEnemies) then
        set killer = null
        return
    endif
    call GroupRemoveUnit(KLS_StoryEnemies,dead)
    set KLS_StoryRemaining = KLS_StoryRemaining-1
    if killer != null then
        set p = GetPlayerId(GetOwningPlayer(killer))
    endif
    if p >= 0 and p < 4 and KLS_Active[p] then
        set KLS_StoryContributor[KLS_StoryStage*4+p] = true
        call SetPlayerState(Player(p),PLAYER_STATE_RESOURCE_GOLD,GetPlayerState(Player(p),PLAYER_STATE_RESOURCE_GOLD)+25)
        call DisplayTimedTextToPlayer(Player(p),0,0,4,"+25 gold for the Crownlands story kill.")
    endif
    if KLS_StoryRemaining <= 0 and KLS_StoryStage != 1 then
        call KLS_StoryComplete()
    endif
    set killer = null
endfunction

function KLS_CrownlandsInit takes nothing returns nothing
    local integer p = 0
    local trigger storySites = CreateTrigger()
    local trigger storyClicks = CreateTrigger()
    local trigger storySync = CreateTrigger()
    local trigger damage = CreateTrigger()
    local timer refuges = CreateTimer()
    local framehandle gameUI = BlzGetOriginFrame(ORIGIN_FRAME_GAME_UI,0)
    set KLS_StoryEnemies = CreateGroup()
    set KLS_StoryCartClock = CreateTimer()
    call KLS_CrownlandsBuildTowns()
    loop
        exitwhen p == 4
        if KLS_Active[p] then
            set KLS_StoryStartButton[p] = BlzCreateFrameByType("GLUETEXTBUTTON","KLSStoryStart",gameUI,"ScriptDialogButton",0)
            call BlzFrameSetSize(KLS_StoryStartButton[p],0.18,0.035)
            call BlzFrameSetText(KLS_StoryStartButton[p],"Begin / contribute")
            call BlzFrameSetAbsPoint(KLS_StoryStartButton[p],FRAMEPOINT_TOPLEFT,0.02,0.22)
            call BlzFrameSetVisible(KLS_StoryStartButton[p],false)
            call BlzTriggerRegisterFrameEvent(storyClicks,KLS_StoryStartButton[p],FRAMEEVENT_CONTROL_CLICK)
            call BlzTriggerRegisterPlayerSyncEvent(storySync,Player(p),"KLSSTORY",false)
        endif
        set p = p+1
    endloop
    call TriggerRegisterAnyUnitEventBJ(storySites,EVENT_PLAYER_UNIT_SELECTED)
    call TriggerAddAction(storySites,function KLS_StorySiteSelected)
    call TriggerAddAction(storyClicks,function KLS_StoryStartClick)
    call TriggerAddAction(storySync,function KLS_StoryStartSync)
    call TriggerRegisterAnyUnitEventBJ(damage,EVENT_PLAYER_UNIT_DAMAGED)
    call TriggerAddAction(damage,function KLS_StoryRecordDamage)
    set KLS_StoryUIClock = CreateTimer()
    call TimerStart(KLS_StoryUIClock,0.25,true,function KLS_StoryUIRefresh)
    call TimerStart(refuges,1.0,true,function KLS_StoryRefugesTick)
    call DisplayTimedTextToForce(bj_FORCE_ALL_PLAYERS,10,"Optional Crownlands story: reclaim Northwatch, escort supplies, restore the quarters, and break the ritual. Objectives remain open during waves.")
    set storySites = null
    set storyClicks = null
    set storySync = null
    set damage = null
    set refuges = null
    set gameUI = null
endfunction
