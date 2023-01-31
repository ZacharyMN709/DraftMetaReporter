"""
This package helps simplify dealing with colours in Magic, by providing typing, constants, and functions
to handle common values, names and relationships surrounding colours and colour identity.
"""

from core.wubrg.typing import *
from core.wubrg.consts import *
from core.wubrg.alias_mappings import *
from core.wubrg.mana_symbols import *
from core.wubrg.funcs import *
from core.wubrg.sorting import *


from_typing = ['COLOR', 'COLOR_IDENTITY', 'COLOR_STRING', 'SPLASH_STRING', 'FORMATTED_MANA_SYMBOL', 'MANA_SYMBOL',
               'COLOR_ALIAS', 'COLOR_ALIAS_EXTENDED', 'COLOR_ALIAS_ALL', 'VALID_COLOR_VALUE']

from_consts = ['WUBRG', 'COLOR_COMBINATIONS', 'COLOR_SINGLES', 'COLOR_PAIRS', 'COLOR_TRIPLES', 'COLOR_QUADRUPLES',
               'NAME_TO_COLOR', 'COLOR_TO_NAME', 'COLOUR_GROUPINGS']

from_alias_mappings = ['ALIAS_MAP', 'GROUPED_ALIAS_MAP']

from_mana_symbols = ['FORMATTED_MANA_SYMBOLS', 'MANA_SYMBOLS']

from_funcs = ['is_color_string', 'get_color_string', 'get_color_identity', 'parse_color_list', 'get_color_alias',
              'parse_cost', 'calculate_cmc', 'get_color_supersets', 'get_color_subsets']

from_sorting = ['wubrg_compare_key', 'pentad_compare_key', 'ColorSortStyles', 'color_filter']


__all__ = from_typing + from_consts + from_alias_mappings + from_mana_symbols + from_funcs + from_sorting
