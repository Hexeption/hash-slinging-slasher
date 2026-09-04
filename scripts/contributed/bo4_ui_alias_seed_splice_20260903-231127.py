#!/usr/bin/env python3
"""Splice BO4 sound aliases only through tokens introduced by UI-Lua evidence.

The generic shared-token splice was exhausted before the BO4 UI-Lua corpus
verified 24 additional aliases locally.  This deliberately does *not* rerun
that corpus: it uses only token families touched by those newly verified UI
aliases, joining real head/tail spellings around the same token.  Very common
tokens are excluded so a UI convention is not mistaken for a global rule.

Reads: the UI-Lua run's sound_alias findings plus current sound-alias tables.
Writes: source-seeded splice candidates to stdout; --size reports the count.
"""

import argparse
import collections
from pathlib import Path
import re
import sys


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
import snapshot

SEEDS = ROOT / 'findings' / 'blkops04' / 'run_20260903-215921_list' / 'sound_alias.txt'
TOKEN = re.compile(r'(?<![A-Za-z0-9])([A-Za-z][A-Za-z0-9-]{2,})(?![A-Za-z0-9])')


def source_seeds() -> set[str]:
    return {
        line.partition(',')[2].strip().lower()
        for line in SEEDS.read_text(encoding='utf-8', errors='ignore').splitlines()
        if ',' in line
    }


def candidates() -> set[str]:
    seeds = source_seeds()
    known = set(snapshot.table_names('fnv1a_soundbanks_aliases'))
    known.update(snapshot.confirmed_names('sound_alias'))
    known = {name.strip().lower().replace('\\', '/') for name in known if name.strip()}
    families: dict[str, list[str]] = collections.defaultdict(list)
    for name in known:
        for token in set(TOKEN.findall(name)):
            families[token].append(name)

    seeded_tokens = {token for seed in seeds for token in TOKEN.findall(seed)}
    output: set[str] = set()
    used = 0
    for token in sorted(seeded_tokens):
        family = families.get(token, [])
        if not 2 <= len(family) <= 480:
            continue
        used += 1
        pieces: list[tuple[str, str]] = []
        for name in family:
            for match in TOKEN.finditer(name):
                if match.group(1) == token:
                    pieces.append((name[:match.start()], name[match.start():]))
        for head, _ in pieces:
            for _, tail in pieces:
                candidate = head + tail
                if candidate not in known:
                    output.add(candidate)
    print(f'{len(seeds)} UI aliases; {used} bounded token families; {len(output):,} candidates', file=sys.stderr)
    return output


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument('--size', action='store_true')
    options = parser.parse_args()
    output = candidates()
    if not options.size:
        print('\n'.join(sorted(output)))


if __name__ == '__main__':
    main()
