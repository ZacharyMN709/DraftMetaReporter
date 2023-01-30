from typing import Optional, Union
from time import sleep
from requests import Response, get

from utilities.auto_logging import logging
from utilities.utils.settings import TRIES, FAIL_DELAY, SUCCESS_DELAY


class Requester:
    """ Helps to handle getting data from url end points, with some configurable options about timing. """
    def __init__(self, tries: Optional[int] = None, fail_delay: Optional[float] = None,
                 success_delay: Optional[float] = None):
        self._TRIES: int = tries or TRIES
        self._FAIL_DELAY: float = fail_delay or FAIL_DELAY
        self._SUCCESS_DELAY: float = success_delay or SUCCESS_DELAY

    def raw_paginated_request(self, url: str, params: Optional[dict[str, str]] = None) -> list[Optional[Response]]:
        response = self.raw_request(url, params)
        ret = [response]
        url = response.json().get('next_page')

        while url:
            try:
                logging.debug(f"Fetching next page. ({url})")
                response = self.raw_request(url)
                ret.append(response)
                url = response.json().get('next_page')
            except KeyError as ex:  # pragma: nocover
                logging.error(f"{ex} was not found in the returned json.")
                break
            except Exception as ex:  # pragma: nocover
                logging.error(f'Encountered unexpected error: {ex}')
                break

        return ret

    def paginated_request(self, url: str, params: Optional[dict[str, str]] = None) -> list[Union[list, dict]]:
        return [r.json() for r in self.raw_paginated_request(url, params) if r]

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

        # Try to get the data the number of time prescribed
        for cnt in range(1, self._TRIES + 1):
            # Try to get the data, logging errors.
            try:
                logging.debug(f"Attempting to get data from '{composed_url}'.")
                response = get(composed_url)

                # And returning the data on a success, breaking the loop.
                if response is not None:
                    logging.debug(f"Successfully got data from '{composed_url}'.")
                    sleep(self._SUCCESS_DELAY)
                    return response
            except Exception as ex:
                logging.error(f'Encountered unexpected error: {ex}')

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
            return ret.json()
        return None
