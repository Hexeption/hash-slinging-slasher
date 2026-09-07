"""Probe aliases formed by duplicating the final underscore token."""
import os, sys
ROOT = os.path.dirname(os.path.abspath(__file__))
while ROOT != os.path.dirname(ROOT) and not os.path.isfile(os.path.join(ROOT, "scripts", "snapshot.py")):
    ROOT = os.path.dirname(ROOT)
sys.path.insert(0, os.path.join(ROOT, "scripts"))
import snapshot
known = {n.strip().lower().replace("\\", "/") for n in snapshot.table_names("fnv1a_soundbanks_aliases")}
known |= {n.strip().lower().replace("\\", "/") for n in snapshot.confirmed_names("sound_alias")}
seen = set()
for name in known:
    if "_" not in name or name.endswith("_"):
        continue
    head, token = name.rsplit("_", 1)
    candidate = name + "_" + token
    if candidate not in known:
        seen.add(candidate)
print(f"{len(known)} known sound aliases; {len(seen)} final-token duplications", file=sys.stderr)
for candidate in sorted(seen):
    print(candidate)
