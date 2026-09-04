"""Put external source basenames into Cold War material directories and decorations."""
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parent.parent
CORPORA = (ROOT / "borrowed" / "bo4-lucy-menu", ROOT / "borrowed" / "t8-atian-menu")
EXTENSIONS = {".gsc", ".csc", ".cfg", ".csv", ".ddl", ".gdb", ".graph", ".raw", ".vision", ".txt", ".json", ".md", ".yml", ".yaml"}
TOKEN = re.compile(r"[A-Za-z0-9][A-Za-z0-9_./\\-]{5,159}")
PREFIXES = ("", "i_", "mtl_", "xmodel_", "xanim_")
SUFFIXES = ("", "_c", "_n", "_g", "_o", "_m", "_s", "_r")
DIRECTORIES = ("mc/", "wc/", "clt/", "splm/", "vd/", "mcs/", "ei/", "cltp/", "vdd/", "el/", "mcp/", "ec/")

names = set()
for corpus in CORPORA:
    if not corpus.is_dir():
        continue
    for path in corpus.rglob("*"):
        if path.is_file() and path.suffix.lower() in EXTENSIONS:
            try:
                body = path.read_text(encoding="utf-8", errors="ignore")
            except OSError:
                continue
            for match in TOKEN.finditer(body):
                value = match.group().lower().replace("\\", "/")
                base = value.rsplit("/", 1)[-1].rsplit(".", 1)[0]
                if len(base) >= 4 and "_" in base and sum(c.isalpha() for c in base) >= 3:
                    names.add(base)
names = sorted(names)[:3000]
for base in names:
    for directory in DIRECTORIES:
        for prefix in PREFIXES:
            for suffix in SUFFIXES:
                print(directory + prefix + base + suffix)
print(f"{len(names):,} external basenames x 12 directories x 5 prefixes x 8 suffixes", file=__import__("sys").stderr)
