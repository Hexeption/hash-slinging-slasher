#!/usr/bin/env python3
"""Emit Abomination exact labels absent from all previously checked BO4 mod sources."""
from pathlib import Path
import importlib.util

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('labels', ROOT / 'contrib' / 'bo4_shieldmenu_delta_labels_20260903.py')
labels = importlib.util.module_from_spec(spec)
spec.loader.exec_module(labels)

if __name__ == '__main__':
    prior_roots = ('bo4-source', 't8-src', 'BO4-BlackoutBots', 'bo4-lucy-menu', 'BO4-BlackOps4ShieldMenu', 'BlackoutBotsBO4')
    prior = set()
    for directory in prior_roots:
        root = ROOT / 'borrowed' / directory
        prior |= labels.literals(root) | labels.hash_labels(root)
    current = ROOT / 'borrowed' / 'Abomination-Unofficial'
    print('\n'.join(sorted((labels.literals(current) | labels.hash_labels(current)) - prior)))
