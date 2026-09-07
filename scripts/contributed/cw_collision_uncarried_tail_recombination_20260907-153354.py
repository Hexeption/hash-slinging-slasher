"""Negative-space collision_ beginning with observed material tails."""
from pathlib import Path
rows=[]
for p in Path('findings').glob('*/material.txt'):
    try: rows += [x.split(',',1)[1].strip() for x in p.read_text(errors='ignore').splitlines() if ',' in x]
    except OSError: pass
heads=sorted({x[:10] for x in rows if x.startswith('collision_')})
tails=sorted({x[x.rfind('_'):] for x in rows if '_' in x})[:80]
for h in heads:
    for t in tails: print(h+t)
