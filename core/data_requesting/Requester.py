"""
Helps to handle getting data from url end points, with some configurable options about timing.
"""
from json import JSONDecodeError
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
        """
        Attempts to get a Response from the given URL, and returns it if it has a valid response code.
        :param url: The url to get data from
        :return: A Response or None
        """
        try:
            # Try to get the data from the URL.
            logging.debug(f"Attempting to get data from '{url}'.")
            response = get(url)

            # If the response is not in one of the valid response codes return None,
            #  to denote we failed to get the data. We use a list of response codes,
            #  since different sites contain useful information on different response codes.
            #  Eg. Scryfall's 404 can be returned if a card has too many matches (like 'Bolt').
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

    def raw_request(self, url: str, params: dict[str, str] = None) -> Optional[Response]:
        """
        Attempts to get a response from a url, within a given number of tries.
        :param url: The url to get data from
        :param params: A dictionary of parameters to include in the url.
        :return: A Response or None
        """
        # Generate the url to check.
        composed_url = url
        if params:
            composed_url = url + '?' + '&'.join([f"{k}={v}" for k, v in params.items()])

        # Try to get the data the number of time prescribed, returning it whenever it's not None.
        #  If it can't be gotten in under the number of tries allowed, break the loop,
        #  log an error, and return None.
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

    def request(self, url: str, params: dict[str, str] = None) -> Optional[Union[list, dict]]:
        """
        Attempts to get json data from a url, within a given number of tries.
        :param url: The url to get data from
        :param params: A dictionary of parameters to include in the url.
        :return: A json object or None
        """
        # Get the response, short-circuiting if it's None.
        response = self.raw_request(url, params)
        if response is None:
            return None

        # Attempt to return the decode the response's JSON, defaulting to None if it can't be parsed.
        try:
            return response.json()
        except JSONDecodeError:
            logging.error(f'Failed to parse JSON for url: {url}')
            logging.error(response)
            logging.error(response.content)
            return None

    def raw_paginated_request(self, url: str, params: dict[str, str] = None) -> Optional[list[Response]]:
        # Get the response, short-circuiting if it's None.
        response = self.raw_request(url, params)
        if response is None:
            return None

        # Initialise a list with the response, and then get the URL for the next page.
        ret = [response]
        url = response.json().get('next_page')

        # While we have a url to query, get the next response.
        while url:
            logging.debug(f"Fetching next page. ({url})")
            response = self.raw_request(url)

            # If the response is None, break. We either have a connection issue or a bad link. Either way,
            #  we don't want to pollute the returned list with None.
            if response is None:
                break

            # Add the response, and then check to see if it has another URL to request.
            ret.append(response)
            url = response.json().get('next_page')

        # Return all of the responses received.
        return ret

    def paginated_request(self, url: str, params: dict[str, str] = None) -> Optional[list[Union[list, dict]]]:
        ret = self.raw_paginated_request(url, params)
        if ret is None:
            return None
        return [r.json() for r in ret if r]
