from __future__ import annotations
from typing import Optional
from datetime import datetime

from game_metadata.GameObjects import Card, Draft


class TrophyStub:

    def __init__(self, results):
        self.DECK_ID: str = results['aggregate_id']
        self._DECK: Optional[Deck] = None
        self.deck_idx: int = results['deck_index']
        self.start_rank: str = results['start_rank']
        self.end_rank: str = results['end_rank']
        self.rank: str = self.end_rank if self.end_rank else self.start_rank
        self.time: datetime = datetime.strptime(results['time'], "%m-%d-%y %H:%M")

    @property
    def DECK(self) -> Deck:
        if self._DECK is None:
            self._DECK = Deck.from_id(self.DECK_ID)
        return self._DECK


class Deck:
    URL_ROOT = "https://www.17lands.com"

    @classmethod
    def from_id(cls, deck_id: str) -> Deck:
        result = None  # Get `result` with `deck_id`
        return Deck(result)

    def __init__(self, result: dict):
        # Isolate the event metadata and track the key parts of it.
        event_info = result['event_info']
        self.DECK_ID: str = event_info['id']
        self.SET: str = event_info['expansion']
        self.FORMAT: str = event_info['format']

        # Store the more cursory information.
        self.wins: int = event_info['wins']
        self.losses: int = event_info['losses']
        self.deck_builds: int = len(event_info['deck_links'])
        self.selected_build: int = self.deck_builds - 1

        # Isolate the lists of cards from the data.
        pre_maindeck = result['groups'][0]["cards"]
        pre_sideboard = result['groups'][1]["cards"]
        self.maindeck: list[Card] = [Card.from_name(card_dict['name']) for card_dict in pre_maindeck]
        self.sideboard: list[Card] = [Card.from_name(card_dict['name']) for card_dict in pre_sideboard]

    @property
    def details_link(self) -> str:
        return f"{self.URL_ROOT}/details/{self.DECK_ID}"

    @property
    def pool_link(self) -> str:
        return f"{self.URL_ROOT}/pool/{self.DECK_ID}"

    @property
    def draft_link(self) -> str:
        return f"{self.URL_ROOT}/draft/{self.DECK_ID}"

    @property
    def DRAFT(self) -> Draft:
        # TODO: Return the draft on request.
        return None

    # Properties that can have multiple links based on different deck builds.
    @property
    def builder_link(self) -> str:
        return f"https://sealeddeck.tech/17lands/deck/{self.DECK_ID}/{self.selected_build}"

    @property
    def deck_link(self) -> str:
        return f"{self.URL_ROOT}/deck/{self.DECK_ID}/{self.selected_build}"

    @property
    def text_link(self) -> str:
        return f"{self.URL_ROOT}/deck/{self.DECK_ID}/{self.selected_build}.txt"


class DeckManager:

    def __init__(self):
        pass
