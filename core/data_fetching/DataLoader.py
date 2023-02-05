from __future__ import annotations
from typing import Optional, Union
from core.data_fetching.utils import CARD_DATA, META_DATA, WUBRG_CARD_DATA
import os
from datetime import date, datetime, time

from core.wubrg import COLOR_COMBINATIONS
from core.utilities.auto_logging import logging
from core.utilities import save_json_file, load_json_file

from core.data_requesting.Requester import Requester
from core.game_metadata import CardManager
from core.data_fetching.utils.settings import DATA_DIR_LOC, DATA_DIR_NAME


class DataLoader:
    """
    Used to get data for a specific set, format and date. Automatically handles how to retrieve
    data based on whether it exists locally or not.
    """

    # TODO: This could be made more space efficient by converting fetched data into a csv format before saving.
    # TODO: Add a check to handle instances of getting back "dummy" data (where all values are 0)
    _DEFAULT_DATE: date = date(2020, 1, 1)
    _BASE_URL: str = 'https://www.17lands.com/'
    _MIN_FILE_SIZE: int = 265

    def __init__(self, set_name: str, format_name: str, target_date: date = None):
        self.SET: str = set_name
        self.FORMAT: str = format_name
        self.DATE: Optional[date] = target_date
        os.makedirs(self.get_folder_path(), exist_ok=True)
        self._fetcher: Requester = Requester()

    def _get_date_filter(self) -> str:
        """Generates a piece of the url to isolate data to a certain date range."""
        if self.DATE:
            return f'&start_date={self.DATE}&end_date={self.DATE}'
        else:
            return f'&start_date={self._DEFAULT_DATE}&end_date={date.today()}'

    def get_card_rating_url(self, colors: str = '') -> str:
        """Generates a piece of the url for card data."""
        url = self._BASE_URL + f'card_ratings/data?expansion={self.SET}&format={self.FORMAT}'
        if colors:
            url += f'&colors={colors}'
        url += self._get_date_filter()
        return url

    def get_color_rating_url(self) -> str:
        """Generates a piece of the url for archetype performances."""
        url = self._BASE_URL + f'color_ratings/data?expansion={self.SET}' \
                               f'&event_type={self.FORMAT}&combine_splash=false'
        url += self._get_date_filter()
        return url

    def get_folder_path(self) -> str:
        """Returns the appropriate folder path, based on the properties of the object."""
        path = os.path.join(DATA_DIR_LOC, DATA_DIR_NAME, self.SET, self.FORMAT)
        if self.DATE:
            return os.path.join(path, str(self.DATE))
        else:
            return os.path.join(path, 'ALL')

    def get_file_path(self, filename: str) -> str:
        """Returns the full file path for a given file name, based on `get_folder_path`"""
        return os.path.join(self.get_folder_path(), filename)

    def file_exists(self, filename: str) -> bool:
        """Checks if a file exists in the appropriate directory for the object."""
        return os.path.isfile(self.get_file_path(filename))

    def get_last_summary_update_time(self) -> datetime:
        """
        Returns a UTC datetime object for the last write time of the managed files.
        :return: A datetime object.
        """
        wrt_tm = datetime.utcnow()
        try:
            files = os.listdir(self.get_folder_path())
            for file in files:
                sum_path = os.path.abspath(self.get_file_path(file))
                wrt_tm = min(datetime.utcfromtimestamp(os.path.getmtime(sum_path)), wrt_tm)
        except FileNotFoundError:  # pragma: no cover
            wrt_tm = datetime.combine(self._DEFAULT_DATE, time(0, 0))
        logging.debug(f'Last write-time: {wrt_tm}')
        return wrt_tm

    def _file_valid(self, filename: str) -> bool:
        """
        Checks if a file contains actual data related to the game, or if it was created with no data.
        :param filename: The name of the file to check.
        :return: True if the file is not an empty list. False, if no real data exists.
        """
        file_path = self.get_file_path(filename)
        valid = os.path.getsize(file_path) > self._MIN_FILE_SIZE
        if not valid:  # pragma: no cover
            logging.debug(f'{filename} contained no data!')
        return valid

    def _get_data(self, url: str, filename: str, overwrite: bool = False) -> \
            Union[CARD_DATA, META_DATA]:  # pragma: no cover
        """
        Automatically gets the appropriate data. If it saved locally, it will query 17Lands for the data
        and then save it to a file. Otherwise, it will load it from the file.
        :param url: The url to get the data from
        :param filename: The file to load/save data from/to
        :param overwrite: Forcibly overwrite the data in the file
        :return: A dictionary of the data.
        """
        fetch = overwrite or (not self.file_exists(filename)) or (not self._file_valid(filename))
        if fetch:
            if overwrite:
                logging.verbose(f"Updating data for '{filename}'. Fetching from 17Lands site...")
            else:
                logging.verbose(f"Data for '{filename}' not found in saved data. Fetching from 17Lands site...")
            raw_data = self._fetcher.request(url)

            if raw_data is None:
                logging.error(f"Data fetched for '{filename}' returned None! Returning empty CARD_DATA struct")
                return CARD_DATA

            # Handles correcting data from 17Lands, since data coming back from MTGA can't be trusted.
            for data in raw_data:
                if 'name' in data:
                    name = data['name']
                    card_obj = CardManager.from_name(name)
                    data['name'] = card_obj.NAME

            save_json_file(self.get_folder_path(), filename, raw_data)
        else:
            raw_data = load_json_file(self.get_folder_path(), filename)
        return raw_data

    def get_card_data(self, color: str = '', overwrite: bool = False) -> CARD_DATA:
        """
        Get the data on individual card performance.
        :param color: The colours to filter card performance on
        :param overwrite: Forcibly overwrite the data in the file
        :return: A list of dictionaries with card value mapping to their data.
        """
        return self._get_data(self.get_card_rating_url(color), f'{color}CardRatings.json', overwrite)

    def get_meta_data(self, overwrite: bool = False) -> META_DATA:
        """
        Gets data on archetype performance.
        :param overwrite: Forcibly overwrite the data in the file
        :return: A dictionary, with archetype names as keys
        """
        return self._get_data(self.get_color_rating_url(), f'ColorRatings.json', overwrite)

    def get_all_card_data(self, overwrite: bool = False) -> WUBRG_CARD_DATA:  # pragma: no cover
        """
        Gets data on card performance for all colour combinations.
        :param overwrite: Forcibly overwrite the data in the file
        :return: A dictionary of dictionaries, with deck colours as keys
        """
        all_card_data = dict()
        for color in COLOR_COMBINATIONS:
            all_card_data[color] = self.get_card_data(color, overwrite)

        return all_card_data

    def get_day_data(self, overwrite: bool = False) -> tuple[WUBRG_CARD_DATA, META_DATA]:  # pragma: no cover
        """
        Gets all data available for the day.
        :param overwrite: Forcibly overwrite the data in the file
        :return: A tuple of dictionaries containing data from 17Lands
        """
        card_data = self.get_all_card_data(overwrite)
        meta_data = self.get_meta_data(overwrite)

        return card_data, meta_data
