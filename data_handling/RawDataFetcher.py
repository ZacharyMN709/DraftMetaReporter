from datetime import time, datetime, timedelta

from utils.Logger import Logger
from utils.date_helper import get_prev_17lands_update_time, utc_today


from JSONHandler import JSONHandler
from game_metadata.FormatMetadata import FormatMetadata


class RawDataFetcher:
    def __init__(self, set_name, format_name):
        self._SET = set_name
        self._FORMAT = format_name
        self.FORMAT_METADATA = FormatMetadata(set_name, format_name)

        self._META_DICT = dict()
        self._CARD_DICTS = dict()

        self._SUMMARY_META_DICT = dict()
        self._SUMMARY_CARD_DICTS = dict()

    @property
    def SET(self):
        """The draft set."""
        return self._SET

    @property
    def FORMAT(self):
        """The queue type."""
        return self._FORMAT

    @property
    def META_DICT(self):
        """The daily data for archetype performance."""
        if not self._META_DICT:
            self.get_set_data()
        return self._META_DICT

    @property
    def CARD_DICTS(self):
        """The daily data for card performance."""
        if not self._CARD_DICTS:
            self.get_set_data()
        return self._CARD_DICTS

    @property
    def SUMMARY_META_DICT(self):
        """The overall data for archetype performance."""
        if not self._SUMMARY_META_DICT:
            self.get_summary_data()
        return self._SUMMARY_META_DICT

    @property
    def SUMMARY_CARD_DICTS(self):
        """The overall data for card performance."""
        if not self._SUMMARY_CARD_DICTS:
            self.get_summary_data()
        return self._SUMMARY_CARD_DICTS

    def get_day_data(self, check_date, reload=False, overwrite=False):
        """
        Gets all of the data for a given day, for the object's set and format.
        If the data does not exist locally, it will be fetched from 17Lands and saved locally.
        :param check_date: The date to get the data for
        :param reload: Force reload data from the file
        :param overwrite: Force overwrite the data in the file
        :return: A tuple of dictionaries filled with the archetype data and card data
        """

        str_date = str(check_date)
        data_missing = (str_date not in self._META_DICT) or (str_date not in self._CARD_DICTS)
        update = data_missing or reload

        if update:
            loader = JSONHandler(self.SET, self.FORMAT, check_date)
            Logger.LOGGER.log(f'Getting data for {self.SET} {self.FORMAT}, date: {str_date}', Logger.FLG.DEFAULT)
            card_dict, meta_dict = loader.get_day_data(overwrite)

            if not card_dict:
                Logger.LOGGER.log(f'`card_dict` for {str_date} is empty.', Logger.FLG.VERBOSE)
            if not meta_dict:
                Logger.LOGGER.log(f'`meta_dict` for {str_date} is empty.', Logger.FLG.VERBOSE)

            self._META_DICT[str_date] = meta_dict
            self._CARD_DICTS[str_date] = {color: card_dict[color] for color in card_dict}

        return self._META_DICT[str_date], self._CARD_DICTS[str_date]

    def get_set_data(self, reload=False, overwrite=False):
        """
        Gets all of the data by day for the set and format.
        If any data does not exist locally, it will be fetched from 17Lands and saved locally.
        :param reload: Force reload data from the file
        :param overwrite: Force overwrite the data in the file
        :return: A tuple of dictionaries filled with the archetype data and card data
        """
        check_date = min(self.FORMAT_METADATA.START_DATE, utc_today())

        run = True
        while run:
            # If the the format is active for the given date, get the data. 
            if self.FORMAT_METADATA.is_active(check_date):
                self.get_day_data(check_date, reload, overwrite)

            # Get the next day, and check to make sure data will exist for it on the site.
            check_date += timedelta(days=1)
            utc_check_date = datetime.combine(check_date, time(2, 0))
            run = utc_check_date < get_prev_17lands_update_time()

        return self._META_DICT, self._CARD_DICTS

    def get_summary_data(self, reload=False, overwrite=False):
        """
        Gets the aggregated data for the set and format
        Depending on the age of the data, it will be updated automatically.
        :param reload: Force reload data from the file
        :param overwrite: Force overwrite the data in the file
        :return: A tuple of dictionaries filled with the archetype data and card data
        """

        # If the set/format hasn't started yet, log a message and return empty dicts.
        has_started = self.FORMAT_METADATA.START_DATE < utc_today()
        if not has_started:
            Logger.LOGGER.log(f'{self.SET} {self.FORMAT} has not begun yet. No data to get!', Logger.FLG.DEFAULT)
            return dict(), dict()

        # Determine the update conditions
        data_missing = (not self._SUMMARY_META_DICT) or (not self._SUMMARY_CARD_DICTS)
        update = data_missing or reload

        # If an update is required, get the data.
        if update:
            loader = JSONHandler(self.SET, self.FORMAT, None)

            # Get the relevant times for updates.
            last_write = loader.get_last_write_time()
            ext_end_date = self.FORMAT_METADATA.END_DATE + timedelta(days=7)

            # Check if the data has been updated since last write and that the format is still open.
            data_updated = last_write < get_prev_17lands_update_time()
            data_live = last_write.date() < ext_end_date

            # Determine if an update is needed.
            update = data_updated and data_live

            Logger.LOGGER.log(f'Getting overall data for {self.SET} {self.FORMAT}', Logger.FLG.DEFAULT)
            self._SUMMARY_CARD_DICTS, self._SUMMARY_META_DICT = loader.get_day_data(overwrite)

        return self._SUMMARY_META_DICT, self._SUMMARY_CARD_DICTS
