#!/usr/bin/env python3
"""Recover BO4 UI-Lua strings assembled solely from file-local constants.

Unlike the literal-concatenation pass, this follows a Lua identifier only when
its latest preceding assignment is itself a fully static concatenation of
quoted literals and previously proven constants.  Runtime values, table
lookups, function calls and unknown identifiers stop evaluation rather than
being guessed.

Reads: borrowed/bo4-source-lua/**/*.lua
Writes: candidate labels to stdout; --size reports the candidate count.
"""

import argparse
from pathlib import Path
import re
import sys


ROOT = Path(__file__).resolve().parents[1] / "borrowed" / "bo4-source-lua"
ATOM = r'(?:"[A-Za-z0-9_./-]{1,160}"|\'[A-Za-z0-9_./-]{1,160}\'|[A-Za-z_][A-Za-z0-9_]*)'
CHAIN = re.compile(rf'(?<![A-Za-z0-9_]){ATOM}(?:\s*\.\.\s*{ATOM})+(?![A-Za-z0-9_])')
TOKEN = re.compile(r'"([A-Za-z0-9_./-]{1,160})"|\'([A-Za-z0-9_./-]{1,160})\'|([A-Za-z_][A-Za-z0-9_]*)')
ASSIGNMENT = re.compile(r'^(?:local\s+)?([A-Za-z_][A-Za-z0-9_]*)\s*=\s*(.+?)(?:\s*--.*)?$')
LETTERS = re.compile(r'[A-Za-z]')


def evaluate(expression: str, constants: dict[str, str]) -> str | None:
    if not re.fullmatch(rf'{ATOM}(?:\s*\.\.\s*{ATOM})*', expression.strip()):
        return None
    pieces: list[str] = []
    for match in TOKEN.finditer(expression):
        literal = match.group(1) or match.group(2)
        if literal is not None:
            pieces.append(literal)
        elif match.group(3) in constants:
            pieces.append(constants[match.group(3)])
        else:
            return None
    return ''.join(pieces)


def plausible(value: str) -> bool:
    return (
        6 <= len(value) <= 160
        and ('_' in value or '/' in value)
        and len(LETTERS.findall(value)) >= 3
        and not value.startswith(('function_', 'hash_', 'var_'))
    )


def candidates() -> set[str]:
    found: set[str] = set()
    files = 0
    for path in ROOT.rglob('*.lua'):
        files += 1
        try:
            lines = path.read_text(encoding='utf-8', errors='ignore').splitlines()
        except OSError as error:
            print(f'skipping {path}: {error}', file=sys.stderr)
            continue
        constants: dict[str, str] = {}
        for line in lines:
            assignment = ASSIGNMENT.match(line.strip())
            if assignment:
                name, expression = assignment.groups()
                value = evaluate(expression, constants)
                if value is None:
                    constants.pop(name, None)
                else:
                    constants[name] = value
            for chain in CHAIN.findall(line):
                value = evaluate(chain, constants)
                if value and plausible(value):
                    found.add(value.lower())
    print(f'{files:,} UI Lua files -> {len(found):,} constant-bound concatenations', file=sys.stderr)
    return found


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument('--size', action='store_true')
    options = parser.parse_args()
    found = candidates()
    if not options.size:
        print('\n'.join(sorted(found)))


if __name__ == '__main__':
    main()
