#!/usr/bin/env python3
"""Offer source-introduced BO4 alias tokens in their observed local contexts.

The global slotswap sweep predates the 24 UI-Lua aliases verified locally.
This pass measures substitutions from the complete alias corpus, but emits
only positions whose two-sided context occurs in one of those source aliases.
It therefore tests new source vocabulary without reopening unrelated slots.

Reads: BO4 UI-Lua sound_alias findings and current sound-alias tables.
Writes: context-preserving substitution candidates on stdout.
"""

import argparse
import collections
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
import snapshot

SEEDS = ROOT / 'findings' / 'blkops04' / 'run_20260903-215921_list' / 'sound_alias.txt'


def split(name: str) -> tuple[list[str], list[str]]:
    texts, marks, current = [], [], ''
    for char in name:
        if char in '_/':
            texts.append(current)
            marks.append(char)
            current = ''
        else:
            current += char
    texts.append(current)
    marks.append('')
    return texts, marks


def shape(token: str) -> str:
    out, digits = [], False
    for char in token:
        if char.isdigit():
            if not digits:
                out.append('#')
                digits = True
        else:
            out.append(char)
            digits = False
    return ''.join(out)


def contexts(name: str) -> list[tuple[str, str]]:
    texts, _ = split(name)
    return [
        (shape(texts[index - 1]) if index else '^', shape(texts[index + 1]) if index + 1 < len(texts) else '$')
        for index in range(len(texts))
    ]


def source_seeds() -> set[str]:
    return {line.partition(',')[2].strip().lower() for line in SEEDS.read_text(encoding='utf-8', errors='ignore').splitlines() if ',' in line}


def candidates() -> set[str]:
    seeds = source_seeds()
    names = set(snapshot.table_names('fnv1a_soundbanks_aliases'))
    names.update(snapshot.confirmed_names('sound_alias'))
    names = {name.strip().lower().replace('\\', '/') for name in names if name.strip()}
    wanted = {context for seed in seeds for context in contexts(seed)}
    alphabet: dict[tuple[str, str], collections.Counter[str]] = collections.defaultdict(collections.Counter)
    for name in names:
        texts, _ = split(name)
        for context, token in zip(contexts(name), texts):
            if context in wanted and token and not token.isdigit():
                alphabet[context][token] += 1
    output: set[str] = set()
    active = 0
    for name in names:
        texts, marks = split(name)
        for index, (context, token) in enumerate(zip(contexts(name), texts)):
            choices = alphabet.get(context)
            if not choices or token.isdigit() or len(choices) < 2:
                continue
            active += 1
            for replacement, count in choices.most_common(16):
                if replacement == token or count < 2:
                    continue
                revised = texts.copy()
                revised[index] = replacement
                candidate = ''.join(text + mark for text, mark in zip(revised, marks))
                if candidate not in names:
                    output.add(candidate)
    print(f'{len(seeds)} UI aliases; {len(wanted)} source contexts; {active} source-context slots; {len(output):,} candidates', file=sys.stderr)
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
