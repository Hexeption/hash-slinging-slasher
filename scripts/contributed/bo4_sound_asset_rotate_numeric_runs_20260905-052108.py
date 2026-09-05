"""Cyclically left-rotate each multi-digit run in BO4 SAB sound basenames."""
from pathlib import Path
import re, sys
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
import snapshot

names = {n.strip() for n in snapshot.confirmed_names("sound_asset") if n.strip()}
names.update(n.strip() for n in snapshot.table_names("fnv1a_english_xsounds") if n.strip())
out = set()
for name in names:
    pos = max(name.rfind("\\"), name.rfind("/"))
    base = name[pos + 1:]
    stem, sep, tail = base.partition(".")
    changed = [False]
    def rotate(match):
        value = match.group(0)
        changed[0] = True
        return value[1:] + value[0]
    new_stem = re.sub(r"\d{2,}", rotate, stem)
    if changed[0]:
        out.add(name[:pos + 1] + new_stem + (sep + tail if sep else ""))
print(f"{len(names):,} seeds -> {len(out):,} candidates", file=sys.stderr)
for candidate in sorted(out):
    print(candidate)
