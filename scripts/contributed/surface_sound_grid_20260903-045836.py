"""Surface Sound Grid: Systematic generator for sound aliases on physical surfaces.

In Call of Duty (Black Ops 4 and Cold War), all sound events that interact with terrain
(foley footsteps fly_, bullet/projectile impacts prj_, zombie sounds zmb_, vehicle tire
surfaces veh_, weapon drops wpn_, and multiplayer collisions mpl_) are assigned across
the engine's 38 surface types.

This generator mines all sound action cores observed with at least one surface type,
and fills the unobserved holes across all 38 physical surfaces.
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

SURFACES = [
    "asphalt", "bark", "bodyarmor", "brick", "carpet", "ceramic", "cloth",
    "concrete", "cushion", "default", "dirt", "flesh", "foliage", "fruit",
    "glass", "glassbulletproof", "glasscar", "grass", "gravel", "ice",
    "metal", "metalcar", "metalcatwalk", "metalhollow", "metalthin", "mud",
    "paintedmetal", "paper", "plaster", "plastic", "rock", "rubber", "sand",
    "snow", "tallgrass", "water", "watershallow", "wood"
]

PREFIXES = ("fly_", "zmb_", "prj_", "veh_", "wpn_", "mpl_", "phy_", "amb_", "evt_")

def main():
    sys.stderr.write("Loading sound aliases and confirmed names...\n")
    known = set()
    for name in snapshot.table_names("fnv1a_soundbanks_aliases", "fnv1a_soundbanks_aliases_v2"):
        known.add(name.strip().lower().replace("\\", "/"))
    for name in snapshot.confirmed_names("sound_alias"):
        known.add(name.strip().lower().replace("\\", "/"))
    for name in snapshot.confirmed_names():
        n = name.strip().lower().replace("\\", "/")
        if any(n.startswith(p) for p in PREFIXES):
            known.add(n)

    surface_set = set(SURFACES)
    cores = set()

    for name in known:
        if "/" in name:
            continue
        parts = name.rsplit("_", 1)
        if len(parts) == 2 and parts[1] in surface_set:
            cores.add(parts[0])

    sys.stderr.write(f"Identified {len(cores)} distinct sound action cores across {len(SURFACES)} surfaces.\n")

    emitted = 0
    for core in sorted(cores):
        for surface in SURFACES:
            candidate = f"{core}_{surface}"
            if candidate not in known:
                sys.stdout.write(candidate + "\n")
                emitted += 1

    sys.stderr.write(f"Generated {emitted} candidates for unobserved surface grid cells.\n")

if __name__ == "__main__":
    main()
