globals
    unit array KLS_TownSite
    group KLS_StoryEnemies = null
    timer KLS_StoryCartClock = null
    unit KLS_StoryCart = null
    dialog array KLS_StoryDialog
    button array KLS_StoryStartButton
    button array KLS_StoryCloseButton
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
            call DisplayTimedTextToPlayer(Player(p),0,0,8,"Crownlands story reward: personal gold and a race relic.")
        endif
        set p = p+1
    endloop
    set KLS_StoryStage = KLS_StoryStage+1
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

function KLS_StoryCartTick takes nothing returns nothing
    local real y
    if KLS_StoryCart == null or KLS_Ended then
        call PauseTimer(KLS_StoryCartClock)
        return
    endif
    set KLS_StoryCartSteps = KLS_StoryCartSteps+1
    set y = -9000.0+I2R(KLS_StoryCartSteps)*220.0
    call SetUnitX(KLS_StoryCart,0.0)
    call SetUnitY(KLS_StoryCart,y)
    if KLS_StoryCartSteps >= 19 then
        call RemoveUnit(KLS_StoryCart)
        set KLS_StoryCart = null
        call PauseTimer(KLS_StoryCartClock)
        call KLS_StoryComplete()
    endif
endfunction

function KLS_StorySpawnEncounter takes integer siteIndex, boolean ritual returns nothing
    local integer n = 0
    local integer kind = 'ugho'
    local unit enemy
    local real x = GetUnitX(KLS_TownSite[siteIndex])
    local real y = GetUnitY(KLS_TownSite[siteIndex])
    set KLS_StoryRemaining = 4
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
        set enemy = KLS_CreateUnit(Player(11),kind,x+I2R(n-2)*150,y+I2R(n-2)*90,270)
        if enemy == null then
            set KLS_StoryRemaining = 0
            return
        endif
        call GroupAddUnit(KLS_StoryEnemies,enemy)
        call SetUnitAcquireRange(enemy,900)
        call IssuePointOrder(enemy,"attack",GetUnitX(KLS_King),GetUnitY(KLS_King))
        set n = n+1
    endloop
    call DisplayTimedTextToForce(bj_FORCE_ALL_PLAYERS,8,"A Crownlands story encounter is attacking during the current wave. It does not change the wave count.")
    set enemy = null
endfunction

function KLS_StoryBegin takes integer p, integer siteIndex returns nothing
    local integer gold
    local integer lumber
    if p < 0 or p >= 4 or not KLS_Active[p] or KLS_Hero[p] == null then
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
        set KLS_StoryCart = KLS_CreateUnit(Player(PLAYER_NEUTRAL_PASSIVE),'hpea',0,-9000,270)
        if KLS_StoryCart == null then
            return
        endif
        set KLS_StoryContributor[KLS_StoryStage*4+p] = true
        call BlzSetUnitName(KLS_StoryCart,"Northwatch Supply Caravan")
        call SetUnitInvulnerable(KLS_StoryCart,true)
        call SetUnitAcquireRange(KLS_StoryCart,0)
        set KLS_StoryCartSteps = 0
        set KLS_StoryCartClock = CreateTimer()
        call TimerStart(KLS_StoryCartClock,1.0,true,function KLS_StoryCartTick)
        call DisplayTimedTextToForce(bj_FORCE_ALL_PLAYERS,8,"The Northwatch supply caravan is following the King's Road. It travels while waves continue.")
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

function KLS_StoryDialogClick takes nothing returns nothing
    local integer p = GetPlayerId(GetTriggerPlayer())
    if p < 0 or p >= 4 then
        return
    endif
    if GetClickedButton() == KLS_StoryStartButton[p] then
        call KLS_StoryBegin(p,KLS_StorySiteChoice[p])
    endif
endfunction

function KLS_StorySiteSelected takes nothing returns nothing
    local unit site = GetTriggerUnit()
    local integer p = GetPlayerId(GetTriggerPlayer())
    local integer siteIndex = GetUnitUserData(site)
    if p >= 0 and p < 4 and KLS_Active[p] and siteIndex >= 0 and siteIndex < 4 and site == KLS_TownSite[siteIndex] then
        set KLS_StorySiteChoice[p] = siteIndex
        if siteIndex == KLS_StoryExpectedSite() then
            call DialogClear(KLS_StoryDialog[p])
            call DialogSetMessage(KLS_StoryDialog[p],"Crownlands: " + GetUnitName(site) + "\nWave time continues while you complete this optional objective.")
            set KLS_StoryStartButton[p] = DialogAddButton(KLS_StoryDialog[p],"Begin / contribute",0)
            set KLS_StoryCloseButton[p] = DialogAddButton(KLS_StoryDialog[p],"Later",512)
            call DialogDisplay(Player(p),KLS_StoryDialog[p],true)
        else
            call DisplayTimedTextToPlayer(Player(p),0,0,6,"Crownlands story: select the marked settlement when you are ready. Objectives stay available during waves.")
        endif
    endif
    set site = null
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
    if KLS_StoryRemaining <= 0 then
        call KLS_StoryComplete()
    endif
    set killer = null
endfunction

function KLS_CrownlandsInit takes nothing returns nothing
    local integer p = 0
    local trigger storySites = CreateTrigger()
    local trigger storyDialogs = CreateTrigger()
    set KLS_StoryEnemies = CreateGroup()
    call KLS_CrownlandsBuildTowns()
    loop
        exitwhen p == 4
        if KLS_Active[p] then
            set KLS_StoryDialog[p] = DialogCreate()
            call TriggerRegisterDialogEvent(storyDialogs,KLS_StoryDialog[p])
        endif
        set p = p+1
    endloop
    call TriggerRegisterAnyUnitEventBJ(storySites,EVENT_PLAYER_UNIT_SELECTED)
    call TriggerAddAction(storySites,function KLS_StorySiteSelected)
    call TriggerAddAction(storyDialogs,function KLS_StoryDialogClick)
    call DisplayTimedTextToForce(bj_FORCE_ALL_PLAYERS,10,"Optional Crownlands story: reclaim Northwatch, escort supplies, restore Moonbark, and break the Wraithfall ritual. Objectives remain open during waves.")
    set storySites = null
    set storyDialogs = null
endfunction
