import pandas as pd

from WUBRG import get_color_identity, get_color_subsets
from game_metadata import SetMetadata

from data_fetching.utils.consts import FORMAT_NICKNAME_DICT
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
        self._compare_key = self._set_metadata.COMPARE_KEY

        self.load_summary = load_summary
        self.load_history = load_history

    def check_for_updates(self) -> None:  # pragma: no cover
        """Populates and updates all data properties, filling in missing data."""
        self.DATA.check_for_updates()

    def reload_data(self) -> None:  # pragma: no cover
        """Populates and updates all data properties, reloading all data."""
        self.DATA.reload_data()

    # TODO: Create a function which takes in common parameters for subsetting the frames, and converts them
    #  into a kwarg dict of slices.

    def deck_group_frame(self, name=None, date=None, summary=False) -> pd.DataFrame:
        """Returns a subset of the 'GROUPED_ARCHETYPE' data as a DataFrame."""
        if name is None: name = slice(None)
        if date is None: date = slice(None)

        if summary:
            return self.DATA.GROUPED_ARCHETYPE_SUMMARY_FRAME.loc(axis=0)[pd.IndexSlice[name]]
        else:
            return self.DATA.GROUPED_ARCHETYPE_HISTORY_FRAME.loc(axis=0)[pd.IndexSlice[date, name]]

    def deck_archetype_frame(self, deck_color=None, date=None, summary=False) -> pd.DataFrame:
        """Returns a subset of the 'SINGLE_ARCHETYPE' data as a DataFrame."""
        if deck_color is None: deck_color = slice(None)
        if isinstance(deck_color, str): deck_color = get_color_identity(deck_color)
        if date is None: date = slice(None)

        if summary:
            return self.DATA.SINGLE_ARCHETYPE_SUMMARY_FRAME.loc(axis=0)[pd.IndexSlice[deck_color]]
        else:
            return self.DATA.SINGLE_ARCHETYPE_HISTORY_FRAME.loc(axis=0)[pd.IndexSlice[date, deck_color]]

    def card_frame(self, name=None, deck_color=None, date=None, card_color=None, card_rarity=None,
                   summary=False) -> pd.DataFrame:
        """Returns a subset of the 'CARD' data as a DataFrame."""
        if name is None: name = slice(None)
        if deck_color is None: deck_color = slice(None)
        if date is None: date = slice(None)
        if isinstance(deck_color, str): deck_color = get_color_identity(deck_color)

        if summary:
            ret = self.DATA.CARD_SUMMARY_FRAME.loc(axis=0)[pd.IndexSlice[deck_color, name]]
        else:
            ret = self.DATA.CARD_HISTORY_FRAME.loc(axis=0)[pd.IndexSlice[date, deck_color, name]]

        if card_color:
            color_set = get_color_subsets(get_color_identity(card_color))
            ret = ret[ret['Color'].isin(list(color_set))]

        if card_rarity:
            ret = ret[ret['Rarity'].isin(list(card_rarity))]

        return ret

    # TODO: Figure out how to best parameterize this/what wrapper functions to have call this
    def compress_date_range_data(self, start_date: str, end_date: str, card_name: str = None) -> pd.DataFrame:
        """
        Summarizes card data over a provided set of time.
        :param start_date: The start date of the data to combine (inclusive)
        :param end_date: The end date of the data to combine (inclusive)
        :param card_name: The card name to isolate the data to.
        :return: A DataFrame with aggregated data over the given date range
        """

        # The columns which have win percents.
        percent_cols = ['GP', 'OH', 'GD', 'GIH', 'GND']

        # Get the relevant dates (and card)
        frame = self.card_frame(card_name, date=slice(start_date, end_date)).copy()

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
        summed = frame[
            ['# Seen', 'ALSA', '# Picked', 'ATA', '# GP', 'GP WR', '# OH', 'OH WR', '# GD', 'GD WR', '# GIH', 'GIH WR',
             '# GND', 'GND WR', 'IWD', 'Color', 'Rarity']]
        idx = list(summed.index)
        idx.sort(key=self._compare_key)
        summed = summed.set_index([idx])

        return summed
