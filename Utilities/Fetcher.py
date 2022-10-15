from typing import Union
import requests
from time import sleep

from Utilities.auto_logging import logging
from Utilities import TRIES, FAIL_DELAY, SUCCESS_DELAY


class Fetcher:
    """ Helps to handle getting data from url end points, with some configurable options about timing. """

    def __init__(self, tries=None, fail_delay=None, success_delay=None):
        self._TRIES = TRIES if tries is None else tries
        self._FAIL_DELAY = FAIL_DELAY if fail_delay is None else fail_delay
        self._SUCCESS_DELAY = SUCCESS_DELAY if success_delay is None else success_delay

    def fetch(self, url: str) -> Union[dict, None]:
        """
        Attempts to get json data from a url.
        :param url: The url to get data from
        :return: A json object or None
        """
        success = False
        count = 0
        url = url.replace(' ', '_')

        while not success:
            count += 1

            try:
                logging.debug(f"Attempting to get data from '{url}'.")
                response = requests.get(url)
                data = response.json()

                success = True
                sleep(self._SUCCESS_DELAY)
                return data
            # TODO: Consider handling errors based on specific connection issue.
            except Exception as ex:
                if count < self._TRIES:
                    logging.info(f'Failed to get data. Trying again in {self._FAIL_DELAY} seconds.')
                    sleep(self._FAIL_DELAY)
                    continue
                else:
                    logging.error(f'Failed to get data after {self._TRIES} attempts.')
                    logging.error(f'Failed URL: {url}')
                    logging.error(f'Exception: {ex}')
                    return None
