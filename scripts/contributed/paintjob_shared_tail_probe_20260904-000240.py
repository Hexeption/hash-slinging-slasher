"""Probe shared-tail cells in the paintjob family using real observed axes."""
from collections import Counter
from pathlib import Path
import sys
import argparse

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import snapshot


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("head", nargs="?", default="paintjob")
    head = parser.parse_args().head.lower().rstrip("_") + "_"
    tables = ("fnv1a_xmaterials", "fnv1a_ximages", "fnv1a_xmodels", "fnv1a_xanims", "fnv1a_soundbanks_aliases", "fnv1a_xsounds")
    known = {n.strip().lower().replace("\\", "/") for t in tables for n in snapshot.table_names(t) if n.strip()}
    known |= {n.strip().lower().replace("\\", "/") for n in snapshot.confirmed_names() if n.strip()}
    observed = []
    for name in known:
        if not name.startswith(head) or "/" in name or "." in name:
            continue
        parts = name.split("_", 2)
        if len(parts) == 3 and parts[1] and parts[2]:
            observed.append((parts[1], parts[2]))
    axes = {axis for axis, _ in observed}
    tails = {tail for tail, count in Counter(tail for _, tail in observed).items() if count > 1}
    candidates = sorted({f"{head}{axis}_{tail}" for axis in axes for tail in tails} - known)
    print(f"{head} shared-tail grid: {len(axes):,} axes x {len(tails):,} tails = {len(candidates):,} candidates", file=sys.stderr)
    sys.stdout.write("\n".join(candidates))
    if candidates:
        sys.stdout.write("\n")


if __name__ == "__main__":
    main()
