from typing import Union

# Typing Consts
CARD_DATA = list[dict[str, Union[str, int, float]]]
META_DATA = list[dict[str, Union[str, int, bool]]]
WUBRG_CARD_DATA = dict[str, CARD_DATA]

# Set Consts
FORMAT_NICKNAME_DICT: dict[str, str] = {
    'PremierDraft': 'Bo1',
    'TradDraft': 'Bo3',
    'QuickDraft': 'Quick',
    'Sealed': 'Seal',
    'TradSealed': 'Bo3Seal',
    'DraftChallenge': 'Chal.',
}

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
