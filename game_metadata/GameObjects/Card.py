from __future__ import annotations
from typing import NoReturn, Optional

from wubrg import get_color_identity
from Utilities.auto_logging import logging

from game_metadata.utils.consts import RARITY_ALIASES, LAYOUT_DICT, CardLayouts, CARD_INFO
from game_metadata.utils import SUPERTYPES, TYPES, SUBTYPE_DICT
from game_metadata.RequestScryfall import RequestScryfall


class CardFace:
    """
    This object helps simplify the logic for full card by separating specific information about a card (power,
    toughness, mana value, etc.) from general information about a card (rarity, number, set, etc.)
    """
    IMG_URL = 'https://c1.scryfall.com/file/scryfall-cards/'

    # sides = ['default', 'left', 'right', 'creature', 'adventure']
    @classmethod
    def single_face(cls, json: CARD_INFO, side: str = 'default') -> CardFace:
        """
        Returns the appropriately configured card face for the side given.
        :param json: The data for the card.
        :param side: The face of the card to generate the data for.
        :return: A CardFace object with nicely formatted data.
        """
        face = cls(json, side)

        # Modify 'default' as needed for easy access to data.
        if side == 'default':
            face.NAME = json.get('name')
            face.MANA_COST = json.get('mana_cost')
            face.TYPE_LINE = json.get('type_line')

        return face

    # sides = ['default', 'front', 'back']
    @classmethod
    def double_faced(cls, json: CARD_INFO, side: str = 'default') -> CardFace:
        """
        Returns the appropriately configured card face for the side given.
        :param json: The data for the card.
        :param side: The face of the card to generate the data for.
        :return: A CardFace object with nicely formatted data.
        """
        face = cls(json, side)

        # Modify 'default' as needed for easy access to data.
        if side == 'default':
            face.NAME = json.get('name')
            face.TYPE_LINE = json.get('type_line')

        return face

    def handle_types(self, type_line: str) -> Optional[NoReturn]:
        """
        Takes in the typeline as a string, and parses it into its supertypes, types and subtypes.
        The values are assigned to the properties of the object rather than returned.
        :param type_line:
        """
        # Check that a type line was found.
        if type_line is None:
            raise ValueError(f"'type_line' is empty for card '{self.NAME}'")
        self.TYPE_LINE = type_line

        # Split the type line on the dash to separate any subtypes
        lst = type_line.split('—')

        # Handle the first half of the type line
        half_one = lst[0].strip()

        # Remove the super types from the first half, and save them
        for t in SUPERTYPES:
            if t in half_one:
                half_one = half_one.replace(t, '')
                self.SUPERTYPES.append(t)

        # The remaining text is all of the types, separated by spaces.
        self.TYPES = half_one.strip().split(' ')
        valid_subtypes = set()
        for t in self.TYPES:
            if t not in TYPES:
                raise ValueError(f"Invalid type '{t}' for card '{self.NAME}'")

            valid_subtypes = valid_subtypes | SUBTYPE_DICT[t]

        # If the second half of the type line exists, handle it.
        if len(lst) == 2:
            subtypes = lst[1].strip().split(' ')

            # For each subtype found,
            for subtype in subtypes:
                # Check that it's a valid subtype among the cards types.
                if subtype in valid_subtypes:
                    self.SUBTYPES.append(subtype)
                # And raise an exception if not.
                else:
                    raise ValueError(f"Invalid subtype '{subtype}' for card '{self.NAME}'")

    def __init__(self, json: CARD_INFO, side: str):
        if side in ['back', 'adventure', 'right']:
            sub_json = json['card_faces'][1]
        else:
            if 'card_faces' in json:
                sub_json = json['card_faces'][0]
            else:
                sub_json = json

        self.ID: str = json['id']
        self.NAME: str = sub_json.get('name')
        self.MANA_COST: str = sub_json.get('mana_cost')
        _cmc = sub_json.get('cmc')
        self.CMC: Optional[int] = None  # TODO: Handle this base on mana_cost later.
        if _cmc is not None:
            self.CMC = int(_cmc)

        _colors = sub_json.get('colors')
        self.COLORS: str = ""
        if _colors is not None:
            self.COLORS = get_color_identity("".join(_colors))

        self.TYPE_LINE: str = ""
        self.SUPERTYPES: list[str] = list()
        self.TYPES: list[str] = list()
        self.SUBTYPES: list[str] = list()
        self.handle_types(sub_json.get('type_line'))

        self.ORACLE: str = sub_json.get('oracle_text')
        self.FLAVOR_TEXT: str = sub_json.get('flavor_text')

        self.POW: str = sub_json.get('power')
        self.TOU: str = sub_json.get('toughness')

        self.CARD_SIDE: str = side
        self.IMG_SIDE: str = 'back' if side == 'back' else 'front'

    # sizes = ['small', 'normal', 'large', 'png', 'art_crop', 'border_crop']
    def image_url(self, size: str = 'normal') -> str:
        """Returns a link to the card, of the appropriate size."""
        return f"{self.IMG_URL}{size}/{self.IMG_SIDE}/{self.ID[0]}/{self.ID[1]}/{self.ID}.jpg"


class Card:
    """
    Provides a succinct collection of information about a card, with the ability to have a simple layer of information
    easily accessible, with a more complicated, but accurate, set of information underneath.
    """
    SCRY_URL = 'https://scryfall.com/card/'
    API_URL = 'https://api.scryfall.com/cards/'

    @classmethod
    def from_name(cls, name):
        return CardManager.from_name(name)

    def _handle_card_faces(self, json: CARD_INFO) -> Optional[NoReturn]:
        """
        Automatically generates and sets the CardFaces for the Card object.
        :param json: The card data.
        """
        if self.LAYOUT == CardLayouts.NORMAL:
            self.DEFAULT_FACE = CardFace.single_face(json)
            self.FACE_1 = self.DEFAULT_FACE
            self.FACE_2 = None
        elif self.LAYOUT == CardLayouts.SAGA:
            self.DEFAULT_FACE = CardFace.single_face(json)
            self.FACE_1 = self.DEFAULT_FACE
            self.FACE_2 = None
        elif self.LAYOUT == CardLayouts.CLASS:
            self.DEFAULT_FACE = CardFace.single_face(json)
            self.FACE_1 = self.DEFAULT_FACE
            self.FACE_2 = None
        elif self.LAYOUT == CardLayouts.ADVENTURE:
            self.DEFAULT_FACE = CardFace.single_face(json)
            self.FACE_1 = CardFace.single_face(json, 'creature')
            self.FACE_2 = CardFace.single_face(json, 'adventure')
        elif self.LAYOUT == CardLayouts.SPLIT:
            self.DEFAULT_FACE = CardFace.single_face(json)
            self.FACE_1 = CardFace.single_face(json, 'left')
            self.FACE_2 = CardFace.single_face(json, 'right')
        elif self.LAYOUT == CardLayouts.TRANSFORM:
            self.DEFAULT_FACE = CardFace.double_faced(json)
            self.FACE_1 = CardFace.double_faced(json, 'front')
            self.FACE_2 = CardFace.double_faced(json, 'back')
        elif self.LAYOUT == CardLayouts.MODAL_DFC:
            self.DEFAULT_FACE = CardFace.double_faced(json)
            self.FACE_1 = CardFace.double_faced(json, 'front')
            self.FACE_2 = CardFace.double_faced(json, 'back')
        else:
            raise Exception(f"Unknown layout '{self.LAYOUT}'")

    def __init__(self, json: CARD_INFO):
        if json['object'] != 'card':
            raise Exception("Invalid JSON provided! Object type is not 'card'")

        self.LAYOUT: CardLayouts = LAYOUT_DICT[json['layout']]
        self.TWO_SIDED: bool = self.LAYOUT is CardLayouts.TWO_SIDED
        self.SPLIT: bool = self.LAYOUT is CardLayouts.FUSED

        self.DEFAULT_FACE: CardFace
        self.FACE_1: CardFace
        self.FACE_2: Optional[CardFace]
        self._handle_card_faces(json)

        # Card ID info
        self.ID: str = json['id']
        self.ARENA_ID: int = json.get('arena_id')  # TODO: Handle Remastered Arena sets.
        self.SET: str = json['set'].upper()
        self.RARITY: str = RARITY_ALIASES[json['rarity']]
        self.NUMBER = json['collector_number']
        self.COLOR_IDENTITY: str = get_color_identity("".join(json['color_identity']))
        self.CAST_IDENTITY: str = get_color_identity(self.MANA_COST)
        self.CMC: int = int(json['cmc'])

    @property
    def NAME(self) -> str:
        """Gets the simple name of the card"""
        if self.LAYOUT == CardLayouts.SPLIT:
            return self.DEFAULT_FACE.NAME
        else:
            return self.FACE_1.NAME

    @property
    def FULL_NAME(self) -> str:
        """Gets the full name of the card"""
        return self.DEFAULT_FACE.NAME

    @property
    def MANA_COST(self) -> str:
        """Gets the mana cost of the card"""
        return self.DEFAULT_FACE.MANA_COST

    @property
    def TYPE_LINE(self) -> str:
        """Gets the type line of the card"""
        return self.DEFAULT_FACE.TYPE_LINE

    @property
    def SUPERTYPES(self) -> list[str]:
        """Gets the supertypes of the card"""
        return self.DEFAULT_FACE.SUPERTYPES

    @property
    def TYPES(self) -> list[str]:
        """Gets the types of the card"""
        return self.DEFAULT_FACE.TYPES

    @property
    def SUBTYPES(self) -> list[str]:
        """Gets the subtypes of the card"""
        return self.DEFAULT_FACE.SUBTYPES

    @property
    def POW(self) -> str:
        """Gets the power of the card"""
        return self.DEFAULT_FACE.POW

    @property
    def TOU(self) -> str:
        """Gets the toughness of the card"""
        return self.DEFAULT_FACE.TOU

    @property
    def API(self) -> str:
        """Link for the API call of the card"""
        return f"{self.API_URL}{self.ID}"

    @property
    def URL(self) -> str:
        """Shortened link to the Scryfall page for the card"""
        return f"{self.SCRY_URL}{self.SET.lower()}/{self.NUMBER}"

    @property
    def IMAGE_URL(self) -> str:
        """Returns a link to the image of the card."""
        return self.DEFAULT_FACE.image_url('normal')

    def __str__(self):
        return self.FULL_NAME

    def __repr__(self):
        return self.FULL_NAME


class CardManager:
    """
    CardManager acts as a global repository for card data. This is both for pulled data from Scryfall, and the results
    and queries of users. In particular, it tracks user's requests (which can be mis-spelled), and logs them as aliases
    for a found card. This means that as more users request cards, fewer calls have to be made to Scryfall.

    It's possible this should be reset at the release of a new set to let the object "re-link" names as their mappings
    may end up changing with the release of new cards, or after a certain amount of time to free up memory.
    """

    # Used to map misspellings back to the correct name, without having to re-query scryfall.
    REDIRECT: dict[str, str] = dict()

    # Used to maintain a constant-time lookup cache of previously requested cards.
    SETS: dict[str, dict[str, Card]] = dict()
    CARDS: dict[str, Card] = dict()

    @classmethod
    def _add_card(cls, card: Card, searched_name: str = '', force_update=True) -> None:
        """
        An internal method to help more easily track cards as they're found/fetched.
        :param card: The card object to track
        :param searched_name: The name provided by the user to find
        """

        # If the card objects isn't tracked in CARDS, add it.
        # This also means if cards from sets are pulled newest to oldest, the most recent version
        # of the card will be the one that is cached.
        if card.NAME not in cls.CARDS or force_update:
            cls.CARDS[card.NAME] = card
            cls.REDIRECT[card.NAME] = card.NAME
            cls.REDIRECT[card.FULL_NAME] = card.NAME

        # Used to re-direct mis-spellings.
        if searched_name != '':
            cls.REDIRECT[searched_name] = card.NAME

    @classmethod
    def from_name(cls, name: str) -> Optional[Card]:
        """
        Searches for a card by name. If not already known, will attempt to query Scryfall for
        the card.
        :param name: The name of the card to look for. Can handle inexact names, to an extent.
        :return: A Card or None
        """
        # If the card already exists, return it.
        prev_card, found = cls._find_card(name)
        if found:
            return prev_card

        # Otherwise, get the card info from scryfall.
        json = RequestScryfall.get_card_by_name(name)
        # If there's an error, log it, mark the alias as '' and return None.
        if 'err_msg' in json:
            logging.info(f'Could not get card for {name}')
            logging.info(f'Error: {json["err_msg"]}')
            cls.REDIRECT[name] = ''
            return None
        # If the card is found, return it.
        else:
            card = Card(json)

            # See if a copy of the card already exists, likely
            # due to a misspelling. If so, use that instead.
            prev_card, found = cls._find_card(card.NAME)
            if prev_card is not None:
                card = prev_card

            cls._add_card(card, name)
            return card

    @classmethod
    def from_set(cls, set_code: str) -> dict[str, Card]:
        """
        Gets a dictionary of card which exist a set.
        :param set_code: The three-letter code of the set.
        :return: A dictionary of cards, with common names as keys.
        """

        # If the set code doesn't already exist,
        if set_code not in cls.SETS:
            # Create a new dictionary for it,
            cls.SETS[set_code] = dict()
            for json in RequestScryfall.get_set_cards(set_code):
                # And fill it with cards fetched from Scryfall.
                card = Card(json)
                cls._add_card(card)
                cls.SETS[set_code][card.NAME] = card

            for card_name in ['Plains', 'Island', 'Swamp', 'Mountain', 'Forest']:
                if card_name in cls.SETS[set_code]:
                    del cls.SETS[set_code][card_name]

        return cls.SETS[set_code]

    @classmethod
    def _find_card(cls, card_name: str) -> tuple[Optional[Card], bool]:
        """
        Attempts to find a saved instance of a card.
        :param card_name: The card name to find
        :return: A Card or None, and whether the name has been previously searched
        """

        previously_searched = card_name in cls.REDIRECT
        card = None

        # If the card has been searched before,
        if previously_searched:
            # Get the name's alias,
            card_name = cls.REDIRECT[card_name]
            # And if it exists, use it to get the card.
            if card_name != '':
                card = cls.CARDS[card_name]

        return card, previously_searched

    @classmethod
    def reset_redirects(cls) -> None:
        """
        Resets the REDIRECT dictionary, clearing any aliases, but preserving the true card names.
        """
        cls.REDIRECT = dict()
        for card_name in cls.CARDS:
            card = cls.CARDS[card_name]
            cls._add_card(card, force_update=True)

    @classmethod
    def flush_cache(cls) -> None:
        """
        Clears the caches of cards.
        """
        del cls.REDIRECT
        del cls.SETS
        del cls.CARDS

        cls.REDIRECT = dict()
        cls.SETS = dict()
        cls.CARDS = dict()
