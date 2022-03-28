import requests
from time import sleep
from datetime import date, time, datetime, timedelta

from Logger import Logger
from Fetcher import Fetcher

class CallScryfall():   
    _BASE_URL = 'https://api.scryfall.com/'
    FETCHER = Fetcher()
    
    def get_set_cards(SET):
        cards = []
        next_page = True
        url = f'{CallScryfall._BASE_URL}cards/search?format=json&include_extras=false&include_multilingual=false&order=set&page=1&q=e%3A{SET}&unique=cards'
        Logger.LOGGER.log(f"Fetching card data for set: {SET}", Logger.FLG.DEFAULT)

        while next_page:
            response = CallScryfall.FETCHER.fetch(url)
            cards += response['data']
            if response['has_more']:
                url = response['next_page']
                Logger.LOGGER.log(f"Fetching next page for set: {SET}", Logger.FLG.VERBOSE)
                Logger.LOGGER.log(f"URL: {url}", Logger.FLG.DEBUG)
            else:
                next_page = False
        
        return cards
    
    def get_card_by_name(NAME):
        """
        Gets card data from scryfall based on a name. Scryfall's fuzzy filter is
        used to handle imprecise queries and spelling errors.
        :param raw_card_name: The card name provided by a user
        :return: A card info struct which contains card data, and an error
        message if a problem occurred.
        """
        card_info = dict()
        card_info['name'] = NAME

        # Attempt to get information on the card.
        try:
            Logger.LOGGER.log(f"Fetching data for card: {NAME}", Logger.FLG.DEFAULT)
            response = CallScryfall.FETCHER.fetch(f'{CallScryfall._BASE_URL}cards/named?fuzzy={NAME}')

            # If is not a card, do some processing and return the struct with some information.
            if response['object'] != 'card':
                Logger.LOGGER.log(f"A non-card was returned for {NAME}", Logger.FLG.VERBOSE)
                # If the response type is an error, use that as the message.
                if response['object'] == 'error':
                    if response['details'][:20] == 'Too many cards match':
                        card_info['err_msg'] = f'Error: Multiple card matches for "{NAME}"'
                    else:
                        card_info['err_msg'] = f'Error: Cannot find card "{NAME}"'
                # If the search return a non-card, add that as the error message.
                else:
                    card_info['err_msg'] = f'Error: "{NAME}" returned non-card'
                Logger.LOGGER.log(card_info['err_msg'], Logger.FLG.DEBUG)
                return card_info
        # If an exception occurs, print it, and add an error massage to the struct.
        except Exception as ex:
            Logger.LOGGER.log(ex, Logger.FLG.ERROR)
            card_info['err_msg'] = f'Error: Failed to query Scryfall for {NAME}\r\n{ex}'
            return card_info
            
        # If no problems occurred, get the relevant card info and populate the card_info_struct
        return response
    
##        # Unusued properties that exist and can be reomved.
##        card_ids = ['oracle_id', 'mtgo_id', 'multiverse_ids', 'tcgplayer_id', 'cardmarket_id']
##        art_props = ['highres_image', 'image_status', 'image_uris', 'uri', 'artist', 'artist_ids', 'artist_id', 'illustration_id']
##        set_props = ['set_id', 'set_name', 'set_type', 'set_uri', 'set_search_uri', 'scryfall_set_uri', 'booster']
##        card_props = ['lang', 'variation', 'full_art', 'textless', 'oversized',
##                      'finishes', 'foil', 'nonfoil', 'promo', 'card_back_id', 
##                      'frame', 'security_stamp', 'watermark', 'border_color', 'story_spotlight']
##        prices = ['prices', 'purchase_uris', 'reserved']
##        games = ['legalities', 'games', 'digital', 'edhrec_rank']
##        uris = ['rulings_uri', 'prints_search_uri', 'related_uris', 'scryfall_uri']
##        release = ['released_at', 'preview', 'reprint']
##        
##        to_remove = card_ids + art_props + set_props + card_props + prices + games + uris + release
##
##        # Make a list of high-level card objects.
##        objs = [response]
##        if 'card_faces' in response: objs +=response['card_faces']
##        
##         Remove any of the unwanted properties from the objects.
##        for obj in objs:
##            for prop in to_remove:
##                if prop in obj: del obj[prop]
