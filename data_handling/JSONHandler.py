from typing import Optional
import os
from datetime import date, datetime
import json

from utils import settings, WUBRG
from utils.Logger import Logger
from utils.Fetcher import Fetcher


class JSONHandler:
    """
    Used to get data for a specific set, format and date. Automatically handles how to retrieve
    data based on whether it exists locally or not.
    """

    _DEFAULT_DATE = '2020-01-01'
    _BASE_URL = 'https://www.17lands.com/'

    def __init__(self, set_name: str, format_name: str, target_date: date = None):
        self.SET: str = set_name
        self.FORMAT: str = format_name
        self.DATE: Optional[date] = target_date
        os.makedirs(self.get_folder_path(), exist_ok=True)
        self._fetcher: Fetcher = Fetcher()

    def _get_date_filter(self) -> str:
        """Generates a piece of the url to isolate data to a certain date range."""
        if self.DATE:
            return f'&start_date={self.DATE}&end_date={self.DATE}'
        else:
            return f'&start_date={self._DEFAULT_DATE}&end_date={date.today()}'

    def get_card_rating_url(self, colors: str) -> str:
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
        path = os.path.join(settings.DATA_DIR_LOC, settings.DATA_DIR_NAME, self.SET, self.FORMAT)
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

    def get_last_write_time(self) -> datetime:
        """
        Returns a UTC datetime object for the last write time of the managed files.
        :return: A datetime object.
        """
        try:
            filepath = os.path.abspath(self.get_file_path('ColorRatings.json'))
            wrt_tm = datetime.utcfromtimestamp(os.path.getmtime(filepath))
        except Exception:
            wrt_tm = datetime(2020, 1, 1)
        Logger.LOGGER.log(f'Last write-time: {wrt_tm}', Logger.FLG.DEBUG)
        return wrt_tm

    def files_valid(self) -> bool:
        """
        Returns a boolean which represents if the files contain valid data.
        Returns False if all of the files contain empty or default data.
        :return: A boolean.
        """
        folder_path = self.get_folder_path()
        files = os.listdir(folder_path)
        for x in files:
            # Min file size is 129.
            if os.path.getsize(os.path.join(folder_path, x)) > 130:
                Logger.LOGGER.log(f'Non-empty file found: {x}', Logger.FLG.DEBUG)
                return True

        Logger.LOGGER.log(f'All files are empty!', Logger.FLG.DEBUG)
        return False

    def load_json_file(self, filename: str) -> dict[str, object]:
        """
        Loads and returns the data from a json file.
        :param filename: The name of the json file (including filetype).
        :return: An object contain the json data.
        """
        filepath = os.path.abspath(self.get_file_path(filename))

        try:
            with open(filepath, 'r') as f:
                json_str = f.read()
                f.close()
                Logger.LOGGER.log(f'File {filename} read successfully.', Logger.FLG.VERBOSE)
                return json.loads(json_str)
        except Exception as ex:
            Logger.LOGGER.log(f'Error reading json file {filename}', Logger.FLG.ERROR)
            Logger.LOGGER.log(ex, Logger.FLG.ERROR)
            return dict()

    def save_json_file(self, filename: str, data: dict[str, object]) -> bool:
        """
        Saves provided data into the specified json file.
        :param filename: The name of the json file (including filetype).
        :param data: The object to be saved as json.
        :return: Whether the save operation was successful.
        """
        filepath = os.path.abspath(self.get_file_path(filename))

        try:
            with open(filepath, 'w') as f:
                f.write(json.dumps(data, indent=4))
                f.close()
            Logger.LOGGER.log(f'File {filename} written to.', Logger.FLG.VERBOSE)
            return True
        except Exception as ex:
            Logger.LOGGER.log(f'Error writing to json file {filename}', Logger.FLG.ERROR)
            Logger.LOGGER.log(ex, Logger.FLG.ERROR)
            return False

    def _get_data(self, url: str, filename: str, overwrite: bool = False) -> dict[str, object]:
        """
        Automatically gets the appropriate data. If it saved locally, it will query 17Lands for the data
        and then save it to a file. Otherwise it will load it from the file.
        :param url: The url to get the data from
        :param filename: The file to load/save data from/to
        :param overwrite: Forcibly overwrite the data in the file
        :return: A dictionary of the data.
        """
        if (not self.file_exists(filename)) or overwrite:
            if overwrite:
                Logger.LOGGER.log(f"Updating data for '{filename}'. Fetching from 17Lands site...", Logger.FLG.DEFAULT)
            else:
                Logger.LOGGER.log(f"Data for '{filename}' not found in saved data. Fetching from 17Lands site...",
                                  Logger.FLG.DEFAULT)
            data = self._fetcher.fetch(url)
            self.save_json_file(filename, data)
        else:
            data = self.load_json_file(filename)
        return data

    def get_card_data(self, color: str, overwrite: bool = False) -> dict[str, object]:
        """
        Get the data on individual card performance
        :param color: The colours to filter card performance on
        :param overwrite: Forcibly overwrite the data in the file
        :return: A dictionary with card names as keys.
        """
        return self._get_data(self.get_card_rating_url(color), f'{color}CardRatings.json', overwrite)

    def get_all_card_data(self, overwrite: bool = False) -> dict[str, dict[str, object]]:
        """
        Gets data on card performance for all colour combinations.
        :param overwrite: Forcibly overwrite the data in the file
        :return: A dictionary of dictionaries, with deck colours as keys
        """
        card_dict = dict()
        for color in WUBRG.COLOR_GROUPS:
            card_dict[color] = self.get_card_data(color, overwrite)

        return card_dict

    def get_meta_data(self, overwrite: bool = False) -> dict[str, object]:
        """
        Gets data on archetype performance.
        :param overwrite: Forcibly overwrite the data in the file
        :return: A dictionary, with archetype names as keys
        """
        return self._get_data(self.get_color_rating_url(), f'ColorRatings.json', overwrite)

    def get_day_data(self, overwrite: bool = False) -> tuple[dict[str, dict[str, object]], dict[str, object]]:
        """
        Gets all data available for the day.
        :param overwrite: Forcibly overwrite the data in the file
        :return: A tuple of dictionaries containing data from 17Lands
        """
        if not self.files_valid():
            overwrite = True

        card_dict = self.get_all_card_data(overwrite)
        meta_dict = self.get_meta_data(overwrite)

        return card_dict, meta_dict
