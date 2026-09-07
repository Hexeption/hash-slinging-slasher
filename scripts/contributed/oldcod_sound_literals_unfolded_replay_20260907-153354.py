from pathlib import Path
src=Path(__file__).with_name('oldcod_sound_literals_unfolded_20260830.candidates.txt')
for x in src.read_text(encoding='utf-8').splitlines():
    if x.strip(): print(x.strip())
