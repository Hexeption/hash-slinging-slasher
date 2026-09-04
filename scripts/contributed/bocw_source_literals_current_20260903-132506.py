"""Extract asset-shaped literals from the borrowed Cold War source corpus.

Run with ``python scripts/contrib/bocw_source_literals_current.py``. Reads
``borrowed/bocw-source`` and writes deduplicated candidate literals to stdout.
Reusable for future corpus refreshes.
"""
import os
import re
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))
while ROOT != os.path.dirname(ROOT) and not os.path.isfile(os.path.join(ROOT, "scripts", "snapshot.py")):
    ROOT = os.path.dirname(ROOT)

TOKEN = re.compile(r"[A-Za-z0-9][A-Za-z0-9_./\\-]{5,159}")
QUOTED = re.compile(r'''[\"']([^\"'\r\n]{6,160})[\"']''')
EXTENSIONS = {"", ".gsc", ".csc", ".cfg", ".csv", ".ddl", ".gdb", ".graph",
              ".raw", ".txt", ".json", ".md", ".lua", ".menu", ".def"}


def keep(value):
    value = value.strip().lower().replace("\\", "/")
    if len(value) < 6 or len(value) > 160 or ("_" not in value and "/" not in value):
        return None
    if sum(ch.isalpha() for ch in value) < 3 or value.startswith(("http://", "https://", "www.")):
        return None
    return value


def main():
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="ignore")
    source = os.path.join(ROOT, "borrowed", "bocw-source")
    values = set()
    files = 0
    for directory, _, filenames in os.walk(source):
        for filename in filenames:
            if os.path.splitext(filename)[1].lower() not in EXTENSIONS:
                continue
            files += 1
            try:
                data = open(os.path.join(directory, filename), encoding="utf-8", errors="ignore").read()
            except OSError:
                continue
            for match in TOKEN.finditer(data):
                value = keep(match.group())
                if value:
                    values.add(value)
            for match in QUOTED.finditer(data):
                value = keep(match.group(1))
                if value:
                    values.add(value)
    print(f"{files:,} files -> {len(values):,} literals", file=sys.stderr)
    sys.stdout.write("\n".join(sorted(values)))
    if values:
        sys.stdout.write("\n")


if __name__ == "__main__":
    main()
