"""Rotate letters right within one sound-alias token, preserving all other tokens."""
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parent.parent; sys.path.insert(0,str(ROOT/'scripts')); import snapshot
names={n.strip().lower().replace('\\','/') for n in snapshot.table_names('fnv1a_soundbanks_aliases')}
names.update(n.strip().lower().replace('\\','/') for n in snapshot.confirmed_names('sound_alias'))
out=set()
for n in sorted(names):
 p=n.split('_')
 for i,t in enumerate(p):
  if len(t)<3 or not t.isalpha(): continue
  q=p[:]; q[i]=t[-1]+t[:-1]; c='_'.join(q)
  if c not in names: out.add(c)
print(f'{len(names):,} aliases -> {len(out):,} candidates',file=sys.stderr)
for c in sorted(out): print(c)
