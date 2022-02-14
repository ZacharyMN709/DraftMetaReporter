import os
import requests
from time import sleep
from datetime import date
import json

import WUBRG
import consts


class JSONHandler:
    _TRIES = 5
    _DELAY = 60
    
    _DEFAULT_DATE = '2020-01-01'
    _BASE_URL = 'https://www.17lands.com/'
        
    def __init__(self, SET: str, FORMAT: str, DATE: date):
        self.SET = SET
        self.FORMAT = FORMAT
        self.DATE = DATE
        os.makedirs(self.get_folder_path(), exist_ok=True)
        
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
    
    def fetch(self, url: str) -> object:
        """
        Attempts to get json data from a url.
        :param url: The url to get data from
        """
        success = False
        count = 0

        while not success:
            count += 1

            try:
                response = requests.get(url)
                data = response.json()

                success = True
                sleep(0.5)
                return data
            except:
                if count < self._TRIES:
                    print(f'Failed to get data. Trying again in {self._DELAY} seconds.')
                    sleep(self._DELAY)
                    continue
                else:
                    print(f'Failed to get data after {self._TRIES} attempts.')
                    print(f'Failed URL: {url}')
                    return None        

    def get_folder_path(self):
        path = os.path.join('..', '17LandsData', self.SET, self.FORMAT)
        if self.DATE:
            return os.path.join(path, str(self.DATE))
        else:
            return os.path.join(path, 'ALL')
         
    def get_file_path(self, filename):
        return os.path.join(self.get_folder_path(), filename)
    
    def file_exists(self, filename):
        return os.path.isfile(self.get_file_path(filename))
    
    
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

                #print(f'File {filename} read sucessfully.')
                return json.loads(json_str)
        except Exception as ex:
            print(f'Error reading json file {filename}')
            print(ex)
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

            #print(f'File {filename} written to.')
            return True
        except Exception as ex:
            print(f'Error writing to json file {filename}')
            print(ex)
            return False
        
    def _get_data(self, url, filename, overwrite=False):
        if (not self.file_exists(filename)) or overwrite:
            if overwrite:
                print(f"Updating data for '{filename}'. Fetching from 17Lands site...")
            else:
                print(f"Data for '{filename}' not found in saved data. Fetching from 17Lands site...")
            data = self.fetch(url)
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
        card_dict = self.get_all_card_data(overwrite)
        meta_dict = self.get_meta_data(overwrite)
        
        return card_dict, meta_dict
