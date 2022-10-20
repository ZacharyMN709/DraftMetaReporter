"""
Contains a set of string, lists and dictionaries to handle colors.
The dictionaries map the most common written/spoken names to an
associated colour combination, and a map which handles the reverse.

As well, the key-value pairs in these dictionaries are all in 'WUBRG' order,
for iterating purposes.
"""

# Colour Mapping
WUBRG: str = 'WUBRG'
COLORS: set = set(WUBRG)
FAILSAFE: str = ''


# List the colour combinations in "WUBRG" order.
COLOR_COMBINATIONS: list[str] = ['', 'W', 'U', 'B', 'R', 'G',
                                 'WU', 'WB', 'WR', 'WG', 'UB', 'UR', 'UG', 'BR', 'BG', 'RG',
                                 'WUB', 'WUR', 'WUG', 'WBR', 'WBG', 'WRG', 'UBR', 'UBG', 'URG', 'BRG',
                                 'WUBR', 'WUBG', 'WURG', 'WBRG', 'UBRG', 'WUBRG']

# List the colour combinations in "Pentad" order.
GROUP_COLOR_COMBINATIONS: list[str] = ['',
                                       'W', 'U', 'B', 'R', 'G',
                                       'WU', 'UB', 'BR', 'RG', 'WG',
                                       'WB', 'BG', 'UG', 'UR', 'WR',
                                       'WUR', 'UBG', 'WBR', 'URG', 'WBG',
                                       'WUB', 'UBR', 'BRG', 'WRG', 'WUG',
                                       'WUBR', 'WUBG', 'WURG', 'WBRG', 'UBRG',
                                       'WUBRG']

# List of colours, by number of colours.
COLOR_SINGLES: list[str] = [colors for colors in COLOR_COMBINATIONS if len(colors) == 1]
COLOR_PAIRS: list[str] = [colors for colors in COLOR_COMBINATIONS if len(colors) == 2]
COLOR_TRIPLES: list[str] = [colors for colors in COLOR_COMBINATIONS if len(colors) == 3]
COLOR_QUADRUPLES: list[str] = [colors for colors in COLOR_COMBINATIONS if len(colors) == 4]

# region Colour Count Dicts
# Dictionaries of the most common aliases for colour combinations, grouped by number of colours, in WUBRG order.
ONE_NAME_TO_COLOR: dict[str, str] = {
    'White': "W",
    'Blue': "U",
    'Black': "B",
    'Red': "R",
    'Green': "G"
}
ONE_COLOR_TO_NAME: dict[str, str] = {v: k for k, v in ONE_NAME_TO_COLOR.items()}

TWO_NAME_TO_COLOR: dict[str, str] = {
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
TWO_COLOR_TO_NAME: dict[str, str] = {v: k for k, v in TWO_NAME_TO_COLOR.items()}

THREE_NAME_TO_COLOR: dict[str, str] = {
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
THREE_COLOR_TO_NAME: dict[str, str] = {v: k for k, v in THREE_NAME_TO_COLOR.items()}

FOUR_NAME_TO_COLOR: dict[str, str] = {
    'Non-G': "WUBR",
    'Non-R': "WUBG",
    'Non-B': "WURG",
    'Non-U': "WBRG",
    'Non-W': "UBRG"
}
FOUR_COLOR_TO_NAME: dict[str, str] = {v: k for k, v in FOUR_NAME_TO_COLOR.items()}

NAME_TO_COLOR: dict[str, str] = {
    '': '',
    **ONE_NAME_TO_COLOR,
    **TWO_NAME_TO_COLOR,
    **THREE_NAME_TO_COLOR,
    **FOUR_NAME_TO_COLOR,
    'Five-Color': 'WUBRG'
}
COLOR_TO_NAME: dict[str, str] = {v: k for k, v in NAME_TO_COLOR.items()}

# Groups of aliases based on the number of colours.
COLOUR_GROUPINGS: dict[str, dict[str, str]] = {
    'Any': {'': ''},
    'Mono-Color': ONE_NAME_TO_COLOR,
    'Two-Color': TWO_NAME_TO_COLOR,
    'Three-Color': THREE_NAME_TO_COLOR,
    'Four-Color': FOUR_NAME_TO_COLOR,
    'Five-Color': {'Five-Color': 'WUBRG'},
    'All Decks': NAME_TO_COLOR
}
# endregion Colour Count Dicts
