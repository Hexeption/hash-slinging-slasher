"""Try one-character deletions in known non-sound asset basenames."""
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import snapshot


def main():
    tables = ("fnv1a_xmodels", "fnv1a_xmaterials", "fnv1a_ximages", "fnv1a_xanims")
    names = {n.strip().lower().replace("\\", "/") for t in tables for n in snapshot.table_names(t) if n.strip()}
    names.update(n.strip().lower().replace("\\", "/") for n in snapshot.confirmed_names() if n.strip())
    alphabet = set("0123456789_abcdefghijklmnopqrstuvwxyz")
    out = set()
    for name in names:
        cut = max(name.rfind("/"), name.rfind("\\")) + 1
        head, base = name[:cut], name[cut:]
        for pos, char in enumerate(base):
            if char in alphabet and len(base) > 1:
                out.add(head + base[:pos] + base[pos + 1:])
    for candidate in sorted(out):
        print(candidate)
    print(f"{len(names):,} non-sound seeds, {len(out):,} deletion candidates", file=sys.stderr)


if __name__ == "__main__":
    main()
