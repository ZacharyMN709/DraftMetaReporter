from typing import Union, Callable, Optional

from Utilities.auto_logging import logging
from Utilities import Fetcher


# A decorator which automatically catches and logs error when querying scryfall.
def trap_error(func: Callable) -> Callable:
    def arg_wrapper(arg1, arg2):
        try:
            return func(arg1, arg2)
        except Exception as ex:
            logging.error(f'Error: Error occurred while querying Scryfall!')
            if isinstance(ex, KeyError):
                logging.error(f"{ex} was not found in the returned json.")
            else:
                logging.error(ex)
            return None
    return arg_wrapper


# TODO: Figure out proper contingencies for connection errors.
class CallScryfall:
    """ A small class which helps get specific data from scryfall, handling the minutia of json checking. """
    _BASE_URL = 'https://api.scryfall.com/'
    FETCHER = Fetcher()

    @classmethod
    @trap_error
    def get_set_cards(cls, set_code: str) -> Optional[list[dict[str, Union[str, dict[str, str], list[str]]]]]:
        cards = []
        next_page = True
        url = f'{cls._BASE_URL}cards/search?format=json&include_extras=false&include_multilingual=false' \
              f'&order=set&page=1&q=e%3A{set_code}&unique=cards'
        logging.info(f"Fetching card data for set: {set_code}")

        while next_page:
            response: dict[str, object] = cls.FETCHER.fetch(url)
            cards += response['data']
            if response['has_more']:
                url = response['next_page']
                logging.debug(f"Fetching next page for set: {set_code}")
                logging.debug(f"URL: {url}")
            else:
                next_page = False

        return cards

    @classmethod
    @trap_error
    def get_set_info(cls, set_code: str) -> Optional[tuple[str, str]]:
        url = f'{cls._BASE_URL}sets/{set_code}'
        logging.info(f"Fetching data for set: {set_code}")
        response: dict[str, str] = cls.FETCHER.fetch(url)
        return response['name'], response['icon_svg_uri']

    @classmethod
    @trap_error
    def get_card_by_name(cls, name: str) -> Optional[dict[str, Union[str, dict[str, str], list[str]]]]:
        """
        Gets card data from scryfall based on a name. Scryfall's fuzzy filter is
        used to handle imprecise queries and spelling errors.
        :param name: The card name provided by a user
        :return: A card info struct which contains card data, and an error
        message if a problem occurred.
        """
        card_info = dict()
        card_info['name'] = name

        # Attempt to get information on the card.
        logging.info(f"Fetching data for card: {name}")
        response = cls.FETCHER.fetch(f'{cls._BASE_URL}cards/named?fuzzy={name}')

        # If is not a card, do some processing and return the struct with some information.
        if response['object'] != 'card':
            logging.verbose(f"A non-card was returned for {name}")
            # If the response type is an error, use that as the message.
            if response['details'][:20] == 'Too many cards match':
                response['err_msg'] = f'Error: Multiple card matches for "{name}"'
            else:
                response['err_msg'] = f'Error: Cannot find card "{name}"'

        return response
