#!/usr/bin/env python3
"""Emit T8 test-script labels absent from all previously checked BO4 source corpora."""
from pathlib import Path
import importlib.util

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('synergy', ROOT / 'contrib' / 'bo4_synergy_delta_labels_20260903.py')
synergy = importlib.util.module_from_spec(spec)
spec.loader.exec_module(synergy)

if __name__ == '__main__':
    prior_roots = ('bo4-source', 't8-src', 'BO4-BlackoutBots', 'bo4-lucy-menu', 'BO4-BlackOps4ShieldMenu', 'BlackoutBotsBO4', 'Abomination-Unofficial', 'Synergy-BO4-GSC-Menu')
    prior = set()
    for directory in prior_roots:
        prior |= synergy.values(ROOT / 'borrowed' / directory)
    print('\n'.join(sorted(synergy.values(ROOT / 'borrowed' / 't8-tests') - prior)))
