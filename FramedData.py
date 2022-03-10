import pandas as pd

from Logger import Logger
import WUBRG
from RawDataHandler import RawDataHandler

class FramedData:   
    def __init__(self, SET, FORMAT, LOGGER=None):
        self._SET = SET
        self._FORMAT = FORMAT
        if LOGGER is None:
            LOGGER = Logger(Logger.FLG.DEFAULT)
        self.LOGGER = LOGGER
        self._DATA = RawDataHandler(SET, FORMAT, self.LOGGER)
        
    
    @property
    def SET(self):
        """The draft set."""
        return self._SET
    
    @property
    def FORMAT(self):
        """The format type."""
        return self._FORMAT
    
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
        """Returns a subset of the 'GROUPED_ARCHTYPE' data as a DataFrame."""
        if name is None: name = slice(None)
        if date is None: date = slice(None)
        
        if summary:
            return self.DATA.GROUPED_ARCHTYPE_SUMMARY_FRAME.loc(axis=0)[pd.IndexSlice[name]]
        else:
            return self.DATA.GROUPED_ARCHTYPE_HISTORY_FRAME.loc(axis=0)[pd.IndexSlice[date, name]]
     
    def deck_archetype_frame(self, deck_color=None, date=None, summary=False):
        """Returns a subset of the 'SINGLE_ARCHTYPE' data as a DataFrame."""
        if deck_color is None: deck_color = slice(None)
        if type(deck_color) is str: deck_color = WUBRG.get_color_identity(deck_color)
        if date is None: date = slice(None)
            
        if summary:
            return self.DATA.SINGLE_ARCHTYPE_SUMMARY_FRAME.loc(axis=0)[pd.IndexSlice[deck_color]]
        else:
            return self.DATA.SINGLE_ARCHTYPE_HISTORY_FRAME.loc(axis=0)[pd.IndexSlice[date, deck_color]]
    
    def card_frame(self, name=None, deck_color=None, date=None, card_color=None, card_rarity=None, summary=False):
        """Returns a subset of the 'CARD' data as a DataFrame."""
        if name is None: name = slice(None)
        if deck_color is None: deck_color = slice(None)
        if date is None: date = slice(None)
        if type(deck_color) is str: deck_color = WUBRG.get_color_identity(deck_color)
        
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
