"""
Running this program will update the ALL folder for the relevant set and format,
fetching the summary of data about the whole set.
"""

from JSONHandler import JSONHandler

TRGT_SET = 'NEO'
TRGT_FMT = 'TradDraft'

fetcher = JSONHandler(TRGT_SET, TRGT_FMT, None)
fetcher.get_day_data()
