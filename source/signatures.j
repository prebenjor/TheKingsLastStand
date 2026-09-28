globals
    integer array KLS_SignatureId
    string array KLS_SignatureName
    string array KLS_SignatureDescription
    integer array KLS_SignatureDamage
    integer array KLS_SignatureHeal
    integer array KLS_SignatureMana
    integer array KLS_SignatureSummon
    integer array KLS_SignatureCount
    integer array KLS_SignatureExtra
endglobals

// GENERATED_SIGNATURES

function KLS_SignatureCast takes nothing returns nothing
    local integer n = 0
    local integer k = 0
    local unit hero = GetTriggerUnit()
    local player owner = GetOwningPlayer(hero)
    local integer p = GetPlayerId(owner)
    local real x = GetSpellTargetX()
    local real y = GetSpellTargetY()
    local integer level = GetHeroLevel(hero)
    local group targets
    local unit u
    local unit dummy
    local real drained = 0
    local real mana
    if p >= 4 or hero != KLS_Hero[p] or not KLS_Active[p] or KLS_Ended then
        return
    endif
    loop
        exitwhen n == 15 or GetSpellAbilityId() == KLS_SignatureId[n]
        set n = n+1
    endloop
    if n == 15 then
        return
    endif
    call KLS_Log(KLS_SignatureName[n]+" cast by p"+I2S(p+1))
    call DestroyEffect(AddSpecialEffect("Abilities\\Spells\\Other\\Monsoon\\MonsoonBoltTarget.mdl",x,y))
    set targets = CreateGroup()
    call GroupEnumUnitsInRange(targets,x,y,350,null)
    loop
        set u = FirstOfGroup(targets)
        exitwhen u == null or KLS_Ended
        call GroupRemoveUnit(targets,u)
        if GetWidgetLife(u) > 0.405 and not IsUnitType(u,UNIT_TYPE_STRUCTURE) then
            if IsUnitEnemy(u,owner) then
                if KLS_SignatureExtra[n] == 3 then
                    set mana = RMinBJ(40,GetUnitState(u,UNIT_STATE_MANA))
                    call SetUnitState(u,UNIT_STATE_MANA,GetUnitState(u,UNIT_STATE_MANA)-mana)
                    set drained = drained+mana
                endif
                if KLS_SignatureDamage[n] > 0 then
                    call UnitDamageTarget(hero,u,KLS_SignatureDamage[n]+20.0*level,false,false,ATTACK_TYPE_MAGIC,DAMAGE_TYPE_MAGIC,null)
                endif
                if KLS_SignatureExtra[n] == 1 and GetWidgetLife(u) > 0.405 and not KLS_Ended then
                    set dummy = KLS_CreateUnit(owner,'hS01',GetUnitX(u),GetUnitY(u),0)
                    if dummy != null then
                        call IssueTargetOrder(dummy,"slow",u)
                        call UnitApplyTimedLife(dummy,'BTLF',3)
                    endif
                endif
            elseif GetPlayerId(GetOwningPlayer(u)) < 4 and IsUnitAlly(u,owner) then
                if KLS_SignatureHeal[n] > 0 then
                    call SetWidgetLife(u,RMinBJ(BlzGetUnitMaxHP(u),GetWidgetLife(u)+KLS_SignatureHeal[n]+15.0*level))
                    call DestroyEffect(AddSpecialEffectTarget("Abilities\\Spells\\Human\\HolyBolt\\HolyBoltSpecialArt.mdl",u,"origin"))
                endif
                if KLS_SignatureMana[n] > 0 then
                    call SetUnitState(u,UNIT_STATE_MANA,RMinBJ(GetUnitState(u,UNIT_STATE_MAX_MANA),GetUnitState(u,UNIT_STATE_MANA)+KLS_SignatureMana[n]))
                endif
            endif
        endif
    endloop
    call DestroyGroup(targets)
    if not KLS_Ended then
        if KLS_SignatureExtra[n] == 2 then
            call SetWidgetLife(hero,RMinBJ(BlzGetUnitMaxHP(hero),GetWidgetLife(hero)+150))
        endif
        if drained > 0 then
            call SetUnitState(hero,UNIT_STATE_MANA,RMinBJ(GetUnitState(hero,UNIT_STATE_MAX_MANA),GetUnitState(hero,UNIT_STATE_MANA)+drained))
        endif
        loop
            exitwhen k == KLS_SignatureCount[n]
            set u = KLS_CreateUnit(owner,KLS_SignatureSummon[n],x+100*Cos(k*2.094),y+100*Sin(k*2.094),270)
            if u == null then
                exitwhen true
            endif
            call SetUnitUseFood(u,false)
            call BlzSetUnitMaxHP(u,300+30*level)
            call SetWidgetLife(u,300+30*level)
            call BlzSetUnitBaseDamage(u,12+2*level,0)
            call SetUnitUserData(u,0)
            call UnitApplyTimedLife(u,'BTLF',25)
            call IssuePointOrder(u,"attack",x,y+400)
            set k = k+1
        endloop
    endif
    set hero = null
    set owner = null
    set targets = null
    set u = null
    set dummy = null
endfunction

function KLS_SignatureInit takes nothing returns nothing
    local trigger spell = CreateTrigger()
    call KLS_SignatureData()
    call TriggerRegisterAnyUnitEventBJ(spell,EVENT_PLAYER_UNIT_SPELL_EFFECT)
    call TriggerAddAction(spell,function KLS_SignatureCast)
    set spell = null
endfunction
