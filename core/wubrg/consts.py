"""
Contains a set of string, lists and dictionaries to handle colors.
The dictionaries map the most common written/spoken names to an
associated colour combination, and a map which handles the reverse.

As well, the key-value pairs in these dictionaries are all in 'WUBRG' order,
for iterating purposes.
"""

from core.utilities import invert_dict
from core.wubrg.typing import COLOR, COLOR_IDENTITY, COLOR_ALIAS


# Colour Mapping
WUBRG: COLOR_IDENTITY = 'WUBRG'
FAILSAFE: COLOR_IDENTITY = ''
COLORS: set[COLOR] = set(WUBRG)

# region Colour Lists
# List the colour combinations in "WUBRG" order.
COLOR_COMBINATIONS: list[COLOR_IDENTITY] = [
    '', 'W', 'U', 'B', 'R', 'G',
    'WU', 'WB', 'WR', 'WG', 'UB', 'UR', 'UG', 'BR', 'BG', 'RG',
    'WUB', 'WUR', 'WUG', 'WBR', 'WBG', 'WRG', 'UBR', 'UBG', 'URG', 'BRG',
    'WUBR', 'WUBG', 'WURG', 'WBRG', 'UBRG', 'WUBRG'
]

# List the colour combinations in "Pentad" order.
GROUP_COLOR_COMBINATIONS: list[COLOR_IDENTITY] = [
    '',
    'W', 'U', 'B', 'R', 'G',
    'WU', 'UB', 'BR', 'RG', 'WG',
    'WB', 'BG', 'UG', 'UR', 'WR',
    'WUR', 'UBG', 'WBR', 'URG', 'WBG',
    'WUB', 'UBR', 'BRG', 'WRG', 'WUG',
    'WUBR', 'WUBG', 'WURG', 'WBRG', 'UBRG',
    'WUBRG'
]

# List of colours, by number of colours.
COLOR_SINGLES: list[COLOR_IDENTITY] = [colors for colors in COLOR_COMBINATIONS if len(colors) == 1]
COLOR_PAIRS: list[COLOR_IDENTITY] = [colors for colors in COLOR_COMBINATIONS if len(colors) == 2]
COLOR_TRIPLES: list[COLOR_IDENTITY] = [colors for colors in COLOR_COMBINATIONS if len(colors) == 3]
COLOR_QUADRUPLES: list[COLOR_IDENTITY] = [colors for colors in COLOR_COMBINATIONS if len(colors) == 4]
# endregion Colour Lists

# region Base Alias Dicts
# Dictionaries of the most common aliases for colour combinations, grouped by number of colours, in WUBRG order.
ONE_NAME_TO_COLOR: dict[COLOR_ALIAS, COLOR_IDENTITY] = {
    'White': "W",
    'Blue': "U",
    'Black': "B",
    'Red': "R",
    'Green': "G"
}
ONE_COLOR_TO_NAME: dict[COLOR_IDENTITY, COLOR_ALIAS] = invert_dict(ONE_NAME_TO_COLOR)

TWO_NAME_TO_COLOR: dict[COLOR_ALIAS, COLOR_IDENTITY] = {
    'Azorius': "WU",
    'Orzhov': "WB",
    'Boros': "WR",
    'Selesnya': "WG",
    'Dimir': "UB",
    'Izzet': "UR",
    'Simic': "UG",
    'Rakdos': "BR",
    'Golgari': "BG",
    'Gruul': "RG"
}
TWO_COLOR_TO_NAME: dict[COLOR_IDENTITY, COLOR_ALIAS] = invert_dict(TWO_NAME_TO_COLOR)

THREE_NAME_TO_COLOR: dict[COLOR_ALIAS, COLOR_IDENTITY] = {
    'Esper': "WUB",
    'Jeskai': "WUR",
    'Bant': "WUG",
    'Mardu': "WBR",
    'Abzan': "WBG",
    'Naya': "WRG",
    'Grixis': "UBR",
    'Sultai': "UBG",
    'Temur': "URG",
    'Jund': "BRG"
}
THREE_COLOR_TO_NAME: dict[COLOR_IDENTITY, COLOR_ALIAS] = invert_dict(THREE_NAME_TO_COLOR)

FOUR_NAME_TO_COLOR: dict[COLOR_ALIAS, COLOR_IDENTITY] = {
    'Non-G': "WUBR",
    'Non-R': "WUBG",
    'Non-B': "WURG",
    'Non-U': "WBRG",
    'Non-W': "UBRG"
}
FOUR_COLOR_TO_NAME: dict[COLOR_IDENTITY, COLOR_ALIAS] = invert_dict(FOUR_NAME_TO_COLOR)

# All previous dictionaries of aliases combined into one, with pairs for colourless and WUBRG added.
NAME_TO_COLOR: dict[COLOR_ALIAS, COLOR_IDENTITY] = {
    '': '',
    **ONE_NAME_TO_COLOR,
    **TWO_NAME_TO_COLOR,
    **THREE_NAME_TO_COLOR,
    **FOUR_NAME_TO_COLOR,
    'Five-Color': 'WUBRG'
}
COLOR_TO_NAME: dict[COLOR_IDENTITY, COLOR_ALIAS] = invert_dict(NAME_TO_COLOR)

# Groups of aliases based on the number of colours.
COLOUR_GROUPINGS: dict[str, dict[COLOR_ALIAS, COLOR_IDENTITY]] = {
    'Any': {'': ''},
    'Mono-Color': ONE_NAME_TO_COLOR,
    'Two-Color': TWO_NAME_TO_COLOR,
    'Three-Color': THREE_NAME_TO_COLOR,
    'Four-Color': FOUR_NAME_TO_COLOR,
    'Five-Color': {'Five-Color': 'WUBRG'},
    'All Decks': NAME_TO_COLOR
}
# endregion Base Alias Dicts
