"""
This package query magic-related data from websites, chiefly 17Lands and Scryfall.
"""

from core.data_requesting.utils import *
from core.data_requesting.Requester import *
from core.data_requesting.Request17Lands import *
from core.data_requesting.RequestScryfall import *

from_utils = ['BASE_17L_URL', 'DEFAULT_FORMAT', 'DEFAULT_DATE']

from_requester = ['Requester']

from_request_17lands = ['Request17Lands']

from_request_scryfall = ['RequestScryfall']


__all__ = from_utils + from_requester + from_request_17lands + from_request_scryfall
