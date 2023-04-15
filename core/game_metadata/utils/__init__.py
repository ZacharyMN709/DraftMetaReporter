"""
This package helps simplify dealing with the properties of cards, decks and drafts in Magic.
It provides values surrounding card faces, card rarities, and card types. It also has Arena's user ranks.
"""

from core.game_metadata.utils.consts import *
from core.game_metadata.utils.funcs import *
from core.game_metadata.utils.settings import *
from core.game_metadata.utils.typing import *


from_consts = ['DATE_FMT', 'RANKS', 'RARITIES', 'RARITY_ALIASES',
               'SUPERTYPES', 'TYPES', 'SUBTYPES', 'SUBTYPE_DICT', 'CardLayouts']

from_funcs = ['new_color_count_dict']

from_settings = ['SETS', 'SET_EXTRAS', 'FORMATS', 'SET_CONFIG']

from_typing = ['RARITY', 'RANK', 'CARD_INFO', 'CARD_SIDE',
               'SUPERTYPE', 'TYPE', 'LAND_SUBTYPE', 'CREATURE_SUBTYPE', 'ARTIFACT_SUBTYPE', 'ENCHANTMENT_SUBTYPE',
               'PLANESWALKER_SUBTYPE', 'INSTANT_SUBTYPE', 'SORCERY_SUBTYPE', 'SUBTYPE', 'ANY_TYPE']


__all__ = from_consts + from_funcs + from_settings + from_typing
