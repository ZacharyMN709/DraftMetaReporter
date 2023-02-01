from typing import Optional
from core.utilities import invert_dict

TIER_LIST_ROOT = "https://www.17lands.com/tier_list/"


tier_to_rank: dict[str, Optional[int]] = {
    "A+": 12,
    "A": 11,
    "A-": 10,
    "B+": 9,
    "B": 8,
    "B-": 7,
    "C+": 6,
    "C": 5,
    "C-": 4,
    "D+": 3,
    "D": 2,
    "D-": 1,
    "F": 0,
    "SB": None,
    "TBD": None
}


rank_to_tier: dict[Optional[int], str] = invert_dict(tier_to_rank)


range_map_vals: list[tuple[int, int]] = [
        (99, 100),
        (95, 99),
        (90, 95),
        (85, 90),
        (76, 85),
        (68, 76),
        (57, 68),
        (45, 57),
        (36, 45),
        (27, 36),
        (17, 27),
        (5, 17),
        (0, 5)
]


# region Colour Hexes
color_hexes: dict[str, str] = {
    'W': '#fefccc',
    'U': '#abdced',
    'B': '#c7bdb4',
    'R': '#f0a387',
    'G': '#96caa4',
}

rarity_hexes: dict[str, str] = {
    'C': '#d0d0d0',
    'U': '#576b73',
    'R': '#83703d',
    'M': '#b02911',
}

rank_hexes: list = [
    '#e67c73', '#eb8b70', '#ef9b6e', '#f3a96c', '#f7b96a',
    '#fbc768', '#ffd666', '#e3d16c', '#c7cd72', '#abc878',
    '#8fc47e', '#73bf84', '#57bb8a'
]


range_hexes: list = [
    '#ffffff', '#eef4fd', '#dee9fb', '#cddef9', '#bdd3f7',
    '#acc8f5', '#9cbdf3', '#8cb2f1', '#7ba7ef', '#6b9ced',
    '#5a91eb',  '#4a86e9', '#3a7ce8'
]
# endregion Colour Hexes
