import requests
from time import sleep

from utils import settings
from utils.Logger import Logger


class Fetcher:

    def __init__(self, tries=None, fail_delay=None, success_delay=None):
        self._TRIES = settings.TRIES if tries is None else tries
        self._FAIL_DELAY = settings.FAIL_DELAY if fail_delay is None else fail_delay
        self._SUCCESS_DELAY = settings.SUCCESS_DELAY if success_delay is None else success_delay

    def fetch(self, url: str) -> dict[str, object]:
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
                sleep(self._SUCCESS_DELAY)
                return data
            except Exception:
                if count < self._TRIES:
                    Logger.LOGGER.log(f'Failed to get data. Trying again in {self._FAIL_DELAY} seconds.',
                                      Logger.FLG.DEFAULT)
                    sleep(self._FAIL_DELAY)
                    continue
                else:
                    Logger.LOGGER.log(f'Failed to get data after {self._TRIES} attempts.', Logger.FLG.ERROR)
                    Logger.LOGGER.log(f'Failed URL: {url}', Logger.FLG.ERROR)
                    return {'err_msg': f'Failed to get data for: {url}'}
