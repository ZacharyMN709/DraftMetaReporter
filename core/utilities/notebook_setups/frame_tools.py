from core.utilities.notebook_setups.notebook_display import *
from core.utilities.notebook_setups.notebook_display import __imports as __sub_imports
from core.utilities.notebook_setups.notebook_display import set_up as sub_set_up

from core.utilities import logging
from core.data_fetching.utils import DATA_DIR_LOC, DATA_DIR_NAME

import core.wubrg
from core.game_metadata import Card, CardManager, SetMetadata, FormatMetadata
from core.data_fetching import DataLoader, LoadedData, DataFramer, FramedData, SetManager, CentralManager
from core.data_fetching.utils import get_name_slice, get_color_slice, get_date_slice, STAT_COL_NAMES, \
    rarity_filter, cmc_filter, card_color_filter, cast_color_filter, compose_filters, filter_frame, \
    tier_to_rank, rank_to_tier

from core.tier_list_analysis.TierList import TierList, TierAggregator


__imports = ['Card', 'CardManager', 'SetMetadata', 'FormatMetadata', 'SetManager', 'CentralManager',
             'get_name_slice', 'get_color_slice', 'get_date_slice',
             'rarity_filter', 'cmc_filter', 'card_color_filter', 'cast_color_filter',
             'compose_filters', 'filter_frame',
             'TierList', 'TierAggregator', 'tier_to_rank', 'rank_to_tier']
__funcs = ['set_up', 'info_splash', 'load_set_data']
__all__ = __imports + __funcs + __sub_imports


def info_splash() -> None:
    print(f"Data Root:           {DATA_DIR_LOC}")
    print(f"17 Lands Data Dir:   {DATA_DIR_NAME}")
    print()


def load_set_data(target_set=SETS[0], load_all=False) -> tuple[CentralManager, SetManager]:
    data_manager = None
    set_data = None

    start = datetime.utcnow()
    if load_all:
        print(f"Getting info for all sets...")
        if data_manager is None:
            data_manager = CentralManager()
            set_data = data_manager[target_set]
        data_manager.check_for_updates()
    else:
        print(f"Getting info for {target_set}...")
        if set_data is None:
            set_data = SetManager(target_set)
        set_data.check_for_updates()
    end = datetime.utcnow()
    logging.sparse(f"\n --- Data loaded in {end - start}.")

    return data_manager, set_data


def set_up(log_lvl=LogLvl.DEBUG, target_set=SETS[0], load_all=False) -> tuple[CentralManager, SetManager]:
    sub_set_up(log_lvl)
    info_splash()

    print("Loading Cards from cache...", end="")
    start = datetime.utcnow()
    CardManager.load_cache_from_file()
    end = datetime.utcnow()
    print(f"   Done!  ({end - start})")

    return load_set_data(target_set, load_all)
