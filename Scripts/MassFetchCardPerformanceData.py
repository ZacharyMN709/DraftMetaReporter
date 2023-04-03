from datetime import datetime
from core.utilities import LogLvl, set_log_level, logging
from core.data_fetching import SetManager
from core.game_metadata.game_objects.Card import CardManager


TARGET_SETS = ['SIR', 'ONE']
LOG_LEVEL = LogLvl.SPARSE
set_log_level(LOG_LEVEL)


def load_set_data(expansion: str):
    start = datetime.utcnow()
    logging.sparse(f"\n --- Loading metadata for {expansion}.")
    set_data = SetManager(expansion)
    logging.sparse(f"\n --- Getting data for {expansion}.")
    set_data.check_for_updates()
    end = datetime.utcnow()
    logging.sparse(f"\n --- Data loaded in {end - start}.")

    return set_data


def main():
    CardManager.load_cache_from_file()
    for s in TARGET_SETS:
        load_set_data(s)


if __name__ == "__main__":
    main()
