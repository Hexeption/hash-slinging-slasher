"""CDL Cosmetics Generator: Call of Duty League stickers, emblems, and calling cards.

Generates systematic combinations of CDL teams, players, seasons, and platform variants
based on observed ground-truth patterns in confirmed Cold War store assets.
"""

import sys

SEASONS = ["s1", "s2", "s3", "s4", "s5", "s6", "cdl", "bps1", "bps2", "bps3", "bps4", "bps5", "bps6"]

PLATFORMS = ["ms", "pc", "sy"]

# Ground-truth team names observed in stickers and emblems
TEAMS_STICKER = [
    "empire", "faze", "guerrillas", "legion", "mutineers", "rokkr",
    "royalravens", "subliners", "surge", "thieves", "ultra", "optic"
]

TEAMS_EMBLEM = [
    "atlantafaze", "empire", "floridamutineers", "lagorrilas", "laguerrillas",
    "lathieves", "londonroyalravens", "newyorkemblem", "newyorksubliners",
    "opticchi", "opticchicago", "parislegion", "rokkrope", "minnesotarokkr",
    "surge", "seattlesurge", "torontoultra", "ultra", "faze", "mutineers",
    "guerrillas", "legion", "rokkr", "royalravens", "subliners", "thieves"
]

# 59 observed CDL players
PLAYERS = [
    ('empire', 'crimsix'), ('empire', 'felo'), ('empire', 'huke'), ('empire', 'illey'), ('empire', 'shotzzy'),
    ('faze', 'abezy'), ('faze', 'arcitys'), ('faze', 'cellium'), ('faze', 'sib'), ('faze', 'simp'),
    ('guerrillas', 'apathy'), ('guerrillas', 'assault'), ('guerrillas', 'cheen'), ('guerrillas', 'mental'), ('guerrillas', 'silly'),
    ('legion', 'aquaa'), ('legion', 'aqua'), ('legion', 'classic'), ('legion', 'fire'), ('legion', 'skrapz'), ('legion', 'theory'),
    ('mutineers', 'havok'), ('mutineers', 'neptune'), ('mutineers', 'owakening'), ('mutineers', 'skyz'), ('mutineers', 'slacked'),
    ('rokkr', 'accuracy'), ('rokkr', 'attach'), ('rokkr', 'majormaniak'), ('rokkr', 'priestahh'), ('rokkr', 'saintt'),
    ('royalravens', 'afro'), ('royalravens', 'alexx'), ('royalravens', 'dylan'), ('royalravens', 'parasite'), ('royalravens', 'seany'), ('royalravens', 'zer0'),
    ('subliners', 'asim'), ('subliners', 'clayster'), ('subliners', 'diamondcon'), ('subliners', 'hydra'), ('subliners', 'mack'), ('subliners', 'zoomaa'),
    ('surge', 'gunless'), ('surge', 'loony'), ('surge', 'nubzy'), ('surge', 'octane'), ('surge', 'prestinni'),
    ('thieves', 'drazah'), ('thieves', 'kenny'), ('thieves', 'slasher'), ('thieves', 'temp'), ('thieves', 'tjhaly'),
    ('ultra', 'bance'), ('ultra', 'cammy'), ('ultra', 'cleanx'), ('ultra', 'insight'), ('ultra', 'methodz'),
    ('optic', 'formal'), ('optic', 'scump'), ('optic', 'dashy'), ('optic', 'envoy')
]

def main():
    seen = set()

    def emit(name):
        n = name.strip().lower()
        if n and n not in seen:
            seen.add(n)
            sys.stdout.write(n + "\n")

    # 1. Player stickers: paintjob_stickers_<season>_<team>_<player>_base_<platform>_mtxitem
    for season in SEASONS:
        for team, player in PLAYERS:
            for plat in PLATFORMS:
                emit(f"paintjob_stickers_{season}_{team}_{player}_base_{plat}_mtxitem")
                emit(f"paintjob_stickers_{season}_{team}_{player}_{plat}_mtxitem")
            emit(f"paintjob_stickers_{season}_{team}_{player}_base_mtxitem")
            emit(f"paintjob_stickers_{season}_{team}_{player}_mtxitem")

    # 2. Team stickers: paintjob_stickers_<season>_<team>_base_<platform>_mtxitem
    for season in SEASONS:
        for team in TEAMS_STICKER:
            for plat in PLATFORMS:
                emit(f"paintjob_stickers_{season}_{team}_base_{plat}_mtxitem")
                emit(f"paintjob_stickers_{season}_{team}_{plat}_mtxitem")
            emit(f"paintjob_stickers_{season}_{team}_base_mtxitem")
            emit(f"paintjob_stickers_{season}_{team}_mtxitem")

    # 3. Emblems: emblems_<season>_<team>_base_<platform>_mtxitem
    for season in SEASONS:
        for team in TEAMS_EMBLEM:
            for plat in PLATFORMS:
                emit(f"emblems_{season}_{team}_base_{plat}_mtxitem")
                emit(f"emblems_{season}_{team}_{plat}_mtxitem")
            emit(f"emblems_{season}_{team}_base_mtxitem")
            emit(f"emblems_{season}_{team}_mtxitem")

    # 4. Calling cards: callingcards_<season>_<team>_base_<platform>_mtxitem
    for season in SEASONS:
        for team in TEAMS_EMBLEM:
            for plat in PLATFORMS:
                emit(f"callingcards_{season}_{team}_base_{plat}_mtxitem")
                emit(f"callingcards_{season}_{team}_{plat}_mtxitem")
            emit(f"callingcards_{season}_{team}_base_mtxitem")
            emit(f"callingcards_{season}_{team}_mtxitem")

    # 5. Non-season qualified variants
    for team, player in PLAYERS:
        for plat in PLATFORMS:
            emit(f"paintjob_stickers_{team}_{player}_base_{plat}_mtxitem")
        emit(f"paintjob_stickers_{team}_{player}_base_mtxitem")
        emit(f"paintjob_stickers_{team}_{player}_mtxitem")

    for team in TEAMS_EMBLEM:
        for plat in PLATFORMS:
            emit(f"emblems_{team}_base_{plat}_mtxitem")
            emit(f"callingcards_{team}_base_{plat}_mtxitem")
        emit(f"emblems_{team}_base_mtxitem")
        emit(f"emblems_{team}_mtxitem")
        emit(f"callingcards_{team}_base_mtxitem")
        emit(f"callingcards_{team}_mtxitem")

if __name__ == "__main__":
    main()
