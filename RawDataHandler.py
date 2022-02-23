import pandas as pd

import WUBRG
import consts
from RawDataFetcher import RawDataFetcher

class RawDataHandler:
    def __init__(self, SET, FORMAT):
        self._SET = SET
        self._FORMAT = FORMAT
        self._FETCHER = RawDataFetcher(SET, FORMAT)
        
        self._GROUPED_ARCHTYPE_HISTORY_FRAME = None
        self._SINGLE_ARCHTYPE_HISTORY_FRAME = None
        self._CARD_HISTORY_FRAME = None
        
        self._GROUPED_ARCHTYPE_SUMMARY_FRAME = None
        self._SINGLE_ARCHTYPE_SUMMARY_FRAME = None
        self._CARD_SUMMARY_FRAME = None
    
    
    @property
    def SET(self):
        """The draft set."""
        return self._SET
    
    @property
    def FORMAT(self):
        """The queue type."""
        return self._FORMAT
    
    
    @property
    def GROUPED_ARCHTYPE_HISTORY_FRAME(self):
        """The daily data about how decks, grouped by number of colours, performs."""
        if self._GROUPED_ARCHTYPE_HISTORY_FRAME is None:
            self.gen_hist()
        return self._GROUPED_ARCHTYPE_HISTORY_FRAME
    
    @property
    def SINGLE_ARCHTYPE_HISTORY_FRAME(self):
        """The daily data for each deck archetype."""
        if self._SINGLE_ARCHTYPE_HISTORY_FRAME is None:
            self.gen_hist()
        return self._SINGLE_ARCHTYPE_HISTORY_FRAME
    
    @property
    def CARD_HISTORY_FRAME(self):
        """The daily data for individual card performance."""
        if self._CARD_HISTORY_FRAME is None:
            self.gen_hist()
        return self._CARD_HISTORY_FRAME
    
    
    @property
    def GROUPED_ARCHTYPE_SUMMARY_FRAME(self):
        """The overall data, about how decks, grouped by number of colours, performs."""
        if self._GROUPED_ARCHTYPE_SUMMARY_FRAME is None:
            self.gen_summary()
        return self._GROUPED_ARCHTYPE_SUMMARY_FRAME
    
    @property
    def SINGLE_ARCHTYPE_SUMMARY_FRAME(self):
        """The overall data, for each deck archetype."""
        if self._SINGLE_ARCHTYPE_SUMMARY_FRAME is None:
            self.gen_summary()
        return self._SINGLE_ARCHTYPE_SUMMARY_FRAME
    
    @property
    def CARD_SUMMARY_FRAME(self):
        """The overall data, about individual card performance."""
        if self._CARD_SUMMARY_FRAME is None:
            self.gen_summary()
        return self._CARD_SUMMARY_FRAME
    
    
    def panadafy_card_dict(self, card_dict: dict) -> pd.DataFrame:
        """
        Turns a dictionary into a DataFrame, with some data cleaning applied.
        :param card_dict: The dictionary containing card data for a colour group
        :return: A DataFrame filled with the cleaned card data
        """
        frame = pd.DataFrame.from_dict(card_dict)
        frame = frame.rename(columns=consts.STAT_NAMES)

        # If there's no data, make a blank frame and return it.
        if len(card_dict) == 0:
            return frame

        frame = frame.set_index('Name')
        
        for col in ["GP WR", "OH WR", "GD WR", "GIH WR", "GND WR", "IWD"]:
            frame[col] = frame[col] * 100

        frame = frame.drop(['sideboard_game_count', 'sideboard_win_rate', 'url', 'url_back'], axis=1)
        frame['Rarity'] = frame['Rarity'].map(consts.RARITY_ALIASES)

        frame['# UGIH'] = frame['# GP'] - frame['# GND']
        frame['UGIH WR'] = (((frame['# GP'] * frame['GP WR']) - (frame['# GND'] * frame['GND WR'])) / frame['# UGIH'])
        
        column_names = ['# Seen', 'ALSA', '# Picked', 'ATA', '# GP', 'GP WR', '# OH', 'OH WR', '# GD', 'GD WR', '# GIH', 'GIH WR', '# UGIH', 'UGIH WR', '# GND', 'GND WR', 'IWD', 'Color', 'Rarity']
        frame = frame.reindex(columns=column_names)
        
        frame = frame.round(3)
        return frame
    
    def panadafy_meta_dict(self, meta_dict: dict) -> pd.DataFrame:
        """
        Turns a dictionary into a DataFrame, with some data cleaning applied.
        :param card_dict: The dictionary containing card data for a colour group
        :return: A DataFrame filled with the cleaned card data
        """
        frame = pd.DataFrame.from_dict(meta_dict)
        frame = frame.rename(columns=consts.META_COLS)

        # If there's no data, make a blank frame and return it.
        if len(meta_dict) == 0:
            return frame, frame.copy()
        
        frame['Name'] = frame['Color Name']
        frame = frame.set_index('Name')
        frame['Win %'] = round((frame['Wins'] / frame['Games']) * 100, 2)
        frame['Splash'] = frame['Color Name'].str.contains("Splash", case=False)
        frame['Colors'] = frame['Color Name'].map(lambda x: x.replace(' + Splash', ''))
        frame = frame[['Colors', 'Splash', 'Wins', 'Games', 'Win %', 'is_summary']]
        
        summary_frame = frame[frame['is_summary'] == True].copy()
        summary_frame = summary_frame.drop(['is_summary'], axis=1)
        summary_frame['Colors'] = summary_frame['Colors'].map(WUBRG.COLOR_COUNT_MAP)

        archetype_frame = frame[frame['is_summary'] == False].copy()
        archetype_frame = archetype_frame.drop(['is_summary'], axis=1)
        archetype_frame['Colors'] = archetype_frame['Colors'].map(lambda x: x[0: (x.find('(') if x.find('(') != -1 else len(x))].strip())
        archetype_frame['Colors'] = archetype_frame['Colors'].map(lambda x: x.replace('Mono-', ''))
        archetype_frame['Colors'] = archetype_frame['Colors'].map(WUBRG.COLOR_ALIASES)
        archetype_frame['Name'] = archetype_frame['Colors']
        archetype_frame = archetype_frame.set_index('Name')

        return summary_frame, archetype_frame

        
    def gen_hist(self):
        """Populates and updates the three 'HISTORY' properties."""
        hist_meta, hist_card = self._FETCHER.get_set_data()
        if (not hist_meta) and (not hist_card):
            return
        
        grouped_arch_frame_dict = dict()
        single_arch_frame_dict = dict()
        card_frame_dict = dict()
        
        for date in hist_meta:
            grouped_arch_frame_dict[date], single_arch_frame_dict[date] = self.panadafy_meta_dict(hist_meta[date])
        grouped_arch_frame = pd.concat(grouped_arch_frame_dict, names=["Date", "Name"])
        single_arch_frame = pd.concat(single_arch_frame_dict, names=["Date", "Name"])
        
        for date in hist_card:
            color_dict = dict()
            for color in hist_card[date]:
                color_dict[color] = self.panadafy_card_dict(hist_card[date][color])
            card_frame_dict[date] = pd.concat(color_dict, names=["Deck Colors", "Name"])
        card_frame = pd.concat(card_frame_dict, names=["Date", "Deck Colors", "Name"])
            
        self._GROUPED_ARCHTYPE_HISTORY_FRAME = grouped_arch_frame
        self._SINGLE_ARCHTYPE_HISTORY_FRAME = single_arch_frame
        self._CARD_HISTORY_FRAME = card_frame

    def gen_summary(self):
        """Populates and updates the three 'SUMMARY' properties."""
        hist_meta, hist_card = self._FETCHER.get_summary_data()
        if (not hist_meta) and (not hist_card):
            return
        
        grouped_arch_frame, single_arch_frame = self.panadafy_meta_dict(hist_meta)

        color_dict = dict()
        for color in hist_card:
            color_dict[color] = self.panadafy_card_dict(hist_card[color])
        card_frame = pd.concat(color_dict, names=["Deck Colors", "Name"])
            
        self._GROUPED_ARCHTYPE_SUMMARY_FRAME = grouped_arch_frame
        self._SINGLE_ARCHTYPE_SUMMARY_FRAME = single_arch_frame
        self._CARD_SUMMARY_FRAME = card_frame
    
    def check_for_updates(self):
        """Populates and updates all data properties."""
        self.gen_hist()
        self.gen_summary()
