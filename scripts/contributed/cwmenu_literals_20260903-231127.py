#!/usr/bin/env python3
"""Emit exact asset-shaped literals from the public cwmenu GSC corpus.

This is a sibling, but non-identical, Cold War menu source. Only direct
quoted literals are used; there are no inferred identifiers or variants.
"""
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1] / 'borrowed' / 'cwmenu'
LITERAL = re.compile(r'(?:#)?"([A-Za-z0-9_./-]{6,160})"')

def main() -> None:
    names = set()
    for path in ROOT.rglob('*.gsc'):
        for name in LITERAL.findall(path.read_text(encoding='utf-8', errors='ignore')):
            name = name.lower()
            if ('_' in name or '/' in name) and sum(char.isalpha() for char in name) >= 3:
                names.add(name)
    print('\n'.join(sorted(names)))

if __name__ == '__main__':
    main()
