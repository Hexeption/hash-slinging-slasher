"""Solve sound-asset names differing from a known seed in their final two bytes.

For ``h = (((prefix ^ a) * P) ^ b) * P``, multiplying backwards twice gives
``((h * P^-1) ^ b) * P^-1 = prefix_hash ^ a``.  Thus each target id needs only 256 lookups,
while the low byte recovers ``a`` exactly.  This is the two-byte extension of final_byte, aimed
only at sound_asset and retaining the raw spelling needed by BO4 SAB names.
"""
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


def choose_snapshot(game):
    for path in snapshot.snapshots():
        shot = snapshot.read(path)
        if shot.game.lower() == game.lower():
            return shot
    raise SystemExit(f"snapshot not found for {game}")


def main(argv):
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--game", required=True, choices=("BLKOPS04", "BLKOPSCW"))
    options = parser.parse_args(argv)
    shot = choose_snapshot(options.game)
    fold = options.game == "BLKOPSCW"
    hash_name = snapshot.fnv1a if fold else snapshot.fnv1a_nofold

    seeds = set(snapshot.table_names("fnv1a_xsounds"))
    seeds.update(snapshot.confirmed_names("sound_asset"))
    prefixes = {}
    for seed in seeds:
        seed = seed.strip().lower()
        if len(seed) < 3:
            continue
        prefix = seed[:-2]
        value = hash_name(prefix)
        prefixes.setdefault(value >> 8, []).append((value & 0xFF, prefix))

    known = snapshot.known_hashes()
    targets = [asset_id for asset_id, pool in shot.unnamed(known).items()
               if pool == "sound_asset"]
    targets = targets + [asset_id | TOP for asset_id in targets]

    found = set()
    for target in targets:
        scaled = (target * INVERSE) & MASK
        for last in PRINTABLE:
            value = ((scaled ^ last) * INVERSE) & MASK
            for low, prefix in prefixes.get(value >> 8, ()):
                first = low ^ (value & 0xFF)
                if first not in PRINTABLE:
                    continue
                candidate = prefix + chr(first) + chr(last)
                if hash_name(candidate) == target:
                    found.add(candidate)

    print(f"{len(seeds):,} seeds, {len(targets) // 2:,} unnamed sound_asset ids -> "
          f"{len(found):,} exact two-byte candidates", file=sys.stderr)
    for candidate in sorted(found):
        print(candidate)


if __name__ == "__main__":
    main(sys.argv[1:])
