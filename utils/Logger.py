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
        if lvl <= self.log_lvl:
            print(msg)

    def pfl(self, msg, lvl=1):
        if lvl <= self.log_lvl:
            # TODO: Output message to a file.
            pass

    def __init__(self, log_lvl, use_timestamp=False):
        self.log_lvl = log_lvl
        # TODO: Implement timestamp prepender.
        self.log = self.prt

    @property
    def log(self):
        """Gets the logging function."""
        return self._log

    @log.setter
    def log(self, value):
        """Sets the logging function."""
        self._log = value


# TODO: Use a better way of handling logging.
Logger.LOGGER = Logger(Flags.DEFAULT)
