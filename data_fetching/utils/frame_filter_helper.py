import functools
from typing import Callable, Literal, Union, NoReturn
import pandas as pd
from WUBRG import get_color_identity


# region Rarity Filtering
@functools.singledispatch
def rarity_filter(rarities: Union[str, list[str], set[str]]) -> Union[Callable[[pd.DataFrame], pd.Series], NoReturn]:
    # By default, if we don't have a specific way of handling a parameter, raise an error.
    raise TypeError(f"Cannot use type '{type(rarities)}' for a name slice. \n"
                    f"Please use one of 'str', 'list[str]' or 'set[str]'.")


@rarity_filter.register(str)
def _rarity_filter_string(rarities: str) -> Callable[[pd.DataFrame], pd.Series]:
    # Convert the string into uppercase, then into a set.
    return lambda frame: frame['Rarity'].isin({i for i in set(rarities.upper())})


@rarity_filter.register(list)
def _rarity_filter_list(rarities: list[str]) -> Callable[[pd.DataFrame], pd.Series]:
    # Convert each element in the list into uppercase, and add to the set.
    return lambda frame: frame['Rarity'].isin({i.upper() for i in set(rarities)})


@rarity_filter.register(set)
def _rarity_filter_set(rarities: set[str]) -> Callable[[pd.DataFrame], pd.Series]:
    # Uppercase each element in the set.
    return lambda frame: frame['Rarity'].isin({i.upper() for i in rarities})
# endregion Rarity Filtering


# region Mana Value Filtering
OPERANDS = Literal['>', '<', '=', '==', '!=', '>=', '<=']


def cmc_filter(cmc: int, op: OPERANDS = "==") \
        -> Callable[[pd.DataFrame], pd.Series]:
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
def _color_filter(colors: Union[str, list[str], set[str]], col_name: str) -> Callable[[pd.DataFrame], pd.Series]:
    # By default, if we don't have a specific way of handling a parameter, raise an error.
    raise TypeError(f"Cannot use type '{type(colors)}' for a color filter. \n"
                    f"Please use one of 'str', 'list[str]' or 'set[str]'.")


@_color_filter.register(str)
def _color_filter_string(colors: str, col_name: str) -> Callable[[pd.DataFrame], pd.Series]:
    # Convert the string into uppercase, then into single element list.
    return lambda frame: frame[col_name].isin({get_color_identity(colors)})


@_color_filter.register(list)
def _color_filter_list(colors: list[str], col_name: str) -> Callable[[pd.DataFrame], pd.Series]:
    # Convert each element in the list into uppercase, and add to the set.
    return _color_filter_set({i.upper() for i in set(colors)}, col_name)


@_color_filter.register(set)
def _color_filter_set(colors: set[str], col_name: str) -> Callable[[pd.DataFrame], pd.Series]:
    # Return a function, based on the provided filter value.
    return lambda frame: frame[col_name].isin(colors)


def card_color_filter(colors: Union[str, list[str], set[str]]) -> Callable[[pd.DataFrame], pd.Series]:
    return _color_filter(colors, 'Color')


def cast_color_filter(colors: Union[str, list[str], set[str]]) -> Callable[[pd.DataFrame], pd.Series]:
    return _color_filter(colors, 'Cast Color')
# endregion Color Filtering


def compose_filters(filters: list[Callable[[pd.DataFrame], pd.Series]]) -> Callable[[pd.DataFrame], pd.Series]:
    def composed_func(frame: pd.DataFrame) -> pd.Series:
        sub_frame = frame.copy()
        filtered_frame = pd.DataFrame()
        for f in filters:
            filtered_frame[id(f)] = f(sub_frame)
        return filtered_frame.T.all()

    return composed_func
