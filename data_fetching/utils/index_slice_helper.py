import functools

from WUBRG import get_color_identity, color_compare_key
from WUBRG.funcs import color_compare


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
    return sorted([get_color_identity(color) for color in val], key=color_compare_key)


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
        if color_compare(col2, col1) == 1:
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
def get_date_slice(arg):
    # By default, if we don't have a special way to handle a parameter, don't change it.
    return arg
# endregion Date Slice
