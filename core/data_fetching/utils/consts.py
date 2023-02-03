from typing import Union, Optional
from core.utilities import invert_dict

# region Colour Count Mappings
# TODO: Tidy this up a little.
# Used for graphing
COLOR_COUNT_MAP: dict[str, int] = {
    "Mono-Color": 1,
    "Two-Color": 2,
    "Three-Color": 3,
    "Four-Color": 4,
    "Five-Color": 5,
    "All Decks": None
}

COLOR_COUNT_SHORTHAND_MAP: dict[str, str] = {
    "All Decks": "ALL",
    "Mono-Color": "1C",
    "Two-Color": "2C",
    "Three-Color": "3C",
    "Four-Color": "4C",
    "Five-Color": "5C"
}

COLOR_COUNT_SHORTHAND: list[str] = [COLOR_COUNT_SHORTHAND_MAP[key] for key in COLOR_COUNT_SHORTHAND_MAP]

COLOR_COUNT_REVERSE_MAP: dict[int, str] = {
    0: "All Decks",
    1: "Mono-Color",
    2: "Two-Color",
    3: "Three-Color",
    4: "Four-Color",
    5: "Five-Color",
    None: "All Decks"
}
# endregion Colour Count Mappings

# Typing Consts
CARD_DATA = list[dict[str, Union[str, int, float]]]
META_DATA = list[dict[str, Union[str, int, bool]]]
WUBRG_CARD_DATA = dict[str, CARD_DATA]

# Set Consts
# noinspection SpellCheckingInspection
FORMAT_NICKNAME_DICT: dict[str, str] = {
    'PremierDraft': 'BO1',
    'TradDraft': 'BO3',
    'QuickDraft': 'QD',
    'Sealed': 'SBO1',
    'TradSealed': 'SBO3',
    'DraftChallenge': 'Chal.',
}

# region Frame Column Consts
STAT_NAME_DICT: dict[str, str] = {
    "name": "Name",
    "color": "Color",
    "rarity": "Rarity",
    "seen_count": "# Seen",
    "avg_seen": "ALSA",
    "pick_count": "# Picked",
    "avg_pick": "ATA",
    "game_count": "# GP",
    "win_rate": "GP WR",
    "opening_hand_game_count": "# OH",
    "opening_hand_win_rate": "OH WR",
    "drawn_game_count": "# GD",
    "drawn_win_rate": "GD WR",
    "ever_drawn_game_count": "# GIH",
    "ever_drawn_win_rate": "GIH WR",
    "never_drawn_game_count": "# GND",
    "never_drawn_win_rate": "GND WR",
    "drawn_improvement_win_rate": "IWD"
}

META_COLS_ALIAS_DICT: dict[str, str] = {
    "is_summary": "is_summary",
    "color_name": "Color Name",
    "wins": "Wins",
    "games": "Games",
}

STAT_FORMAT_STRINGS: dict[str, str] = {
    "Name": "`{:<20}`",
    "Color": "`{:^6}`",
    "Rarity": "`{:^6}`",
    "# Seen": "`{:>6.0f}`",
    "ALSA": "`{:^6.2f}`",
    "# Picked": "`{:>6.0f}`",
    "ATA": "`{:^6.2f}`",
    "# GP": "`{:>6.0f}`",
    "GP WR": "`{:5.2f}%`",
    "# OH": "`{:>6.0f}`",
    "OH WR": "`{:5.2f}%`",
    "# GD": "`{:>6.0f}`",
    "GD WR": "`{:5.2f}%`",
    "# GIH": "`{:>6.0f}`",
    "GIH WR": "`{:5.2f}%`",
    "# GND": "`{:>6.0f}`",
    "GND WR": "`{:5.2f}%`",
    "IWD": "`{:5.2f}%`"
}

PERCENT_COLUMNS: list[str] = ["GP WR", "OH WR", "GD WR", "GIH WR", "GND WR", "IWD"]

STAT_COL_NAMES: list[str] = ['# Seen', 'ALSA', '# Picked', 'ATA', '# GP', 'GP WR', 'GP GW',
                             '# OH', 'OH WR', 'OH GW', '# GD', 'GD WR', 'GD GW',
                             '# GIH', 'GIH WR', 'GIH GW', '# GND', 'GND WR', 'GND GW', 'IWD']

SHARED_COL_NAMES: list[str] = ['Rarity', 'Color']

CARD_INFO_COL_NAMES: list[str] = ['Cast Color', 'CMC', 'Type Line', 'Supertypes', 'Types', 'Subtypes',
                                  'Power', 'Toughness']
# endregion Frame Column Consts

# region Tier Rank Consts
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
    (0, 5),
    (5, 17),
    (17, 27),
    (27, 36),
    (36, 45),
    (45, 57),
    (57, 68),
    (68, 76),
    (76, 85),
    (85, 90),
    (90, 95),
    (95, 99),
    (99, 100),
]
# endregion Tier Rank Consts
