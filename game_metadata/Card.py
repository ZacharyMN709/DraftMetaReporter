from typing import Union
from enum import Flag, auto

from utils.consts import RARITY_ALIASES
from utils.WUBRG import get_color_identity


# https://scryfall.com/docs/api/layouts
class CardLayouts(Flag):
    NORMAL = auto()
    SPLIT = auto()
    FLIP = auto()
    TRANSFORM = auto()
    MODAL_DFC = auto()
    MELD = auto()
    LEVELER = auto()
    CLASS = auto()
    SAGA = auto()
    ADVENTURE = auto()

    TWO_SIDED = TRANSFORM | MODAL_DFC
    FUSED = ADVENTURE | SPLIT | FLIP


LAYOUT_DICT = {
    "normal": CardLayouts.NORMAL,
    "split": CardLayouts.SPLIT,
    "flip": CardLayouts.FLIP,
    "transform": CardLayouts.TRANSFORM,
    "modal_dfc": CardLayouts.MODAL_DFC,
    "meld": CardLayouts.MELD,
    "leveler": CardLayouts.LEVELER,
    "class": CardLayouts.CLASS,
    "saga": CardLayouts.SAGA,
    "adventure": CardLayouts.ADVENTURE
}


class CardFace:
    SCRY_URL = 'https://scryfall.com/card/'
    API_URL = 'https://api.scryfall.com/cards/'
    IMG_URL = 'https://c1.scryfall.com/file/scryfall-cards/'

    # sides = ['default', 'left', 'right', 'creature', 'adventure']
    @classmethod
    def single_face(cls, json: dict[str, Union[str, dict[str, str], list[str]]], side: str = 'default') -> 'CardFace':
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
    def double_faced(cls, json: dict[str, Union[str, dict[str, str]], list[str]], side: str = 'default') -> 'CardFace':
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

    def __init__(self, json: dict[str, Union[str, dict[str, str], list[str]]], side: str):
        if side in ['back', 'adventure', 'right']:
            sub_json = json['card_faces'][1]
        else:
            if 'card_faces' in json:
                sub_json = json['card_faces'][0]
            else:
                sub_json = json

        self.ID = json['id']
        self.NAME = sub_json.get('name')
        self.MANA_COST = sub_json.get('mana_cost')
        # self.CMC = sub_json.get('cmc')  #TODO: Handle this more precisely later.
        self.COLORS = sub_json.get('colors')
        if self.COLORS is not None:
            self.COLORS = get_color_identity("".join(self.COLORS))
        self.TYPE_LINE = sub_json.get('type_line')

        self.ORACLE = sub_json.get('oracle_text')
        self.FLAVOR_TEXT = sub_json.get('flavor_text')

        self.POW = sub_json.get('power')
        self.TOU = sub_json.get('toughness')

        self.CARD_SIDE = side
        self.IMG_SIDE = 'back' if side == 'back' else 'front'

    # sizes = ['small', 'normal', 'large', 'png', 'art_crop', 'border_crop']
    def image_url(self, size: str = 'normal') -> str:
        """Returns a link to the card, of the appropriate size."""
        return f"{self.IMG_URL}{size}/{self.IMG_SIDE}/{self.ID[0]}/{self.ID[1]}/{self.ID}.jpg"


class Card:
    SCRY_URL = 'https://scryfall.com/card/'
    API_URL = 'https://api.scryfall.com/cards/'
    IMG_URL = 'https://c1.scryfall.com/file/scryfall-cards/'

    def _handle_card_faces(self, json: dict[str, Union[str, dict[str, str], list[str]]]) -> None:
        """
        Automatically generates and sets the CardFaces for the Card object.
        :param json: The card data.
        """
        if self.LAYOUT == CardLayouts.NORMAL:
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

    def __init__(self, json: dict[str, Union[str, dict[str, str], list[str]]]):
        if json['object'] != 'card':
            raise Exception("Invalid JSON provided! Object type is not 'card'")

        # Card ID info
        self.ID = json['id']
        self.ARENA_ID = json.get('arena_id')  # TODO: Handle Remastered Arena sets.
        self.SET = json['set'].upper()
        self.RARITY = RARITY_ALIASES[json['rarity']]
        self.NUMBER = json['collector_number']
        self.COLOR_IDENTITY = get_color_identity("".join(json['color_identity']))
        self.CMC = json['cmc']  # TODO: Have this handled by a card face later.
        self.LAYOUT = LAYOUT_DICT[json['layout']]
        self.TWO_SIDED = self.LAYOUT is CardLayouts.TWO_SIDED
        self.SPLIT = self.LAYOUT is CardLayouts.FUSED
        self._handle_card_faces(json)

    @property
    def name(self) -> str:
        """Gets the simple name of the card"""
        if self.LAYOUT == CardLayouts.SPLIT:
            return self.DEFAULT_FACE.NAME
        else:
            return self.FACE_1.NAME

    @property
    def full_name(self) -> str:
        """Gets the full name of the card"""
        return self.DEFAULT_FACE.NAME

    @property
    def mana_cost(self) -> str:
        """Gets the mana cost of the card"""
        return self.DEFAULT_FACE.MANA_COST

    @property
    def api(self) -> str:
        """Link for the API call of the card"""
        return f"{self.API_URL}{self.ID}"

    @property
    def url(self) -> str:
        """Shortened link to the Scryfall page for the card"""
        return f"{self.SCRY_URL}{self.SET.lower()}/{self.NUMBER}"

    @property
    def image_url(self) -> str:
        """Returns a link to the image of the card."""
        return self.DEFAULT_FACE.image_url('normal')

    # TODO: Consider removing this.
    def list_contents(self) -> str:
        """Returns a text summary of the card. Mainly meant for debugging."""
        s = ""
        s += f"NAME: {self.name}\n"
        s += f"FULL_NAME: {self.full_name}\n"
        s += f"MANA_COST: {self.mana_cost}\n"
        for key in self.__dict__.keys():
            s += f"{key}: {self.__dict__[key]}\n"
            if isinstance(self.__dict__[key], CardFace):
                for k in self.__dict__[key].__dict__.keys():
                    s += f"  {k}: {self.__dict__[key].__dict__[k]}\n"
                s += f"  IMAGE_URL: {self.__dict__[key].image_url()}\n"
        s += f"IMAGE_URL: {self.image_url}\n"
        s += f"API: {self.api}\n"
        s += f"URL: {self.url}\n"
        return s

    def __str__(self):
        return self.full_name

    def __repr__(self):
        return self.full_name
