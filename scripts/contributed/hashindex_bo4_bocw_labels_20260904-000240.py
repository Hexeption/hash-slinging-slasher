#!/usr/bin/env python3
"""Emit HashIndex's BO4/BOCW global, script, and generic plaintext labels."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FILES = (
    'hashes/global/bo4.csv',
    'hashes/scr/bo4.csv',
    'hashes/scr/bocw.csv',
    'hashes/xassets/strings.csv',
)

if __name__ == '__main__':
    index = ROOT / 'borrowed' / 'HashIndex'
    names = set()
    for relative in FILES:
        for line in (index / relative).read_text(encoding='utf-8', errors='ignore').splitlines():
            _, separator, name = line.partition(',')
            name = name.strip()
            if separator and name:
                names.add(name)
    print('\n'.join(sorted(names)))
