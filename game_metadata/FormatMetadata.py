from typing import Union
from datetime import date, timedelta

from utils.settings import SETS, FORMATS, SET_CONFIG
from game_metadata.CardManager import CardManager
from game_metadata.Card import Card


class SetMetadata:
    _set: str
    _card_dict: dict[str, Card]
    METADATA = {s: dict() for s in SETS}

    @classmethod
    def get_metadata(cls, set_name) -> 'SetMetadata':
        # TODO: Implement some checks so only valid sets are added.
        # TODO: Make the check update along with added sets.
        if set_name not in cls.METADATA or not cls.METADATA[set_name]:
            cls.METADATA[set_name] = cls(set_name)
        return cls.METADATA[set_name]

    def __init__(self, set_name):
        self._set = set_name
        self._card_dict = CardManager.from_set(self.set)

    @property
    def set(self) -> str:
        """The draft set."""
        return self._set

    @property
    def release_date(self) -> date:
        """The (Arena) release date of the set's format."""
        return SET_CONFIG[self.set]["PremierDraft"][0][0]

    @property
    def card_dict(self) -> dict[str, Card]:
        """The dictionary of cards in the set"""
        return self._card_dict

    @property
    def card_list(self) -> list[Card]:
        """The list of cards in the set"""
        return [self._card_dict[name] for name in self._card_dict]

    def find_card(self, card_name) -> Union[Card, None]:
        """
        Looks for a card name in the list of cards for the set.
        :param card_name: The card name, simple or full. Must be an exact match. If 'NONE', today's date is used.
        :return: A Card object or None
        """
        if card_name in CardManager.REDIRECT:
            card_name = CardManager.REDIRECT[card_name]
        if card_name in self.card_dict:
            return self.card_dict[card_name]
        else:
            return None


class FormatMetadata:
    METADATA = {s: {f: dict() for f in FORMATS} for s in SETS}

    @staticmethod
    def get_metadata(set_name, format_name) -> 'FormatMetadata':
        # TODO: Implement some checks so only valid sets are added.
        # TODO: Make the check update along with added sets.
        if set_name not in FormatMetadata.METADATA or not FormatMetadata.METADATA[set_name]:
            FormatMetadata.METADATA[set_name] = dict()
        if format_name not in FormatMetadata.METADATA[set_name] or not FormatMetadata.METADATA[set_name][format_name]:
            FormatMetadata.METADATA[set_name][format_name] = FormatMetadata(set_name, format_name)
        return FormatMetadata.METADATA[set_name][format_name]

    def __init__(self, set_name, format_name):
        self._set = set_name
        self._format = format_name

        self._active_periods = SET_CONFIG[set_name][format_name]
        self._start_date = self._active_periods[0][0]
        self._end_date = self._active_periods[-1][1]

        self._set_metadata = SetMetadata.get_metadata(set_name)

    @property
    def set(self) -> str:
        """The draft set."""
        return self._set

    @property
    def format(self) -> str:
        """The format type."""
        return self._format

    @property
    def start_date(self) -> date:
        """The start date of the set's format."""
        return self._start_date

    @property
    def end_date(self) -> date:
        """The end date of the set's format."""
        return self._end_date

    @property
    def card_dict(self) -> dict[str, Card]:
        """The dictionary of cards in the set"""
        return self._set_metadata.card_dict

    @property
    def card_list(self) -> list[Card]:
        """The list of cards in the set"""
        return self._set_metadata.card_list

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
