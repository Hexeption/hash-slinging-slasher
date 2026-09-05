"""Probe xanim names formed by deleting their final underscore token."""
import os, sys
ROOT = os.path.dirname(os.path.abspath(__file__))
while ROOT != os.path.dirname(ROOT) and not os.path.isfile(os.path.join(ROOT, "scripts", "snapshot.py")):
    ROOT = os.path.dirname(ROOT)
sys.path.insert(0, os.path.join(ROOT, "scripts"))
import snapshot
known = {n.strip().lower().replace("\\", "/") for n in snapshot.table_names("fnv1a_xanims")}
known |= {n.strip().lower().replace("\\", "/") for n in snapshot.confirmed_names("xanim")}
seen = set()
for name in known:
    if "_" not in name:
        continue
    candidate = name.rsplit("_", 1)[0]
    if candidate and candidate not in known:
        seen.add(candidate)
print(f"{len(known)} known xanims; {len(seen)} final-token deletions", file=sys.stderr)
for candidate in sorted(seen):
    print(candidate)
