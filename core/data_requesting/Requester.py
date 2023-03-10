"""
Helps to handle getting data from url end points, with some configurable options about timing.
"""
from json import JSONDecodeError
from typing import Optional, Union, Any
from time import sleep
from requests import Response, get

from core.utilities import logging

from core.data_requesting.utils import TRIES, FAIL_DELAY, SUCCESS_DELAY


class Requester:
    """ Helps to handle getting data from url end points, with some configurable options about timing. """
    def __init__(self, tries: int = None, fail_delay: float = None, success_delay: float = None,
                 valid_codes: list[int] = None):
        self._TRIES: int = tries or TRIES
        self._FAIL_DELAY: float = fail_delay or FAIL_DELAY
        self._SUCCESS_DELAY: float = success_delay or SUCCESS_DELAY
        self.valid_responses: list[int] = valid_codes or [200]

    @staticmethod
    def _gen_url(url: str, params: dict[str, Any] = None) -> str:
        """
        Takes a url and appends a dictionary of parameters to it.
        :param url: The base url.
        :param params: The parameters to include in the new url.
        :return: The new url.
        """
        # Generate the url to check, ignoring any parameters which are None
        composed_url = url
        if params:
            composed_url = url + '?' + '&'.join([f"{k}={v}" for k, v in params.items() if v is not None])
        return composed_url

    def request(self, url) -> Optional[Response]:
        """
        Attempts to get a Response from the given URL, and returns it if it has a valid response code.
        :param url: The url to get data from.
        :return: A Response or None.
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

    def get_response(self, url: str, params: dict[str, str] = None) -> Optional[Response]:
        """
        Attempts to get a response from a url, within a given number of tries.
        :param url: The url to get data from.
        :param params: A dictionary of parameters to include in the url.
        :return: A Response or None.
        """
        # Get the url to query based on the parameters.
        composed_url = self._gen_url(url, params)

        # Try to get the data the number of time prescribed, returning it whenever it's not None.
        #  If it can't be gotten in under the number of tries allowed, break the loop,
        #  log an error, and return None.
        for cnt in range(1, self._TRIES + 1):
            response = self.request(composed_url)
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

    def get_json_response(self, url: str, params: dict[str, str] = None) -> Optional[Union[list, dict]]:
        """
        Attempts to get json data from a url, within a given number of tries.
        :param url: The url to get data from.
        :param params: A dictionary of parameters to include in the url.
        :return: A json object or None.
        """
        # Get the response, short-circuiting if it's None.
        response = self.get_response(url, params)
        if response is None:
            return None

        # Attempt to return the decode the response's JSON, defaulting to None if it can't be parsed.
        try:
            return response.json()
        except JSONDecodeError:
            logging.error(f'Failed to parse JSON for url: {url}')
            logging.error(response)
            return None

    # TODO: Handle pagination more generically, instead of relying on JSON to exist.
    def get_paginated_response(self, url: str, params: dict[str, str] = None,
                               url_key: str = 'next_page') -> Optional[list[Response]]:
        """
        Attempts to get a series of responses from a url, within a given number of tries.
        :param url: The url to get data from.
        :param params: A dictionary of parameters to include in the url.
        :param url_key: The key to get the next page url from.
        :return: A list of Responses or None.
        """
        # Set up a list to store the responses.
        ret = list()

        # Define a helper function which validates the response and the url, keeping track of the responses.
        def parse_response(old_url):
            # Get the response, and initialise a variable for url.
            new_response = self.get_response(old_url)
            new_url = None

            # If a response is gotten, add it it the list, and try to get a url to query next.
            if new_response is not None:
                ret.append(new_response)
                try:
                    new_url = new_response.json().get(url_key)
                except JSONDecodeError:
                    logging.warning(f"Failed to get next url with key '{url_key}'")
            return new_response, new_url

        # Get the initial url to use, and get the response and url to fetch next.
        composed_url = self._gen_url(url, params)
        response, url = parse_response(composed_url)

        # While we have a url to query, get the next response and url.
        while url:
            logging.debug(f"Fetching next page. ({url})")
            response, url = parse_response(url)

        # Return all of the responses received, return None instead if the list is empty.
        if len(ret) == 0:
            return None
        return ret

    def get_paginated_json_response(self, url: str, params: dict[str, str] = None) -> Optional[list[Union[list, dict]]]:
        """
        Attempts to get a series of json objects from a url, within a given number of tries.
        :param url: The url to get data from.
        :param params: A dictionary of parameters to include in the url.
        :return: A list of json objects or None.
        """
        # Get the responses to parse the json from, short-circuiting if it's None.
        responses = self.get_paginated_response(url, params)
        if responses is None:
            return None

        # Initialise a list to hold the parse json, and then parse each response.
        ret = list()
        for response in responses:
            try:
                ret.append(response.json())
            except JSONDecodeError:
                # If we fail to parse a response, log an error and return None.
                logging.error(f'Failed to parse JSON for url: {url}')
                logging.error(response)
                return None
        return ret
