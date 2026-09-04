"""Extract asset-shaped ASCII literals from the installed COD26 executable.

    python contrib/cod26_executable_strings.py

Reads the installed ``cod26-cod.exe`` and writes no files; it emits unique path-like
asset strings to stdout for confirmation against the target snapshots.  This is a
one-off external-source probe, not a reusable name generator.
"""
import pathlib
import re
import sys

EXE = pathlib.Path(r"C:\Program Files (x86)\Call of Duty\_beta_\cod26-cod.exe")

# Keep this deliberately conservative: executable symbol/config strings are useful only
# when they resemble one of the six asset naming families, not arbitrary English text.
PATTERNS = [
    re.compile(rb"(?i)(?:[a-z0-9_.-]+[\\/])+[a-z0-9_.-]+\.(?:xmodel|xanim|material|image|snd|wav|mp3|flac|bnk)"),
    # Runtime lookups commonly use the extensionless asset name. Require both a path
    # separator and an underscore so ordinary URLs and library symbols stay out.
    re.compile(rb"(?i)(?:[a-z0-9_.-]+[\\/])+[a-z0-9_.-]*_[a-z0-9_.-]+"),
]


def main():
    if not EXE.exists():
        raise SystemExit(f"missing executable: {EXE}")
    data = EXE.read_bytes()
    found = set()
    for pattern in PATTERNS:
        for match in pattern.finditer(data):
            value = match.group().decode("ascii", "ignore")
            value = value.replace("\\", "/")
            if 8 <= len(value) <= 180:
                found.add(value)
    for value in sorted(found):
        print(value)
    print(f"cod26 executable: {len(data):,} bytes, {len(found):,} asset-shaped strings", file=sys.stderr)


if __name__ == "__main__":
    main()
