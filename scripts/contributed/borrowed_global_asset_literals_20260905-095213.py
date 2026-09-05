"""Extract explicit asset-shaped literals from all borrowed text corpora.

This deliberately scans only text-like source/data files and only namespaces that the two
confirmers can plausibly hold. It is a cross-repository source probe, not a word recombination.
"""
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
BORROWED = ROOT / "borrowed"
TEXT_EXTENSIONS = {
    ".c", ".cc", ".cfg", ".cpp", ".csv", ".gsc", ".h", ".hpp", ".ini", ".json",
    ".js", ".lua", ".md", ".py", ".txt", ".ts", ".xml", ".yaml", ".yml",
}
TOKEN = re.compile(r"(?<![A-Za-z0-9_])(?:[A-Za-z0-9$\[\]][A-Za-z0-9_$\[\]./\\:-]{4,220})(?![A-Za-z0-9_])")
PREFIXES = (
    "mc/", "wc/", "clt/", "splm/", "vd/", "mcs/", "ei/", "cltp/", "vdd/", "el/", "mcp/", "ec/",
    "i_", "mtl_", "xmodel_", "xanim_", "wpn_", "weapon_", "zm_", "mp_", "ui_", "snd_", "amb_",
)


def main():
    names = set()
    files = 0
    for path in BORROWED.rglob("*"):
        if not path.is_file() or path.suffix.lower() not in TEXT_EXTENSIONS:
            continue
        try:
            if path.stat().st_size > 20_000_000:
                continue
            text = path.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            continue
        files += 1
        for match in TOKEN.finditer(text):
            value = match.group(0).strip("'\"`.,;()[]{}<>|\r\n\t").lower().replace("\\", "/")
            if not any(value.startswith(prefix) for prefix in PREFIXES):
                continue
            if value.endswith(("/", ":")) or value.count("/") > 12:
                continue
            if sum(char.isalpha() for char in value) < 3:
                continue
            names.add(value)
    print(f"{files:,} borrowed text files -> {len(names):,} asset-shaped literals", file=sys.stderr)
    for value in sorted(names):
        print(value)


if __name__ == "__main__":
    main()
