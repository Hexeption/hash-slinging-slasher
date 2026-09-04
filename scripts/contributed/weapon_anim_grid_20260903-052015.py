"""Weapon Animation Systematic Grid Generator.

Systematically mines all known weapon archetypes and animation actions across:
- Prefixes: pt_, vm_, pb_
- Weapon stems: ar_, smg_, tr_, lmg_, sniper_, shotgun_, pistol_, launcher_, melee_
- Generational tags: t8, t9, bare
- Stances: stand, crouch, prone, sprint, slide, walk
- Genders: male, fem, bare
- Actions: inspect, reload, reload_empty, reload_quick, reload_partial, firstraise, rechamber, fire, ads
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

WEAPON_CLASSES = [
    "ar_accurate", "ar_damage", "ar_fastfire", "ar_galil", "ar_lever_action",
    "ar_mg1909", "ar_modular", "ar_peacekeeper", "ar_season6", "ar_slowfire",
    "ar_slowhandling", "ar_standard", "ar_stealth",
    "smg_accurate", "smg_capacity", "smg_cqb", "smg_fastfire", "smg_folding",
    "smg_handling", "smg_heavy", "smg_pump", "smg_season6", "smg_semiauto",
    "smg_standard", "smg_thompson",
    "tr_accurate", "tr_damage", "tr_fastburst", "tr_flechette", "tr_longburst",
    "tr_midburst", "tr_powersemi", "tr_precision",
    "lmg_accurate", "lmg_fastfire", "lmg_heavy", "lmg_light", "lmg_slowfire",
    "lmg_standard",
    "sniper_fastfire", "sniper_heavy", "sniper_powerbolt", "sniper_powersemi",
    "sniper_quickscope", "sniper_standard",
    "shotgun_break", "shotgun_fullauto", "shotgun_leveraction", "shotgun_pump",
    "shotgun_semiauto", "shotgun_standard",
    "pistol_burst", "pistol_fullauto", "pistol_revolver", "pistol_semiauto",
    "pistol_shotgun", "pistol_standard",
    "launcher_standard", "launcher_radial", "launcher_freefire",
    "knife_combat", "crossbow"
]

STANCES = ["stand", "crouch", "prone"]
GENDERS = ["male", "fem"]
ACTIONS = [
    "inspect", "reload", "reload_empty", "reload_quick", "reload_partial",
    "firstraise", "rechamber", "putaway", "pullout", "fire", "drop"
]

def main():
    known = set()
    for name in snapshot.table_names("fnv1a_xanims"):
        known.add(name.strip().lower().replace("\\", "/"))
    for name in snapshot.confirmed_names("xanim"):
        known.add(name.strip().lower().replace("\\", "/"))

    candidates = set()

    for w in WEAPON_CLASSES:
        w_type = w.split("_")[0]
        w_name = w[len(w_type)+1:]

        # Patterns observed in pt_ and vm_:
        # 1. pt_<w_type>_t8_<w_name>_<stance>_<action>
        # 2. pt_<w_type>_<w_name>_t9_<gender>_<stance>_<action>
        # 3. pt_<w_type>_t9_<w_name>_<stance>_<action>
        # 4. pt_<w_type>_<w_name>_t8_<stance>_<action>
        # 5. pt_<w_type>_<w_name>_<stance>_<action>
        # 6. vm_<w>_t8_<action>
        # 7. vm_<w>_t9_<action>
        # 8. vm_<w>_<action>

        for stance in STANCES:
            for action in ACTIONS:
                # BO4 pt style
                candidates.add(f"pt_{w_type}_t8_{w_name}_{stance}_{action}")
                candidates.add(f"pt_{w_type}_{w_name}_t8_{stance}_{action}")
                candidates.add(f"pt_{w_type}_{w_name}_{stance}_{action}")
                candidates.add(f"pt_rifle_t8_{w}_{stance}_{action}")

                # Cold War gendered pt style
                for g in GENDERS:
                    candidates.add(f"pt_{w}_t9_{g}_{stance}_{action}")
                    candidates.add(f"pt_{w_type}_{w_name}_t9_{g}_{stance}_{action}")
                    candidates.add(f"pt_{w_type}_t9_{w_name}_{g}_{stance}_{action}")
                    candidates.add(f"pt_{w}_{g}_{stance}_{action}")

        # Viewmodel style
        for action in ACTIONS:
            candidates.add(f"vm_{w}_t8_{action}")
            candidates.add(f"vm_{w}_t9_{action}")
            candidates.add(f"vm_{w}_{action}")
            candidates.add(f"vm_{w_type}_t8_{w_name}_{action}")
            candidates.add(f"vm_{w_type}_t9_{w_name}_{action}")
            candidates.add(f"vm_{w_type}_{w_name}_{action}")

    unseen = [c for c in sorted(candidates) if c not in known]
    sys.stderr.write(f"Generated {len(unseen)} unseen weapon animation candidates.\n")
    for cand in unseen:
        sys.stdout.write(cand + "\n")

if __name__ == "__main__":
    main()
