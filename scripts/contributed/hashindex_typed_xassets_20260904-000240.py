#!/usr/bin/env python3
"""Emit the plaintext labels from HashIndex's typed xasset CSVs."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FILES = ('xanims.csv', 'ximages.csv', 'xmaterials.csv', 'xmodels.csv', 'xsounds.csv')

if __name__ == '__main__':
    root = ROOT / 'borrowed' / 'HashIndex' / 'hashes' / 'xassets'
    names = set()
    for filename in FILES:
        for line in (root / filename).read_text(encoding='utf-8', errors='ignore').splitlines():
            _, separator, name = line.partition(',')
            name = name.strip()
            if separator and name:
                names.add(name)
    print('\n'.join(sorted(names)))
