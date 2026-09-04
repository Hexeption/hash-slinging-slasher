"""Decode C-style escaped BO4 source literals that raw string scans cannot see.

Run: python contrib/bo4_source_escaped_literals.py | bin\\windows\\confirm_list.exe - --game BLKOPS04 --no-fold --label "BO4 escaped source literals" --script contrib/bo4_source_escaped_literals.py
Reads: borrowed/bo4-source text-like files. Writes: one decoded, asset-shaped candidate per line.
Reusable after the borrowed source corpus changes. This is a new source representation; its
candidate count and matches are measured by confirm_list, not assumed here.
"""
import codecs
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
while ROOT != ROOT.parent and not (ROOT / "scripts" / "snapshot.py").is_file():
    ROOT = ROOT.parent

SOURCE = ROOT / "borrowed" / "bo4-source"
QUOTED = re.compile(r'"((?:\\\\.|[^"\\\\]){6,220})"')
TOKEN = re.compile(r"[A-Za-z0-9][A-Za-z0-9_./\\\\-]{5,180}$")
EXTENSIONS = {".gsc", ".csc", ".csv", ".ddl", ".txt", ".raw", ".gdb", ".cfg", ".vision", ".json"}


def decode(value):
    try:
        return codecs.decode(value, "unicode_escape")
    except UnicodeDecodeError:
        return ""


def main():
    candidates = set()
    files = 0
    for path in SOURCE.rglob("*"):
        if not path.is_file() or path.suffix.lower() not in EXTENSIONS:
            continue
        files += 1
        try:
            text = path.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            continue
        for match in QUOTED.finditer(text):
            raw = match.group(1)
            if "\\" not in raw:
                continue
            value = decode(raw).strip().lower()
            if not TOKEN.fullmatch(value) or "_" not in value:
                continue
            if sum(ch.isalpha() for ch in value) < 3:
                continue
            candidates.add(value)
    for value in sorted(candidates):
        print(value)
    print(f"{len(candidates):,} decoded escaped literals from {files:,} source files", file=sys.stderr)


if __name__ == "__main__":
    main()
