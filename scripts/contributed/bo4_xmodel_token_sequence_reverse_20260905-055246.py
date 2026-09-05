"""Reverse complete underscore-token sequences in BO4 xmodel basenames."""
import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
import snapshot

names = {n.strip() for n in snapshot.confirmed_names("xmodel") if n.strip()}
out = set()
for name in names:
    pos = name.rfind("/")
    prefix, stem = name[:pos + 1], name[pos + 1:]
    tokens = stem.split("_")
    if len(tokens) < 3:
        continue
    rev = "_".join(reversed(tokens))
    if rev != stem:
        out.add(prefix + rev)
print(f"{len(names):,} seeds -> {len(out):,} candidates", file=sys.stderr)
for candidate in sorted(out):
    print(candidate)
