from typing import Optional, Union
from time import sleep
import requests
from requests import Response

from Utilities.auto_logging import logging
from Utilities.utils.settings import TRIES, FAIL_DELAY, SUCCESS_DELAY


class Requester:
    """ Helps to handle getting data from url end points, with some configurable options about timing. """

    def __init__(self, tries: Optional[int] = None, fail_delay: Optional[float] = None,
                 success_delay: Optional[float] = None):
        self._TRIES: int = tries or TRIES
        self._FAIL_DELAY: float = fail_delay or FAIL_DELAY
        self._SUCCESS_DELAY: float = success_delay or SUCCESS_DELAY

    def request(self, url: str) -> Optional[Union[list, dict]]:
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


class Requester_2:  # pragma: no cover
    """ Helps to handle getting data from url end points, with some configurable options about timing. """

    def __init__(self, tries: Optional[int] = None, fail_delay: Optional[float] = None,
                 success_delay: Optional[float] = None):
        self._TRIES: int = tries or TRIES
        self._FAIL_DELAY: float = fail_delay or FAIL_DELAY
        self._SUCCESS_DELAY: float = success_delay or SUCCESS_DELAY

    def request(self, url: str, params: Optional[dict[str, str]] = None) -> Optional[Response]:
        """
        Attempts to get json data from a url.
        :param url: The url to get data from
        :param params: A dictionary of parameters to include in the url.
        :return: A json object or None
        """
        success = False
        count = 0
        composed_url = url
        if params:
            composed_url = url + '?' + '&'.join([f"{k}={v}" for k, v in params.items()])

        while not success:
            count += 1

            try:
                logging.debug(f"Attempting to get data from '{composed_url}'.")
                response = requests.get(composed_url)

                success = True
                sleep(self._SUCCESS_DELAY)
                return response
            # TODO: Consider handling errors based on specific connection issue.
            except Exception as ex:
                if count < self._TRIES:
                    logging.info(f'Failed to get data. Trying again in {self._FAIL_DELAY} seconds.')
                    sleep(self._FAIL_DELAY)
                    continue
                else:
                    logging.error(f'Failed to get data after {self._TRIES} attempts.')
                    logging.error(f'Failed URL: {composed_url}')
                    logging.error(f'Exception: {ex}')
                    return None
