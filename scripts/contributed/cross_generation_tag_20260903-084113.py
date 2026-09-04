"""Cross-generation engine tag transposition.

Treyarch games (Black Ops 3: t7, Black Ops 4: t8, Cold War: t9) reuse engine
assets, weapons, rigs, attachments, props, and materials across generations,
updating only the generational identifier token (e.g., _t8_ <-> _t9_, _p8_ <-> _p9_).

This generator systematically transposes these generational tokens across all
known assets from both games to discover legacy and forward-ported assets.
"""
import os
import re
import sys

_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(_root, "scripts"))
import snapshot

TRANSFORMS = [
    # T8 <-> T9 (Black Ops 4 <-> Cold War)
    (re.compile(r"(^|[/_])t8([/_])"), r"\g<1>t9\g<2>"),
    (re.compile(r"(^|[/_])t9([/_])"), r"\g<1>t8\g<2>"),
    # P8 <-> P9 (Player/Prop tags)
    (re.compile(r"(^|[/_])p8([/_])"), r"\g<1>p9\g<2>"),
    (re.compile(r"(^|[/_])p9([/_])"), r"\g<1>p8\g<2>"),
    # T7 -> T8 (BO3 -> BO4) and T7 -> T9 (BO3 -> Cold War)
    (re.compile(r"(^|[/_])t7([/_])"), r"\g<1>t8\g<2>"),
    (re.compile(r"(^|[/_])t7([/_])"), r"\g<1>t9\g<2>"),
]

def main():
    known = set()
    for table in ["fnv1a_xmodels", "fnv1a_xmaterials", "fnv1a_ximages", "fnv1a_xanims"]:
        known.update(snapshot.table_names(table))
    for pool in ["xmodel", "material", "image", "xanim"]:
        known.update(snapshot.confirmed_names(pool))

    candidates = set()
    for name in known:
        name = name.strip().lower().replace("\\", "/")
        for pattern, replacement in TRANSFORMS:
            if pattern.search(name):
                new_name = pattern.sub(replacement, name)
                if new_name != name and new_name not in known:
                    candidates.add(new_name)

    for cand in sorted(candidates):
        sys.stdout.write(cand + "\n")

    sys.stderr.write(
        f"Generated {len(candidates):,} cross-generation tag candidates from {len(known):,} seeds.\n"
    )

if __name__ == "__main__":
    main()
