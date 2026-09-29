# Playtest plan

Use docs/ROADMAP-AND-ACCEPTANCE.md for current build identity, pending status, and ordered human checks. Use docs/PLAYER-GUIDE.md for launch and diagnostic commands.

Current build: KLS-D-7951d852c3. Map SHA-256: 42922eb38fd46bd6f6071fef7df08f4329e4abd921d8773bdfc32286f9421b1c.

The first required check is a separate World Editor open/save/close/reopen/Test Map on this exact build, then direct Custom Game launch with the same visible build ID. Capture full -diag output if any unit, building, model, or shop is missing. During item testing, use -gear to report the six normal slots, occupied backpack positions, nine equipment slots, catalog slot and owner marker. If gear fails to equip, also capture -diag immediately; the transaction log now includes buyer type/owner/life state, inventory capacity and item location/ownership, plus the retry count.
