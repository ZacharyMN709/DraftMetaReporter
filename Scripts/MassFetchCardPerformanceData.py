from datetime import datetime
from core.utilities import LogLvl, set_log_level, logging
from core.data_fetching import SetManager


TARGET_SET = 'BRO'
LOG_LEVEL = LogLvl.SPARSE
set_log_level(LOG_LEVEL)


def load_set_data():
    start = datetime.utcnow()
    set_data = SetManager(TARGET_SET)
    set_data.check_for_updates()
    end = datetime.utcnow()
    logging.sparse(f"\n --- Data loaded in {end - start}.")

    return set_data


def main():
    from core.game_metadata.game_objects.Card import CardManager
    CardManager.load_cache_from_file()
    load_set_data()


if __name__ == "__main__":
    main()
