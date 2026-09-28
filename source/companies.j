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
    unit array KLS_CompanyHall
    unit array KLS_CompanyYard
    boolean array KLS_CompanyFoundry
endglobals

// GENERATED_COMPANIES

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
    if GetUnitTypeId(barracks) == 'hbar' then
        call KLS_CompanyAddBarracksStock(barracks,p)
    endif
    set barracks = null
endfunction

function KLS_CompanyApplyFoundry takes unit recruit returns nothing
    local integer p
    local integer rawcode
    local real oldMax
    local real newMax
    local real oldLife
    local integer damage
    if recruit == null then
        return
    endif
    set p = GetPlayerId(GetOwningPlayer(recruit))
    set rawcode = GetUnitTypeId(recruit)
    if p >= 0 and p < 4 and KLS_Active[p] then
        if KLS_CompanyFoundry[p] and KLS_HeroChoice[p] >= 0 and GetUnitUserData(recruit) == 0 then
            if rawcode == KLS_CompanyUnitId[KLS_HeroChoice[p]] or rawcode == KLS_CompanySupportId[KLS_HeroChoice[p]] then
                set oldMax = BlzGetUnitMaxHP(recruit)
                set oldLife = GetWidgetLife(recruit)
                set newMax = oldMax*1.20
                set damage = BlzGetUnitBaseDamage(recruit,0)
                call BlzSetUnitMaxHP(recruit,R2I(newMax))
                call SetWidgetLife(recruit,RMinBJ(newMax,oldLife+oldMax*0.20))
                call BlzSetUnitBaseDamage(recruit,R2I(damage*1.20),0)
                call SetUnitUserData(recruit,1)
                call KLS_Log("Royal Foundry applied to "+GetUnitName(recruit)+" for p"+I2S(p+1))
            endif
        endif
    endif
endfunction

function KLS_CompanyFoundryEnum takes nothing returns nothing
    call KLS_CompanyApplyFoundry(GetEnumUnit())
endfunction

function KLS_CompanyProductPrice takes integer rawcode, boolean support returns integer
    local integer i = 0
    loop
        exitwhen i == 17
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
        exitwhen i == 17
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
            call KLS_CompanyApplyFoundry(recruit)
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
        if rawcode == KLS_CompanyHallId then
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
        elseif rawcode == KLS_CompanyFoundryId then
            set KLS_CompanyFoundry[p] = true
            set owned = CreateGroup()
            call GroupEnumUnitsOfPlayer(owned,Player(p),null)
            call ForGroup(owned,function KLS_CompanyFoundryEnum)
            call DestroyGroup(owned)
            set owned = null
            call KLS_Log("Royal Foundry veteran upgrades completed for p"+I2S(p+1))
        elseif rawcode == KLS_CompanySiegeYardId then
            set KLS_CompanyYard[p] = building
            call UnitAddAbility(building,'Aneu')
            call AddUnitToStock(building,KLS_CompanySupportId[KLS_HeroChoice[p]],99,99)
            call SetUnitAcquireRange(building,0)
            call KLS_Log("Siege Yard completed for p"+I2S(p+1)+" support="+GetObjectName(KLS_CompanySupportId[KLS_HeroChoice[p]]))
        elseif rawcode == 'hbar' and KLS_CompanyHall[p] != null then
            call KLS_CompanyAddBarracksStock(building,p)
        endif
    endif
    set building = null
endfunction

function KLS_CompanyInit takes nothing returns nothing
    local integer p = 0
    local trigger constructed = CreateTrigger()
    local trigger sold = CreateTrigger()
    call KLS_CompanyCatalogInit()
    loop
        exitwhen p == 4
        set KLS_HeroChoice[p] = -1
        set KLS_CompanyFoundry[p] = false
        set KLS_CompanyHall[p] = null
        set KLS_CompanyYard[p] = null
        set p = p+1
    endloop
    call TriggerRegisterAnyUnitEventBJ(constructed,EVENT_PLAYER_UNIT_CONSTRUCT_FINISH)
    call TriggerAddAction(constructed,function KLS_CompanyConstructed)
    call TriggerRegisterAnyUnitEventBJ(sold,EVENT_PLAYER_UNIT_SELL)
    call TriggerAddAction(sold,function KLS_CompanySellUnit)
    set constructed = null
    set sold = null
    call KLS_Log("Oathbound Companies initialized for 17 selectable heroes")
endfunction
