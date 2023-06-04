import logging
import requests
from io import BytesIO
from PIL import Image
from time import sleep
from functools import cache

import config as cfg

# Create a blank cache to fill with data.
CARD_CACHE = dict()


def populate_cache(sets):
    """Load the data for the provided sets into the cache."""
    start_cnt = len(CARD_CACHE)

    base_url = "https://api.scryfall.com/cards/search?format=json&order=set&q=e%3A"
    for s in sets:
        next_url = base_url + s
        while next_url is not None:
            response = requests.get(next_url)
            sleep(0.1)  # Scryfall requests this, so I try to be a good netizen.
            data = response.json()
            next_url = None
            if 'next_page' in data:
                next_url = data['next_page']
            for card in data['data']:
                logging.debug(f"Adding '{card['name']}' to `CARD_CACHE`")
                CARD_CACHE[card['name']] = card
                if "card_faces" in card:
                    face = card['card_faces'][0]
                    logging.debug(f"Adding '{face['name']}' to `CARD_CACHE`")
                    CARD_CACHE[face['name']] = card

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
    sleep(0.1)  # Scryfall requests this, so I try to be a good netizen.

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
    sleep(0.1)  # Scryfall requests this, so I try to be a good netizen.
    return image_data


def format_image(card_image_url, rotate, out_loc):
    image_data = get_image_data(card_image_url)

    with BytesIO(image_data) as b_io:
        with Image.open(b_io) as img:
            new_height = cfg.HEIGHT
            new_width = cfg.WIDTH

            if rotate:
                img = img.rotate(270, expand=True)  # Rotate image by -90 degrees
                new_height, new_width = new_width, new_height  # Switch the height and width, since we've rotated.

            # Save the image fetched from the web as a JPEG, then use that file location to add the image into the docx.
            img.save(out_loc, format='JPEG')
    return new_height, new_width


def download_card_image(card_name):
    def _get_url(face):
        uris = ['large', 'border_crop', 'normal', 'small', 'art_crop']
        for uri in uris:
            if uri in face["image_uris"]:
                return face["image_uris"][uri]

    card_data = get_card_data(card_name)

    if "layout" in card_data and card_data["layout"] == "transform":
        front_face = card_data["card_faces"][0]
        rotate = front_face['type_line'] == 'Battle — Siege'
        height, width = format_image(_get_url(front_face), rotate, cfg.TEMP_FRONT_LOC)
        front = Image.open(cfg.TEMP_FRONT_LOC)

        back_face = card_data["card_faces"][1]
        h, w = format_image(_get_url(back_face), False, cfg.TEMP_BACK_LOC)
        height = max(height, h)
        width += w
        back = Image.open(cfg.TEMP_BACK_LOC)

        new = Image.new('RGBA', (front.size[0] + back.size[0], max(front.size[1], back.size[1])), (255, 255, 255, 255))
        new.paste(front, (0, (new.size[1] - front.size[1]) // 2))
        new.paste(back, (front.size[0], (new.size[1] - back.size[1]) // 2))
        new.save(cfg.TEMP_LOC, format='PNG')
    else:
        height, width = format_image(_get_url(card_data), False, cfg.TEMP_LOC)

    return height, width

