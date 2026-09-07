"""Cross-title lineage probe: substitute t9 token with t8 in CW materials."""
from pathlib import Path
seen=set()
for p in Path('findings').glob('*/material.txt'):
    try:
        for l in p.read_text(errors='ignore').splitlines():
            if ',' in l:
                n=l.split(',',1)[1].strip()
                if 't9' in n.lower(): seen.add(n.replace('t9','t8').replace('T9','T8'))
    except OSError: pass
for n in sorted(seen)[:2000]: print(n)
