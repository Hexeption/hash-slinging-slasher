"""Hunt Black Ops 4 sound_asset (70,697 unnamed IDs) using backslashed cores and dotted tails.

Black Ops 4 sound names keep their backslashes and use no folding (hash of raw path).
Many BO4 sounds share cores with BO3 SAB and Cold War xsounds, but with BO4-specific
dotted tails (.ll100.pc.snd, .ln100.pc.snd, .rr75.pc.all.snd, etc.).
"""

import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent

LANGUAGES = {"en", "ru", "fr", "de", "it", "es", "pt", "pl", "ja", "ko", "zh", "cz", "ar"}

def split_tail(name):
    dot = name.find(".")
    return (name, "") if dot == -1 else (name[:dot], name[dot:])

def main():
    cores = set()
    tails = set()

    # 1. Read known BO4 sound assets for ground-truth tails and cores
    bo4_sound_path = ROOT / "all_names" / "blkops04" / "sound_asset.txt"
    if bo4_sound_path.exists():
        with bo4_sound_path.open(encoding="utf-8", errors="replace") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                name = line.split(",", 1)[1] if "," in line else line
                core, tail = split_tail(name.lower())
                if core:
                    cores.add(core)
                if tail:
                    tails.add(tail)

    # 2. Read BO3 SAB names
    bo3_path = ROOT / "cod-name-db" / "csv" / "bo3_sab.csv"
    if bo3_path.exists():
        with bo3_path.open(encoding="utf-8", errors="replace") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                name = line.split(",", 1)[1] if "," in line else line
                name = name.lower().replace("/", "\\")
                core, tail = split_tail(name)
                pieces = core.split("\\")
                if len(pieces) > 1 and pieces[0] in LANGUAGES:
                    pieces = pieces[1:]
                if pieces:
                    cores.add("\\".join(pieces))
                if tail:
                    tails.add(tail.lower())

    # 3. Read Cold War xsounds (many are ports of BO4 Blackout and MP audio)
    cw_sound_path = ROOT / "cod-name-db" / "csv" / "fnv1a_xsounds.csv"
    if cw_sound_path.exists():
        with cw_sound_path.open(encoding="utf-8", errors="replace") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                name = line.split(",", 1)[1] if "," in line else line
                # Convert forward slashes to BO4 backslashes
                name_bo4 = name.lower().replace("/", "\\")
                core, tail = split_tail(name_bo4)
                if core:
                    cores.add(core)
                if tail:
                    tails.add(tail)

    # Filter and normalize tails for BO4 (.pc.snd, .all.snd, etc.)
    valid_tails = set()
    for t in tails:
        if t.endswith(".snd") and "\\" not in t and t.count(".") <= 5 and len(t) <= 30:
            valid_tails.add(t)
            # Add 100/75 variations
            if "75" in t:
                valid_tails.add(t.replace("75", "100"))
            if "100" in t:
                valid_tails.add(t.replace("100", "75"))
            if ".all." in t:
                valid_tails.add(t.replace(".all.", ".en."))
            if ".en." in t:
                valid_tails.add(t.replace(".en.", ".all."))

    # Save lists
    cores_file = ROOT / "contrib" / "bo4_sound_hunter_cores.txt"
    tails_file = ROOT / "contrib" / "bo4_sound_hunter_tails.txt"
    plan_file = ROOT / "plans" / "bo4_sound_hunter.txt"

    cores_file.write_text("\n".join(sorted(cores)) + "\n", encoding="utf-8")
    tails_file.write_text("\n".join(sorted(valid_tails)) + "\n", encoding="utf-8")

    plan_content = f"""label: BO4 sound assets from cross-title cores and dotted tails
describe: hunting the 70,697 unnamed BO4 sound assets using unfolded backslashes
stem: @contrib/bo4_sound_hunter_cores.txt
end:  @contrib/bo4_sound_hunter_tails.txt
bare: yes
fold: no
"""
    plan_file.write_text(plan_content, encoding="utf-8")

    print(f"Extracted {len(cores):,} cores and {len(valid_tails):,} tails.")
    print(f"Total candidates: {len(cores) * len(valid_tails):,}")
    print(f"Plan written to {plan_file}")

if __name__ == "__main__":
    main()
