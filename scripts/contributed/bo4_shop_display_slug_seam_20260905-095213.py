"""Bounded display-name slug seam from BlackOps4Shop records."""
import json, re
try:
    root = json.load(open('borrowed/BlackOps4Shop/raw/items.json', encoding='utf-8'))
except Exception:
    root = []
vals = set()
def walk(v):
    if isinstance(v, dict):
        for x in v.values(): walk(x)
    elif isinstance(v, list):
        for x in v: walk(x)
    elif isinstance(v, str):
        s = re.sub(r'[^a-z0-9]+', '_', v.lower()).strip('_')
        if 2 < len(s) < 100 and '_' in s: vals.add(s)
walk(root)
for s in sorted(vals):
    print('i_' + s)
    print('mtl_' + s)
