from __future__ import annotations
from typing import Optional
from datetime import datetime

from Utilities.auto_logging import logging
from game_metadata.GameObjects import Card, Draft


class TrophyStub:

    @classmethod
    def parse_simple_rank(cls, rank_1, rank_2) -> str:
        # TODO: Implement a better version of this.
        return rank_2 if rank_2 else rank_1

    def __init__(self, results):
        self.DECK_ID: str = results['aggregate_id']
        self._DECK: Optional[LimitedDeck] = None
        self.deck_idx: int = results['deck_index']
        self.start_rank: str = results['start_rank']
        self.end_rank: str = results['end_rank']
        self.rank: str = self.parse_simple_rank(self.start_rank, self.end_rank)
        self.time: datetime = datetime.strptime(results['time'], "%m-%d-%y %H:%M")

    @property
    def DECK(self) -> LimitedDeck:
        if self._DECK is None:
            self._DECK = LimitedDeck.from_id(self.DECK_ID)
            self._DECK.trophy_stub = self
        return self._DECK


class Deck:
    name: str
    wins: int
    losses: int
    _maindeck: list[Card] = list()
    _sideboard: list[Card] = list()
    _maindeck_dict: dict[str, int] = dict()
    _sideboard_dict: dict[str, int] = dict()

    @classmethod
    def _gen_card_dict(cls, card_list: list[Card]) -> dict[str, int]:
        card_dict = dict()
        for card in card_list:
            if card.NAME not in card_dict:
                card_dict[card.NAME] = 0
            card_dict[card.NAME] += 1
        return card_dict

    @property
    def maindeck(self) -> list[Card]:
        return self._maindeck

    @property
    def maindeck_dict(self) -> dict[str, int]:
        return self._maindeck_dict

    @maindeck.setter
    def maindeck(self, value):
        self._maindeck = value
        self._maindeck_dict = self._gen_card_dict(value)

    @property
    def sideboard(self) -> list[Card]:
        return self._sideboard

    @property
    def sideboard_dict(self) -> dict[str, int]:
        return self._sideboard_dict

    @sideboard.setter
    def sideboard(self, value):
        self._sideboard = value
        self._sideboard_dict = self._gen_card_dict(value)

    @property
    def cardpool(self) -> list[Card]:
        return self.maindeck + self.sideboard

    @property
    def win_rate(self) -> float:
        denominator = self.wins + self.losses
        if denominator == 0:
            return 0
        else:
            return self.wins / denominator

    def compare_decks(self, deck):
        # TODO: Compare the current deck with the other deck.
        # TODO: Figure out out to format the differences to return.
        raise NotImplementedError()
        pass


class LimitedDeck(Deck):
    URL_ROOT = "https://www.17lands.com"

    @classmethod
    def from_id(cls, deck_id: str) -> LimitedDeck:
        result = None  # Get `result` with `deck_id`
        return LimitedDeck(result)

    def __init__(self, result: dict):
        # Isolate the event metadata and track the key parts of it.
        event_info = result['event_info']
        self.DECK_ID: str = event_info['id']
        self.SET: str = event_info['expansion']
        self.FORMAT: str = event_info['format']
        self._DRAFT: Optional[Draft] = None
        self.trophy_stub: Optional[TrophyStub] = None

        # Store the more cursory information.
        self.name = f"{self.SET} - {self.FORMAT} ({self.DECK_ID})"
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
        if self._DRAFT is None:
            # TODO: Return the draft on request.
            raise NotImplementedError()
        return self._DRAFT

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


class ConstructedDeck(Deck):
    @classmethod
    def parse_decklist(cls, decklist: str) -> tuple[list[str], list[str]]:
        maindeck = list()
        sideboard = list()
        raise NotImplementedError()

        return maindeck, sideboard

    def __init__(self, name: str, decklist: str):
        self.name = name
        self.maindeck, self.sideboard = self.parse_decklist(decklist)


class DeckManager:
    """

    """
    # Used to maintain a constant-time lookup cache of previously requested cards.
    SETS: dict[str, dict[str, LimitedDeck]] = dict()
    DECKS: dict[str, Optional[LimitedDeck]] = dict()

    @classmethod
    def _add_deck(cls, deck: LimitedDeck, force_update=True) -> None:
        """
        An internal method to help more easily track decks as they're found/fetched.
        :param deck: The decks object to track
        """
        # If the deck object isn't tracked in DECKS, add it to DECKS and SETS.
        if deck.DECK_ID not in cls.DECKS or force_update:

            # If the set the deck is from doesn't exist in the dictionary, initialize an empty dictionary.
            if deck.SET not in cls.SETS:
                cls.SETS[deck.SET] = dict()
            cls.DECKS[deck.DECK_ID] = deck
            cls.SETS[deck.SET][deck.DECK_ID] = deck

    @classmethod
    def from_deck_id(cls, deck_id: str) -> Optional[LimitedDeck]:
        """
        Searches for a card by name. If not already known, will attempt to query Scryfall for
        the card.
        :param deck_id: The name of the card to look for. Can handle inexact names, to an extent.
        :return: A Deck or None
        """
        # If the deck already exists, return it.
        prev_deck, found = cls._find_deck(deck_id)
        if found:
            return prev_deck

        # Otherwise, get the card info from scryfall.
        # TODO: Update this to get the deck from 17Lands.
        json = dict()
        raise NotImplementedError()
        # If there's an error, log it, log the id as None, return None.
        if 'err_msg' in json:
            logging.info(f"Could not get deck with deck_id: '{deck_id}'")
            logging.info(f"Error: {json['err_msg']}")
            cls.DECKS[deck_id] = None
            return None
        # If the deck is found, return it.
        else:
            deck = LimitedDeck(json)
            cls._add_deck(deck)
            return deck

    @classmethod
    def _find_deck(cls, deck_id: str) -> tuple[Optional[LimitedDeck], bool]:
        """
        Attempts to find a saved instance of a card.
        :param deck_id: The card name to find
        :return: A Card or None, and whether the name exists in REDIRECT
        """

        if deck_id in cls.DECKS:
            return cls.DECKS[deck_id], True
        else:
            return None, False

    @classmethod
    def clear_blank_decks(cls) -> None:
        for deck_id in cls.DECKS:
            if cls.DECKS[deck_id] is None:
                del cls.DECKS[deck_id]

    @classmethod
    def flush_cache(cls) -> None:
        """
        Clears the caches of decks.
        """
        del cls.SETS
        del cls.DECKS

        cls.SETS = dict()
        cls.DECKS = dict()
