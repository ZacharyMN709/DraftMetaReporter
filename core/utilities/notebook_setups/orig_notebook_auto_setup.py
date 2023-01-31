# This is intended as a helper file which can be imported at the top of notebooks in this project to automatically
#  handle key imports, tune the notebook settings, and prints out cursory information about the default state.

import sys
import datetime
from datetime import datetime
import seaborn as sns
from IPython.core.display import display, HTML

from core.utilities import LogLvl, set_log_level, logging

from core.game_metadata import SETS
from core.data_fetching import SetManager, CentralManager
from core.data_fetching.utils import get_next_17lands_update_time, get_prev_17lands_update_time


def set_notebook_display() -> None:
    sns.set_theme()
    sns.set_color_codes()
    display(HTML("<style>.container { width:95% !important; }</style>"))


def info_splash() -> None:
    print(f"PYTHON VER:          {sys.version}")
    print(f"LOG LEVEL:           {logging.root.name} ({logging.root.level})")
    print()
    print(f'Available sets:      {SETS}')
    print(f"Default Set:         {SETS[0]}")
    print()
    print(f"Current Local Time:  {datetime.now()}")
    print(f"Last 17Lands Update: {get_prev_17lands_update_time()}")
    print(f"Current UTC Time:    {datetime.utcnow()}")
    print(f"Next 17Lands Update: {get_next_17lands_update_time()}")


def load_set_data(target_set=SETS[0], load_all=False) -> tuple[CentralManager, SetManager]:
    data_manager = None
    set_data = None

    start = datetime.utcnow()
    if load_all:
        if data_manager is None:
            data_manager = CentralManager()
            set_data = data_manager[target_set]
        data_manager.check_for_updates()
    else:
        if set_data is None:
            set_data = SetManager(target_set)
        set_data.check_for_updates()
    end = datetime.utcnow()
    logging.sparse(f"\n --- Data loaded in {end - start}.")

    return data_manager, set_data


def notebook_set_up(log_lvl=LogLvl.DEBUG):
    set_log_level(log_lvl)
    set_notebook_display()
    info_splash()
