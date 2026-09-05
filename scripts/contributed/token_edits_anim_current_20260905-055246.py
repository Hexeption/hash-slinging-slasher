"""Replay the staged current animation token-edit candidate corpus."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
for line in (ROOT / "contrib" / "token_edits_anim_current_20260928.txt").open(encoding="utf-8"):
    print(line, end="")
