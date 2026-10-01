globals
    unit KLS_Castle = null
endglobals

function KLS_KingRefund takes player payer, integer gold, integer lumber returns nothing
    if gold > 0 then
        call SetPlayerState(payer,PLAYER_STATE_RESOURCE_GOLD,GetPlayerState(payer,PLAYER_STATE_RESOURCE_GOLD)+gold)
    endif
    if lumber > 0 then
        call SetPlayerState(payer,PLAYER_STATE_RESOURCE_LUMBER,GetPlayerState(payer,PLAYER_STATE_RESOURCE_LUMBER)+lumber)
    endif
endfunction

// Castle item buttons pay their displayed native stock cost before this event.
// Chat shortcuts use the same transaction without prepayment.
function KLS_KingContribute takes player payer, boolean upgrade, integer expectedTier, boolean prepaid returns nothing
    local integer p = GetPlayerId(payer)
    local integer goldCost
    local integer woodCost
    local integer goldPaid = 0
    local integer woodPaid = 0
    local real life = GetWidgetLife(KLS_King)
    local integer maxLife = BlzGetUnitMaxHP(KLS_King)
    local timer healCooldown = LoadTimerHandle(KLS_GearData,GetHandleId(KLS_King),71)
    if upgrade then
        set goldCost = 400+200*KLS_KingTier
        set woodCost = 150
        if prepaid then
            set goldPaid = 400+200*expectedTier
            set woodPaid = 150
        endif
    else
        set goldCost = 150
        set woodCost = 50
        if prepaid then
            set goldPaid = 150
            set woodPaid = 50
        endif
    endif
    if p >= 4 or not KLS_Active[p] or KLS_Ended or life <= 0.405 then
        call KLS_KingRefund(payer,goldPaid,woodPaid)
        return
    endif
    if upgrade and KLS_KingTier >= 5 then
        call KLS_KingRefund(payer,goldPaid,woodPaid)
        call DisplayTimedTextToPlayer(payer,0,0,6,"King Aldric is already at maximum tier (5/5). No resources charged.")
        return
    endif
    if upgrade and expectedTier != KLS_KingTier then
        call KLS_KingRefund(payer,goldPaid,woodPaid)
        call DisplayTimedTextToPlayer(payer,0,0,6,"Another defender upgraded the king. Review the new tier price. No resources charged.")
        return
    endif
    if not upgrade and life >= maxLife then
        call KLS_KingRefund(payer,goldPaid,woodPaid)
        call DisplayTimedTextToPlayer(payer,0,0,6,"King Aldric is at full health. No resources charged.")
        return
    endif
    if not upgrade and healCooldown != null and TimerGetRemaining(healCooldown) > 0 then
        call KLS_KingRefund(payer,goldPaid,woodPaid)
        call DisplayTimedTextToPlayer(payer,0,0,3,"King healing is available again after one second. No resources charged.")
        return
    endif
    if GetPlayerState(payer,PLAYER_STATE_RESOURCE_GOLD) < goldCost-goldPaid or GetPlayerState(payer,PLAYER_STATE_RESOURCE_LUMBER) < woodCost-woodPaid then
        call KLS_KingRefund(payer,goldPaid,woodPaid)
        call DisplayTimedTextToPlayer(payer,0,0,6,"Not enough personal resources for this contribution. No resources charged.")
        return
    endif
    if goldCost > goldPaid then
        call SetPlayerState(payer,PLAYER_STATE_RESOURCE_GOLD,GetPlayerState(payer,PLAYER_STATE_RESOURCE_GOLD)-(goldCost-goldPaid))
    endif
    if woodCost > woodPaid then
        call SetPlayerState(payer,PLAYER_STATE_RESOURCE_LUMBER,GetPlayerState(payer,PLAYER_STATE_RESOURCE_LUMBER)-(woodCost-woodPaid))
    endif
    if upgrade then
        set KLS_KingTier = KLS_KingTier+1
        call BlzSetUnitMaxHP(KLS_King,maxLife+4000)
        call SetWidgetLife(KLS_King,life+4000)
        call BlzSetUnitBaseDamage(KLS_King,BlzGetUnitBaseDamage(KLS_King,0)+30,0)
        call DisplayTimedTextToForce(bj_FORCE_ALL_PLAYERS,8,GetPlayerName(payer)+" upgraded King Aldric to tier "+I2S(KLS_KingTier)+"/5: +4,000 maximum health and +30 damage.")
        call KLS_Log("King upgrade by p"+I2S(p+1)+": tier "+I2S(KLS_KingTier)+", gold="+I2S(goldCost))
    else
        call SetWidgetLife(KLS_King,RMinBJ(maxLife,life+2000))
        if healCooldown == null then
            set healCooldown = CreateTimer()
            call SaveTimerHandle(KLS_GearData,GetHandleId(KLS_King),71,healCooldown)
        endif
        call TimerStart(healCooldown,1.0,false,null)
        call DisplayTimedTextToPlayer(payer,0,0,6,"King Aldric healed for "+I2S(R2I(GetWidgetLife(KLS_King)-life))+" health.")
        call KLS_Log("King healed by p"+I2S(p+1)+": "+I2S(R2I(GetWidgetLife(KLS_King)-life))+" health")
    endif
    call KLS_HUDUpdate()
    set healCooldown = null
endfunction

// Castle healing and upgrades use the castle's native item command card. The
// empty function remains as an explicit initializer boundary in the pipeline.
function KLS_CastleInit takes nothing returns nothing
endfunction
