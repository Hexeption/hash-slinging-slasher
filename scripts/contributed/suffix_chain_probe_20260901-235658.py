"""Compose two common observed suffixes after a known name base."""
import collections
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.join(ROOT, "scripts"))
import snapshot


def main():
    tables = (
        "fnv1a_xmodels",
        "fnv1a_xmaterials",
        "fnv1a_ximages",
        "fnv1a_xanims",
        "fnv1a_soundbanks_aliases",
    )
    known = {
        n.strip().lower().replace("\\", "/")
        for table in tables
        for n in snapshot.table_names(table)
        if n.strip()
    }
    known.update(
        n.strip().lower().replace("\\", "/")
        for n in snapshot.confirmed_names()
        if n.strip()
    )
    with open(os.path.join(ROOT, "data", "suffixes.txt"), encoding="utf-8") as handle:
        endings = [line.strip().lower() for line in handle if line.strip()]
    endings = endings[:20]
    bases = set()
    for name in known:
        for ending in endings:
            if name.endswith(ending) and len(name) > len(ending):
                bases.add(name[: -len(ending)])
    candidates = {
        base + first + second
        for base in bases
        for first in endings
        for second in endings
        if base + first + second not in known
    }
    print(
        f"{len(known):,} known names, {len(bases):,} bases, "
        f"{len(endings):,} endings, {len(candidates):,} candidates",
        file=sys.stderr,
    )
    for candidate in sorted(candidates):
        print(candidate)


if __name__ == "__main__":
    main()
