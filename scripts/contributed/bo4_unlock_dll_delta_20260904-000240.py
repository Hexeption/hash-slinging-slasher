#!/usr/bin/env python3
"""Emit printable BO4 unlock-DLL labels absent from prior BO4 script corpora."""
from pathlib import Path
import importlib.util
import re

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('synergy', ROOT / 'contrib' / 'bo4_synergy_delta_labels_20260903.py')
synergy = importlib.util.module_from_spec(spec)
spec.loader.exec_module(synergy)
TOKEN = re.compile(r'[A-Za-z0-9_./-]{6,160}')


def values(text: str) -> set[str]:
    out = set()
    for raw in TOKEN.findall(text):
        name = synergy.labels.acceptable(raw.lower())
        if name:
            out.add(name)
    return out


def dll_values() -> tuple[set[str], set[str]]:
    dll = next((ROOT / 'borrowed' / 'Magic-Muffin-Bot-Bo4-Unlock-All').glob('*.dll'))
    data = dll.read_bytes()
    return values(data.decode('ascii', errors='ignore')), values(data.decode('utf-16le', errors='ignore'))


if __name__ == '__main__':
    prior_roots = ('bo4-source', 't8-src', 'BO4-BlackoutBots', 'bo4-lucy-menu', 'BO4-BlackOps4ShieldMenu', 'BlackoutBotsBO4', 'Abomination-Unofficial', 'Synergy-BO4-GSC-Menu', 't8-tests', 'Shield-Menu-BO4', 'bo4-pap-mod')
    prior = set()
    for directory in prior_roots:
        prior |= synergy.values(ROOT / 'borrowed' / directory)
    ascii_values, utf16_values = dll_values()
    # The ASCII part was independently confirmed in the preceding pass; only emit the distinct
    # UTF-16 metadata corpus, avoiding a replay under a new extractor fingerprint.
    print('\n'.join(sorted(utf16_values - prior - ascii_values)))
