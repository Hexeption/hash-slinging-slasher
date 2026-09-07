"""Extract explicit CoD asset literals and filenames from the newly acquired weapon-pack source."""
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1] / "borrowed" / "Black-Ops-Trilogy-Weapon-Packs"
EXTENSIONS = {".c", ".cc", ".cfg", ".cpp", ".csv", ".gsc", ".h", ".hpp", ".ini", ".json",
              ".js", ".lua", ".md", ".py", ".txt", ".ts", ".xml", ".yaml", ".yml"}
TOKEN = re.compile(r"(?<![A-Za-z0-9_])(?:mc/|wc/|clt/|splm/|vd/|mcs/|ei/|cltp/|vdd/|el/|mcp/|ec/|i_|mtl_|xmodel_|xanim_|wpn_|weapon_|zm_|mp_|ui_|snd_|amb_|fx_)[A-Za-z0-9_$\[\]./\\:-]{4,220}(?![A-Za-z0-9_])", re.I)


def main():
    names = set()
    files = 0
    for path in ROOT.rglob("*"):
        if ".git" in path.parts:
            continue
        if not path.is_file():
            continue
        files += 1
        try:
            relative = path.relative_to(ROOT).as_posix().lower()
            if path.suffix.lower() in EXTENSIONS:
                text = path.read_text(encoding="utf-8", errors="ignore")
                values = [m.group(0) for m in TOKEN.finditer(text)]
            else:
                values = []
            values.append(relative)
        except OSError:
            continue
        for raw in values:
            value = raw.strip("'\"`.,;()[]{}<>|\r\n\t").lower().replace("\\", "/")
            if value.endswith(("/", ":")) or value.count("/") > 12:
                continue
            if any(value.startswith(prefix) for prefix in ("mc/", "wc/", "clt/", "splm/", "vd/", "mcs/", "ei/", "cltp/", "vdd/", "el/", "mcp/", "ec/", "i_", "mtl_", "xmodel_", "xanim_", "wpn_", "weapon_", "zm_", "mp_", "ui_", "snd_", "amb_", "fx_")) and sum(char.isalpha() for char in value) >= 3:
                names.add(value)
    print(f"{files:,} weapon-pack files -> {len(names):,} asset literals", file=sys.stderr)
    for name in sorted(names):
        print(name)


if __name__ == "__main__":
    main()
