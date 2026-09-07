"""Cross-type prefix seam over independent BO4 shop-export literals."""
import subprocess, re
src = ".tmp-bo4shop/raw/items.json"
try:
    text = open(src, encoding="utf-8").read()
except OSError:
    text = ""
vals = sorted(set(re.findall(r'"([A-Za-z0-9_./\\-]{4,220})"', text)))
for s in vals:
    if "/" in s or "\\" in s or "_" in s:
        for p in ("i_", "mtl_"):
            print(p + s)
