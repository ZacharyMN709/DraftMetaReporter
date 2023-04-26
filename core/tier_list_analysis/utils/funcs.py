import logging

from core.game_metadata import CardManager

from core.tier_list_analysis.utils.consts import range_hexes, rarity_hexes, rank_hexes, color_hexes, change_hexes


# region Dataframe Formatting
ON_ERROR = f'color: black; background-color: #55555566'


def failsafe(function):
    def wrapper(*args, **kwargs):
        try:
            output = function(*args, **kwargs)
            return output
        except KeyError:
            return ON_ERROR
        except TypeError:
            return ON_ERROR
        except ValueError:
            return ON_ERROR

    return wrapper


def gen_background_str(color: str | int, alpha: str | int = '') -> str:
    if isinstance(color, str) and color.startswith('#'):
        color = color[1:]
    return f'color: black; background-color: #{color}{alpha}'


def safe_to_int(val):
    try:
        return int(val)
    except TypeError:
        return ' - '
    except ValueError:
        return ' - '


def format_short_float(val):
    return '{:.1f}'.format(val)


def format_long_float(val):
    return '{:.3f}'.format(val)


def hover_card(card_name):
    try:
        card = CardManager.from_name(card_name)
        html = '<style>.hover_img a { position:relative; }\n' + \
               '.hover_img a span { position:absolute; display:none; z-index:300; }\n' + \
               '.hover_img a:hover span { display:block; height: 300px; width: 300px; overflow: visible; ' \
               'margin-left: -175px; }</style>\n' + \
               '<div class="hover_img">\n' + \
               f'<a href="#">{card.NAME}<span><img src="{card.IMAGE_URL}" alt="image"/></span></a>\n' + \
               '</div>'
        return html
    except:
        return card_name


@failsafe
def color_map(val):
    if len(val) == 1:
        return gen_background_str(color_hexes[val], 44)
    elif len(val) > 1:
        return gen_background_str('cea952', 44)


@failsafe
def user_map(val):
    return gen_background_str(rank_hexes[round(val)], 'cc')


@failsafe
def stat_map(val):
    return gen_background_str(rank_hexes[round(val)], '44')


@failsafe
def change_map(val):
    return gen_background_str(change_hexes[round(val) + 12])


@failsafe
def range_map(val):
    return gen_background_str(range_hexes[round(val)])


@failsafe
def rarity_map(val):
    return gen_background_str(rarity_hexes[val], 22)
# endregion Dataframe Formatting
