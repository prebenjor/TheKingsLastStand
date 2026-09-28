// The King's Last Stand: native JASS development runtime.
globals
    unit KLS_King = null
    unit array KLS_Hero
    unit array KLS_FirstWorker
    rect array KLS_Plot
    real array KLS_X
    real array KLS_Y
    boolean array KLS_Active
    integer KLS_Players = 0
    integer KLS_Wave = 0
    integer KLS_Alive = 0
    integer KLS_Prep = 45
    integer KLS_NormalPrep = 90
    integer KLS_BossPrep = 180
    boolean KLS_Ended = false
    timer KLS_Clock = null
    group KLS_Enemies = null
    integer array KLS_Respawn
    integer KLS_KingTier = 0
    integer KLS_Seconds = 0
endglobals

function KLS_Message takes string s returns nothing
    call DisplayTimedTextToForce(bj_FORCE_ALL_PLAYERS, 8.0, s)
endfunction

function KLS_GoldToast takes integer p, integer amount returns nothing
    if p >= 0 and p < 4 and amount > 0 then
        call DisplayTimedTextToPlayer(Player(p),0,0.22,2.5,"|cffffcc00+"+I2S(amount)+" gold|r")
    endif
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
    local integer gear = 'I010'
    local item reward
    if KLS_Wave == 20 then
        set gear = 'I011'
    elseif KLS_Wave == 30 then
        set gear = 'I012'
    elseif KLS_Wave == 40 then
        set gear = 'I013'
    endif
    loop
        exitwhen i == 4
        if KLS_Active[i] then
            call SetPlayerState(Player(i), PLAYER_STATE_RESOURCE_GOLD, GetPlayerState(Player(i), PLAYER_STATE_RESOURCE_GOLD) + 250 + KLS_Wave * 10)
            call KLS_GoldToast(i,250 + KLS_Wave * 10)
            set reward = CreateItem(gear, KLS_X[i], KLS_Y[i])
            call SetItemPlayer(reward, Player(i), false)
            call SetItemUserData(reward, i+1)
            if not UnitAddItem(KLS_Hero[i], reward) then
                call SetItemVisible(reward, true)
                call SetItemPosition(reward, KLS_X[i], KLS_Y[i])
                call DisplayTimedTextToPlayer(Player(i), 0, 0, 12, "Your personal boss reward is waiting at your base.")
            endif
        endif
        set i = i + 1
    endloop
    set reward = null
endfunction

function KLS_AwardBounty takes integer bounty returns nothing
    local integer i = 0
    local integer activeCount = 0
    local integer share = 0
    local integer remainder = 0
    local integer payout = 0
    loop
        exitwhen i == 4
        if KLS_Active[i] then
            set activeCount = activeCount + 1
        endif
        set i = i + 1
    endloop
    if activeCount == 0 then
        return
    endif
    set share = bounty / activeCount
    set remainder = ModuloInteger(bounty, activeCount)
    set i = 0
    loop
        exitwhen i == 4
        if KLS_Active[i] then
            set payout = share
            if remainder > 0 then
                set payout = payout + 1
                set remainder = remainder - 1
            endif
            call SetPlayerState(Player(i), PLAYER_STATE_RESOURCE_GOLD, GetPlayerState(Player(i), PLAYER_STATE_RESOURCE_GOLD) + payout)
            call KLS_GoldToast(i,payout)
        endif
        set i = i + 1
    endloop
endfunction

function KLS_Death takes nothing returns nothing
    local unit dead = GetTriggerUnit()
    local integer i = 0
    if KLS_Ended then
        return
    endif
    if dead == KLS_King then
        call KLS_End(false)
    elseif IsUnitInGroup(dead, KLS_Enemies) then
        call GroupRemoveUnit(KLS_Enemies, dead)
        set KLS_Alive = KLS_Alive - 1
        call KLS_AwardBounty(KLS_EnemyBounty(dead))
        if dead == KLS_Boss then
            set KLS_Boss = null
            if GetWidgetLife(KLS_King) <= 0.405 then
                call KLS_End(false)
            else
                call KLS_BossReward()
                if KLS_Wave == 40 then
                    call KLS_End(true)
                else
                    call KLS_Message("Boss defeated! Clear the remaining enemies.")
                endif
            endif
        endif
        if not KLS_Ended and KLS_Alive == 0 then
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
    local integer kind = 'ugho'
    local unit u
    local real hp
    local boolean spawnFailed = false
    set KLS_Wave = KLS_Wave + 1
    set KLS_Boss = null
    set KLS_BossCast = 0
    set KLS_BossMechanic = 0
    call KLS_Log("Wave spawn started: " + I2S(KLS_Wave))
    set count = 7 + KLS_Wave * 2 + KLS_Players * 3
    loop
        exitwhen n == count or spawnFailed or KLS_Ended
        set kind = KLS_Roster[KLS_Wave*20+ModuloInteger(n,KLS_RosterSize[KLS_Wave])]
        set u = KLS_CreateUnit(Player(11), kind, I2R(ModuloInteger(n, 5) - 2) * 140, 6200 + I2R(n / 5) * 40, 270)
        if u != null then
            set hp = 180 + KLS_Wave * 55 + KLS_Players * 35
            call BlzSetUnitMaxHP(u, R2I(hp))
            call SetWidgetLife(u, hp)
            call BlzSetUnitBaseDamage(u, 6 + KLS_Wave * 2, 0)
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
        set kind = 'Udea'
        if KLS_Wave == 20 then
            set kind = 'Ulic'
        elseif KLS_Wave == 30 then
            set kind = 'Udre'
        elseif KLS_Wave == 40 then
            set kind = 'Uanb'
        endif
        set u = KLS_CreateUnit(Player(11), kind, 0, 6800, 270)
        if u != null then
            set KLS_Boss = u
            set KLS_BossMechanic = KLS_BossMechanicForWave(KLS_Wave)
            set KLS_BossCast = 0
            call SetHeroLevel(u, KLS_Wave / 2, false)
            set hp = KLS_Wave * 550 * (1 + KLS_Players * 0.3)
            call BlzSetUnitMaxHP(u, R2I(hp))
            call SetWidgetLife(u, hp)
            call BlzSetUnitBaseDamage(u, KLS_Wave * 5, 0)
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
        set KLS_Prep = KLS_Prep - 1
        if KLS_Prep <= 0 then
            call KLS_Spawn()
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
    endif
    if KLS_Ended then
        return
    endif
    if s == "-repair" then
        call KLS_KingContribute(p,false,KLS_KingTier,false)
    elseif s == "-upgrade" then
        call KLS_KingContribute(p,true,KLS_KingTier,false)
    elseif s == "-power" and KLS_TalentPoints[i] > 0 then
        set KLS_TalentPoints[i] = KLS_TalentPoints[i] - 1
        call BlzSetUnitBaseDamage(KLS_Hero[i], BlzGetUnitBaseDamage(KLS_Hero[i], 0)+12, 0)
    elseif s == "-vitality" and KLS_TalentPoints[i] > 0 then
        set KLS_TalentPoints[i] = KLS_TalentPoints[i] - 1
        call BlzSetUnitMaxHP(KLS_Hero[i], BlzGetUnitMaxHP(KLS_Hero[i])+300)
        call SetWidgetLife(KLS_Hero[i], GetWidgetLife(KLS_Hero[i])+300)
    elseif s == "-wisdom" and KLS_TalentPoints[i] > 0 then
        set KLS_TalentPoints[i] = KLS_TalentPoints[i] - 1
        call SetHeroInt(KLS_Hero[i], GetHeroInt(KLS_Hero[i], false)+10, true)
    elseif s == "-gold" and KLS_Debug then
        call SetPlayerState(p, PLAYER_STATE_RESOURCE_GOLD, gold+5000)
        call SetPlayerState(p, PLAYER_STATE_RESOURCE_LUMBER, wood+5000)
    elseif SubString(s, 0, 6) == "-wave " and KLS_Debug then
        if S2I(SubString(s, 6, StringLength(s))) >= 1 and S2I(SubString(s, 6, StringLength(s))) <= 40 then
            call ForGroup(KLS_Enemies, function KLS_DebugRemove)
            call GroupClear(KLS_Enemies)
            set KLS_Alive = 0
            set KLS_Wave = S2I(SubString(s, 6, StringLength(s)))-1
            call KLS_Spawn()
        endif
    elseif s == "-help" then
        call DisplayTimedTextToPlayer(p, 0, 0, 30, "Defend the king through 40 waves. Build in your personal plot. Gold mines and trees fund your army. Select King Aldric's Castle to heal or upgrade him. -repair: 150 gold/50 lumber, heals 2000. -upgrade: 400+200 per tier gold/150 lumber. Heroes revive after 20 seconds. The Forsaken Field Pack adds 30 storage and nine equipment slots.")
    endif
    set p = null
endfunction

function KLS_AddTree takes real x, real y returns nothing
    local destructable tree = KLS_CreateDestructable('LTlt', x, y, 0, 1.0, 0)
    if tree == null then
        return
    endif
    call SetDestructableMaxLife(tree, 1500)
    call SetDestructableLife(tree, 1500)
    set tree = null
endfunction

function KLS_StampPlot takes real cx, real cy returns nothing
    local real p = cx - 1024
    local real q = cy - 1024
    loop
        exitwhen p > cx + 1024
        call SetTerrainType(p, cy - 1024, 'Lrok', -1, 1, 0)
        call SetTerrainType(p, cy + 1024, 'Lrok', -1, 1, 0)
        set p = p + 128
    endloop
    loop
        exitwhen q > cy + 1024
        call SetTerrainType(cx - 1024, q, 'Lrok', -1, 1, 0)
        call SetTerrainType(cx + 1024, q, 'Lrok', -1, 1, 0)
        set q = q + 128
    endloop
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
    // Mark all four build plots and resource clearings, including vacant
    // slots in a one-player test so their positions are easy to read.
    loop
        exitwhen i == 4
        call KLS_StampPlot(KLS_X[i], KLS_Y[i])
        // Compact rear-right lumber stand: 650-850 south of the hall.
        // Keep the altar at (-650,-500), mine route and worker spawn clear.
        set j = 0
        loop
            exitwhen j == 4
            call KLS_AddTree(KLS_X[i]+180+j*180,KLS_Y[i]-650)
            if KLS_Ended then
                return
            endif
            call KLS_AddTree(KLS_X[i]+180+j*180,KLS_Y[i]-850)
            if KLS_Ended then
                return
            endif
            set j = j+1
        endloop
        set i = i + 1
    endloop
    // A stone-paved road connects the gates, king's courtyard and southern
    // market. Terrain/pathing extents are generated with the expanded W3E/WPM.
    set y = -7800
    loop
        exitwhen y > 7800
        call SetTerrainType(0, y, 'Lrok', -1, 4, 0)
        set y = y + 128
    endloop
    set gate = null
endfunction

function KLS_PlayerLeft takes nothing returns nothing
    local player departing = GetTriggerPlayer()
    local integer p = GetPlayerId(departing)
    if p < 4 and KLS_Active[p] then
        set KLS_Active[p] = false
        set KLS_Players = KLS_Players-1
        call KLS_Log("Defender left; active players=" + I2S(KLS_Players))
        call KLS_Message(GetPlayerName(departing) + " has left the defense. Their army keeps its current orders.")
        if KLS_Selecting then
            call KLS_FinishSelection()
        endif
        if KLS_Players == 0 then
            call KLS_End(false)
        else
            call KLS_HUDUpdate()
        endif
    endif
    set departing = null
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
    local trigger market = CreateTrigger()
    local trigger leaves = CreateTrigger()
    local real x
    local real y
    local destructable tree
    set KLS_Enemies = CreateGroup()
    call KLS_Log("Initialization entered")
    set KLS_X[0] = -6000
    set KLS_X[1] = -3300
    set KLS_X[2] = 3300
    set KLS_X[3] = 6000
    set KLS_Y[0] = -500
    set KLS_Y[1] = -500
    set KLS_Y[2] = -500
    set KLS_Y[3] = -500
    call KLS_BuildLandscape()
    if KLS_Ended then
        return
    endif
    call KLS_Log("Landscape creation completed")
    call SetPlayerAlliance(Player(PLAYER_NEUTRAL_PASSIVE), Player(11), ALLIANCE_PASSIVE, false)
    call SetPlayerAlliance(Player(11), Player(PLAYER_NEUTRAL_PASSIVE), ALLIANCE_PASSIVE, false)
    // The keep is centered on the marked defense row. King Aldric holds the
    // northern face so incoming undead reach him before the castle.
    set u = KLS_CreateUnit(Player(PLAYER_NEUTRAL_PASSIVE), 'hC01', 0, -500, 270)
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
    set KLS_King = KLS_CreateUnit(Player(PLAYER_NEUTRAL_PASSIVE), 'Hpal', 0, 350, 270)
    if KLS_King == null then
        return
    endif
    call BlzSetUnitName(KLS_King, "King Aldric")
    call BlzSetHeroProperName(KLS_King, "King Aldric")
    call SetHeroLevel(KLS_King, 10, false)
    call BlzSetUnitMaxHP(KLS_King, 15000)
    call SetWidgetLife(KLS_King, 15000)
    call BlzSetUnitBaseDamage(KLS_King, 80, 0)
    call SetUnitAcquireRange(KLS_King, 0)
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
            set u = KLS_CreateUnit(Player(PLAYER_NEUTRAL_PASSIVE), 'ngol', x, y + 1200, 270)
            if u == null then
                return
            endif
            call SetResourceAmount(u, 100000)
            set u = KLS_CreateUnit(Player(i), 'htow', x, y, 270)
            if u == null then
                return
            endif
            set KLS_Altar[i] = KLS_CreateUnit(Player(i), 'h000', x - 650, y - 500, 270)
            if KLS_Altar[i] == null then
                return
            endif
            set j = 0
            loop
                exitwhen j == 5
                set u = KLS_CreateUnit(Player(i), 'hpea', x - 250 + j * 90, y - 300, 270)
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
    call TriggerAddAction(leaves,function KLS_PlayerLeft)
    call TriggerRegisterAnyUnitEventBJ(deaths, EVENT_PLAYER_UNIT_DEATH)
    call TriggerAddAction(deaths, function KLS_Death)
    call TriggerRegisterAnyUnitEventBJ(builds, EVENT_PLAYER_UNIT_CONSTRUCT_START)
    call TriggerAddAction(builds, function KLS_Construct)
    call TriggerAddAction(chats, function KLS_Chat)
    call TriggerRegisterAnyUnitEventBJ(talents, EVENT_PLAYER_HERO_LEVEL)
    call TriggerAddAction(talents, function KLS_TalentLevel)
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
    set market = null
    set leaves = null
endfunction
