from typing import NoReturn
import pandas as pd

from game_metadata import SetMetadata

from data_fetching.utils.consts import FORMAT_NICKNAME_DICT
from data_fetching.utils.index_slice_helper import get_name_slice, get_color_slice, get_date_slice
from data_fetching.DataFramer import DataFramer


class FramedData:
    """
    Acts as a wrapper for DataFramer, adding some extended functionality in how data can bet accessed and handled.
    One of its primary features is the ability to compress data over a given range into a summary, allowing data to be
    examined over certain parts of a format (After week 2, first meta shift, under-drafted colour becomes good, etc.)
    """

    def __init__(self, set_code: str, format_name: str, load_summary: bool = True, load_history: bool = True):
        self._set_metadata = SetMetadata.get_metadata(set_code)
        self.SET = set_code
        self.SET_NAME = self._set_metadata.FULL_NAME
        self.FORMAT = format_name
        self.FORMAT_ALIAS = FORMAT_NICKNAME_DICT[self.FORMAT].upper()
        self.DATA = DataFramer(set_code, format_name, load_summary, load_history)
        self._compare_key = self._set_metadata.FRAME_COMPARE_KEY

        self.load_summary = load_summary
        self.load_history = load_history

    def check_for_updates(self) -> NoReturn:  # pragma: no cover
        """Populates and updates all data properties, filling in missing data."""
        self.DATA.check_for_updates()

    def reload_data(self) -> NoReturn:  # pragma: no cover
        """Populates and updates all data properties, reloading all data."""
        self.DATA.reload_data()

    def deck_group_frame(self, name=None, date=None, summary=False) -> pd.DataFrame:
        """Returns a subset of the 'GROUPED_ARCHETYPE' data as a DataFrame."""
        name_slice = get_name_slice(name)
        date_slice = get_date_slice(date)

        if summary:
            return self.DATA.GROUPED_ARCHETYPE_SUMMARY_FRAME.loc(axis=0)[name_slice]
        else:
            return self.DATA.GROUPED_ARCHETYPE_HISTORY_FRAME.loc(axis=0)[date_slice, name_slice]

    def deck_archetype_frame(self, deck_color=None, date=None, summary=False) -> pd.DataFrame:
        """Returns a subset of the 'SINGLE_ARCHETYPE' data as a DataFrame."""
        deck_color_slice = get_color_slice(deck_color)
        date_slice = get_date_slice(date)

        if summary:
            return self.DATA.SINGLE_ARCHETYPE_SUMMARY_FRAME.loc(axis=0)[deck_color_slice]
        else:
            return self.DATA.SINGLE_ARCHETYPE_HISTORY_FRAME.loc(axis=0)[date_slice, deck_color_slice]

    def card_frame(self, name=None, deck_color=None, date=None, summary=False) -> pd.DataFrame:
        """Returns a subset of the 'CARD' data as a DataFrame."""
        name_slice = get_name_slice(name)
        deck_color_slice = get_color_slice(deck_color)
        date_slice = get_date_slice(date)

        if summary:
            return self.DATA.CARD_SUMMARY_FRAME.loc(axis=0)[deck_color_slice, name_slice]
        else:
            return self.DATA.CARD_HISTORY_FRAME.loc(axis=0)[date_slice, deck_color_slice, name_slice]

    def aggregate_card_frame(self, frame: pd.DataFrame) -> pd.DataFrame:  # pragma: no cover
        """
        Summarizes card data over a provided set of time.
        :param frame: The frame to run the aggregation operation on.
        :return: A DataFrame with aggregated data across the date range
        """

        # The columns which have win percents.
        percent_cols = ['GP', 'OH', 'GD', 'GIH', 'GND']

        # Calculate helper stats to recalculate value later.
        frame['ALSA SUM'] = frame['ALSA'] * frame['# Seen']
        frame['ATA SUM'] = frame['ATA'] * frame['# Picked']
        for col in percent_cols:
            frame[f'# {col} WINS'] = pd.to_numeric(frame[f'# {col}'] * frame[f'{col} WR'])

        # Take the expanded frame, and drop the dates.
        frame = frame.reset_index(level=0)
        frame = frame.drop('Date', axis=1)

        # Sum the frame by deck colours and cards.
        temp = frame.groupby(['Deck Colors', 'Name']).max()  # Used to preserve color and rarity.
        frame = frame.groupby(['Deck Colors', 'Name']).sum()
        frame['Color'] = temp['Color']
        frame['Rarity'] = temp['Rarity']

        # Re-calculate the stats based on the processing from above.
        frame['ALSA'] = frame['ALSA SUM'] / frame['# Seen']
        frame['ATA'] = frame['ATA SUM'] / frame['# Picked']
        for col in ['GP', 'OH', 'GD', 'GIH', 'GND']:
            frame[f'{col} WR'] = pd.to_numeric(frame[f'# {col} WINS'] / frame[f'# {col}'])
        frame['IWD'] = frame['GIH WR'] - frame['GND WR']

        # Trim the helper columns from the expanded frame.
        # TODO: Update this to contain the new information taken from Scryfall, and calculated from raw data.
        summed = frame[['# Seen', 'ALSA', '# Picked', 'ATA', '# GP', 'GP WR', '# OH', 'OH WR', '# GD', 'GD WR',
                        '# GIH', 'GIH WR', '# GND', 'GND WR', 'IWD', 'Color', 'Rarity']]
        idx = list(summed.index)
        idx.sort(key=self._compare_key)
        summed = summed.set_index([idx])

        return summed

    # TODO: Create aggregation functions for the other data structures.
    def aggregate_archetype_winrate_data(self, frame: pd.DataFrame) -> pd.DataFrame:  # pragma: no cover
        return frame

    def aggregate_archetype_summary_data(self, frame: pd.DataFrame) -> pd.DataFrame:  # pragma: no cover
        return frame
