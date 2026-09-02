"""Replay the staged BO4 final-byte candidates after image-channel gains."""
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CANDIDATES = ROOT / "contrib" / "final_byte_after_upstream_bo4_20260829.candidates.txt"


def main():
    print(CANDIDATES.read_text(encoding="utf-8"), end="")


if __name__ == "__main__":
    main()
