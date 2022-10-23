from __future__ import annotations
from typing import NoReturn, Optional

from Utilities.auto_logging import logging
from wubrg import get_color_identity

from game_metadata.utils.consts import RARITY_ALIASES, CARD_INFO, SUPERTYPES, TYPES, SUBTYPE_DICT, ALL_SUBTYPES, \
    LAYOUT_DICT, CardLayouts, CARD_SIDE
from game_metadata.RequestScryfall import RequestScryfall


class CardFace:
    """
    This object helps simplify the logic for full card by separating specific information about a card (power,
    toughness, mana value, etc.) from general information about a card (rarity, number, set, etc.)
    """
    IMG_URL = 'https://c1.scryfall.com/file/scryfall-cards/'

    # sides = ['default', 'left', 'right', 'main', 'adventure']
    @classmethod
    def single_face(cls, json: CARD_INFO, side: CARD_SIDE = 'default') -> CardFace:
        """
        Returns the appropriately configured card face for the side given.
        :param json: The data for the card.
        :param side: The face of the card to generate the data for.
        :return: A CardFace object with nicely formatted data.
        """
        face = cls(json, side)

        # TODO: See if this can be moved into __init__
        # Modify 'default' as needed for easy access to data.
        if side == 'default':
            face.NAME = json.get('name')
            face.MANA_COST = json.get('mana_cost')
            face.TYPE_LINE = json.get('type_line')

        return face

    # sides = ['default', 'front', 'back']
    @classmethod
    def double_faced(cls, json: CARD_INFO, side: CARD_SIDE = 'default') -> CardFace:
        """
        Returns the appropriately configured card face for the side given.
        :param json: The data for the card.
        :param side: The face of the card to generate the data for.
        :return: A CardFace object with nicely formatted data.
        """
        face = cls(json, side)

        # TODO: See if this can be moved into __init__
        # Modify 'default' as needed for easy access to data.
        if side == 'default':
            face.NAME = json.get('name')
            face.TYPE_LINE = json.get('type_line')

        return face

    @staticmethod
    def _extract_face_dict(side, json) -> CARD_INFO:
        if side in ['back', 'adventure', 'right']:
            sub_json = json['card_faces'][1]
        else:
            if 'card_faces' in json:
                sub_json = json['card_faces'][0]
            else:
                sub_json = json

        return sub_json

    def _parse_cmc(self, face_dict) -> Optional[int]:
        # TODO: Handle this base on mana_cost later.
        _cmc = face_dict.get('cmc')
        ret = None
        if _cmc is not None:
            ret = int(_cmc)
        else:
            logging.warning(f"'cmc' is empty for card '{self.NAME}'")
        return ret

    def _parse_colors(self, face_dict, key) -> str:
        _colors = face_dict.get(key)
        ret = ""
        if _colors is not None:
            ret = get_color_identity("".join(_colors))
        else:
            logging.warning(f"'colors' is empty for card '{self.NAME}'")
        return ret

    def _get_type_line(self, face_dict) -> str:
        type_line = face_dict.get('type_line')
        if type_line is None:
            logging.warning(f"'type_line' is empty for card '{self.NAME}'")
            type_line = ''
        return type_line

    def _get_all_types(self) -> set[str]:
        # TODO: Test 'Archangel Avacyn'
        # Replace the (possible) dash, and separate on spaces to get a list of types.
        type_list = self.TYPE_LINE.replace(' —', '')
        # type_list = type_list.replace(' //', '')
        type_list = type_list.split(' ')
        return set(type_list)

    def _validate_types(self) -> None:
        length_all_types = len(self.ALL_TYPES)
        length_sum_types = len(self.SUBTYPES) + len(self.TYPES) + len(self.SUPERTYPES)

        if length_all_types != length_sum_types:
            logging.warning(f"Card '{self.NAME}' contains invalid types!\n  TYPE_LINE: '{self.TYPE_LINE}'")

        valid_subtypes = set()
        for t in self.TYPES:
            valid_subtypes = valid_subtypes | SUBTYPE_DICT[t]

        for subtype in self.SUBTYPES:
            # Check that it's a valid subtype among the cards types.
            if subtype not in valid_subtypes:
                logging.warning(f"Invalid subtype '{subtype}' for card '{self.NAME}'")

    def __init__(self, json: CARD_INFO, side: CARD_SIDE):
        self.ID: str = json['id']
        face_dict = self._extract_face_dict(side, json)

        self.NAME: str = face_dict.get('name')
        self.MANA_COST: str = face_dict.get('mana_cost')
        self.CMC: Optional[int] = self._parse_cmc(face_dict)
        self.COLORS: str = self._parse_colors(face_dict, 'colors')
        self.COLOR_IDENTITY: str = self._parse_colors(face_dict, 'color_identity')

        self.TYPE_LINE: str = self._get_type_line(face_dict)
        self.ALL_TYPES: set[str] = self._get_all_types()
        self.SUPERTYPES: set[str] = self.ALL_TYPES & SUPERTYPES
        self.TYPES: set[str] = self.ALL_TYPES & TYPES
        self.SUBTYPES: set[str] = self.ALL_TYPES & ALL_SUBTYPES
        self._validate_types()

        self.ORACLE: str = face_dict.get('oracle_text')
        self.KEYWORDS: str = face_dict.get('keywords', list())
        self.MANA_PRODUCED: str = face_dict.get('produced_mana', list())
        self.FLAVOR_TEXT: str = face_dict.get('flavor_text')

        self.POW: Optional[str] = face_dict.get('power')
        self.TOU: Optional[str] = face_dict.get('toughness')

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
    def from_name(cls, name) -> Card:
        return CardManager.from_name(name)

    @classmethod
    def from_set(cls, set_code) -> dict[str, Card]:
        return CardManager.from_set(set_code)

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
            self.FACE_1 = CardFace.single_face(json, 'main')
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

        # Handle simple layout information to reference later.
        self.LAYOUT: CardLayouts = LAYOUT_DICT[json['layout']]
        self.TWO_SIDED: bool = self.LAYOUT is CardLayouts.TWO_SIDED
        self.SPLIT: bool = self.LAYOUT is CardLayouts.FUSED

        # Initialize empty card faces, and fill them based on layout.
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
    def SUPERTYPES(self) -> set[str]:
        """Gets the supertypes of the card"""
        return self.DEFAULT_FACE.SUPERTYPES

    @property
    def TYPES(self) -> set[str]:
        """Gets the types of the card"""
        return self.DEFAULT_FACE.TYPES

    @property
    def SUBTYPES(self) -> set[str]:
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
