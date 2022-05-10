from typing import Union
import functools

import pandas
from pandas import DataFrame
from pandas.io.formats.style import Styler, StylerRenderer


"""
@functools.singledispatch
def prettify_frame(arg):
    raise TypeError(f"Cannot convert type: '{type(arg)}'")


@prettify_frame.register(type(DataFrame))
def _prettify_frame(frame):
    frame.fillna('---')
    s = frame.style
    return _prettify_style(s)


@prettify_frame.register(type(Styler))
@prettify_frame.register(type(StylerRenderer))
@prettify_frame.register(type(pandas.io.formats.style.Styler))
@prettify_frame.register(type(pandas.io.formats.style.StylerRenderer))
def _prettify_style(styler):
    styler = styler.format(precision=2)
    cell_hover = {  # for row hover use <tr> instead of <td>
        'selector': 'td:hover',
        'props': [('background-color', '#ffffb3')]
    }
    index_names = {
        'selector': '.index_name',
        'props': 'font-style: italic; color: darkgrey; font-weight:normal;'
    }
    headers = {
        'selector': 'th:not(.index_name)',
        'props': 'background-color: #555555; color: white;'
    }
    styler.set_table_styles([cell_hover, index_names, headers])
    styler.set_table_styles([{'selector': 'th.col_heading', 'props': 'text-align: left;'}], overwrite=False)
    return styler
"""


def prettify_frame(arg: Union[DataFrame, Styler]):
    if isinstance(arg, DataFrame):
        frame = arg.fillna('---')
        styler = frame.style
    else:
        styler = arg
    styler = styler.format(precision=2)
    cell_hover = {  # for row hover use <tr> instead of <td>
        'selector': 'td:hover',
        'props': [('background-color', '#ffffb3')]
    }
    index_names = {
        'selector': '.index_name',
        'props': 'font-style: italic; color: darkgrey; font-weight:normal;'
    }
    headers = {
        'selector': 'th:not(.index_name)',
        'props': 'background-color: #555555; color: white;'
    }
    styler.set_table_styles([cell_hover, index_names, headers])
    styler.set_table_styles([{'selector': 'th.col_heading', 'props': 'text-align: left;'}], overwrite=False)
    return styler
