from typing import Literal


# TODO: Consider using this for stricter handling of color strings.
COLOR_STRING = Literal[
    '', 'W', 'U', 'B', 'R', 'G',
    'WU', 'WB', 'WR', 'WG', 'UB', 'UR', 'UG', 'BR', 'BG', 'RG',
    'WUB', 'WUR', 'WUG', 'WBR', 'WBG', 'WRG', 'UBR', 'UBG', 'URG', 'BRG',
    'WUBR', 'WUBG', 'WURG', 'WBRG', 'UBRG', 'WUBRG'
]
