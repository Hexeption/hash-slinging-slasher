"""Delete the final underscore token from confirmed BO4 material names."""
import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
import snapshot

names = {n.strip() for n in snapshot.confirmed_names("material") if n.strip()}
out = set()
for name in names:
    pos = name.rfind("/")
    prefix, stem = name[:pos + 1], name[pos + 1:]
    if "_" not in stem:
        continue
    out.add(prefix + stem.rsplit("_", 1)[0])
print(f"{len(names):,} seeds -> {len(out):,} candidates", file=sys.stderr)
for candidate in sorted(out):
    print(candidate)
