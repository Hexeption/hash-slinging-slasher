"""Negative-space probe: uncarried mcdp/mtl heads with observed material tails."""
from pathlib import Path
import re
rows=[]
for p in Path('findings').glob('*/material.txt'):
    try: rows += [x.split(',',1)[1].strip() for x in p.read_text(errors='ignore').splitlines() if ',' in x]
    except OSError: pass
heads=sorted({x[:x.find('_',5)+1] for x in rows if x.startswith('mcdp/mtl_')})[:40]
tails=sorted({x[x.find('_',5)+1:] for x in rows if not x.startswith('mcdp/mtl_') and '_' in x})[:40]
for h in heads:
    for t in tails:
        print(h+t)
