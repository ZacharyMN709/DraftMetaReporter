"""
Stores information about sets and format to gte data from, along with the dates to get data for.
Also stores the location of where card caches should be saved.
"""

import os

from core.utilities import load_json_file

# Locations of card caches.
SCRYFALL_CACHE_DIR: str = r'C:\Users\Zachary\Coding\GitHub\ScryfallData'
SCRYFALL_CACHE_FILE: str = r'oracle-cards.json'
SCRYFALL_CACHE_FILE_ARENA: str = r'oracle-cards-arena.json'

# Game Format Defaults and Data
SETS: list[str] = ["MKM", "LCI", "WOE", "LTR", "MOM", "SIR", "ONE", "BRO", "DMU", "SNC", "NEO", "VOW", "MID"]

SET_EXTRAS: dict[str, list[str]] = {
    "MKM": [],
    "LCI": [],
    "WOE": ["WOT"],
    "LTR": [],
    "MOM": ["MUL"],
    "SIR": ["SIS"],
    "ONE": [],
    "BRO": ["BRR"],
    "DMU": [],
    "SNC": [],
    "NEO": [],
    "VOW": [],
    "MID": [],
}

FORMATS: list[str] = ["PremierDraft", "TradDraft"]

# Location of event calendar data. Sourced from https://mtgarena.pro/mtga-event-calendar/,
#  and populated into json using GenerateEventCalendar.py
__cur_dir = os.path.split(__file__)[0]
EVENT_CALENDAR_JSON = r'event_calendar.json'

SET_CONFIG: dict[str, dict[str, list[tuple[str, str]]]] = load_json_file(__cur_dir, EVENT_CALENDAR_JSON)
