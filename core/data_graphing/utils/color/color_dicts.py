from core.wubrg.typing import COLOR_IDENTITY

from colors import Color

# For internal use, for easy palette changing.
_LIGHT_WHITE = Color.AMBER_100
_LIGHT_BLUE = Color.BLUE_500
_LIGHT_BLACK = Color.GREY_500
_LIGHT_RED = Color.RED_500
_LIGHT_GREEN = Color.GREEN_500

_WHITE = Color.AMBER_200
_BLUE = Color.BLUE_700
_BLACK = Color.GREY_700
_RED = Color.RED_700
_GREEN = Color.GREEN_700

_DARK_WHITE = Color.AMBER_300
_DARK_BLUE = Color.BLUE_900
_DARK_BLACK = Color.GREY_900
_DARK_RED = Color.RED_900
_DARK_GREEN = Color.GREEN_900


# Externally accessible dictionaries, which map archetypes to colours.
WHITE: dict[COLOR_IDENTITY, Color] = {
     'WU': _BLUE,
     'WB': _BLACK,
     'WR': _RED,
     'WG': _GREEN,
}

BLUE: dict[COLOR_IDENTITY, Color] = {
     'WU': _WHITE,
     'UB': _BLACK,
     'UR': _RED,
     'UG': _GREEN,
}

BLACK: dict[COLOR_IDENTITY, Color] = {
     'WB': _WHITE,
     'UB': _BLUE,
     'BR': _RED,
     'BG': _GREEN,
}

RED: dict[COLOR_IDENTITY, Color] = {
     'WR': _WHITE,
     'UR': _BLUE,
     'BR': _BLACK,
     'RG': _GREEN,
}

GREEN: dict[COLOR_IDENTITY, Color] = {
    'WG': _WHITE,
    'UG': _BLUE,
    'BG': _BLACK,
    'RG': _RED,
}

ALLIED: dict[COLOR_IDENTITY, Color] = {
     'WG': _WHITE,
     'WU': _BLUE,
     'UB': _BLACK,
     'BR': _RED,
     'RG': _GREEN,
}

ENEMY: dict[COLOR_IDENTITY, Color] = {
     'WB': _WHITE,
     'UR': _BLUE,
     'BG': _BLACK,
     'WR': _RED,
     'UG': _GREEN,
}

SHARD: dict[COLOR_IDENTITY, Color] = {
     'WUG': _WHITE,
     'WUB': _BLUE,
     'UBR': _BLACK,
     'BRG': _RED,
     'WRG': _GREEN,
}

WEDGE: dict[COLOR_IDENTITY, Color] = {
     'WBR': _WHITE,
     'URG': _BLUE,
     'WBG': _BLACK,
     'WUR': _RED,
     'UBG': _GREEN,
}

NEPHILIM: dict[COLOR_IDENTITY, Color] = {
     'UBRG': _WHITE,
     'WBRG': _BLUE,
     'WURG': _BLACK,
     'WUBG': _RED,
     'WUBR': _GREEN,
}

TWO_COLOR: dict[COLOR_IDENTITY, Color] = {
     'WG': _WHITE,
     'WU': _BLUE,
     'UB': _BLACK,
     'BR': _RED,
     'RG': _GREEN,
     'WB': _DARK_WHITE,
     'UR': _DARK_BLUE,
     'BG': _DARK_BLACK,
     'WR': _DARK_RED,
     'UG': _DARK_GREEN,
}

THREE_COLOR: dict[COLOR_IDENTITY, Color] = {
     'WUG': _WHITE,
     'WUB': _BLUE,
     'UBR': _BLACK,
     'BRG': _RED,
     'WRG': _GREEN,
     'WBR': _DARK_WHITE,
     'URG': _DARK_BLUE,
     'WBG': _DARK_BLACK,
     'WUR': _DARK_RED,
     'UBG': _DARK_GREEN,
}

COLOR_COUNTS: dict[str, Color] = {
     'ALL': Color.PURPLE_A400,
     '1C': Color.PURPLE_100,
     '2C': Color.PURPLE_300,
     '3C': Color.PURPLE_500,
     '4C': Color.PURPLE_700,
     '5C': Color.PURPLE_900,
}


COLOR_MAPPINGS: dict[str, dict[COLOR_IDENTITY, Color]] = {
     "White": WHITE,
     "Blue": BLUE,
     "Black": BLACK,
     "Red": RED,
     "Green": GREEN,
     "Allied": ALLIED,
     "Enemy": ENEMY,
     "Shard": SHARD,
     "Wedge": WEDGE,
     "Nephilim": NEPHILIM,
     "Two Color": TWO_COLOR,
     "Three Color": THREE_COLOR,
     "Four Color": NEPHILIM,
}
