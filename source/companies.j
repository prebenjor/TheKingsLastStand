globals
    integer KLS_CompanyHallId = 'kH00'
    integer KLS_CompanyFoundryId = 'kF00'
    integer KLS_CompanySiegeYardId = 'kY00'
    integer array KLS_CompanyUnitId
    integer array KLS_CompanySupportId
    integer array KLS_CompanyBannerAbility
    integer array KLS_CompanyUnitGold
    integer array KLS_CompanyUnitLumber
    integer array KLS_CompanySupportGold
    integer array KLS_CompanySupportLumber
    integer array KLS_HeroChoice
    integer array KLS_FactionTownHallId
    integer array KLS_FactionWorkerId
    integer array KLS_FactionAltarId
    integer array KLS_FactionBarracksId
    integer array KLS_FactionFoodId
    integer array KLS_FactionBlacksmithId
    integer array KLS_FactionArcaneId
    integer array KLS_FactionTowerId
    integer array KLS_FactionHallId
    integer array KLS_FactionFoundryId
    integer array KLS_FactionFoundryRecipeId
    integer array KLS_FactionSiegeYardId
    integer array KLS_PlayerRace
    unit array KLS_CompanyHall
    unit array KLS_CompanyYard
    boolean array KLS_CompanyFoundry
    integer array KLS_CompanyUnitHP
    integer array KLS_CompanySupportHP
    integer array KLS_CompanyUnitDamage
    integer array KLS_CompanySupportDamage
    integer array KLS_CompanyPowerId
    integer array KLS_CompanyPowerDamage
    integer array KLS_CompanyPowerHeal
    integer array KLS_CompanyPowerMana
    boolean array KLS_CompanyPowerSlow
    integer array KLS_CompanyResearchId
    integer array KLS_CompanyResearchRole
    integer array KLS_CompanyResearchBranch
    integer array KLS_CompanyResearchLevel
    integer array KLS_CompanyResearchGold
    integer array KLS_CompanyResearchLumber
    integer array KLS_CompanyResearchRank
    hashtable KLS_CompanyUpgradeData = null
endglobals

// GENERATED_COMPANIES

function KLS_CompanyServiceIndex takes integer rawcode returns integer
    local integer i = 0
    loop
        exitwhen i == 11
        if rawcode == KLS_CompanyResearchId[i] then
            return i
        endif
        set i = i+1
    endloop
    return -1
endfunction

function KLS_CompanyBuildingRole takes unit building returns integer
    local integer rawcode = GetUnitTypeId(building)
    local integer p = GetPlayerId(GetOwningPlayer(building))
    if KLS_IsFactionHall(rawcode) then
        return 0
    elseif KLS_IsFactionFoundry(rawcode) then
        return 1
    elseif KLS_IsFactionSiegeYard(rawcode) then
        return 2
    elseif p >= 0 and p < 4 and rawcode == KLS_FactionArcaneId[KLS_PlayerRace[p]] then
        return 3
    endif
    return -1
endfunction

function KLS_CompanyResearchAllowed takes integer p, integer index returns boolean
    local integer branch = KLS_CompanyResearchBranch[index]
    local integer rank = KLS_CompanyResearchLevel[index]
    if KLS_CompanyResearchRank[p*5+branch] != rank-1 then
        return false
    endif
    if branch == 0 and KLS_Wave < rank*10 and KLS_StoryStage < rank then
        return false
    endif
    return true
endfunction

function KLS_CompanyResearchStock takes unit building returns nothing
    local integer p = GetPlayerId(GetOwningPlayer(building))
    local integer role = KLS_CompanyBuildingRole(building)
    local integer i = 0
    if p < 0 or p >= 4 or not KLS_Active[p] or role < 0 or not LoadBoolean(KLS_CompanyUpgradeData,GetHandleId(building),3) or GetWidgetLife(building) <= 0.405 or GetUnitTypeId(building) == 0 then
        return
    endif
    call UnitAddAbility(building,'Aneu')
    call UnitAddAbility(building,'Apit')
    call UnitAddAbility(building,'Asid')
    call UnitAddAbility(building,'Asud')
    loop
        exitwhen i == 11
        call RemoveItemFromStock(building,KLS_CompanyResearchId[i])
        if KLS_CompanyResearchRole[i] == role and KLS_CompanyResearchAllowed(p,i) then
            call AddItemToStock(building,KLS_CompanyResearchId[i],1,1)
        endif
        set i = i+1
    endloop
endfunction

function KLS_CompanyResearchStockEnum takes nothing returns nothing
    if GetUnitTypeId(GetEnumUnit()) != 0 and LoadBoolean(KLS_CompanyUpgradeData,GetHandleId(GetEnumUnit()),3) then
        call KLS_CompanyResearchStock(GetEnumUnit())
    endif
endfunction

function KLS_CompanyResearchRefresh takes nothing returns nothing
    local integer p = 0
    local group owned = CreateGroup()
    loop
        exitwhen p == 4
        if KLS_Active[p] then
            call GroupEnumUnitsOfPlayer(owned,Player(p),null)
            call ForGroup(owned,function KLS_CompanyResearchStockEnum)
            call GroupClear(owned)
        endif
        set p = p+1
    endloop
    call DestroyGroup(owned)
    set owned = null
endfunction

function KLS_CompanyApplyUpgrades takes unit recruit returns nothing
    local integer p = GetPlayerId(GetOwningPlayer(recruit))
    local integer heroIndex
    local integer rawcode = GetUnitTypeId(recruit)
    local integer key = GetHandleId(recruit)
    local integer baseHP
    local integer baseDamage
    local integer hpBonus
    local integer damageBonus
    local integer armorBonus
    local integer deltaHP
    local real veteran = 0.0
    local real chapter
    if recruit == null or p < 0 or p >= 4 or not KLS_Active[p] or KLS_HeroChoice[p] < 0 then
        return
    endif
    set heroIndex = KLS_HeroChoice[p]
    if rawcode == KLS_CompanyUnitId[heroIndex] then
        set baseHP = KLS_CompanyUnitHP[heroIndex]
        set baseDamage = KLS_CompanyUnitDamage[heroIndex]
    elseif rawcode == KLS_CompanySupportId[heroIndex] then
        set baseHP = KLS_CompanySupportHP[heroIndex]
        set baseDamage = KLS_CompanySupportDamage[heroIndex]
    else
        return
    endif
    if KLS_CompanyFoundry[p] then
        set veteran = 0.20
        call SetUnitUserData(recruit,1)
    endif
    set chapter = 0.05*I2R(KLS_CompanyResearchRank[p*5])
    set hpBonus = R2I(I2R(baseHP)*(veteran+chapter+0.10*I2R(KLS_CompanyResearchRank[p*5+2])))
    set damageBonus = R2I(I2R(baseDamage)*(veteran+chapter+0.10*I2R(KLS_CompanyResearchRank[p*5+1])))
    set armorBonus = 2*KLS_CompanyResearchRank[p*5+2]
    set deltaHP = hpBonus-LoadInteger(KLS_CompanyUpgradeData,key,0)
    call BlzSetUnitMaxHP(recruit,BlzGetUnitMaxHP(recruit)+deltaHP)
    if GetWidgetLife(recruit) > 0.405 then
        call SetWidgetLife(recruit,RMinBJ(I2R(BlzGetUnitMaxHP(recruit)),GetWidgetLife(recruit)+I2R(deltaHP)))
    endif
    call BlzSetUnitBaseDamage(recruit,BlzGetUnitBaseDamage(recruit,0)+damageBonus-LoadInteger(KLS_CompanyUpgradeData,key,1),0)
    call BlzSetUnitRealField(recruit,UNIT_RF_DEFENSE,BlzGetUnitRealField(recruit,UNIT_RF_DEFENSE)+I2R(armorBonus-LoadInteger(KLS_CompanyUpgradeData,key,2)))
    call SaveInteger(KLS_CompanyUpgradeData,key,0,hpBonus)
    call SaveInteger(KLS_CompanyUpgradeData,key,1,damageBonus)
    call SaveInteger(KLS_CompanyUpgradeData,key,2,armorBonus)
endfunction

function KLS_CompanyUpgradeEnum takes nothing returns nothing
    call KLS_CompanyApplyUpgrades(GetEnumUnit())
endfunction

function KLS_CompanyResearchBuy takes unit shop, unit buyer, item service returns nothing
    local integer index = KLS_CompanyServiceIndex(GetItemTypeId(service))
    local integer p = GetPlayerId(GetOwningPlayer(buyer))
    local integer branch
    local group owned
    local real dx = GetUnitX(buyer)-GetUnitX(shop)
    local real dy = GetUnitY(buyer)-GetUnitY(shop)
    if index < 0 then
        return
    endif
    if p < 0 or p >= 4 then
        call RemoveItem(service)
        return
    endif
    if KLS_Ended or not KLS_Active[p] or buyer != KLS_Hero[p] or GetOwningPlayer(shop) != Player(p) or GetWidgetLife(buyer) <= 0.405 or dx*dx+dy*dy > 490000.0 or KLS_CompanyBuildingRole(shop) != KLS_CompanyResearchRole[index] or not KLS_CompanyResearchAllowed(p,index) then
        call SetPlayerState(Player(p),PLAYER_STATE_RESOURCE_GOLD,GetPlayerState(Player(p),PLAYER_STATE_RESOURCE_GOLD)+KLS_CompanyResearchGold[index])
        call SetPlayerState(Player(p),PLAYER_STATE_RESOURCE_LUMBER,GetPlayerState(Player(p),PLAYER_STATE_RESOURCE_LUMBER)+KLS_CompanyResearchLumber[index])
        call DisplayTimedTextToPlayer(Player(p),0,0,6,"Research requires your living hero at your matching building and the next unlocked rank. Costs refunded.")
    else
        set branch = KLS_CompanyResearchBranch[index]
        set KLS_CompanyResearchRank[p*5+branch] = KLS_CompanyResearchLevel[index]
        set owned = CreateGroup()
        call GroupEnumUnitsOfPlayer(owned,Player(p),null)
        call ForGroup(owned,function KLS_CompanyUpgradeEnum)
        call DestroyGroup(owned)
        set owned = null
        call DisplayTimedTextToPlayer(Player(p),0,0,6,GetItemName(service)+" completed for your company.")
    endif
    call RemoveItem(service)
    call KLS_CompanyResearchRefresh()
endfunction

function KLS_CompanyPowerCast takes nothing returns nothing
    local unit caster = GetTriggerUnit()
    local integer p = GetPlayerId(GetOwningPlayer(caster))
    local integer index
    local integer expected
    local group targets
    local unit target
    local unit dummy
    local real potency
    local real x = GetSpellTargetX()
    local real y = GetSpellTargetY()
    if p < 0 or p >= 4 or not KLS_Active[p] or KLS_Ended or KLS_HeroChoice[p] < 0 then
        set caster = null
        return
    endif
    set index = KLS_HeroChoice[p]*2
    if GetUnitTypeId(caster) == KLS_CompanySupportId[KLS_HeroChoice[p]] then
        set index = index+1
    elseif GetUnitTypeId(caster) != KLS_CompanyUnitId[KLS_HeroChoice[p]] then
        set caster = null
        return
    endif
    if GetSpellAbilityId() != KLS_CompanyPowerId[index] then
        set caster = null
        return
    endif
    set potency = 1.0+0.15*I2R(KLS_CompanyResearchRank[p*5])
    if ModuloInteger(index,2) == 1 then
        set potency = potency+0.25*I2R(KLS_CompanyResearchRank[p*5+4])
    endif
    set targets = CreateGroup()
    call GroupEnumUnitsInRange(targets,x,y,250,null)
    loop
        set target = FirstOfGroup(targets)
        exitwhen target == null
        call GroupRemoveUnit(targets,target)
        if GetWidgetLife(target) > 0.405 and not IsUnitType(target,UNIT_TYPE_STRUCTURE) then
            if IsUnitEnemy(target,Player(p)) then
                call UnitDamageTarget(caster,target,I2R(KLS_CompanyPowerDamage[index])*potency,false,false,ATTACK_TYPE_NORMAL,DAMAGE_TYPE_MAGIC,WEAPON_TYPE_WHOKNOWS)
                if KLS_CompanyPowerSlow[index] then
                    set dummy = KLS_CreateUnitOptional(Player(p),'hS01',GetUnitX(target),GetUnitY(target),0,"company slow")
                    if dummy != null then
                        call IssueTargetOrder(dummy,"slow",target)
                        call UnitApplyTimedLife(dummy,'BTLF',3)
                    endif
                endif
            elseif IsUnitAlly(target,Player(p)) and target != KLS_King then
                call SetWidgetLife(target,RMinBJ(I2R(BlzGetUnitMaxHP(target)),GetWidgetLife(target)+I2R(KLS_CompanyPowerHeal[index])*potency))
                call SetUnitState(target,UNIT_STATE_MANA,RMinBJ(GetUnitState(target,UNIT_STATE_MAX_MANA),GetUnitState(target,UNIT_STATE_MANA)+I2R(KLS_CompanyPowerMana[index])*potency))
            endif
        endif
    endloop
    call DestroyGroup(targets)
    set targets = null
    set caster = null
    set target = null
    set dummy = null
endfunction

function KLS_CompanyCounterSiege takes nothing returns nothing
    local unit attacker = GetEventDamageSource()
    local unit target = GetTriggerUnit()
    local integer p = GetPlayerId(GetOwningPlayer(attacker))
    if p >= 0 and p < 4 and KLS_Active[p] and KLS_HeroChoice[p] >= 0 and KLS_CompanyResearchRank[p*5+3] > 0 and BlzGetEventIsAttack() and GetEventDamage() > 0.0 then
        if GetUnitTypeId(attacker) == KLS_CompanySupportId[KLS_HeroChoice[p]] and IsUnitEnemy(target,Player(p)) and (IsUnitType(target,UNIT_TYPE_STRUCTURE) or KLS_IsSiegeInvader(GetUnitTypeId(target))) then
            call BlzSetEventDamage(GetEventDamage()*1.50)
        endif
    endif
    set attacker = null
    set target = null
endfunction

function KLS_CompanyAddBarracksStock takes unit barracks, integer p returns nothing
    if p >= 0 and p < 4 and barracks != null and KLS_CompanyHall[p] != null and KLS_HeroChoice[p] >= 0 then
        call UnitAddAbility(barracks,'Aneu')
        call AddUnitToStock(barracks,KLS_CompanyUnitId[KLS_HeroChoice[p]],99,99)
        call SetUnitAcquireRange(barracks,0)
        call KLS_Log("Company stock unlocked: "+GetUnitName(barracks)+" has "+GetObjectName(KLS_CompanyUnitId[KLS_HeroChoice[p]]))
    endif
endfunction

function KLS_CompanyBarracksEnum takes nothing returns nothing
    local unit barracks = GetEnumUnit()
    local integer p = GetPlayerId(GetOwningPlayer(barracks))
    if KLS_IsFactionBarracks(GetUnitTypeId(barracks)) then
        call KLS_CompanyAddBarracksStock(barracks,p)
    endif
    set barracks = null
endfunction

function KLS_CompanyApplyFoundry takes unit recruit returns nothing
    call KLS_CompanyApplyUpgrades(recruit)
endfunction

function KLS_CompanyFoundryEnum takes nothing returns nothing
    call KLS_CompanyApplyFoundry(GetEnumUnit())
endfunction

// Native stock purchase creates a fresh unit. Its recycled numeric handle must
// never inherit previous company totals. Preserve the table on ordinary death
// so a resurrected unit keeps its already-applied bonuses without double gains.
function KLS_CompanyPrepareNewRecruit takes unit recruit returns nothing
    call FlushChildHashtable(KLS_CompanyUpgradeData,GetHandleId(recruit))
    call KLS_CompanyApplyUpgrades(recruit)
endfunction

function KLS_CompanyConstructionStarted takes nothing returns nothing
    call FlushChildHashtable(KLS_CompanyUpgradeData,GetHandleId(GetConstructingStructure()))
endfunction

function KLS_CompanyProductPrice takes integer rawcode, boolean support returns integer
    local integer i = 0
    loop
        exitwhen i == KLS_HeroCount
        if support then
            if rawcode == KLS_CompanySupportId[i] then
                return KLS_CompanySupportGold[i]
            endif
        elseif rawcode == KLS_CompanyUnitId[i] then
            return KLS_CompanyUnitGold[i]
        endif
        set i = i+1
    endloop
    return 0
endfunction

function KLS_CompanyProductLumber takes integer rawcode, boolean support returns integer
    local integer i = 0
    loop
        exitwhen i == KLS_HeroCount
        if support then
            if rawcode == KLS_CompanySupportId[i] then
                return KLS_CompanySupportLumber[i]
            endif
        elseif rawcode == KLS_CompanyUnitId[i] then
            return KLS_CompanyUnitLumber[i]
        endif
        set i = i+1
    endloop
    return 0
endfunction

function KLS_CompanySellUnit takes nothing returns nothing
    local unit shop = GetSellingUnit()
    local unit buyer = GetBuyingUnit()
    local unit recruit = GetSoldUnit()
    local integer p = 4
    local integer shopOwner = 4
    local integer rawcode = 0
    local integer gold = 0
    local integer lumber = 0
    local boolean support = false
    if buyer != null then
        set p = GetPlayerId(GetOwningPlayer(buyer))
    endif
    if shop != null then
        set shopOwner = GetPlayerId(GetOwningPlayer(shop))
    endif
    if recruit != null then
        set rawcode = GetUnitTypeId(recruit)
    endif
    if rawcode != 0 then
        set support = KLS_CompanyProductPrice(rawcode,true) > 0
        set gold = KLS_CompanyProductPrice(rawcode,support)
        set lumber = KLS_CompanyProductLumber(rawcode,support)
    endif
    if p >= 0 and p < 4 and rawcode != 0 and gold > 0 then
        if not KLS_Active[p] or shopOwner != p or buyer != KLS_Hero[p] or KLS_Ended then
            call RemoveUnit(recruit)
            call SetPlayerState(Player(p),PLAYER_STATE_RESOURCE_GOLD,GetPlayerState(Player(p),PLAYER_STATE_RESOURCE_GOLD)+gold)
            call SetPlayerState(Player(p),PLAYER_STATE_RESOURCE_LUMBER,GetPlayerState(Player(p),PLAYER_STATE_RESOURCE_LUMBER)+lumber)
            call DisplayTimedTextToPlayer(Player(p),0,0,6,"That company is personal to its owner. Your resources were refunded.")
            call KLS_Log("Rejected company purchase from a mismatched Barracks/Siege Yard; refunded p"+I2S(p+1))
        else
            call KLS_CompanyPrepareNewRecruit(recruit)
            call AddUnitToStock(shop,rawcode,1,99)
            call KLS_Log("Company unit trained for p"+I2S(p+1)+": "+GetUnitName(recruit))
        endif
    endif
    set shop = null
    set buyer = null
    set recruit = null
endfunction

function KLS_CompanyConstructed takes nothing returns nothing
    local unit building = GetConstructedStructure()
    local integer p = GetPlayerId(GetOwningPlayer(building))
    local integer rawcode = GetUnitTypeId(building)
    local group owned
    local integer doctrine
    if p >= 0 and p < 4 and KLS_Active[p] and KLS_HeroChoice[p] >= 0 then
        if KLS_IsFactionHall(rawcode) then
            set KLS_CompanyHall[p] = building
            set doctrine = KLS_CompanyBannerAbility[KLS_HeroChoice[p]]
            call UnitAddAbility(building,doctrine)
            call UnitMakeAbilityPermanent(building,true,doctrine)
            set owned = CreateGroup()
            call GroupEnumUnitsOfPlayer(owned,Player(p),null)
            call ForGroup(owned,function KLS_CompanyBarracksEnum)
            call DestroyGroup(owned)
            set owned = null
            call KLS_Log("Hall of Banners completed for p"+I2S(p+1)+" doctrine="+GetObjectName(doctrine))
        elseif KLS_IsFactionFoundry(rawcode) then
            set KLS_CompanyFoundry[p] = true
            call UnitAddAbility(building,'Aneu')
            call UnitAddAbility(building,'Apit')
            call UnitAddAbility(building,'Asid')
            call UnitAddAbility(building,'Asud')
            call AddItemToStock(building,KLS_FactionFoundryRecipeId[KLS_PlayerRace[p]],1,1)
            call SetUnitAcquireRange(building,0)
            set owned = CreateGroup()
            call GroupEnumUnitsOfPlayer(owned,Player(p),null)
            call ForGroup(owned,function KLS_CompanyFoundryEnum)
            call DestroyGroup(owned)
            set owned = null
            call KLS_Log("Royal Foundry veteran upgrades and racial Legendary pattern stock completed for p"+I2S(p+1))
        elseif KLS_IsFactionSiegeYard(rawcode) then
            set KLS_CompanyYard[p] = building
            call UnitAddAbility(building,'Aneu')
            call AddUnitToStock(building,KLS_CompanySupportId[KLS_HeroChoice[p]],99,99)
            call SetUnitAcquireRange(building,0)
            call KLS_Log("Siege Yard completed for p"+I2S(p+1)+" support="+GetObjectName(KLS_CompanySupportId[KLS_HeroChoice[p]]))
        elseif KLS_IsFactionBarracks(rawcode) and KLS_CompanyHall[p] != null then
            call KLS_CompanyAddBarracksStock(building,p)
        endif
    endif
    call SaveBoolean(KLS_CompanyUpgradeData,GetHandleId(building),3,true)
    call KLS_CompanyResearchStock(building)
    set building = null
endfunction

function KLS_CompanyInit takes nothing returns nothing
    local integer p = 0
    local trigger constructed = CreateTrigger()
    local trigger starting = CreateTrigger()
    local trigger sold = CreateTrigger()
    local trigger powers = CreateTrigger()
    local trigger counter = CreateTrigger()
    set KLS_CompanyUpgradeData = InitHashtable()
    call KLS_CompanyCatalogInit()
    call KLS_FactionCatalogInit()
    loop
        exitwhen p == 4
        set KLS_HeroChoice[p] = -1
        set KLS_CompanyFoundry[p] = false
        set KLS_CompanyHall[p] = null
        set KLS_CompanyYard[p] = null
        set p = p+1
    endloop
    call TriggerRegisterAnyUnitEventBJ(starting,EVENT_PLAYER_UNIT_CONSTRUCT_START)
    call TriggerAddAction(starting,function KLS_CompanyConstructionStarted)
    call TriggerRegisterAnyUnitEventBJ(constructed,EVENT_PLAYER_UNIT_CONSTRUCT_FINISH)
    call TriggerAddAction(constructed,function KLS_CompanyConstructed)
    call TriggerRegisterAnyUnitEventBJ(sold,EVENT_PLAYER_UNIT_SELL)
    call TriggerAddAction(sold,function KLS_CompanySellUnit)
    call TriggerRegisterAnyUnitEventBJ(powers,EVENT_PLAYER_UNIT_SPELL_EFFECT)
    call TriggerAddAction(powers,function KLS_CompanyPowerCast)
    call TriggerRegisterAnyUnitEventBJ(counter,EVENT_PLAYER_UNIT_DAMAGED)
    call TriggerAddAction(counter,function KLS_CompanyCounterSiege)
    set powers = null
    set counter = null
    set starting = null
    set constructed = null
    set sold = null
    call KLS_Log("Race-matched companies, workers, buildings and towers initialized for 25 heroes")
endfunction
