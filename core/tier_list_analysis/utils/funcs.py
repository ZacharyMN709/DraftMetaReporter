from core.game_metadata import CardManager

from core.tier_list_analysis.utils.consts import range_hexes, rarity_hexes, rank_hexes, color_hexes


# region Dataframe Formatting
def safe_to_int(val):
    try:
        return int(val)
    except Exception:
        return ' - '


def format_short_float(val):
    return '{:.1f}'.format(val)


def format_long_float(val):
    return '{:.3f}'.format(val)


def hover_card(card_name):
    card = CardManager.from_name(card_name)
    html = '<style>.hover_img a { position:relative; }\n' + \
           '.hover_img a span { position:absolute; display:none; z-index:300; }\n' + \
           '.hover_img a:hover span { display:block; height: 300px; width: 300px; overflow: visible; ' \
           'margin-left: -175px; }</style>\n' + \
           '<div class="hover_img">\n' + \
           f'<a href="#">{card.NAME}<span><img src="{card.IMAGE_URL}" alt="image"/></span></a>\n' + \
           '</div>'
    return html


def color_map(val):
    if len(val) == 1:
        return f'color: black; background-color: {color_hexes[val]}44'
    elif len(val) > 1:
        return f'color: black; background-color: #cea95244'


def rank_map(val, alpha='cc'):
    try:
        x = round(val)
        return f'color: black; background-color: {rank_hexes[x]}{alpha}'
    except:
        return f'color: black; background-color: #55555566'


def user_map(val):
    return rank_map(val, 'cc')


def stat_map(val):
    return rank_map(val, '44')


def range_map(val):
    return f'color: black; background-color: {range_hexes[round(val)]}'


def rarity_map(val):
    return f'color: black; background-color: {rarity_hexes[val]}22'
# endregion Dataframe Formatting
