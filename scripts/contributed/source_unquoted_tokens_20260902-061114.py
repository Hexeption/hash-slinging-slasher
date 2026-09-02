"""Extract asset-shaped tokens that occur outside strings and comments.

The retail source harvesters already cover quoted literals.  This deliberately targets the
different vocabulary channel used by bare identifiers, enum values, and path-like tokens in
decompiled source and data files.
"""
import argparse
import re
import sys
from pathlib import Path


EXTENSIONS = {
    '.ai_htn', '.cfg', '.csc', '.csv', '.ddl', '.gdb', '.graph', '.gsc', '.raw', '.txt', '.vision'
}
TOKEN = re.compile(r'[A-Za-z][A-Za-z0-9_./-]{5,159}')
LETTERS = re.compile(r'[A-Za-z]')
NOISE = {
    'default', 'include', 'namespace', 'return', 'true', 'false', 'self', 'undefined',
    'function', 'struct', 'string', 'vector', 'level', 'player', 'entity', 'script',
}
NOISE_PREFIXES = ('function_', 'hash_', 'var_', 'http_', 'https_')


def uncommented_code(text):
    # Replace comments and quoted strings with whitespace, retaining line boundaries.  This
    # prevents the method from rediscovering the already-tested quoted-literal corpus.
    pattern = re.compile(r'("(?:\\.|[^"\\])*"|/\*.*?\*/|//[^\r\n]*|#[^\r\n]*)', re.S)
    return pattern.sub(lambda match: ''.join('\n' if c == '\n' else ' ' for c in match.group()), text)


def plausible(value):
    value = value.lower()
    if value in NOISE or value.startswith(NOISE_PREFIXES):
        return False
    if '_' not in value and '/' not in value and '.' not in value:
        return False
    return len(LETTERS.findall(value)) >= 3


def main(argv):
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument('--root', required=True, help='retail source root')
    options = parser.parse_args(argv)
    root = Path(options.root)
    if not root.is_dir():
        raise SystemExit(f'source dump not found: {root}')

    names = set()
    files = 0
    for path in root.rglob('*'):
        if not path.is_file() or path.suffix.lower() not in EXTENSIONS:
            continue
        files += 1
        try:
            text = path.read_text(encoding='utf-8', errors='ignore')
        except OSError as error:
            print(f'skipping {path}: {error}', file=sys.stderr)
            continue
        for match in TOKEN.finditer(uncommented_code(text)):
            value = match.group().lower().strip('./-')
            if plausible(value):
                names.add(value)

    print(f'{files:,} source files -> {len(names):,} unquoted name-shaped tokens', file=sys.stderr)
    sys.stdout.write('\n'.join(sorted(names)))
    if names:
        sys.stdout.write('\n')


if __name__ == '__main__':
    main(sys.argv[1:])
