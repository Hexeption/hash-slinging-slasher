"""Probe the untested BO4 material mc/ <-> mcs/ directory counterpart."""
import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
import snapshot

names = {n.strip() for n in snapshot.confirmed_names("material") if n.strip()}
out = set()
for name in names:
    if name.startswith("mc/"):
        out.add("mcs/" + name[3:])
    elif name.startswith("mcs/"):
        out.add("mc/" + name[4:])
print(f"{len(names):,} seeds -> {len(out):,} candidates", file=sys.stderr)
for candidate in sorted(out):
    print(candidate)
