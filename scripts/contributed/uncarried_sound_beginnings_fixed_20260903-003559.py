"""Probe high-frequency sound beginnings omitted by the measured prefix list."""
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
BEGINNINGS = (
    "bik_execution_", "grp_", "cac_wildcard_equip_", "duk_",
    "phy_impact_hard_", "phy_impact_metal_", "phy_impact_soft_", "chr_gib_",
    "vox_", "amb_", "foley_", "npc_", "weap_", "ui_", "streak_", "radio_",
)


def main():
    suffixes = [
        value.strip().lower().replace("\\", "/")
        for value in (ROOT / "data" / "sound.suffixes.txt").read_text().splitlines()
        if value.strip()
    ]
    out = {begin + suffix.lstrip("_") for begin in BEGINNINGS for suffix in suffixes}
    for value in sorted(out):
        print(value)
    print(
        f"{len(BEGINNINGS)} uncarried sound beginnings x {len(suffixes)} measured suffixes = {len(out)} candidates",
        file=sys.stderr,
    )


if __name__ == "__main__":
    main()
