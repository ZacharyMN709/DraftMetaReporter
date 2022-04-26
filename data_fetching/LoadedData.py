from datetime import time, date, datetime, timedelta

from Utilities import Logger
from game_metadata import FormatMetadata

from data_fetching.utils.date_helper import get_prev_17lands_update_time, utc_today
from data_fetching.DataLoader import DataLoader


class LoadedData:
    """
    LoadedData is meant as an intermediary step between getting the data and converting it into Pandas
    DataFrames. It's been left separate to reduce the size of classes, along with allowing for ways to access and
    handle data without the use of Pandas - though that's not recommended.
    """

    def __init__(self, set_name: str, format_name: str):
        self.SET = set_name
        self.FORMAT = format_name
        self._format_metadata = FormatMetadata.get_metadata(set_name, format_name)

        self._META_DICT = dict()
        self._CARD_DICTS = dict()

        self._SUMMARY_META_DICT = dict()
        self._SUMMARY_CARD_DICTS = dict()

    def get_day_data(self, check_date: date, reload: bool = False, overwrite: bool = False) -> tuple[dict, dict]:
        """
        Gets all of the data for a given day, for the object's set and format.
        If the data does not exist locally, it will be fetched from 17Lands and saved locally.
        :param check_date: The date to get the data for
        :param reload: Forces reload data from the file
        :param overwrite: Forces overwrite the data in the file
        :return: A tuple of dictionaries filled with the archetype data and card data
        """

        str_date = str(check_date)
        data_missing = (str_date not in self._META_DICT) or (str_date not in self._CARD_DICTS)
        update = data_missing or reload

        if update:
            loader = DataLoader(self.SET, self.FORMAT, check_date)
            Logger.LOGGER.log(f'Getting data for {self.SET} {self.FORMAT}, date: {str_date}', Logger.FLG.DEFAULT)
            card_dict, meta_dict = loader.get_day_data(overwrite)

            if not card_dict:  # pragma: no cover
                Logger.LOGGER.log(f'`card_dict` for {str_date} is empty.', Logger.FLG.VERBOSE)
            if not meta_dict:  # pragma: no cover
                Logger.LOGGER.log(f'`meta_dict` for {str_date} is empty.', Logger.FLG.VERBOSE)

            self._CARD_DICTS[str_date] = {color: card_dict[color] for color in card_dict}
            self._META_DICT[str_date] = meta_dict

        return self._CARD_DICTS[str_date], self._META_DICT[str_date]

    def get_historic_data(self, reload: bool = False, overwrite: bool = False) -> tuple[dict, dict]:
        """
        Gets all of the data by day for the set and format.
        If any data does not exist locally, it will be fetched from 17Lands and saved locally.
        :param reload: Forces reload data from the file
        :param overwrite: Forces overwrite the data in the file
        :return: A tuple of dictionaries filled with the archetype data and card data
        """
        check_date = min(self._format_metadata.START_DATE, utc_today())

        run = True
        while run:
            # If the format is active for the given date, get the data.
            if self._format_metadata.is_active(check_date):
                self.get_day_data(check_date, reload, overwrite)

            # Get the next day, and check to make sure data will exist for it on the site.
            check_date += timedelta(days=1)
            utc_check_date = datetime.combine(check_date, time(2, 0))
            run = utc_check_date < get_prev_17lands_update_time()

        return self._CARD_DICTS, self._META_DICT

    def get_summary_data(self, reload: bool = False, overwrite: bool = False) -> tuple[dict, list]:
        """
        Gets the aggregated data for the set and format
        Depending on the age of the data, it will be updated automatically.
        :param reload: Forces reload data from the file
        :param overwrite: Forces overwrite the data in the file
        :return: A tuple of dictionaries filled with the archetype data and card data
        """

        # If the set/format hasn't started yet, log a message and return empty dicts.
        has_started = self._format_metadata.START_DATE < utc_today()
        if not has_started:  # pragma: no cover
            Logger.LOGGER.log(f'{self.SET} {self.FORMAT} has not begun yet. No data to get!', Logger.FLG.DEFAULT)
            return dict(), list()

        # Determine the object is missing data.
        data_missing = (not self._SUMMARY_META_DICT) or (not self._SUMMARY_CARD_DICTS)

        # Initialize the loader.
        loader = DataLoader(self.SET, self.FORMAT, None)

        # Get the relevant times for updates.
        last_write = loader.get_last_write_time()
        ext_end_date = self._format_metadata.END_DATE + timedelta(days=7)

        # Check if the data has been updated since last write and that the format is still open.
        data_updated = last_write < get_prev_17lands_update_time()
        data_live = last_write.date() < ext_end_date
        stale_data = data_updated and data_live

        # Determine if an update is needed.
        update = reload or data_missing or stale_data

        if update:
            # If we want to force an overwrite or if the existing data is stale, set the overwrite flag.
            overwrite = overwrite or stale_data
            Logger.LOGGER.log(f'Getting overall data for {self.SET} {self.FORMAT}', Logger.FLG.DEFAULT)
            self._SUMMARY_CARD_DICTS, self._SUMMARY_META_DICT = loader.get_day_data(overwrite)

        return self._SUMMARY_CARD_DICTS, self._SUMMARY_META_DICT
