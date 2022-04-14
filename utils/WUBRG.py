# Colour Mapping
COLORS: str = "WUBRG"

# Groupings of colour-sets supported.
COLOR_ALIASES_SUPPORT: dict[str, dict[str, str]] = {
    'Colors': {
        'White': "W",
        'Blue': "U",
        'Black': "B",
        'Red': "R",
        'Green': "G"
    },
    'Guilds': {
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
    },
    'Colleges': {
        'Silverquill': "WB",
        'Lorehold': "WR",
        'Prismari': "UR",
        'Quandrix': "UG",
        'Witherbloom': "BG"
    },
    'Wedges': {
        'Jeskai': "WUR",
        'Mardu': "WBR",
        'Abzan': "WBG",
        'Sultai': "UBG",
        'Temur': "URG"
    },
    'Triomes': {
        'Raugrin': "WUR",
        'Savai': "WBR",
        'Indatha': "WBG",
        'Zagoth': "UBG",
        'Ketria': "URG"
    },
    'Shards': {
        'Esper': "WUB",
        'Bant': "WUG",
        'Naya': "WRG",
        'Grixis': "UBR",
        'Jund': "BRG"
    },
    'Nephillim': {
        'Yore': "WUBR",
        'Witch': "WUBG",
        'Ink': "WURG",
        'Dune': "WBRG",
        'Glint': "UBRG"
    }
}

# Merging all of the supported colour-sets.
COLOR_ALIASES: dict[str, str] = {
    '5-Color': "WUBRG",
    'All': "WUBRGC",
    'None': ""
}

for d in COLOR_ALIASES_SUPPORT:
    COLOR_ALIASES = COLOR_ALIASES | COLOR_ALIASES_SUPPORT[d]
    # COLOR_ALIASES = {**COLOR_ALIASES, **COLOR_ALIASES_SUPPORT[d]}

# Lists of aliases based on the number of colours.
COLOUR_GROUPINGS: dict[str, dict[str, str]] = {
    'Mono-Color': COLOR_ALIASES_SUPPORT['Colors'],
    'Two-Color': COLOR_ALIASES_SUPPORT['Guilds'],
    'Three-Color': COLOR_ALIASES_SUPPORT['Wedges'] | COLOR_ALIASES_SUPPORT['Shards'],
    # 'Three-Color': {**COLOR_ALIASES_SUPPORT['Wedges'], **COLOR_ALIASES_SUPPORT['Shards']},
    'Four-Color': COLOR_ALIASES_SUPPORT['Nephillim'],
}

COLOR_COUNT_MAP: dict[str, int] = {
    "Mono-color": 1,
    "Two-color": 2,
    "Three-color": 3,
    "Four-color": 4,
    "Five-color": 5,
    "All Decks": None
}


def get_color_string(s: str) -> str:
    """
    Takes in a string, and attempts to convert it to a color string.
    If the string is invalid, returns 'WUBRGC'.
    This function will attempt to convert common names into their colours.
    Eg. 'Bant' -> 'WUG'
    :param s: The string to convert.
    :return: A color string, which contains only characters found in 'WUBRGC'.
    """
    s = s.upper()

    if s.title() in COLOR_ALIASES:
        s = COLOR_ALIASES[s.title()]

    # Validate the string by using the set difference
    valid_chars = set(COLOR_ALIASES['All'])
    char_set = set(s)
    remainder = char_set - valid_chars

    if len(remainder) > 0:
        print(f'Invalid color string provided: {s}. Converting to "WUBRGC"')
        s = "WUBRGC"

    return s


def get_color_identity(color_string: str) -> str:
    """
    Takes in a color string, and attempts to convert it to a
    color identity string.
    :param color_string: The color string to convert.
    :return: A color identity string, a subset of 'WUBRGC'.
    """
    char_set = set(get_color_string(color_string))
    s = ''
    for c in COLOR_ALIASES['All']:
        if c in char_set:
            s += c
    return s


def get_color_alias(color_string: str) -> str:
    """
    Takes in a colour string and attempts to return a more
    common name for the colors. Eg. 'WUR' -> 'Jeskai'
    :param color_string: The color string to convert.
    :return: A common name which represents the colours in color_string.
    """
    color_identity = get_color_identity(color_string)
    if color_identity == 'WUBRG':
        return '5-Colour'
    elif color_identity == 'All':
        return ''

    for g in COLOUR_GROUPINGS:
        for c in COLOUR_GROUPINGS[g]:
            if color_identity == get_color_string(c):
                alias = c
                if len(color_identity) == 1:
                    alias = 'Mono-' + alias
                return alias


COLOR_GROUPS: list[str] = [''] + [get_color_string(y) for x in COLOUR_GROUPINGS for y in COLOUR_GROUPINGS[x]] + ['WUBRG']
COLOR_PAIRS: list[str] = [COLOR_ALIASES_SUPPORT['Guilds'][key] for key in COLOR_ALIASES_SUPPORT['Guilds']]


# Takes in a valid colour string, or colour string alias,
# and then returns a dictionary of booleans.
def get_color_map(color_str: str):
    s = get_color_string(color_str)
    colors_exist = {'W': False,
                    'U': False,
                    'B': False,
                    'R': False,
                    'G': False,
                    'C': False}

    for c in s:
        colors_exist[c] = True

    return colors_exist


def get_color_supersets(color_id: str, max_len: int = 5, strict: bool = False) -> list[str]:
    """
    Gets all possible permutations of WUBRG which contain the color_id.
    Can limit the length of the permutations returned with l.
    :param color_id: The colours to look for in the permutations.
    :param max_len: The max length of the permutations. Default: 5
    :param strict: Whether the subset should be strict
    :return: A list of color ids.
    """
    color_ids = list()

    cis = set(get_color_string(color_id))
    for c in COLOR_GROUPS:
        if strict:
            if len(c) < max_len and cis < set(c):
                color_ids.append(c)
        else:
            if len(c) <= max_len and cis <= set(c):
                color_ids.append(c)

    return color_ids


def get_color_subsets(color_id: str, min_len: int = 0, strict: bool = False) -> list[str]:
    """
    Gets all possible permutations of WUBRG which are contained in color_id.
    Can limit the length of the permutations returned with l.
    :param color_id: The colours to look for in the permutations.
    :param min_len: The min length of the permutations. Default: 0
    :param strict: Whether the subset should be strict
    :return: A list of color ids.
    """
    colour_ids = list()

    cis = set(get_color_string(color_id))
    for c in COLOR_GROUPS:
        if strict:
            if len(c) > min_len and cis > set(c):
                colour_ids.append(c)
        else:
            if len(c) >= min_len and cis >= set(c):
                colour_ids.append(c)

    return colour_ids
