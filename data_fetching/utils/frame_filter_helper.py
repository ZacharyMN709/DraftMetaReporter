import functools
from typing import Callable, Literal, Union, NoReturn
import pandas as pd

import WUBRG.funcs
from WUBRG import get_color_identity, COLORS, ColorSortStyles
from game_metadata.utils.consts import RARITIES


# region Set Parsing
@functools.singledispatch
def _parse_to_set(arg) -> Union[set[str], NoReturn]:
    """
    Takes string, lists and sets, and standardizes them into sets with uppercase values.
    """
    # By default, if we don't have a specific way of handling a parameter, raise an error.
    raise TypeError(f"Cannot use type '{type(arg)}' for a name slice. \n"
                    f"Please use one of 'str', 'list[str]' or 'set[str]'.")


@_parse_to_set.register(str)
def _parse_to_set_string(val: str) -> set[str]:
    # Convert the string into uppercase, then into a set.
    return {i for i in set(val.upper())}


@_parse_to_set.register(list[str])
def _parse_to_set_list(val: list[str]) -> set[str]:
    # Convert each element in the list into uppercase, adn add to the set.
    return {i.upper() for i in set(val)}


@_parse_to_set.register(set[str])
def _parse_to_set_slice(val: set[str]) -> set[str]:
    # Uppercase each element in the set.
    return {i.upper() for i in val}
# endregion Set Parsing


# region Rarity Filtering
def rarity_filter(rarities: Union[str, set]) \
        -> Callable[[pd.DataFrame], pd.DataFrame]:
    rarities = _parse_to_set(rarities)
    if len(rarities - RARITIES) != 0:
        raise ValueError(f"Set must be composed of subset of {RARITIES}")

    return lambda frame: frame['Rarity'].isin(rarities)
# endregion Rarity Filtering


# region Mana Value Filtering
OPERANDS = Literal['>', '<', '=', '==', '!=', '>=', '<=']


def cmc_filter(cmc: int, op: OPERANDS = "==") \
        -> Callable[[pd.DataFrame], pd.DataFrame]:
    # Make sure the mana value is an int.
    if type(cmc) is not int:
        raise ValueError("`cmc` must be an int.")

    # Map each of the enumeration values to a sort function.
    ops = {
        '>': lambda frame: frame['CMC'] > cmc,
        '<': lambda frame: frame['CMC'] < cmc,
        '=': lambda frame: frame['CMC'] == cmc,
        '==': lambda frame: frame['CMC'] == cmc,
        '!=': lambda frame: frame['CMC'] != cmc,
        '>=': lambda frame: frame['CMC'] >= cmc,
        '<=': lambda frame: frame['CMC'] <= cmc
    }

    # Verify that the provided filter value is valid.
    if op not in ops:
        raise ValueError(f"`op` must be one of {OPERANDS}")

    # Return a function, based on the provided filter value.
    return ops[op]
# endregion Mana Value Filtering


# region Color Filtering
def _color_filter(colors: Union[str, set], style: ColorSortStyles, col_name: str) \
        -> Callable[[pd.DataFrame], pd.DataFrame]:
    # TODO: Consider if/how this should handle sets of colours.

    # Validate the color string passed in.
    colors = _parse_to_set(colors)
    if len(colors - COLORS) != 0:
        raise ValueError(f"Set must be composed of subset of {COLORS}")

    # Take the set of colours, and merge it into a single string.
    colors = get_color_identity(''.join(colors))

    # Return a function, based on the provided filter value.
    return lambda frame: frame[col_name].isin(WUBRG.funcs.color_filter(colors, style))


def card_color_filter(colors: Union[str, set], style: ColorSortStyles = ColorSortStyles.exact) \
        -> Callable[[pd.DataFrame], pd.DataFrame]:
    return _color_filter(colors, style, 'Color')


def cast_color_filter(colors: Union[str, set], style: ColorSortStyles = ColorSortStyles.exact) \
        -> Callable[[pd.DataFrame], pd.DataFrame]:
    return _color_filter(colors, style, 'Cast Color')
# endregion Color Filtering


def compose_filters(filters: list[Callable[[pd.DataFrame], pd.DataFrame]]) -> Callable[[pd.DataFrame], pd.DataFrame]:
    def composed_func(frame: pd.DataFrame) -> pd.DataFrame:
        sub_frame = frame.copy()
        filtered_frame = pd.DataFrame()
        for f in filters:
            filtered_frame[id(f)] = f(sub_frame)
        return sub_frame[filtered_frame.T.all()]

    return composed_func
