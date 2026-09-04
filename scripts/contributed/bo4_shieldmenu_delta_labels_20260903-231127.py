#!/usr/bin/env python3
"""Emit exact Shield Menu labels not already carried by earlier BO4 sources."""
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
LITERAL = re.compile(r'(?:#)?"([A-Za-z0-9_./-]{6,160})"')
EXTENSIONS = {'.gsc', '.csc', '.cfg', '.csv', '.ddl', '.gdb', '.graph', '.raw', '.txt', '.vision'}


def acceptable(name: str) -> str | None:
    name = name.strip().lower()
    if len(name) < 6 or len(name) > 160:
        return None
    if not re.fullmatch(r'[a-z0-9_./-]+', name):
        return None
    if '_' not in name and '/' not in name:
        return None
    return name if sum(char.isalpha() for char in name) >= 3 else None


def literals(root: Path) -> set[str]:
    names = set()
    for path in root.rglob('*'):
        if not path.is_file() or path.suffix.lower() not in EXTENSIONS:
            continue
        for raw in LITERAL.findall(path.read_text(encoding='utf-8', errors='ignore')):
            if name := acceptable(raw):
                names.add(name)
    return names


def hash_labels(root: Path) -> set[str]:
    path = root / 'hashes.txt'
    if not path.exists():
        return set()
    names = set()
    for line in path.read_text(encoding='utf-8', errors='ignore').splitlines():
        _, separator, raw = line.partition(',')
        if separator and (name := acceptable(raw)):
            names.add(name)
    return names


if __name__ == '__main__':
    old_roots = ('bo4-source', 't8-src', 'BO4-BlackoutBots', 'bo4-lucy-menu')
    prior = set()
    for directory in old_roots:
        root = ROOT / 'borrowed' / directory
        prior |= literals(root) | hash_labels(root)
    current = ROOT / 'borrowed' / 'BO4-BlackOps4ShieldMenu'
    print('\n'.join(sorted((literals(current) | hash_labels(current)) - prior)))
