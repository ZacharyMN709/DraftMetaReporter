from typing import Optional
from enum import IntEnum, unique


# https://docs.python.org/3/howto/logging.html#advanced-logging-tutorial

@unique
class Flags(IntEnum):
    NONE = 0
    ERROR = 1
    KEY = 2
    DEFAULT = 3
    VERBOSE = 4
    DEBUG = 5


class Logger:  # pragma: no cover
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



def add_custom_levels() -> None:
    """
    Adds the VERBOSE (15) and SPARSE (15) log levels and functions to the logging module.
    """

    # Taken from: https://stackoverflow.com/q/35804945#35804945
    def addLoggingLevel(level_name: str, level_num: int, method_name: str = None):
        """
        Comprehensively adds a new logging level to the `logging` module and the
        currently configured logging class.

        `level_name` becomes an attribute of the `logging` module with the value
        `level_num`. `method_name` becomes a convenience method for both `logging`
        itself and the class returned by `logging.getLoggerClass()` (usually just
        `logging.Logger`). If `method_name` is not specified, `level_name.lower()` is
        used.

        To avoid accidental clobberings of existing attributes, this method will
        raise an `AttributeError` if the level name is already an attribute of the
        `logging` module or if the method name is already present
        """
        if not method_name:
            method_name = level_name.lower()

        if hasattr(logging, level_name):
            raise AttributeError('{} already defined in logging module'.format(level_name))
        if hasattr(logging, method_name):
            raise AttributeError('{} already defined in logging module'.format(method_name))
        if hasattr(logging.getLoggerClass(), method_name):
            raise AttributeError('{} already defined in logger class'.format(method_name))

        # This method was inspired by the answers to Stack Overflow post
        # http://stackoverflow.com/q/2183233/2988730, especially
        # http://stackoverflow.com/a/13638084/2988730
        def logForLevel(self, message, *args, **kwargs):
            if self.isEnabledFor(level_num):
                self._log(level_num, message, args, **kwargs)

        def logToRoot(message, *args, **kwargs):
            logging.log(level_num, message, *args, **kwargs)

        logging.addLevelName(level_num, level_name)
        setattr(logging, level_name, level_num)
        setattr(logging.getLoggerClass(), method_name, logForLevel)
        setattr(logging, method_name, logToRoot)

    addLoggingLevel('SPARSE', 25, 'sparse')
    addLoggingLevel('VERBOSE', 15, 'verbose')


def set_log_level(lvl: int, filename: Optional[str] = None, filemode: Optional[str] = 'a'):
    fmt = '[%(asctime)s] %(levelname)-8s: %(message)s'
    datefmt = '%Y/%m/%d %H:%M:%S'
    logging.basicConfig(level=lvl, filename=filename, filemode=filemode, format=fmt, datefmt=datefmt)


def auto_log():
    add_custom_levels()
    set_log_level(logging.VERBOSE)


if __name__ == "__main__":
    import logging

    #logger = logging.getLogger('simple_example')
    #logger.setLevel(logging.DEBUG)

    set_log_level(logging.DEBUG)

    logging.debug('debug message')
    logging.info('info message')
    logging.warning('warn message')
    logging.sparse('sparse message')
    logging.error('error message')
    logging.verbose('verbose message')
    logging.critical('critical message')

