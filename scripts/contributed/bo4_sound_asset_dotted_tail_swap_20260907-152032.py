"""Swap the first and final dotted-tail components of known BO4 SAB sound paths."""
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parent.parent; sys.path.insert(0,str(ROOT/'scripts')); import snapshot
names={n.strip() for n in snapshot.confirmed_names('sound_asset') if n.strip()}
names.update(n.strip() for n in snapshot.table_names('fnv1a_english_xsounds') if n.strip())
out=set()
for n in names:
 base=n.rsplit('\\',1)[-1].rsplit('/',1)[-1]
 if base.count('.')<3: continue
 bits=base.split('.'); bits[1],bits[-2]=bits[-2],bits[1]
 pos=max(n.rfind('\\'),n.rfind('/')); out.add(n[:pos+1]+'.'.join(bits))
print(f'{len(names):,} seeds -> {len(out):,} candidates',file=sys.stderr)
for c in sorted(out): print(c)
