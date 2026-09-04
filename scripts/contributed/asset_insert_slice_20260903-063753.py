"""Bounded one-character insertion variants in known non-sound asset basenames."""
import argparse
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.join(ROOT, "scripts"))
import snapshot

TABLES = {"model": ("fnv1a_xmodels", "xmodel"), "material": ("fnv1a_xmaterials", "material"),
          "image": ("fnv1a_ximages", "image"), "anim": ("fnv1a_xanims", "xanim")}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--type", choices=sorted(TABLES), default="image")
    parser.add_argument("--offset", type=int, default=0)
    parser.add_argument("--limit", type=int, default=2000)
    args = parser.parse_args()
    table, pool = TABLES[args.type]
    names = {n.strip().lower().replace("\\", "/") for n in snapshot.table_names(table) if n.strip()}
    names.update(n.strip().lower().replace("\\", "/") for n in snapshot.confirmed_names(pool) if n.strip())
    seeds = sorted(names)[args.offset:args.offset + args.limit]
    alphabet = "0123456789_abcdefghijklmnopqrstuvwxyz"
    count = 0
    for name in seeds:
        cut = name.rfind("/") + 1
        head, base = name[:cut], name[cut:]
        if not base or "." in base:
            continue
        for pos in range(len(base) + 1):
            for char in alphabet:
                if base[pos:pos + 1] == char:
                    continue
                print(head + base[:pos] + char + base[pos:])
                count += 1
    print(f"{args.type}: {len(seeds):,} seeds, {count:,} candidates", file=sys.stderr)


if __name__ == "__main__":
    main()
