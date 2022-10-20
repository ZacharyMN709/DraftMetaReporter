"""
Provides typing when dealing with colours as parameters and return values.
"""

from typing import Literal, Union

# TODO: Consider using this for stricter handling of color strings.
COLOR_IDENTITY = Literal[
    '', 'W', 'U', 'B', 'R', 'G',
    'WU', 'WB', 'WR', 'WG', 'UB', 'UR', 'UG', 'BR', 'BG', 'RG',
    'WUB', 'WUR', 'WUG', 'WBR', 'WBG', 'WRG', 'UBR', 'UBG', 'URG', 'BRG',
    'WUBR', 'WUBG', 'WURG', 'WBRG', 'UBRG', 'WUBRG'
]

# TODO: See if there's a way to define a color string as a type.
COLOR_STRING = Literal['']

COLOR_ALIAS = Literal[
    'Any', '',
    'White', 'Blue', 'Black', 'Red', 'Green',
    'Azorius', 'Dimir', 'Rakdos', 'Gruul', 'Selesnya',
    'Orzhov', 'Golgari', 'Simic', 'Izzet', 'Boros',
    'Jeskai', 'Sultai', 'Mardu', 'Temur', 'Abzan',
    'Esper', 'Grixis', 'Jund', 'Naya', 'Bant',
    'Non-G', 'Non-R', 'Non-B', 'Non-U', 'Non-W',
    'WUBRG', 'All',
]

COLOR_ALIAS_EXTENDED = Literal[
    None, 'None',
    'Mono-White', 'Mono-Blue', 'Mono-Black', 'Mono-Red', 'Mono-Green',
    'Silverquill', 'Witherbloom', 'Quandrix', 'Prismari', 'Lorehold',
    'Raugrin', 'Zagoth', 'Savai', 'Ketria', 'Indatha',
    'Obscura', 'Maestros', 'Riveteers', 'Cabaretti', 'Brokers',
    'Yore', 'Witch', 'Ink', 'Dune', 'Glint',
    '5-Color', 'Five-Color',
]

COLOR_ALIAS_ALL = Union[COLOR_ALIAS, COLOR_ALIAS_EXTENDED]

VALID_COLOR_VALUE = Union[COLOR_ALIAS_ALL, COLOR_STRING]
