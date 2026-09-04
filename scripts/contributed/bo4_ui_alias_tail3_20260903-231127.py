#!/usr/bin/env python3
"""Replace the final three bytes of only the BO4 UI-Lua verified aliases.

This is the tail derivation restricted to the 24 exact aliases introduced by
the independent UI source, rather than re-running the 47-billion-candidate
global tail pass.  The 37-character alphabet is measured from known names.

Reads: BO4 UI-Lua alias findings and the current name corpus.
Writes: source-seeded three-byte tail variants on stdout.
"""

import itertools
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
import tails

SEEDS = ROOT / 'findings' / 'blkops04' / 'run_20260903-215921_list' / 'sound_alias.txt'


def main() -> None:
    seeds = {line.partition(',')[2].strip().lower() for line in SEEDS.read_text(encoding='utf-8', errors='ignore').splitlines() if ',' in line}
    alphabet = tails.alphabet_of(tails.known_names(), tails.ALPHABET)
    endings = [''.join(chars) for chars in itertools.product(alphabet, repeat=3)]
    print(f'{len(seeds)} UI aliases x {len(endings):,} measured tails', file=sys.stderr)
    for stem in sorted({name[:-3] for name in seeds if len(name) > 7}):
        for ending in endings:
            print(stem + ending)


if __name__ == '__main__':
    main()
