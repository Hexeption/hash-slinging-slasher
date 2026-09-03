"""Fill observed grid cells under sound-alias heads omitted by the prefix list."""
import collections
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))
import snapshot


def main():
    tables = snapshot.table_names("fnv1a_soundbanks_aliases")
    confirmed = snapshot.confirmed_names("sound_alias")
    known = {name.strip().lower().replace("\\", "/") for name in tables + confirmed if name.strip()}
    carried = {
        line.strip().lower()
        for line in (ROOT / "data" / "sound.prefixes.txt").read_text(encoding="utf-8", errors="replace").splitlines()
        if line.strip()
    }
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
            if len(parts) == 2 and parts[0] and parts[1]:
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
