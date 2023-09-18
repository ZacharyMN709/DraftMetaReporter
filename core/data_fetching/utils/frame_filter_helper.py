import functools
from typing import Callable, Literal, Union, NoReturn
import pandas as pd

from core.wubrg import get_color_identity

FilterLike = Union[None, str, list[str], set[str]]
FilterFunc = Callable[[pd.DataFrame], pd.Series]


# region Rarity Filtering
@functools.singledispatch
def rarity_filter(rarities: FilterLike) -> Union[FilterFunc, NoReturn]:
    # By default, if we don't have a specific way of handling a parameter, raise an error.
                    f"Please use one of 'str', 'list[str]' or 'set[str]'.")
    raise TypeError(f"Cannot use type '{type(rarities)}' for a rarity filter. \n"


@rarity_filter.register(str)
def _rarity_filter_string(rarities: str) -> FilterFunc:
    # Convert the string into uppercase, then into a set.
    return lambda frame: frame['Rarity'].isin({i for i in set(rarities.upper())})


@rarity_filter.register(list)
def _rarity_filter_list(rarities: list[str]) -> FilterFunc:
    # Convert each element in the list into uppercase, and add to the set.
    return lambda frame: frame['Rarity'].isin({i.upper() for i in set(rarities)})


@rarity_filter.register(set)
def _rarity_filter_set(rarities: set[str]) -> FilterFunc:
    # Uppercase each element in the set.
    return lambda frame: frame['Rarity'].isin({i.upper() for i in rarities})
# endregion Rarity Filtering


# region Mana Value Filtering
OPERANDS = Literal['>', '<', '=', '==', '!=', '>=', '<=']


def cmc_filter(cmc: int, op: OPERANDS = "==") -> FilterFunc:
    # Make sure the mana value is an int, and op is str
    if type(cmc) is not int:
        raise TypeError("`cmc` must be an int.")
    if type(op) is not str:
        raise TypeError("`op` must be a str.")

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
@functools.singledispatch
def _color_filter(colors: FilterLike, _: str) -> FilterFunc:
    # By default, if we don't have a specific way of handling a parameter, raise an error.
    raise TypeError(f"Cannot use type '{type(colors)}' for a color filter. \n"
                    f"Please use one of 'str', 'list[str]' or 'set[str]'.")


@_color_filter.register(str)
def _color_filter_string(colors: str, col_name: str) -> FilterFunc:
    # Convert the string into uppercase, then into single element list.
    return lambda frame: frame[col_name].isin({get_color_identity(colors)})


@_color_filter.register(list)
def _color_filter_list(colors: list[str], col_name: str) -> FilterFunc:
    # Convert each element in the list into uppercase, and add to the set.
    return _color_filter_set({i.upper() for i in set(colors)}, col_name)


@_color_filter.register(set)
def _color_filter_set(colors: set[str], col_name: str) -> FilterFunc:
    # Return a function, based on the provided filter value.
    return lambda frame: frame[col_name].isin(colors)


def card_color_filter(colors: FilterLike) -> FilterFunc:
    return _color_filter(colors, 'Color')


def cast_color_filter(colors: FilterLike) -> FilterFunc:
    return _color_filter(colors, 'Cast Color')
# endregion Color Filtering


def compose_filters(filters: list[FilterFunc]) -> FilterFunc:
    def composed_func(frame: pd.DataFrame) -> pd.Series:
        sub_frame = frame.copy()
        filtered_frame = pd.DataFrame()
        for f in filters:
            filtered_frame[id(f)] = f(sub_frame)
        return filtered_frame.T.all()

    return composed_func


def filter_frame(frame, order: str = None, filters: list[FilterFunc] = None, asc: bool = False):
    if filters:
        sub_frame = pd.DataFrame()
        for f in filters:
            sub_frame[id(f)] = f(frame)
        frame = frame[sub_frame.T.all()]

    if order:
        return frame.sort_values(order, ascending=asc)
    else:
        return frame
