"""Negative-space sound probe for uncarried wolf VOX beginning."""
from pathlib import Path
tails=set()
for p in Path('findings').glob('*/sound_alias.txt'):
    try:
        for l in p.read_text(errors='ignore').splitlines():
            if ',' in l:
                n=l.split(',',1)[1].strip(); i=n.rfind('_')
                if i>=0: tails.add(n[i:])
    except OSError: pass
for t in sorted(tails)[:1000]: print('vox/scripted/wolf/vox'+t)
