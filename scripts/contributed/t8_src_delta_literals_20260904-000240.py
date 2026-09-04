#!/usr/bin/env python3
"""Emit only exact T8-source literals absent from the prior BO4 source dump."""
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
LITERAL = re.compile(r'(?:#)?"([A-Za-z0-9_./-]{6,160})"')

def collect(root: Path) -> set[str]:
    names = set()
    for path in root.rglob('*'):
        if not path.is_file() or path.suffix.lower() not in {'.gsc', '.csc', '.cfg', '.csv', '.ddl', '.gdb', '.graph', '.raw', '.txt', '.vision'}:
            continue
        for name in LITERAL.findall(path.read_text(encoding='utf-8', errors='ignore')):
            name = name.lower()
            if ('_' in name or '/' in name) and sum(char.isalpha() for char in name) >= 3:
                names.add(name)
    return names

if __name__ == '__main__':
    print('\n'.join(sorted(collect(ROOT / 'borrowed' / 't8-src') - collect(ROOT / 'borrowed' / 'bo4-source'))))
