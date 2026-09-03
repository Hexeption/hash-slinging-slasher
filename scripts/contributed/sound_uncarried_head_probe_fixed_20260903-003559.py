"""Probe selected uncarried sound-alias family heads against measured sound endings."""
import argparse
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))
import snapshot


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("heads", nargs="+")
    args = parser.parse_args()
    known = {
        name.strip().lower().replace("\\", "/")
        for name in snapshot.table_names("fnv1a_soundbanks_aliases") + snapshot.confirmed_names("sound_alias")
        if name.strip()
    }
    endings = [
        line.strip().lower()
        for line in (ROOT / "data" / "sound.suffixes.txt").read_text(encoding="utf-8", errors="replace").splitlines()
        if line.strip()
    ]
    candidates = set()
    seed_count = 0
    stem_count = 0
    for raw_head in args.heads:
        head = raw_head.lower()
        family = sorted(name for name in known if name.startswith(head))
        seed_count += len(family)
        stems = set()
        for name in family:
            rest = name[len(head):]
            tokens = rest.split("_")
            if len(rest) >= 4:
                stems.add(rest)
            for cut in range(1, len(tokens)):
                core = "_".join(tokens[:-cut])
                if len(core) >= 4:
                    stems.add(core)
        stem_count += len(stems)
        candidates.update(
            head + stem + ending
            for stem in stems
            for ending in endings
            if head + stem + ending not in known
        )
    print(
        f"{len(args.heads)} heads, {seed_count:,} family seeds, {stem_count:,} stems, {len(candidates):,} candidates",
        file=sys.stderr,
    )
    for candidate in sorted(candidates):
        print(candidate)


if __name__ == "__main__":
    main()
