import logging
from typing import Callable, Optional
import numpy as np
import pandas as pd
from scipy.stats import norm

from core.game_metadata import SetMetadata

from core.data_fetching.utils.consts import FORMAT_NICKNAME_DICT, rank_to_tier, range_map_vals
from core.data_fetching.utils.index_slice_helper import get_name_slice, get_color_slice, get_date_slice
from core.data_fetching.DataFramer import DataFramer


class FramedData:
    """
    Acts as a wrapper for DataFramer, adding some extended functionality in how data can bet accessed and handled.
    One of its primary features is the ability to compress data over a given range into a summary, allowing data to be
    examined over certain parts of a format (After week 2, first meta shift, under-drafted colour becomes good, etc.)
    """

    def __init__(self, set_code: str, format_name: str, load_summary: bool = True, load_history: bool = True):
        self._set_metadata = SetMetadata.get_metadata(set_code)
        self.SET: str = set_code
        self.SET_NAME: str = self._set_metadata.FULL_NAME
        self.FORMAT: str = format_name
        self.FORMAT_ALIAS: str = FORMAT_NICKNAME_DICT[self.FORMAT].upper()
        self.DATA: DataFramer = DataFramer(set_code, format_name, load_summary, load_history)
        self._compare_key: Callable = self._set_metadata.FRAME_ORDER_KEY

        self.load_summary: bool = load_summary
        self.load_history: bool = load_history

    def check_for_updates(self) -> None:  # pragma: no cover
        """Populates and updates all data properties, filling in missing data."""
        self.DATA.check_for_updates()

    def reload_data(self) -> None:  # pragma: no cover
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

    def get_stats_grades(self, deck_color: str = '') -> Optional[pd.DataFrame]:
        # Get the non-colour specific card stats, then normalize GIH WR to from 0-100 for each card.
        frame = self.card_frame(deck_color=deck_color, summary=True).copy()

        # Get all of the rows where GIH WR is non NaN, convert it to a float, cancelling if none exist.
        available_rows = frame[~frame['GIH WR'].isna()].copy()
        if len(available_rows) == 0:
            logging.warning(f"{self.SET}'s {self.FORMAT_ALIAS} Dataframe had no valid data.")
            return None
        available_gih = np.array(available_rows['GIH WR'], dtype=float)

        # Get the stats, and use it to normalize the data, assigning it back to the available rows.
        mu, std = norm.fit(available_gih)
        available_rows['Percentile'] = norm.cdf(available_gih, mu, std).round(4) * 100

        # Re-map the available rows back to the main frame by reindexing, making empty rows.
        available_rows = available_rows.reindex(frame.index, fill_value=None)
        frame['Percentile'] = available_rows['Percentile']

        # For each "Percentile", use a pre-defined mapping to assign that a tier, and in turn, a letter grade.
        range_map = [frame['Percentile'].between(start, end) for start, end in range_map_vals]
        frame['Tier'] = np.select(range_map, [i for i in range(0, len(range_map))], 0)
        frame['Rank'] = frame['Tier'].map(rank_to_tier)

        # Reset any ranks and tiers which weren't originally found.
        mask = frame['Percentile'].isna()
        frame.loc[mask, 'Tier'] = None
        frame.loc[mask, 'Rank'] = None
        return frame

    # region Dataframe Creation
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
    # endregion Dataframe Creation
