"""Harvest asset-shaped strings from a later installed CoD build's xpak metadata."""
import argparse
import re
import sys
from pathlib import Path

RUN = re.compile(rb'[\x20-\x7e]{4,}')
NAME = re.compile(rb'[A-Za-z0-9][A-Za-z0-9_/.-]{5,159}')
NOISE = re.compile(rb'([A-Za-z0-9])\1{3,}')


def plausible(value):
    return (b'_' in value or b'/' in value) and sum(c in b'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'
                                                    for c in value) >= 3 and not NOISE.search(value)


def main(argv):
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument('--root', required=True)
    parser.add_argument('--extension', default='.xpak', choices=('.xpak', '.fp'))
    options = parser.parse_args(argv)
    root = Path(options.root)
    names = set()
    files = 0
    for path in root.rglob('*' + options.extension):
        files += 1
        try:
            with path.open('rb') as handle:
                carry = b''
                while True:
                    block = handle.read(1 << 24)
                    if not block:
                        break
                    data = carry + block
                    for run in RUN.finditer(data):
                        for value in NAME.finditer(run.group()):
                            if plausible(value.group()):
                                names.add(value.group().decode('ascii').lower())
                    carry = data[-256:]
        except OSError as error:
            print(f'skipping {path}: {error}', file=sys.stderr)
    print(f'{files:,} {options.extension} files -> {len(names):,} asset-shaped strings', file=sys.stderr)
    sys.stdout.write('\n'.join(sorted(names)))
    if names:
        sys.stdout.write('\n')


if __name__ == '__main__':
    main(sys.argv[1:])
