"""
Running this program will update the ALL folder for the relevant set and format,
fetching the summary of data about the whole set.
"""
from JSONHandler import JSONHandler
from RawDataFetcher import RawDataFetcher

TRGT_SET = 'NEO'
TRGT_FMT = 'PremierDraft'


def get_set_data():
    fetcher = RawDataFetcher(TRGT_SET, TRGT_FMT)
    fetcher.get_set_data()
    print('Done!')


def get_all_data():
    formats = ['PremierDraft', 'TradDraft', 'QuickDraft']
    for f in formats:
        fetcher = RawDataFetcher(TRGT_SET, f)
        fetcher.get_set_data()
    print('Done!')


if __name__ == '__main__':
    get_all_data()


