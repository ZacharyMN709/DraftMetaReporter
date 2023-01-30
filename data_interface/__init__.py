"""
This package query magic-related data from websites, chiefly 17Lands and Scryfall.
"""

from data_interface.utils import *
from data_interface.Requester import *
from data_interface.Request17Lands import *
from data_interface.RequestScryfall import *

from_utils = ['BASE_17L_URL', 'DEFAULT_FORMAT', 'DEFAULT_DATE']

from_requester = ['Requester']

from_request_17lands = ['Request17Lands']

from_request_scryfall = ['RequestScryfall']


__all__ = from_utils + from_requester + from_request_17lands + from_request_scryfall
