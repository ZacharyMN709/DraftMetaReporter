import requests
from time import sleep
import json

import settings
from Logger import Logger

class Fetcher():
    
    def __init__(self, tries=None, fail_delay=None, succ_delay=None):
        ## TODO: Handle values via a defaults or config.
        self._TRIES = tries if tries is not None else 5
        self._FAIL_DELAY = fail_delay if fail_delay is not None else 60
        self._SUCC_DELAY = succ_delay if succ_delay is not None else 1
        
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
                Logger.LOGGER.log(f'Attempting to get data from {url}.', Logger.FLG.DEBUG)
                response = requests.get(url)
                data = response.json()

                success = True
                sleep(self._SUCC_DELAY)
                return data
            except:
                if count < self._TRIES:
                    Logger.LOGGER.log(f'Failed to get data. Trying again in {self._FAIL_DELAY} seconds.', Logger.FLG.DEFAULT)
                    sleep(self._FAIL_DELAY)
                    continue
                else:
                    Logger.LOGGER.log(f'Failed to get data after {self._TRIES} attempts.', Logger.FLG.ERROR)
                    Logger.LOGGER.log(f'Failed URL: {url}', Logger.FLG.ERROR)
                    return None  

