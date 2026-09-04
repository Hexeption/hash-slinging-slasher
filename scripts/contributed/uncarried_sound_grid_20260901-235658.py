"""Fill grid cells under sound-alias family heads that the general prefix list cannot carry.

Run: python contrib/uncarried_sound_grid_20260901.py | bin/windows/confirm_list.exe - --game BLKOPS04 --no-fold --label "uncarried sound alias grids" --script contrib/uncarried_sound_grid_20260901.py

Reads the sound-alias tables, confirmed names, and data/sound.prefixes.txt. Writes candidates to
stdout and is reusable: it derives uncarried heads and shared axis/tail cells on each run.
Measured: 190 candidates, 0 matches in each title on 2026-09-01.
"""
import collections
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parent
while not (ROOT / "scripts" / "snapshot.py").exists() and ROOT != ROOT.parent:
    ROOT = ROOT.parent
sys.path.insert(0, str(ROOT / "scripts"))
import snapshot


def main():
    tables = snapshot.table_names("fnv1a_soundbanks_aliases")
    confirmed = snapshot.confirmed_names("sound_alias")
    known = {n.strip().lower().replace("\\", "/") for n in tables + confirmed if n.strip()}
    with (ROOT / "data" / "sound.prefixes.txt").open(encoding="utf-8", errors="replace") as f:
        carried = {line.strip().lower() for line in f if line.strip()}

    families = collections.defaultdict(list)
    for name in known:
        if "/" in name or "." in name or "\\" in name:
            continue
        first, sep, rest = name.partition("_")
        if sep and "_" in rest:
            families[first + "_"].append(name)

    candidates = set()
    selected = 0
    for head, names in families.items():
        if any(head[:cut] in carried for cut in range(1, min(len(head), 40) + 1)):
            continue
        axes = set()
        tails = collections.Counter()
        for name in names:
            rest = name[len(head):]
            parts = rest.split("_", 1)
            if len(parts) != 2 or not parts[0] or not parts[1]:
                continue
            axes.add(parts[0])
            tails[parts[1]] += 1
        shared = {tail for tail, count in tails.items() if count > 1}
        if len(axes) < 2 or not shared:
            continue
        selected += 1
        for axis in axes:
            for tail in shared:
                candidate = head + axis + "_" + tail
                if candidate not in known:
                    candidates.add(candidate)

    print(f"{selected:,} uncarried sound families, {len(candidates):,} grid cells", file=sys.stderr)
    for candidate in sorted(candidates):
        print(candidate)


if __name__ == "__main__":
    main()
