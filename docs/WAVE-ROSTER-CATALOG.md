# Generated wave roster catalog

Generated from `tools/wave_rosters.py`; this table is the ordered rawcode sequence used by the wave generator. Waves 1-40 remain the original four chapters. Waves 41-50 introduce the Naga, Blood Elf, Fel Orc, Burning Legion and Scourge campaign crossover. Wave 49 is the five-force convergence; the campaign Lady Vashj leads the separate Wave 50 boss spawn.

Live waves after 50 reuse these ten rows with the bounded source index `41 + ((wave - 41) % 10)`. Counts and unit health, damage, bounty, and boss scaling continue to use the live wave number. Bosses spawn separately every ten waves.

| Wave | Chapter / crossover | Ordered unit rawcodes |
|---:|---|---|
| 1 | The Broken Verge | ugho, uske, ugho, ucry, nska, nfel, hfoo, ugho |
| 2 | The Broken Verge | uske, ugho, ucry, nska, nfel, hfoo, ugho, ugho |
| 3 | The Broken Verge | ugho, ucry, nska, nfel, hfoo, ugho, ugho, uske |
| 4 | The Broken Verge | ucry, nska, nfel, hfoo, nfgu, ugho, uske, ugho |
| 5 | The Broken Verge | nska, nfel, hfoo, nfgu, ugho, uske, ugho, ucry |
| 6 | The Broken Verge | nfel, hfoo, nfgu, ugho, uske, ugho, ucry, nska |
| 7 | The Broken Verge | hfoo, nfgu, unec, nsat, ugho, uske, ugho, ucry, nska, nfel |
| 8 | The Broken Verge | nfgu, unec, nsat, ugho, uske, ugho, ucry, nska, nfel, hfoo |
| 9 | The Broken Verge | unec, nsat, ugho, uske, ugho, ucry, nska, nfel, hfoo, nfgu |
| 10 | The Broken Verge | nsat, ugho, uske, ugho, ucry, nska, nfel, hfoo, nfgu, unec |
| 11 | The Grave March | uabo, ndqn, ugho, uske, ugho, ucry, nska, nfel, hfoo, nfgu, unec, nsat |
| 12 | The Grave March | ndqn, ugho, uske, ugho, ucry, nska, nfel, hfoo, nfgu, unec, nsat, uabo |
| 13 | The Grave March | ugho, uske, ugho, ucry, nska, nfel, hfoo, nfgu, unec, nsat, uabo, ndqn |
| 14 | The Grave March | uske, ugho, ucry, nska, nfel, hfoo, nfgu, unec, nsat, uabo, ndqn, ugho |
| 15 | The Grave March | ugho, ucry, nska, nfel, hfoo, nfgu, unec, nsat, uabo, ndqn, ugho, uske |
| 16 | The Grave March | uske, ugho, ucry, nska, nfel, hfoo, nfgu, unec, nsat, uabo, ndqn, ucry, nvdw, ugho |
| 17 | The Grave March | ugho, ucry, nska, nfel, hfoo, nfgu, unec, nsat, uabo, ndqn, ucry, nvdw, ugho, uske |
| 18 | The Grave March | ucry, nska, nfel, hfoo, nfgu, unec, nsat, uabo, ndqn, ucry, nvdw, ugho, uske, ugho |
| 19 | The Grave March | nska, nfel, hfoo, nfgu, unec, nsat, uabo, ndqn, ucry, nvdw, ugho, uske, ugho, ucry |
| 20 | The Grave March | nfel, hfoo, nfgu, unec, nsat, uabo, ndqn, ucry, nvdw, ugho, uske, ugho, ucry, nska |
| 21 | The Siege Tide | nska, nfel, hfoo, nfgu, unec, nsat, uabo, ndqn, ucry, nvdw, umtw, nbal, ugho, uske, ugho, ucry |
| 22 | The Siege Tide | nfel, hfoo, nfgu, unec, nsat, uabo, ndqn, ucry, nvdw, umtw, nbal, ugho, uske, ugho, ucry, nska |
| 23 | The Siege Tide | hfoo, nfgu, unec, nsat, uabo, ndqn, ucry, nvdw, umtw, nbal, ugho, uske, ugho, ucry, nska, nfel |
| 24 | The Siege Tide | nfgu, unec, nsat, uabo, ndqn, ucry, nvdw, umtw, nbal, ugho, uske, ugho, ucry, nska, nfel, hfoo |
| 25 | The Siege Tide | unec, nsat, uabo, ndqn, ucry, nvdw, umtw, nbal, ugho, uske, ugho, ucry, nska, nfel, hfoo, nfgu |
| 26 | The Siege Tide | nfgu, unec, nsat, uabo, ndqn, ucry, nvdw, umtw, nbal, unec, nfgu, ugho, uske, ugho, ucry, nska, nfel, hfoo |
| 27 | The Siege Tide | unec, nsat, uabo, ndqn, ucry, nvdw, umtw, nbal, unec, nfgu, ugho, uske, ugho, ucry, nska, nfel, hfoo, nfgu |
| 28 | The Siege Tide | nsat, uabo, ndqn, ucry, nvdw, umtw, nbal, unec, nfgu, ugho, uske, ugho, ucry, nska, nfel, hfoo, nfgu, unec |
| 29 | The Siege Tide | uabo, ndqn, ucry, nvdw, umtw, nbal, unec, nfgu, ugho, uske, ugho, ucry, nska, nfel, hfoo, nfgu, unec, nsat |
| 30 | The Siege Tide | ndqn, ucry, nvdw, umtw, nbal, unec, nfgu, ugho, uske, ugho, ucry, nska, nfel, hfoo, nfgu, unec, nsat, uabo |
| 31 | The Last Host | uabo, ndqn, ucry, nvdw, umtw, nbal, unec, nfgu, ninf, uabo, ugho, uske, ugho, ucry, nska, nfel, hfoo, nfgu, unec, nsat |
| 32 | The Last Host | ndqn, ucry, nvdw, umtw, nbal, unec, nfgu, ninf, uabo, ugho, uske, ugho, ucry, nska, nfel, hfoo, nfgu, unec, nsat, uabo |
| 33 | The Last Host | ucry, nvdw, umtw, nbal, unec, nfgu, ninf, uabo, ugho, uske, ugho, ucry, nska, nfel, hfoo, nfgu, unec, nsat, uabo, ndqn |
| 34 | The Last Host | nvdw, umtw, nbal, unec, nfgu, ninf, uabo, ugho, uske, ugho, ucry, nska, nfel, hfoo, nfgu, unec, nsat, uabo, ndqn, ucry |
| 35 | The Last Host | umtw, nbal, unec, nfgu, ninf, uabo, ugho, uske, ugho, ucry, nska, nfel, hfoo, nfgu, unec, nsat, uabo, ndqn, ucry, nvdw |
| 36 | The Last Host | nbal, unec, nfgu, ninf, uabo, ugho, uske, ugho, ucry, nska, nfel, hfoo, nfgu, unec, nsat, uabo, ndqn, ucry, nvdw, umtw |
| 37 | The Last Host | unec, nfgu, ninf, uabo, ugho, uske, ugho, ucry, nska, nfel, hfoo, nfgu, unec, nsat, uabo, ndqn, ucry, nvdw, umtw, nbal |
| 38 | The Last Host | nfgu, ninf, uabo, ugho, uske, ugho, ucry, nska, nfel, hfoo, nfgu, unec, nsat, uabo, ndqn, ucry, nvdw, umtw, nbal, unec |
| 39 | The Last Host | ninf, uabo, ugho, uske, ugho, ucry, nska, nfel, hfoo, nfgu, unec, nsat, uabo, ndqn, ucry, nvdw, umtw, nbal, unec, nfgu |
| 40 | The Last Host | uabo, ugho, uske, ugho, ucry, nska, nfel, hfoo, nfgu, unec, nsat, uabo, ndqn, ucry, nvdw, umtw, nbal, unec, nfgu, ninf |
| 41 | The Drowned Vanguard | nmyr, nmyr, nnsw, nnmg, ucry, uske, nfel, nbel, nbee, nchg, nfgu, nska |
| 42 | The Sunken Embassy | nnrg, nnsw, nhyc, nbel, nbee, hbew, uske, unec, nchg, nchw, nfgu, nfel, nwgs |
| 43 | The Ashen Pact | nchg, nchg, nchr, nchw, nckb, nnmg, nnrg, ucry, nska, nbel, nbal, nfgu, nmyr |
| 44 | Legion Inheritance | nfgu, nfel, nbal, ninf, nchr, nchw, nmyr, nnsw, uabo, unec, nbel, nbee, hbew |
| 45 | The Barrow Tide | uske, uske, nska, ugho, ucry, ucry, unec, uabo, umtw, nmyr, nnsw, nfel, nchr, nbel |
| 46 | The Returned Host | nmyr, nnmg, nwgs, nbel, nbee, nchw, nfgu, ucry, nska, unec, nbal, uabo, hbew, nhyc |
| 47 | Four Oathbreakers | nchg, nchr, nchw, nckb, nnrg, nhyc, nbel, hbew, nfel, nfgu, uske, uabo, umtw, nwgs |
| 48 | The Open Confluence | nmyr, nnmg, nnsw, nbel, nbee, hbew, nchg, nchr, nchw, nckb, nfel, nfgu, nbal, ucry, unec, umtw, nwgs |
| 49 | Crownlands Convergence | nmyr, nnrg, nbel, nbee, nchg, nchr, nfgu, ninf, uske, umtw, nnsw, nfel, nchw, ucry, nska, unec, nhyc, hbew |
| 50 | Vashj Ascendant | nnrg, nwgs, nmyr, nnsw, nbel, nchw, nchr, nfgu, nfel, ucry, uabo, ninf, hbew, unec, umtw |
