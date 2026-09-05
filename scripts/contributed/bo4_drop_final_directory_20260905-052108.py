"""Remove the final directory component from confirmed BO4 non-sound paths."""
import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
import snapshot

names = set()
for pool in ("xmodel", "material", "image", "xanim"):
    names.update(n.strip() for n in snapshot.confirmed_names(pool) if n.strip())
out = set()
for name in names:
    pos = name.rfind("/")
    if pos <= 0:
        continue
    parent = name[:pos]
    cut = parent.rfind("/")
    if cut < 0:
        continue
    out.add(parent[:cut + 1] + name[pos + 1:])
print(f"{len(names):,} seeds -> {len(out):,} candidates", file=sys.stderr)
for candidate in sorted(out):
    print(candidate)
