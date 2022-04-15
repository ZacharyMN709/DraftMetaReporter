# Colour Mapping
COLORS: str = "WUBRG"

# Groupings of colour combinations by origin/description.
SINGLE_COLORS: dict[str, str] = {
    'White': "W",
    'Blue': "U",
    'Black': "B",
    'Red': "R",
    'Green': "G"
}

GUILDS: dict[str, str] = {
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

COLLEGES: dict[str, str] = {
    'Silverquill': "WB",
    'Lorehold': "WR",
    'Prismari': "UR",
    'Quandrix': "UG",
    'Witherbloom': "BG"
}

WEDGES: dict[str, str] = {
    'Jeskai': "WUR",
    'Mardu': "WBR",
    'Abzan': "WBG",
    'Sultai': "UBG",
    'Temur': "URG"
}

TRIOMES: dict[str, str] = {
    'Raugrin': "WUR",
    'Savai': "WBR",
    'Indatha': "WBG",
    'Zagoth': "UBG",
    'Ketria': "URG"
}

SHARDS: dict[str, str] = {
    'Esper': "WUB",
    'Bant': "WUG",
    'Naya': "WRG",
    'Grixis': "UBR",
    'Jund': "BRG"
}

FAMILIES: dict[str, str] = {
    'Obscura': "WUB",
    'Brokers': "WUG",
    'Cabaretti': "WRG",
    'Maestros': "UBR",
    'Riveteers': "BRG"
}

NEPHILLIM: dict[str, str] = {
    'Yore': "WUBR",
    'Witch': "WUBG",
    'Ink': "WURG",
    'Dune': "WBRG",
    'Glint': "UBRG"
}


# Groupings of colour-combinations supported.
COLOR_ALIAS_GROUPS: dict[str, dict[str, str]] = {
    'Mono-Color': SINGLE_COLORS,
    'Guilds': GUILDS,
    'Colleges': COLLEGES,
    'Wedges': WEDGES,
    'Triomes': TRIOMES,
    'Shards': SHARDS,
    'Families': FAMILIES,
    'Nephillim': NEPHILLIM
}

# Aliases for the colour combinations.
COLOR_ALIASES: dict[str, str] = {
    'None': '',
    'Any': '',
    '': '',
    **SINGLE_COLORS,
    **GUILDS,
    **COLLEGES,
    **WEDGES,
    **TRIOMES,
    **SHARDS,
    **FAMILIES,
    **NEPHILLIM,
    'WUBRG': 'WUBRG',
    '5-Color': 'WUBRG',
    'Five-Color': 'WUBRG',
    'All': 'WUBRG'
}

SIMPLE_COLOR_ALIASES: dict[str, str] = {
    '': '',
    **SINGLE_COLORS,
    **GUILDS,
    **WEDGES,
    **SHARDS,
    **NEPHILLIM,
    'Five-Color': 'WUBRG'
}


# Groups of aliases based on the number of colours.
COLOUR_GROUPINGS: dict[str, dict[str, str]] = {
    'Any': {'': ''},
    'Mono-Color': SINGLE_COLORS,
    'Two-Color': GUILDS,
    'Three-Color': WEDGES | SHARDS,
    'Four-Color': NEPHILLIM,
    'Five-Color': {'Five-Color': 'WUBRG'}
}


# Lists of colour combinations of given length.
COLOR_COMBINATIONS: list[str] = [COLOUR_GROUPINGS[x][y] for x in COLOUR_GROUPINGS for y in COLOUR_GROUPINGS[x]]
COLOR_SINGLES: list[str] = [colors for colors in COLOR_COMBINATIONS if len(colors) == 1]
COLOR_PAIRS: list[str] = [colors for colors in COLOR_COMBINATIONS if len(colors) == 2]
COLOR_TRIPLES: list[str] = [colors for colors in COLOR_COMBINATIONS if len(colors) == 3]
COLOR_QUADRUPLES: list[str] = [colors for colors in COLOR_COMBINATIONS if len(colors) == 4]


# Used for sorting.
COLOR_INDEXES = {COLOR_COMBINATIONS[x]: x for x in range(0, len(COLOR_COMBINATIONS))}
