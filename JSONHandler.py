import os
from datetime import date, datetime
import json

import settings
import WUBRG
import consts
from Logger import Logger
from Fetcher import Fetcher


class JSONHandler:
    _TRIES = 5
    _FAIL_DELAY = 60
    _SUCC_DELAY = 1
    #TODO: Create and move to a config file.
    
    _DEFAULT_DATE = '2020-01-01'
    _BASE_URL = 'https://www.17lands.com/'
        
    def __init__(self, SET: str, FORMAT: str, DATE: date=None, LOGGER=None):
        self.SET = SET
        self.FORMAT = FORMAT
        self.DATE = DATE
        if LOGGER is None:
            LOGGER = Logger()
        self.LOGGER = LOGGER
        os.makedirs(self.get_folder_path(), exist_ok=True)
        self.FETCHER = Fetcher(self.LOGGER)
        
    def get_date_filter(self) -> str:
        if self.DATE:
            return f'&start_date={self.DATE}&end_date={self.DATE}'
        else:
            return f'&start_date={self._DEFAULT_DATE}&end_date={date.today()}'
        
    def get_card_rating_url(self, colors) -> str:
        url = self._BASE_URL + f'card_ratings/data?expansion={self.SET}&format={self.FORMAT}'
        if colors:
            url += f'&colors={colors}'
        url += self.get_date_filter()
        return url
        
    def get_color_rating_url(self) -> str:
        url = self._BASE_URL + f'color_ratings/data?expansion={self.SET}&event_type={self.FORMAT}&combine_splash=false'
        url += self.get_date_filter()
        return url

    def get_folder_path(self):
        path = os.path.join(settings.DATA_DIR_LOC, settings.DATA_DIR_NAME, self.SET, self.FORMAT)
        if self.DATE:
            return os.path.join(path, str(self.DATE))
        else:
            return os.path.join(path, 'ALL')
         
    def get_file_path(self, filename):
        return os.path.join(self.get_folder_path(), filename)
    
    def file_exists(self, filename):
        return os.path.isfile(self.get_file_path(filename))

    def get_last_write_time(self):
        """
        Returns a UTC datetime object for the last write time of the managed files.
        :return: A datetime object.
        """
        try:
            filepath = os.path.abspath(self.get_file_path('ColorRatings.json'))
            wrt_tm = datetime.utcfromtimestamp(os.path.getmtime(filepath))
        except:
            wrt_tm = datetime(2020, 1, 1)
        self.LOGGER.log(f'Last write-time: {wrt_tm}', Logger.FLG.DEBUG)
        return wrt_tm

    def files_valid(self):
        """
        Returns a boolean which represents if the files contain valid data.
        Returns False if all of the files contain empty or default data.
        :return: A boolean.
        """
        folder_path = self.get_folder_path()
        files = os.listdir(folder_path)
        for x in files:
            # Min filesize is 129.
            if os.path.getsize(os.path.join(folder_path, x)) > 130:
                self.LOGGER.log(f'Non-empty file found: {x}', Logger.FLG.DEBUG)
                return True

        self.LOGGER.log(f'All files are empty!', Logger.FLG.DEBUG)
        return False
    
    def load_json_file(self, filename):
        """
        Loads and returns the data from a json file.
        :param folder: The folder the json file is in.
        :param filename: The name of the json file (including filetype).
        :return: An object contain the json data.
        """
        filepath = os.path.abspath(self.get_file_path(filename))

        try:
            with open(filepath, 'r') as f:
                json_str = f.read()
                f.close()
                self.LOGGER.log(f'File {filename} read sucessfully.', Logger.FLG.VERBOSE)
                return json.loads(json_str)
        except Exception as ex:
            self.LOGGER.log(f'Error reading json file {filename}', Logger.FLG.ERROR)
            self.LOGGER.log(ex, Logger.FLG.ERROR)
            return None

    def save_json_file(self, filename, data):
        """
        Saves provided data into the specified json file.
        :param folder: The folder the json file is in.
        :param filename: The name of the json file (including filetype).
        :param data: The object to be saved as json.
        :return: Whether the save operation was successful.
        """
        filepath = os.path.abspath(self.get_file_path(filename))

        try:
            with open(filepath, 'w') as f:
                f.write(json.dumps(data, indent=4))
                f.close()
            self.LOGGER.log(f'File {filename} written to.', Logger.FLG.VERBOSE)
            return True
        except Exception as ex:
            self.LOGGER.log(f'Error writing to json file {filename}', Logger.FLG.ERROR)
            self.LOGGER.log(ex, Logger.FLG.ERROR)
            return False
        
    def _get_data(self, url, filename, overwrite=False):
        if (not self.file_exists(filename)) or overwrite:
            if overwrite:
                self.LOGGER.log(f"Updating data for '{filename}'. Fetching from 17Lands site...", Logger.FLG.DEFAULT)
            else:
                self.LOGGER.log(f"Data for '{filename}' not found in saved data. Fetching from 17Lands site...", Logger.FLG.DEFAULT)
            data = self.FETCHER.fetch(url)
            self.save_json_file(filename, data)
        else:
            data = self.load_json_file(filename)
        return data
    
    def get_card_data(self, color, overwrite=False):
        return self._get_data(self.get_card_rating_url(color), f'{color}CardRatings.json', overwrite)

    def get_all_card_data(self, overwrite=False):
        card_dict = dict()
        for color in WUBRG.COLOR_GROUPS:
            card_dict[color] = self.get_card_data(color, overwrite)
        
        return card_dict

    def get_meta_data(self, overwrite=False):
        return self._get_data(self.get_color_rating_url(), f'ColorRatings.json', overwrite)
        
    def get_day_data(self, overwrite=False):
        if not self.files_valid():
            overwrite = True
        
        card_dict = self.get_all_card_data(overwrite)
        meta_dict = self.get_meta_data(overwrite)
        
        return card_dict, meta_dict
