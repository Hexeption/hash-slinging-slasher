"""Sort numeric underscore tokens by value in BO4 SAB sound basenames."""
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
    tokens = stem.split("_")
    numeric = [(i, int(t), t) for i, t in enumerate(tokens) if re.fullmatch(r"\d+", t)]
    if len(numeric) < 2:
        continue
    ordered = sorted((value, text) for _, value, text in numeric)
    if [value for _, value, _ in numeric] == [value for value, _ in ordered]:
        continue
    rebuilt = list(tokens)
    for (index, _, _), (_, text) in zip(numeric, ordered):
        rebuilt[index] = text
    out.add(name[:pos + 1] + "_".join(rebuilt) + (sep + tail if sep else ""))
print(f"{len(names):,} seeds -> {len(out):,} candidates", file=sys.stderr)
for candidate in sorted(out):
    print(candidate)
