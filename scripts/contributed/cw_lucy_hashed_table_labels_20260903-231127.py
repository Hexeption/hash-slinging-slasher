#!/usr/bin/env python3
"""Emit explicit labels preserved in Cold War Lucy's hashed-table dump.

``UnsortedHashes2.txt`` contains tabular BO Cold War metadata with either an
explicit ``#label`` or an unresolved ``#hash_...`` placeholder.  Only exact,
non-placeholder labels are retained.  They are independent of the regular
GSC literal harvest and are reverified against the game snapshots.

Reads: borrowed/ColdWar-Lucy-Base/UnsortedHashes2.txt and hashes.txt
Writes: unique exact labels on stdout.
"""

from pathlib import Path
import re


ROOT = Path(__file__).resolve().parents[1] / 'borrowed' / 'ColdWar-Lucy-Base'
TAG = re.compile(r'(?<![A-Za-z0-9_])#([A-Za-z0-9_./-]{3,160})')


def main() -> None:
    labels: set[str] = set()
    for path in (ROOT / 'UnsortedHashes2.txt', ROOT / 'hashes.txt'):
        for line in path.read_text(encoding='utf-8', errors='ignore').splitlines():
            for label in TAG.findall(line):
                if not label.startswith('hash_'):
                    labels.add(label.lower())
            _hash, delimiter, label = line.partition(',')
            if delimiter:
                label = label.strip().lower()
                if re.fullmatch(r'[a-z0-9_./-]{3,160}', label):
                    labels.add(label)
    print('\n'.join(sorted(labels)))


if __name__ == '__main__':
    main()
