"""Negative-space probe for uncarried lut_mp_ beginning."""
from pathlib import Path
tails=set()
for p in Path('findings').glob('*/material.txt'):
    try:
        for l in p.read_text(errors='ignore').splitlines():
            if ',' in l:
                n=l.split(',',1)[1].strip(); i=n.find('_')
                if i>=0: tails.add(n[i:])
    except OSError: pass
for t in sorted(tails)[:2000]: print('lut_mp'+t)
