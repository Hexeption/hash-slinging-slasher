"""Sound-asset within-name transform: duplicate final basename character."""
from pathlib import Path
seen=set()
p=Path('findings/blkops04/sound_asset.txt')
try:
    for l in p.read_text(errors='ignore').splitlines():
        if ',' in l:
            n=l.split(',',1)[1].strip(); base=n.rsplit('\\',1)[-1].rsplit('/',1)[-1]
            if base: seen.add(n+base[-1])
except OSError: pass
for n in sorted(seen): print(n)
