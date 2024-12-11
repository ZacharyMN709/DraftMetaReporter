import logging
from typing import Optional

from core.data_requesting import RequestScryfall
from core.game_metadata.game_objects.Card import Card


REQUESTER = RequestScryfall()


def from_query(query: str) -> list[Card]:
    # Otherwise, get the card info from scryfall.
    results = REQUESTER.get_by_query(query)
    return [Card(json) for json in results]


def get_land_type(landtype: str, count: int = 1, oracle_tag: str = None) -> list[tuple[str, str, int]]:
    if oracle_tag:
        cards = from_query(f"oracletag:{oracle_tag}")
    else:
        cards = from_query(f"is:{landtype}")
    lands = [(card.NAME, landtype.title(), count) for card in cards]
    for name, category, count in lands:
        print(f"{count}x {name} [{category}]")
    print()
    return lands


if __name__ == "__main__":
    pass
    #get_land_type("shockland", 3)
    #get_land_type("fetchland", 3)
    #get_land_type("pathway", 1)
    #get_land_type("filterland", 2)
    #get_land_type("triome", 2)

    #get_land_type("checkland", 2)
    #get_land_type("fastland", 2)
    #get_land_type("slowland", 2)
    #get_land_type("triland", 1)

    #get_land_type("battlebondland", 3)
    #get_land_type("Artifact Land", 1, "cycle-mrd-artifact-land")
    #get_land_type("surveilland", 2, "cycle-mkm-surveil-land")
    #get_land_type("LTR Land", 2, "cycle-ltr-legendary-land")
    #get_land_type("channelland", 2, "cycle-neo-legendary-land")

    # get_land_type("painland", 3)

