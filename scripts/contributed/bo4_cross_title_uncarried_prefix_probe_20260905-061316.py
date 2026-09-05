"""Bounded probe of BO4-only uncarried heads over Cold War non-sound cores."""
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parent.parent; sys.path.insert(0,str(ROOT/'scripts'))
import snapshot, seams
carried={x.strip() for x in (ROOT/'data'/'prefixes.txt').read_text().splitlines() if x.strip()}
tables=('fnv1a_xmodels','fnv1a_xmaterials','fnv1a_ximages','fnv1a_xanims')
bo4={n.strip().lower().replace('\\','/') for t in tables for n in snapshot.table_names(t)}
counts={}
for n in bo4:
 for i,ch in enumerate(n):
  if ch in '_/' and i<40: counts[n[:i+1]]=counts.get(n[:i+1],0)+1
heads=[h for h,_ in sorted(((h,c) for h,c in counts.items() if h not in carried),key=lambda x:(-x[1],x[0]))[:25]]
red=dict(seams.REDUCTIONS); cw=[]
for t in tables:
 for n in snapshot.table_names(t):
  n=n.strip().lower().replace('\\','/')
  for label in ('no head','no ends'):
   c=red[label](n)
   if len(c)>=8: cw.append(c)
cores=sorted(set(cw))[:250]
out={h+c for h in heads for c in cores}
print(f'{len(heads)} uncarried BO4 heads x {len(cores)} CW cores = {len(out):,} candidates',file=sys.stderr)
for n in sorted(out): print(n)
