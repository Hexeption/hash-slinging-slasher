"""Probe direct xmodel-to-xanim relabelings from confirmed BO4 names."""
from pathlib import Path
import sys
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
import snapshot

names = snapshot.confirmed_names("xmodel")
out = set()
for name in names:
    name = name.strip()
    if name.startswith("xmodel_"):
        out.add("xanim_" + name[len("xmodel_"):])
print(f"{len(names):,} seeds -> {len(out):,} candidates", file=sys.stderr)
for candidate in sorted(out):
    print(candidate)
