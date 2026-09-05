"""Replay the staged Atian source-context candidate corpus."""
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
path = ROOT / "contrib" / "atian_source_context_20260829.candidates.txt"
for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
    if line.strip():
        print(line.strip())
