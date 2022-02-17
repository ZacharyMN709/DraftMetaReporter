from datetime import date, time, datetime, timedelta

SETS = ["NEO", "VOW", "MID"]

FORMATS = ["PremierDraft", "TradDraft", "QuickDraft"]

SET_CONFIG = {
        "NEO" : {
            "PremierDraft": [(date(2022, 2, 10), date(2022, 4, 28))],
            "TradDraft": [(date(2022, 2, 10), date(2022, 4, 28))],
            "QuickDraft": [(date(2022, 2, 25), date(2022, 4, 28))]
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

class FormatMetadata:
    def __init__(self, SET, FORMAT):
        self._SET = SET
        self._FORMAT = FORMAT
        
        self._ACTIVE_PERIODS = SET_CONFIG[SET][FORMAT]
        self._START_DATE = self._ACTIVE_PERIODS[0][0]
        self._END_DATE = self._ACTIVE_PERIODS[-1][1]

        
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
