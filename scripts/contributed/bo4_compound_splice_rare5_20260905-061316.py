"""Bounded BO4 compound splice using only very-rare shared interior tokens."""
from pathlib import Path
import collections, sys
ROOT=Path(__file__).resolve().parent.parent
sys.path.insert(0,str(ROOT/'scripts')); import snapshot
tables=('fnv1a_xmodels','fnv1a_xmaterials','fnv1a_ximages','fnv1a_xanims')
names={n.strip().lower().replace('\\','/') for t in tables for n in snapshot.table_names(t)}
names.update(n.strip().lower().replace('\\','/') for n in snapshot.confirmed_names())
occ=collections.Counter(); sides=collections.defaultdict(lambda:[set(),set()])
for n in names:
 d,_,r=n.partition('/'); d=(d+'/' if r and len(d)<=6 and '_' not in d else ''); p=(r if d else n).split('_')
 if len(p)<4: continue
 for i,t in enumerate(p[1:-1],1): occ[(d,t)]+=1; sides[(d,t)][0].add('_'.join(p[:i])); sides[(d,t)][1].add('_'.join(p[i+1:]))
out=set()
for (d,t), (pre,suf) in sides.items():
 if 2<=occ[(d,t)]<=5:
  for a in pre:
   for b in suf: out.add(d+a+'_'+t+'_'+b)
print(f'{len(out):,} candidates',file=sys.stderr)
for n in sorted(out): print(n)
