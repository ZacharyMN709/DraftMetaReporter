"""
Contains a (hopefully) comprehensive set of dictionaries which map common
written/spoken names to an associated colour combination.

As well, the key-value pairs in these dictionaries are all in 'Pentad' order,
for iterating purposes.
"""

from WUBRG.typing import COLOR_IDENTITY, COLOR_ALIAS_ALL

# region Single Color Groups
SINGLE_COLOR_MAP: dict[COLOR_ALIAS_ALL, COLOR_IDENTITY] = {
    'White': "W",
    'Blue': "U",
    'Black': "B",
    'Red': "R",
    'Green': "G",
}

MONO_COLOR_MAP: dict[COLOR_ALIAS_ALL, COLOR_IDENTITY] = {
    'Mono-White': "W",
    'Mono-Blue': "U",
    'Mono-Black': "B",
    'Mono-Red': "R",
    'Mono-Green': "G"
}

KINGDOM_COLOR_MAP: dict[COLOR_ALIAS_ALL, COLOR_IDENTITY] = {
    'Ardenvale': "W",
    'Vantress': "U",
    'Locthwain': "B",
    'Embereth': "R",
    'Garenbrig': "G",
}

MIRRODIN_COLOR_MAP: dict[COLOR_ALIAS_ALL, COLOR_IDENTITY] = {
    'Auriok': "W",
    'Neurok': "U",
    'Moriok': "B",
    'Vulshok': "R",
    'Sylvok': "G",
}
# endregion Single Color Groups

# region Two Colour Groups
GUILDS: dict[COLOR_ALIAS_ALL, COLOR_IDENTITY] = {
    'Azorius': "WU",
    'Dimir': "UB",
    'Rakdos': "BR",
    'Gruul': "RG",
    'Selesnya': "WG",
    'Orzhov': "WB",
    'Golgari': "BG",
    'Simic': "UG",
    'Izzet': "UR",
    'Boros': "WR",
}

ALLIED_GUILDS: dict[COLOR_ALIAS_ALL, COLOR_IDENTITY] = {
    'Azorius': "WU",
    'Dimir': "UB",
    'Rakdos': "BR",
    'Gruul': "RG",
    'Selesnya': "WG",
}

DRAGONLORDS: dict[COLOR_ALIAS_ALL, COLOR_IDENTITY] = {
    'Ojutai': "WU",
    'Silumgar': "UB",
    'Kolaghan': "BR",
    'Atarka': "RG",
    'Dromoka': "WG",
}

ENEMY_GUILDS: dict[COLOR_ALIAS_ALL, COLOR_IDENTITY] = {
    'Orzhov': "WB",
    'Golgari': "BG",
    'Simic': "UG",
    'Izzet': "UR",
    'Boros': "WR",
}

COLLEGES: dict[COLOR_ALIAS_ALL, COLOR_IDENTITY] = {
    'Silverquill': "WB",
    'Witherbloom': "BG",
    'Quandrix': "UG",
    'Prismari': "UR",
    'Lorehold': "WR",
}
# endregion Two Colour Groups

# region Three Colour Groups
WEDGES: dict[COLOR_ALIAS_ALL, COLOR_IDENTITY] = {
    'Jeskai': "WUR",
    'Sultai': "UBG",
    'Mardu': "WBR",
    'Temur': "URG",
    'Abzan': "WBG",
}

TRIOMES: dict[COLOR_ALIAS_ALL, COLOR_IDENTITY] = {
    'Raugrin': "WUR",
    'Zagoth': "UBG",
    'Savai': "WBR",
    'Ketria': "URG",
    'Indatha': "WBG",
}

CHAOS_DRAGONS: dict[COLOR_ALIAS_ALL, COLOR_IDENTITY] = {
    'Numot': "WUR",
    'Vorosh': "UBG",
    'Oros': "WBR",
    'Intet': "URG",
    'Teneb': "WBG",
}

VOLVERS: dict[COLOR_ALIAS_ALL, COLOR_IDENTITY] = {
    'Raka': "WUR",
    'Ana': "UBG",
    'Dega': "WBR",
    'Ceta': "URG",
    'Necra': "WBG",
}

SHARDS: dict[COLOR_ALIAS_ALL, COLOR_IDENTITY] = {
    'Esper': "WUB",
    'Grixis': "UBR",
    'Jund': "BRG",
    'Naya': "WRG",
    'Bant': "WUG",
}

FAMILIES: dict[COLOR_ALIAS_ALL, COLOR_IDENTITY] = {
    'Obscura': "WUB",
    'Maestros': "UBR",
    'Riveteers': "BRG",
    'Cabaretti': "WRG",
    'Brokers': "WUG",
}
# endregion Three Colour Groups

# region Four Colour Groups
NEPHILLIM: dict[COLOR_ALIAS_ALL, COLOR_IDENTITY] = {
    'Yore': "WUBR",
    'Witch': "WUBG",
    'Ink': "WURG",
    'Dune': "WBRG",
    'Glint': "UBRG",
}

OFFICIAL_FOUR_COLOUR: dict[COLOR_ALIAS_ALL, COLOR_IDENTITY] = {
    'Artifice': "WUBR",
    'Growth': "WUBG",
    'Altruism': "WURG",
    'Aggression': "WBRG",
    'Chaos': "UBRG",
}

NON_COLOR: dict[COLOR_ALIAS_ALL, COLOR_IDENTITY] = {
    'Non-G': "WUBR",
    'Non-R': "WUBG",
    'Non-B': "WURG",
    'Non-U': "WBRG",
    'Non-W': "UBRG",
}
# endregion Four Colour Groups

# region Five Colour Groups
ALL_COLOURS_ALIASES: dict[COLOR_ALIAS_ALL, COLOR_IDENTITY] = {
        'WUBRG': 'WUBRG',
        '5-Color': 'WUBRG',
        'Five-Color': 'WUBRG',
        'All': 'WUBRG',
    }
# endregion Five Colour Groups

# region Any Colour Groups
ANY_COLOURS_ALIASES: dict[COLOR_ALIAS_ALL, COLOR_IDENTITY] = {
        None: '',
        'None': '',
        'Any': '',
        '': '',
    }
# endregion Any Colour Groups


# region Master Alias Mappings
# Aliases for the colour combinations.
ALIAS_MAP: dict[COLOR_ALIAS_ALL, COLOR_IDENTITY] = {
    **ANY_COLOURS_ALIASES,
    **SINGLE_COLOR_MAP,
    **GUILDS,
    **COLLEGES,
    **WEDGES,
    **TRIOMES,
    **SHARDS,
    **FAMILIES,
    **NEPHILLIM,
    **ALL_COLOURS_ALIASES,
}

# Groupings of colour-combinations supported.
GROUPED_ALIAS_MAP: dict[str, dict[COLOR_ALIAS_ALL, COLOR_IDENTITY]] = {
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
    'All': ALL_COLOURS_ALIASES,
}
# endregion Master Alias Mappings
