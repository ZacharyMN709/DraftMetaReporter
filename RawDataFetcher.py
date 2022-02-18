from datetime import date, time, datetime, timedelta

import WUBRG
import consts
from JSONHandler import JSONHandler
from FormatMetadata import FormatMetadata

class RawDataFetcher:    
    def __init__(self, SET, FORMAT):
        self._SET = SET
        self._FORMAT = FORMAT
        self.FORMAT_METADATA = FormatMetadata(SET, FORMAT)
        
        self._META_DICT = dict()
        self._CARD_DICTS = dict()

        self._SUMMARY_META_DICT = dict()
        self._SUMMARY_CARD_DICTS = dict()

    
    @property
    def SET(self):
        """The draft set."""
        return self._SET
    
    @property
    def FORMAT(self):
        """The queue type."""
        return self._FORMAT


    @property
    def META_DICT(self):
        """The daily data for archetype performance."""
        if not self._META_DICT:
            self.get_set_data()
        return self._META_DICT
    
    @property
    def CARD_DICTS(self):
        """The daily data for card performance."""
        if not self._CARD_DICTS:
            self.get_set_data()
        return self._CARD_DICTS


    @property
    def SUMMARY_META_DICT(self):
        """The overall data for archetype performance."""
        if not self._SUMMARY_META_DICT:
            self.get_summary_data()
        return self._SUMMARY_META_DICT
    
    @property
    def SUMMARY_CARD_DICTS(self):
        """The overall data for card performance."""
        if not self._SUMMARY_CARD_DICTS:
            self.get_summary_data()
        return self._SUMMARY_CARD_DICTS


    def get_day_data(self, check_date):
        """
        Gets all of the data for a given day, for the object's set and format.
        If the data does not exist locally, it will be fetched from 17Lands and saved locally.
        :param check_date: The date to get the data for
        :return: A tuple of dictionaries filled with the archetype data and card data
        """
        loader = JSONHandler(self.SET, self.FORMAT, check_date)
        str_date = str(check_date)
        print(f'Getting data for {self.SET} {self.FORMAT}, date: {str_date}')
        card_dict, meta_dict = loader.get_day_data()
        
        self._META_DICT[str_date] = meta_dict
        self._CARD_DICTS[str_date] = {color: card_dict[color] for color in card_dict}
            
        return meta_dict, card_dict

    def get_set_data(self):
        """
        Gets all of the data by day for the set and format.
        If any data does not exist locally, it will be fetched from 17Lands and saved locally.
        :return: A tuple of dictionaries filled with the archetype data and card data
        """
        check_date = self.FORMAT_METADATA.START_DATE

        run = True        
        while(run):
            if self.FORMAT_METADATA.is_active(check_date):
                self.get_day_data(check_date)
            check_date += timedelta(days=1)
            utc_check_date = datetime.combine(check_date, time(2, 0))
            run = utc_check_date < RawDataFetcher.get_prev_site_update_time()
    
        return self._META_DICT, self._CARD_DICTS
    
    def get_summary_data(self):
        """
        Gets the aggregated data for the set and format
        Depending on the age of the data, it will be updated automatically.
        :return: A tuple of dictionaries filled with the archetype data and card data
        """
        loader = JSONHandler(self.SET, self.FORMAT, None)
        update = loader.get_last_write_time() < RawDataFetcher.get_prev_site_update_time()
        print(f'Getting overall data for {self.SET} {self.FORMAT}')
        card_dict, meta_dict = loader.get_day_data(overwrite=update)            
        return meta_dict, card_dict


    def get_prev_site_update_time():
        utc = datetime.utcnow()
        dt = datetime.combine(date(utc.year, utc.month, utc.day), time(2, 0))
        if dt > utc:
            dt -= timedelta(days=1)
        return dt

    def get_next_site_update_time():
        return RawDataFetcher.get_prev_site_update_time() + timedelta(days=1)
