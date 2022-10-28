"""
Provides typing when dealing with colours as parameters and return values.
"""

from typing import Literal, Union, Annotated


# region Colours
COLOR = Literal['W', 'U', 'B', 'R', 'G']

COLOR_IDENTITY = Literal[
    '', 'W', 'U', 'B', 'R', 'G',
    'WU', 'WB', 'WR', 'WG', 'UB', 'UR', 'UG', 'BR', 'BG', 'RG',
    'WUB', 'WUR', 'WUG', 'WBR', 'WBG', 'WRG', 'UBR', 'UBG', 'URG', 'BRG',
    'WUBR', 'WUBG', 'WURG', 'WBRG', 'UBRG', 'WUBRG'
]

COLOR_STRING = Annotated[str, "A string made up of only characters in 'WUBRG'"]

_SPLASH_ADD_ON = Annotated[str, "A string made up of 'wubrg' to denote splashes."]

SPLASH_STRING = Annotated[Union[COLOR_STRING, _SPLASH_ADD_ON],
                          "A string made up of only characters in 'WUBRG', and 'wubrg' to denote splashes."]
# endregion Colours

# region Aliases
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
    'Ardenvale', 'Vantress', 'Locthwain', 'Embereth', 'Garenbrig',
    'Auriok', 'Neurok', 'Moriok', 'Vulshok', 'Sylvok',
    'Ojutai', 'Silumgar', 'Kolaghan', 'Atarka', 'Dromoka',
    'Silverquill', 'Witherbloom', 'Quandrix', 'Prismari', 'Lorehold',
    'Raugrin', 'Zagoth', 'Savai', 'Ketria', 'Indatha',
    'Numot', 'Vorosh', 'Oros', 'Intet', 'Teneb',
    'Raka', 'Ana', 'Dega', 'Ceta', 'Necra',
    'Obscura', 'Maestros', 'Riveteers', 'Cabaretti', 'Brokers',
    'Yore', 'Witch', 'Ink', 'Dune', 'Glint',
    'Artifice', 'Growth', 'Altruism', 'Aggression', 'Chaos',
    '5-Color', 'Five-Color',
]

COLOR_ALIAS_ALL = Union[COLOR_ALIAS, COLOR_ALIAS_EXTENDED]
# endregion Aliases

# region Misc
VALID_COLOR_VALUE = Union[COLOR_ALIAS_ALL, COLOR_STRING]

FORMATTED_MANA_SYMBOL = Annotated[str, "Mana symbols wrapped with {}"]

MANA_SYMBOL = Annotated[str, "Mana symbols without any embellishments"]
# endregion Misc
