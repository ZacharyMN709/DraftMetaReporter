"""
Contains configuration for how to query websites.
"""

from datetime import date

# Web Request Defaults
TRIES: int = 5
FAIL_DELAY: int = 60
SUCCESS_DELAY: float = 0.2

# 17Lands Querying Defaults
DEFAULT_FORMAT: str = 'PremierDraft'
DEFAULT_DATE: date = date(2020, 1, 1)
