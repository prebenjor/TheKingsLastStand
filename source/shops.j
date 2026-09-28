globals
    unit array KLS_Shops
endglobals

// GENERATED_CATALOG
// GENERATED_RECIPES

function KLS_CreateShops takes nothing returns nothing
    local integer tier = 0
    local integer i
    local string array quality
    local string array qualityColor
    local string array categories
    set KLS_GearData = InitHashtable()
    call KLS_CatalogInit()
    set quality[0] = "Common"
    set quality[1] = "Uncommon"
    set quality[2] = "Rare"
    set quality[3] = "Epic"
    set quality[4] = "Legendary"
    set qualityColor[0] = "|cffffffff"
    set qualityColor[1] = "|cff1eff00"
    set qualityColor[2] = "|cff0070dd"
    set qualityColor[3] = "|cffa335ee"
    set qualityColor[4] = "|cffff8000"
    set categories[0] = "Arms & Armor"
    set categories[1] = "Apparel & Relics"
    loop
        exitwhen tier == 5
        set i = 0
        loop
            exitwhen i == 2
            set KLS_Shops[tier*2+i] = KLS_CreateUnit(Player(PLAYER_NEUTRAL_PASSIVE),'hS00',-2300+tier*1150,-3900-i*560,270)
            if KLS_Shops[tier*2+i] == null then
                return
            endif
            call BlzSetUnitName(KLS_Shops[tier*2+i],qualityColor[tier]+quality[tier]+"|r "+categories[i])
            call SetUnitInvulnerable(KLS_Shops[tier*2+i],true)
            set i = i+1
        endloop
        set tier = tier+1
    endloop
    set KLS_Shops[10] = KLS_CreateUnit(Player(PLAYER_NEUTRAL_PASSIVE),'hS00',3450,-3900,270)
    if KLS_Shops[10] == null then
        return
    endif
    call BlzSetUnitName(KLS_Shops[10],"Field Apothecary")
    call SetUnitInvulnerable(KLS_Shops[10],true)
    set KLS_Shops[11] = KLS_CreateUnit(Player(PLAYER_NEUTRAL_PASSIVE),'hS02',4100,-3900,270)
    if KLS_Shops[11] == null then
        return
    endif
    call BlzSetUnitName(KLS_Shops[11],"Sage's Archive")
    call SetUnitInvulnerable(KLS_Shops[11],true)
    call SetUnitAcquireRange(KLS_Shops[11],0)
    call AddItemToStock(KLS_Shops[10],'phea',1,1)
    call AddItemToStock(KLS_Shops[10],'pman',1,1)
    call AddItemToStock(KLS_Shops[10],'stwp',1,1)
    call AddItemToStock(KLS_Shops[10],'shea',1,1)
    call KLS_StockCatalog()
    call KLS_StockRecipes()
    call KLS_Log("Sixteen gear families stocked across five tiers; Apothecary, Sage's Archive, and Master Forge recipes created.")
endfunction
