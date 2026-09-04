#!/usr/bin/env python3
"""Emit demo-mod source literals absent from all checked BO4 and Cold War corpora."""
from pathlib import Path
import importlib.util

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('t9', ROOT / 'contrib' / 't9_src_delta_literals_20260904.py')
t9 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(t9)

if __name__ == '__main__':
    prior_roots = ('bocw-source', 't9-src', 'ColdWarGSCMenu', 'coldwar.gsc', 'cwmenu', 'ColdWar-Lucy-Base', 'bo4-source', 't8-src', 'BO4-BlackoutBots', 'bo4-lucy-menu', 'BO4-BlackOps4ShieldMenu', 'BlackoutBotsBO4', 'Abomination-Unofficial', 'Synergy-BO4-GSC-Menu', 't8-tests', 'Shield-Menu-BO4', 'bo4-pap-mod')
    prior = set()
    for directory in prior_roots:
        prior |= t9.collect(ROOT / 'borrowed' / directory)
    print('\n'.join(sorted(t9.collect(ROOT / 'borrowed' / 'demo_mods') - prior)))
