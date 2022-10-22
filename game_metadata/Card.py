from __future__ import annotations
from typing import NoReturn, Optional

from wubrg import get_color_identity

from game_metadata.utils.consts import RARITY_ALIASES, LAYOUT_DICT, CardLayouts, CARD_INFO
from game_metadata.utils import SUPERTYPES, TYPES, SUBTYPE_DICT


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
