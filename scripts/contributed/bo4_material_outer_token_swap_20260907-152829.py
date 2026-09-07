"""Swap first/last basename tokens in confirmed BO4 material paths."""
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
    tokens = stem.split("_")
    if len(tokens) < 3 or tokens[0] == tokens[-1]:
        continue
    tokens[0], tokens[-1] = tokens[-1], tokens[0]
    out.add(prefix + "_".join(tokens))
print(f"{len(names):,} seeds -> {len(out):,} candidates", file=sys.stderr)
for candidate in sorted(out):
    print(candidate)
