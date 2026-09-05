"""Replay the staged Lucy source-path corpus as exact literals."""
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
for line in (ROOT / "contrib" / "lucy_source_paths_20260829.candidates.txt").read_text(encoding="utf-8").splitlines():
    if line.strip():
        print(line.strip())
