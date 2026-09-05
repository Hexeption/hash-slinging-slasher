"""Substitute basename tokens using alternatives in the harvested BO4 sound source paths."""
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
LEDGER = ROOT / "logs" / "bo4_source_sound_paths_current_20260905.raw"
by_dir = {}
rows = []
for raw in LEDGER.read_text(encoding="utf-8", errors="ignore").splitlines():
    name = raw.strip().lower().replace("/", "\\")
    cut = name.rfind("\\")
    if cut < 0:
        continue
    base = name[cut + 1:]
    dot = base.find(".")
    if dot <= 0:
        continue
    core, tail = base[:dot], base[dot:]
    parts = core.split("_")
    if len(parts) < 3:
        continue
    directory = name[:cut]
    rows.append((directory, parts, tail))
    by_dir.setdefault(directory, set()).update(parts[1:-1])
out = set()
for directory, parts, tail in rows:
    for i in range(1, len(parts) - 1):
        for token in by_dir[directory]:
            if token != parts[i]:
                out.add(directory + "\\" + "_".join(parts[:i] + [token] + parts[i + 1:]) + tail)
print(f"{len(rows):,} source paths, {len(out):,} contextual-token candidates", file=sys.stderr)
for candidate in sorted(out):
    print(candidate)
