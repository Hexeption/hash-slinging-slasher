"""Unified family shared tail grid generator across all 22 measured asset families.

Combines and fixes the 22 orphaned shared-tail scripts (p8, p9, ui, uie, vm, wpn,
weap, callingcards, emblems, zmb, att, amb, evt, fly, mus, sat, mpl, etc.),
filling unobserved cells where an axis and a tail are each known in the family.
"""

import collections
import os
import sys

_root = os.path.dirname(os.path.abspath(__file__))
while _root != os.path.dirname(_root) and not os.path.isfile(
    os.path.join(_root, "scripts", "snapshot.py")
):
    _root = os.path.dirname(_root)
sys.path.insert(0, os.path.join(_root, "scripts"))

import snapshot

TABLES = (
    "fnv1a_xmaterials", "fnv1a_xmaterials_v2",
    "fnv1a_ximages", "fnv1a_ximages_v2",
    "fnv1a_xmodels", "fnv1a_xmodels_v2",
    "fnv1a_xanims", "fnv1a_xanims_v2",
    "fnv1a_soundbanks_aliases", "fnv1a_soundbanks_aliases_v2",
    "fnv1a_xsounds", "fnv1a_xsounds_v2",
)

FAMILIES = [
    "p8", "p9", "p7", "ui", "uie", "vm", "wpn", "weap", "callingcards",
    "emblems", "zmb", "att", "amb", "evt", "fly", "mus", "sat", "mpl",
    "icon", "jup", "pt", "i"
]

def main():
    target_families = sys.argv[1:] if len(sys.argv) > 1 else FAMILIES
    
    sys.stderr.write("Loading known names...\n")
    have = {n.strip().lower().replace("\\", "/") for n in snapshot.table_names(*TABLES)}
    have |= {n.strip().lower().replace("\\", "/") for n in snapshot.confirmed_names()}
    
    total_candidates = 0
    
    for family in target_families:
        observed = []
        prefix = family + "_"
        for name in have:
            if not name.startswith(prefix) or "/" in name or "." in name:
                continue
            parts = name.split("_", 2)
            if len(parts) >= 3:
                axis, tail = parts[1], parts[2]
                if axis and tail:
                    observed.append((axis, tail))
                    
        if not observed:
            continue
            
        axes = {axis for axis, _ in observed}
        counts = collections.Counter(tail for _, tail in observed)
        tails = {tail for tail, count in counts.items() if count > 1}
        
        candidates = sorted({f"{family}_{axis}_{tail}" for axis in axes for tail in tails} - have)
        sys.stderr.write(f"[{family}] {len(axes):,} axes x {len(tails):,} tails = {len(candidates):,} candidates\n")
        
        for cand in candidates:
            print(cand)
        total_candidates += len(candidates)
        
    sys.stderr.write(f"Total candidates across {len(target_families)} families: {total_candidates:,}\n")

if __name__ == "__main__":
    main()
