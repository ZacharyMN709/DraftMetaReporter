from typing import NoReturn
import pandas as pd

from Utilities import Logger

from data_fetching.utils.pandafy import gen_card_frame, gen_meta_frame, append_card_info
from data_fetching.LoadedData import LoadedData
from game_metadata import FormatMetadata


class DataFramer:
    """
    DataFramer is responsible for converting the data aggregated by LoadedData into Pandas DataFrames.
    Once it does, it contains all summary and historical data for a given set and format.
    """

    def __init__(self, set_code: str, format_name: str, load_summary: bool = True, load_history: bool = True):
        self._SET = set_code
        self._FORMAT = format_name
        self._FETCHER = LoadedData(set_code, format_name)
        self._format_metadata = FormatMetadata.get_metadata(set_code, format_name)

        self.load_summary = load_summary
        self.load_history = load_history

        self._GROUPED_ARCHETYPE_HISTORY_FRAME = None
        self._SINGLE_ARCHETYPE_HISTORY_FRAME = None
        self._CARD_HISTORY_FRAME = None

        self._GROUPED_ARCHETYPE_SUMMARY_FRAME = None
        self._SINGLE_ARCHETYPE_SUMMARY_FRAME = None
        self._CARD_SUMMARY_FRAME = None

    @property
    def SET(self):  # pragma: no cover
        """The draft set."""
        return self._SET

    @property
    def FORMAT(self):  # pragma: no cover
        """The queue type."""
        return self._FORMAT

    @property
    def GROUPED_ARCHETYPE_HISTORY_FRAME(self):
        """The daily data about how decks, grouped by number of colours, performs."""
        if self.load_history and self._GROUPED_ARCHETYPE_HISTORY_FRAME is None:  # pragma: no cover
            self.gen_hist()
        return self._GROUPED_ARCHETYPE_HISTORY_FRAME

    @property
    def SINGLE_ARCHETYPE_HISTORY_FRAME(self):
        """The daily data for each deck archetype."""
        if self.load_history and self._SINGLE_ARCHETYPE_HISTORY_FRAME is None:  # pragma: no cover
            self.gen_hist()
        return self._SINGLE_ARCHETYPE_HISTORY_FRAME

    @property
    def CARD_HISTORY_FRAME(self):
        """The daily data for individual card performance."""
        if self.load_history and self._CARD_HISTORY_FRAME is None:  # pragma: no cover
            self.gen_hist()
        return self._CARD_HISTORY_FRAME

    @property
    def GROUPED_ARCHETYPE_SUMMARY_FRAME(self):
        """The overall data, about how decks, grouped by number of colours, performs."""
        if self.load_summary and self._GROUPED_ARCHETYPE_SUMMARY_FRAME is None:  # pragma: no cover
            self.gen_summary()
        return self._GROUPED_ARCHETYPE_SUMMARY_FRAME

    @property
    def SINGLE_ARCHETYPE_SUMMARY_FRAME(self):
        """The overall data, for each deck archetype."""
        if self.load_summary and self._SINGLE_ARCHETYPE_SUMMARY_FRAME is None:  # pragma: no cover
            self.gen_summary()
        return self._SINGLE_ARCHETYPE_SUMMARY_FRAME

    @property
    def CARD_SUMMARY_FRAME(self):
        """The overall data, about individual card performance."""
        if self.load_summary and self._CARD_SUMMARY_FRAME is None:  # pragma: no cover
            self.gen_summary()
        return self._CARD_SUMMARY_FRAME

    def gen_hist(self, reload: bool = False, overwrite: bool = False) -> None:
        """Populates and updates the three 'HISTORY' properties."""
        hist_card, hist_meta = self._FETCHER.get_historic_data(reload, overwrite)
        if (not hist_card) and (not hist_meta):  # pragma: no cover
            return

        # TODO: Attempt to handle this in a way so the entire history frames
        #  aren't reloaded each time this function is called.

        grouped_arch_frame_dict: dict[str, pd.DataFrame] = dict()
        single_arch_frame_dict: dict[str, pd.DataFrame] = dict()
        card_frame_dict: dict[str, pd.DataFrame] = dict()

        Logger.LOGGER.log(f'Pandafying historical data for {self.SET} {self.FORMAT}...', Logger.FLG.VERBOSE)

        for date in hist_meta:
            grouped, single = gen_meta_frame(hist_meta[date])
            grouped_arch_frame_dict[date] = grouped
            single_arch_frame_dict[date] = single
        grouped_arch_frame = pd.concat(grouped_arch_frame_dict, names=["Date", "Name"])
        single_arch_frame = pd.concat(single_arch_frame_dict, names=["Date", "Name"])

        for date in hist_card:
            color_dict: dict[str, pd.DataFrame] = dict()
            for color in hist_card[date]:
                frame = gen_card_frame(hist_card[date][color])
                frame = append_card_info(frame, self._format_metadata.CARD_DICT)
                color_dict[color] = frame
            card_frame_dict[date] = pd.concat(color_dict, names=["Deck Colors", "Name"])
        card_frame = pd.concat(card_frame_dict, names=["Date", "Deck Colors", "Name"])

        Logger.LOGGER.log(f'Finished pandafying data.', Logger.FLG.VERBOSE)

        self._GROUPED_ARCHETYPE_HISTORY_FRAME = grouped_arch_frame
        self._SINGLE_ARCHETYPE_HISTORY_FRAME = single_arch_frame
        self._CARD_HISTORY_FRAME = card_frame

    def gen_summary(self, reload: bool = False, overwrite: bool = False) -> NoReturn:
        """Populates and updates the three 'SUMMARY' properties."""
        hist_card, hist_meta = self._FETCHER.get_summary_data(reload, overwrite)
        if (not hist_card) and (not hist_meta):  # pragma: no cover
            return

        grouped_arch_frame, single_arch_frame = gen_meta_frame(hist_meta)

        color_dict = dict()
        for color in hist_card:
            frame = gen_card_frame(hist_card[color])
            frame = append_card_info(frame, self._format_metadata.CARD_DICT)
            color_dict[color] = frame
        card_frame = pd.concat(color_dict, names=["Deck Colors", "Name"])

        self._GROUPED_ARCHETYPE_SUMMARY_FRAME = grouped_arch_frame
        self._SINGLE_ARCHETYPE_SUMMARY_FRAME = single_arch_frame
        self._CARD_SUMMARY_FRAME = card_frame

    def check_for_updates(self) -> NoReturn:  # pragma: no cover
        """Populates and updates data properties, filling in missing selected data."""
        Logger.LOGGER.log(f'Checking for missing data for {self.SET} {self.FORMAT}...', Logger.FLG.KEY)
        if self.load_summary:
            self.gen_summary()
        if self.load_history:
            self.gen_hist()
        Logger.LOGGER.log(f'Finished checking for missing data for {self.SET} {self.FORMAT}.\r\n', Logger.FLG.KEY)

    def reload_data(self) -> NoReturn:  # pragma: no cover
        """Populates and updates data properties, reloading selected data."""
        Logger.LOGGER.log(f'Loading data for {self.SET} {self.FORMAT}', Logger.FLG.KEY)
        if self.load_summary:
            self.gen_summary(True)
        if self.load_history:
            self.gen_hist(True)
        Logger.LOGGER.log(f'Finished loading data for {self.SET} {self.FORMAT}.\r\n', Logger.FLG.KEY)

    def force_update(self) -> NoReturn:  # pragma: no cover
        """Forcibly re-fetches and overwrites selected data."""
        Logger.LOGGER.log(f'Re-downloading data for {self.SET} {self.FORMAT}', Logger.FLG.KEY)
        if self.load_summary:
            self.gen_summary(True, True)
        if self.load_history:
            self.gen_hist(True, True)
        Logger.LOGGER.log(f'Finished re-downloading data for {self.SET} {self.FORMAT}.\r\n', Logger.FLG.KEY)
