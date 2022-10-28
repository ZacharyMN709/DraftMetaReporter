from __future__ import annotations
from typing import Optional
from datetime import datetime
import re

from wubrg import COLOR

from Utilities.auto_logging import logging
from game_metadata.utils.consts import RANKS, new_color_count_dict
from game_metadata.Request17Lands import Request17Lands
from game_metadata.GameObjects.Card import CardManager, Card
import game_metadata.GameObjects.Draft as Draft


trim_numeric = re.compile("-[/d]*]")


class TrophyStub:

    @classmethod
    def parse_simple_rank(cls, rank_1: Optional[str], rank_2: Optional[str]) -> str:
        """
        Merges the start and end rank of a draft into a simpler rank, taking the highest rank.
        Eg. "Silver-1" and "Gold-2" would return "Gold".
        """
        r1 = trim_numeric.sub('', str(rank_1))
        r2 = trim_numeric.sub('', str(rank_2))

        idx1 = RANKS.index(r1)
        idx2 = RANKS.index(r2)

        if idx1 > idx2:
            return r1
        else:
            return r2

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
        """ The deck associated with the draft. """
        if self._DECK is None:
            self._DECK = LimitedDeck.from_id(self.DECK_ID)
            self._DECK.trophy_stub = self
        return self._DECK


class Deck:
    name: str
    wins: int
    losses: int
    _produced_mana: Optional[dict[COLOR, int]]
    _casting_pips: Optional[dict[COLOR, int]]
    _all_pips: Optional[dict[COLOR, int]]
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

    def _get_produced_mana(self) -> dict[COLOR, int]:
        d = new_color_count_dict()
        for card in self.cardpool:
            for mana in card.DEFAULT_FACE.MANA_PRODUCED:
                d[mana] += 1
        return d

    @property
    def produced_mana(self) -> Optional[dict[COLOR, int]]:
        if self._produced_mana is None:
            self._produced_mana = self._get_produced_mana()
        return self._produced_mana

    def _get_casting_pips(self) -> dict[COLOR, int]:
        d = new_color_count_dict()
        for card in self.cardpool:
            for mana in card.DEFAULT_FACE.MANA_COST:
                d[mana] += 1
        return d

    @property
    def casting_pips(self) -> Optional[dict[COLOR, int]]:
        if self._casting_pips is None:
            self._casting_pips = self._get_casting_pips()
        return self._casting_pips

    def _get_all_pips(self) -> dict[COLOR, int]:
        d = new_color_count_dict()
        for card in self.cardpool:
            for mana in card.DEFAULT_FACE.MANA_PRODUCED:
                d[mana] += 1
        return d

    @property
    def all_pips(self) -> Optional[dict[COLOR, int]]:
        if self._all_pips is None:
            self._all_pips = self._get_all_pips()
        return self._all_pips

    @property
    def maindeck(self) -> list[Card]:
        """ The list of cards the deck plays in the maindeck """
        return self._maindeck

    @maindeck.setter
    def maindeck(self, value):
        self._maindeck = value
        self._maindeck_dict = self._gen_card_dict(value)

    @property
    def sideboard(self) -> list[Card]:
        """ The list of cards the deck plays in the sideboard """
        return self._sideboard

    @sideboard.setter
    def sideboard(self, value):
        self._sideboard = value
        self._sideboard_dict = self._gen_card_dict(value)

    @property
    def cardpool(self) -> list[Card]:
        """ The complete list of cards the deck has access to """
        return self.maindeck + self.sideboard

    @property
    def win_rate(self) -> float:
        denominator = self.wins + self.losses
        if denominator == 0:
            return 0
        else:
            return self.wins / denominator

    def compare_decks(self, deck: LimitedDeck) -> tuple[dict[str, int], dict[str, int]]:
        """
        Compares the contents of this deck with a provided deck.
        :param deck: The deck to compare with.
        :return: A maindeck and sideboard dictionary of card number differences.
        """
        def subtract_dicts(d1, d2):
            d = dict()
            for k in d2:
                if k in d1:
                    v = d1[k] - d2[k]
                    if v != 0:
                        d[k] -= v
                else:
                    d[k] = -d2[k]
            return d

        maindeck_diff = subtract_dicts(self._maindeck_dict, deck._maindeck_dict)
        sideboard_diff = subtract_dicts(self._sideboard_dict, deck._sideboard_dict)
        return maindeck_diff, sideboard_diff


class LimitedDeck(Deck):
    URL_ROOT = "https://www.17lands.com"

    @classmethod
    def from_id(cls, deck_id: str) -> LimitedDeck:
        return DeckManager.from_deck_id(deck_id)

    def __init__(self, result: dict):
        # Isolate the event metadata and track the key parts of it.
        event_info = result['event_info']
        self.DECK_ID: str = event_info['id']
        self.SET: str = event_info['expansion']
        self.FORMAT: str = event_info['format']
        self._DRAFT: Optional[Draft.Draft] = None
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
        self.maindeck: list[Card] = [CardManager.from_name(card_dict['name']) for card_dict in pre_maindeck]
        self.sideboard: list[Card] = [CardManager.from_name(card_dict['name']) for card_dict in pre_sideboard]

    @property
    def DRAFT(self) -> Draft.Draft:
        """ The draft associated with the deck """
        if self._DRAFT is None:
            self._DRAFT = Draft.Draft.from_id(self.DECK_ID)
        return self._DRAFT

    @property
    def colors(self) -> str:
        """ Returns the colours of the deck, based on cards played and mana produced."""
        # TODO: Come up with clever way to get the colors of the maindeck.
        #  This should be based on Casting Cost, Color Identity, and the Manabase.

        """
        Some rules should be followed for this:
        Firstly, main casting costs trumps all. If a deck is all W, but has WB card it's casting the Deck is Wb.
        Secondly, mana produced should only count if there's a way to use it.
          eg. 'Crystal Grotto' shouldn't make a R deck wubRg, if there are no WUBG cards to play with it.
        Thirdly, optional costs should only count if there's the capacity to use them.
          eg. 'Benalish Sleeper' should be W if there's no way to produce black mana. 
          If black mana is available, it should be WB 
        Fourthly, hybrid mana costs should not count towards a colour that doesn't otherwise exist in the deck.
          eg. 'Pest Summonning' should be B if no green exists elsewhere in the deck.
        Fifthly, phyrexian mana costs should not count towards a colour that doesn't otherwise exist in the deck.
          eg. 'Phyrexian Metamorph' should be U only if blue exists elsewhere in the deck.
        """

        raise NotImplementedError()

        return ""

    @property
    def is_valid(self) -> bool:
        return len(self.maindeck) >= 40

    @property
    def details_link(self) -> str:
        """ A link to the details page of the deck on 17Lands"""
        return f"{self.URL_ROOT}/details/{self.DECK_ID}"

    @property
    def pool_link(self) -> str:
        """ A link to the card pool on 17Lands """
        return f"{self.URL_ROOT}/pool/{self.DECK_ID}"

    @property
    def draft_link(self) -> str:
        """ A link to the draft log on 17Lands """
        return f"{self.URL_ROOT}/draft/{self.DECK_ID}"

    # Properties that can have multiple links based on different deck builds.
    @property
    def builder_link(self) -> str:
        """ A link to the deck in sealeddeck.tech """
        return f"https://sealeddeck.tech/17lands/deck/{self.DECK_ID}/{self.selected_build}"

    @property
    def deck_link(self) -> str:
        """ A link to the 17Lands deck page """
        return f"{self.URL_ROOT}/deck/{self.DECK_ID}/{self.selected_build}"

    @property
    def text_link(self) -> str:
        """ A link to a text version of the deck """
        return f"{self.URL_ROOT}/deck/{self.DECK_ID}/{self.selected_build}.txt"


class ConstructedDeck(Deck):
    @classmethod
    def parse_decklist(cls, decklist: str) -> tuple[list[str], list[str]]:
        maindeck = list()
        sideboard = list()
        # TODO: Parse the decklist.
        raise NotImplementedError()
        return maindeck, sideboard

    def __init__(self, name: str, decklist: str):
        self.name = name
        self.maindeck, self.sideboard = self.parse_decklist(decklist)

    @property
    def colors(self) -> str:
        """ Returns the colours of the deck, based on cards played and mana produced."""
        # TODO: Come up with clever way to get the colors of the card_pool.
        #  This should be based on Casting Cost, Color Identity, and the Manabase.
        raise NotImplementedError()

        return ""

    @property
    def is_valid(self) -> bool:
        return len(self.maindeck) >= 60 and len(self.sideboard) <= 15


class DeckManager:
    """
    DeckManager acts as a global repository for decks. This is populated as more and more requests are made,
    and is mainly here to ease the burden on 17Lands.
    """
    # Used to maintain a constant-time lookup cache of previously requested cards.
    SETS: dict[str, dict[str, LimitedDeck]] = dict()
    DECKS: dict[str, Optional[LimitedDeck]] = dict()
    REQUESTER = Request17Lands()

    @classmethod
    def _add_deck(cls, deck: LimitedDeck, force_update=True) -> None:
        """
        An internal method to help more easily track decks as they're found/fetched.
        :param deck: The deck object to track
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
        Attempts to get a deck for the provided ID. Will check the cache first, and then
        attempt to fetch the deck from 17Lands otherwise.
        :param deck_id: The deck id to search for.
        :return: A LimitedDeck or None.
        """
        # If the deck already exists, return it.
        prev_deck, found = cls._find_deck(deck_id)
        if found:
            return prev_deck

        # Otherwise, try and get it from 17Lands.
        try:
            deck = LimitedDeck(cls.REQUESTER.get_deck(deck_id))
            cls._add_deck(deck)
            return deck
        except:
            # TODO: Better handle errors here.
            logging.info(f"Could not get deck with deck_id: '{deck_id}'")
            cls.DECKS[deck_id] = None
            return None

    @classmethod
    def _find_deck(cls, deck_id: str) -> tuple[Optional[LimitedDeck], bool]:
        """
        Attempts to find a deck in the cache, and if it's been searched before.
        """
        if deck_id in cls.DECKS:
            return cls.DECKS[deck_id], True
        else:
            return None, False

    @classmethod
    def clear_blank_decks(cls) -> None:
        """
        Clears cls.DECKS of pairs where the value is None.
        """
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
