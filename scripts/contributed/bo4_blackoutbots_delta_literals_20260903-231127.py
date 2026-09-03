#!/usr/bin/env python3
"""Emit BO4 BlackoutBots literals not present in prior BO4 source corpora."""
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
    prior = collect(ROOT / 'borrowed' / 'bo4-source') | collect(ROOT / 'borrowed' / 't8-src')
    print('\n'.join(sorted(collect(ROOT / 'borrowed' / 'BO4-BlackoutBots') - prior)))
