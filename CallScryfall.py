from utils.Logger import Logger
from utils.Fetcher import Fetcher


class CallScryfall:
    _BASE_URL = 'https://api.scryfall.com/'
    FETCHER = Fetcher()

    @staticmethod
    def get_set_cards(set_name: str):
        cards = []
        next_page = True
        url = f'{CallScryfall._BASE_URL}cards/search?format=json&include_extras=false&include_multilingual=false' \
              f'&order=set&page=1&q=e%3A{set_name}&unique=cards '
        Logger.LOGGER.log(f"Fetching card data for set: {set_name}", Logger.FLG.DEFAULT)

        while next_page:
            response: dict[str, object] = CallScryfall.FETCHER.fetch(url)
            cards += response['data']
            if response['has_more']:
                url = response['next_page']
                Logger.LOGGER.log(f"Fetching next page for set: {set_name}", Logger.FLG.VERBOSE)
                Logger.LOGGER.log(f"URL: {url}", Logger.FLG.DEBUG)
            else:
                next_page = False

        return cards

    @staticmethod
    def get_card_by_name(name: str):
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
        try:
            Logger.LOGGER.log(f"Fetching data for card: {name}", Logger.FLG.DEFAULT)
            response: dict[str, object] = \
                CallScryfall.FETCHER.fetch(f'{CallScryfall._BASE_URL}cards/named?fuzzy={name}')

            # If is not a card, do some processing and return the struct with some information.
            if response['object'] != 'card':
                Logger.LOGGER.log(f"A non-card was returned for {name}", Logger.FLG.VERBOSE)
                # If the response type is an error, use that as the message.
                if response['object'] == 'error':
                    if response['details'][:20] == 'Too many cards match':
                        card_info['err_msg'] = f'Error: Multiple card matches for "{name}"'
                    else:
                        card_info['err_msg'] = f'Error: Cannot find card "{name}"'
                # If the search return a non-card, add that as the error message.
                else:
                    card_info['err_msg'] = f'Error: "{name}" returned non-card'
                Logger.LOGGER.log(card_info['err_msg'], Logger.FLG.DEBUG)
                return card_info
        # If an exception occurs, print it, and add an error massage to the struct.
        except Exception as ex:
            Logger.LOGGER.log(ex, Logger.FLG.ERROR)
            card_info['err_msg'] = f'Error: Failed to query Scryfall for {name}\r\n{ex}'
            return card_info

        # If no problems occurred, get the relevant card info and populate the card_info_struct
        return response
