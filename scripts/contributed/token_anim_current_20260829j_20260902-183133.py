"""Replay the staged paired-token-block animation candidates.

The candidate list was generated during the paired-token-blocks-anim reconnaissance pass and
survived in the staging area after its original generator was lost.  Keeping this replay wrapper
beside the list lets confirmation and submission preserve the method provenance.
"""
import pathlib


ROOT = pathlib.Path(__file__).resolve().parent.parent
CANDIDATES = ROOT / "contrib" / "token_anim_current_20260829j.candidates.txt"


def main():
    print(CANDIDATES.read_text(encoding="utf-8"), end="")


if __name__ == "__main__":
    main()
