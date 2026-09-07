"""Delete or duplicate one interior token in harvested BO4 sound paths."""
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
ledger = ROOT / "logs" / "bo4_source_sound_paths_current_20260905.raw"
out = set()
seeds = 0
for raw in ledger.read_text(encoding="utf-8", errors="ignore").splitlines():
    name = raw.strip().lower()
    if not name:
        continue
    seeds += 1
    cut = max(name.rfind("/"), name.rfind("\\")) + 1
    head, base = name[:cut], name[cut:]
    dot = base.find(".")
    if dot <= 0:
        continue
    core, tail = base[:dot], base[dot:]
    parts = core.split("_")
    if len(parts) < 3:
        continue
    for index in range(1, len(parts) - 1):
        out.add(head + "_".join(parts[:index] + parts[index + 1:]) + tail)
        out.add(head + "_".join(parts[:index] + [parts[index], parts[index]] + parts[index + 1:]) + tail)
print(f"{seeds:,} source paths, {len(out):,} token-edit candidates", file=sys.stderr)
for name in sorted(out):
    print(name)
