"""
This package helps simplify logging, handling data types, and json files.
"""

from utilities.funcs import *
from utilities.auto_logging import *


from_funcs = ['flatten_lists', 'load_json_file', 'save_json_file']

from_auto_logging = ['LogLvl', 'set_log_level', 'auto_log', 'logging']


__all__ = from_funcs + from_auto_logging
