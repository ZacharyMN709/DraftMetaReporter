"""
Contains functions which handle colour string and colour combination manipulation.
"""

from typing import Optional
import re
import logging

from WUBRG.consts import WUBRG, COLOR_TO_NAME, COLOR_COMBINATIONS
from WUBRG.alias_mappings import ALIAS_MAP
from WUBRG.mana_symbols import MANA_SYMBOLS

mana_cost_re = re.compile(r'{(.*?)}')


def get_color_string(text: Optional[str]) -> str:
    """
    Takes in a string, and attempts to convert it to a color string.
    If the string is invalid, returns ''.
    This function will attempt to convert common names into their colours.
    Eg. 'Bant' -> 'WUG', 'bant' -> 'WUG'
    :param text: The string to convert.
    :return: A color string, which contains only characters found in 'WUBRG'.
    """

    # If the string is None, log a warning.
    if text is None:
        logging.warning(f"Invalid color string provided: `None`. Converting to ''.")
        return ''

    # Tidy the string to make matching to a color alias more forgiving.
    s = text.strip().title()
    if s in ALIAS_MAP:
        return ALIAS_MAP[s]

    # Get all the characters that are in WUBRG
    ret = ''.join(c for c in s.upper() if c in WUBRG)

    # If the return string is empty, log a warning message.
    if not ret:
        logging.warning(f"Invalid color string provided: {text}. No color values could be found in string.")

    return ret


def get_color_identity(text: str) -> str:
    """
    Takes in a color string, and attempts to convert it to a
    color identity string.
    :param text: The color string to convert.
    :return: A color identity string, a subset of 'WUBRG'.
    """
    color_string = get_color_string(text)
    char_set = set(color_string)
    return ''.join(c for c in WUBRG if c in char_set)


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
        return COLOR_TO_NAME[color_identity]


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
