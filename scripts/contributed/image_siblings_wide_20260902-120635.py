"""Every image a confirmed material implies, using measured image prefixes and suffixes.

    python contrib/image_siblings_wide.py | bin/windows/confirm_list.exe - \
        --label "wide image siblings of confirmed materials" --script contrib/image_siblings_wide.py
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

# Top image suffixes measured across fnv1a_ximages + confirmed image corpus
SUFFIXES = [
    "", "_c", "_n", "_g", "_o", "_m", "_s", "_r", "_e", "_col", "_nml",
    "_icon", "_large", "_spc", "_gls", "_ao", "_d", "_h", "_a", "_mask",
    "_small", "_thermalmap", "_cm", "_v2", "_normal", "_depth", "_albedo",
    "_specular", "_cos", "_geo", "_render", "_xl", "_sm", "_swatch", "_dmg"
]

# Top image prefixes measured across fnv1a_ximages
PREFIXES = [
    "i_", "", "mtl_", "i_c_", "i_t8_", "i_t9_", "i_mtl_", "ui_", "uie_",
    "i_p8_", "i_p9_", "i_vm_", "i_wpn_", "i_weap_"
]

STRIP = ["mtl_", "i_", "i_c_", "i_t8_", "i_t9_", "i_mtl_"]


def core(name):
    """A material name reduced to the part an image would share with it."""
    directory, _, rest = name.rpartition("/")
    for lead in STRIP:
        if rest.startswith(lead):
            rest = rest[len(lead):]
            break
    if rest.endswith("_c") or rest.endswith("_n") or rest.endswith("_m") or rest.endswith("_s"):
        rest = rest[:-2]
    return rest.strip()


def main():
    confirmed_materials = snapshot.confirmed_names("material")
    published_materials = snapshot.table_names("fnv1a_xmaterials")
    
    known = {n.strip().lower().replace("\\", "/") for n in snapshot.table_names("fnv1a_ximages", "fnv1a_ximages_v2")}
    known |= {n.strip().lower().replace("\\", "/") for n in snapshot.confirmed_names("image")}
    
    cores = set()
    for name in list(confirmed_materials) + list(published_materials):
        c = core(name)
        if len(c) >= 3:
            cores.add(c)
            
    seen = set()
    for c in sorted(cores):
        for p in PREFIXES:
            for s in SUFFIXES:
                cand = p + c + s
                if cand not in known and cand not in seen:
                    seen.add(cand)
                    print(cand)


if __name__ == "__main__":
    main()
