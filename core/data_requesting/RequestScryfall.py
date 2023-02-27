"""
A small class which helps get specific data from scryfall, handling the minutia of json checking.
"""

from typing import Union, Optional, Any

from core.utilities import logging, flatten_lists

from core.data_requesting.utils import *
from core.data_requesting.Requester import Requester


class RequestScryfall(Requester):
    """ A small class which helps get specific data from scryfall, handling the minutia of json checking. """
    def __init__(self, tries: int = None, fail_delay: float = None, success_delay: float = None):
        super().__init__(tries, fail_delay, success_delay, [200, 404])

    def _get_set_cards(self, set_code: str, order: str = 'set') -> list[dict[str, Any]]:
        """
        Gets the cards from a given set, with an optional order.
        :param set_code: The set to get cards for.
        :param order: The order in which cards are returned. Default: 'set'
        :return: A list of card json objects.
        """
        params = {
            'format': 'json',
            'q': f'e%3A{set_code}',
            'is': 'booster',
            'unique': 'cards',
            'order': order,
            'include_multilingual': False,
            'include_extras': False,
        }
        logging.info(f"Fetching card data for set: {set_code}")
        responses = self.get_paginated_json_response(CARD_SCRYFALL_URL, params=params)

        # Create a list to store the returned json objects.
        ret = list()

        # For each response, check that the data exists in the response and add it to the return list.
        for response in responses:
            if 'data' in response:
                ret.append(response['data'])

        # If no data was found, likely due to a bad order or set code, return the empty list.
        if len(ret) == 0:
            return ret

        # Otherwise, flatten the lists into one long list, to handle more easily.
        return flatten_lists(ret)

    def get_set_cards(self, set_code: str) -> list[dict[str, Any]]:
        """
        Gets the cards from a given set, in the 'set' order (based on card number).
        :param set_code: The set to get cards for.
        :return: A list of card json objects.
        """
        return self._get_set_cards(set_code, 'set')

    def get_set_review_order(self, set_code: str) -> list[dict[str, Any]]:
        """
        Gets the cards from a given set, in the 'review' order (based on cmc/mv and rarity).
        :param set_code: The set to get cards for.
        :return: A list of card json objects.
        """
        return self._get_set_cards(set_code, 'review')

    def get_set_info(self, set_code: str) -> Union[tuple[None, None], tuple[str, str]]:
        """
        Gets the name and the icon for a set.
        :param set_code: The 3-character code for the set.
        :return: The full set name and a link to the set symbol. If the set cannot be found Nones are returned.
        """
        url = f'{SET_SCRYFALL_URL}/{set_code}'
        logging.info(f"Fetching data for set: {set_code}")
        response = self.get_json_response(url)

        try:
            return response['name'], response['icon_svg_uri']
        except KeyError:
            logging.warning(f"No info for set: {set_code}")
            return None, None

    def get_card_by_name(self, name: str) -> Optional[dict[str, Any]]:
        """
        Gets card data from scryfall based on a name. Scryfall's fuzzy filter is
        used to handle imprecise queries and spelling errors.
        :param name: The card name provided by a user
        :return: A card info struct which contains card data, and an error
        message if a problem occurred.
        """
        params = {
            "fuzzy": name
        }

        # Attempt to get information on the card.
        logging.info(f"Fetching data for card: {name}")
        response = self.get_json_response(FUZZY_SCRYFALL_URL, params)

        # If the response is not None, but not a card, do some processing and return the struct with some information.
        if response is not None and response['object'] != 'card':
            logging.verbose(f"A non-card was returned for {name}")
            # If the response type is an error, use that as the message.
            if response['details'][:20] == 'Too many cards match':
                response['err_msg'] = f'Error: Multiple card matches for "{name}"'
            else:
                response['err_msg'] = f'Error: Cannot find card "{name}"'

        return response

    # NOTE: The two functions below are expensive and slow, especially to Scryfall.
    #  They should be called only as required.
    def get_arena_cards(self) -> list[dict[str, Any]]:
        """
        Gets all cards which are currently available on arena.
        :return: A list of card json objects.
        """
        params = {
            'format': 'json',
            'q': f'game%3Aarena',
        }
        logging.info(f"Fetching card data for all Arena cards.")
        return flatten_lists([x['data'] for x in self.get_paginated_json_response(CARD_SCRYFALL_URL, params=params)])

    def get_bulk_data(self) -> list[dict[str, Any]]:
        """
        Gets all cards which are stored on Scryfall.
        :return: A list of card json objects.
        """
        logging.info(f"Fetching bulk data...")
        response = self.get_json_response(BULK_SCRYFALL_URL)
        return self.get_json_response(response['download_uri'])
