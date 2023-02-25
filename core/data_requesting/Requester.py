"""
Helps to handle getting data from url end points, with some configurable options about timing.
"""

from typing import Optional, Union
from time import sleep
from requests import Response, get

from core.utilities import logging

from core.data_requesting.utils import TRIES, FAIL_DELAY, SUCCESS_DELAY


class Requester:
    """ Helps to handle getting data from url end points, with some configurable options about timing. """
    def __init__(self, tries: int = None, fail_delay: float = None, success_delay: float = None):
        self._TRIES: int = tries or TRIES
        self._FAIL_DELAY: float = fail_delay or FAIL_DELAY
        self._SUCCESS_DELAY: float = success_delay or SUCCESS_DELAY
        self.valid_responses: list[int] = [200]

    def fetch(self, url) -> Optional[Response]:
        try:
            # Try to get the data from the URL.
            logging.debug(f"Attempting to get data from '{url}'.")
            response = get(url)

            # TODO: Consider how to handle 100 and 300 responses.
            # If the response is 400s or 500s (Client/Server Errors) return None.
            if response.status_code not in self.valid_responses:
                logging.debug(f'Response did not contain a valid status code. ({response.status_code})')
                return None

            # Otherwise, getting the data was a success, so wait and return it.
            logging.debug(f"Successfully got response from '{url}'.")
            sleep(self._SUCCESS_DELAY)
            return response
        except Exception as ex:
            # On an failure to connect to the URL, return None.
            logging.error(f'Encountered unexpected error: {ex}')
            return None

    def raw_request(self, url: str, params: Optional[dict[str, str]] = None) -> Optional[Response]:
        """
        Attempts to get json data from a url.
        :param url: The url to get data from
        :param params: A dictionary of parameters to include in the url.
        :return: A json object or None
        """
        # Generate the url to check.
        composed_url = url
        if params:
            composed_url = url + '?' + '&'.join([f"{k}={v}" for k, v in params.items()])

        # Try to get the data the number of time prescribed, returning it when it's not None.
        for cnt in range(1, self._TRIES + 1):
            response = self.fetch(composed_url)
            if response is not None:
                return response

            # If it isn't the last try, wait and try again.
            if cnt < self._TRIES:
                logging.warning(f'Failed to get data. Trying again in {self._FAIL_DELAY} seconds.')
                sleep(self._FAIL_DELAY)

        # Logging any failure to get data, and returning None.
        logging.error(f'Failed to get data after {self._TRIES} attempts.')
        logging.error(f'Failed URL: {composed_url}')
        return None

    def request(self, url: str, params: Optional[dict[str, str]] = None) -> Optional[Union[list, dict]]:
        ret = self.raw_request(url, params)
        if ret is not None:
            try:
                return ret.json()
            except Exception as ex:
                logging.error(f'Failed to parse JSON for url: {url}')
                logging.error(ret)
                logging.error(ret.content)
                raise ex
        return None

    def raw_paginated_request(self, url: str, params: Optional[dict[str, str]] = None) -> Optional[list[Response]]:
        response = self.raw_request(url, params)

        if response is None:
            return None

        ret = [response]
        url = response.json().get('next_page')

        while url:
            try:
                logging.debug(f"Fetching next page. ({url})")
                response = self.raw_request(url)
                ret.append(response)
                url = response.json().get('next_page')
            except KeyError as ex:
                logging.error(f"{ex} was not found in the returned json.")
                break
            except Exception as ex:
                logging.error(f'Encountered unexpected error: {ex}')
                break

        return ret

    def paginated_request(self, url: str, params: Optional[dict[str, str]] = None) -> Optional[list]:
        ret = self.raw_paginated_request(url, params)
        if ret is None:
            return None
        return [r.json() for r in ret if r]
