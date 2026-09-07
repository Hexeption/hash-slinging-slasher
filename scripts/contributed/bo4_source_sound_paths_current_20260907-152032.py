"""Extract unfolded BO4 .snd paths from the repository's source tree."""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "borrowed" / "bo4-source"
PATH = re.compile(r"[A-Za-z0-9_./\\-]{6,180}\.([A-Za-z0-9]+)\.snd", re.IGNORECASE)
EXTENSIONS = {".gsc", ".csc", ".csv", ".ddl", ".txt", ".raw", ".gdb", ".cfg", ".vision"}

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
    for match in PATH.finditer(body):
        value = match.group().lower().replace("/", "\\")
        if "\\" in value and sum(ch.isalpha() for ch in value) >= 3:
            names.add(value)

print(f"{len(names):,} unfolded source sound paths from {files:,} files", file=sys.stderr)
for name in sorted(names):
    print(name)
