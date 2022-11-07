from __future__ import annotations
from typing import Optional, Union, Callable
from functools import cmp_to_key
from datetime import date, time, datetime, timedelta

from utilities.auto_logging import logging
from wubrg import index_dist_wubrg, COLOR_IDENTITY

from game_metadata.utils.settings import SET_CONFIG
from data_interface.RequestScryfall import RequestScryfall
from game_metadata.game_objects.Card import Card, CardManager


class SetMetadata:
    """
    SetMetadata acts as a global repository for set data. Each set is defined by its three-letter code, and from
    there all information about the set can be gathered. As the information won't change, getting the information
    multiple time is unnecessary, so this acts as a central hub for that data. In particular, the costly operation of
    getting all cards in a set only needs to be done once, and then can be accessed from any place in the code.
    """
    METADATA: dict[str, Optional[SetMetadata]] = dict()
    __cls_lock = object()

    @classmethod
    def get_metadata(cls, set_code: str) -> Optional[SetMetadata]:
        """
        Returns an existing instance of a FormatMetadata object, or creates one if none exists.
        :param set_code: The three-letter code for the set.
        :return: The SetMetadata for the set.
        """
        # TODO: Make the check update along with added sets.
        if set_code not in cls.METADATA:
            cls.METADATA[set_code] = cls(cls.__cls_lock, set_code)
        return cls.METADATA[set_code]

    def __init__(self, cls_lock, set_code):
        if cls_lock != self.__cls_lock:
            raise Exception("Must use 'SetMetadata.get_metadata' class method.")

        self.SET: str = set_code
        logging.info(f"Loading set metadata for: {set_code}")
        _full_name, _icon_url = RequestScryfall.get_set_info(set_code)
        self.FULL_NAME: str = _full_name
        self.ICON_URL: str = _icon_url
        self.RELEASE_DATE: date = SET_CONFIG[self.SET]["PremierDraft"][0][0]
        # Set up dictionaries for quicker sorting.
        self.CARD_PRINT_ORDER_INDEXES: dict[str, int] = \
            {k.NAME: v for v, k in enumerate(self.CARD_LIST)}
        self.CARD_REVIEW_ORDER_INDEXES: dict[str, int] = \
            {k: v for v, k in enumerate(RequestScryfall.get_set_review_order(self.SET))}
        self.CARD_PRINT_ORDER_KEY: Callable = cmp_to_key(self._print_order_compare)
        self.CARD_REVIEW_ORDER_KEY: Callable = cmp_to_key(self._review_order_compare)
        self.FRAME_ORDER_KEY: Callable = cmp_to_key(self._frame_order_compare)
        logging.info(f"Done!\n")

    @property
    def CARD_DICT(self) -> dict[str, Card]:
        return CardManager.from_set(self.SET)

    @property
    def CARD_LIST(self) -> list[Card]:
        return [self.CARD_DICT[name] for name in self.CARD_DICT]

    def _print_order_compare(self, card_name1: str, card_name2: str):
        # Convert the names into numeric indexes
        name_idx1 = self.CARD_PRINT_ORDER_INDEXES[card_name1]
        name_idx2 = self.CARD_PRINT_ORDER_INDEXES[card_name2]
        return name_idx1 - name_idx2

    def _review_order_compare(self, card_name1: str, card_name2: str):
        # Convert the names into numeric indexes
        name_idx1 = self.CARD_REVIEW_ORDER_INDEXES[card_name1]
        name_idx2 = self.CARD_REVIEW_ORDER_INDEXES[card_name2]
        return name_idx1 - name_idx2

        # Creating a custom sorting algorithm to order frames

    def _frame_order_compare(self, pair1: tuple[COLOR_IDENTITY, str], pair2: tuple[COLOR_IDENTITY, str]) -> int:
        # Compares the colour strings.
        color_compare_result = index_dist_wubrg(pair1[0], pair2[0])

        # If the colours are the same, use the card to sort instead.
        if color_compare_result == 0:
            # Convert the names into numeric indexes
            return self._print_order_compare(pair1[1], pair2[1])
        else:
            return color_compare_result

    def find_card(self, card_name) -> Optional[Card]:
        """
        Looks for a card name in the list of cards for the set.
        :param card_name: The card name, simple or full. Must be an exact match.
        :return: A Card object or None
        """
        if card_name in CardManager.REDIRECT:
            old_name = card_name
            card_name = CardManager.REDIRECT[card_name]
            logging.verbose(f"Changing '{old_name}' to '{card_name}'")

        if card_name in self.CARD_DICT:
            return self.CARD_DICT[card_name]
        else:
            logging.warning(f"Could not find {card_name} in CARD_DICT")
            return None

    def get_cards_by_colors(self, colors: list[str]) -> list[Card]:
        """
        Get cards which have colour identities which are contained in the provided list
        :param colors: A list of colours.
        :return: A list of cards which are one of the colours.
        """
        ret = list()
        for card in self.CARD_LIST:
            for color in colors:
                if card.COLOR_IDENTITY == color:
                    ret.append(card)
                    break

        return ret

    @classmethod
    def __class_getitem__(cls, set_code):
        return cls.METADATA[set_code]


class FormatMetadata:
    """
    FormatMetadata acts as a global repository for each format's data. Each format is defined by the three-letter set
    code, along with the string description of the format/game-type. FormatMetadata has access to all of the relevant
    SetMetadata, along with data specific to the format, such as dates.
    """
    METADATA: dict[str, dict[str, Optional[FormatMetadata]]] = dict()
    __cls_lock = object()

    @staticmethod
    def get_metadata(set_code: str, format_name: str) -> Optional[FormatMetadata]:
        """
        Returns an existing instance of a FormatMetadata object, or creates one if none exists.
        :param set_code: The three-letter code for the set.
        :param format_name: The identifier for the format.
        :return: The FormatMetadata for the set and format.
        """
        # TODO: Make the check update along with added sets.
        if set_code not in FormatMetadata.METADATA:
            FormatMetadata.METADATA[set_code] = dict()
        if format_name not in FormatMetadata.METADATA[set_code]:
            inst = FormatMetadata(FormatMetadata.__cls_lock, set_code, format_name)
            FormatMetadata.METADATA[set_code][format_name] = inst
        return FormatMetadata.METADATA[set_code][format_name]

    def __init__(self, cls_lock, set_name: str, format_name: str):
        if cls_lock != self.__cls_lock:
            raise Exception("Must use 'FormatMetadata.get_metadata' class method.")

        self.SET: str = set_name
        self.FORMAT: str = format_name

        self._active_periods: list[tuple[date, date]] = SET_CONFIG[set_name][format_name]
        self.START_DATE: date = self._active_periods[0][0]
        self.END_DATE: date = self._active_periods[-1][1]

        self._set_metadata: SetMetadata = SetMetadata.get_metadata(set_name)

    @property
    def CARD_DICT(self) -> dict[str, Card]:
        return self._set_metadata.CARD_DICT

    @property
    def CARD_LIST(self) -> list[Card]:
        return self._set_metadata.CARD_LIST

    def find_card(self, card_name: str) -> Optional[Card]:
        """
        Looks for a card name in the list of cards for the set.
        :param card_name: The card name, simple or full. Must be an exact match.
        :return: A Card object or None
        """
        return self._set_metadata.find_card(card_name)

    @property
    def has_started(self) -> bool:
        return datetime.utcnow() > datetime.combine(self.START_DATE, time(15, 0))

    @property
    def has_data(self) -> bool:
        return datetime.utcnow() > datetime.combine(self.START_DATE + timedelta(days=1), time(2, 0))

    def is_active(self, check_date: Union[date, datetime] = None) -> bool:
        """
        Checks if the draft queue is active for a given date.
        :param check_date: The date to check. If 'NONE', today's date is used.
        :return: A boolean
        """
        if check_date is None:
            check_date = date.today()

        if isinstance(check_date, datetime):
            check_date = check_date.date()

        active = False
        for time_period in self._active_periods:
            active = active or (time_period[0] <= check_date <= time_period[1])

        return active

    def get_active_days(self) -> list[date]:
        """
        Gets the days when a draft queue was active.
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
