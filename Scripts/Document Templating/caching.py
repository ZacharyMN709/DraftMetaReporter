import logging

import requests
from time import sleep
from functools import cache

import config as cfg

# Create a blank cache to fll with data.
CARD_CACHE = dict()


def populate_cache(sets):
    """Load the data for the provided sets into the cache."""
    start_cnt = len(CARD_CACHE)

    base_url = "https://api.scryfall.com/cards/search?format=json&order=set&q=e%3A"
    for s in sets:
        next_url = base_url + s
        while next_url is not None:
            response = requests.get(next_url)
            sleep(0.1)  # Scryfall requests this, so I try to be a good citizen.
            data = response.json()
            next_url = None
            if 'next_page' in data:
                next_url = data['next_page']
            for card in data['data']:
                CARD_CACHE[card['name']] = card

    end_cnt = len(CARD_CACHE)
    logging.debug(f"{end_cnt - start_cnt} cards added to `CARD_CACHE`")


@cache  # Save the results, so we don't re-query stuff we have in CARD_CACHE.
def get_card_data(card_name):
    """Get data for a card based on it's name, taking it from the cache if at all possible."""
    if card_name in CARD_CACHE:
        return CARD_CACHE[card_name]

    search_url = f"https://api.scryfall.com/cards/named?fuzzy={card_name}"
    response = requests.get(search_url)
    data = response.json()
    sleep(0.1)  # Scryfall requests this, so I try to be a good citizen.

    if data["object"] == 'card':
        if data['name'] in CARD_CACHE:
            return CARD_CACHE[data['name']]
        else:
            return data
    else:
        print(f"Could not find card for '{card_name}'")
        return None


@cache  # Save the results so if we remake the document, we don't re-fetch all the images.
def get_image_data(card_image_url):
    """Get the image for a given url."""
    response = requests.get(card_image_url)
    image_data = response.content
    sleep(0.1)  # Scryfall requests this, so I try to be a good citizen.
    return image_data


populate_cache(cfg.SETS)
