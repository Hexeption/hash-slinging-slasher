"""Try one-character deletions in known sound basenames."""
from pathlib import Path
import sys
import argparse

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import snapshot


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--unfolded", action="store_true")
    args = parser.parse_args()
    tables = ("fnv1a_xsounds", "fnv1a_english_xsounds", "fnv1a_soundbanks_aliases")
    def normal(n):
        n = n.strip().lower()
        return n.replace("/", "\\") if args.unfolded else n.replace("\\", "/")
    names = {normal(n) for t in tables for n in snapshot.table_names(t) if n.strip()}
    names.update(normal(n) for n in snapshot.confirmed_names() if n.strip())
    alphabetic = set("0123456789_abcdefghijklmnopqrstuvwxyz")
    out = set()
    for name in names:
        cut = max(name.rfind("/"), name.rfind("\\")) + 1
        head, base = name[:cut], name[cut:]
        dot = base.find(".")
        if dot < 2:
            continue
        core, tail = base[:dot], base[dot:]
        for pos, char in enumerate(core):
            if char in alphabetic:
                out.add(head + core[:pos] + core[pos + 1:] + tail)
    for candidate in sorted(out):
        print(candidate)
    print(f"{len(names):,} sound seeds, {len(out):,} deletion candidates", file=sys.stderr)


if __name__ == "__main__":
    main()
