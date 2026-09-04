"""Cross rare-token-linked real heads and tails.

Unlike an unrestricted head/tail product, this keeps only pieces whose source names share a
non-generic token.  The shared token is a cheap semantic guard against arbitrary recombination.
"""
import argparse
import collections
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "scripts"))
import snapshot

TABLES = (
    "fnv1a_xmodels", "fnv1a_xmaterials", "fnv1a_ximages", "fnv1a_xanims",
    "fnv1a_soundbanks_aliases",
)


def names():
    out = set()
    for table in TABLES:
        out.update(n.strip().lower().replace("\\", "/") for n in snapshot.table_names(table))
    out.update(n.strip().lower().replace("\\", "/") for n in snapshot.confirmed_names())
    return {n for n in out if n}


def pieces(name):
    cuts = [i for i, c in enumerate(name) if c == "_"]
    return [(name[:i + 1], name[i:]) for i in cuts if i >= 2 and len(name[i:]) >= 3]


def main(argv):
    ap = argparse.ArgumentParser()
    ap.add_argument("--cap", type=int, default=2000000)
    ap.add_argument("--min-count", type=int, default=2)
    ap.add_argument("--max-count", type=int, default=24)
    args = ap.parse_args(argv)

    known = names()
    token_names = collections.defaultdict(list)
    token_heads = collections.defaultdict(set)
    token_tails = collections.defaultdict(set)
    for name in known:
        ps = pieces(name)
        for head, tail in ps:
            for token in set(name.replace("/", "_").split("_")):
                if len(token) >= 3:
                    token_heads[token].add(head)
                    token_tails[token].add(tail)
        for token in set(name.replace("/", "_").split("_")):
            if len(token) >= 3:
                token_names[token].append(name)

    candidates = set()
    eligible = 0
    for token, source_names in sorted(token_names.items()):
        if not args.min_count <= len(source_names) <= args.max_count:
            continue
        eligible += 1
        hs = token_heads[token]
        ts = token_tails[token]
        for head in hs:
            for tail in ts:
                candidate = head + tail
                if candidate not in known:
                    candidates.add(candidate)
                    if len(candidates) >= args.cap:
                        break
            if len(candidates) >= args.cap:
                break
        if len(candidates) >= args.cap:
            break

    print("known=%d eligible_tokens=%d candidates=%d" % (len(known), eligible, len(candidates)), file=sys.stderr)
    for candidate in sorted(candidates):
        print(candidate)


if __name__ == "__main__":
    main(sys.argv[1:])
