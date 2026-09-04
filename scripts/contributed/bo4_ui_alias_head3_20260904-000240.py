#!/usr/bin/env python3
"""Replace the first three bytes of only the BO4 UI-Lua verified aliases.

The source-tail pass is negative.  This is its unmeasured mirror, retaining
the complete UI-derived suffix and trying only the measured 38-character name
front alphabet.  It is restricted to the independent source seeds.
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
    alphabet = tails.alphabet_of(tails.known_names(), tails.ALPHABET, head=True)
    heads = [''.join(chars) for chars in itertools.product(alphabet, repeat=3)]
    print(f'{len(seeds)} UI aliases x {len(heads):,} measured heads', file=sys.stderr)
    for tail in sorted({name[3:] for name in seeds if len(name) > 7}):
        for head in heads:
            print(head + tail)


if __name__ == '__main__':
    main()
