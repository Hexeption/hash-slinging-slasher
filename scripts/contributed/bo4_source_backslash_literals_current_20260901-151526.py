"""Extract backslash-bearing asset-shaped literals from the BO4 source dump."""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SOURCE = ROOT / "borrowed" / "bo4-source"
TOKEN = re.compile(r"[A-Za-z0-9][A-Za-z0-9_./\\-]{5,180}")
EXTENSIONS = {".gsc", ".csc", ".csv", ".ddl", ".txt", ".raw", ".gdb", ".cfg", ".vision"}


def main():
    names = set()
    files = 0
    for path in SOURCE.rglob("*"):
        if not path.is_file() or path.suffix.lower() not in EXTENSIONS:
            continue
        files += 1
        try:
            body = path.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            continue
        for match in TOKEN.finditer(body):
            value = match.group().lower()
            if "\\" not in value or "_" not in value or sum(ch.isalpha() for ch in value) < 3:
                continue
            names.add(value)
    for value in sorted(names):
        print(value)
    print(f"{len(names):,} backslash-bearing source literals from {files:,} files", file=sys.stderr)


if __name__ == "__main__":
    main()
