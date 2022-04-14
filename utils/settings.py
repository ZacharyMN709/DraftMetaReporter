from datetime import date

# Game Format Defaults and Data
SETS: list[str] = ["SNC", "NEO", "VOW", "MID"]

FORMATS: list[str] = ["PremierDraft", "TradDraft", "QuickDraft"]

SET_CONFIG: dict[str, dict[str, list[tuple[date, date]]]] = {
    "SNC": {
        "PremierDraft": [(date(2022, 4, 28), date(2022, 5, 28))],
        "TradDraft": [(date(2022, 4, 28), date(2022, 5, 28))],
        "QuickDraft": [(date(2022, 5, 13), date(2022, 5, 27))]
    },
    "NEO": {
        "PremierDraft": [(date(2022, 2, 10), date(2022, 4, 28))],
        "TradDraft": [(date(2022, 2, 10), date(2022, 4, 28))],
        "QuickDraft": [(date(2022, 2, 25), date(2022, 3, 11)), (date(2022, 3, 25), date(2022, 4, 8)),
                       (date(2022, 4, 22), date(2022, 4, 29))]
    },
    "VOW": {
        "PremierDraft": [(date(2021, 11, 11), date(2022, 2, 10))],
        "TradDraft": [(date(2021, 11, 11), date(2022, 2, 10))],
        "QuickDraft": [(date(2021, 11, 26), date(2021, 12, 10)), (date(2021, 12, 24), date(2022, 1, 7))]
    },
    "MID": {
        "PremierDraft": [(date(2021, 9, 16), date(2021, 11, 11))],
        "TradDraft": [(date(2021, 9, 16), date(2021, 11, 11))],
        "QuickDraft": [(date(2021, 10, 1), date(2021, 10, 15)), (date(2021, 10, 29), date(2022, 11, 12))]
    }
}

# Web Request Defaults
TRIES: int = 5
FAIL_DELAY: int = 60
SUCCESS_DELAY: int = 1

# Data Storage Defaults
ROOT_DIR: str = '..'
DATA_DIR_NAME: str = '17LandsData'
DATA_DIR_LOC: str = '../..'

# Graphing Defaults
ROLL: int = 3
GRAPH_DIR_NAME: str = 'Graphs'
GRAPH_DIR_LOC: str = '../..'
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
