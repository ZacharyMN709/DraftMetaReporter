"""
This package helps simplify dealing with the properties of cards, decks and drafts in Magic.
It provides values surrounding card faces, card rarities, and card types. It also has Arena's user ranks.
"""

from game_metadata.utils.consts import *
from game_metadata.utils.funcs import *
from game_metadata.utils.settings import *


from_consts = ['RANKS', 'RARITIES', 'RARITY_ALIASES', 'SUPERTYPES', 'TYPES', 'SUBTYPES', 'SUBTYPE_DICT', 'CardLayouts']

from_funcs = ['new_color_count_dict']

from_settings = ['SETS', 'FORMATS', 'SET_CONFIG']


__all__ = from_consts + from_funcs + from_settings
