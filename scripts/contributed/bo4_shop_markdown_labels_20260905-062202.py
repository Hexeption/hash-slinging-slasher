"""Bounded BO4 shop-repository Markdown code-label provenance probe."""
from pathlib import Path
import re
out = set()
for p in Path('.tmp-bo4shop').rglob('*.md'):
    try: s = p.read_text(encoding='utf-8', errors='ignore')
    except OSError: continue
    for x in re.findall(r'(?<![A-Za-z0-9_])(?:wpn|i|mtl|xmodel|xanim)_[A-Za-z0-9_./\\-]{3,180}', s):
        out.add(x.rstrip('.,:;`)]'))
for x in sorted(out): print(x)
