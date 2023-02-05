"""
This package helps simplify managing code which requests data from websites.
"""

from core.data_requesting.utils.consts import *
from core.data_requesting.utils.funcs import *
from core.data_requesting.utils.settings import *

from_consts = ['BASE_17L_URL', 'COLOR_17L_URL', 'EXPANSIONS_17L_URL', 'FORMATS_17L_URL', 'PLAY_DRAW_17L_URL',
               'COLOR_RATING_17L_URL', 'CARD_RATING_17L_URL', 'CARD_EVAL_17L_URL', 'TROPHY_17L_URL',
               'DRAFT_LOG_17L_URL', 'DECK_17L_URL', 'DETAILS_17L_URL', 'TIER_17L_URL',
               'BASE_SCRYFALL_URL', 'CARD_SCRYFALL_URL', 'SET_SCRYFALL_URL',
               'FUZZY_SCRYFALL_URL', 'BULK_SCRYFALL_URL']

from_funcs = ['clean_card_tier']

from_settings = ['TRIES', 'FAIL_DELAY', 'SUCCESS_DELAY', 'DEFAULT_FORMAT', 'DEFAULT_DATE']


__all__ = from_consts + from_funcs + from_settings
