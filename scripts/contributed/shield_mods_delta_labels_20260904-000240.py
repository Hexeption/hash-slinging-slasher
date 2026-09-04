#!/usr/bin/env python3
"""Emit Shield Mods GSC/Lua literals absent from all checked source corpora."""
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
LITERAL = re.compile(r'(?:#)?"([A-Za-z0-9_./-]{6,160})"')
EXTENSIONS = {'.gsc', '.csc', '.cfg', '.csv', '.ddl', '.gdb', '.graph', '.raw', '.txt', '.vision', '.lua'}


def collect(root: Path) -> set[str]:
    names = set()
    for path in root.rglob('*'):
        if not path.is_file() or path.suffix.lower() not in EXTENSIONS:
            continue
        for name in LITERAL.findall(path.read_text(encoding='utf-8', errors='ignore')):
            name = name.lower()
            if ('_' in name or '/' in name) and sum(char.isalpha() for char in name) >= 3:
                names.add(name)
    return names


if __name__ == '__main__':
    prior_roots = ('bocw-source', 't9-src', 'ColdWarGSCMenu', 'coldwar.gsc', 'cwmenu', 'ColdWar-Lucy-Base', 'bo4-source', 'bo4-source-lua', 't8-src', 'BO4-BlackoutBots', 'bo4-lucy-menu', 'BO4-BlackOps4ShieldMenu', 'BlackoutBotsBO4', 'Abomination-Unofficial', 'Synergy-BO4-GSC-Menu', 't8-tests', 'Shield-Menu-BO4', 'bo4-pap-mod', 'demo_mods')
    prior = set()
    for directory in prior_roots:
        prior |= collect(ROOT / 'borrowed' / directory)
    print('\n'.join(sorted(collect(ROOT / 'borrowed' / 'shield_mods') - prior)))
