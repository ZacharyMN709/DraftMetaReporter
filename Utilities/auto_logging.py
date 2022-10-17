from typing import Optional, NoReturn
from enum import IntEnum, unique
import logging


@unique
class LogLvl(IntEnum):
    CRITICAL = 50
    ERROR = 40
    WARNING = 30
    SPARSE = 25
    INFO = 20
    VERBOSE = 15
    DEBUG = 10
    NOTSET = 0


# Taken from: https://stackoverflow.com/q/35804945#35804945
def addLoggingLevel(level_name: str, level_num: int, method_name: str) -> Optional[NoReturn]:
    """
    Comprehensively adds a new logging level to the `logging` module and the
    currently configured logging class.

    `level_name` becomes an attribute of the `logging` module with the value
    `level_num`. `method_name` becomes a convenience method for both `logging`
    itself and the class returned by `logging.getLoggerClass()` (usually just
    `logging.Logger`). If `method_name` is not specified, `level_name.lower()` is
    used.

    To avoid accidental clobbering of existing attributes, this method will
    raise an `AttributeError` if the level name is already an attribute of the
    `logging` module or if the method name is already present
    """
    if hasattr(logging, level_name):  # pragma: no cover
        raise AttributeError('{} already defined in logging module'.format(level_name))
    if hasattr(logging, method_name):  # pragma: no cover
        raise AttributeError('{} already defined in logging module'.format(method_name))
    if hasattr(logging.getLoggerClass(), method_name):  # pragma: no cover
        raise AttributeError('{} already defined in logger class'.format(method_name))

    # This method was inspired by the answers to Stack Overflow post
    # http://stackoverflow.com/q/2183233/2988730, especially
    # http://stackoverflow.com/a/13638084/2988730
    def logForLevel(self, message, *args, **kwargs):  # pragma: no cover
        if self.isEnabledFor(level_num):
            self._log(level_num, message, args, **kwargs)

    def logToRoot(message, *args, **kwargs):  # pragma: no cover
        logging.log(level_num, message, *args, **kwargs)

    logging.addLevelName(level_num, level_name)
    setattr(logging, level_name, level_num)
    setattr(logging.getLoggerClass(), method_name, logForLevel)
    setattr(logging, method_name, logToRoot)


def add_custom_levels() -> None:
    """
    Adds any missing log levels from LogLvl as values and functions to the logging module.
    """
    for lvl in LogLvl:
        try:
            addLoggingLevel(lvl.name.upper(), lvl, lvl.name.lower())
        except AttributeError:
            pass


def set_log_level(lvl: LogLvl, filename: Optional[str] = None, filemode: Optional[str] = 'a') -> LogLvl:
    fmt = '[%(asctime)s] %(levelname)-8s: %(message)s'
    datefmt = '%Y/%m/%d %H:%M:%S'
    logging.basicConfig(level=lvl, filename=filename, filemode=filemode, format=fmt, datefmt=datefmt, force=True)
    return lvl


def auto_log(lvl: LogLvl = LogLvl.VERBOSE) -> None:
    add_custom_levels()
    set_log_level(lvl)


# When this module is loaded, automatically add in the custom levels of logging.
add_custom_levels()
