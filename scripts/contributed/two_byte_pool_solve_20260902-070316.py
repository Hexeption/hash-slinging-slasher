"""Solve final-two-byte variants independently for model, material, image, and anim pools."""
import argparse
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "scripts"))
import snapshot

MASK = (1 << 64) - 1
TOP = 1 << 63
PRIME = 0x100000001B3
INVERSE = pow(PRIME, -1, 1 << 64)
PRINTABLE = range(0x20, 0x7F)
TABLES = {
    "xmodel": "fnv1a_xmodels",
    "material": "fnv1a_xmaterials",
    "image": "fnv1a_ximages",
    "xanim": "fnv1a_xanims",
}


def main(argv):
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--game", required=True, choices=("BLKOPS04", "BLKOPSCW"))
    options = parser.parse_args(argv)
    shot = next(snapshot.read(path) for path in snapshot.snapshots()
                if snapshot.read(path).game.lower() == options.game.lower())
    known = snapshot.known_hashes()
    found = set()
    measurements = []

    for kind, table in TABLES.items():
        seeds = set(snapshot.table_names(table))
        seeds.update(snapshot.confirmed_names(kind))
        prefixes = {}
        for seed in seeds:
            seed = seed.strip().lower()
            if len(seed) < 3:
                continue
            prefix = seed[:-2]
            value = snapshot.fnv1a(prefix)
            prefixes.setdefault(value >> 8, []).append((value & 0xFF, prefix))

        targets = [asset_id for asset_id, pool in shot.unnamed(known).items() if pool == kind]
        targets += [asset_id | TOP for asset_id in targets]
        before = len(found)
        for target in targets:
            scaled = (target * INVERSE) & MASK
            for last in PRINTABLE:
                value = ((scaled ^ last) * INVERSE) & MASK
                for low, prefix in prefixes.get(value >> 8, ()):
                    first = low ^ (value & 0xFF)
                    if first not in PRINTABLE:
                        continue
                    candidate = prefix + chr(first) + chr(last)
                    if snapshot.fnv1a(candidate) == target:
                        found.add(candidate)
        measurements.append(f"{kind}:{len(seeds)}/{len(targets)//2}/{len(found)-before}")

    print(f"game {options.game}: " + ", ".join(measurements) +
          f"; {len(found):,} exact candidates", file=sys.stderr)
    for candidate in sorted(found):
        print(candidate)


if __name__ == "__main__":
    main(sys.argv[1:])
