"""Reverse complete dotted extension tails of known BO4 SAB sound paths."""
from pathlib import Path
import sys
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
import snapshot

names = {n.strip() for n in snapshot.confirmed_names("sound_asset") if n.strip()}
names.update(n.strip() for n in snapshot.table_names("fnv1a_english_xsounds") if n.strip())
out = set()
for name in names:
    base = name.rsplit("\\", 1)[-1].rsplit("/", 1)[-1]
    if base.count(".") < 3:
        continue
    stem, tail = base.split(".", 1)
    parts = tail.split(".")
    if len(parts) < 3:
        continue
    pos = max(name.rfind("\\"), name.rfind("/"))
    out.add(name[:pos + 1] + stem + "." + ".".join(reversed(parts)))
print(f"{len(names):,} seeds -> {len(out):,} candidates", file=sys.stderr)
for candidate in sorted(out):
    print(candidate)
