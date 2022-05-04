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

STATS_COLOR_DICT = {
    'GIH WR': (0.33, 0.66, 0.41, 0.9),
    'GND WR': (0.77, 0.31, 0.32, 0.9),
    'ATA': (0.87, 0.52, 0.32, 0.9),
    'ALSA': (0.3, 0.45, 0.69, 0.9),
    '# GP': (0.51, 0.45, 0.7, 0.9),
    '# GIH': (0.33, 0.66, 0.41, 0.9),
    '# Picked': (0.87, 0.52, 0.32, 0.9),
    '# Seen': (0.3, 0.45, 0.69, 0.9)
}


ARCHETYPES_COLOR_DICT = {
    'WU': (0.3, 0.45, 0.69, 0.9),
    'WB': (0.00, 0.00, 0.00),
    'WR': (0.00, 0.00, 0.00),
    'WG': (0.87, 0.52, 0.32, 0.9),
    'UB': (0.00, 0.00, 0.00),
    'UR': (0.00, 0.00, 0.00),
    'UG': (0.00, 0.00, 0.00),
    'BR': (0.77, 0.31, 0.32, 0.9),
    'BG': (0.00, 0.00, 0.00),
    'RG': (0.33, 0.66, 0.41, 0.9),
    'AVG': (0.00, 0.00, 0.00),
    '1C': (0.00, 0.00, 0.00),
    '2C': (0.00, 0.00, 0.00),
    '3C': (0.00, 0.00, 0.00),
    '4C': (0.00, 0.00, 0.00),
    '5C': (0.00, 0.00, 0.00)
}
