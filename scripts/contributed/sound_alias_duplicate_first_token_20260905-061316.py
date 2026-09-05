from pathlib import Path
for line in Path('data/sound.aliases.txt').read_text().splitlines():
    s=line.strip()
    if not s: continue
    p=s.split('_')
    if len(p)>1: print(p[0]+'_'+s)
