"""Solve sound-alias names differing from a known alias in their final three bytes."""
import argparse
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "scripts"))
import snapshot

MASK = (1 << 64) - 1
TOP = 1 << 63
PRIME = 0x100000001B3
INVERSE = pow(PRIME, -1, 1 << 64)
PRINTABLE = tuple(range(0x20, 0x7F))


def main(argv):
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--game", required=True, choices=("BLKOPS04", "BLKOPSCW"))
    options = parser.parse_args(argv)
    shot = next(snapshot.read(path) for path in snapshot.snapshots()
                if snapshot.read(path).game.lower() == options.game.lower())
    seeds = set(snapshot.table_names("fnv1a_soundbanks_aliases"))
    seeds.update(snapshot.confirmed_names("sound_alias"))
    prefixes = {}
    for seed in seeds:
        seed = seed.strip().lower()
        if len(seed) < 4:
            continue
        prefix = seed[:-3]
        value = snapshot.fnv1a(prefix)
        prefixes.setdefault(value >> 8, []).append((value & 0xFF, prefix))

    known = snapshot.known_hashes()
    targets = [asset_id for asset_id, pool in shot.unnamed(known).items()
               if pool == "sound_alias"]
    targets += [asset_id | TOP for asset_id in targets]
    found = set()
    for target in targets:
        first_reverse = (target * INVERSE) & MASK
        for last in PRINTABLE:
            second_reverse = ((first_reverse ^ last) * INVERSE) & MASK
            for middle in PRINTABLE:
                value = ((second_reverse ^ middle) * INVERSE) & MASK
                for low, prefix in prefixes.get(value >> 8, ()):
                    first = low ^ (value & 0xFF)
                    if first not in PRINTABLE:
                        continue
                    candidate = prefix + chr(first) + chr(middle) + chr(last)
                    if snapshot.fnv1a(candidate) == target:
                        found.add(candidate)

    print(f"{len(seeds):,} seeds, {len(targets)//2:,} unnamed sound_alias ids -> "
          f"{len(found):,} exact three-byte candidates", file=sys.stderr)
    for candidate in sorted(found):
        print(candidate)


if __name__ == "__main__":
    main(sys.argv[1:])
