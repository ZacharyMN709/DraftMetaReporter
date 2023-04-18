import logging

# Logging
LOG_LVL = logging.DEBUG
FMT = '[%(asctime)s] %(levelname)-8s: %(message)s'
DATE_FORMAT = '%Y/%m/%d %H:%M:%S'

# Add some logging, to better see what the requests are doing.
logging.basicConfig(level=LOG_LVL, format=FMT, datefmt=DATE_FORMAT, force=True)


# Caching
SETS = ['MOM', 'MUL']


# Tier List
TIER_LIST_ROOT = f'C:\\Users\\Zachary\\Coding\\GitHub\\17LandsData\\MOM\\Tiers\\'
TIER_LIST_FILE = 'MOM Gradings.xlsx'
TIER_LIST_LOC = TIER_LIST_ROOT + TIER_LIST_FILE


# Image Locations
IMAGE_FOLDER = 'C:\\Users\\Zachary\\Coding\\GitHub\\DraftMetaReporter\\Notebooks\\'
TEMP_LOC = IMAGE_FOLDER + 'temp.jpeg'
TEMP_FRONT_LOC = IMAGE_FOLDER + 'f.jpeg'
TEMP_BACK_LOC = IMAGE_FOLDER + 'b.jpeg'


# Image Sizing
SCALE = 0.9
BASE_HEIGHT = 3.24
BASE_WIDTH = 2.29
HEIGHT = BASE_HEIGHT * SCALE
WIDTH = BASE_WIDTH * SCALE


# Font Defaults
FONT_NAME = 'Calibri Light'
FONT_SIZE = 16
FONT_COLOR = 0x1F, 0x37, 0x63
