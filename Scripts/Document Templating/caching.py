from typing import Optional, Iterable

import logging
import requests
from io import BytesIO
from PIL import Image
from time import sleep
from functools import cache

import config as cfg


class Scryfall:
    @classmethod
    @cache
    def _request(cls, url: str) -> requests.Response:
        """
        Request data from a url, with an automatic delay that Scryfall requests.
        :param url: The url to request data from.
        :return: The response from the request.
        """
        response = requests.get(url)
        sleep(0.1)  # Scryfall requests this, so I try to be a good netizen.
        return response

    @classmethod
    def scryfall_search(cls, query: str) -> dict[str, dict]:
        """
        Search scryfall for multiple cards, populating the card cache with the results.
        :param query: The query to use, formatted for url.
        :return: A list of names added to the cache.
        """
        cards = dict()
        url = f"https://api.scryfall.com/cards/search?format=json&order=set&q={query}"
        while url:
            data = cls._request(url).json()
            url = data.get('next_page', None)
            cards |= {card['name']: card for card in data['data']}

        return cards

    @classmethod
    def scryfall_card(cls, query: str) -> Optional[dict]:
        """
        Search scryfall for a specific card, populating the card cache with the results.
        :param query: The url parameter/path for the card.
        :return: The card data, if found.
        """
        url = f"https://api.scryfall.com/cards/{query}"
        data = cls._request(url).json()

        if data["object"] == 'card':
            return data["object"]
        else:
            logging.warning(f"Could not find card for '{url}'")
            return None

    @classmethod
    def _get_image_url(cls, face) -> str:
        """
        Get the highest resolution image available from a card face
        :param face: The card or card face data.
        :return: A url to the image.
        """
        uris = ['large', 'border_crop', 'normal', 'small', 'art_crop']
        for uri in uris:
            if uri in face["image_uris"]:
                return face["image_uris"][uri]

    @classmethod
    def get_face_image(cls, card_face: dict) -> Image:
        url = cls._get_image_url(card_face)
        image_data = cls._request(url).content
        return Image.open(BytesIO(image_data))


class CardCache:
    @classmethod
    def from_expansions(cls, expansions: list[str]):
        card_cache = cls()
        for expansion in expansions:
            card_cache.populate_cache_by_expansion(expansion)
        return card_cache

    @classmethod
    def from_queries(cls, queries: list[str]):
        card_cache = cls()
        for query in queries:
            card_cache.populate_cache_by_query(query)
        return card_cache

    @classmethod
    def from_config(cls):
        card_cache = cls()

        # TODO: Load these from a config file
        expansions = list()
        queries = list()

        for expansion in expansions:
            card_cache.populate_cache_by_expansion(expansion)

        for query in queries:
            card_cache.populate_cache_by_query(query)
        return card_cache

    def __init__(self):
        self._card_cache = dict()

    def _add_to_cache(self, card, overwrite: bool = False) -> bool:
        """
        Adds new card data to the cache, skipping existing records.
        Can be set to overwrite data with the `overwrite` flag.
        :param card: The card data to add to the cache.
        :param overwrite: Whether to overwrite existing data.
        :return: Whether the value was updated.
        """
        name = card['name']
        if name in self._card_cache and not overwrite:
            return False

        logging.debug(f"Adding '{name}' to `CARD_CACHE`")
        self._card_cache[name] = card

        if "card_faces" in card:
            short_name = card['card_faces'][0]['name']
            logging.debug(f"Adding '{short_name}' to `CARD_CACHE`")
            self._card_cache[short_name] = card
        return True

    def populate_cache_by_query(self, query) -> None:
        """
        Populates the card cache with results from searching scryfall using a query.
        :param query: The query to use, following Scryfall's search syntax.
        """
        query = query.replace(' ', '+').replace('=', '%3D').replace(':', '%3A')
        cards = Scryfall.scryfall_search(query)
        for _, card in cards:
            self._add_to_cache(card)

    def populate_cache_by_expansion(self, expansion) -> None:
        """
        Popluates the card cache with results for a specific set.
        :param expansion: The set to get cards from.
        """
        cards = Scryfall.scryfall_search(f"e%3A{expansion}")
        for _, card in cards:
            self._add_to_cache(card)

    @cache
    def get_card_data(self, card_name) -> Optional[dict]:
        """
        Gets data for a card, by name. Uses Scryfall's fuzzy match, if a card can't be found in the cache.
        :param card_name: The name of the card.
        :return: The card data, if found.
        """
        if card_name in self._card_cache:
            return self._card_cache[card_name]

        card = Scryfall.scryfall_card(f"named?fuzzy={card_name}")
        self._add_to_cache(card)
        return card

    def get_card_data_by_set(self, card_name, expansion, number) -> Optional[dict]:
        """
        Gets data for a card, using its name, set and collector number.
        This allows for specifying a printing of a card.
        :param card_name: The card name.
        :param expansion: The set the card comes from.
        :param number: The card's collector number in the set.
        :return: The card data, if found.
        """
        card = self._card_cache.get(card_name, None)
        if card and card['set'].lower() == expansion.lower():
            return card

        card = Scryfall.scryfall_card(f"{expansion.lower()}/{number}")
        self._add_to_cache(card)
        return card


card_cache = CardCache()


def generate_slide_image(card_name: str) -> Image:
    print(card_name)
    card_data = card_cache.get_card_data(card_name)

    if "layout" in card_data and card_data["layout"] != "transform":
        return Scryfall.get_face_image(card_data)

    front_image = Scryfall.get_face_image(card_data["card_faces"][0])
    back_image = Scryfall.get_face_image(card_data["card_faces"][1])

    if "Battle" in card_data["card_faces"][0]["type_line"]:
        front_image = front_image.rotate(270, expand=True)  # Rotate image by -90 degrees

    merge_image_size = (front_image.size[0] + back_image.size[0], max(front_image.size[1], back_image.size[1]))
    merged_image = Image.new("RGBA", merge_image_size, (255, 255, 255, 255))

    front_image_location = (0, (merged_image.size[1] - front_image.size[1]) // 2)
    back_image_location = (front_image.size[0], (merged_image.size[1] - back_image.size[1]) // 2)
    merged_image.paste(front_image, front_image_location)
    merged_image.paste(back_image, back_image_location)
    return merged_image


def format_and_save_temp_image(img: Image, rotate: bool, out_loc: str) -> tuple[float, float]:
    new_height = cfg.HEIGHT
    new_width = cfg.WIDTH

    if rotate:
        img = img.rotate(270, expand=True)  # Rotate image by -90 degrees
        new_height, new_width = new_width, new_height  # Switch the height and width, since we've rotated.

    # Save the image fetched from the web as a JPEG, then use that file location to add the image into the docx.
    img.save(out_loc, format='JPEG')
    return new_height, new_width


def download_card_image(card_name: str) -> tuple[float, float]:
    card_data = card_cache.get_card_data(card_name)

    if "layout" in card_data and card_data["layout"] == "transform":
        front_face = card_data["card_faces"][0]
        rotate = front_face['type_line'] == 'Battle — Siege'
        front_image = Scryfall.get_face_image(front_face)
        height, width = format_and_save_temp_image(front_image, rotate, cfg.TEMP_FRONT_LOC)
        front = Image.open(cfg.TEMP_FRONT_LOC)

        back_image = Scryfall.get_face_image(card_data["card_faces"][1])
        h, w = format_and_save_temp_image(back_image, False, cfg.TEMP_BACK_LOC)
        height = max(height, h)
        width += w
        back = Image.open(cfg.TEMP_BACK_LOC)

        new = Image.new('RGBA', (front.size[0] + back.size[0], max(front.size[1], back.size[1])), (255, 255, 255, 255))
        new.paste(front, (0, (new.size[1] - front.size[1]) // 2))
        new.paste(back, (front.size[0], (new.size[1] - back.size[1]) // 2))
        new.save(cfg.TEMP_LOC, format='PNG')
    else:
        image = Scryfall.get_face_image(card_data)
        height, width = format_and_save_temp_image(image, False, cfg.TEMP_LOC)

    return height, width


def image_generator(card_names: Iterable[str]):
    for card_name in card_names:
        yield generate_slide_image(card_name)
