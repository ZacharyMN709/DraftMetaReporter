from functools import cmp_to_key
import pandas as pd

from utils import consts, WUBRG

from RawDataHandler import RawDataHandler


class FramedData:
    def __init__(self, SET, FORMAT):
        self._SET = SET
        self._FORMAT = FORMAT
        self._DATA = RawDataHandler(SET, FORMAT)

    @property
    def SET(self):
        """The draft set."""
        return self._SET

    @property
    def FULL_SET(self):
        """The full name of the draft set."""
        # TODO: Have this information be pulled from somewhere
        return self._SET

    @property
    def FORMAT(self):
        """The format type."""
        return self._FORMAT

    @property
    def SHORT_FORMAT(self):
        """The shorthand of the format type."""
        return consts.FORMAT_NICKNAMES[self._FORMAT].upper()

    @property
    def DATA(self):
        """The object which contains the data about the set and format."""
        return self._DATA

    @property
    def FUNCS(self):
        """A helper object which contains convenience functions for plotting and subsetting."""
        return self._FUNCS

    def check_for_updates(self):
        """Populates and updates all data properties, filling in missing data."""
        self._DATA.check_for_updates()

    def reload_data(self):
        """Populates and updates all data properties, reloading all data."""
        self._DATA.reload_data()

    def deck_group_frame(self, name=None, date=None, summary=False):
        """Returns a subset of the 'GROUPED_ARCHETYPE' data as a DataFrame."""
        if name is None: name = slice(None)
        if date is None: date = slice(None)

        if summary:
            return self.DATA.GROUPED_ARCHETYPE_SUMMARY_FRAME.loc(axis=0)[pd.IndexSlice[name]]
        else:
            return self.DATA.GROUPED_ARCHETYPE_HISTORY_FRAME.loc(axis=0)[pd.IndexSlice[date, name]]

    def deck_archetype_frame(self, deck_color=None, date=None, summary=False):
        """Returns a subset of the 'SINGLE_ARCHETYPE' data as a DataFrame."""
        if deck_color is None: deck_color = slice(None)
        if isinstance(deck_color, str): deck_color = WUBRG.get_color_identity(deck_color)
        if date is None: date = slice(None)

        if summary:
            return self.DATA.SINGLE_ARCHETYPE_SUMMARY_FRAME.loc(axis=0)[pd.IndexSlice[deck_color]]
        else:
            return self.DATA.SINGLE_ARCHETYPE_HISTORY_FRAME.loc(axis=0)[pd.IndexSlice[date, deck_color]]

    def card_frame(self, name=None, deck_color=None, date=None, card_color=None, card_rarity=None, summary=False):
        """Returns a subset of the 'CARD' data as a DataFrame."""
        if name is None: name = slice(None)
        if deck_color is None: deck_color = slice(None)
        if date is None: date = slice(None)
        if isinstance(deck_color, str): deck_color = WUBRG.get_color_identity(deck_color)

        if summary:
            ret = self.DATA.CARD_SUMMARY_FRAME.loc(axis=0)[pd.IndexSlice[deck_color, name]]
        else:
            ret = self.DATA.CARD_HISTORY_FRAME.loc(axis=0)[pd.IndexSlice[date, deck_color, name]]

        if card_color:
            color_set = WUBRG.get_color_subsets(WUBRG.get_color_identity(card_color))
            ret = ret[ret['Color'].isin(list(color_set))]

        if card_rarity:
            ret = ret[ret['Rarity'].isin(list(card_rarity))]

        return ret

    # TODO: Figure out how to best parameterize this/what wrapper functions to have call this
    def compress_date_range_data(self, start_date, end_date, card_name=None):
        """Summarizes card data over a provided set of time."""
        # Set up dictionaries for quicker sorting.
        COLOR_INDEXES = {WUBRG.COLOR_GROUPS[x]: x for x in range(0, len(WUBRG.COLOR_GROUPS))}
        # TODO: Have the cards be pulled from Scryfall via SetMetadata
        CARDS = list(self.card_frame(summary=True, deck_color='').reset_index(level=0).index)
        CARD_INDEXES = {CARDS[x]: x for x in range(0, len(CARDS))}

        # Creating a custom sorting algorithm
        def compare(pair1, pair2):
            # Convert the colors and names into numeric indexes
            color1, name1 = pair1
            col_idx1 = COLOR_INDEXES[color1]
            name_idx1 = CARD_INDEXES[name1]
            color2, name2 = pair2
            col_idx2 = COLOR_INDEXES[color2]
            name_idx2 = CARD_INDEXES[name2]

            # Sort by deck colour than card number.
            if col_idx1 == col_idx2:
                if name_idx1 < name_idx2:
                    return -1
                else:
                    return 1
            if col_idx1 < col_idx2:
                return -1
            else:
                return 1

        compare_key = cmp_to_key(compare)

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
        idx.sort(key=compare_key)
        summed = summed.set_index([idx])

        return summed
