"""
Contains a (hopefully) comprehensive set of dictionaries which map common
written/spoken names to an associated colour combination.

As well, the key-value pairs in these dictionaries are all in 'Pentad' order,
for iterating purposes.
"""

# region Single Color Groups
SINGLE_COLOR_MAP: dict[str, str] = {
    'White': "W",
    'Blue': "U",
    'Black': "B",
    'Red': "R",
    'Green': "G"
}

MONO_COLOR_MAP: dict[str, str] = {
    'Mono-White': "W",
    'Mono-Blue': "U",
    'Mono-Black': "B",
    'Mono-Red': "R",
    'Mono-Green': "G"
}
# endregion Single Color Groups

# region Two Colour Groups
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

ALLIED_GUILDS: dict[str, str] = {
    'Azorius': "WU",
    'Dimir': "UB",
    'Rakdos': "BR",
    'Gruul': "RG",
    'Selesnya': "WG"
}

ENEMY_GUILDS: dict[str, str] = {
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
NEPHILLIM: dict[str, str] = {
    'Yore': "WUBR",
    'Witch': "WUBG",
    'Ink': "WURG",
    'Dune': "WBRG",
    'Glint': "UBRG"
}

NON_COLOR: dict[str, str] = {
    'Non-G': "WUBR",
    'Non-R': "WUBG",
    'Non-B': "WURG",
    'Non-U': "WBRG",
    'Non-W': "UBRG"
}
# endregion Four Colour Groups

# region Five Colour Groups
ALL_COLOURS_ALIASES: dict[str, str] = {
        'WUBRG': 'WUBRG',
        '5-Color': 'WUBRG',
        'Five-Color': 'WUBRG',
        'All': 'WUBRG'
    }
# endregion Five Colour Groups

# region Any Colour Groups
ANY_COLOURS_ALIASES: dict[str, str] = {
        None: '',
        'None': '',
        'Any': '',
        '': ''
    }
# endregion Any Colour Groups


# region Master Alias Mappings
# Aliases for the colour combinations.
ALIAS_MAP: dict[str, str] = {
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

# Groupings of colour-combinations supported.
GROUPED_ALIAS_MAP: dict[str, dict[str, str]] = {
    'Any': ANY_COLOURS_ALIASES,
    'Single-Color': SINGLE_COLOR_MAP,
    'Mono-Color': MONO_COLOR_MAP,
    'Allied': ALLIED_GUILDS,
    'Enemy': ENEMY_GUILDS,
    'Guilds': GUILDS,
    'Colleges': COLLEGES,
    'Wedges': WEDGES,
    'Triomes': TRIOMES,
    'Shards': SHARDS,
    'Families': FAMILIES,
    'Nephillim': NEPHILLIM,
    'Non-': NON_COLOR,
    'All': ALL_COLOURS_ALIASES
}
# endregion Master Alias Mappings
