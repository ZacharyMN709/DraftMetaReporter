from typing import Union, Optional
from time import sleep
from datetime import timedelta
import requests
from requests import Response
from requests_cache import CachedSession

from Utilities.auto_logging import logging
from Utilities import TRIES, FAIL_DELAY, SUCCESS_DELAY


class Fetcher:
    """ Helps to handle getting data from url end points, with some configurable options about timing. """

    def __init__(self, tries=None, fail_delay=None, success_delay=None) -> None:
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


class Fetcher_2:
    """ Helps to handle getting data from url end points, with some configurable options about timing. """

    def __init__(self, cache_folder: str, tries: int = TRIES,
                 fail_delay: int = FAIL_DELAY, success_delay: int = SUCCESS_DELAY) -> None:
        self.cache_folder = cache_folder
        self._tries = tries
        self._fail_delay = fail_delay
        self._success_delay = success_delay

        # Cache API responses with requests_cache
        self.session = CachedSession(
            self.cache_folder,
            backend='filesystem',
            serializer='json',
            expire_after=timedelta(days=180),
            cache_control=True,
            allowable_codes=[200],
            allowable_method=['GET'],
            stale_if_error=False
        )

    def fetch(self, url: str, params: Optional[dict[str, str]] = None, refresh: bool = False) -> Optional[Response]:
        """
        Attempts to get json data from a url.
        :param url: The url to get data from
        :param params: A dictionary of parameters to include in the url.
        :param refresh: Clear the element in the cache before sending the request.
        :return: A json object or None
        """
        success = False
        count = 0

        if refresh:
            self.session.cache.delete_url(url)

        while not success:
            count += 1

            try:
                logging.debug(f"Attempting to get data from '{url}'.")
                result = self.session.get(url=url, params=params)
                success = True
                sleep(self._success_delay)
                return result
            # TODO: Handle errors based on specific connection issue.
            except Exception as ex:
                if count < self._tries:
                    logging.info(f'Failed to get data. Trying again in {self._fail_delay} seconds.')
                    sleep(self._fail_delay)
                    continue
                else:
                    logging.error(f'Failed to get data after {self._tries} attempts.')
                    logging.error(f'Failed URL: {url}')
                    logging.error(f'Exception: {ex}')
                    return None
