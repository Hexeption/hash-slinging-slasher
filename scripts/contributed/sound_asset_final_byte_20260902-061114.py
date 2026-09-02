"""Emit sound-asset names differing from a known sound asset in exactly one final byte.

This is the sound-specific counterpart to ``scripts/final_byte.py``.  Sound assets are excluded
from that general solver because Black Ops 4 SAB names hash with literal backslashes; keeping the
original spelling here lets the verifier use ``--no-fold`` for that title.
"""
import argparse
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)) + os.sep + ".." + os.sep + "scripts")
import snapshot


def names():
    values = snapshot.table_names("fnv1a_xsounds")
    values += snapshot.confirmed_names("sound_asset")
    return {value.strip().lower() for value in values if value.strip()}


def main(argv):
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--alphabet", default="printable",
                        choices=("printable", "bytes"),
                        help="final bytes to emit (printable is sufficient for asset names)")
    options = parser.parse_args(argv)

    alphabet = range(0x20, 0x7f) if options.alphabet == "printable" else range(256)
    seen = set()
    for value in names():
        if len(value) < 2:
            continue
        prefix = value[:-1]
        for byte in alphabet:
            candidate = prefix + chr(byte)
            if candidate != value and candidate not in seen:
                seen.add(candidate)
                print(candidate)

    print(f"{len(names()):,} sound-asset seeds -> {len(seen):,} one-byte candidates",
          file=sys.stderr)


if __name__ == "__main__":
    main(sys.argv[1:])
