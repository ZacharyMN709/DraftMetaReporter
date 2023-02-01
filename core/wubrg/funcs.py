"""
Contains functions which handle colour string and colour combination manipulation.
"""

from typing import Optional, Callable
import re
import logging

from core.wubrg.typing import COLOR, COLOR_STRING, COLOR_IDENTITY, COLOR_ALIAS, MANA_SYMBOL, FORMATTED_MANA_SYMBOL
from core.wubrg.consts import WUBRG, COLOR_TO_NAME, COLOR_COMBINATIONS
from core.wubrg.alias_mappings import ALIAS_MAP
from core.wubrg.mana_symbols import MANA_SYMBOLS


_mana_cost_re = re.compile(r'{(.*?)}')
_mana_symbol_scrub = re.compile('[0-9{}XC]')


# region Color String Conversions
def is_color_string(text: str) -> bool:
    """ Checks if the provided string is a valid COLOR_STRING """
    return set(text.upper()) <= set(WUBRG)


def get_color_string(text: Optional[str]) -> COLOR_STRING:
    """
    Takes in a string, and attempts to convert it to a color string, with some amount
    of forgiveness for mis-spelling and casing. If the string is invalid, returns ''.
    This function will attempt to convert common names and costs into their colours.
    Egs. 'Bant' -> 'WUG', 'bant' -> 'WUG', '{2}{G}{G}' -> 'GG', '{2}{G{G}' -> 'GG', 'A' -> ''
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
        # If the string is in the dictionary, it has to be a COLOR_ALIAS.
        # noinspection PyTypeChecker
        return ALIAS_MAP[s]

    # Replace '{', '}', 'X' or any numeric.
    ret = _mana_symbol_scrub.sub('', s)

    # If the incoming string was a colorless mana-cost, it will be empty.
    if ret == '':
        return ''

    # Get all the characters that are in WUBRG
    ret = ''.join(c for c in ret.upper() if c in WUBRG)

    # If the return string is empty, log a warning message.
    if not ret:
        logging.warning(f"Invalid color string provided: {text}. No color values could be found in string.")

    return ret


def get_color_identity(text: str) -> COLOR_IDENTITY:
    """
    Takes in a color string, and attempts to convert it to a
    color identity string.
    :param text: The color string to convert.
    :return: A color identity string, a subset of 'WUBRG', in 'WUBRG' order.
    """

    # Get the colour string, and put it into a set to remove duplicate characters.
    color_string = get_color_string(text)
    char_set = set(color_string)

    # Removes any non-COLOR symbols from the set, converting it to a COLOR_IDENTITY
    # noinspection PyTypeChecker
    color_identity: COLOR_IDENTITY = ''.join(c for c in WUBRG if c in char_set)
    return color_identity


def parse_color_list(color_list: list[COLOR]) -> COLOR_IDENTITY:
    """
    Takes a lists of colours and combines it into a COLOR_STRING.
    """
    color_str = ''.join(color_list)
    return get_color_identity(color_str)


def get_color_alias(color_string: str) -> Optional[COLOR_ALIAS]:
    """
    Takes in a colour string and attempts to return a more
    common name for the colors. e.g. 'WUR' -> 'Jeskai'
    An invalid string or the colorless colour identity returns None.
    :param color_string: The color string to convert.
    :return: A common name which represents the colours in color_string, or None.
    """

    # Get the colour identity of the string, to use to map.
    color_identity = get_color_identity(color_string)

    # If the incoming string was invalid or colorless, return None.
    if color_identity == '':
        return None

    # Otherwise, we have something to map. Return its alias.
    return COLOR_TO_NAME[color_identity]
# endregion Color String Conversions


# region Mana Cost Conversions
def parse_cost(mana_cost: FORMATTED_MANA_SYMBOL) -> list[MANA_SYMBOL]:
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
        logging.warning(f"Invalid mana cost provided: {mana_cost}. Converting to '{default}'")
        return default

    # Find anything like {.} in the string,
    costs = _mana_cost_re.findall(mana_cost)
    # And for the contents of each element,
    for cost in costs:
        # Make sure it is a valid mana symbol.
        if cost not in MANA_SYMBOLS:
            # If not, return a dummy value.
            logging.warning(f"Invalid mana cost provided: {mana_cost}. Converting to '{default}'")
            return default

    # If all checks passed, return the found values.
    return costs


def calculate_cmc(mana_cost: FORMATTED_MANA_SYMBOL) -> int:
    # Get each mana symbol in the mana cost, add its cost to the total cmc.
    cmc_str = parse_cost(mana_cost)
    cmc = 0
    for symbol in cmc_str:
        if symbol.isnumeric():
            cmc += int(symbol)
        else:
            if symbol == 'X':
                continue
            cmc += 1
    return cmc
# endregion Mana Cost Conversions


# region Color Set Generation
def _get_color_sets(eval_func: Callable[[COLOR_IDENTITY, COLOR_IDENTITY], bool],
                    color_id: str, strict: bool = False) -> list[COLOR_IDENTITY]:
    """
    Gets all possible permutations of WUBRG which contain the color_id, based on a
    provided evaluation function.
    :param eval_func: The function to determine if an element belongs to the results set.
    :param color_id: The colours to look for in the permutations.
    :param strict: Whether the subset should be strict. Default: False
    :return: A list of colour identities.
    """

    # Get the colour identity of the incoming string, to standardize the string.
    color_id = get_color_identity(color_id)

    # Initialize a return list, and for each colour combination add it to the list if it meets the requirements.
    color_ids = list()
    for to_add in COLOR_COMBINATIONS:
        if eval_func(to_add, color_id):
            color_ids.append(to_add)

    # If the strict flag is set, remove the original colour id.
    if strict:
        color_ids.remove(color_id)

    return color_ids


def get_color_supersets(color_id: str, max_len: int = 5, strict: bool = False) -> list[COLOR_IDENTITY]:
    """
    Gets all possible permutations of WUBRG which contain the color_id.
    Can limit the length of the permutations returned with max_len.
    :param color_id: The colours to look for in the permutations.
    :param max_len: The max length of the permutations. Default: 5
    :param strict: Whether the subset should be strict. Default: False
    :return: A list of colour identities.
    """

    # A function which determines if the color to_add belongs to the desired set.
    def eval_func(to_add: COLOR_IDENTITY, base_id: COLOR_IDENTITY):
        return len(to_add) <= max_len and set(base_id) <= set(to_add)

    return _get_color_sets(eval_func, color_id, strict)


def get_color_subsets(color_id: str, min_len: int = 0, strict: bool = False) -> list[COLOR_IDENTITY]:
    """
    Gets all possible permutations of WUBRG which are contained in color_id.
    Can limit the length of the permutations returned with min_len.
    :param color_id: The colours to look for in the permutations.
    :param min_len: The min length of the permutations. Default: 0
    :param strict: Whether the subset should be strict. Default: False
    :return: A list of colour identities.
    """

    # A function which determines if the color to_add belongs to the desired set.
    def eval_func(to_add: COLOR_IDENTITY, base_id: COLOR_IDENTITY):
        return len(to_add) >= min_len and set(base_id) >= set(to_add)

    return _get_color_sets(eval_func, color_id, strict)
# endregion Color Set Generation
