"""Probe direct i_-to-mtl_ relabelings from confirmed BO4 image names."""
from pathlib import Path
import sys
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
import snapshot

names = snapshot.confirmed_names("image")
out = set()
for name in names:
    name = name.strip()
    if name.startswith("i_"):
        out.add("mtl_" + name[2:])
print(f"{len(names):,} seeds -> {len(out):,} candidates", file=sys.stderr)
for candidate in sorted(out):
    print(candidate)
