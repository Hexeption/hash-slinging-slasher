"""Sound-only within-name delimiter transform: dotted tail to underscore."""
from pathlib import Path
seen=set()
for p in [Path('findings/blkops04/sound_asset.txt'),Path('findings/blkops04/sound.txt'),Path('findings/blkops04/sound_alias.txt')]:
    try:
        for l in p.read_text(errors='ignore').splitlines():
            if ',' in l:
                n=l.split(',',1)[1].strip()
                if '.' in n: seen.add(n.replace('.', '_'))
    except OSError: pass
for n in sorted(seen): print(n)
