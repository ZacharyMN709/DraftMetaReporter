from typing import Union, Optional
from os import path
import json

from Utilities.utils.settings import ENCODING
from Utilities.auto_logging import logging


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
    :param indent: The indeting to use for the json.
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
