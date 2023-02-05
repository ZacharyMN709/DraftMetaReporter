# This is intended as a helper file which can be imported at the top of notebooks in this project to automatically
#  handle key imports, tune the notebook settings, and prints out cursory information about the default state.

import os
from os import path as path
import sys
from datetime import date, time, datetime, timedelta

import numpy as np
import pandas as pd
import seaborn as sns
from IPython.core.display import display, HTML

from core.utilities import LogLvl, set_log_level, logging
from core.game_metadata import SETS, FORMATS
from core.data_fetching.utils import get_next_17lands_update_time, get_prev_17lands_update_time

__imports = ['os', 'path', 'date', 'time', 'datetime', 'timedelta', 'np', 'pd', 'sns', 'LogLvl', 'SETS', 'FORMATS']
__funcs = ['set_up', 'info_splash', 'set_notebook_display']
__all__ = __imports + __funcs


def set_notebook_display() -> None:
    sns.set_theme()
    sns.set_color_codes()
    display(HTML("<style>.container { width:97% !important; }</style>"))


def info_splash() -> None:
    print(f"PYTHON VER:          {sys.version}")
    print(f"LOG LEVEL:           {logging.root.name} ({logging.root.level})")
    print()
    print(f'Available Sets:      {SETS}')
    print(f"Default Set:         {SETS[0]}")
    print()
    print(f'Available Formats:   {FORMATS}')
    print(f"Default Format:      {FORMATS[0]}")
    print()
    print(f"Current Local Time:  {datetime.now()}")
    print(f"Last 17Lands Update: {get_prev_17lands_update_time()}")
    print(f"Current UTC Time:    {datetime.utcnow()}")
    print(f"Next 17Lands Update: {get_next_17lands_update_time()}")
    print()


def set_up(log_lvl=LogLvl.DEBUG) -> None:
    set_log_level(log_lvl)
    set_notebook_display()
    info_splash()
