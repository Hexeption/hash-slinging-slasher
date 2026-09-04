#!/usr/bin/env python3
"""Emit exact T9 decompiled-source literals absent from prior Cold War sources."""
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
LITERAL = re.compile(r'(?:#)?"([A-Za-z0-9_./-]{6,160})"')
EXTENSIONS = {'.gsc', '.csc', '.cfg', '.csv', '.ddl', '.gdb', '.graph', '.raw', '.txt', '.vision'}


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
    prior_roots = ('bocw-source', 'ColdWarGSCMenu', 'coldwar.gsc', 'cwmenu', 'ColdWar-Lucy-Base')
    prior = set()
    for directory in prior_roots:
        prior |= collect(ROOT / 'borrowed' / directory)
    print('\n'.join(sorted(collect(ROOT / 'borrowed' / 't9-src') - prior)))
