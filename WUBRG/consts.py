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

# region Two Colour Groups
# Dictionaries of two-colour combinations, in wheel order.
ALLIED: dict[str, str] = {
    'Azorius': "WU",
    'Dimir': "UB",
    'Rakdos': "BR",
    'Gruul': "RG",
    'Selesnya': "WG"
}

ENEMY: dict[str, str] = {
    'Orzhov': "WB",
    'Golgari': "BG",
    'Simic': "UG",
    'Izzet': "UR",
    'Boros': "WR"
}

GUILDS: dict[str, str] = {
    'Azorius': "WU",
    'Dimir': "UB",
    'Rakdos': "BR",
    'Gruul': "RG",
    'Selesnya': "WG",
    'Orzhov': "WB",
    'Golgari': "BG",
    'Simic': "UG",
    'Izzet': "UR",
    'Boros': "WR"
}

COLLEGES: dict[str, str] = {
    'Silverquill': "WB",
    'Witherbloom': "BG",
    'Quandrix': "UG",
    'Prismari': "UR",
    'Lorehold': "WR"
}
# endregion Two Colour Groups

# region Three Colour Groups
# Dictionaries of three-colour combinations, in wheel order.
WEDGES: dict[str, str] = {
    'Jeskai': "WUR",
    'Sultai': "UBG",
    'Mardu': "WBR",
    'Temur': "URG",
    'Abzan': "WBG"
}

TRIOMES: dict[str, str] = {
    'Raugrin': "WUR",
    'Zagoth': "UBG",
    'Savai': "WBR",
    'Ketria': "URG",
    'Indatha': "WBG"
}

SHARDS: dict[str, str] = {
    'Esper': "WUB",
    'Grixis': "UBR",
    'Jund': "BRG",
    'Naya': "WRG",
    'Bant': "WUG"
}

FAMILIES: dict[str, str] = {
    'Obscura': "WUB",
    'Maestros': "UBR",
    'Riveteers': "BRG",
    'Cabaretti': "WRG",
    'Brokers': "WUG",
}
# endregion Three Colour Groups

# region Four Colour Groups
# Dictionaries of four-colour combinations, in wheel order.
NEPHILLIM: dict[str, str] = {
    'Yore': "WUBR",
    'Witch': "WUBG",
    'Ink': "WURG",
    'Dune': "WBRG",
    'Glint': "UBRG"
}
# endregion Four Colour Groups

# region Five Colour Groups
# Dictionaries of five-colour aliases.
ALL_COLOURS_ALIASES: dict[str, str] = {
        'WUBRG': 'WUBRG',
        '5-Color': 'WUBRG',
        'Five-Color': 'WUBRG',
        'All': 'WUBRG'
    }
# endregion Five Colour Groups

# region Any Colour Groups
# Dictionaries of any colour aliases.
ANY_COLOURS_ALIASES: dict[str, str] = {
        None: '',
        'None': '',
        'Any': '',
        '': ''
    }
# endregion Any Colour Groups


# region Master Alias Mappings
# Groupings of colour-combinations supported.
ALL_COLOR_ALIAS_GROUP_MAP: dict[str, dict[str, str]] = {
    'Any': ANY_COLOURS_ALIASES,
    'Mono-Color': SINGLE_COLOR_MAP,
    'Allied': ALLIED,
    'Enemy': ENEMY,
    'Guilds': GUILDS,
    'Colleges': COLLEGES,
    'Wedges': WEDGES,
    'Triomes': TRIOMES,
    'Shards': SHARDS,
    'Families': FAMILIES,
    'Nephillim': NEPHILLIM,
    'All': ALL_COLOURS_ALIASES
}

# Aliases for the colour combinations.
ALL_COLOR_ALIAS_MAP: dict[str, str] = {
    **ANY_COLOURS_ALIASES,
    **SINGLE_COLOR_MAP,
    **GUILDS,
    **COLLEGES,
    **WEDGES,
    **TRIOMES,
    **SHARDS,
    **FAMILIES,
    **NEPHILLIM,
    **ALL_COLOURS_ALIASES
}
# endregion Master Alias Mappings


# region Colour Count Mappings
# TODO: Tidy this up a little.
# Used for graphing
COLOR_COUNT_MAP: dict[str, int] = {
    "Mono-Color": 1,
    "Two-Color": 2,
    "Three-Color": 3,
    "Four-Color": 4,
    "Five-Color": 5,
    "All Decks": None
}

COLOR_COUNT_SHORTHAND_MAP: dict[str, str] = {
    "All Decks": "ALL",
    "Mono-Color": "1C",
    "Two-Color": "2C",
    "Three-Color": "3C",
    "Four-Color": "4C",
    "Five-Color": "5C"
}

COLOR_COUNT_SHORTHAND: list[str] = [COLOR_COUNT_SHORTHAND_MAP[key] for key in COLOR_COUNT_SHORTHAND_MAP]

COLOR_COUNT_REVERSE_MAP: dict[int, str] = {
    0: "All Decks",
    1: "Mono-Color",
    2: "Two-Color",
    3: "Three-Color",
    4: "Four-Color",
    5: "Five-Color",
    None: "All Decks"
}
# endregion Colour Count Mappings
