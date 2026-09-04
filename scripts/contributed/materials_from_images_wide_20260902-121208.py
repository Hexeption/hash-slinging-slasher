"""Every material an image implies, through all 13 observed material directories (including mcdp/).

    python contrib/materials_from_images_wide.py | bin/windows/confirm_list.exe - \
        --label "wide materials from images" --script contrib/materials_from_images_wide.py
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

DIRECTORIES = [
    "mc/", "wc/", "clt/", "splm/", "vd/", "mcs/", "ei/", "cltp/", "vdd/", "el/",
    "mcp/", "ec/", "mcdp/"
]

IMAGE_CHANNELS = {
    "c", "n", "g", "o", "m", "s", "r", "e", "col", "nml", "icon", "large",
    "spc", "gls", "ao", "d", "h", "a", "mask", "small", "thermalmap", "cm",
    "v2", "normal", "depth", "albedo", "specular", "cos", "geo", "render",
    "xl", "sm", "swatch", "dmg"
}

IMAGE_PREFIXES = [
    "i_c_", "i_t8_", "i_t9_", "i_p8_", "i_p9_", "i_vm_", "i_wpn_", "i_weap_",
    "i_mtl_", "i_", "ui_", "uie_"
]


def core(name):
    """An image name reduced to its shared core."""
    name = name.strip().lower().replace("\\", "/")
    # Remove directory if present
    if "/" in name:
        name = name.split("/", 1)[1]
    for p in IMAGE_PREFIXES:
        if name.startswith(p):
            name = name[len(p):]
            break
    head, _, tail = name.rpartition("_")
    if head and (tail in IMAGE_CHANNELS or tail.isdigit() or len(tail) <= 2):
        name = head
    return name.strip()


def main():
    confirmed_images = snapshot.confirmed_names("image")
    published_images = snapshot.table_names("fnv1a_ximages")
    
    known = {n.strip().lower().replace("\\", "/") for n in snapshot.table_names("fnv1a_xmaterials", "fnv1a_xmaterials_v2")}
    known |= {n.strip().lower().replace("\\", "/") for n in snapshot.confirmed_names("material")}
    
    cores = set()
    for name in list(confirmed_images) + list(published_images):
        c = core(name)
        if len(c) >= 3:
            cores.add(c)
            
    seen = set()
    for c in sorted(cores):
        for d in DIRECTORIES:
            for mtl in ("mtl_", ""):
                cand = d + mtl + c
                if cand not in known and cand not in seen:
                    seen.add(cand)
                    print(cand)


if __name__ == "__main__":
    main()
