import logging

from core.utilities.auto_logging import LogLvl, auto_log
from core.game_metadata.game_objects.Card import CardManager

NEXT_SET = "MKM"
EXTRA_SETS = [NEXT_SET, "PLST", "SPG", "WOT", "MUL", "SIS", "BRR", "STA"]
# TODO: Handle the list and special guest cards more elegantly, by which I likely mean separately.


def refresh_scryfall_caches():
    logging.sparse("Generating caches...")
    CardManager.generate_cache_file()
    logging.sparse("  Full cache re-generated.")
    CardManager.generate_arena_cache_file(EXTRA_SETS)
    logging.sparse("  Arena cache re-generated.")
    logging.sparse("Finished generating caches!")


if __name__ == "__main__":
    auto_log(LogLvl.VERBOSE)
    refresh_scryfall_caches()
