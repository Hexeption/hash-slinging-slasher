from pathlib import Path

src = Path(__file__).with_name('cw_two_byte_pool.candidates.txt')
for line in src.read_text(encoding='utf-8').splitlines():
    line=line.strip()
    if line: print(line)
