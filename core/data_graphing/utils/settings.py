# Graphing Defaults
ROLL: int = 3
ALPHA: float = 0.85
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
