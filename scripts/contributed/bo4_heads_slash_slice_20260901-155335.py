"""Probe an untested slice of slash-bearing five-character name fronts."""
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
begins = (ROOT / "plans" / "codex_heads5_slash_20260825.begins.txt").read_text(encoding="utf-8").splitlines()
stems = (ROOT / "plans" / "codex_heads5_slash_20260825.stems.txt").read_text(encoding="utf-8").splitlines()

# Disjoint from the earlier bounded probe: fronts 1,001-2,000 and bodies 5,001-10,000.
for begin in begins[1000:2000]:
    for stem in stems[5000:10000]:
        if begin and stem:
            print(begin + stem)
