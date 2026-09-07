from pathlib import Path
for x in Path('.tmp-shop-sound-bo4.candidates').read_text().splitlines():
    if x.strip(): print(x.strip())
