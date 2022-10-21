"""
This package helps simplify dealing with colours in Magic, by providing typing, constants, and functions
to handle common values, names and relationships surrounding colours and colour identity.
"""

from WUBRG.typing import COLOR_STRING, COLOR_IDENTITY, COLOR_ALIAS, COLOR_ALIAS_ALL, MANA_SYMBOL, VALID_COLOR_VALUE
from WUBRG.consts import WUBRG, FAILSAFE, COLORS, COLOR_COMBINATIONS, GROUP_COLOR_COMBINATIONS, COLOUR_GROUPINGS
from WUBRG.consts import COLOR_SINGLES, COLOR_PAIRS, COLOR_TRIPLES, COLOR_QUADRUPLES, NAME_TO_COLOR, COLOR_TO_NAME
from WUBRG.alias_mappings import ALIAS_MAP, GUILDS, ALLIED_GUILDS, ENEMY_GUILDS, WEDGES, SHARDS
from WUBRG.mana_symbols import MANA_SYMBOLS, BASE_MANA_SYMBOLS, NUMERIC_MANA_SYMBOLS, HYBRID_MANA_SYMBOLS
from WUBRG.funcs import get_color_string, get_color_identity, get_color_supersets, get_color_subsets
from WUBRG.funcs import get_color_alias, parse_cost
from WUBRG.sorting import ColorSortStyles, exact, subset, superset, adjacent, shares, color_filter
from WUBRG.sorting import order_by_wubrg, order_by_groups, color_compare_wubrg, color_compare_group
