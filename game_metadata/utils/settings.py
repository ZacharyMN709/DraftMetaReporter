from datetime import date

# Game Format Defaults and Data
SETS: list[str] = ["SNC", "NEO", "VOW", "MID"]

FORMATS: list[str] = ["PremierDraft", "TradDraft", "QuickDraft"]

# TODO: Change this so the dates are formatted strings, and the Set/FormatMetadata objects parse the dates on load.
#  This will allow for the SET_CONFIG to be updated from a JSON file and have the Set/FormatMetadata objects re-
#  parse the data to update the sets information.
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
