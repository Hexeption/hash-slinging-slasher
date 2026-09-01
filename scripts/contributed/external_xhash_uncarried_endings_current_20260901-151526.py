"""Write all-boundary cores from external BO4 xhash names for an uncarried-ending plan."""
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parent.parent
SOURCE = ROOT / "borrowed" / "bo4_xhash_table_names_current.txt"


def main():
    cores = set()
    for raw in SOURCE.read_text(encoding="utf-8", errors="ignore").splitlines():
        value = raw.strip().lower().replace("\\", "/")
        if not value:
            continue
        base = value.rsplit("/", 1)[-1]
        if "." in base:
            base = base.rsplit(".", 1)[0]
        for index, char in enumerate(base):
            if char == "_" and index >= 8:
                cores.add(base[:index])
        if len(base) >= 8:
            cores.add(base)
    for core in sorted(cores):
        print(core)
    print(f"{len(cores):,} external xhash all-boundary cores", file=sys.stderr)


if __name__ == "__main__":
    main()
