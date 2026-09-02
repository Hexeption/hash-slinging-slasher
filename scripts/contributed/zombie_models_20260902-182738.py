"""Zombies-flavoured xmodel names, recombined from every zombies name already known to be real.

    python contrib/zombie_models.py | bin/windows/confirm_list.exe - \
        --label "zombie xmodels" --script contrib/zombie_models.py --game BLKOPS04
"""
import os
import re
import sys

_root = os.path.dirname(os.path.abspath(__file__))
while _root != os.path.dirname(_root) and not os.path.isfile(
    os.path.join(_root, "scripts", "snapshot.py")
):
    _root = os.path.dirname(_root)
sys.path.insert(0, os.path.join(_root, "scripts"))

import snapshot

WANTED = re.compile(r"zombie|zmb|_zm_|^zm_|/zm_")

OPENINGS = [
    "", "p9_", "p8_", "p7_", "p6_", "c_", "t9_", "vm_", "wm_", "attach_", "veh_", "ai_",
    "p9_zmb_", "p8_zmb_", "c_zmb_", "zmb_", "zm_", "p9_zombie_", "c_zombie_", "zombie_",
    "clt/", "splm/", "cltp/", "mc/",
]

TAILS = ["", "_lod0", "_lod1", "_lod2", "_lod3", "_body", "_head", "_hat", "_arms", "_legs",
         "_torso", "_hands", "_fx", "_dead", "_gib", "_world", "_view", "_dmg", "_variant"]
for number in range(0, 13):
    TAILS.append("_%02d" % number)
    TAILS.append("_%d" % number)


def measured(name):
    path = os.path.join(_root, "data", name)
    with open(path, encoding="utf-8") as handle:
        return [line.strip() for line in handle if line.strip()]


def corpus():
    for name in snapshot.table_names("fnv1a_xmodels"):
        yield name.strip().lower().replace("\\", "/")
    for name in snapshot.confirmed_names("xmodel"):
        yield name.strip().lower().replace("\\", "/")


def stems_of(name):
    base = name.rpartition("/")[2]
    parts = base.split("_")

    for start in range(len(parts)):
        for end in range(start + 1, len(parts) + 1):
            piece = "_".join(parts[start:end])
            if len(piece) >= 3:
                yield piece


def main():
    seen_stems = set()
    for name in corpus():
        if not WANTED.search(name):
            continue
        for stem in stems_of(name):
            seen_stems.add(stem)

    stems = sorted(stem for stem in seen_stems
                   if WANTED.search(stem) and stem.count("_") <= 3)
    print("zombies stems: %d" % len(stems), file=sys.stderr)

    endings = TAILS + [item for item in measured("suffixes.txt") if item.count("_") == 1][:20]
    endings = list(dict.fromkeys(endings))
    print("endings: %d, openings: %d" % (len(endings), len(OPENINGS)), file=sys.stderr)
    print("candidates: %d" % (len(stems) * len(endings) * len(OPENINGS)), file=sys.stderr)

    out = sys.stdout
    for stem in stems:
        for opening in OPENINGS:
            head = opening + stem
            for ending in endings:
                out.write(head + ending + "\n")


if __name__ == "__main__":
    main()
