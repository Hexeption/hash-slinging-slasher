#!/usr/bin/env python3
"""Emit exact labels from BO4 Lucy Menu's curated hashes.txt mapping.

The menu includes a hand-maintained ``hex hash, label`` file.  This treats the
label field as an external name corpus, independent of the generic script
literal harvest; hashes are ignored and every label is reverified against the
target snapshots.

Reads: borrowed/bo4-lucy-menu/hashes.txt
Writes: unique labels on stdout.
"""

from pathlib import Path


SOURCE = Path(__file__).resolve().parents[1] / 'borrowed' / 'bo4-lucy-menu' / 'hashes.txt'


def main() -> None:
    names: set[str] = set()
    for line in SOURCE.read_text(encoding='utf-8', errors='ignore').splitlines():
        _hash, delimiter, name = line.partition(',')
        if delimiter and name.strip():
            names.add(name.strip())
    print('\n'.join(sorted(names)))


if __name__ == '__main__':
    main()
