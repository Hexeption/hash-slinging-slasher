"""Recovers missing xmodel assets by pairing sibling states (view/world, lods, damage).

Call of Duty weapons, attachments, and props follow strict pairing conventions:
- Every _view model has a _world counterpart (and vice-versa)
- LOD models (_lod1 through _lod5)
- Scale variants (_lrg, _med, _sml)
- State variants (_dmg, _full, _clean)
"""

import sys
import os

_root = os.path.dirname(os.path.abspath(__file__))
while _root != os.path.dirname(_root) and not os.path.isfile(
    os.path.join(_root, "scripts", "snapshot.py")
):
    _root = os.path.dirname(_root)
sys.path.insert(0, os.path.join(_root, "scripts"))

import snapshot

LODS = ["_lod1", "_lod2", "_lod3", "_lod4", "_lod5"]
SCALES = ["_lrg", "_med", "_sml"]
STATES = ["_dmg", "_full", "_clean"]

def generate_variants(name):
    variants = set()
    
    # 1. view <-> world
    if name.endswith("_view"):
        variants.add(name[:-5] + "_world")
    elif name.endswith("_world"):
        variants.add(name[:-6] + "_view")
        
    if "_view_" in name:
        variants.add(name.replace("_view_", "_world_"))
    elif "_world_" in name:
        variants.add(name.replace("_world_", "_view_"))
        
    # 2. LOD variants
    for i, lod in enumerate(LODS):
        if lod in name:
            for other_lod in LODS:
                if other_lod != lod:
                    variants.add(name.replace(lod, other_lod))
            break
            
    # 3. Scale variants
    for scale in SCALES:
        if scale in name:
            for other_scale in SCALES:
                if other_scale != scale:
                    variants.add(name.replace(scale, other_scale))
            break
            
    # 4. State variants
    for st in STATES:
        if st in name:
            for other_st in STATES:
                if other_st != st:
                    variants.add(name.replace(st, other_st))
            break

    return variants

def main():
    known_models = set(snapshot.table_names("fnv1a_xmodels"))
    known_models |= set(snapshot.confirmed_names("xmodel"))
    
    candidates = set()
    for name in known_models:
        name = name.strip().lower()
        for v in generate_variants(name):
            if v not in known_models:
                candidates.add(v)
                
    for c in sorted(candidates):
        print(c)
        
    sys.stderr.write(f"Generated {len(candidates):,} candidate xmodels.\n")

if __name__ == "__main__":
    main()
