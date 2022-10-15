from functools import cmp_to_key
from typing import Optional, Callable
import re

from Utilities.auto_logging import logging
from WUBRG.consts import WUBRG, FAILSAFE, ALL_COLOR_ALIAS_MAP, COLOR_COMBINATIONS, REVERSE_COLOR_MAP, MANA_SYMBOLS, \
    WUBRG_COLOR_INDEXES, GROUP_COLOR_INDEXES, ColorSortStyles

mana_cost_re = re.compile(r'{(.*?)}')


def get_color_string(s: Optional[str]) -> str:
    """
    Takes in a string, and attempts to convert it to a color string.
    If the string is invalid, returns ''.
    This function will attempt to convert common names into their colours.
    Eg. 'Bant' -> 'WUG'
    :param s: The string to convert.
    :return: A color string, which contains only characters found in 'WUBRG'.
    """
    if s is None:
        logging.warning(f"Invalid color string provided: `None`. Converting to '{FAILSAFE}'")
        return FAILSAFE

    s = s.strip()
    s = re.sub('[0-9{}]', '', s)

    # If the colour name exists in the color alias dictionary,
    if s.title() in ALL_COLOR_ALIAS_MAP:
        # Return the string provided by the alias dictionary.
        return ALL_COLOR_ALIAS_MAP[s.title()]

    # For each character in the upper-case input,
    ret = ''
    for c in s.upper():
        # If it's one of the colours,
        if c in WUBRG:
            # Add it to the string.
            ret += c

    # If the return string is empty, log a warning message.
    if not ret:
        logging.warning(f"Invalid color string provided: {s}. Converting to '{FAILSAFE}'")
        return FAILSAFE
    # Otherwise, return the generated string.
    else:
        return ret


def get_color_identity(color_string: str) -> str:
    """
    Takes in a color string, and attempts to convert it to a
    color identity string.
    :param color_string: The color string to convert.
    :return: A color identity string, a subset of 'WUBRG'.
    """
    char_set = set(get_color_string(color_string))
    s = ''
    for c in WUBRG:
        if c in char_set:
            s += c
    return s


def get_color_alias(color_string: str) -> Optional[str]:
    """
    Takes in a colour string and attempts to return a more
    common name for the colors. e.g. 'WUR' -> 'Jeskai'
    :param color_string: The color string to convert.
    :return: A common name which represents the colours in color_string, or None.
    """
    color_identity = get_color_identity(color_string)
    if color_identity == '':
        return None
    else:
        return REVERSE_COLOR_MAP[color_identity]


def get_color_supersets(color_id: str, max_len: int = 5, strict: bool = False) -> list[str]:
    """
    Gets all possible permutations of WUBRG which contain the color_id.
    Can limit the length of the permutations returned with max_len.
    :param color_id: The colours to look for in the permutations.
    :param max_len: The max length of the permutations. Default: 5
    :param strict: Whether the subset should be strict. Default: False
    :return: A list of color ids.
    """
    color_ids = list()
    color_id = get_color_identity(color_id)
    cis = set(color_id)
    for c in COLOR_COMBINATIONS:
        if len(c) <= max_len and cis <= set(c):
            color_ids.append(c)

    if strict:
        color_ids.remove(color_id)

    return color_ids


def get_color_subsets(color_id: str, min_len: int = 0, strict: bool = False) -> list[str]:
    """
    Gets all possible permutations of WUBRG which are contained in color_id.
    Can limit the length of the permutations returned with min_len.
    :param color_id: The colours to look for in the permutations.
    :param min_len: The min length of the permutations. Default: 0
    :param strict: Whether the subset should be strict. Default: False
    :return: A list of color ids.
    """
    color_ids = list()
    color_id = get_color_identity(color_id)
    cis = set(color_id)
    for c in COLOR_COMBINATIONS:
        if len(c) >= min_len and cis >= set(c):
            color_ids.append(c)

    if strict:
        color_ids.remove(color_id)

    return color_ids


def parse_cost(mana_cost: str) -> list[str]:
    """
    Converts the typically used mana cost to a list of strings to more easily iterate over.
    Eg. {10}{G}{G} would return ['10', 'G', 'G']
    :param mana_cost: A mana cost, in the form of {W}{U}{B}{R}{G}.
    :return: A list of mana symbols as strings.
    """
    sym_left = '{'
    sym_right = '}'
    default = ['A']

    # If the parenthesis don't match, return a dummy value.
    if mana_cost.count(sym_left) != mana_cost.count(sym_right):
        return default

    # Find anything like {.} in the string,
    costs = mana_cost_re.findall(mana_cost)
    # And for the contents of each element,
    for cost in costs:
        # Make sure it is a valid mana symbol.
        if cost not in MANA_SYMBOLS:
            # If not, return a dummy value.
            logging.warning(f"Invalid mana cost provided: {mana_cost}. Converting to '{default}'")
            return default

    # If all checks passed, return the found values.
    return costs


# Creating a custom sorting algorithm to order in WUBRG order
def color_compare_wubrg(col1: str, col2: str) -> int:
    # Convert the colors into numeric indexes
    col_idx1 = WUBRG_COLOR_INDEXES[col1]
    col_idx2 = WUBRG_COLOR_INDEXES[col2]

    if col_idx1 < col_idx2:
        return -1
    else:
        return 1


def list_color_dict(d: dict[str, str]) -> list[str]:
    return [d[s] for s in d]


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


# region Color Set Filtering and Sorting
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
# endregion Color Set Filtering
