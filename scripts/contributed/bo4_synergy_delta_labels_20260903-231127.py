#!/usr/bin/env python3
"""Emit Synergy Menu labels absent from every earlier checked BO4 mod corpus."""
from pathlib import Path
import importlib.util

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('labels', ROOT / 'contrib' / 'bo4_shieldmenu_delta_labels_20260903.py')
labels = importlib.util.module_from_spec(spec)
spec.loader.exec_module(labels)


def values(root: Path) -> set[str]:
    names = labels.literals(root)
    for path in root.rglob('hashes.txt'):
        for line in path.read_text(encoding='utf-8', errors='ignore').splitlines():
            _, separator, raw = line.partition(',')
            if separator and (name := labels.acceptable(raw)):
                names.add(name)
    return names


if __name__ == '__main__':
    prior_roots = ('bo4-source', 't8-src', 'BO4-BlackoutBots', 'bo4-lucy-menu', 'BO4-BlackOps4ShieldMenu', 'BlackoutBotsBO4', 'Abomination-Unofficial')
    prior = set()
    for directory in prior_roots:
        prior |= values(ROOT / 'borrowed' / directory)
    print('\n'.join(sorted(values(ROOT / 'borrowed' / 'Synergy-BO4-GSC-Menu') - prior)))
