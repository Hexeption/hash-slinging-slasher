"""Sort out-of-order numeric underscore tokens in BO4 non-sound names."""
from pathlib import Path
import re, sys
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
import snapshot

names = set()
for pool in ("xmodel", "material", "image", "xanim"):
    names.update(n.strip() for n in snapshot.confirmed_names(pool) if n.strip())
out = set()
for name in names:
    pos = max(name.rfind("\\"), name.rfind("/"))
    stem = name[pos + 1:]
    tokens = stem.split("_")
    nums = [(i, int(t), t) for i, t in enumerate(tokens) if re.fullmatch(r"\d+", t)]
    if len(nums) < 2:
        continue
    ordered = sorted((v, t) for _, v, t in nums)
    if [v for _, v, _ in nums] == [v for v, _ in ordered]:
        continue
    rebuilt = list(tokens)
    for (idx, _, _), (_, text) in zip(nums, ordered):
        rebuilt[idx] = text
    out.add(name[:pos + 1] + "_".join(rebuilt))
print(f"{len(names):,} seeds -> {len(out):,} candidates", file=sys.stderr)
for candidate in sorted(out):
    print(candidate)
