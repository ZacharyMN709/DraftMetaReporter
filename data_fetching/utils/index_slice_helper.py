import functools
from datetime import date, datetime

from WUBRG import get_color_identity, wubrg_compare_key
from WUBRG.funcs import color_compare_wubrg


# TODO: Consider simplifying these down to the bare minimum of what people might expect.
#  That would likely be None, slice, str, list, date, datetime

# region Name Slice
@functools.singledispatch
def get_name_slice(arg):
    # By default, if we don't have a special way to handle a parameter, don't change it.
    return arg


@get_name_slice.register(type(None))
def _get_name_slice_single(val):
    # If the parameter is None, marshall it into a slice.
    return slice(val)


@get_name_slice.register(str)
def _get_name_slice_string(val):
    # If the parameter is a string, marshall it into a single element list to filter properly.
    return [val]


@get_name_slice.register(set)
def _get_name_slice_unhashable(val):
    # If the parameter is a set, we need to convert it to a list so it's hashable.
    return sorted([name for name in val])
# endregion Name Slice


# region Color Slice
@functools.singledispatch
def get_color_slice(arg):
    # By default, if we don't have a special way to handle a parameter, don't change it.
    return arg


@get_color_slice.register(type(None))
def _get_color_slice_none(val):
    # If the parameter is a None, marshall it into a slice.
    return slice(val)


@get_color_slice.register(str)
def _get_color_slice_string(val):
    # If the parameter is a string, marshall it into a single element list to filter properly.
    return [get_color_identity(val)]


@get_color_slice.register(set)
def _get_color_slice_set(val):
    # If the parameter is a set, we need to convert it to a list so it's hashable.
    # While here sort, so colours show up in the correct order, and fix mis-ordered colours elements.
    return sorted([get_color_identity(color) for color in val], key=wubrg_compare_key)


@get_color_slice.register(list)
@get_color_slice.register(dict)
def _get_color_slice_iterable(val):
    # If the parameter is iterable, first convert it to a set to remove duplicates, then handle.
    return _get_color_slice_set({get_color_identity(color) for color in val})


@get_color_slice.register(tuple)
def _get_color_slice_range(val):
    # If the parameter is iterable, check if it should be a range.
    if len(val) == 2:
        # If it should be a range, get the colours check that the colours elements are properly ordered.
        col1 = get_color_identity(val[0])
        col2 = get_color_identity(val[1])
        # Then make sure a valid range is returned.
        if color_compare_wubrg(col2, col1) == 1:
            return slice(col1, col2)
        else:
            # TODO: See if returning a reversed range is possible.
            return slice(col2, col1)
    else:
        # If not, handle it like as an iterable.
        return _get_color_slice_iterable(val)
# endregion Color Slice


# region Date Slice
@functools.singledispatch
def _stringify_for_date_slice(arg):
    # By default, if we don't have a special way to handle a parameter, don't change it.
    return arg


@_stringify_for_date_slice.register(date)
def _stringify_for_date_slice_date(arg):
    # Convert the date into a string, then handle that.
    return _stringify_for_date_slice(str(arg))


@_stringify_for_date_slice.register(datetime)
def _stringify_for_date_slice_datetime(arg):
    # Isolate the date from the datetime, then handle that.
    return _stringify_for_date_slice_date(arg.date())


@functools.singledispatch
def get_date_slice(arg):
    # By default, if we don't have a special way to handle a parameter, don't change it.
    return arg


@get_date_slice.register(type(None))
def _get_date_slice_none(val):
    # If the parameter is a None, marshall it into a slice.
    return slice(val)


@get_date_slice.register(str)
@get_date_slice.register(date)
@get_date_slice.register(datetime)
def _get_date_slice_string(val):
    # If the parameter is a string, date or datetime, stringify it and marshall
    # it into a single element list to filter properly.
    return [_stringify_for_date_slice(val)]


@get_date_slice.register(set)
def _get_date_slice_set(val):
    # If the parameter is as set, attempt to convert all of its elements, and return them as a list.
    return sorted([_stringify_for_date_slice(str_date) for str_date in val])


@get_date_slice.register(list)
@get_date_slice.register(dict)
def _get_date_slice_iterable(val):
    # If the parameter is iterable, attempt to convert all of its elements, and parse it as a set.
    return _get_date_slice_set({_stringify_for_date_slice(str_date) for str_date in val})


@get_date_slice.register(tuple)
def _get_date_slice_range(val):
    # If the parameter is iterable, check if it should be a range.
    if len(val) == 2:
        # If it should be a range, get the make sure we have the string version we need for the slice.
        str_date1 = _stringify_for_date_slice(val[0])
        str_date2 = _stringify_for_date_slice(val[1])

        # TODO: Check the this properly orders dates.
        # Then make sure a valid range is returned.
        if str_date1 < str_date2:
            return slice(str_date1, str_date2)
        else:
            # TODO: See if returning a reversed range is possible.
            return slice(str_date2, str_date1)
    else:
        # If not, handle it like as an iterable.
        return _get_date_slice_iterable(val)
# endregion Date Slice
