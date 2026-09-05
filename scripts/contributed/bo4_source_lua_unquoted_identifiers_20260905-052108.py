"""Extract asset-shaped unquoted identifiers from hashed BO4 Lua source files."""
from pathlib import Path
import re, sys
ROOT=Path(__file__).resolve().parent.parent; src=ROOT/'borrowed'/'bo4-source-lua'
out=set(); ident=re.compile(r'(?<![A-Za-z0-9_])([A-Za-z][A-Za-z0-9_./\\-]{5,120})(?![A-Za-z0-9_])')
for p in src.rglob('*.lua'):
 try: text=p.read_text(encoding='utf-8',errors='ignore')
 except OSError: continue
 for m in ident.finditer(text):
  v=m.group(1).lower()
  if '_' in v and any(x in v for x in ('xmodel','xanim','image','mtl','weapon','zm_','mp_')): out.add(v)
print(f'{len(out):,} unquoted Lua identifiers',file=sys.stderr)
for v in sorted(out): print(v)
