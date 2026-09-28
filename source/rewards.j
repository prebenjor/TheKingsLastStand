globals
    hashtable KLS_PersonalRewardData = null
    integer array KLS_PersonalRewardHead
    integer array KLS_PersonalRewardTail
    integer array KLS_PersonalRewardRetry
endglobals

function KLS_PersonalRewardInit takes nothing returns nothing
    local integer p = 0
    set KLS_PersonalRewardData = InitHashtable()
    loop
        exitwhen p == 4
        set KLS_PersonalRewardHead[p] = 0
        set KLS_PersonalRewardTail[p] = 0
        set KLS_PersonalRewardRetry[p] = 0
        set p = p+1
    endloop
endfunction

// Deliver a personal item into its owner's hero inventory. If that inventory
// cannot accept it, leave the item visibly bound at the owner's base instead.
// A false result means CreateItem returned null and the caller must retain the
// entitlement for a later retry.
function KLS_PersonalRewardDeliver takes integer p, integer itemCode returns boolean
    local item reward
    local unit hero
    local boolean stored = false
    if p < 0 or p >= 4 or itemCode == 0 then
        return false
    endif
    set reward = CreateItem(itemCode,KLS_X[p],KLS_Y[p])
    if reward == null then
        return false
    endif
    call SetItemPlayer(reward,Player(p),false)
    call SetItemUserData(reward,p+1)
    set hero = KLS_Hero[p]
    if hero != null then
        set stored = UnitAddItem(hero,reward)
    endif
    if stored then
        call DisplayTimedTextToPlayer(Player(p),0,0,8,"Your personal reward was added to your hero's inventory.")
    else
        call SetItemVisible(reward,true)
        call SetItemPosition(reward,KLS_X[p],KLS_Y[p])
        call DisplayTimedTextToPlayer(Player(p),0,0,12,"Your personal reward is waiting at your base.")
        call KLS_Log("Personal reward placed at base owner=p"+I2S(p+1)+" item="+GetObjectName(itemCode))
    endif
    set reward = null
    set hero = null
    return true
endfunction

function KLS_PersonalRewardEnqueue takes integer p, integer itemCode, string source returns nothing
    if p < 0 or p >= 4 or not KLS_Active[p] or itemCode == 0 then
        return
    endif
    if KLS_PersonalRewardDeliver(p,itemCode) then
        return
    endif
    set KLS_PersonalRewardTail[p] = KLS_PersonalRewardTail[p]+1
    call SaveInteger(KLS_PersonalRewardData,p,KLS_PersonalRewardTail[p],itemCode)
    if KLS_PersonalRewardRetry[p] <= 0 then
        set KLS_PersonalRewardRetry[p] = 5
    endif
    call KLS_Log("ERROR "+source+" item creation failed; personal reward queued owner=p"+I2S(p+1)+" item="+GetObjectName(itemCode))
    call DisplayTimedTextToPlayer(Player(p),0,0,10,"Your personal reward could not be created yet. It will be retried automatically.")
endfunction

function KLS_PersonalRewardTick takes nothing returns nothing
    local integer p = 0
    local integer entry
    local integer itemCode
    local integer tail
    local integer head
    loop
        exitwhen p == 4
        if KLS_PersonalRewardHead[p] < KLS_PersonalRewardTail[p] then
            set KLS_PersonalRewardRetry[p] = KLS_PersonalRewardRetry[p]-1
            if KLS_PersonalRewardRetry[p] <= 0 then
                set tail = KLS_PersonalRewardTail[p]
                set entry = KLS_PersonalRewardHead[p]+1
                loop
                    exitwhen entry > tail
                    set itemCode = LoadInteger(KLS_PersonalRewardData,p,entry)
                    if itemCode != 0 then
                        if KLS_PersonalRewardDeliver(p,itemCode) then
                            call SaveInteger(KLS_PersonalRewardData,p,entry,0)
                        else
                            call KLS_Log("ERROR personal reward retry failed owner=p"+I2S(p+1)+" item="+GetObjectName(itemCode))
                        endif
                    endif
                    set entry = entry+1
                endloop
                set head = KLS_PersonalRewardHead[p]
                loop
                    exitwhen head >= tail
                    exitwhen LoadInteger(KLS_PersonalRewardData,p,head+1) != 0
                    set head = head+1
                endloop
                set KLS_PersonalRewardHead[p] = head
                if head >= tail then
                    call FlushChildHashtable(KLS_PersonalRewardData,p)
                    set KLS_PersonalRewardHead[p] = 0
                    set KLS_PersonalRewardTail[p] = 0
                    set KLS_PersonalRewardRetry[p] = 0
                else
                    set KLS_PersonalRewardRetry[p] = 5
                endif
            endif
        endif
        set p = p+1
    endloop
endfunction
