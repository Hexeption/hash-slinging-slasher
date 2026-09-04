#!/usr/bin/env python3
"""Emit compile-time string concatenations from the BO4 UI Lua source dump.

The preceding Lua pass checked individual literals.  Lua uses ``..`` rather
than GSC's ``+`` operator, so this extracts only uninterrupted chains where
every operand is itself a simple quoted literal.  Variables are never
substituted and no name pieces are invented.

Reads: borrowed/bo4-source-lua/**/*.lua
Writes: sorted candidate labels on stdout; --size reports the measured count.
"""

import argparse
from pathlib import Path
import re
import sys


ROOT = Path(__file__).resolve().parents[1] / "borrowed" / "bo4-source-lua"
RUN = re.compile(r"(?:[\"'][A-Za-z0-9_./-]{1,160}[\"']\s*\.\.\s*)+[\"'][A-Za-z0-9_./-]{1,160}[\"']")
PART = re.compile(r"[\"']([A-Za-z0-9_./-]{1,160})[\"']")
LETTERS = re.compile(r"[A-Za-z]")


def plausible(value: str) -> bool:
    return (
        6 <= len(value) <= 160
        and ("_" in value or "/" in value)
        and len(LETTERS.findall(value)) >= 3
        and not value.startswith(("function_", "hash_", "var_"))
    )


def candidates() -> set[str]:
    found: set[str] = set()
    files = 0
    for path in ROOT.rglob("*.lua"):
        files += 1
        try:
            source = path.read_text(encoding="utf-8", errors="ignore")
        except OSError as error:
            print(f"skipping {path}: {error}", file=sys.stderr)
            continue
        for run in RUN.finditer(source):
            value = "".join(PART.findall(run.group())).lower()
            if plausible(value):
                found.add(value)
    print(f"{files:,} UI Lua files -> {len(found):,} literal concatenations", file=sys.stderr)
    return found


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--size", action="store_true")
    options = parser.parse_args()
    found = candidates()
    if not options.size:
        print("\n".join(sorted(found)))


if __name__ == "__main__":
    main()
