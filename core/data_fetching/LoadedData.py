from core.data_fetching.utils import META_DATA, WUBRG_CARD_DATA
from datetime import time, date, datetime, timedelta

from core.utilities.auto_logging import logging
from core.game_metadata import FormatMetadata

from core.data_fetching.utils.date_helper import get_prev_17lands_update_time
from core.data_fetching.DataLoader import DataLoader


class LoadedData:
    """
    LoadedData is meant as an intermediary step between getting the data and converting it into Pandas
    DataFrames. It's been left separate to reduce the size of classes, along with allowing for ways to access and
    handle data without the use of Pandas - though that's not recommended.
    """

    def __init__(self, set_code: str, format_name: str):
        self.SET: str = set_code
        self.FORMAT: str = format_name
        self._format_metadata: FormatMetadata = FormatMetadata.get_metadata(set_code, format_name)

        self._CARD_DATA_DICT: dict[str, WUBRG_CARD_DATA] = dict()
        self._META_DATA_DICT: dict[str, META_DATA] = dict()

        self._CARD_SUMMARY_DICTS: WUBRG_CARD_DATA = dict()
        self._META_SUMMARY_DICT: META_DATA = list()

    def get_day_data(self, check_date: date, reload: bool = False, overwrite: bool = False) \
            -> tuple[WUBRG_CARD_DATA, META_DATA]:
        """
        Gets all of the data for a given day, for the object's set and format.
        If the data does not exist locally, it will be fetched from 17Lands and saved locally.
        :param check_date: The date to get the data for
        :param reload: Forces reload data from the file
        :param overwrite: Forces overwrite the data in the file
        :return: A tuple of dictionaries filled with the archetype data and card data
        """

        str_date: str = str(check_date)
        data_missing: bool = (str_date not in self._META_DATA_DICT) or (str_date not in self._CARD_DATA_DICT)
        update: bool = data_missing or reload

        if update:
            loader: DataLoader = DataLoader(self.SET, self.FORMAT, check_date)
            logging.info(f'Getting data for {self.SET} {self.FORMAT}, date: {str_date}')
            card_data, meta_data = loader.get_day_data(overwrite)

            if not card_data:  # pragma: no cover
                logging.verbose('`card_data` for {str_date} is empty.')
            if not meta_data:  # pragma: no cover
                logging.verbose(f'`meta_data` for {str_date} is empty.')

            self._CARD_DATA_DICT[str_date] = {color: card_data[color] for color in card_data}
            self._META_DATA_DICT[str_date] = meta_data

        return self._CARD_DATA_DICT[str_date], self._META_DATA_DICT[str_date]

    def _is_historic_data_available(self, requested_date: datetime, last_17l_update: datetime) \
            -> bool:
        # Data for a given day will be exist at 2am UTC the following day.
        update_date: datetime = datetime.combine(requested_date, time(2, 0)) + timedelta(days=1)
        has_updated: bool = update_date <= last_17l_update
        is_active: bool = self._format_metadata.is_active(requested_date)

        logging.debug(f'Date to get data for:          {requested_date}')
        logging.debug(f'Date this data is available:   {update_date}')
        logging.debug(f'Last 17Lands Update:           {last_17l_update}')
        logging.debug(f'Data has updated:              {has_updated}')
        logging.debug(f'Set active on date:            {is_active}\n')

        return has_updated and is_active

    def get_historic_data(self, reload: bool = False, overwrite: bool = False) \
            -> tuple[dict[str, WUBRG_CARD_DATA], dict[str, META_DATA]]:
        """
        Gets all of the data by day for the set and format.
        If any data does not exist locally, it will be fetched from 17Lands and saved locally.
        :param reload: Forces reload data from the file
        :param overwrite: Forces overwrite the data in the file
        :return: A tuple of dictionaries filled with the archetype data and card data
        """

        # If the set/format has no data yet, log a message and return blank values.
        if not self._format_metadata.has_data:  # pragma: no cover
            logging.info(f'{self.SET} {self.FORMAT} has no historic data to get!')
            return dict(), dict()

        # Initialize the relevant dates to determine if data is available.
        requested_date: datetime = datetime.combine(self._format_metadata.START_DATE, time(0, 0))
        last_17l_update_date: datetime = get_prev_17lands_update_time()

        # If the update date is before the last time 17Lands updated, the data could exist so,
        while requested_date <= last_17l_update_date:
            # Check if data is available for the requested_date, and if so do the update.
            if self._is_historic_data_available(requested_date, last_17l_update_date):
                self.get_day_data(requested_date.date(), reload, overwrite)
            requested_date += timedelta(days=1)

        return self._CARD_DATA_DICT, self._META_DATA_DICT

    def _is_summary_data_stale(self, last_write: datetime, last_17l_update: datetime) \
            -> bool:
        # Check if the data has been updated since last write and that the format is still open.
        end_date = self._format_metadata.END_DATE + timedelta(days=3)
        data_updated = last_write < last_17l_update
        data_live = last_write.date() < end_date

        logging.debug(f'Last File Write Time:          {last_write}')
        logging.debug(f'Last 17Lands Update:           {last_17l_update}')
        logging.debug(f'End Date:                      {end_date}')
        logging.debug(f'Cached data is stale:          {data_updated}')
        logging.debug(f'The set is live:               {data_live}\n')

        return data_updated and data_live

    def get_summary_data(self, reload: bool = False, overwrite: bool = False) -> \
            tuple[WUBRG_CARD_DATA, META_DATA]:
        """
        Gets the aggregated data for the set and format
        Depending on the age of the data, it will be updated automatically.
        :param reload: Forces reload data from the file
        :param overwrite: Forces overwrite the data in the file
        :return: A tuple of dictionaries filled with the archetype data and card data
        """

        # If the set/format has no data yet, log a message and return blank values.
        if not self._format_metadata.has_data:  # pragma: no cover
            logging.info(f'{self.SET} {self.FORMAT} has no summary data to get!')
            return dict(), list()

        # Initialize the loader
        loader = DataLoader(self.SET, self.FORMAT, None)

        # Determine the object is missing data.
        data_unloaded = (not self._META_SUMMARY_DICT) or (not self._CARD_SUMMARY_DICTS)

        # Get the relevant times for updates, and check if the data is stale.
        last_write = loader.get_last_summary_update_time()
        last_17l_update = get_prev_17lands_update_time()
        stale_data = self._is_summary_data_stale(last_write, last_17l_update)

        # Reload the data if necessary.
        if reload or data_unloaded or stale_data:
            # If we want to force an overwrite or if the existing data is stale, set the overwrite flag.
            overwrite = overwrite or stale_data
            logging.info(f'Getting overall data for {self.SET} {self.FORMAT}')
            self._CARD_SUMMARY_DICTS, self._META_SUMMARY_DICT = loader.get_day_data(overwrite)

        return self._CARD_SUMMARY_DICTS, self._META_SUMMARY_DICT
