"""Extract explicit asset literals from text-like members of borrowed ZIP archives."""
from pathlib import Path
import re
import sys
import zipfile

ROOT = Path(__file__).resolve().parents[1]
EXTENSIONS = {".c", ".cc", ".cfg", ".cpp", ".csv", ".gsc", ".h", ".hpp", ".ini", ".json",
              ".js", ".lua", ".md", ".py", ".txt", ".ts", ".xml", ".yaml", ".yml"}
TOKEN = re.compile(r"(?<![A-Za-z0-9_])(?:[A-Za-z0-9$\[\]][A-Za-z0-9_$\[\]./\\:-]{4,220})(?![A-Za-z0-9_])")
PREFIXES = ("mc/", "wc/", "clt/", "splm/", "vd/", "mcs/", "ei/", "cltp/", "vdd/", "el/", "mcp/", "ec/",
            "i_", "mtl_", "xmodel_", "xanim_", "wpn_", "weapon_", "zm_", "mp_", "ui_", "snd_", "amb_")


def main():
    names = set()
    archives = members = 0
    for archive in (ROOT / "borrowed").rglob("*.zip"):
        try:
            with zipfile.ZipFile(archive) as bundle:
                archives += 1
                for info in bundle.infolist():
                    if Path(info.filename).suffix.lower() not in EXTENSIONS or info.file_size > 20_000_000:
                        continue
                    members += 1
                    try:
                        text = bundle.read(info).decode("utf-8", "ignore")
                    except (OSError, KeyError, RuntimeError, ValueError):
                        continue
                    for match in TOKEN.finditer(text):
                        value = match.group(0).strip("'\"`.,;()[]{}<>|\r\n\t").lower().replace("\\", "/")
                        if not any(value.startswith(prefix) for prefix in PREFIXES):
                            continue
                        if value.endswith(("/", ":")) or value.count("/") > 12:
                            continue
                        if sum(char.isalpha() for char in value) >= 3:
                            names.add(value)
        except (OSError, zipfile.BadZipFile):
            continue
    print(f"{archives:,} archives, {members:,} text members -> {len(names):,} literals", file=sys.stderr)
    for name in sorted(names):
        print(name)


if __name__ == "__main__":
    main()
