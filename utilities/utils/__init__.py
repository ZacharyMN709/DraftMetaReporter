"""
This package wraps simple functions and globally required constants.
"""

from utilities.utils.funcs import *
from utilities.utils.settings import *


from_funcs = ['ENCODING', 'DATA_DIR_NAME', 'DATA_DIR_LOC']

from_settings = ['flatten_lists', 'load_json_file', 'save_json_file']


__all__ = from_funcs + from_settings
