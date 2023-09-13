# Graphing Defaults
ROLL: int = 3
GRAPH_DIR_NAME: str = 'Images'
GRAPH_DIR_LOC: str = r'C:\Users\Zachary\Coding\GitHub'
DPI: int = 400
ACCREDIT_STR: str = "Data taken from 17Lands"
ACCREDIT_KWARGS: dict[str, str] = {
    'ha': 'center',
    'va': 'bottom',
    'weight': 'demi',
    'size': 'medium',
    'style': 'oblique'
}

FILTER_KWARGS: dict[str, str] = {
    'ha': 'center',
    'va': 'center',
    'weight': 'light',
    'size': 'small',
    'style': 'oblique'
}

TITLE_SIZE: float = 16.5
LABEL_SIZE: float = 13.5

# Type information for colors used in graphing.
Color = tuple[float, float, float, float]

STATS_COLOR_DICT: dict[str, Color] = {
    'GIH WR': (0.33, 0.66, 0.41, 0.9),
    'GND WR': (0.77, 0.31, 0.32, 0.9),
    'ATA': (0.87, 0.52, 0.32, 0.9),
    'ALSA': (0.3, 0.45, 0.69, 0.9),
    '# GP': (0.51, 0.45, 0.7, 0.9),
    '# GIH': (0.33, 0.66, 0.41, 0.9),
    '# Picked': (0.87, 0.52, 0.32, 0.9),
    '# Seen': (0.3, 0.45, 0.69, 0.9)
}


ARCHETYPES_COLOR_DICT: dict[str, Color] = {
             'WG': (0.87, 0.52, 0.32, 0.9),
             'WU': (0.3, 0.45, 0.69, 0.9),
             'UB': (0.15, 0.15, 0.15, 0.9),
             'BR': (0.77, 0.31, 0.32, 0.9),
             'RG': (0.33, 0.66, 0.41, 0.9),

             'WB': (0.87, 0.52, 0.32, 0.65),
             'UR': (0.3, 0.45, 0.69, 0.65),
             'BG': (0.15, 0.15, 0.15, 0.65),
             'WR': (0.77, 0.31, 0.32, 0.65),
             'UG': (0.33, 0.66, 0.41, 0.65),

             'WUG': (0.87, 0.52, 0.32, 0.65),
             'WUB': (0.3, 0.45, 0.69, 0.65),
             'UBR': (0.15, 0.15, 0.15, 0.65),
             'BRG': (0.77, 0.31, 0.32, 0.65),
             'WRG': (0.33, 0.66, 0.41, 0.65),

             'ALL': (0.9, 0.3, 0.9, 0.9),
             '1C': (0.8, 0.4, 0.8, 0.65),
             '2C': (0.7, 0.2, 0.7, 0.65),
             '3C': (0.5, 0.2, 0.5, 0.65),
             '4C': (0.4, 0.1, 0.4, 0.65),
             '5C': (0.3, 0.1, 0.3, 0.65)
}
