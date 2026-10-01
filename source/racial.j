globals
    integer array KLS_SpecialistId
    integer array KLS_SpecialistAbility
    integer array KLS_SpecialistHP
    integer array KLS_SpecialistDamage
    hashtable KLS_RacialData = null
endglobals

// GENERATED_RACIAL_CATALOG

function KLS_SpecialistIndex takes integer rawcode returns integer
    local integer i = 0
    loop
        exitwhen i == 8
        if rawcode == KLS_SpecialistId[i] then
            return i
        endif
        set i = i+1
    endloop
    return -1
endfunction

function KLS_RacialExpire takes integer key returns nothing
    local unit target = LoadUnitHandle(KLS_RacialData,key,0)
    local integer kind = LoadInteger(KLS_RacialData,key,3)
    local real value = LoadReal(KLS_RacialData,key,5)
    local timer clock = LoadTimerHandle(KLS_RacialData,key,8)
    if target != null and GetUnitTypeId(target) != 0 then
        if kind == 0 or kind == 7 then
            call BlzSetUnitRealField(target,UNIT_RF_DEFENSE,BlzGetUnitRealField(target,UNIT_RF_DEFENSE)-value)
        elseif kind == 2 then
            call SetUnitMoveSpeed(target,GetUnitMoveSpeed(target)/(1.0-value))
        elseif kind == 3 then
            call BlzSetUnitAttackCooldown(target,BlzGetUnitAttackCooldown(target,0)*(1.0+value),0)
            if BlzGetUnitAttackCooldown(target,1) > 0.0 then
                call BlzSetUnitAttackCooldown(target,BlzGetUnitAttackCooldown(target,1)*(1.0+value),1)
            endif
        elseif kind == 4 then
            call UnitRemoveAbility(target,'rBr0')
            call UnitRemoveAbility(target,'rBa0')
        endif
    endif
    if target != null and LoadTimerHandle(KLS_RacialData,GetHandleId(target),100+kind) == clock then
        call RemoveSavedHandle(KLS_RacialData,GetHandleId(target),100+kind)
    endif
    call PauseTimer(clock)
    call DestroyTimer(clock)
    call FlushChildHashtable(KLS_RacialData,key)
    set target = null
    set clock = null
endfunction

function KLS_RacialTick takes nothing returns nothing
    local timer clock = GetExpiredTimer()
    local integer key = GetHandleId(clock)
    local unit target = LoadUnitHandle(KLS_RacialData,key,0)
    local unit caster = LoadUnitHandle(KLS_RacialData,key,1)
    local integer kind = LoadInteger(KLS_RacialData,key,3)
    local integer ticks = LoadInteger(KLS_RacialData,key,4)-1
    local real power = LoadReal(KLS_RacialData,key,6)
    if target == null or caster == null or GetUnitTypeId(target) == 0 or GetWidgetLife(target) <= 0.405 or GetWidgetLife(caster) <= 0.405 or GetOwningPlayer(target) != LoadPlayerHandle(KLS_RacialData,key,2) or GetOwningPlayer(caster) != LoadPlayerHandle(KLS_RacialData,key,7) then
        call KLS_RacialExpire(key)
    else
        if ModuloInteger(ticks,4) == 0 then
            if kind == 1 then
                call SetWidgetLife(target,RMinBJ(I2R(BlzGetUnitMaxHP(target)),GetWidgetLife(target)+60.0*power))
            elseif kind == 7 then
                call UnitDamageTarget(caster,target,25.0*power,false,false,ATTACK_TYPE_NORMAL,DAMAGE_TYPE_MAGIC,WEAPON_TYPE_WHOKNOWS)
            endif
        endif
        call SaveInteger(KLS_RacialData,key,4,ticks)
        if ticks <= 0 then
            call KLS_RacialExpire(key)
        endif
    endif
    set clock = null
    set target = null
    set caster = null
endfunction

function KLS_RacialBuff takes unit caster, unit target, integer kind, real duration, real value, real power returns nothing
    local integer unitKey = GetHandleId(target)
    local timer prior = LoadTimerHandle(KLS_RacialData,unitKey,100+kind)
    local timer clock
    local integer key
    if prior != null then
        call KLS_RacialExpire(GetHandleId(prior))
    endif
    set clock = CreateTimer()
    set key = GetHandleId(clock)
    call SaveUnitHandle(KLS_RacialData,key,0,target)
    call SaveUnitHandle(KLS_RacialData,key,1,caster)
    call SavePlayerHandle(KLS_RacialData,key,2,GetOwningPlayer(target))
    call SaveInteger(KLS_RacialData,key,3,kind)
    call SaveInteger(KLS_RacialData,key,4,R2I(duration*4.0))
    call SaveReal(KLS_RacialData,key,5,value)
    call SaveReal(KLS_RacialData,key,6,power)
    call SavePlayerHandle(KLS_RacialData,key,7,GetOwningPlayer(caster))
    call SaveTimerHandle(KLS_RacialData,key,8,clock)
    call SaveTimerHandle(KLS_RacialData,unitKey,100+kind,clock)
    if kind == 0 or kind == 7 then
        call BlzSetUnitRealField(target,UNIT_RF_DEFENSE,BlzGetUnitRealField(target,UNIT_RF_DEFENSE)+value)
    elseif kind == 2 then
        call SetUnitMoveSpeed(target,GetUnitMoveSpeed(target)*(1.0-value))
    elseif kind == 3 then
        call BlzSetUnitAttackCooldown(target,BlzGetUnitAttackCooldown(target,0)/(1.0+value),0)
        if BlzGetUnitAttackCooldown(target,1) > 0.0 then
            call BlzSetUnitAttackCooldown(target,BlzGetUnitAttackCooldown(target,1)/(1.0+value),1)
        endif
    endif
    call TimerStart(clock,0.25,true,function KLS_RacialTick)
    set prior = null
    set clock = null
endfunction

function KLS_RacialShield takes nothing returns nothing
    local unit target = GetTriggerUnit()
    local timer clock = LoadTimerHandle(KLS_RacialData,GetHandleId(target),106)
    local integer key
    local real remaining
    local real absorbed
    if clock != null and GetEventDamage() > 0.0 then
        set key = GetHandleId(clock)
        if GetOwningPlayer(target) == LoadPlayerHandle(KLS_RacialData,key,2) and GetOwningPlayer(LoadUnitHandle(KLS_RacialData,key,1)) == LoadPlayerHandle(KLS_RacialData,key,7) and GetWidgetLife(LoadUnitHandle(KLS_RacialData,key,1)) > 0.405 then
            set remaining = LoadReal(KLS_RacialData,key,5)
            set absorbed = RMinBJ(remaining,GetEventDamage())
            call BlzSetEventDamage(GetEventDamage()-absorbed)
            call SaveReal(KLS_RacialData,key,5,remaining-absorbed)
            if remaining <= absorbed then
                call KLS_RacialExpire(key)
            endif
        else
            call KLS_RacialExpire(key)
        endif
    endif
    set target = null
    set clock = null
endfunction

function KLS_RacialCast takes nothing returns nothing
    local unit caster = GetTriggerUnit()
    local integer index = KLS_SpecialistIndex(GetUnitTypeId(caster))
    local integer p = GetPlayerId(GetOwningPlayer(caster))
    local group targets
    local unit target = GetSpellTargetUnit()
    local unit dummy
    local real potency
    local real duration = 3.0
    local real x = GetSpellTargetX()
    local real y = GetSpellTargetY()
    if index < 0 or p < 0 or p >= 4 or not KLS_Active[p] or KLS_Ended or GetSpellAbilityId() != KLS_SpecialistAbility[index] then
        set caster = null
        set target = null
        return
    endif
    set potency = 1.0+0.15*I2R(KLS_CompanyResearchRank[p*5])
    if ModuloInteger(index,2) == 1 then
        set potency = potency+0.25*I2R(KLS_CompanyResearchRank[p*5+4])
    endif
    if index == 1 then
        if target != null and target != KLS_King and IsUnitAlly(target,Player(p)) and IsUnitType(target,UNIT_TYPE_STRUCTURE) and GetWidgetLife(target) > 0.405 then
            call KLS_RacialBuff(caster,target,1,5.0,0.0,potency)
        endif
    elseif index == 4 then
        if target != null and IsUnitEnemy(target,Player(p)) and not IsUnitType(target,UNIT_TYPE_STRUCTURE) and GetWidgetLife(target) > 0.405 then
            if target == KLS_Boss or IsUnitType(target,UNIT_TYPE_HERO) then
                set duration = 1.0
            endif
            call KLS_RacialBuff(caster,target,4,duration,0.0,potency)
            set dummy = KLS_CreateUnitOptional(Player(p),'rD00',GetUnitX(target),GetUnitY(target),0,"binding thorns")
            if dummy != null then
                if duration == 1.0 then
                    call SetUnitAbilityLevel(dummy,'rRt0',2)
                endif
                call IssueTargetOrder(dummy,"ensnare",target)
                call UnitApplyTimedLife(dummy,'BTLF',2.0)
            endif
        endif
    elseif index == 6 then
        call KLS_RacialBuff(caster,caster,6,8.0,250.0*potency,potency)
    else
        set targets = CreateGroup()
        call GroupEnumUnitsInRange(targets,x,y,250.0,null)
        loop
            set target = FirstOfGroup(targets)
            exitwhen target == null
            call GroupRemoveUnit(targets,target)
            if GetWidgetLife(target) > 0.405 and not IsUnitType(target,UNIT_TYPE_STRUCTURE) then
                if IsUnitAlly(target,Player(p)) and target != KLS_King then
                    if index == 0 then
                        call KLS_RacialBuff(caster,target,0,8.0,4.0*potency,potency)
                    elseif index == 3 then
                        call KLS_RacialBuff(caster,target,3,6.0,0.15*potency,potency)
                    elseif index == 5 then
                        call SetWidgetLife(target,RMinBJ(I2R(BlzGetUnitMaxHP(target)),GetWidgetLife(target)+150.0*potency))
                        call SetUnitState(target,UNIT_STATE_MANA,RMinBJ(GetUnitState(target,UNIT_STATE_MAX_MANA),GetUnitState(target,UNIT_STATE_MANA)+30.0*potency))
                    endif
                elseif IsUnitEnemy(target,Player(p)) then
                    if index == 2 then
                        call UnitDamageTarget(caster,target,60.0*potency,false,false,ATTACK_TYPE_NORMAL,DAMAGE_TYPE_MAGIC,WEAPON_TYPE_WHOKNOWS)
                        call KLS_RacialBuff(caster,target,2,3.0,0.20,potency)
                    elseif index == 7 then
                        call KLS_RacialBuff(caster,target,7,4.0,-3.0*potency,potency)
                    endif
                endif
            endif
        endloop
        call DestroyGroup(targets)
        set targets = null
    endif
    set caster = null
    set target = null
    set dummy = null
endfunction

function KLS_RacialInit takes nothing returns nothing
    local trigger casts = CreateTrigger()
    local trigger shield = CreateTrigger()
    set KLS_RacialData = InitHashtable()
    call KLS_RacialCatalog()
    call TriggerRegisterAnyUnitEventBJ(casts,EVENT_PLAYER_UNIT_SPELL_EFFECT)
    call TriggerAddAction(casts,function KLS_RacialCast)
    call TriggerRegisterAnyUnitEventBJ(shield,EVENT_PLAYER_UNIT_DAMAGED)
    call TriggerAddAction(shield,function KLS_RacialShield)
    set casts = null
    set shield = null
endfunction
