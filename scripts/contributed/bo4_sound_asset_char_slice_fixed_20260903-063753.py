"""Unfolded BO4 SAB sound interior-character variants from real table seeds."""
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

    snap_path = next(p for p in snapshot.snapshots() if "blkops04" in os.path.basename(p).lower())
    snap = snapshot.read(snap_path)
    wanted = {aid for aid, pool in snap.records if snap.pool_name(pool) == "sound_asset"}
    names = set()
    for table in ("fnv1a_xsounds", "fnv1a_english_xsounds"):
        for raw in snapshot.table_names(table):
            name = raw.strip().lower().replace("/", "\\")
            if name and snapshot.fnv1a_nofold(name) & snapshot.ID_MASK in wanted:
                names.add(name)
    names.update(snapshot.confirmed_names("sound_asset"))

    seeds = sorted(names)[args.offset:args.offset + args.limit]
    alphabet = "_0123456789abcdefghijklmnopqrstuvwxyz"
    emitted = 0
    for name in seeds:
        cut = name.rfind("\\") + 1
        head, base = name[:cut], name[cut:]
        dot = base.find(".")
        if dot <= 0:
            continue
        core, tail = base[:dot], base[dot:]
        for pos, old in enumerate(core[:-4]):
            for char in alphabet:
                if char != old:
                    print(head + core[:pos] + char + core[pos + 1:] + tail)
                    emitted += 1
    print(f"BO4 fixed unfolded sound character slice: {len(seeds)} seeds, {emitted} candidates", file=sys.stderr)


if __name__ == "__main__":
    main()
