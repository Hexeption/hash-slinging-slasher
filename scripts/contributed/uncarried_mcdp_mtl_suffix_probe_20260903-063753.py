"""Probe the high-volume uncarried mcdp/mtl_ head with observed stem/end seams."""
import argparse
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.join(ROOT, "scripts"))
import snapshot


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--limit", type=int, default=1000)
    parser.add_argument("--head", default="mcdp/mtl_")
    args = parser.parse_args()
    head = args.head.lower()
    tables = ("fnv1a_xmodel", "fnv1a_material", "fnv1a_image", "fnv1a_xanim")
    names = set()
    for table in tables:
        for raw in snapshot.table_names(table):
            name = raw.strip().lower()
            if name.startswith(head):
                names.add(name)
    for pool in ("xmodel", "material", "image", "xanim"):
        for raw in snapshot.confirmed_names(pool):
            name = raw.strip().lower()
            if name.startswith(head):
                names.add(name)
    endings = [line.strip().lower() for line in open(os.path.join(ROOT, "data", "suffixes.txt"), encoding="utf-8", errors="replace") if line.strip()]
    stems = set()
    for name in sorted(names)[:args.limit]:
        rest = name[len(head):]
        pieces = rest.split("_")
        for cut in range(1, len(pieces)):
            stem = "_".join(pieces[:-cut])
            if len(stem) >= 2:
                stems.add(stem)
    candidates = {head + stem + ending for stem in stems for ending in endings}
    print(f"{len(names):,} seeds, {len(stems):,} stems, {len(candidates):,} candidates", file=sys.stderr)
    for candidate in sorted(candidates):
        print(candidate)


if __name__ == "__main__":
    main()
