globals
    boolean KLS_Selecting = true
    integer KLS_SelectionLeft = 45
    integer KLS_HeroCount = 25
    integer array KLS_HeroType
    string array KLS_HeroName
    string array KLS_HeroDescription
    integer array KLS_HeroRace
    texttag array KLS_PreviewLabel
    unit array KLS_Preview
    integer array KLS_Candidate
    button array KLS_Confirm
    button array KLS_Back
endglobals

function KLS_ReleaseStartingUnit takes nothing returns nothing
    call PauseUnit(GetEnumUnit(), false)
endfunction

function KLS_ConfigureStartingMine takes integer p, integer raceId returns nothing
    local integer mineType = 0
    local integer amount = 1000000
    local real x
    local real y
    local real facing
    local unit ownedMine
    if p < 0 or p >= 4 or KLS_BaseMine[p] == null then
        return
    endif
    if raceId == 2 then
        set mineType = 'egol'
    elseif raceId == 3 then
        set mineType = 'ugol'
    endif
    if mineType == 0 then
        call SetResourceAmount(KLS_BaseMine[p],amount)
        call KLS_Log("Starting mine reserve normalized race="+KLS_RaceName(raceId)+" type="+GetObjectName(GetUnitTypeId(KLS_BaseMine[p]))+" player="+I2S(p+1)+" gold="+I2S(amount))
        return
    endif
    set x = GetUnitX(KLS_BaseMine[p])
    set y = GetUnitY(KLS_BaseMine[p])
    set facing = GetUnitFacing(KLS_BaseMine[p])
    set ownedMine = KLS_CreateUnitChecked(Player(p),mineType,x,y,facing,true,"starting racial gold mine")
    if ownedMine == null then
        return
    endif
    call SetResourceAmount(ownedMine,amount)
    call RemoveUnit(KLS_BaseMine[p])
    set KLS_BaseMine[p] = ownedMine
    call KLS_Log("Starting mine configured race="+KLS_RaceName(raceId)+" type="+GetObjectName(GetUnitTypeId(ownedMine))+" player="+I2S(p+1)+" gold="+I2S(amount))
    set ownedMine = null
endfunction

function KLS_ReplaceStartingFaction takes integer p, integer heroIndex returns nothing
    local integer raceId = KLS_HeroRace[heroIndex]
    local integer workerIndex = 0
    local integer rawcode
    local racepreference racePreference
    local real x = KLS_X[p]
    local real y = KLS_Y[p]
    local unit candidate
    local unit created
    local group owned = CreateGroup()
    set KLS_PlayerRace[p] = raceId
    if raceId == 0 then
        set racePreference = RACE_PREF_HUMAN
    elseif raceId == 1 then
        set racePreference = RACE_PREF_ORC
    elseif raceId == 2 then
        set racePreference = RACE_PREF_NIGHTELF
    else
        set racePreference = RACE_PREF_UNDEAD
    endif
    call SetPlayerRacePreference(Player(p),racePreference)
    call KLS_ConfigureStartingMine(p,raceId)
    if raceId != 0 then
        call GroupEnumUnitsOfPlayer(owned,Player(p),null)
        loop
            set candidate = FirstOfGroup(owned)
            exitwhen candidate == null
            call GroupRemoveUnit(owned,candidate)
            set rawcode = GetUnitTypeId(candidate)
            if candidate != KLS_Hero[p] and (rawcode == 'htow' or rawcode == 'h000' or rawcode == 'hpea') then
                call RemoveUnit(candidate)
            endif
        endloop
        set created = KLS_CreateUnit(Player(p),KLS_FactionTownHallId[raceId],x,y,270)
        if created == null then
            call DestroyGroup(owned)
            return
        endif
        call PauseUnit(created,true)
        set KLS_BaseTownHall[p] = created
        set KLS_Altar[p] = KLS_CreateUnit(Player(p),KLS_FactionAltarId[raceId],x+KLS_AltarOffsetX,y+KLS_AltarOffsetY,270)
        if KLS_Altar[p] == null then
            call DestroyGroup(owned)
            return
        endif
        call PauseUnit(KLS_Altar[p],true)
        set workerIndex = 0
        loop
            exitwhen workerIndex == 5
            set created = KLS_CreateUnit(Player(p),KLS_FactionWorkerId[raceId],x+KLS_WorkerOffsetX+workerIndex*90,y+KLS_WorkerOffsetY,270)
            if created == null then
                call DestroyGroup(owned)
                return
            endif
            call PauseUnit(created,true)
            if workerIndex == 0 then
                set KLS_FirstWorker[p] = created
            endif
            set workerIndex = workerIndex+1
        endloop
    endif
    call KLS_Log("Hero race selected for p"+I2S(p+1)+": "+KLS_RaceName(raceId)+" worker="+GetUnitName(KLS_FirstWorker[p]))
    call DestroyGroup(owned)
    set owned = null
    set candidate = null
    set created = null
    set racePreference = null
endfunction

function KLS_FinishSelection takes nothing returns nothing
    local integer p = 0
    local integer n = 0
    local group army = CreateGroup()
    loop
        exitwhen p == 4
        if KLS_Active[p] and not KLS_ClassChosen[p] then
            call DestroyGroup(army)
            set army = null
            return
        endif
        set p = p + 1
    endloop
    call KLS_LockDifficulty()
    call KLS_Log("Difficulty locked: "+KLS_DifficultyName(KLS_Difficulty)+"; votes="+KLS_DifficultyTallyText())
    call KLS_ResetReadyVotes()
    call KLS_Log("Selection complete; preparation starts at 45 seconds")
    set KLS_Selecting = false
    set KLS_Prep = 45
    loop
        exitwhen n == KLS_HeroCount
        call DestroyTextTag(KLS_PreviewLabel[n])
        set KLS_PreviewLabel[n] = null
        call RemoveUnit(KLS_Preview[n])
        set KLS_Preview[n] = null
        set n = n + 1
    endloop
    set p = 0
    loop
        exitwhen p == 4
        if KLS_Active[p] then
            call GroupEnumUnitsOfPlayer(army, Player(p), null)
            call ForGroup(army, function KLS_ReleaseStartingUnit)
            call GroupClear(army)
            call DisplayTimedTextToPlayer(Player(p), 0, 0, 10, "All heroes ready. Prepare your defenses: 45 seconds until wave 1.")
        endif
        set p = p + 1
    endloop
    call DestroyGroup(army)
    set army = null
endfunction

function KLS_ChooseHero takes integer p, integer n returns nothing
    if p < 0 or p >= 4 or n < 0 or n >= KLS_HeroCount then
        return
    endif
    if not KLS_Selecting or not KLS_Active[p] or KLS_ClassChosen[p] or KLS_Ended then
        return
    endif
    call KLS_Log("Hero choice player=" + I2S(p) + " hero=" + KLS_HeroName[n])
    set KLS_Hero[p] = KLS_CreateUnit(Player(p), KLS_HeroType[n], GetUnitX(KLS_Altar[p]), GetUnitY(KLS_Altar[p]) - 250, 270)
    if KLS_Hero[p] == null then
        return
    endif
    set KLS_HeroChoice[p] = n
    set KLS_ClassChosen[p] = true
    call KLS_ReplaceStartingFaction(p,n)
    call DialogDisplay(Player(p), KLS_ClassDialog[p], false)
    call BlzSetUnitName(KLS_Hero[p], KLS_HeroName[n])
    call SetHeroLevel(KLS_Hero[p], 1, false)
    call UnitModifySkillPoints(KLS_Hero[p],1-GetHeroSkillPoints(KLS_Hero[p]))
    call SetHeroXP(KLS_Hero[p], 0, false)
    call KLS_Log("Hero progression initialized player="+I2S(p+1)+" level="+I2S(GetHeroLevel(KLS_Hero[p]))+" xp="+I2S(GetHeroXP(KLS_Hero[p])))
    set KLS_LastTalentMilestone[p] = GetHeroLevel(KLS_Hero[p]) / 5
    call UnitAddAbility(KLS_Hero[p], KLS_SignatureId[n])
    call UnitMakeAbilityPermanent(KLS_Hero[p], true, KLS_SignatureId[n])
    call UnitAddItemById(KLS_Hero[p], 'stwp')
    call UnitAddItemById(KLS_Hero[p], 'ebac')
    if UnitExtendedInventorySize(KLS_Hero[p]) != 30 then
        call KLS_Log("ERROR FK backpack storage=" + I2S(UnitExtendedInventorySize(KLS_Hero[p])) + " expected=30")
    else
        call KLS_Log("FK backpack verified: storage=30, equipment UI abilities installed")
    endif
    call PauseUnit(KLS_Hero[p], true)
    if GetLocalPlayer() == Player(p) then
        call SetCameraBounds(-11520, -11520, 11520, 11520, -11520, 11520, 11520, -11520)
        call SetCameraField(CAMERA_FIELD_TARGET_DISTANCE, 1650, 0)
        call PanCameraToTimed(GetUnitX(KLS_Hero[p]), GetUnitY(KLS_Hero[p]), 0)
        call ClearSelection()
        call SelectUnit(KLS_Hero[p], true)
    endif
    call DisplayTimedTextToPlayer(Player(p), 0, 0, 8, "Hero confirmed. Waiting for the other defenders to choose.")
    call KLS_FinishSelection()
endfunction

function KLS_ClassClick takes nothing returns nothing
    local integer p = GetPlayerId(GetTriggerPlayer())
    if p < 4 and GetClickedButton() == KLS_Confirm[p] then
        call KLS_ChooseHero(p, KLS_Candidate[p])
    elseif p < 4 and GetLocalPlayer() == Player(p) then
        call ClearSelection()
    endif
endfunction

function KLS_PreviewSelected takes nothing returns nothing
    local integer p = GetPlayerId(GetTriggerPlayer())
    local integer n = 0
    if p >= 4 or not KLS_Selecting or KLS_ClassChosen[p] or not KLS_Active[p] then
        return
    endif
    loop
        exitwhen n == KLS_HeroCount
        if GetTriggerUnit() == KLS_Preview[n] then
            set KLS_Candidate[p] = n
            call DialogClear(KLS_ClassDialog[p])
            call DialogSetMessage(KLS_ClassDialog[p], KLS_HeroName[n] + "|n|n" + KLS_HeroDescription[n] + "|n|nBonus ability: " + KLS_SignatureName[n] + "|n" + KLS_SignatureDescription[n])
            set KLS_Confirm[p] = DialogAddButton(KLS_ClassDialog[p], "Confirm " + KLS_HeroName[n], 0)
            set KLS_Back[p] = DialogAddButton(KLS_ClassDialog[p], "Back to heroes", 0)
            call DialogDisplay(Player(p), KLS_ClassDialog[p], true)
            return
        endif
        set n = n + 1
    endloop
endfunction

function KLS_SelectionTick takes nothing returns nothing
    local integer p = 0
    set KLS_SelectionLeft = KLS_SelectionLeft - 1
    loop
        exitwhen p == 4
        if KLS_Active[p] and GetPlayerSlotState(Player(p)) != PLAYER_SLOT_STATE_PLAYING then
            set KLS_Active[p] = false
            set KLS_Players = KLS_Players - 1
        endif
        if KLS_Active[p] and not KLS_ClassChosen[p] and KLS_SelectionLeft <= 0 then
            call KLS_ChooseHero(p, 0)
        endif
        set p = p + 1
    endloop
    if KLS_Selecting then
        call KLS_FinishSelection()
    endif
endfunction

function KLS_PauseStartingUnit takes nothing returns nothing
    call PauseUnit(GetEnumUnit(), true)
endfunction

function KLS_SelectionInit takes nothing returns nothing
    local integer n = 0
    local integer p = 0
    local real x
    local real y
    local texttag label
    local trigger previews = CreateTrigger()
    local group army = CreateGroup()
    set KLS_HeroType[0] = 'Hpal'
    set KLS_HeroName[0] = "Paladin"
    set KLS_HeroDescription[0] = "Frontline support: Holy Light heals living allies or harms undead; Divine Shield, Devotion Aura, Resurrection."
    set KLS_HeroType[1] = 'Hmkg'
    set KLS_HeroName[1] = "Mountain King"
    set KLS_HeroDescription[1] = "Melee control: Storm Bolt, Thunder Clap, Bash and Avatar."
    set KLS_HeroType[2] = 'H000'
    set KLS_HeroName[2] = "Priest"
    set KLS_HeroDescription[2] = "Healer: Holy Light, Brilliance Aura, Divine Shield and Resurrection."
    set KLS_HeroType[3] = 'Hblm'
    set KLS_HeroName[3] = "Blood Mage"
    set KLS_HeroDescription[3] = "Area damage: Flame Strike, Banish, Siphon Mana and Phoenix."
    set KLS_HeroType[4] = 'Obla'
    set KLS_HeroName[4] = "Blademaster"
    set KLS_HeroDescription[4] = "Melee damage: Wind Walk, Mirror Image, Critical Strike and Bladestorm."
    set KLS_HeroType[5] = 'Ofar'
    set KLS_HeroName[5] = "Far Seer"
    set KLS_HeroDescription[5] = "Ranged summoner: Chain Lightning, Far Sight, Spirit Wolves and Earthquake."
    set KLS_HeroType[6] = 'Otch'
    set KLS_HeroName[6] = "Tauren Chieftain"
    set KLS_HeroDescription[6] = "Frontline control: Shockwave, War Stomp, Endurance Aura and Reincarnation."
    set KLS_HeroType[7] = 'Oshd'
    set KLS_HeroName[7] = "Shadow Hunter"
    set KLS_HeroDescription[7] = "Support: Healing Wave, Hex, Serpent Ward and Big Bad Voodoo."
    set KLS_HeroType[8] = 'Edem'
    set KLS_HeroName[8] = "Demon Hunter"
    set KLS_HeroDescription[8] = "Melee damage: Mana Burn, Immolation, Evasion and Metamorphosis."
    set KLS_HeroType[9] = 'Ekee'
    set KLS_HeroName[9] = "Keeper of the Grove"
    set KLS_HeroDescription[9] = "Control and healing: Entangling Roots, tree-free Briar Host, Thorns Aura and Tranquility, plus Grove Awakening."
    set KLS_HeroType[10] = 'Emoo'
    set KLS_HeroName[10] = "Priestess of the Moon"
    set KLS_HeroDescription[10] = "Ranged support: Scout, Searing Arrows, Trueshot Aura and Starfall."
    set KLS_HeroType[11] = 'Ewar'
    set KLS_HeroName[11] = "Warden"
    set KLS_HeroDescription[11] = "Mobile damage: Fan of Knives, Blink, Shadow Strike and Vengeance."
    set KLS_HeroType[12] = 'Udea'
    set KLS_HeroName[12] = "Death Knight"
    set KLS_HeroDescription[12] = "Frontline support: Death Coil heals undead or harms living enemies; Death Pact, Unholy Aura and Animate Dead."
    set KLS_HeroType[13] = 'Ulic'
    set KLS_HeroName[13] = "Lich"
    set KLS_HeroDescription[13] = "Area damage: Frost Nova, Frost Armor, Dark Ritual and Death and Decay."
    set KLS_HeroType[14] = 'Nbrn'
    set KLS_HeroName[14] = "Dark Ranger"
    set KLS_HeroDescription[14] = "Ranged control: Silence, Black Arrow, Life Drain and Charm."
    set KLS_HeroType[15] = 'Hjsm'
    set KLS_HeroName[15] = "Ilastar, Human"
    set KLS_HeroDescription[15] = "Support caster: Sacred Aura, Sacred Flame - Light's Mercy, Mind Control and Surge of Light."
    set KLS_HeroType[16] = 'Npal'
    set KLS_HeroName[16] = "Forsaken Paladin"
    set KLS_HeroDescription[16] = "Frontline purifier: Consecration, Righteous Fury, Sacred Aura and Cleansing Fire."
    // GENERATED_HERO_CATALOG
    loop
        exitwhen n == KLS_HeroCount
        set x = KLS_HeroHubX + ModuloInteger(n, KLS_HubColumns) * KLS_HubSpacing
        set y = KLS_HeroHubY + (n / KLS_HubColumns) * KLS_HubSpacing
        set KLS_Preview[n] = KLS_CreateUnit(Player(PLAYER_NEUTRAL_PASSIVE), KLS_HeroType[n], x, y, 270)
        if KLS_Preview[n] == null then
            return
        endif
        call SetUnitInvulnerable(KLS_Preview[n], true)
        call PauseUnit(KLS_Preview[n], true)
        call SetUnitPathing(KLS_Preview[n], false)
        call SetHeroLevel(KLS_Preview[n], 1, false)
        call BlzSetUnitName(KLS_Preview[n], KLS_HeroName[n])
        set label = CreateTextTag()
        set KLS_PreviewLabel[n] = label
        call SetTextTagText(label, KLS_HeroName[n], 0.017)
        call SetTextTagPos(label, x - 150, y - 100, 100)
        call SetTextTagColor(label, 255, 220, 100, 255)
        set n = n + 1
    endloop
    call TriggerRegisterAnyUnitEventBJ(previews, EVENT_PLAYER_UNIT_SELECTED)
    call TriggerAddAction(previews, function KLS_PreviewSelected)
    loop
        exitwhen p == 4
        if KLS_Active[p] then
            call GroupEnumUnitsOfPlayer(army, Player(p), null)
            call ForGroup(army, function KLS_PauseStartingUnit)
            call GroupClear(army)
            if GetLocalPlayer() == Player(p) then
                call ClearSelection()
                call SetCameraBounds(-11520, -11520, -8200, -8200, -11520, -8200, -8200, -11520)
                call SetCameraField(CAMERA_FIELD_TARGET_DISTANCE, 2600, 0)
                call PanCameraToTimed(-10000, -10000, 0)
            endif
            call DisplayTimedTextToPlayer(Player(p), 0, 0, 30, "Choose your hero: click one of the 25 hero previews, read their abilities, then confirm. Duplicate choices are allowed. Paladin is chosen automatically after 45 seconds.")
        endif
        set p = p + 1
    endloop
    call DestroyGroup(army)
    set army = null
    set previews = null
    set label = null
endfunction
