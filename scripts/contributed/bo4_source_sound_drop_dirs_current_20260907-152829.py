"""Drop one interior directory from harvested BO4 source sound paths."""
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
ledger = ROOT / "logs" / "bo4_source_sound_paths_current_20260905.raw"
out = set()
seeds = 0
for raw in ledger.read_text(encoding="utf-8", errors="ignore").splitlines():
    name = raw.strip().lower().replace("/", "\\")
    if not name:
        continue
    seeds += 1
    bits = name.split("\\")
    if len(bits) < 4:
        continue
    for index in range(1, len(bits) - 1):
        out.add("\\".join(bits[:index] + bits[index + 1:]))
print(f"{seeds:,} source paths, {len(out):,} dropped-directory candidates", file=sys.stderr)
for name in sorted(out):
    print(name)
