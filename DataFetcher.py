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
    fetcher.get_summary_data()

def __main__():
    get_set_data()


