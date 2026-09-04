"""Probe missing role-axis cells in the observed ``fly_`` animation family.

    python contrib/fly_role_grid_current.py

Reads published and confirmed names, writes no files, and prints extensionless ``fly_``
animation candidates formed by replacing an observed terminal actor-role suffix with
another observed role suffix. This is a reusable family-specific grid probe.
"""
import os
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))
while ROOT != os.path.dirname(ROOT) and not os.path.isfile(os.path.join(ROOT, "scripts", "snapshot.py")):
    ROOT = os.path.dirname(ROOT)
sys.path.insert(0, os.path.join(ROOT, "scripts"))
import snapshot

TABLES = ("fnv1a_soundbanks_aliases", "fnv1a_soundbanks_aliases_v2")
ROLES = ("npc", "plr", "hv", "lt_npc", "lt_plr", "npc_hv",
         "igc_lt_plr", "medium_lt_plr", "rapid_lt_plr", "soft_lt_plr", "soft_lt_npc")


def main():
    known = {n.strip().lower().replace("\\", "/") for n in snapshot.table_names(*TABLES)}
    known.update(n.strip().lower().replace("\\", "/") for n in snapshot.confirmed_names("sound_alias"))
    candidates = set()
    bases = set()
    for name in known:
        if not name.startswith("fly_"):
            continue
        for role in ROLES:
            marker = "_" + role
            if name.endswith(marker) and len(name) > len(marker) + 4:
                bases.add(name[:-len(marker)])
                break
    for base in bases:
        for role in ROLES:
            candidate = base + "_" + role
            if candidate not in known:
                candidates.add(candidate)
    for candidate in sorted(candidates):
        print(candidate)
    print(f"fly role grid: {len(bases):,} bases x {len(ROLES)} roles -> {len(candidates):,} unseen cells", file=sys.stderr)


if __name__ == "__main__":
    main()
