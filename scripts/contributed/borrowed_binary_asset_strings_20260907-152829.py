"""Extract printable asset-shaped strings embedded in borrowed binary files."""
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
TEXT_EXTENSIONS = {".c", ".cc", ".cfg", ".cpp", ".csv", ".gsc", ".h", ".hpp", ".ini", ".json",
                   ".js", ".lua", ".md", ".py", ".txt", ".ts", ".xml", ".yaml", ".yml"}
TOKEN = re.compile(rb"(?<![A-Za-z0-9_])(?:mc/|wc/|clt/|splm/|vd/|mcs/|ei/|cltp/|vdd/|el/|mcp/|ec/|i_|mtl_|xmodel_|xanim_|wpn_|weapon_|zm_|mp_|ui_|snd_|amb_)[A-Za-z0-9_$\[\]./\\:-]{4,220}(?![A-Za-z0-9_])", re.I)


def main():
    names = set()
    files = 0
    for path in (ROOT / "borrowed").rglob("*"):
        if not path.is_file() or path.suffix.lower() in TEXT_EXTENSIONS:
            continue
        try:
            size = path.stat().st_size
            if size > 100_000_000:
                continue
            data = path.read_bytes()
        except OSError:
            continue
        files += 1
        for match in TOKEN.finditer(data):
            value = match.group(0).decode("ascii", "ignore").strip("'\"`.,;()[]{}<>|\r\n\t").lower().replace("\\", "/")
            if value.endswith(("/", ":")) or value.count("/") > 12:
                continue
            if sum(char.isalpha() for char in value) >= 3:
                names.add(value)
    print(f"{files:,} borrowed binary files -> {len(names):,} embedded literals", file=sys.stderr)
    for name in sorted(names):
        print(name)


if __name__ == "__main__":
    main()
