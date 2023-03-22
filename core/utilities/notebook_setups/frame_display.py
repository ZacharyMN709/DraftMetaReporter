from core.utilities.notebook_setups.frame_tools import *
from core.utilities.notebook_setups.frame_tools import __imports as __sub_imports
from core.utilities.notebook_setups.frame_tools import set_up as sub_set_up

import dataframe_image as dfi
from scipy.stats import norm
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

# TODO: Make this and the other setup functions use an abstract base class, and layer
#  each version on top  of the previous.
from core.utilities.auto_logging import LogLvl, set_log_level, logging

__imports = []
__funcs = []
__all__ = __imports + __funcs + __sub_imports


def info_splash() -> None:
    pass


def set_up(log_lvl=LogLvl.DEBUG, target_set=SETS[0], load_all=False) -> tuple[CentralManager, SetManager]:
    _main, _set = sub_set_up(log_lvl, target_set, load_all)
    info_splash()
    return _main, _set
