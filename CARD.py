from enum import unique

from CallScryfall import CallScryfall
from consts import RARITY_ALIASES
from WUBRG import get_color_identity


def safe_get(dic, key):
    return dic[key] if key in dic else None 


class CardLayouts():
    NORMAL = 0
    ADVENTURE = 1
    SPLIT = 2
    TRANSFORM = 3
    MODAL_DFC = 4


class CardFace():
    SCRY_URL = 'https://scryfall.com/card/'
    API_URL = 'https://api.scryfall.com/cards/'
    IMG_URL = 'https://c1.scryfall.com/file/scryfall-cards/'

    
    # sides = ['default', 'left', 'right', 'creature', 'adventure']
    def SingleFace(json, side='default'):            
        face = CardFace(json, side)
        
        # Modify 'default' as needed for easy access to data.
        if side == 'default':
            face.NAME = safe_get(json, 'name')
            face.MANA_COST = safe_get(json, 'mana_cost')
            face.TYPE_LINE = safe_get(json, 'type_line')
       
        return face

    
    # sides = ['default', 'front', 'back']
    def DoubleFaced(json, side='default'):
        face = CardFace(json, side)
        
        # Modify 'default' as needed for easy access to data.
        if side == 'default':
            face.NAME = safe_get(json, 'name')
            face.TYPE_LINE = safe_get(json, 'type_line')

        return face

    
    def __init__(self, json, side):
        if side in ['back', 'adventure', 'right']:
            sub_json = json['card_faces'][1]
        else:
            if 'card_faces' in json:
                sub_json = json['card_faces'][0]
            else:
                sub_json = json
        
        self.ID = json['id']
        self.NAME = safe_get(sub_json, 'name')
        self.MANA_COST = safe_get(sub_json, 'mana_cost')
        #self.CMC = safe_get(sub_json, 'cmc')  #TODO: Handle this more precicely later.
        self.COLORS = safe_get(sub_json, 'colors')
        if self.COLORS is not None:
            self.COLORS = get_color_identity("".join(self.COLORS))
        self.TYPE_LINE = safe_get(sub_json, 'type_line')
        
        self.ORACLE = safe_get(sub_json, 'oracle_text')
        self.FLAVOR_TEXT = safe_get(sub_json, 'flavor_text')
        
        self.POW = safe_get(sub_json, 'power')
        self.TOU = safe_get(sub_json, 'toughness')
        
        self.CARD_SIDE = side
        self.IMG_SIDE = 'back' if side == 'back' else 'front'
        
    # sizes = ['small', 'normal', 'large', 'png', 'art_crop', 'border_crop']
    def IMAGE_URL(self, size='normal'):
        """Returns a link to the card, of the appropriate size."""
        return f"{self.IMG_URL}{size}/{self.IMG_SIDE}/{self.ID[0]}/{self.ID[1]}/{self.ID}.jpg"


class Card():
    # https://scryfall.com/docs/api/layouts has information about card layouts,
    # which are necessary for determining how to handle a card.
    # relevant_layouts = ['normal', adventure', 'split', 'transform', 'modal_dfc']
        
    SCRY_URL = 'https://scryfall.com/card/'
    API_URL = 'https://api.scryfall.com/cards/'
    IMG_URL = 'https://c1.scryfall.com/file/scryfall-cards/'
    
    def from_name(name):
        scry = CallScryfall()
        json = scry.get_card_by_name(name)
        return Card(json)
    
    def _handle_card_faces(self, json):
        if self.LAYOUT == CardLayouts.NORMAL:
            self.DEFAULT_FACE = CardFace.SingleFace(json)
            self.FACE_1 = self.DEFAULT_FACE
            self.FACE_2 = None
        elif self.LAYOUT == CardLayouts.ADVENTURE: 
            self.DEFAULT_FACE = CardFace.SingleFace(json)
            self.FACE_1 = CardFace.SingleFace(json, 'creature')
            self.FACE_2 = CardFace.SingleFace(json, 'adventure')
        elif self.LAYOUT == CardLayouts.SPLIT: 
            self.DEFAULT_FACE = CardFace.SingleFace(json)
            self.FACE_1 = CardFace.SingleFace(json, 'left')
            self.FACE_2 = CardFace.SingleFace(json, 'right')
        elif self.LAYOUT == CardLayouts.TRANSFORM: 
            self.DEFAULT_FACE = CardFace.DoubleFaced(json)
            self.FACE_1 = CardFace.DoubleFaced(json, 'front')
            self.FACE_2 = CardFace.DoubleFaced(json, 'back')
        elif self.LAYOUT == CardLayouts.MODAL_DFC: 
            self.DEFAULT_FACE = CardFace.DoubleFaced(json)
            self.FACE_1 = CardFace.DoubleFaced(json, 'front')
            self.FACE_2 = CardFace.DoubleFaced(json, 'back')
        else: raise Exception(f"Unknown layout '{layout}'")
            
    def _handle_layout(self, layout):
        if layout == 'normal': 
            self.LAYOUT = CardLayouts.NORMAL
        elif layout == 'adventure': 
            self.LAYOUT = CardLayouts.ADVENTURE
        elif layout == 'split': 
            self.LAYOUT = CardLayouts.SPLIT
        elif layout == 'transform': 
            self.LAYOUT = CardLayouts.TRANSFORM
        elif layout == 'modal_dfc': 
            self.LAYOUT = CardLayouts.MODAL_DFC
        else: raise Exception(f"Unknown layout '{layout}'")

        self.TWO_SIDED = layout in ['transform', 'modal_dfc']
        self.SPLIT = layout in ['adventure', 'split']
        
    def __init__(self, json):
        if json['object'] != 'card':
            raise Exception("Invalid JSON provided! Object type is not 'card'")
        
        # Card ID info
        self.ID = json['id']
        self.ARENA_ID = safe_get(json, 'arena_id')  #TODO: Handle Remastered Arena sets.
        self.SET = json['set'].upper()
        self.RARITY = RARITY_ALIASES[json['rarity']]
        self.NUMBER = json['collector_number']
        self.COLOR_IDENTITY = get_color_identity("".join(json['color_identity']))
        self.CMC = json['cmc'] ## TODO: Have this handled by a card face later.
        self._handle_layout(json['layout'])
        self._handle_card_faces(json)
      
    @property
    def NAME(self):
        """Gets the simple name of the card"""
        if self.LAYOUT == CardLayouts.SPLIT:
            return self.DEFAULT_FACE.NAME
        else:
            return self.FACE_1.NAME
    
    @property
    def FULL_NAME(self):
        """Gets the full name of the card"""
        return self.DEFAULT_FACE.NAME
    
    @property
    def MANA_COST(self):
        """Gets the mana cost of the card"""
        return self.DEFAULT_FACE.MANA_COST
        
    @property
    def API(self):
        """Link for the API call of the card"""
        return f"{self.API_URL}{self.ID}"

    @property
    def URL(self):
        """Shortened link to the Scryfall page for the card"""
        return f"{self.SCRY_URL}{self.SET.lower()}/{self.NUMBER}"
    
    @property
    def IMAGE_URL(self):
        """Returns a link to the image of the card."""
        return self.DEFAULT_FACE.IMAGE_URL('normal')
    
    def list_contents(self):
        s = ""
        s += f"NAME: {self.NAME}\r\n"
        s += f"FULL_NAME: {self.FULL_NAME}\r\n"
        s += f"MANA_COST: {self.MANA_COST}\r\n"
        for key in self.__dict__.keys():
            s += f"{key}: {self.__dict__[key]}\r\n"
            if isinstance(self.__dict__[key], CardFace):
                for k in self.__dict__[key].__dict__.keys():
                    s += f"  {k}: {self.__dict__[key].__dict__[k]}\r\n"
                s += f"  IMAGE_URL: {self.__dict__[key].IMAGE_URL()}\r\n"
        s += f"IMAGE_URL: {self.IMAGE_URL}\r\n"
        s += f"API: {self.API}\r\n"
        s += f"URL: {self.URL}\r\n"
        return s

    def __str__(self):
        return self.FULL_NAME

    def __repr__(self):
        return self.FULL_NAME
