"""Try swapping each adjacent basename character in known non-sound assets."""
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import snapshot


def main():
    tables = ("fnv1a_xmodels", "fnv1a_xmaterials", "fnv1a_ximages", "fnv1a_xanims")
    names = {n.strip().lower().replace("\\", "/") for t in tables for n in snapshot.table_names(t) if n.strip()}
    names.update(n.strip().lower().replace("\\", "/") for n in snapshot.confirmed_names() if n.strip())
    out = set()
    for name in names:
        cut = max(name.rfind("/"), name.rfind("\\")) + 1
        head, base = name[:cut], name[cut:]
        for pos in range(len(base) - 1):
            if base[pos] != base[pos + 1]:
                out.add(head + base[:pos] + base[pos + 1] + base[pos] + base[pos + 2:])
    for candidate in sorted(out):
        print(candidate)
    print(f"{len(names):,} non-sound seeds, {len(out):,} adjacent-transpose candidates", file=sys.stderr)


if __name__ == "__main__":
    main()
