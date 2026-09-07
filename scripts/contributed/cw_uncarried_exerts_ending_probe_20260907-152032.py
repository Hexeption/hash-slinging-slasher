"""Negative-space within-name probe for uncarried _exerts ending."""
from pathlib import Path
seen=set()
for p in Path('findings').glob('*/material.txt'):
    try:
        for l in p.read_text(errors='ignore').splitlines():
            if ',' in l:
                n=l.split(',',1)[1].strip()
                if n and not n.endswith('_exerts'): seen.add(n+'_exerts')
    except OSError: pass
for n in sorted(seen)[:2000]: print(n)
