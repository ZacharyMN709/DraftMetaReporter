# This is intended as a helper file which can be imported at the top of notebooks in this project to automatically
#  handle key imports, tune the notebook settings, and prints out cursory information about the default state.

from IPython.core.display import display, HTML
import sys
import os
from os import path
from datetime import date, time, datetime, timedelta
import numpy as np
import pandas as pd
import dataframe_image as dfi
from scipy.stats import norm
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import seaborn as sns

from Utilities.auto_logging import LogLvl, set_log_level, logging
import WUBRG
from WUBRG import get_color_identity, list_color_dict

from game_metadata import SETS, FORMATS
from game_metadata import Card, CardManager, SetMetadata, FormatMetadata
from data_fetching import DataLoader, LoadedData, DataFramer, FramedData, SetManager, CentralManager
from data_fetching.utils import get_next_17lands_update_time, get_prev_17lands_update_time, \
    get_name_slice, get_color_slice, get_date_slice, STAT_COL_NAMES, \
    rarity_filter, cmc_filter, card_color_filter, cast_color_filter, compose_filters


LOAD_ALL = False
TRGT_SET = 'DMU'
LOG_LEVEL = LogLvl.INFO
set_log_level(LOG_LEVEL)


def set_notebook_display():
    sns.set_theme()
    sns.set_color_codes()
    display(HTML("<style>.container { width:95% !important; }</style>"))


def info_splash():
    print(f"PYTHON VER:          {sys.version}")
    print(f"LOAD_ALL:            {LOAD_ALL}")
    print(f"TRGT_SET:            {TRGT_SET}")
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
            set_data = data_manager[TRGT_SET]
        data_manager.check_for_updates()
    else:
        if set_data is None:
            set_data = SetManager(TRGT_SET)
        set_data.check_for_updates()
    end = datetime.utcnow()
    logging.sparse(f"\n --- Data loaded in {end - start}.")

    return data_manager, set_data


# When this module is loaded, run these functions, as the assumption is this module automatically sets up a notebook.
set_notebook_display()
info_splash()
