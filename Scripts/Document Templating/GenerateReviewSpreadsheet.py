from typing import Any
import pandas as pd

from core.game_metadata import Card

import card_ordering
import caching


def gen_dict_from_card(card: Card, reviewers: list[str] = None) -> dict[str, Any]:
    sanitized_name = card.NAME.replace('"', '')
    mapping_dict = {
        "Card Name": f'=HYPERLINK("{card.URL}", "{sanitized_name}")',
        "Color": card.CAST_IDENTITY,
        "Cost": card.MANA_COST,
        "Rarity": card.RARITY,
        "Type": " ".join(card.TYPES)
    }

    if reviewers:
        for reviewer in reviewers:
            mapping_dict[reviewer] = ""
    return mapping_dict


def gen_review_spreadsheet(file_name: str, set_code: str, reviewers: list[str] = None):
    caching.populate_cache([set_code])
    cards = card_ordering.get_set_order(set_code)
    records = [gen_dict_from_card(card, reviewers) for card in cards]
    frame = pd.DataFrame.from_records(records)
    frame.to_excel(file_name)


if __name__ == "__main__":
    SET = "WOT"
    FILE = f"{SET} Gradings.xlsx"
    REVIEWERS = ["Alex", "Marc"]
    gen_review_spreadsheet(FILE, SET, REVIEWERS)
