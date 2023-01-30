"""
This package helps simplify dealing with the the data surrounding Cards and Drafts.
"""

from data_fetching.utils import *
from data_fetching.DataLoader import *
from data_fetching.LoadedData import *
from data_fetching.DataFramer import *
from data_fetching.FramedData import *
from data_fetching.SetManager import *

# Explicitly masking the name of the file.
from data_fetching.DataLoader import DataLoader as DataLoader
from data_fetching.LoadedData import LoadedData as LoadedData
from data_fetching.DataFramer import DataFramer as DataFramer
from data_fetching.FramedData import FramedData as FramedData
from data_fetching.SetManager import SetManager as SetManager


from_utils = ['FORMAT_NICKNAME_DICT', 'STAT_FORMAT_STRINGS',
              'PERCENT_COLUMNS', 'STAT_COL_NAMES', 'SHARED_COL_NAMES', 'CARD_INFO_COL_NAMES',
              'utc_today', 'get_prev_17lands_update_time', 'get_next_17lands_update_time',
              'rarity_filter', 'cmc_filter', 'card_color_filter', 'cast_color_filter', 'compose_filters',
              'get_name_slice', 'get_color_slice', 'get_date_slice']

from_data_loader = ['DataLoader']

from_loaded_data = ['LoadedData']

from_data_framer = ['DataFramer']

from_framed_data = ['FramedData']

from_set_manager = ['SetManager']

__all__ = from_utils + from_data_loader + from_loaded_data + from_data_framer + from_framed_data + from_set_manager
