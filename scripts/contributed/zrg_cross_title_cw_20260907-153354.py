from pathlib import Path
for x in Path('.tmp-zrg.candidates').read_text().splitlines():
    if x.strip(): print(x.strip())
