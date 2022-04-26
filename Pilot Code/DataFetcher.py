"""
Running this program will update the ALL folders for the relevant set and format,
fetching the summary of data about the whole set.
"""
from data_fetching import DataLoader, LoadedData

TARGET_SET = 'NEO'
TARGET_FORMAT = 'TradDraft'


def json_handler():
    handler = DataLoader(TARGET_SET, TARGET_FORMAT)
    data = handler.get_day_data()
    print('Done!')
    return data


def get_set_data():
    fetcher = LoadedData(TARGET_SET, TARGET_FORMAT)
    fetcher.get_historic_data()
    print('Done!')


def get_summary_data():
    fetcher = LoadedData(TARGET_SET, TARGET_FORMAT)
    fetcher.get_summary_data()
    print('Done!')


def get_all_data():
    formats = ['PremierDraft', 'TradDraft', 'QuickDraft']
    for f in formats:
        fetcher = LoadedData(TARGET_SET, f)
        fetcher.get_historic_data()
    print('Done!')


if __name__ == '__main__':
    get_summary_data()
