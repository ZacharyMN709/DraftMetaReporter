from typing import Union

from utils.Logger import Logger
from utils.CallScryfall import CallScryfall

from game_metadata.Card import Card


class CardManager:
    REDIRECT = dict()
    SETS = dict()
    CARDS = dict()

    @classmethod
    def _add_card(cls, card: Card, searched_name: str) -> None:
        """
        An internal method to help more easily track cards as they're found/fetched.
        :param card: The card object to track
        :param searched_name: The name provided by the user to find
        """
        cls.CARDS[card.name] = card
        cls.REDIRECT[card.name] = card.name
        cls.REDIRECT[card.full_name] = card.name
        # Used to re-direct mis-spellings.
        cls.REDIRECT[searched_name] = card.name

    @classmethod
    def from_name(cls, name: str) -> Union[Card, None]:
        """
        Searches for a card by name. If not already known, will attempt to query Scryfall for
        the card.
        :param name: The name of the card to look for. Can handle inexact names, to an extent.
        :return: A Card or None
        """
        # If the card already exists, return it.
        prev_card = cls.find_card(name)
        if prev_card is not None:
            return prev_card
        # Otherwise, get the card info from scryfall.
        else:
            json = CallScryfall.get_card_by_name(name)
            # If there's an error, log it and return None.
            if 'err_msg' in json:
                Logger.LOGGER.log(f'Could not get card for {name}', Logger.FLG.DEFAULT)
                Logger.LOGGER.log(f'Error: {json["err_msg"]}', Logger.FLG.DEFAULT)
                return None
            # If the card is found, return it.
            else:
                card = Card(json)

                # See if a copy of the card already exists, likely
                # due to a misspelling. If so, use that instead.
                prev_card = cls.find_card(card.name)
                if prev_card is not None:
                    card = prev_card

                cls._add_card(card, name)
                return card

    @classmethod
    def from_set(cls, set_code: str) -> dict[str, Card]:
        """
        Gets a dictionary of card which exist a set.
        :param set_code: The three letter code of the set.
        :return: A dictionary of cards, with common names as keys.
        """

        # If the set code doesn't already exist,
        if set_code not in cls.SETS:
            # Create a new dictionary for it,
            cls.SETS[set_code] = dict()
            for json in CallScryfall.get_set_cards(set_code):
                # And fill it with cards fetched from Scryfall.
                card = Card(json)
                cls._add_card(card, card.name)
                cls.SETS[set_code][card.name] = card

        return cls.SETS[set_code]

    @classmethod
    def find_card(cls, card_name: str) -> Union[Card, None]:
        """
        Attempts to find a saved instance of a card.
        :param card_name: The card name to find
        :return: A Card or None
        """

        # If the card has been found before,
        if card_name in cls.REDIRECT:
            # Get the name it was found under, and return it.
            card_name = cls.REDIRECT[card_name]
            return cls.CARDS[card_name]
        else:
            return None
