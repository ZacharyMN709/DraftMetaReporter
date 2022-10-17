from datetime import date

# Web Request Defaults
TRIES: int = 5
FAIL_DELAY: int = 60
SUCCESS_DELAY: int = 1

# File Location Defaults
DATA_DIR_NAME: str = '17LandsData'
DATA_DIR_LOC: str = r'C:\Users\Zachary\Coding\GitHub'

# 17Lands Querying Defaults
DEFAULT_FORMAT: str = 'PremierDraft'
DEFAULT_DATE: date = date(2020, 1, 1)
