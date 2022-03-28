import requests
from time import sleep
import json


import settings
from Logger import Logger

class Fetcher():
    _TRIES = 5
    _FAIL_DELAY = 60
    _SUCC_DELAY = 1
    
    def __init__(self, LOGGER=None):
        if LOGGER is None:
            LOGGER = Logger()
        self.LOGGER = LOGGER

        
    def fetch(self, url: str) -> object:
        """
        Attempts to get json data from a url.
        :param url: The url to get data from
        :return: A json object or None
        """
        success = False
        count = 0

        while not success:
            count += 1

            try:
                self.LOGGER.log(f'Attempting to get data from {url}.', Logger.FLG.DEBUG)
                response = requests.get(url)
                data = response.json()

                success = True
                sleep(self._SUCC_DELAY)
                return data
            except:
                if count < self._TRIES:
                    self.LOGGER.log(f'Failed to get data. Trying again in {self._FAIL_DELAY} seconds.', Logger.FLG.DEFAULT)
                    sleep(self._FAIL_DELAY)
                    continue
                else:
                    self.LOGGER.log(f'Failed to get data after {self._TRIES} attempts.', Logger.FLG.ERROR)
                    self.LOGGER.log(f'Failed URL: {url}', Logger.FLG.ERROR)
                    return None  
