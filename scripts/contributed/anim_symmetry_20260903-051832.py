"""Animation Symmetry Generator: Stance, Gender, and Hand Pose Grid Completion.

In Call of Duty (Black Ops 4 and Cold War), animations are authored across systematic
engine dimensions:
1. Stances: stand <-> crouch <-> prone
2. Rig Genders: male <-> fem
3. Hand Poses: hand_pose_r <-> hand_pose_l

This generator finds all unobserved animation grid cells where at least one sister
variant is already known to be real.
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

STANCES = ["stand", "crouch", "prone"]

def main():
    known = set()
    for name in snapshot.table_names("fnv1a_xanims"):
        known.add(name.strip().lower().replace("\\", "/"))
    for name in snapshot.confirmed_names("xanim"):
        known.add(name.strip().lower().replace("\\", "/"))

    sys.stderr.write(f"Loaded {len(known)} known animation names.\n")

    candidates = set()

    for name in known:
        # 1. Stance symmetries: stand <-> crouch <-> prone
        for s in STANCES:
            token = f"_{s}_"
            if token in name:
                for target in STANCES:
                    if target != s:
                        cand = name.replace(token, f"_{target}_")
                        if cand not in known:
                            candidates.add(cand)

        # 2. Gender symmetries: male <-> fem
        if "_male_" in name:
            cand = name.replace("_male_", "_fem_")
            if cand not in known:
                candidates.add(cand)
        if "_fem_" in name:
            cand = name.replace("_fem_", "_male_")
            if cand not in known:
                candidates.add(cand)

        # 3. Hand poses: hand_pose_r <-> hand_pose_l
        if "_hand_pose_r" in name:
            cand = name.replace("_hand_pose_r", "_hand_pose_l")
            if cand not in known:
                candidates.add(cand)
        if "_hand_pose_l" in name:
            cand = name.replace("_hand_pose_l", "_hand_pose_r")
            if cand not in known:
                candidates.add(cand)

    sys.stderr.write(f"Generated {len(candidates)} animation symmetry candidates.\n")
    for cand in sorted(candidates):
        sys.stdout.write(cand + "\n")

if __name__ == "__main__":
    main()
