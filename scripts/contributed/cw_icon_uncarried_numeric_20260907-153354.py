"""Within-name probe for uncarried icon_ numeric ending."""
from pathlib import Path
seen=set()
for p in Path('findings').glob('*/material.txt'):
    try:
        for l in p.read_text(errors='ignore').splitlines():
            if ',' in l:
                n=l.split(',',1)[1].strip()
                if n.startswith('icon_'): seen.add(n+'_01')
    except OSError: pass
for n in sorted(seen): print(n)
