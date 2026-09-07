from pathlib import Path

for line in (Path(__file__).with_name('families_gaps_after_legacy_20260829.candidates.txt')).read_text(encoding='utf-8').splitlines():
    line = line.strip()
    if line:
        print(line)
