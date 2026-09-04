#!/usr/bin/env python3
"""Emit BlackoutBotsBO4 exact labels absent from all earlier BO4 mod sources."""
from pathlib import Path
import importlib.util

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('shield', ROOT / 'contrib' / 'bo4_shieldmenu_delta_labels_20260903.py')
shield = importlib.util.module_from_spec(spec)
spec.loader.exec_module(shield)

if __name__ == '__main__':
    prior_roots = ('bo4-source', 't8-src', 'BO4-BlackoutBots', 'bo4-lucy-menu', 'BO4-BlackOps4ShieldMenu')
    prior = set()
    for directory in prior_roots:
        root = ROOT / 'borrowed' / directory
        prior |= shield.literals(root) | shield.hash_labels(root)
    current = ROOT / 'borrowed' / 'BlackoutBotsBO4'
    print('\n'.join(sorted((shield.literals(current) | shield.hash_labels(current)) - prior)))
