globals
    multiboard KLS_HUD = null
    boolean KLS_Won = false
endglobals

// GENERATED_BOSSES

function KLS_HUDRow takes integer row, string label, string value returns nothing
    local multiboarditem cell = MultiboardGetItem(KLS_HUD, row, 0)
    call MultiboardSetItemValue(cell, label)
    call MultiboardReleaseItem(cell)
    set cell = MultiboardGetItem(KLS_HUD, row, 1)
    call MultiboardSetItemValue(cell, value)
    call MultiboardReleaseItem(cell)
    set cell = null
endfunction

function KLS_TimeText takes integer seconds returns string
    local string tail = I2S(ModuloInteger(IMaxBJ(0, seconds), 60))
    if ModuloInteger(IMaxBJ(0, seconds), 60) < 10 then
        set tail = "0" + tail
    endif
    return I2S(IMaxBJ(0, seconds) / 60) + ":" + tail
endfunction

function KLS_BossThreatText takes nothing returns string
    if KLS_Boss != null and GetWidgetLife(KLS_Boss) > 0.405 and KLS_BossCast > 0 then
        return KLS_BossMechanicName(KLS_BossMechanic)+" in "+I2S(KLS_BossCast)+"s - "+KLS_BossMechanicWarning(KLS_BossMechanic)
    elseif KLS_TowerSuppression > 0 then
        return "Towers suppressed: "+I2S(KLS_TowerSuppression)+"s"
    endif
    return "Clear"
endfunction

function KLS_HUDUpdate takes nothing returns nothing
    local integer wave = KLS_Wave
    local integer p = GetPlayerId(GetLocalPlayer())
    local string revival = "Ready"
    if KLS_HUD == null then
        return
    endif
    if KLS_Ended then
        if KLS_Won then
            call KLS_HUDRow(0, "Result", "Final boss defeated")
        else
            call KLS_HUDRow(0, "Result", "King defeated")
        endif
        call KLS_HUDRow(2, "Match", "Finished")
    elseif KLS_Selecting then
        set wave = 1
        call KLS_HUDRow(0, "Hero selection", "25 heroes")
        call KLS_HUDRow(2, "Choose within", KLS_TimeText(KLS_SelectionLeft))
    elseif KLS_Alive == 0 then
        set wave = IMinBJ(40, wave + 1)
        call KLS_HUDRow(0, "Next wave", I2S(wave) + " / 40")
        call KLS_HUDRow(2, "Next wave in", KLS_TimeText(KLS_Prep))
    else
        call KLS_HUDRow(0, "Wave", I2S(wave) + " / 40")
        call KLS_HUDRow(2, "Enemies remaining", I2S(KLS_Alive))
    endif
    call KLS_HUDRow(1, "Chapter", I2S((IMaxBJ(1, wave) - 1) / 10 + 1) + " / 4")
    call KLS_HUDRow(3, "King health", I2S(IMaxBJ(0, R2I(GetWidgetLife(KLS_King)))) + " / " + I2S(BlzGetUnitMaxHP(KLS_King)))
    call KLS_HUDRow(4, "King upgrade", I2S(KLS_KingTier) + " / 5")
    // Local values affect presentation only; all handles are created on every client.
    if p < 4 then
        if KLS_Respawn[p] > 0 then
            set revival = KLS_TimeText(KLS_Respawn[p])
        endif
    endif
    if KLS_Ended then
        set revival = "Finished"
    endif
    call KLS_HUDRow(5, "Your hero", revival)
    call KLS_HUDRow(6, "Boss warning", KLS_BossThreatText())
endfunction

function KLS_HUDInit takes nothing returns nothing
    set KLS_HUD = CreateMultiboard()
    call MultiboardSetTitleText(KLS_HUD, "The King's Last Stand - DEVELOPMENT")
    call MultiboardSetColumnCount(KLS_HUD, 2)
    call MultiboardSetRowCount(KLS_HUD, 7)
    call MultiboardSetItemsStyle(KLS_HUD, true, false)
    call MultiboardSetItemsWidth(KLS_HUD, 0.12)
    call KLS_HUDUpdate()
    call MultiboardMinimize(KLS_HUD, false)
    call MultiboardDisplay(KLS_HUD, true)
endfunction
