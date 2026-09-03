"""Bounded one-character insertions in known sound basenames."""
import argparse
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.join(ROOT, "scripts"))
import snapshot


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--offset", type=int, default=0)
    parser.add_argument("--limit", type=int, default=2000)
    args = parser.parse_args()
    tables = ("fnv1a_xsounds", "fnv1a_english_xsounds", "fnv1a_soundbanks_aliases")
    names = {n.strip().lower() for n in snapshot.table_names(*tables) if n.strip()}
    names.update(n.strip().lower() for n in snapshot.confirmed_names("sound_asset") if n.strip())
    seeds = sorted(names)[args.offset:args.offset + args.limit]
    alphabet = "0123456789_abcdefghijklmnopqrstuvwxyz"
    count = 0
    for name in seeds:
        cut = max(name.rfind("/"), name.rfind("\\")) + 1
        head, base = name[:cut], name[cut:]
        dot = base.find(".")
        if dot <= 0:
            continue
        core, tail = base[:dot], base[dot:]
        for pos in range(len(core) + 1):
            for char in alphabet:
                if core[pos:pos + 1] == char:
                    continue
                print(head + core[:pos] + char + core[pos:] + tail)
                count += 1
    print(f"{len(seeds):,} seeds, {count:,} candidates", file=sys.stderr)


if __name__ == "__main__":
    main()
