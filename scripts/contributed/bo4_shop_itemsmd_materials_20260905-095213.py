"""Source-backed BO4 ITEMS.md title-to-material seam."""
import re
try: text=open('borrowed/BlackOps4Shop/ITEMS.md',encoding='utf-8').read()
except OSError: text=''
seen=set()
for line in text.splitlines():
    m=re.match(r'^#+\s+(.+?)\s*$',line)
    if not m: continue
    s=re.sub(r'[^a-z0-9]+','_',m.group(1).lower()).strip('_')
    if 3<len(s)<100 and '_' in s: seen.add(s)
for s in sorted(seen): print('mtl_'+s)
