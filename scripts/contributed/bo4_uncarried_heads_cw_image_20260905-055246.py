"""Probe BO4 uncarried leading cuts over independently sourced CW image cores."""
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parent.parent; sys.path.insert(0,str(ROOT/'scripts'))
import snapshot, seams
carried={x.strip() for x in (ROOT/'data'/'prefixes.txt').read_text().splitlines() if x.strip()}
bo4={n.strip().lower().replace('\\','/') for n in snapshot.table_names('fnv1a_ximages')}
counts={}
for n in bo4:
 for i,ch in enumerate(n):
  if ch in '_/' and i<40: counts[n[:i+1]]=counts.get(n[:i+1],0)+1
heads=[h for h,_ in sorted(((h,c) for h,c in counts.items() if h not in carried),key=lambda x:(-x[1],x[0]))[:20]]
red=dict(seams.REDUCTIONS); cores=set()
for n in snapshot.table_names('fnv1a_ximages'):
 n=n.strip().lower().replace('\\','/')
 for label in ('no head','no ends'):
  c=red[label](n)
  if len(c)>=8: cores.add(c)
cores=sorted(cores)[:200]; out={h+c for h in heads for c in cores}
print(f'{len(heads)} heads x {len(cores)} CW image cores = {len(out):,}',file=sys.stderr)
for n in sorted(out): print(n)
