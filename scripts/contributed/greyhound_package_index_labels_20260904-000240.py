#!/usr/bin/env python3
"""Print exact FNV-1a labels from Greyhound's public package index.

The index is an external historical vocabulary, independent of the local
cod-name-db.  Its CSVs are ``hex_hash,label``; this keeps only the textual
label and lets confirm_list decide whether it names an unresolved CW or BO4
asset.  It intentionally performs no path, case, or punctuation edits.

Run from the repository root:
  python contrib/greyhound_package_index_labels_20260903.py | \
    bin/windows/confirm_list.exe - --game BLKOPS04 --label "Greyhound package-index exact labels" --script contrib/greyhound_package_index_labels_20260903.py

Reads: borrowed/GreyhoundPackageIndex/PackageIndexSources/FNV1A/*.csv
Writes: candidate labels to stdout.
"""

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / "borrowed" / "GreyhoundPackageIndex" / "PackageIndexSources" / "FNV1A"
FILES = (
    "fnv1a_xanims.csv",
    "fnv1a_ximages.csv",
    "fnv1a_xmaterials.csv",
    "fnv1a_xmodels.csv",
    "fnv1a_xsounds.csv",
)


def main() -> None:
    seen: set[str] = set()
    for filename in FILES:
        with (INDEX / filename).open("r", encoding="utf-8", errors="surrogateescape") as source:
            for line in source:
                _hash, separator, label = line.rstrip("\r\n").partition(",")
                if not separator or not label or label in seen:
                    continue
                seen.add(label)
                print(label)


if __name__ == "__main__":
    main()
