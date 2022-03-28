from datetime import date, time, datetime, timedelta

from CardManager import CardManager

SETS = ["NEO", "VOW", "MID"]

FORMATS = ["PremierDraft", "TradDraft", "QuickDraft"]

SET_CONFIG = {
        "NEO" : {
            "PremierDraft": [(date(2022, 2, 10), date(2022, 4, 28))],
            "TradDraft": [(date(2022, 2, 10), date(2022, 4, 28))],
            "QuickDraft": [(date(2022, 2, 25), date(2022, 3, 11)), (date(2022, 3, 26), date(2022, 4, 8))]
        },
        "VOW" : {
            "PremierDraft": [(date(2021, 11, 11), date(2022, 2, 10))],
            "TradDraft": [(date(2021, 11, 11), date(2022, 2, 10))],
            "QuickDraft": [(date(2021, 11, 26), date(2021, 12, 10)), (date(2021, 12, 24), date(2022, 1, 7))]
        },
        "MID" : {
            "PremierDraft": [(date(2021, 9, 16), date(2021, 11, 11))],
            "TradDraft": [(date(2021, 9, 16), date(2021, 11, 11))],
            "QuickDraft": [(date(2021, 10, 1), date(2021, 10, 15)), (date(2021, 10, 29), date(2022, 11, 12))]
        }
    }


class SetMetadata:
    METADATA = { s : dict() for s in SETS }


    def get_metadata(SET):
        ## TODO: Implement some checks so only valid sets are added.
        ## TODO: Make the check update along with added sets.
        if SET not in SetMetadata.METADATA or not SetMetadata.METADATA[SET]:
            SetMetadata.METADATA[SET] = SetMetadata(SET)
        return SetMetadata.METADATA[SET]

    
    def __init__(self, SET):       
        self._SET = SET
        self._CARD_DICT = CardManager.from_set(self.SET)
        
        
    @property
    def SET(self):
        """The draft set."""
        return self._SET     
    
    
    @property
    def RELEASE_DATE(self):
        """The (Arena) release date of the set's format."""
        return SET_CONFIG[self.SET]["PremierDraft"][0][0]


    @property
    def CARD_DICT(self):
        """The dicitionary of cards in the set"""
        return self._CARD_DICT
    

    @property
    def CARD_LIST(self):
        """The list of cards in the set"""
        return [self._CARD_DICT[name] for name in self._CARD_DICT]


    def find_card(self, card_name):
        """
        Looks for a card name in the list of cards for the set.
        :param card_name: The card name, simple or full. Must be an exact match. If 'NONE', today's date is used.
        :return: A Card object or None
        """
        if card_name in CardManager.REDIRECT:
            card_name = CardManager.REDIRECT[card_name]
        if card_name in self.CARD_DICT:
            return self.CARD_DICT[card_name]
        else:
            return None
    

class FormatMetadata:
    METADATA = { s : { f : dict() for f in FORMATS } for s in SETS }


    def get_metadata(SET, FORMAT):
        ## TODO: Implement some checks so only valid sets are added.
        ## TODO: Make the check update along with added sets.
        if SET not in FormatMetadata.METADATA or not FormatMetadata.METADATA[SET]:
            FormatMetadata.METADATA[SET] = dict()
        if FORMAT not in FormatMetadata.METADATA[SET] or not FormatMetadata.METADATA[SET][FORMAT]:
            FormatMetadata.METADATA[SET][FORMAT] = FormatMetadata(SET, FORMAT)
        return FormatMetadata.METADATA[SET][FORMAT]

    
    def __init__(self, SET, FORMAT):       
        self._SET = SET
        self._FORMAT = FORMAT
        
        self._ACTIVE_PERIODS = SET_CONFIG[SET][FORMAT]
        self._START_DATE = self._ACTIVE_PERIODS[0][0]
        self._END_DATE = self._ACTIVE_PERIODS[-1][1]

        self._SET_METADATA = SetMetadata.get_metadata(SET)

        
    @property
    def SET(self):
        """The draft set."""
        return self._SET     
    
    
    @property
    def FORMAT(self):
        """The format type."""
        return self._FORMAT
        
    
    @property
    def START_DATE(self):
        """The start date of the set's format."""
        return self._START_DATE

    
    @property
    def END_DATE(self):
        """The end date of the set's format."""
        return self._END_DATE


    @property
    def CARD_DICT(self):
        """The dicitionary of cards in the set"""
        return self._SET_METADATA.CARD_DICT
    

    @property
    def CARD_LIST(self):
        """The list of cards in the set"""
        return self._SET_METADATA.CARD_LIST


    def find_card(self, card_name):
        """
        Looks for a card name in the list of cards for the set.
        :param card_name: The card name, simple or full. Must be an exact match. If 'NONE', today's date is used.
        :return: A Card object or None
        """
        return self._SET_METADATA.find_card(card_name)

    
    def is_active(self, check_date=None):
        """
        Checks if the draft queue is active for a given date.
        :param card_dict: The date to check. If 'NONE', today's date is used.
        :return: A boolean
        """
        if check_date is None:
            check_date = date.today()
            
        active = False
        for time_period in self._ACTIVE_PERIODS:
            active = active or (time_period[0] <= check_date <= time_period[1])
        
        return active
    
    def get_active_days(self):
        """
        Gets the days where a draft queue was active.
        :return: A list of Date objects
        """
        active_days = list()
        
        for time_period in self._ACTIVE_PERIODS:
            start_date = time_period[0]
            active_days.append(start_date)
            new_date = start_date
            while (new_date < time_period[1]):
                new_date += timedelta(days=1)
                active_days.append(new_date)
        return active_days
     
