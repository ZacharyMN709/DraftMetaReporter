from typing import Optional

from Utilities.auto_logging import logging
from Utilities.SiteRequests.RequestScryfall import RequestScryfall

from game_metadata.Card import Card


class CardManager:
    """
    CardManager acts as a global repository for card data. This is both for pulled data from Scryfall, and the results
    and queries of users. In particular, it tracks user's requests (which can be mis-spelled), and logs them as aliases
    for a found card. This means that as more users request cards, fewer calls have to be made to Scryfall.

    It's possible this should be reset at the release of a new set to let the object "re-link" names as their mappings
    may end up changing with the release of new cards, or after a certain amount of time to free up memory.
    """

    # Used to map misspellings back to the correct name, without having to re-query scryfall.
    REDIRECT: dict[str, str] = dict()

    # Used to maintain a constant-time lookup cache of previously requested cards.
    SETS: dict[str, dict[str, Card]] = dict()
    CARDS: dict[str, Card] = dict()

    @classmethod
    def _add_card(cls, card: Card, searched_name: str = '', force_update=True) -> None:
        """
        An internal method to help more easily track cards as they're found/fetched.
        :param card: The card object to track
        :param searched_name: The name provided by the user to find
        """

        # If the card objects isn't tracked in CARDS, add it.
        # This also means if cards from sets are pulled newest to oldest, the most recent version
        # of the card will be the one that is cached.
        if card.NAME not in cls.CARDS or force_update:
            cls.CARDS[card.NAME] = card
            cls.REDIRECT[card.NAME] = card.NAME
            cls.REDIRECT[card.FULL_NAME] = card.NAME

        # Used to re-direct mis-spellings.
        if searched_name != '':
            cls.REDIRECT[searched_name] = card.NAME

    @classmethod
    def from_name(cls, name: str) -> Optional[Card]:
        """
        Searches for a card by name. If not already known, will attempt to query Scryfall for
        the card.
        :param name: The name of the card to look for. Can handle inexact names, to an extent.
        :return: A Card or None
        """
        # If the card already exists, return it.
        prev_card, found = cls._find_card(name)
        if found:
            return prev_card
        # Otherwise, get the card info from scryfall.
        else:
            json = RequestScryfall.get_card_by_name(name)
            # If there's an error, log it, mark the alias as '' and return None.
            if 'err_msg' in json:
                logging.info(f'Could not get card for {name}')
                logging.info(f'Error: {json["err_msg"]}')
                cls.REDIRECT[name] = ''
                return None
            # If the card is found, return it.
            else:
                card = Card(json)

                # See if a copy of the card already exists, likely
                # due to a misspelling. If so, use that instead.
                prev_card, found = cls._find_card(card.NAME)
                if prev_card is not None:
                    card = prev_card

                cls._add_card(card, name)
                return card

    @classmethod
    def from_set(cls, set_code: str) -> dict[str, Card]:
        """
        Gets a dictionary of card which exist a set.
        :param set_code: The three-letter code of the set.
        :return: A dictionary of cards, with common names as keys.
        """

        # If the set code doesn't already exist,
        if set_code not in cls.SETS:
            # Create a new dictionary for it,
            cls.SETS[set_code] = dict()
            for json in RequestScryfall.get_set_cards(set_code):
                # And fill it with cards fetched from Scryfall.
                card = Card(json)
                cls._add_card(card)
                cls.SETS[set_code][card.NAME] = card

            for card_name in ['Plains', 'Island', 'Swamp', 'Mountain', 'Forest']:
                if card_name in cls.SETS[set_code]:
                    del cls.SETS[set_code][card_name]

        return cls.SETS[set_code]

    @classmethod
    def _find_card(cls, card_name: str) -> tuple[Optional[Card], bool]:
        """
        Attempts to find a saved instance of a card.
        :param card_name: The card name to find
        :return: A Card or None, and whether the name exists in REDIRECT
        """

        # If the card has been found before,
        if card_name in cls.REDIRECT:
            # Get the name it was found under, and return it.
            card_name = cls.REDIRECT[card_name]
            if card_name == '':
                return None, True
            else:
                return cls.CARDS[card_name], True
        else:
            return None, False

    @classmethod
    def reset_redirects(cls) -> None:
        """
        Resets the REDIRECT dictionary, clearing any aliases, but preserving the true card names.
        """
        cls.REDIRECT = dict()
        for card_name in cls.CARDS:
            card = cls.CARDS[card_name]
            cls._add_card(card, force_update=True)

    @classmethod
    def flush_cache(cls) -> None:
        """
        Clears the caches of cards.
        """
        del cls.REDIRECT
        del cls.SETS
        del cls.CARDS

        cls.REDIRECT = dict()
        cls.SETS = dict()
        cls.CARDS = dict()
