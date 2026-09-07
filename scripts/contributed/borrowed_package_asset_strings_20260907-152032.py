"""Extract asset-shaped strings from borrowed package/index binaries."""
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
EXTENSIONS = {".wni", ".bin", ".dat", ".ff", ".pak", ".idx", ".cache"}
TOKEN = re.compile(rb"(?<![A-Za-z0-9_])(?:mc/|wc/|clt/|splm/|vd/|mcs/|ei/|cltp/|vdd/|el/|mcp/|ec/|i_|mtl_|xmodel_|xanim_|xmaterial_|ximage_|wpn_|weapon_|model_|anim_|viewmodel_|zm_|mp_|ui_|snd_|sound_|amb_|fx_|veh_|char_)[A-Za-z0-9_$\[\]./\\:-]{4,220}(?![A-Za-z0-9_])", re.I)


def main():
    names = set()
    files = 0
    for path in (ROOT / "borrowed").rglob("*"):
        if not path.is_file() or path.suffix.lower() not in EXTENSIONS:
            continue
        try:
            if path.stat().st_size > 100_000_000:
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
    print(f"{files:,} package/index binaries -> {len(names):,} embedded literals", file=sys.stderr)
    for name in sorted(names):
        print(name)


if __name__ == "__main__":
    main()
