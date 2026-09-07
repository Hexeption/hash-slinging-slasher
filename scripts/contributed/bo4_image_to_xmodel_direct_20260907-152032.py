"""Probe direct i_-to-xmodel_ relabelings from confirmed BO4 image names."""
import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
import snapshot

names = snapshot.confirmed_names("image")
out = set()
for name in names:
    name = name.strip()
    if name.startswith("i_"):
        out.add("xmodel_" + name[2:])
print(f"{len(names):,} seeds -> {len(out):,} candidates", file=sys.stderr)
for candidate in sorted(out):
    print(candidate)
