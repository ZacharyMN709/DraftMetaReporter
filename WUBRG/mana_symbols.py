"""
Lists of mana/cost symbols in their formatted ("{X}") and regular ("X") forms.
More info: https://api.scryfall.com/symbology
"""

from WUBRG.typing import FORMATTED_MANA_SYMBOL, MANA_SYMBOL

# region Formatted Mana Symbols
FORMATTED_BASE_MANA_SYMBOLS: list[FORMATTED_MANA_SYMBOL] = [
    "{W}", "{U}", "{B}", "{R}", "{G}", "{C}"
]

FORMATTED_NUMERIC_MANA_SYMBOLS: list[FORMATTED_MANA_SYMBOL] = [
    "{0}", "{1}", "{2}", "{3}", "{4}", "{5}", "{6}", "{7}", "{8}", "{9}", "{10}",
    "{11}", "{12}", "{13}", "{14}", "{15}", "{16}", "{17}", "{18}", "{19}", "{20}"
]

FORMATTED_HYBRID_MANA_SYMBOLS: list[FORMATTED_MANA_SYMBOL] = [
    "{W/U}", "{W/B}", "{B/R}", "{B/G}", "{U/B}",
    "{U/R}", "{R/G}", "{R/W}", "{G/W}", "{G/U}"
]

FORMATTED_PHYREXIAN_MANA_SYMBOLS: list[FORMATTED_MANA_SYMBOL] = [
    "{W/P}", "{U/P}", "{B/P}", "{R/P}", "{G/P}"
]

FORMATTED_HYBRID_PHYREXIAN_MANA_SYMBOLS: list[FORMATTED_MANA_SYMBOL] = [
    "{B/G/P}", "{B/R/P}", "{G/U/P}", "{G/W/P}", "{R/G/P}",
    "{R/W/P}", "{U/B/P}", "{U/R/P}", "{W/B/P}", "{W/U/P}"
]

FORMATTED_COLORLESS_HYBRID_MANA_SYMBOLS: list[FORMATTED_MANA_SYMBOL] = [
    "{2/W}", "{2/U}", "{2/B}", "{2/R}", "{2/G}"
]

FORMATTED_SPECIAL_MANA_SYMBOLS: list[FORMATTED_MANA_SYMBOL] = [
    "{A}", "{X}", "{Y}", "{Z}", "{S}"
]

FORMATTED_COST_SYMBOLS: list[FORMATTED_MANA_SYMBOL] = [
    "{T}", "{Q}", "{E}"
]

FORMATTED_MANA_SYMBOLS: list[FORMATTED_MANA_SYMBOL] = \
    FORMATTED_BASE_MANA_SYMBOLS + FORMATTED_NUMERIC_MANA_SYMBOLS + FORMATTED_HYBRID_MANA_SYMBOLS \
    + FORMATTED_PHYREXIAN_MANA_SYMBOLS + FORMATTED_HYBRID_PHYREXIAN_MANA_SYMBOLS \
    + FORMATTED_COLORLESS_HYBRID_MANA_SYMBOLS + FORMATTED_SPECIAL_MANA_SYMBOLS + FORMATTED_COST_SYMBOLS
# endregion Formatted Mana Symbols


# region Mana Symbols
BASE_MANA_SYMBOLS: list[MANA_SYMBOL] = [
    "W", "U", "B", "R", "G", "C"
]

NUMERIC_MANA_SYMBOLS: list[MANA_SYMBOL] = [
    "0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10",
    "11", "12", "13", "14", "15", "16", "17", "18", "19", "20"
]

HYBRID_MANA_SYMBOLS: list[MANA_SYMBOL] = [
    "W/U", "W/B", "B/R", "B/G", "U/B", "U/R", "R/G", "R/W", "G/W", "G/U"
]

PHYREXIAN_MANA_SYMBOLS: list[MANA_SYMBOL] = [
    "W/P", "U/P", "B/P", "R/P", "G/P"
]

HYBRID_PHYREXIAN_MANA_SYMBOLS: list[MANA_SYMBOL] = [
    "B/G/P", "B/R/P", "G/U/P", "G/W/P", "R/G/P",
    "R/W/P", "U/B/P", "U/R/P", "W/B/P", "W/U/P"
]

COLORLESS_HYBRID_MANA_SYMBOLS: list[MANA_SYMBOL] = [
    "2/W", "2/U", "2/B", "2/R", "2/G"
]

SPECIAL_MANA_SYMBOLS: list[MANA_SYMBOL] = [
    "A", "X", "Y", "Z", "S"
]

COST_SYMBOLS: list[MANA_SYMBOL] = [
    "T", "Q", "E"
]

MANA_SYMBOLS: list[MANA_SYMBOL] = \
    BASE_MANA_SYMBOLS + NUMERIC_MANA_SYMBOLS + HYBRID_MANA_SYMBOLS \
    + PHYREXIAN_MANA_SYMBOLS + HYBRID_PHYREXIAN_MANA_SYMBOLS \
    + COLORLESS_HYBRID_MANA_SYMBOLS + SPECIAL_MANA_SYMBOLS + COST_SYMBOLS
# endregion Mana Symbols
