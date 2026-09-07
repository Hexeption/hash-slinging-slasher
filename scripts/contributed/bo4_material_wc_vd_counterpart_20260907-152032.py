"""Probe the BO4 material wc/ <-> vd/ directory counterpart."""
import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
import snapshot

names = {n.strip() for n in snapshot.confirmed_names("material") if n.strip()}
out = set()
for name in names:
    if name.startswith("wc/"):
        out.add("vd/" + name[3:])
    elif name.startswith("vd/"):
        out.add("wc/" + name[3:])
print(f"{len(names):,} seeds -> {len(out):,} candidates", file=sys.stderr)
for candidate in sorted(out):
    print(candidate)
