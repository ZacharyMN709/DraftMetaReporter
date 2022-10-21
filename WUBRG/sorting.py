"""
Contains sorting and filtering enums and functions.
"""

from enum import Flag, auto
from functools import cmp_to_key
from typing import Callable

from WUBRG.typing import COLOR_IDENTITY
from WUBRG.consts import COLOR_COMBINATIONS, GROUP_COLOR_COMBINATIONS
from WUBRG.funcs import get_color_identity, get_color_supersets, get_color_subsets


# region Color Sorting
# Maps colour groups to integers, so they can easily be used for sorting.
WUBRG_COLOR_INDEXES: dict[COLOR_IDENTITY, int] = \
    {COLOR_COMBINATIONS[x]: x for x in range(0, len(COLOR_COMBINATIONS))}
PENTAD_COLOR_INDEXES: dict[COLOR_IDENTITY, int] = \
    {GROUP_COLOR_COMBINATIONS[x]: x for x in range(0, len(GROUP_COLOR_COMBINATIONS))}


def index_dist_wubrg(col1: COLOR_IDENTITY, col2: COLOR_IDENTITY) -> int:
    """
    Compares two color identities and determines which comes first in "WUBRG" order.
    """
    # Convert the colors into numeric indexes
    col_idx1 = WUBRG_COLOR_INDEXES[col1]
    col_idx2 = WUBRG_COLOR_INDEXES[col2]

    return col_idx1 - col_idx2


def index_dist_pentad(col1: COLOR_IDENTITY, col2: COLOR_IDENTITY) -> int:
    """
    Compares two color identities and determines which comes first in "Pentad" order.
    """
    # Convert the colors into numeric indexes
    col_idx1 = PENTAD_COLOR_INDEXES[col1]
    col_idx2 = PENTAD_COLOR_INDEXES[col2]

    return col_idx1 - col_idx2


wubrg_compare_key: Callable = cmp_to_key(index_dist_wubrg)
pentad_compare_key: Callable = cmp_to_key(index_dist_pentad)
# endregion Color Sorting


# region Colour Filtering
class ColorSortStyles(Flag):
    """
    Different relations applicable to two colour identities.
    """
    exact = auto()
    subset = auto()
    contains = auto()
    superset = contains
    adjacent = auto()
    shares = auto()


def order_by_wubrg(color_list: list[COLOR_IDENTITY]) -> list[COLOR_IDENTITY]:
    """
    Take a list and orders it in WUBRG order.
    :param color_list: The list to sort.
    :return: The sorted list.
    """
    return sorted(color_list, key=wubrg_compare_key)


def order_by_pentad(color_list: list[COLOR_IDENTITY]) -> list[COLOR_IDENTITY]:
    """
    Take a list and orders it in Pentad order.
    :param color_list: The list to sort.
    :return: The sorted list.
    """
    return sorted(color_list, key=pentad_compare_key)


def exact(colors: COLOR_IDENTITY) -> list[COLOR_IDENTITY]:
    """
    Returns a list of colours that match the provided string. (Wraps the provided string in a list.)
    'exact': 'U' --> 'U'
    :param colors: A color string.
    :return: A list of color strings.
    """
    return [get_color_identity(colors)]


def subset(colors: COLOR_IDENTITY) -> list[COLOR_IDENTITY]:
    """
    Returns a list of the subsets of the provided colour string.
    'subset': 'UW' --> 'U', 'W', 'WU'
    :param colors: A color string.
    :return: A list of color strings.
    """
    return get_color_subsets(colors)


def superset(colors: COLOR_IDENTITY) -> list[COLOR_IDENTITY]:
    """
    Returns a list of the supersets of the provided colour string.
    'superset': 'UW' --> 'UW', 'UBW', 'URW', 'UGW'...
    :param colors: A color string.
    :return: A list of color strings.
    """
    return get_color_supersets(colors)


def adjacent(colors: COLOR_IDENTITY) -> list[COLOR_IDENTITY]:
    """
    Returns a list of color strings with no more than one colour different than the provided colour string.
    'adjacent': 'UW' --> 'U', 'W', 'UW', 'UG', 'WG', 'UWG'...
    :param colors: A color string.
    :return: A list of color strings.
    """
    _subset = get_color_subsets(colors, len(colors) - 1, True)
    _superset = get_color_supersets(colors, len(colors) + 1)
    return _subset + _superset


def shares(colors: COLOR_IDENTITY) -> list[COLOR_IDENTITY]:
    # noinspection SpellCheckingInspection
    """
    Returns a list of color strings which share any colour with the provided colour string.
    'adjacent': 'UW' --> 'U', 'W', 'UW', 'UG', 'UWG', 'UWRG', 'WUBRG'...
    :param colors: A color string.
    :return: A list of color strings.
    """

    if colors == '':
        return ['']

    shared = set()
    for color in colors:
        shared = shared.union(set(get_color_supersets(color)))
    return order_by_wubrg(shared)


def color_filter(colors: COLOR_IDENTITY, style: ColorSortStyles) -> list[COLOR_IDENTITY]:
    """
    Returns a list of color strings based on the provided colour string and filter.
    :param colors: A color string.
    :param style: The style of filter to apply.
    :return: A list of color strings.
    """
    # Map each of the enumeration values to a sort function.
    funcs = {
        ColorSortStyles.exact: exact,
        ColorSortStyles.subset: subset,
        ColorSortStyles.contains: superset,
        ColorSortStyles.superset: superset,
        ColorSortStyles.adjacent: adjacent,
        ColorSortStyles.shares: shares
    }

    # Verify that the provided filter value is valid.
    if style not in funcs:
        raise ValueError(f"`style` must be one of `ColorSortStyles` enums")

    # Return a function, based on the provided filter value.
    return funcs[style](get_color_identity(colors))
# endregion Colour Filtering
