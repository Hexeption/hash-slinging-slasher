#!/usr/bin/env python3
"""Emit asset-shaped exact literals from the public BO4 UI Lua source dump.

This corpus is deliberately separate from ``borrowed/bo4-source`` (the GSC
and data dump already measured).  Lua UI scripts contain direct references to
icons, materials, models and sound aliases.  Candidates are only lower-cased,
matching normal asset hashing; no invented suffixes are added.

Reads: borrowed/bo4-source-lua/**/*.lua
Writes: sorted candidate labels on stdout.
"""

from pathlib import Path
import re
import sys


ROOT = Path(__file__).resolve().parents[1] / "borrowed" / "bo4-source-lua"
LITERAL = re.compile(r'(?<!\\)["\']([A-Za-z0-9_./-]{6,160})["\']')
LETTER = re.compile(r"[A-Za-z]")
NOISE_PREFIXES = ("function_", "hash_", "var_")


def plausible(value: str) -> bool:
    return (
        value.startswith(NOISE_PREFIXES) is False
        and ("_" in value or "/" in value)
        and len(LETTER.findall(value)) >= 3
    )


def main() -> None:
    names: set[str] = set()
    for path in ROOT.rglob("*.lua"):
        try:
            source = path.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            continue
        for literal in LITERAL.findall(source):
            literal = literal.lower()
            if plausible(literal):
                names.add(literal)
    print(f"{len(names):,} UI-Lua asset-shaped literals", file=sys.stderr)
    for name in sorted(names):
        print(name)


if __name__ == "__main__":
    main()
