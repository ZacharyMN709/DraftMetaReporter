from typing import Optional
import re
from WUBRG.consts import COLORS, COLOR_ALIASES, COLOR_COMBINATIONS, COLOR_COMBINATION_TO_ALIAS, MANA_SYMBOLS


def get_color_string(s: str) -> str:
    """
    Takes in a string, and attempts to convert it to a color string.
    If the string is invalid, returns ''.
    This function will attempt to convert common names into their colours.
    Eg. 'Bant' -> 'WUG'
    :param s: The string to convert.
    :return: A color string, which contains only characters found in 'WUBRG'.
    """
    if s.title() in COLOR_ALIASES:
        # Return the string provided by the alias dictionary.
        return COLOR_ALIASES[s.title()]
    else:
        # Validate the string by using the set difference
        if set(s.upper()) > set(COLORS):
            # If the string isn't a subset of 'WUBRG', the string is invalid.
            print(f"Invalid color string provided: {s}. Converting to ''")
            return ''
        else:
            # Otherwise, the string is valid. Return it.
            return s.upper()


def get_color_identity(color_string: str) -> str:
    """
    Takes in a color string, and attempts to convert it to a
    color identity string.
    :param color_string: The color string to convert.
    :return: A color identity string, a subset of 'WUBRG'.
    """
    char_set = set(get_color_string(color_string))
    s = ''
    for c in COLORS:
        if c in char_set:
            s += c
    return s


def get_color_alias(color_string: str) -> Optional[str]:
    """
    Takes in a colour string and attempts to return a more
    common name for the colors. Eg. 'WUR' -> 'Jeskai'
    :param color_string: The color string to convert.
    :return: A common name which represents the colours in color_string, or None.
    """
    color_identity = get_color_identity(color_string)
    if color_identity in COLOR_COMBINATION_TO_ALIAS:
        return COLOR_COMBINATION_TO_ALIAS[color_identity]
    else:
        return None


def get_color_supersets(color_id: str, max_len: int = 5, strict: bool = False) -> list[str]:
    """
    Gets all possible permutations of WUBRG which contain the color_id.
    Can limit the length of the permutations returned with l.
    :param color_id: The colours to look for in the permutations.
    :param max_len: The max length of the permutations. Default: 5
    :param strict: Whether the subset should be strict
    :return: A list of color ids.
    """
    color_ids = list()

    cis = set(get_color_identity(color_id))
    for c in COLOR_COMBINATIONS:
        if strict:
            if len(c) < max_len and cis < set(c):
                color_ids.append(c)
        else:
            if len(c) <= max_len and cis <= set(c):
                color_ids.append(c)

    return color_ids


def get_color_subsets(color_id: str, min_len: int = 0, strict: bool = False) -> list[str]:
    """
    Gets all possible permutations of WUBRG which are contained in color_id.
    Can limit the length of the permutations returned with l.
    :param color_id: The colours to look for in the permutations.
    :param min_len: The min length of the permutations. Default: 0
    :param strict: Whether the subset should be strict
    :return: A list of color ids.
    """
    colour_ids = list()

    cis = set(get_color_identity(color_id))
    for c in COLOR_COMBINATIONS:
        if strict:
            if len(c) > min_len and cis > set(c):
                colour_ids.append(c)
        else:
            if len(c) >= min_len and cis >= set(c):
                colour_ids.append(c)

    return colour_ids


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
    costs = re.findall(r'{(.*?)}', mana_cost)
    # And for the contents of each element,
    for cost in costs:
        # Make sure it is a valid mana symbol.
        if cost not in MANA_SYMBOLS:
            # If not, return a dummy value.
            return default

    # If all check passed, return the found values.
    return costs
