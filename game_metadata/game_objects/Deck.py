from __future__ import annotations
from typing import Optional
from datetime import datetime
import re
from os import path

from utilities.utils.funcs import flatten_lists
from wubrg import COLOR

from utilities.auto_logging import logging
from game_metadata.utils.consts import RANKS
from game_metadata.utils.funcs import new_color_count_dict
from data_interface.Request17Lands import Request17Lands
from game_metadata.game_objects.Card import CardManager, Card
import game_metadata.game_objects.Draft as Draft


# Alternate regex for ranks: r"(\w*)-([\d])"
trim_numeric = re.compile(r"-[\d]*")
card_line = re.compile(r"^([0-9]{0,3}) ?([^(\n]*)(?: |$)(\(\w{3}\))? ?(\d{1,3})?")


class TrophyStub:
    # TODO: See if this can be folded into LimitedDeck with any ease.

    @classmethod
    def parse_simple_rank(cls, rank_1: Optional[str], rank_2: Optional[str]) -> str:
        """
        Merges the start and end rank of a draft, taking the highest "metal" rank.
        Eg. "Silver-1" and "Gold-2" would return "Gold".
        """
        # Take the rank and convert it to a string, turning None into 'None', and replace the numerics.
        r1 = trim_numeric.sub('', str(rank_1))
        r2 = trim_numeric.sub('', str(rank_2))

        # Get the indexes for the ranks
        idx1 = RANKS.index(r1)
        idx2 = RANKS.index(r2)

        # Use the indexes to return the higher rank.
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
        self.time: datetime = datetime.strptime(results['time'], "%Y-%m-%d %H:%M")

    @property
    def deck(self) -> LimitedDeck:
        """ The deck associated with the draft. """
        if self._DECK is None:
            self._DECK = LimitedDeck.from_id(self.DECK_ID)
            self._DECK.trophy_stub = self
        return self._DECK


class Deck:
    _DECKS = 0
    _maindeck: list[Card] = list()
    _sideboard: list[Card] = list()
    name: str
    wins: int
    losses: int
    _maindeck_dict: dict[Card, int] = dict()
    _sideboard_dict: dict[Card, int] = dict()

    _produced_mana: Optional[dict[COLOR, int]]
    _casting_pips: Optional[dict[COLOR, int]]
    _all_pips: Optional[dict[COLOR, int]]
    colors: str

    # region Decklist Parsing
    @classmethod
    def parse_decklist(cls, decklist: list[str]) -> tuple[list[Card], list[Card]]:
        def parse_line(line: str) -> list[str]:
            # If the line is empty or the deck header, return
            if line in ["Deck", "Sideboard", "Commander"]:
                return list()

            # Split the card line into bits, based on a typical Arena decklist export.
            _match = card_line.match(line)
            _cnt, _card, _set, _num = _match.groups()

            # If a card name couldn't be matched, return.
            if not _card:
                return list()

            # Get the number of cards in the deck, defaulting to 1 if there's no value.
            _cnt = int(_cnt) if _cnt else 1

            # Return the card name the number of times it appears in the deck.
            return [_card] * int(_cnt)

        # Find the line to split for sideboard cards,
        try:
            # If the list contains 'Sideboard', split the list on that index.
            idx = decklist.index('Sideboard')
            pre_maindeck = [parse_line(c) for c in decklist[:idx]]
            pre_sideboard = [parse_line(c) for c in decklist[idx:]]
        except ValueError:
            # Otherwise, an error is thrown, and assume no sideboard.
            pre_maindeck = [parse_line(c) for c in decklist]
            pre_sideboard = list()

        # Flatten the lists and return them as Cards.
        maindeck = [CardManager.from_name(name) for name in flatten_lists(pre_maindeck)]
        sideboard = [CardManager.from_name(name) for name in flatten_lists(pre_sideboard)]
        return maindeck, sideboard

    @classmethod
    def parse_decklist_from_string(cls, text: str) -> tuple[list[Card], list[Card]]:
        # Split the string into a list on newlines.
        return cls.parse_decklist(text.split('\n'))

    @classmethod
    def parse_decklist_from_file(cls, file_path: str) -> tuple[list[Card], list[Card]]:
        # Check that the file exists.
        load = path.exists(file_path) and path.isfile(file_path)
        if not load:
            raise ValueError(f"Provided value ({file_path}) is not a file path!")

        # If it does, load it as a string, And parse the decklist.
        with open(file_path, 'r') as f:
            return cls.parse_decklist_from_string(f.read())

    # noinspection PyUnreachableCode
    @classmethod
    def parse_decklist_from_url(cls, url: str) -> tuple[list[Card], list[Card]]:
        requester = Request17Lands()
        _id, _deck = re.match("https://www.17lands.com/deck/(.*)/(.*)", url).groups()
        # _id, _deck = re.match("https://www.17lands.com/data/deck?draft_id=(.*)&deck_index=(.*)", url).groups()
        data = requester.get_deck(_id, _deck)['groups']
        deck = ["Deck"] + [d['name'] for d in data[0]['cards']]
        sideboard = ["Sideboard"] + [d['name'] for d in data[1]['cards']]
        decklist = deck + [''] + sideboard
        return cls.parse_decklist(decklist)
    # endregion Decklist Parsing

    def __init__(self, maindeck: list[Card], sideboard: list[Card], name: Optional[str],
                 wins: int = 0, losses: int = 0):
        self._maindeck = maindeck
        self._sideboard = sideboard
        self.wins = wins
        self.losses = losses

        # Track the number of decks instantiated, and use it as a default name if needed.
        Deck._DECKS += 1
        if not name:
            self.name = f"Deck {Deck._DECKS}"
        else:
            self.name = name

        self._maindeck_dict = self._gen_card_dict(self.maindeck)
        self._sideboard_dict = self._gen_card_dict(self.sideboard)

    @classmethod
    def from_decklist(cls, card_list: list[str], name: Optional[str], wins: int = 0, losses: int = 0) -> Deck:
        maindeck, sideboard = Deck.parse_decklist(card_list)
        return Deck(maindeck, sideboard, name, wins, losses)

    @classmethod
    def from_string(cls, text: str, name: Optional[str], wins: int = 0, losses: int = 0) -> Deck:
        maindeck, sideboard = Deck.parse_decklist_from_string(text)
        return Deck(maindeck, sideboard, name, wins, losses)

    @classmethod
    def from_file(cls, file_path: str, name: Optional[str], wins: int = 0, losses: int = 0) -> Deck:
        maindeck, sideboard = Deck.parse_decklist_from_file(file_path)
        return Deck(maindeck, sideboard, name, wins, losses)

    @classmethod
    def from_url(cls, url: str, name: Optional[str], wins: int = 0, losses: int = 0) -> Deck:
        maindeck, sideboard = Deck.parse_decklist_from_url(url)
        return Deck(maindeck, sideboard, name, wins, losses)

    # region Pip Calculations
    @classmethod
    def _gen_card_dict(cls, card_list: list[Card]) -> dict[Card, int]:  # pragma: nocover
        card_dict = dict()
        for card in card_list:
            if card not in card_dict:
                card_dict[card] = 0
            card_dict[card] += 1
        return card_dict

    def _get_produced_mana(self) -> dict[COLOR, int]:  # pragma: nocover
        d = new_color_count_dict()
        for card in self.cardpool:
            for mana in card.DEFAULT_FACE.MANA_PRODUCED:
                d[mana] += 1
        return d

    @property
    def produced_mana(self) -> Optional[dict[COLOR, int]]:  # pragma: nocover
        if self._produced_mana is None:
            self._produced_mana = self._get_produced_mana()
        return self._produced_mana

    def _get_casting_pips(self) -> dict[COLOR, int]:  # pragma: nocover
        d = new_color_count_dict()
        for card in self.cardpool:
            for mana in card.DEFAULT_FACE.MANA_COST:
                d[mana] += 1
        return d

    @property
    def casting_pips(self) -> Optional[dict[COLOR, int]]:  # pragma: nocover
        if self._casting_pips is None:
            self._casting_pips = self._get_casting_pips()
        return self._casting_pips

    def _get_all_pips(self) -> dict[COLOR, int]:  # pragma: nocover
        d = new_color_count_dict()
        for card in self.cardpool:
            for mana in card.DEFAULT_FACE.MANA_PRODUCED:
                d[mana] += 1
        return d

    @property
    def all_pips(self) -> Optional[dict[COLOR, int]]:  # pragma: nocover
        if self._all_pips is None:
            self._all_pips = self._get_all_pips()
        return self._all_pips
    # endregion Pip Calculations

    # region Basic Deck Properties
    @property
    def maindeck(self) -> list[Card]:
        """ The list of cards the deck plays in the maindeck """
        return self._maindeck

    @property
    def sideboard(self) -> list[Card]:
        """ The list of cards the deck plays in the sideboard """
        return self._sideboard

    @property
    def cardpool(self) -> list[Card]:
        """ The complete list of cards the deck has access to """
        return self._maindeck + self._sideboard

    @property
    def unique_cards(self) -> set[Card]:
        return set(self.maindeck) | set(self.sideboard)

    @property
    def win_rate(self) -> float:
        """ Returns the winrate as a percent. No games played results in a 0% win rate. """
        denominator = self.wins + self.losses
        if denominator == 0:
            return 0
        else:
            return (self.wins / denominator) * 100
    # endregion Basic Deck Properties

    def deck_differences(self, deck: Deck) -> tuple[dict[Card, int], dict[Card, int]]:
        """
        Compares the contents of this deck with a provided deck. Differences of 0 are omitted.
        :param deck: The deck to compare with.
        :return: A maindeck and sideboard dictionary of card differences.
        """
        def subtract_dicts(d1: dict[Card, int], d2: dict[Card, int]) -> dict[Card, int]:
            """
            Generates a dictionary which contains the card differences between the two card dictionaries.
            Differences of 0 are omitted from the output dictionary for clarity.
            """
            # Create an empty dictionary and get all the keys.
            d = dict()
            all_keys = d1.keys() | d2.keys()

            # For each key get its value, defaulting to 0 if not in the dictionary.
            for k in all_keys:
                # Subtract the values, to get the difference i cards counts between the two decks.
                # If the difference is 0, skip the entry, since the decks have the same number of the given card.
                v = d1.get(k, 0) - d2.get(k, 0)
                if v != 0:
                    d[k] = v

            return d

        maindeck_diff = subtract_dicts(self._maindeck_dict, deck._maindeck_dict)
        sideboard_diff = subtract_dicts(self._sideboard_dict, deck._sideboard_dict)
        return maindeck_diff, sideboard_diff

    def deck_overlap(self, deck: Deck) -> tuple[dict[str, int], dict[str, int]]:
        """
        Compares the contents of this deck with a provided deck. Gets the shared cards between the two.
        :param deck: The deck to compare with.
        :return: A maindeck and sideboard dictionary of cards shared.
        """
        def overlap_dicts(d1: dict[str, int], d2: dict[str, int]) -> dict[str, int]:
            """
            Generates a dictionary which contains the card overlaps between the two card dictionaries.
            """
            # Create an empty dictionary and split the keys.
            d = dict()
            all_keys = d1.keys() | d2.keys()

            # For each key get its value, defaulting to 0 if not in the dictionary.
            for k in all_keys:
                # Get thw lowest of the two values, which is how many copies of a card the decks share.
                # If the value is 0, skip the entry, since one deck has none of the given card.
                v = min(d1.get(k, 0), d2.get(k, 0))
                if v != 0:
                    d[k] = v

            return d

        maindeck_over = overlap_dicts(self._maindeck_dict, deck._maindeck_dict)
        sideboard_over = overlap_dicts(self._sideboard_dict, deck._sideboard_dict)
        return maindeck_over, sideboard_over

    def __sub__(self, other: Deck) -> tuple[dict[str, int], dict[str, int]]:
        return self.deck_differences(other)

    def __or__(self, other: Deck) -> tuple[dict[str, int], dict[str, int]]:
        return self.deck_overlap(other)

    def __repr__(self):
        # TODO: Improve this with colour information and similar.
        return self.name


class LimitedDeck(Deck):
    URL_ROOT = "https://www.17lands.com"

    @classmethod
    def from_id(cls, deck_id: str) -> LimitedDeck:
        return DeckManager.from_deck_id(deck_id)

    def __init__(self, result: dict):
        # Get the event info from the result.
        event_info = result['event_info']

        # Get the data needed to initialize the super-class.
        _deck_id: str = event_info['id']
        _set: str = event_info['expansion']
        _format: str = event_info['format']
        name = f"{_set} - {_format} ({_deck_id})"
        wins: int = event_info['wins']
        losses: int = event_info['losses']
        maindeck = [CardManager.from_name(card_dict['name']) for card_dict in result['groups'][0]["cards"]]
        sideboard = [CardManager.from_name(card_dict['name']) for card_dict in result['groups'][1]["cards"]]
        super().__init__(maindeck, sideboard, name, wins, losses)

        # Add the key parts of event metadata.
        self.DECK_ID: str = _deck_id
        self.SET: str = _set
        self.FORMAT: str = _format
        self.deck_builds: int = len(event_info['deck_links'])
        self.selected_build: int = self.deck_builds - 1
        self._draft: Optional[Draft.Draft] = None
        self.trophy_stub: Optional[TrophyStub] = None

    @property
    def draft(self) -> Draft.Draft:
        """ The draft associated with the deck """
        if self._draft is None:
            self._draft = Draft.Draft.from_id(self.DECK_ID)
        return self._draft

    # noinspection PyUnreachableCode
    def _calc_colors(self):
        """ Returns the colours of the deck, based on cards played and mana produced."""
        # TODO: Come up with clever way to get the colors of the maindeck.
        #  This should be based on Casting Cost, Color Identity, and the Manabase.
        #  Development of this may need to go back to Card/CardFace to extend the
        #  information those cards contain to support determining deck colours.

        """
        Some rules should be followed for this:
        Firstly, main casting costs trumps all. If a deck is all W, but has WB card it's casting the Deck is Wb.
        Secondly, mana produced should only count if there's a way to use it.
          eg. 'Crystal Grotto' shouldn't make a R deck wubRg, if there are no WUBG cards to play with it.
        Thirdly, optional costs should only count if there's the capacity to use them.
          eg. 'Benalish Sleeper' should be W if there's no way to produce black mana. 
          If black mana is available, it should be WB 
        Fourthly, hybrid mana costs should not count towards a colour that doesn't otherwise exist in the deck.
          eg. 'Pest Summoning' should be B if no green exists elsewhere in the deck.
        Fifthly, phyrexian mana costs should not count towards a colour that doesn't otherwise exist in the deck.
          eg. 'Phyrexian Metamorph' should be U only if blue exists elsewhere in the deck.
        """

        raise NotImplementedError()

        return ""  # pragma: nocover

    @property
    def is_valid(self) -> bool:
        """ If the deck is valid for organized play. """
        return len(self.maindeck) >= 40

    @property
    def has_trophy_stub(self) -> bool:
        """ If the deck has an associate Trophy Stub. """
        return self.trophy_stub is not None

    # region Link Properties
    # Properties that have a single link regardless of different deck builds.
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
    # endregion Link Properties


class ConstructedDeck(Deck):
    # TODO: Flesh this out with more utility.

    def __init__(self, maindeck: list[Card], sideboard: list[Card], name: str, wins: int = 0, losses: int = 0):
        super().__init__(maindeck, sideboard, name, wins, losses)

    # noinspection PyUnreachableCode
    def _calc_colors(self):
        """ Returns the colours of the deck, based on cards played and mana produced."""
        # TODO: Come up with clever way to get the colors of the card_pool.
        #  This should be based on Casting Cost, Color Identity, and the Manabase.
        raise NotImplementedError()

        return ""  # pragma: nocover

    @property
    def is_valid(self) -> bool:
        """ If the deck is valid for organized play. """
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
        """ Attempts to find a deck in the cache, and if it's been searched before. """
        if deck_id in cls.DECKS:
            return cls.DECKS[deck_id], True
        else:
            return None, False

    @classmethod
    def clear_blank_decks(cls) -> None:
        """ Clears cls.DECKS of pairs where the value is None. """
        to_del = list()
        for deck_id in cls.DECKS:
            if cls.DECKS[deck_id] is None:
                to_del.append(deck_id)

        for deck_id in to_del:
            del cls.DECKS[deck_id]

    @classmethod
    def flush_cache(cls) -> None:
        """ Clears the caches of decks. """
        del cls.SETS
        del cls.DECKS

        cls.SETS = dict()
        cls.DECKS = dict()
