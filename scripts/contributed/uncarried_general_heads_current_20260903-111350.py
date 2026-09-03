"""Probe high-frequency general-asset heads omitted by the measured prefix ceiling."""
import argparse
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.join(ROOT, "scripts"))
import snapshot

HEADS = (
    "collision_", "o_", "icon_", "s4_", "special_", "core_", "lut_",
    "reflex_", "volume14_state0_reflection_probes_f788ac97_", "acog_",
    "streaming_temp_image_", "holo_", "dualoptic_", "mms_",
)
TABLES = (
    "fnv1a_xmodels", "fnv1a_xmaterials", "fnv1a_ximages",
    "fnv1a_xanims", "fnv1a_soundbanks_aliases",
)


def known():
    names = []
    for table in TABLES:
        names.extend(snapshot.table_names(table))
    names.extend(snapshot.confirmed_names())
    return {n.strip().lower().replace("\\", "/") for n in names if n.strip()}


def endings():
    path = os.path.join(ROOT, "data", "suffixes.txt")
    return {
        line.strip().lower().replace("\\", "/")
        for line in open(path, encoding="utf-8", errors="replace")
        if line.strip()
    }


def candidates():
    present = known()
    suffixes = endings()
    out = set()
    for head in HEADS:
        family = [name[len(head):] for name in present if name.startswith(head)]
        stems = set()
        for rest in family:
            if len(rest) >= 4:
                stems.add(rest)
            tokens = rest.split("_")
            for cut in range(1, len(tokens)):
                core = "_".join(tokens[:-cut])
                if len(core) >= 4:
                    stems.add(core)
        for stem in stems:
            for ending in suffixes:
                candidate = head + stem + ending.lstrip("_")
                if candidate not in present:
                    out.add(candidate)
    return sorted(out)


def main(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument("--count", action="store_true")
    args = parser.parse_args(argv)
    out = candidates()
    print(
        f"{len(HEADS)} heads, {len(out):,} candidates from the measured general endings",
        file=sys.stderr,
    )
    if args.count:
        return
    sys.stdout.write("\n".join(out))
    if out:
        sys.stdout.write("\n")


if __name__ == "__main__":
    main(sys.argv[1:])
