"""Extract asset-shaped names from paths of files in borrowed directory trees."""
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
TOKEN = re.compile(r"(?:^|/)((?:mc|wc|clt|splm|vd|mcs|ei|cltp|vdd|el|mcp|ec)/[^/]+|(?:i_|mtl_|xmodel_|xanim_|wpn_|weapon_|zm_|mp_|ui_|snd_|amb_)[A-Za-z0-9_./\\:-]{3,220})$", re.I)


def main():
    names = set()
    files = 0
    for path in (ROOT / "borrowed").rglob("*"):
        if not path.is_file():
            continue
        files += 1
        try:
            relative = path.relative_to(ROOT / "borrowed").as_posix().lower()
        except ValueError:
            continue
        match = TOKEN.search(relative)
        if not match:
            continue
        value = relative.strip("'\"`.,;()[]{}<>|\r\n\t")
        if value.count("/") <= 12 and sum(char.isalpha() for char in value) >= 3:
            names.add(value)
    print(f"{files:,} borrowed files -> {len(names):,} asset-shaped paths", file=sys.stderr)
    for name in sorted(names):
        print(name)


if __name__ == "__main__":
    main()
