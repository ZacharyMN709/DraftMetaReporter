from __future__ import annotations
from typing import NoReturn, Optional

from Utilities.auto_logging import logging
from wubrg import get_color_identity, parse_cost, parse_color_list, COLOR_STRING

from game_metadata.utils.consts import RARITY_ALIASES, CARD_INFO, SUPERTYPES, TYPES, SUBTYPE_DICT, ALL_SUBTYPES, \
    LAYOUT_DICT, CardLayouts, CARD_SIDE
from game_metadata.RequestScryfall import RequestScryfall


class CardFace:
    """
    This object helps simplify the logic for full card by separating specific information about a card (power,
    toughness, mana value, etc.) from general information about a card (rarity, number, set, etc.)
    """
    IMG_URL = 'https://c1.scryfall.com/file/scryfall-cards/'

    def _extract_face_dict(self, json) -> CARD_INFO:
        """
        Get the relevant card face dictionary based on the side of the card.
        """
        if self.CARD_SIDE == 'default':
            return json
        if self.CARD_SIDE in ['back', 'adventure', 'right', 'flipped']:
            return json['card_faces'][1]
        if 'card_faces' in json:
            return json['card_faces'][0]

    def _parse_from_json(self, json, key, default=None):
        """
        Searches for the key in the json dictionary from most specific to least specific.
        This allows for "inner" faces to fall-back to general information about a card.
        """
        # Attempt to get the value from a specific face
        face_dict = self._extract_face_dict(json)
        val = face_dict.get(key)
        if val is not None:
            return val

        # Attempt to get the value from general card information
        val = json.get(key)
        if val is not None:
            return val

        # Fall-back to the default
        logging.debug(f"'{key}' is empty for card '{self.NAME}'")
        return default

    def _calculate_cmc(self, json) -> int:
        """
        Gets the CMC of the card, falling back ona manual calculation if needed.
        """
        # Attempt to get the CMC from the relevant section of the card.
        face_dict = self._extract_face_dict(json)
        cmc = face_dict.get('cmc')
        if cmc is not None:
            return int(cmc)

        # Get each mana symbol in the mana cost, add its cost to the total cmc.
        cmc_str = parse_cost(self.MANA_COST)
        cmc = 0
        for symbol in cmc_str:
            if symbol.isnumeric():
                cmc += int(symbol)
            else:
                if symbol == 'X':
                    continue
                cmc += 1
        return cmc

    def _validate_types(self) -> None:
        """
        Checks the sts of types found to make sure the information is valid.
        """
        # Check if there's mismatches between the separated types and all types found.
        length_all_types = len(self.ALL_TYPES)
        length_sum_types = len(self.SUBTYPES) + len(self.TYPES) + len(self.SUPERTYPES)
        if length_all_types != length_sum_types:
            logging.warning(f"Card '{self.NAME}' contains invalid types!\n  TYPE_LINE: '{self.TYPE_LINE}'")

        # Generate a set of valid subtypes.
        valid_subtypes = set()
        for t in self.TYPES:
            valid_subtypes = valid_subtypes | SUBTYPE_DICT[t]

        # Check that only valid subtypes exist among the card's subtypes.
        for subtype in self.SUBTYPES:
            if subtype not in valid_subtypes:
                logging.warning(f"Invalid subtype '{subtype}' for card '{self.NAME}'")

    def _apply_overrides(self, json):
        # TODO: These are something akin to hacks, and it would (likely) be better to handle this
        #  as part of the base logic which populates each field of the CardFace.

        if self.LAYOUT == CardLayouts.FLIP and self.CARD_SIDE == 'flipped':
            self.MANA_COST = json['mana_cost']
            self.CMC: int = self._calculate_cmc(json)

        if self.LAYOUT == CardLayouts.TRANSFORM and self.CARD_SIDE == 'default':
            front_face = json["card_faces"][0]
            self.COLORS = parse_color_list(json['color_identity'])
            self.MANA_COST = front_face["mana_cost"]
            self.ORACLE = front_face["oracle_text"]

        if self.LAYOUT == CardLayouts.TRANSFORM and self.CARD_SIDE == 'back':
            self.MANA_COST = ''
            self.CMC = json["cmc"]

        if self.LAYOUT == CardLayouts.MODAL_DFC and self.CARD_SIDE == 'default':
            front_face = json["card_faces"][0]
            self.MANA_COST = front_face["mana_cost"]
            self.COLORS = self.COLOR_IDENTITY
            self.ORACLE = front_face["oracle_text"]

        if self.LAYOUT == CardLayouts.MODAL_DFC and self.CARD_SIDE == 'back':
            self.MANA_PRODUCED = set(json.get("produced_mana", list()))

    def __init__(self, json: CARD_INFO, layout: CardLayouts, side: CARD_SIDE = 'default'):
        self.SCRYFALL_ID: str = json['id']
        self.ORACLE_ID: str = json['oracle_id']
        self.LAYOUT: CardLayouts = layout
        self.CARD_SIDE: str = side
        self.IMG_SIDE: str = 'back' if side == 'back' else 'front'
        self.NAME: str = self._parse_from_json(json, 'name')

        # NOTE: Colours and costs might be mor complicated than previously thought.
        self.MANA_COST: str = self._parse_from_json(json, 'mana_cost', '')
        self.CMC: int = self._calculate_cmc(json)
        self.COLORS: COLOR_STRING = parse_color_list(self._parse_from_json(json, 'colors', ''))
        self.COLOR_IDENTITY: COLOR_STRING = parse_color_list(self._parse_from_json(json, 'color_identity', ''))

        self.TYPE_LINE: str = self._parse_from_json(json, 'type_line', '')
        self.ALL_TYPES: set[str] = set(self.TYPE_LINE.split(' ')) - {'—', '//'}
        self.SUPERTYPES: set[str] = self.ALL_TYPES & SUPERTYPES
        self.TYPES: set[str] = self.ALL_TYPES & TYPES
        self.SUBTYPES: set[str] = self.ALL_TYPES & ALL_SUBTYPES
        self._validate_types()

        face_dict = self._extract_face_dict(json)
        self.ORACLE: str = face_dict.get('oracle_text')
        self.KEYWORDS: set = set(face_dict.get('keywords', list()))
        self.MANA_PRODUCED: set = set(face_dict.get('produced_mana', list()))
        self.FLAVOR_TEXT: str = face_dict.get('flavor_text')

        self.POW: Optional[str] = face_dict.get('power')
        self.TOU: Optional[str] = face_dict.get('toughness')

        self._apply_overrides(json)

    # sizes = ['small', 'normal', 'large', 'png', 'art_crop', 'border_crop']
    def image_url(self, size: str = 'normal') -> str:
        """Returns a link to the card, of the appropriate size."""
        return f"{self.IMG_URL}{size}/{self.IMG_SIDE}/" \
               f"{self.SCRYFALL_ID[0]}/{self.SCRYFALL_ID[1]}/{self.SCRYFALL_ID}.jpg"


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
        self.DEFAULT_FACE = CardFace(json, self.LAYOUT, 'default')

        if self.LAYOUT in {CardLayouts.NORMAL, CardLayouts.SAGA, CardLayouts.CLASS}:
            self.FACE_1 = self.DEFAULT_FACE
            self.FACE_2 = None
        if self.LAYOUT == CardLayouts.MELD:
            self.FACE_1 = self.DEFAULT_FACE
            meld_json = None  # TODO: Get meld json based on link found in json.
            self.FACE_2 = CardFace(meld_json, self.LAYOUT, 'melded')
        elif self.LAYOUT == CardLayouts.ADVENTURE:
            self.FACE_1 = CardFace(json, self.LAYOUT, 'main')
            self.FACE_2 = CardFace(json, self.LAYOUT, 'adventure')
        elif self.LAYOUT == CardLayouts.SPLIT:
            self.FACE_1 = CardFace(json, self.LAYOUT, 'left')
            self.FACE_2 = CardFace(json, self.LAYOUT, 'right')
        elif self.LAYOUT == CardLayouts.FLIP:
            self.FACE_1 = CardFace(json, self.LAYOUT, 'main')
            self.FACE_2 = CardFace(json, self.LAYOUT, 'flipped')
        elif self.LAYOUT in {CardLayouts.TRANSFORM, CardLayouts.MODAL_DFC}:
            self.FACE_1 = CardFace(json, self.LAYOUT, 'front')
            self.FACE_2 = CardFace(json, self.LAYOUT, 'back')
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
                new_card = Card(json)

                # While keeping references to previously fetched cards.
                card, _ = cls._find_card(new_card.NAME)
                if card is not None:
                    new_card = card

                cls._add_card(new_card)
                cls.SETS[set_code][new_card.NAME] = new_card

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
