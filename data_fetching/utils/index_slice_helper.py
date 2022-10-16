import functools
from typing import Union, NoReturn
from datetime import date, datetime

from wubrg import get_color_identity


# region Name Slice
@functools.singledispatch
def get_name_slice(arg) -> Union[slice, list[str], NoReturn]:
    # By default, if we don't have a specific way of handling a parameter, raise an error.
    raise TypeError(f"Cannot use type '{type(arg)}' for a name slice. \n"
                    f"Please use one of 'None', 'str', 'slice', 'list[str]' or 'tuple[str, str]'.")


@get_name_slice.register(type(None))
def _get_name_slice_none(val: None) -> slice:
    # Convert 'None' into an empty slice.
    return slice(val)


@get_name_slice.register(str)
def _get_name_slice_string(val: str) -> list[str]:
    # Wrap a string in a list
    return [val]


@get_name_slice.register(slice)
def _get_name_slice_slice(val: slice) -> slice:
    # Return a slice as-is.
    return val


@get_name_slice.register(list)
def _get_name_slice_list(val: list[str]) -> list[str]:
    # Return a list as-is.
    return val


@get_name_slice.register(tuple)
def _get_name_slice_range(val: tuple[str, str]) -> Union[slice, NoReturn]:
    # If the parameter is a tuple, see if it has two elements.
    if len(val) == 2:
        # If so, use that as a range for a slice
        return slice(val[0], val[1])
    else:
        # Otherwise raise an error
        raise TypeError(f"Type 'tuple' can only be used with 2 'str' elements, to define a range for a name slice. \n"
                        f"Please use one of 'None', 'str', 'slice', 'list[str] or 'tuple[str, str]'.")
# endregion Name Slice


# region Color Slice
@functools.singledispatch
def get_color_slice(arg) -> Union[slice, list[str], NoReturn]:
    # By default, if we don't have a specific way of handling a parameter, raise an error.
    raise TypeError(f"Cannot use type '{type(arg)}' for a color slice. \n"
                    f"Please use one of 'None', 'str', 'slice', 'list[str]' or 'tuple[str, str]'.")


@get_color_slice.register(type(None))
def _get_color_slice_none(val: None) -> slice:
    # Convert 'None' into an empty slice.
    return slice(val)


@get_color_slice.register(str)
def _get_color_slice_string(val: str) -> list[str]:
    # Wrap a string in a list
    return [get_color_identity(val)]


@get_color_slice.register(slice)
def _get_color_slice_slice(val: slice) -> slice:
    # Return a slice as-is.
    return val


@get_color_slice.register(list)
def _get_color_slice_list(val: list[str]) -> list[str]:
    # Return a list, with some checks to make sure the color elements are in WUBRG order.
    return [get_color_identity(color) for color in val]


@get_color_slice.register(tuple)
def _get_color_slice_range(val: tuple[str, str]) -> Union[slice, NoReturn]:
    # If the parameter is a tuple, see if it has two elements.
    if len(val) == 2:
        # If so, use that as a range for a slice, with some checks.
        return slice(get_color_identity(val[0]), get_color_identity(val[1]))
    else:
        # Otherwise raise an error
        raise TypeError(f"Type 'tuple' can only be used with 2 'str' elements, to define a range for a color slice. \n"
                        f"Please use one of 'None', 'str', 'slice', 'list[str] or 'tuple[str, str]'.")
# endregion Color Slice


# region Date Slice
@functools.singledispatch
def stringify_for_date_slice(arg) -> Union[str, NoReturn]:
    # By default, if we don't have a specific way of handling a parameter, raise an error.
    raise TypeError(f"Cannot use type '{type(arg)}' for a value as part of a date slice. \n"
                    f"Values inside 'slice', 'list' and 'tuple' types which can be properly converted are: "
                    f"'str', 'date' and 'datetime.")


@stringify_for_date_slice.register(str)
def _stringify_for_date_slice_string(arg: str) -> str:
    # Return a string as-is.
    return arg


@stringify_for_date_slice.register(date)
def _stringify_for_date_slice_date(arg: date) -> str:
    # Convert the date into a string.
    return str(arg)


@stringify_for_date_slice.register(datetime)
def _stringify_for_date_slice_datetime(arg: datetime) -> str:
    # Isolate the date from the datetime, then convert to a string.
    return str(arg.date())


@functools.singledispatch
def get_date_slice(arg) -> Union[slice, list[str], NoReturn]:
    # By default, if we don't have a specific way of handling a parameter, raise an error.
    raise TypeError(f"Cannot use type '{type(arg)}' for a date slice. \n"
                    f"Please use one of 'None', 'str', 'date', 'datetime, 'slice', 'list[Union[str, date, datetime]]' "
                    f"or 'tuple[Union[str, date, datetime], Union[str, date, datetime]]'.")


@get_date_slice.register(type(None))
def _get_date_slice_none(val: None) -> slice:
    # If the parameter is a None, marshall it into a slice.
    return slice(val)


@get_date_slice.register(str)
@get_date_slice.register(date)
@get_date_slice.register(datetime)
def _get_date_slice_string(val: Union[str, date, datetime]) -> list[str]:
    # If the parameter is a string, date, or datetime, stringify it wap it in a list.
    return [stringify_for_date_slice(val)]


@get_date_slice.register(slice)
def _get_date_slice_slice(val: slice) -> slice:
    # Return a slice as-is.
    return val


@get_date_slice.register(list)
def _get_date_slice_iterable(val: list[Union[str, date, datetime]]) -> list[str]:
    # For the list, attempt to convert all of its elements, and return it.
    return [stringify_for_date_slice(str_date) for str_date in val]


@get_date_slice.register(tuple)
def _get_date_slice_range(val: tuple[Union[str, date, datetime], Union[str, date, datetime]]) -> Union[slice, NoReturn]:
    # If the parameter is a tuple, check if it should be a range.
    if len(val) == 2:
        # If it should be a range, get the make sure we have the string version we need for the slice.
        return slice(stringify_for_date_slice(val[0]), stringify_for_date_slice(val[1]))
    else:
        raise TypeError(f"Type 'tuple' can only be used with 2 'Union[str, date, datetime]' elements, "
                        f"to define a range for a date slice. \n"
                        f"Please use one of 'None', 'str', 'date', 'datetime, 'slice', "
                        f"'list[Union[str, date, datetime]]' or "
                        f"'tuple[Union[str, date, datetime], Union[str, date, datetime]]'.")
# endregion Date Slice
