"""
Lists of mana/cost symbols in their raw ("{X}") and regular ("X") forms.
More info: https://api.scryfall.com/symbology
"""

RAW_BASE_MANA_SYMBOLS: list[str] = ["{W}", "{U}", "{B}", "{R}", "{G}", "{C}"]
RAW_NUMERIC_MANA_SYMBOLS: list[str] = ["{0}", "{1}", "{2}", "{3}", "{4}", "{5}", "{6}", "{7}", "{8}", "{9}", "{10}",
                                       "{11}", "{12}", "{13}", "{14}", "{15}", "{16}", "{17}", "{18}", "{19}", "{20}"]
RAW_HYBRID_MANA_SYMBOLS: list[str] = ["{W/U}", "{W/B}", "{B/R}", "{B/G}", "{U/B}",
                                      "{U/R}", "{R/G}", "{R/W}", "{G/W}", "{G/U}"]
RAW_PHYREXIAN_MANA_SYMBOLS: list[str] = ["{W/P}", "{U/P}", "{B/P}", "{R/P}", "{G/P}"]
RAW_HYBRID_PHYREXIAN_MANA_SYMBOLS: list[str] = ["{B/G/P}", "{B/R/P}", "{G/U/P}", "{G/W/P}", "{R/G/P}",
                                                "{R/W/P}", "{U/B/P}", "{U/R/P}", "{W/B/P}", "{W/U/P}"]
RAW_COLORLESS_HYBRID_MANA_SYMBOLS: list[str] = ["{2/W}", "{2/U}", "{2/B}", "{2/R}", "{2/G}"]
RAW_SPECIAL_MANA_SYMBOLS: list[str] = ["{A}", "{X}", "{Y}", "{Z}", "{S}"]
RAW_COST_SYMBOLS: list[str] = ["{T}", "{Q}", "{E}"]

RAW_MANA_SYMBOLS: list[str] = RAW_BASE_MANA_SYMBOLS + RAW_NUMERIC_MANA_SYMBOLS + RAW_HYBRID_MANA_SYMBOLS \
                             + RAW_PHYREXIAN_MANA_SYMBOLS + RAW_HYBRID_PHYREXIAN_MANA_SYMBOLS \
                             + RAW_COLORLESS_HYBRID_MANA_SYMBOLS + RAW_SPECIAL_MANA_SYMBOLS + RAW_COST_SYMBOLS


BASE_MANA_SYMBOLS: list[str] = ["W", "U", "B", "R", "G", "C"]
NUMERIC_MANA_SYMBOLS: list[str] = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10",
                                   "11", "12", "13", "14", "15", "16", "17", "18", "19", "20"]
HYBRID_MANA_SYMBOLS: list[str] = ["W/U", "W/B", "B/R", "B/G", "U/B", "U/R", "R/G", "R/W", "G/W", "G/U"]
PHYREXIAN_MANA_SYMBOLS: list[str] = ["W/P", "U/P", "B/P", "R/P", "G/P"]
HYBRID_PHYREXIAN_MANA_SYMBOLS: list[str] = ["B/G/P", "B/R/P", "G/U/P", "G/W/P", "R/G/P",
                                            "R/W/P", "U/B/P", "U/R/P", "W/B/P", "W/U/P"]
COLORLESS_HYBRID_MANA_SYMBOLS: list[str] = ["2/W", "2/U", "2/B", "2/R", "2/G"]
SPECIAL_MANA_SYMBOLS: list[str] = ["A", "X", "Y", "Z", "S"]
COST_SYMBOLS: list[str] = ["T", "Q", "E"]

MANA_SYMBOLS: list[str] = BASE_MANA_SYMBOLS + NUMERIC_MANA_SYMBOLS + HYBRID_MANA_SYMBOLS \
                         + PHYREXIAN_MANA_SYMBOLS + HYBRID_PHYREXIAN_MANA_SYMBOLS \
                         + COLORLESS_HYBRID_MANA_SYMBOLS + SPECIAL_MANA_SYMBOLS + COST_SYMBOLS
