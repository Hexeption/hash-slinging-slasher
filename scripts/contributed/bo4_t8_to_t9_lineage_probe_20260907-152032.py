"""Reverse cross-title lineage probe: BO4 t8 materials to CW t9."""
from pathlib import Path
seen=set()
for l in Path('findings/blkops04/material.txt').read_text(errors='ignore').splitlines():
    if ',' in l:
        n=l.split(',',1)[1].strip()
        if 't8' in n.lower(): seen.add(n.replace('t8','t9').replace('T8','T9'))
for n in sorted(seen)[:2000]: print(n)
