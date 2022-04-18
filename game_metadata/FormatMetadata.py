from typing import Union, Optional
from functools import cmp_to_key
from datetime import date, timedelta

from WUBRG.consts import COLOR_INDEXES

from game_metadata.utils.settings import SETS, FORMATS, SET_CONFIG
from game_metadata.CallScryfall import CallScryfall
from game_metadata.CardManager import CardManager
from game_metadata.Card import Card


class SetMetadata:
    """
    SetMetadata acts as a global repository for set data. Each set is defined by its three-letter code, and from
    there all information about the set can be gathered. As the information won't change, getting the information
    multiple time is unnecessary, so this acts as a central hub for that data. In particular, the costly operation of
    getting all cards in a set only needs to be done once, and then can be accessed from any place in the code.
    """
    METADATA: dict[str, Optional['SetMetadata']] = {s: None for s in SETS}

    @classmethod
    def get_metadata(cls, set_code: str) -> 'SetMetadata':
        """
        Returns an existing instance of a FormatMetadata object, or creates one if none exists.
        :param set_code: The three letter code for the set.
        :return: The SetMetadata for the set.
        """
        # TODO: Implement some checks so only valid sets are added.
        # TODO: Make the check update along with added sets.
        if set_code not in cls.METADATA or not cls.METADATA[set_code]:
            cls.METADATA[set_code] = cls(set_code)
        return cls.METADATA[set_code]

    def __init__(self, set_code):
        self.SET = set_code
        self.CARD_DICT = CardManager.from_set(set_code)
        self.FULL_NAME, self.ICON_URL = CallScryfall.get_set_info(set_code)
        self.RELEASE_DATE = SET_CONFIG[self.SET]["PremierDraft"][0][0]
        self.CARD_LIST = [self.CARD_DICT[name] for name in self.CARD_DICT]
        # Set up a dictionary for quicker sorting.
        self.CARD_INDEXES = {card.NAME: card.NUMBER for card in self.CARD_LIST}
        self.COMPARE_KEY = cmp_to_key(self._sort_compare)

    # Creating a custom sorting algorithm to order frames
    def _sort_compare(self, pair1: tuple[str, str], pair2: tuple[str, str]) -> int:
        # Convert the colors and names into numeric indexes
        # color1, name1 = pair1
        col_idx1 = COLOR_INDEXES[pair1[0]]
        name_idx1 = self.CARD_INDEXES[pair1[1]]
        # color2, name2 = pair2
        col_idx2 = COLOR_INDEXES[pair2[0]]
        name_idx2 = self.CARD_INDEXES[pair2[1]]

        # Sort by deck colour than card number.
        if col_idx1 == col_idx2:
            if name_idx1 < name_idx2:
                return -1
            else:
                return 1
        if col_idx1 < col_idx2:
            return -1
        else:
            return 1

    def find_card(self, card_name) -> Union[Card, None]:
        """
        Looks for a card name in the list of cards for the set.
        :param card_name: The card name, simple or full. Must be an exact match. If 'NONE', today's date is used.
        :return: A Card object or None
        """
        if card_name in CardManager.REDIRECT:
            card_name = CardManager.REDIRECT[card_name]
        if card_name in self.CARD_DICT:
            return self.CARD_DICT[card_name]
        else:
            return None

    @classmethod
    def __class_getitem__(cls, set_code):
        return cls.get_metadata(set_code)


class FormatMetadata:
    """
    FormatMetadata acts as a global repository for each format's data. Each format is defined by the three-letter set
    code, along with the string description of the format/game-type. FormatMetadata has access to all of the relevant
    SetMetadata, along with data specific to the format, such as dates.
    """
    METADATA: dict[str, dict[str, Optional['FormatMetadata']]] = {s: {f: None for f in FORMATS} for s in SETS}

    @staticmethod
    def get_metadata(set_code, format_name) -> 'FormatMetadata':
        """
        Returns an existing instance of a FormatMetadata object, or creates one if none exists.
        :param set_code: The three letter code for the set.
        :param format_name: The identifier for the format.
        :return: The FormatMetadata for the set and format.
        """
        # TODO: Implement some checks so only valid sets are added.
        # TODO: Make the check update along with added sets.
        if set_code not in FormatMetadata.METADATA or not FormatMetadata.METADATA[set_code]:
            FormatMetadata.METADATA[set_code] = dict()
        if format_name not in FormatMetadata.METADATA[set_code] or not FormatMetadata.METADATA[set_code][format_name]:
            FormatMetadata.METADATA[set_code][format_name] = FormatMetadata(set_code, format_name)
        return FormatMetadata.METADATA[set_code][format_name]

    def __init__(self, set_name, format_name):
        self.SET = set_name
        self.FORMAT = format_name

        self._active_periods = SET_CONFIG[set_name][format_name]
        self.START_DATE = self._active_periods[0][0]
        self.END_DATE = self._active_periods[-1][1]

        self._set_metadata = SetMetadata.get_metadata(set_name)
        self.CARD_DICT = self._set_metadata.CARD_DICT
        self.CARD_LIST = self._set_metadata.CARD_LIST

    def find_card(self, card_name) -> Card:
        """
        Looks for a card name in the list of cards for the set.
        :param card_name: The card name, simple or full. Must be an exact match. If 'NONE', today's date is used.
        :return: A Card object or None
        """
        return self._set_metadata.find_card(card_name)

    def is_active(self, check_date=None) -> bool:
        """
        Checks if the draft queue is active for a given date.
        :param check_date: The date to check. If 'NONE', today's date is used.
        :return: A boolean
        """
        if check_date is None:
            check_date = date.today()

        active = False
        for time_period in self._active_periods:
            active = active or (time_period[0] <= check_date <= time_period[1])

        return active

    def get_active_days(self) -> list[date]:
        """
        Gets the days where a draft queue was active.
        :return: A list of Date objects
        """
        active_days = list()

        for time_period in self._active_periods:
            start_date = time_period[0]
            active_days.append(start_date)
            new_date = start_date
            while new_date < time_period[1]:
                new_date += timedelta(days=1)
                active_days.append(new_date)
        return active_days
