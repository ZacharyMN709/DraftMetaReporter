import sys
from datetime import datetime

from Utilities.auto_logging import LogLvl, set_log_level, logging

from game_metadata import SETS
from data_fetching import SetManager, CentralManager
from data_fetching.utils import get_next_17lands_update_time, get_prev_17lands_update_time

LOAD_ALL = False
TARGET_SET = 'DMU'
LOG_LEVEL = LogLvl.INFO
set_log_level(LOG_LEVEL)


def info_splash():
    print(f"PYTHON VER:          {sys.version}")
    print(f"LOAD_ALL:            {LOAD_ALL}")
    print(f"TARGET_SET:          {TARGET_SET}")
    print(f"LOG LEVEL:           {LOG_LEVEL.name} ({LOG_LEVEL})")
    print()
    print(f'Available sets:      {SETS}')
    print()
    print(f"Current Local Time:  {datetime.now()}")
    print(f"Last 17Lands Update: {get_prev_17lands_update_time()}")
    print(f"Current UTC Time:    {datetime.utcnow()}")
    print(f"Next 17Lands Update: {get_next_17lands_update_time()}")


def load_set_data():
    data_manager = None
    set_data = None

    start = datetime.utcnow()
    if LOAD_ALL:
        if data_manager is None:
            data_manager = CentralManager()
            set_data = data_manager[TARGET_SET]
        data_manager.check_for_updates()
    else:
        if set_data is None:
            set_data = SetManager(TARGET_SET)
        set_data.check_for_updates()
    end = datetime.utcnow()
    logging.sparse(f"\n --- Data loaded in {end - start}.")

    return data_manager, set_data


def main():
    info_splash()
    load_set_data()


if __name__ == "__main__":
    main()
