"""Rotate characters in the final alphabetic token of BO4 xanim basenames."""
from pathlib import Path
import re, sys
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
import snapshot

names = snapshot.confirmed_names("xanim")
out = set()
for name in names:
    name = name.strip()
    pos = max(name.rfind("\\"), name.rfind("/"))
    prefix, stem = name[:pos + 1], name[pos + 1:]
    tokens = stem.split("_")
    if not tokens or not re.fullmatch(r"[A-Za-z]{3,}", tokens[-1]):
        continue
    value = tokens[-1]
    tokens[-1] = value[1:] + value[0]
    out.add(prefix + "_".join(tokens))
print(f"{len(names):,} seeds -> {len(out):,} candidates", file=sys.stderr)
for candidate in sorted(out):
    print(candidate)
