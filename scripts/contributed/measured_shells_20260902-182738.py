"""A known name's MIDDLE, wearing a different name's opening and a different name's ending.

    python contrib/measured_shells.py --head 6 --tail 6 --top 1200
    bin/windows/confirm_plan.exe plans/shell_h6t6.txt --size
    bin/windows/confirm_plan.exe plans/shell_h6t6.txt
"""

import argparse
import os
import sys
from collections import Counter

_root = os.path.dirname(os.path.abspath(__file__))
while _root != os.path.dirname(_root) and not os.path.isfile(
    os.path.join(_root, "scripts", "snapshot.py")
):
    _root = os.path.dirname(_root)
sys.path.insert(0, os.path.join(_root, "scripts"))

import snapshot

REPO = _root
PUBLISHED = ["fnv1a_xmaterials", "fnv1a_ximages", "fnv1a_xmodels", "fnv1a_xanims"]
GENERAL = ("image", "material", "xmodel", "xanim")


def load():
    names = set()
    for fn in PUBLISHED:
        for name in snapshot.table_names(fn):
            name = name.strip().lower().replace("\\", "/")
            if name:
                names.add(name)
    for g in GENERAL:
        for name in snapshot.confirmed_names(g):
            name = name.strip().lower().replace("\\", "/")
            if name:
                names.add(name)
    return names


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--head", type=int, default=6, help="characters replaced at the front")
    ap.add_argument("--tail", type=int, default=6, help="characters replaced at the end")
    ap.add_argument("--top", type=int, default=1200,
                    help="keep the N commonest openings and the N commonest endings")
    ap.add_argument("--out", default=None)
    args = ap.parse_args()
    h, t = args.head, args.tail

    names = [n for n in load() if len(n) > h + t + 4]
    sys.stderr.write("names usable at head=%d tail=%d: %d\n" % (h, t, len(names)))

    openings, endings, middles = Counter(), Counter(), set()
    for n in names:
        openings[n[:h]] += 1
        endings[n[-t:]] += 1
        middles.add(n[h:-t])

    begins = [o for o, _ in openings.most_common(args.top)]
    ends = [e for e, _ in endings.most_common(args.top)]
    middles = sorted(middles)

    out = args.out or os.path.join(REPO, "plans", "shell_h%dt%d" % (h, t))

    def write(path, rows):
        with open(path, "w", encoding="utf-8", newline="\n") as fh:
            for r in rows:
                fh.write(r + "\n")

    write(out + ".begins.txt", begins)
    write(out + ".mids.txt", middles)
    write(out + ".ends.txt", ends)
    rel = os.path.basename(out)
    with open(out + ".txt", "w", encoding="utf-8", newline="\n") as fh:
        fh.write("# Written by contrib/measured_shells.py --head %d --tail %d --top %d\n#\n"
                 % (h, t, args.top))
        fh.write("# Every known name with %d characters cut off the front and %d off the end,\n"
                 % (h, t))
        fh.write("# wearing every opening and every ending the corpus is observed to use at\n")
        fh.write("# those lengths -- the two measured-offset methods applied at once.\n\n")
        fh.write("label: measured shells, head %d tail %d, top %d\n" % (h, t, args.top))
        fh.write("begin: @plans/%s.begins.txt\n" % rel)
        fh.write("stem:  @plans/%s.mids.txt\n" % rel)
        fh.write("end:   @plans/%s.ends.txt\n" % rel)

    total = len(begins) * len(middles) * len(ends)
    print("head=%d tail=%d top=%d: %s openings x %s middles x %s endings = %s candidates"
          % (h, t, args.top, "{:,}".format(len(begins)), "{:,}".format(len(middles)),
             "{:,}".format(len(ends)), "{:,}".format(total)))
    print("      full vocabulary would be %s x %s -- capped %.0fx"
          % ("{:,}".format(len(openings)), "{:,}".format(len(endings)),
             (len(openings) * len(endings)) / float(max(1, len(begins) * len(ends)))))
    print("wrote %s.txt" % out)


if __name__ == "__main__":
    main()
