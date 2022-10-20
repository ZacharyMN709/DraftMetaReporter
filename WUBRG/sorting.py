"""
Contains sorting and filtering enums and functions.
"""

from enum import Flag, auto
from functools import cmp_to_key
from typing import Callable

from WUBRG.consts import COLOR_COMBINATIONS, GROUP_COLOR_COMBINATIONS
from WUBRG.funcs import get_color_identity, get_color_supersets, get_color_subsets


# region Color Sorting
# Creating a custom sorting algorithm to order in WUBRG order
# Maps colour groups to integers, so they can easily be used for sorting.
WUBRG_COLOR_INDEXES: dict[str, int] = {COLOR_COMBINATIONS[x]: x for x in range(0, len(COLOR_COMBINATIONS))}
GROUP_COLOR_INDEXES: dict[str, int] = {GROUP_COLOR_COMBINATIONS[x]: x for x in range(0, len(GROUP_COLOR_COMBINATIONS))}


def color_compare_wubrg(col1: str, col2: str) -> int:
    # Convert the colors into numeric indexes
    col_idx1 = WUBRG_COLOR_INDEXES[col1]
    col_idx2 = WUBRG_COLOR_INDEXES[col2]

    if col_idx1 < col_idx2:
        return -1
    else:
        return 1


# Creating a custom sorting algorithm to order in group order
def color_compare_group(col1: str, col2: str) -> int:
    # Convert the colors into numeric indexes
    col_idx1 = GROUP_COLOR_INDEXES[col1]
    col_idx2 = GROUP_COLOR_INDEXES[col2]

    if col_idx1 < col_idx2:
        return -1
    else:
        return 1


wubrg_compare_key: Callable = cmp_to_key(color_compare_wubrg)
group_compare_key: Callable = cmp_to_key(color_compare_group)
# endregion Color Sorting


# region Color Set Filtering and Sorting
# Color filtering enums.
class ColorSortStyles(Flag):
    exact = auto()
    subset = auto()
    contains = auto()
    superset = contains
    adjacent = auto()
    shares = auto()


def order_by_wubrg(color_list: list[str]) -> list[str]:
    return sorted(color_list, key=wubrg_compare_key)


def order_by_groups(color_list: list[str]) -> list[str]:
    return sorted(color_list, key=group_compare_key)


def exact(colors: str) -> list[str]:
    """
    Returns a list of colours that match the provided string. (Wraps the provided string in a list.)
    'exact': 'U' --> 'U'
    :param colors: A color string.
    :return: A list of color strings.
    """
    return [get_color_identity(colors)]


def subset(colors: str) -> list[str]:
    """
    Returns a list of the subsets of the provided colour string.
    'subset': 'UW' --> 'U', 'W', 'WU'
    :param colors: A color string.
    :return: A list of color strings.
    """
    return get_color_subsets(colors)


def superset(colors: str) -> list[str]:
    """
    Returns a list of the supersets of the provided colour string.
    'superset': 'UW' --> 'UW', 'UBW', 'URW', 'UGW'...
    :param colors: A color string.
    :return: A list of color strings.
    """
    return get_color_supersets(colors)


def adjacent(colors: str) -> list[str]:
    """
    Returns a list of color strings with no more than one colour different than the provided colour string.
    'adjacent': 'UW' --> 'U', 'W', 'UW', 'UG', 'WG', 'UWG'...
    :param colors: A color string.
    :return: A list of color strings.
    """
    _subset = get_color_subsets(colors, len(colors) - 1, True)
    _superset = get_color_supersets(colors, len(colors) + 1)
    return _subset + _superset


# noinspection SpellCheckingInspection
def shares(colors: str) -> list[str]:
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


def color_filter(colors: str, style: ColorSortStyles) -> list[str]:
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
