"""Probe xanim spellings for independently exported BO4 model basenames."""
import pathlib, sys
ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
import snapshot
def main():
    seeds = {x.strip().lower() for x in (ROOT / ".tmp-skye-bo4-models.candidates").read_text(encoding="utf-8").splitlines() if x.strip()}
    known = set(snapshot.table_names("fnv1a_xanims")) | set(snapshot.confirmed_names("anim"))
    out = {"xanim_" + x for x in seeds if "_" in x and "xanim_" + x not in known}
    print(f"{len(seeds):,} external model seeds, {len(out):,} xanim relabel candidates", file=sys.stderr)
    for x in sorted(out): print(x)
if __name__ == "__main__": main()
