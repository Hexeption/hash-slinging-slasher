"""Emit asset-shaped paths carried as filenames inside borrowed ZIP archives."""
from pathlib import Path
import re
import sys
import zipfile

ROOT = Path(__file__).resolve().parents[1]
TOKEN = re.compile(r"(?:^|/)((?:mc|wc|clt|splm|vd|mcs|ei|cltp|vdd|el|mcp|ec)/[^/]+|(?:i_|mtl_|xmodel_|xanim_|wpn_|weapon_|zm_|mp_|ui_|snd_|amb_)[A-Za-z0-9_./\\:-]{3,220})$", re.I)


def main():
    names = set()
    archives = 0
    members = 0
    for archive in (ROOT / "borrowed").rglob("*.zip"):
        try:
            with zipfile.ZipFile(archive) as bundle:
                archives += 1
                for info in bundle.infolist():
                    members += 1
                    path = info.filename.replace("\\", "/").strip("/").lower()
                    if not path or path.endswith("/"):
                        continue
                    match = TOKEN.search(path)
                    if not match:
                        continue
                    value = path.strip("'\"`.,;()[]{}<>|\r\n\t")
                    if sum(char.isalpha() for char in value) >= 3:
                        names.add(value)
        except (OSError, zipfile.BadZipFile):
            continue
    print(f"{archives:,} archives, {members:,} member paths -> {len(names):,} literals", file=sys.stderr)
    for name in sorted(names):
        print(name)


if __name__ == "__main__":
    main()
