"""Extract asset-shaped quoted literals from standalone BO4 source-lua default file."""
from pathlib import Path
import re, sys
ROOT=Path(__file__).resolve().parent.parent
text=(ROOT/'borrowed'/'bo4-source-lua'/'default.lua').read_text(encoding='utf-8',errors='ignore')
out=set()
for m in re.finditer(r'''["']([A-Za-z0-9_./\\-]{6,160})["']''',text):
 v=m.group(1).lower()
 if '_' in v and any(x in v for x in ('xmodel','xanim','image','mtl','weapon','menu')): out.add(v)
print(f'{len(out):,} default.lua asset-shaped literals',file=sys.stderr)
for v in sorted(out): print(v)
