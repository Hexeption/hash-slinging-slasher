"""Reverse complete underscore-token sequences in Cold War xmodel basenames."""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
import snapshot

names = {name.strip() for name in snapshot.confirmed_names("xmodel") if name.strip()}
output = set()
for name in names:
    slash = name.rfind("/")
    prefix, stem = name[: slash + 1], name[slash + 1 :]
    tokens = stem.split("_")
    if len(tokens) < 3:
        continue
    reversed_stem = "_".join(reversed(tokens))
    if reversed_stem != stem:
        output.add(prefix + reversed_stem)

print(f"{len(names):,} seeds -> {len(output):,} candidates", file=sys.stderr)
for candidate in sorted(output):
    print(candidate)
