from typing import Union, Optional, NoReturn, Any

from utilities.auto_logging import logging
from utilities.utils.funcs import flatten_lists

from data_interface.Requester import Requester


class RequestScryfall(Requester):
    """ A small class which helps get specific data from scryfall, handling the minutia of json checking. """
    _BASE_URL = 'https://api.scryfall.com/'

    def __init__(self, tries: Optional[int] = None, fail_delay: Optional[float] = None,
                 success_delay: Optional[float] = None):
        super().__init__(tries, fail_delay, success_delay)

    def _get_set_cards(self, set_code: str, order: str) -> Union[NoReturn, list[dict[str, Any]]]:
        params = {
            'format': 'json',
            'q': f'e%3A{set_code}',
            'is': 'booster',
            'unique': 'cards',
            'order': order,
            'include_multilingual': False,
            'include_extras': False,
        }
        url = f'{self._BASE_URL}cards/search'
        logging.info(f"Fetching card data for set: {set_code}")
        return flatten_lists([x['data'] for x in self.paginated_request(url, params=params)])

    def get_set_cards(self, set_code: str) -> Union[NoReturn, list[dict[str, Any]]]:
        return self._get_set_cards(set_code, 'set')

    def get_set_review_order(self, set_code: str) -> Union[NoReturn, list[dict[str, Any]]]:
        return self._get_set_cards(set_code, 'review')

    def get_set_info(self, set_code: str) -> Union[NoReturn, tuple[str, str]]:
        url = f'{self._BASE_URL}sets/{set_code}'
        logging.info(f"Fetching data for set: {set_code}")
        response = self.request(url)
        return response['name'], response['icon_svg_uri']

    def get_card_by_name(self, name: str) -> Union[NoReturn, dict[str, Any]]:
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
        response = self.request(f'{self._BASE_URL}cards/named', params)

        # If is not a card, do some processing and return the struct with some information.
        if response['object'] != 'card':
            logging.verbose(f"A non-card was returned for {name}")
            # If the response type is an error, use that as the message.
            if response['details'][:20] == 'Too many cards match':
                response['err_msg'] = f'Error: Multiple card matches for "{name}"'
            else:
                response['err_msg'] = f'Error: Cannot find card "{name}"'

        return response

    # NOTE: The two functions below are expensive and slow, especially to Scryfall.
    #  They should be called only as required.
    def get_arena_cards(self) -> Union[NoReturn, list[dict[str, Any]]]:
        params = {
            'format': 'json',
            'q': f'game%3Aarena',
        }
        url = f'{self._BASE_URL}/cards/search'
        logging.info(f"Fetching card data for all Arena cards.")
        return flatten_lists([x['data'] for x in self.paginated_request(url, params=params)])

    def get_bulk_data(self) -> Union[NoReturn, list[dict[str, Any]]]:
        logging.info(f"Fetching bulk data...")
        response = self.request(f'{self._BASE_URL}bulk-data/oracle-cards')
        return self.request(response['download_uri'])
