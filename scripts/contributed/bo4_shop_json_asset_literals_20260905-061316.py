"""Bounded BO4 shop-export JSON asset-literal provenance probe."""
import json, re

src = ".tmp-bo4shop/raw/items.json"
try:
    root = json.load(open(src, encoding="utf-8"))
except Exception:
    root = None

out = set()
def walk(v):
    if isinstance(v, dict):
        for x in v.values(): walk(x)
    elif isinstance(v, list):
        for x in v: walk(x)
    elif isinstance(v, str):
        s = v.strip()
        if 3 < len(s) < 240 and ("/" in s or "\\" in s or "_" in s) and re.fullmatch(r"[A-Za-z0-9_./\\-]+", s):
            out.add(s)
walk(root)
for s in sorted(out):
    print(s)
