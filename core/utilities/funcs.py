"""
Hosts basic functions which can be useful throughout the application.

Data structure manipulation and json handling are the current focus.
"""

from typing import Any, Union, Optional, TypeVar
from os import path
import json
from itertools import chain

from core.utilities.auto_logging import logging

ENCODING = 'utf-8'

T = TypeVar('T')
T1 = TypeVar('T1')
T2 = TypeVar('T2')


def flatten_lists(lst: list[list[T]]) -> list[T]:
    return [item for sublist in lst for item in sublist]


def weave_lists(l1: list[T], l2: list[T]) -> list[T]:
    """Interweaves elements of two equal-length lists into one."""
    if len(l1) != len(l2):
        raise ValueError("List length must be equal!")
    return list(chain.from_iterable(zip(l1, l2)))


def invert_dict(d: dict[T1, T2]) -> dict[T2, T1]:
    return {v: k for k, v in d.items()}


def validate_json(json_str: str) -> bool:
    try:
        json.loads(json_str)
    except ValueError:
        return False
    return True


def load_json_file(folder: str, filename: str) -> Union[dict, list[dict], None]:
    """
    Loads and returns the data from a json file.
    :param folder: The folder the json file is in.
    :param filename: The name of the json file (including filetype).
    :return: An object containing the json data.
    """
    filepath = path.join(folder, filename)

    try:
        with open(filepath, 'r', encoding=ENCODING) as f:
            json_str = f.read()
            f.close()
            logging.verbose(f'File {filename} read successfully.')
            return json.loads(json_str)
    except Exception as ex:
        logging.error(f'Error reading json file {filename}')
        logging.error(ex)
        return None


def save_json_file(folder: str, filename: str, data: [dict, list[dict]], indent: Optional[int] = 4) -> bool:
    """
    Saves provided data into the specified json file.
    :param folder: The folder the json file is in.
    :param filename: The name of the json file (including filetype).
    :param data: The object to be saved as json.
    :param indent: The indenting to use for the json.
    :return: Whether the save operation was successful.
    """
    filepath = path.join(folder, filename)

    try:
        with open(filepath, 'w', encoding=ENCODING) as f:
            f.write(json.dumps(data, indent=indent))
            f.close()
        logging.verbose(f'File {filename} written to.')
        return True
    except Exception as ex:
        logging.error(f'Error writing to json file {filename}')
        logging.error(ex)
        return False


def reformat_json_file(folder: str, filename: str, indent: Optional[int] = 4) -> None:
    """
    Re-writes the json file in question, if it can be parsed, with the provided indents.
    :param folder: The folder the json file is in.
    :param filename: The name of the json file (including filetype).
    :param indent: The indenting to use for the json.
    """
    data = load_json_file(folder, filename)
    if data:
        save_json_file(folder, filename, data, indent=indent)
