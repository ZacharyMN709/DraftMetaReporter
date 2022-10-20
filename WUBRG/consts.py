# Colour Mapping
WUBRG: str = 'WUBRG'
COLORS: set = set(WUBRG)
FAILSAFE: str = ''


# List the colour combinations in WUBRG order.
COLOR_COMBINATIONS: list[str] = ['', 'W', 'U', 'B', 'R', 'G',
                                 'WU', 'WB', 'WR', 'WG', 'UB', 'UR', 'UG', 'BR', 'BG', 'RG',
                                 'WUB', 'WUR', 'WUG', 'WBR', 'WBG', 'WRG', 'UBR', 'UBG', 'URG', 'BRG',
                                 'WUBR', 'WUBG', 'WURG', 'WBRG', 'UBRG', 'WUBRG']

# List of colours, by number of colours.
COLOR_SINGLES: list[str] = [colors for colors in COLOR_COMBINATIONS if len(colors) == 1]
COLOR_PAIRS: list[str] = [colors for colors in COLOR_COMBINATIONS if len(colors) == 2]
COLOR_TRIPLES: list[str] = [colors for colors in COLOR_COMBINATIONS if len(colors) == 3]
COLOR_QUADRUPLES: list[str] = [colors for colors in COLOR_COMBINATIONS if len(colors) == 4]

# List the colour combinations in "Pentad" order.
GROUP_COLOR_COMBINATIONS: list[str] = ['',
                                       'W', 'U', 'B', 'R', 'G',
                                       'WU', 'UB', 'BR', 'RG', 'WG',
                                       'WB', 'BG', 'UG', 'UR', 'WR',
                                       'WUR', 'UBG', 'WBR', 'URG', 'WBG',
                                       'WUB', 'UBR', 'BRG', 'WRG', 'WUG',
                                       'WUBR', 'WUBG', 'WURG', 'WBRG', 'UBRG',
                                       'WUBRG']


# region Colour Count Dicts
# Dictionaries of the most common aliases for colour combinations, grouped by number of colours, in WUBRG order.
SINGLE_COLOR_MAP: dict[str, str] = {
    'White': "W",
    'Blue': "U",
    'Black': "B",
    'Red': "R",
    'Green': "G"
}
REVERSE_SINGLE_COLOR_MAP: dict[str, str] = {v: k for k, v in SINGLE_COLOR_MAP.items()}

TWO_COLOR_MAP: dict[str, str] = {
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
REVERSE_TWO_COLOR_MAP: dict[str, str] = {v: k for k, v in TWO_COLOR_MAP.items()}

THREE_COLOR_MAP: dict[str, str] = {
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
REVERSE_THREE_COLOR_MAP: dict[str, str] = {v: k for k, v in THREE_COLOR_MAP.items()}

FOUR_COLOR_MAP: dict[str, str] = {
    'Non-G': "WUBR",
    'Non-R': "WUBG",
    'Non-B': "WURG",
    'Non-U': "WBRG",
    'Non-W': "UBRG"
}
REVERSE_FOUR_COLOR_MAP: dict[str, str] = {v: k for k, v in FOUR_COLOR_MAP.items()}

COLOR_MAP: dict[str, str] = {
    '': '',
    **SINGLE_COLOR_MAP,
    **TWO_COLOR_MAP,
    **THREE_COLOR_MAP,
    **FOUR_COLOR_MAP,
    'Five-Color': 'WUBRG'
}
REVERSE_COLOR_MAP: dict[str, str] = {v: k for k, v in COLOR_MAP.items()}

# Groups of aliases based on the number of colours.
COLOUR_GROUPINGS: dict[str, dict[str, str]] = {
    'Any': {'': ''},
    'Mono-Color': SINGLE_COLOR_MAP,
    'Two-Color': TWO_COLOR_MAP,
    'Three-Color': THREE_COLOR_MAP,
    'Four-Color': FOUR_COLOR_MAP,
    'Five-Color': {'Five-Color': 'WUBRG'},
    'All Decks': COLOR_MAP
}
# endregion Colour Count Dicts
