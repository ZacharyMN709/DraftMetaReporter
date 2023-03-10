"""
A small class which helps get specific data from scryfall, handling the minutia of json checking.
"""

from typing import Optional
from datetime import date
import json
import pandas as pd

from core.data_requesting.utils import *
from core.data_requesting.Requester import Requester


# Adapted from 'https://github.com/diogojapinto/mtg-data-mining/blob/main/utils/api_clients/seventeen_lands/client.py'
class Request17Lands(Requester):
    """ A small class which helps get specific data from scryfall, handling the minutia of json checking. """
    def __init__(self, tries: int = None, fail_delay: float = None, success_delay: float = None):
        super().__init__(tries, fail_delay, success_delay, [200])

    def get_colors(self) -> Optional[list[str]]:
        """
        Gets the list of colours 17 Lands supports.
        :return: A list of colours
        """
        return self.get_json_response(url=COLOR_17L_URL)

    def get_expansions(self) -> Optional[list[str]]:
        """
        Gets the list of expansions (sets) 17 Lands supports.
        :return: A list expansion codes.
        """
        return self.get_json_response(url=EXPANSIONS_17L_URL)

    def get_event_types(self) -> Optional[list[str]]:
        """
        Gets the list of event types (game modes: eg. 'Premier Draft') 17 Lands supports.
        :return: A list event types.
        """
        return self.get_json_response(url=FORMATS_17L_URL)

    def get_play_draw_stats(self) -> Optional[list[dict]]:
        """
        Returns the play-draw stats for the formats 17 Lands has available, from PLAY_DRAW_17L_URL.
        :return: The play-draw data.
        """
        return self.get_json_response(url=PLAY_DRAW_17L_URL)

    def get_color_ratings(self, expansion: str, event_type: str = None,
                          start_date: date = None, end_date: date = None,
                          user_group: str = None, combine_splash: bool = False) -> Optional[list[dict]]:
        """
        Gets data on win-rates for different colour combinations of decks.
        :param expansion: The set code to get data for.
        :param event_type: The event type to get the data for. ('PremierDraft', etc.) Default: DEFAULT_FORMAT
        :param start_date: The start date for the data range. Default: DEFAULT_DATE
        :param end_date: The end date for the data range. Default: date.today()
        :param user_group: The tier of player to filter on ('top', 'middle', 'bottom'). Default: None
        :param combine_splash: Whether to combine decks that splash with those that don't. Default: False
        :return: A list of dictionaries containing archetype information.
        """
        # Handle parameters, and package them into a dict to be used for the url.
        event_type = event_type or DEFAULT_FORMAT
        start_date = start_date or DEFAULT_DATE
        end_date = end_date or date.today()
        params = {
            'expansion': expansion,
            'event_type': event_type,
            'start_date': start_date.strftime('%Y-%m-%d'),
            'end_date': end_date.strftime('%Y-%m-%d'),
            'combine_splash': combine_splash,
            'user_group': user_group
        }

        result = self.get_json_response(url=COLOR_RATING_17L_URL, params=params)

        # If the result is the default list, no data was found, so return None instead.
        if len(result) == 1:
            return None

        return result

    def get_card_ratings(self, expansion: str, event_type: str = None,
                         start_date: date = None, end_date: date = None,
                         user_group: str = None, deck_colors: str = None) -> Optional[list[dict]]:
        """
        Gets data on the performance of cards in a draft.
        :param expansion: The set code to get data for.
        :param event_type: The event type to get the data for. ('PremierDraft', etc.) Default: DEFAULT_FORMAT
        :param start_date: The start date for the data range. Default: DEFAULT_DATE
        :param end_date: The end date for the data range. Default: date.today()
        :param user_group: The tier of player to filter on ('top', 'middle', 'bottom'). Default: None
        :param deck_colors: The colour of deck to filter on. Default: None
        :return: A list of dictionaries containing card information.
        """
        # Handle parameters, and package them into a dict to be used for the url.
        event_type = event_type or DEFAULT_FORMAT
        start_date = start_date or DEFAULT_DATE
        end_date = end_date or date.today()
        params = {
            'expansion': expansion,
            'format': event_type,
            'start_date': start_date.strftime('%Y-%m-%d'),
            'end_date': end_date.strftime('%Y-%m-%d'),
            'user_group': user_group,
            'colors': deck_colors
        }

        result = self.get_json_response(url=CARD_RATING_17L_URL, params=params)

        # If the result is an empty list, no trophy decks were found, so return None instead.
        if len(result) == 0:
            return None

        return result

    def get_card_evaluations(self, expansion: str, event_type: str = None,
                             start_date: date = None, end_date: date = None,
                             rarity: str = None, color: str = None) -> Optional[dict]:
        """
        Gets data on how highly cards are being taken during a draft, and its changes over time.
        The returned data seems to be duplicated 21 times?
        :param expansion: The set code to get data for.
        :param event_type: The event type to get the data for. ('PremierDraft', etc.) Default: DEFAULT_FORMAT
        :param start_date: The start date for the data range. Default: DEFAULT_DATE
        :param end_date: The end date for the data range. Default: date.today()
        :param rarity: The rarity of the card to filter on. Default: None
        :param color: The color of the card to filter on. Default: None
        :return: Returns a dict with 4 lists, which need to be joined into tabular data.
        """

        # TODO: The data returned from this is weirdly duplicated. Check on that with 17Lands.
        # NOTE: This request doesn't handle large time spans well. Use with caution.
        # Handle parameters, and package them into a dict to be used for the url.
        event_type = event_type or DEFAULT_FORMAT
        start_date = start_date or DEFAULT_DATE
        end_date = end_date or date.today()
        params = {
            'expansion': expansion,
            'format': event_type,
            'start_date': start_date.strftime('%Y-%m-%d'),
            'end_date': end_date.strftime('%Y-%m-%d'),
            'rarity': rarity,
            'color': color
        }

        return self.get_json_response(url=CARD_EVAL_17L_URL, params=params)

    def get_trophy_deck_metadata(self, expansion: str, event_type: Optional[str] = None) -> Optional[list[dict]]:
        """
        Gets cursory information on (up to) the 500 most recent trophy decks, from TROPHY_17L_URL.
        :param expansion: The set/expansion to get data on.
        :param event_type: The event type to get data on. Default: DEFAULT_FORMAT
        :return: A list of metadata of the trophy decks.
        """
        # Handle parameters, and package them into a dict to be used for the url.
        event_type = event_type or DEFAULT_FORMAT
        params = {
            'expansion': expansion,
            'format': event_type
        }

        # Request the information.
        result = self.get_json_response(url=TROPHY_17L_URL, params=params)

        # If the result is an empty list, no trophy decks were found, so return None instead.
        if len(result) == 0:
            return None

        return result

    def get_deck(self, draft_id: str, deck_index: int = 0) -> Optional[dict]:
        """
        Gets details of a particular deck from DECK_17L_URL, based on the draft id and deck index provided.
        :param draft_id: The id of the draft.
        :param deck_index: The index of the deck to look for. Default: 0
        :return: The details of the specified deck, if found.
        """
        # Handle parameters, and package them into a dict to be used for the url.
        params = {
            'draft_id': draft_id,
            'deck_index': deck_index
        }

        # Request the information, and return the result.
        return self.get_json_response(url=DECK_17L_URL, params=params)

    def get_details(self, draft_id: str) -> Optional[dict]:
        """
        Gets details of a run from DETAILS_17L_URL, based on the draft id provided.
        :param draft_id: The id of the draft.
        :return: A dictionary with the run's details, if found.
        """
        params = {
            'draft_id': draft_id,
        }

        return self.get_json_response(url=DETAILS_17L_URL, params=params)

    def get_draft(self, draft_id: str) -> Optional[dict]:
        """
        Gets a draft log from DRAFT_LOG_17L_URL, based on the draft id provided.
        :param draft_id: The id of the draft.
        :return: A dictionary with the draft data, if found.
        """
        params = {
            'draft_id': draft_id
        }

        # Make a request and abort if None is returned.
        result = self.get_response(url=DRAFT_LOG_17L_URL, params=params)
        if result is None:
            return None

        # Process built-in JSON, and return it.
        result = json.loads(result.text[6:-2])
        return result['payload']

    def get_tier_list(self, tier_list_id: str) -> Optional[list[dict]]:
        """
        Requests information on a tier list from TIER_17L_URL, based on a tier list id.
        :param tier_list_id: The id for the tier list.
        :return: A list of card tier information. A an invalid id returns None.
        """
        # Make a request to the appropriate url and get the result.
        url = TIER_17L_URL + f"/{tier_list_id}"
        result = self.get_json_response(url=url)

        # If the result is an empty list, no valid tier list was found, so return None instead.
        if len(result) == 0:
            return None

        return result
