"""Negative-space probe for the uncarried o_ beginning."""
from pathlib import Path
tails=set()
for p in Path('findings').glob('*/material.txt'):
    try:
        for line in p.read_text(errors='ignore').splitlines():
            if ',' in line:
                n=line.split(',',1)[1].strip()
                if '_' in n: tails.add(n[n.find('_'):])
    except OSError: pass
for t in sorted(tails)[:200]: print('o'+t)
