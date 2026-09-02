"""Extract asset-shaped string values from retail source JSON bundles."""
import argparse
import re
import sys
from pathlib import Path

LITERAL = re.compile(r'"([A-Za-z0-9_./\\-]{6,160})"')
LETTERS = re.compile(r'[A-Za-z]')
NOISE_PREFIXES = ('function_', 'hash_', 'var_', 'http_', 'https_')


def plausible(value):
    value = value.lower()
    if value.startswith(NOISE_PREFIXES):
        return False
    if '_' not in value and '/' not in value and '\\' not in value:
        return False
    return len(LETTERS.findall(value)) >= 3


def main(argv):
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument('--root', required=True)
    options = parser.parse_args(argv)
    root = Path(options.root)
    if not root.is_dir():
        raise SystemExit(f'source dump not found: {root}')

    names = set()
    files = 0
    for path in root.rglob('*.json'):
        files += 1
        try:
            text = path.read_text(encoding='utf-8', errors='ignore')
        except OSError:
            continue
        for value in LITERAL.findall(text):
            if plausible(value):
                names.add(value.lower())

    print(f'{files:,} JSON files -> {len(names):,} name-shaped literals', file=sys.stderr)
    sys.stdout.write('\n'.join(sorted(names)))
    if names:
        sys.stdout.write('\n')


if __name__ == '__main__':
    main(sys.argv[1:])
