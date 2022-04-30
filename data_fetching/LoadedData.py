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
        self._summary_loader = DataLoader(self.SET, self.FORMAT, None)

        self._META_DICT = dict()
        self._CARD_DICTS = dict()

        self._SUMMARY_META_DICT: list[dict] = list()
        self._SUMMARY_CARD_DICTS: dict[str, list[dict]] = dict()

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

        if utc_today() < self._format_metadata.START_DATE:
            Logger.LOGGER.log(f'{self.SET} {self.FORMAT} has no historic data to get!', Logger.FLG.DEFAULT)
            return dict(), dict()

        # Initialize the date to start pulling data from, using the start of the set.
        target_date = self._format_metadata.START_DATE

        # Get the last time 17Lands updated its data.
        last_17l_update_date = get_prev_17lands_update_time()

        # Calculate when the data for the target date would be exist (the day after at 2am UTC).
        update_date = datetime.combine(target_date, time(2, 0)) + timedelta(days=1)

        # If the update date is before the last time 17Lands updated, the data should exist so,
        while update_date <= last_17l_update_date:
            Logger.LOGGER.log(f'Date to get data for:          {target_date}', Logger.FLG.DEBUG)
            Logger.LOGGER.log(f'Date this data is available:   {update_date}', Logger.FLG.DEBUG)

            # If the format is active for the target date, get the data.
            if self._format_metadata.is_active(target_date):
                self.get_day_data(target_date, reload, overwrite)

            # Increment to the next day, and repeat until we're looking for data that doesn't exist.
            target_date += timedelta(days=1)
            update_date += timedelta(days=1)

        return self._CARD_DICTS, self._META_DICT

    def get_summary_data(self, reload: bool = False, overwrite: bool = False) -> \
            tuple[dict[str, list[dict]], list[dict]]:
        """
        Gets the aggregated data for the set and format
        Depending on the age of the data, it will be updated automatically.
        :param reload: Forces reload data from the file
        :param overwrite: Forces overwrite the data in the file
        :return: A tuple of dictionaries filled with the archetype data and card data
        """

        # If the set/format has no data yet, log a message and return empty dicts.
        if not self._format_metadata.has_data:  # pragma: no cover
            Logger.LOGGER.log(f'{self.SET} {self.FORMAT} has no summary data to get!', Logger.FLG.DEFAULT)
            return dict(), list()

        # Determine the object is missing data.
        data_unloaded = (not self._SUMMARY_META_DICT) or (not self._SUMMARY_CARD_DICTS)

        # Get the relevant times for updates, and check if the data is stale.
        last_write = self._summary_loader.get_last_summary_update_time()
        last_17l_update = get_prev_17lands_update_time()
        end_date = self._format_metadata.END_DATE + timedelta(days=3)

        Logger.LOGGER.log(f'Last File Write Time:          {last_write}', Logger.FLG.DEBUG)
        Logger.LOGGER.log(f'Last 17Lands Update:           {last_17l_update}', Logger.FLG.DEBUG)
        Logger.LOGGER.log(f'End Date:                      {end_date}', Logger.FLG.DEBUG)

        # Check if the data has been updated since last write and that the format is still open.
        data_updated = last_write < last_17l_update
        data_live = last_write.date() < end_date
        stale_data = data_updated and data_live

        # Reload the data if necessary.
        if reload or data_unloaded or stale_data:
            # If we want to force an overwrite or if the existing data is stale, set the overwrite flag.
            overwrite = overwrite or stale_data
            Logger.LOGGER.log(f'Getting overall data for {self.SET} {self.FORMAT}', Logger.FLG.DEFAULT)
            self._SUMMARY_CARD_DICTS, self._SUMMARY_META_DICT = self._summary_loader.get_day_data(overwrite)

        return self._SUMMARY_CARD_DICTS, self._SUMMARY_META_DICT
