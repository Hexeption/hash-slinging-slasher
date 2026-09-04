"""Generate printable final-byte variants of confirmed xanim names.

Run with ``python scripts/contrib/xanim_final_byte_seed_current.py``.  Reads the
xanim table and confirmed xanim findings; writes candidates to stdout.  Reusable.
"""
import os
import string
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))
while ROOT != os.path.dirname(ROOT) and not os.path.isfile(os.path.join(ROOT, "scripts", "snapshot.py")):
    ROOT = os.path.dirname(ROOT)
sys.path.insert(0, os.path.join(ROOT, "scripts"))
import snapshot


def main():
    names = set(snapshot.table_names("fnv1a_xanims"))
    names.update(snapshot.confirmed_names("xanim"))
    alphabet = string.ascii_lowercase + string.digits + "_-"
    out = set()
    for value in names:
        value = value.strip().lower().replace("\\", "/")
        if len(value) < 2:
            continue
        for char in alphabet:
            candidate = value[:-1] + char
            if candidate != value:
                out.add(candidate)
    for candidate in sorted(out):
        print(candidate)
    print(f"{len(names):,} xanim seeds -> {len(out):,} final-byte candidates", file=sys.stderr)


if __name__ == "__main__":
    main()
