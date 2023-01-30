"""
This package helps simplify creating and managing code which requests data from websites.
"""

from data_interface.utils.consts import *
from data_interface.utils.settings import *

from_consts = ['BASE_17L_URL', 'COLOR_17L_URL', 'EXPANSIONS_17L_URL', 'FORMATS_17L_URL', 'PLAY_DRAW_17L_URL',
               'COLOR_RATING_17L_URL', 'CARD_RATING_17L_URL', 'CARD_EVAL_17L_URL', 'TROPHY_17L_URL',
               'DRAFT_LOG_17L_URL', 'DECK_17L_URL', 'DETAILS_17L_URL', 'TIER_17L_URL']

from_settings = ['TRIES', 'FAIL_DELAY', 'SUCCESS_DELAY', 'DEFAULT_FORMAT', 'DEFAULT_DATE']


__all__ = from_consts + from_settings
