"""Translate independent Skye BO4 xmodel export labels into image/material spellings."""
import pathlib, sys
ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
import snapshot

def main():
    models = set(n.strip().lower() for n in snapshot.table_names("fnv1a_xmodels"))
    models |= set(n.strip().lower() for n in snapshot.confirmed_names("model"))
    # External export labels are supplied as a fixed, provenance-backed seed file.
    seeds = set()
    for line in (ROOT / ".tmp-skye-bo4-models.candidates").read_text(encoding="utf-8").splitlines():
        n = line.strip().lower()
        if n and "_" in n and not n.startswith("ximage_"):
            seeds.add(n)
    known = set()
    for t in ("fnv1a_ximages", "fnv1a_xmaterials"):
        known |= set(n.strip().lower() for n in snapshot.table_names(t))
    for p in ("image", "material"):
        known |= set(n.strip().lower() for n in snapshot.confirmed_names(p))
    out = {prefix + n for n in seeds for prefix in ("i_", "mtl_") if prefix + n not in known}
    print(f"{len(seeds):,} external xmodel seeds, {len(out):,} cross-type candidates", file=sys.stderr)
    for n in sorted(out): print(n)
if __name__ == "__main__": main()
