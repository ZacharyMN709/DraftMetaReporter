from typing import Union, NoReturn
import functools

from pandas import DataFrame
from pandas.io.formats.style import Styler

from core.game_metadata import Card


@functools.singledispatch
def prettify_frame(arg) -> Union[Styler, NoReturn]:  # pragma: no cover
    raise TypeError(f"Cannot convert type '{type(arg)}' to a prettified frame.\n"
                    f"Types accepted: 'DataFrame', 'Styler'")


@prettify_frame.register(DataFrame)
def _prettify_frame(frame: DataFrame) -> Styler:  # pragma: no cover
    new_frame = frame.fillna('---')
    s = new_frame.style
    return _prettify_style(s)


# noinspection SpellCheckingInspection
@prettify_frame.register(Styler)
def _prettify_style(styler: Styler) -> Styler:  # pragma: no cover
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


def hyperlink_card_index(card_name: str, card_dict: dict[str, Card]) -> str:
    try:
        card = card_dict[card_name]
        html = (
            f'<style>\n'
            f'    .hover_img a {{ position:relative; }}\n'
            f'    .hover_img a span {{ position:absolute; display:none; z-index:300; }}\n'
            f'    .hover_img a:hover span {{ \n'
            f'        display:block; height: 300px; width: 300px; overflow: visible; margin-left: 50px;\n'
            f'     }}\n'
            f'    .hover_img a:link {{ color: white; }}\n'
            f'    .hover_img a:visited {{ color: white; }}\n'
            f'</style>\n'
            f'<div class="hover_img">\n'
            f'    <a href="{card.URL}" target="_blank">{card.NAME}\n'
            f'        <span><img src="{card.IMAGE_URL}" alt="image"/></span>\n'
            f'    </a>\n'
            f'</div>'
        )
        return html
    except KeyError:
        return card_name
