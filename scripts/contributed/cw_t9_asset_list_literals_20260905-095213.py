"""Extract conservative asset-shaped literals from the public T9 extracted list."""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "borrowed" / "T9-Assets-Extracted-List" / "Assets Extracted"
TOKEN = re.compile(r"[A-Za-z0-9][A-Za-z0-9_./\\-]{5,180}")
PREFIXES = ("mc/", "wc/", "clt/", "splm/", "vd/", "mcs/", "ei/", "cltp/", "vdd/", "el/", "mcp/", "ec/",
            "i_", "mtl_", "xmodel_", "xanim_", "p9_", "p8_", "p7_", "wpn_", "weapon_", "zmb_", "ui_")
found = set()
files = 0
for path in SOURCE.rglob("*"):
    if not path.is_file() or path.suffix.lower() not in {".csv", ".lua"}:
        continue
    files += 1
    text = path.read_text(encoding="utf-8", errors="ignore")
    for value in TOKEN.findall(text):
        value = value.lower().replace("\\", "/").strip("'\".,;()[]{}")
        if "_" not in value and "/" not in value:
            continue
        if not any(value.startswith(prefix) for prefix in PREFIXES):
            continue
        if sum(char.isalpha() for char in value) < 3:
            continue
        found.add(value)
print(f"{files:,} T9 list files, {len(found):,} asset-shaped literals")
for value in sorted(found):
    print(value)
