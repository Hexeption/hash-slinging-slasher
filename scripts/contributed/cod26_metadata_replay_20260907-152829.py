"""Replay the precomputed COD26 metadata asset-shaped string slice."""
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
for line in (ROOT / "contrib" / "cod26_metadata.candidates.txt").read_text(encoding="utf-8").splitlines():
    if line.strip():
        print(line.strip())
