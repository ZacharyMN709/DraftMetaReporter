from enum import IntEnum, unique

@unique
class Flags(IntEnum):
    NONE = 0
    ERROR = 1
    KEY = 2
    DEFAULT = 3
    VERBOSE = 4
    DEBUG = 5


class Logger:
    FLG = Flags
    LOGGER = None
    
    def void(self, msg, lvl=1):
        pass

    def prt(self, msg, lvl=1):
        if lvl <= self.LOG_LVL:
            print(msg)

    def pfl(self, msg, lvl=1):
        if lvl <= self.LOG_LVL:
            #TODO: Output message to a file.
            pass

        
    def __init__(self, LOG_LVL, USE_TIMESTAMP=False):
        self.LOG_LVL = LOG_LVL
        #TODO: Implement timestamp prepender.
        self.log = self.prt




    @property
    def log(self):
        """Gets the logging function."""
        return self._log

    @log.setter
    def log(self, value):
        """Sets the logging function."""
        self._log = value
        
    
Logger.LOGGER = Logger(Flags.DEFAULT)

