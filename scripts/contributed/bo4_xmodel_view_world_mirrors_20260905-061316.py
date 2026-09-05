"""Generate missing terminal view/world xmodel mirrors from BO4 controls."""
import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
import snapshot

names = {n.strip() for n in snapshot.confirmed_names("xmodel") if n.strip()}
out = set()
for name in names:
    if name.endswith("_view"):
        out.add(name[:-5] + "_world")
    elif name.endswith("_world"):
        out.add(name[:-6] + "_view")
print(f"{len(names):,} seeds -> {len(out):,} candidates", file=sys.stderr)
for candidate in sorted(out):
    print(candidate)
