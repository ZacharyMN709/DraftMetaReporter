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

    def _is_historic_data_available(self, requested_date: date, last_17l_update: datetime) -> bool:
        # Data for a given day will be exist at 2am UTC the following day.
        update_date = datetime.combine(requested_date, time(2, 0)) + timedelta(days=1)
        is_active = self._format_metadata.is_active(requested_date)
        has_updated = update_date <= last_17l_update

        Logger.LOGGER.log(f'Date to get data for:          {requested_date}', Logger.FLG.DEBUG)
        Logger.LOGGER.log(f'Date this data is available:   {update_date}', Logger.FLG.DEBUG)
        Logger.LOGGER.log(f'Last 17Lands Update:           {last_17l_update}', Logger.FLG.DEBUG)
        Logger.LOGGER.log(f'Data has updated:              {has_updated}', Logger.FLG.DEBUG)
        Logger.LOGGER.log(f'Set active on date:            {is_active}\n', Logger.FLG.DEBUG)

        return has_updated and is_active

    def get_historic_data(self, reload: bool = False, overwrite: bool = False) -> tuple[dict, dict]:
        """
        Gets all of the data by day for the set and format.
        If any data does not exist locally, it will be fetched from 17Lands and saved locally.
        :param reload: Forces reload data from the file
        :param overwrite: Forces overwrite the data in the file
        :return: A tuple of dictionaries filled with the archetype data and card data
        """

        # If the set/format has no data yet, log a message and return blank values.
        if utc_today() < self._format_metadata.START_DATE:
            Logger.LOGGER.log(f'{self.SET} {self.FORMAT} has no historic data to get!', Logger.FLG.DEFAULT)
            return dict(), dict()

        # Initialize the relevant dates to determine if data is available.
        requested_date = self._format_metadata.START_DATE
        last_17l_update_date = get_prev_17lands_update_time()

        # If the update date is before the last time 17Lands updated, the data could exist so,
        while requested_date <= last_17l_update_date:
            # Check if data is available for the requested_date, and if so do the update.
            if self._is_historic_data_available(requested_date, last_17l_update_date):
                self.get_day_data(requested_date, reload, overwrite)
            requested_date += timedelta(days=1)

        return self._CARD_DICTS, self._META_DICT

    def _is_summary_data_stale(self, last_write, last_17l_update):
        # Check if the data has been updated since last write and that the format is still open.
        end_date = self._format_metadata.END_DATE + timedelta(days=3)
        data_updated = last_write < last_17l_update
        data_live = last_write.date() < end_date

        Logger.LOGGER.log(f'Last File Write Time:          {last_write}', Logger.FLG.DEBUG)
        Logger.LOGGER.log(f'Last 17Lands Update:           {last_17l_update}', Logger.FLG.DEBUG)
        Logger.LOGGER.log(f'End Date:                      {end_date}', Logger.FLG.DEBUG)
        Logger.LOGGER.log(f'Cached data is stale:          {data_updated}', Logger.FLG.DEBUG)
        Logger.LOGGER.log(f'The set is live:               {data_live}', Logger.FLG.DEBUG)

        return data_updated and data_live

    def get_summary_data(self, reload: bool = False, overwrite: bool = False) -> \
            tuple[dict[str, list[dict]], list[dict]]:
        """
        Gets the aggregated data for the set and format
        Depending on the age of the data, it will be updated automatically.
        :param reload: Forces reload data from the file
        :param overwrite: Forces overwrite the data in the file
        :return: A tuple of dictionaries filled with the archetype data and card data
        """

        # If the set/format has no data yet, log a message and return blank values.
        if not self._format_metadata.has_data:  # pragma: no cover
            Logger.LOGGER.log(f'{self.SET} {self.FORMAT} has no summary data to get!', Logger.FLG.DEFAULT)
            return dict(), list()

        # Initialize the loader
        loader = DataLoader(self.SET, self.FORMAT, None)

        # Determine the object is missing data.
        data_unloaded = (not self._SUMMARY_META_DICT) or (not self._SUMMARY_CARD_DICTS)

        # Get the relevant times for updates, and check if the data is stale.
        last_write = loader.get_last_summary_update_time()
        last_17l_update = get_prev_17lands_update_time()
        stale_data = self._is_summary_data_stale(last_write, last_17l_update)

        # Reload the data if necessary.
        if reload or data_unloaded or stale_data:
            # If we want to force an overwrite or if the existing data is stale, set the overwrite flag.
            overwrite = overwrite or stale_data
            Logger.LOGGER.log(f'Getting overall data for {self.SET} {self.FORMAT}', Logger.FLG.DEFAULT)
            self._SUMMARY_CARD_DICTS, self._SUMMARY_META_DICT = loader.get_day_data(overwrite)

        return self._SUMMARY_CARD_DICTS, self._SUMMARY_META_DICT
