#!/usr/bin/env python3
"""Emit exact asset-shaped literals from two independent public Cold War mods.

These are developer GSC sources, deliberately separate from the retail-source
dump.  Only quoted literals with an underscore or path separator are emitted;
no identifiers, generated variants, or hashes are guessed.

Reads: borrowed/ColdWarGSCMenu and borrowed/coldwar.gsc (*.gsc)
Writes: unique candidate labels on stdout.
"""

from pathlib import Path
import re


ROOT = Path(__file__).resolve().parents[1]
CORPORA = (ROOT / 'borrowed' / 'ColdWarGSCMenu', ROOT / 'borrowed' / 'coldwar.gsc')
LITERAL = re.compile(r'(?:#)?"([A-Za-z0-9_./-]{6,160})"')
LETTERS = re.compile(r'[A-Za-z]')


def main() -> None:
    names: set[str] = set()
    for corpus in CORPORA:
        for path in corpus.rglob('*.gsc'):
            try:
                text = path.read_text(encoding='utf-8', errors='ignore')
            except OSError:
                continue
            for name in LITERAL.findall(text):
                name = name.lower()
                if ('_' in name or '/' in name) and len(LETTERS.findall(name)) >= 3:
                    names.add(name)
    print('\n'.join(sorted(names)))


if __name__ == '__main__':
    main()
