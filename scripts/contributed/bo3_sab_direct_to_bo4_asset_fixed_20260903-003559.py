"""Corrected direct BO3 SAB cores respelled with BO4 literal-backslash tails."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
TAILS = ("ln100.pc.snd", "ll100.pc.snd", "sn100.pc.snd", "sl100.pc.snd", "pn100.pc.snd", "pl100.pc.snd")
LANG = {"en", "ru", "fr", "de", "it", "es", "pt", "pl", "ja", "ko", "zh", "cz", "ar"}


def main():
    seen = set()
    source = ROOT / "cod-name-db" / "csv" / "bo3_sab.csv"
    for line in source.read_text(encoding="utf-8", errors="replace").splitlines():
        _, sep, name = line.partition(",")
        if not sep:
            continue
        parts = name.strip().lower().replace("/", "\\").split(".", 1)[0].split("\\")
        if parts and parts[0] in LANG:
            parts = parts[1:]
        if parts:
            seen.add("\\".join(parts))
    for core in sorted(seen):
        for tail in TAILS:
            print(core + "." + tail)
    print(f"{len(seen)} BO3 cores, {len(seen) * len(TAILS)} candidates", file=__import__("sys").stderr)


if __name__ == "__main__":
    main()
