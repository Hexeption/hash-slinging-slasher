"""Cross-Generation Animation Tag Swapper: t8 (BO4) <-> t9 (Cold War).

Treyarch's viewmodel and gameplay animations frequently share common animation rig identifiers,
differing only by their game generation tag (_t8_ vs _t9_) or the presence/absence of the tag.

This generator mines all confirmed and published xanims and generates:
1. t9 -> t8 substitutions
2. t8 -> t9 substitutions
3. t8 -> bare (untagged) substitutions
4. t9 -> bare (untagged) substitutions
5. bare -> t8 / t9 insertions where applicable
"""

import os
import sys

_root = os.path.dirname(os.path.abspath(__file__))
while _root != os.path.dirname(_root) and not os.path.isfile(
    os.path.join(_root, "scripts", "snapshot.py")
):
    _root = os.path.dirname(_root)
sys.path.insert(0, os.path.join(_root, "scripts"))

import snapshot

def main():
    known = set()
    for name in snapshot.table_names("fnv1a_xanims"):
        known.add(name.strip().lower().replace("\\", "/"))
    for name in snapshot.confirmed_names("xanim"):
        known.add(name.strip().lower().replace("\\", "/"))

    sys.stderr.write(f"Loaded {len(known)} known animation names.\n")

    candidates = set()

    for name in known:
        # 1. t9 -> t8 and t8 -> t9
        if "_t9_" in name:
            c8 = name.replace("_t9_", "_t8_")
            if c8 not in known:
                candidates.add(c8)
            cbare = name.replace("_t9_", "_")
            if cbare not in known:
                candidates.add(cbare)

        if "_t8_" in name:
            c9 = name.replace("_t8_", "_t9_")
            if c9 not in known:
                candidates.add(c9)
            cbare = name.replace("_t8_", "_")
            if cbare not in known:
                candidates.add(cbare)

        # Endings: _t9 vs _t8
        if name.endswith("_t9"):
            c8 = name[:-3] + "_t8"
            if c8 not in known:
                candidates.add(c8)
            cbare = name[:-3]
            if cbare not in known:
                candidates.add(cbare)

        if name.endswith("_t8"):
            c9 = name[:-3] + "_t9"
            if c9 not in known:
                candidates.add(c9)
            cbare = name[:-3]
            if cbare not in known:
                candidates.add(cbare)

        # Beginnings: t9_ vs t8_
        if name.startswith("t9_"):
            c8 = "t8_" + name[3:]
            if c8 not in known:
                candidates.add(c8)
        if name.startswith("t8_"):
            c9 = "t9_" + name[3:]
            if c9 not in known:
                candidates.add(c9)

    sys.stderr.write(f"Generated {len(candidates)} cross-generation animation candidates.\n")
    for cand in sorted(candidates):
        sys.stdout.write(cand + "\n")

if __name__ == "__main__":
    main()
