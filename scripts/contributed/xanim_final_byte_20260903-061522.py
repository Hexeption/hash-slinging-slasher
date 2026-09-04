"""Try printable final-byte substitutions using only known xanim names as seeds."""
import os
import string
import sys

_root = os.path.dirname(os.path.abspath(__file__))
while _root != os.path.dirname(_root) and not os.path.isfile(
    os.path.join(_root, "scripts", "snapshot.py")
):
    _root = os.path.dirname(_root)
sys.path.insert(0, os.path.join(_root, "scripts"))
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
            if candidate not in names:
                out.add(candidate)
    for candidate in sorted(out):
        sys.stdout.write(candidate + "\n")
    sys.stderr.write(f"{len(names):,} xanim seeds -> {len(out):,} final-byte candidates\n")

if __name__ == "__main__":
    main()
