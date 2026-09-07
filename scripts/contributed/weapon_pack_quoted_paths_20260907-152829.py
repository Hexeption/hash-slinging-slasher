"""Extract quoted slash-bearing source/config strings from the isolated weapon-pack corpus."""
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1] / "borrowed" / "Black-Ops-Trilogy-Weapon-Packs"
EXTENSIONS = {".c", ".cc", ".cfg", ".cpp", ".csv", ".gsc", ".h", ".hpp", ".ini", ".json",
              ".js", ".lua", ".md", ".py", ".txt", ".ts", ".xml", ".yaml", ".yml"}
QUOTED = re.compile(r"[\"']([^\"'\r\n]{3,240}/[^\"'\r\n]{2,240})[\"']")


def main():
    names = set()
    files = 0
    for path in ROOT.rglob("*"):
        if ".git" in path.parts or not path.is_file() or path.suffix.lower() not in EXTENSIONS:
            continue
        files += 1
        try:
            text = path.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            continue
        for match in QUOTED.finditer(text):
            value = match.group(1).strip().lower().replace("\\", "/")
            value = value.strip(".,;()[]{}<>|")
            if value.count("/") <= 12 and sum(char.isalpha() for char in value) >= 3:
                names.add(value)
    print(f"{files:,} source files -> {len(names):,} quoted slash strings", file=sys.stderr)
    for name in sorted(names):
        print(name)


if __name__ == "__main__":
    main()
