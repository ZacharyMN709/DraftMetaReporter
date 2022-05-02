import pandas as pd

from WUBRG import COLOR_ALIASES, get_color_identity
from WUBRG.consts import COLOR_COUNT_MAP

from data_fetching.utils.consts import RARITY_ALIAS_DICT, STAT_NAME_DICT, META_COLS_ALIAS_DICT, \
    STAT_COL_NAMES, SHARED_COL_NAMES, CARD_INFO_COL_NAMES
from game_metadata import Card


def gen_card_frame(card_dict: list[dict[str, object]]) -> pd.DataFrame:
    """
    Turns a dictionary into a DataFrame, with some data cleaning applied.
    :param card_dict: The dictionary containing card data for a colour group
    :return: A DataFrame filled with the cleaned card data
    """
    frame = pd.DataFrame(card_dict)
    frame = frame.rename(columns=STAT_NAME_DICT)

    # If there's no data, make a blank frame and return it.
    if card_dict is None or len(card_dict) == 0:
        return frame

    frame = frame.set_index('Name')

    for col in ["GP WR", "OH WR", "GD WR", "GIH WR", "GND WR", "IWD"]:
        frame[col] = frame[col] * 100

    frame = frame.drop(['sideboard_game_count', 'sideboard_win_rate', 'url', 'url_back'], axis=1)
    frame['Rarity'] = frame['Rarity'].map(RARITY_ALIAS_DICT)

    column_names = STAT_COL_NAMES + SHARED_COL_NAMES
    frame = frame.reindex(columns=column_names)

    frame = frame.round(3)
    return frame


def append_card_info(frame: pd.DataFrame, card_dict: dict[str, Card]) -> pd.DataFrame:
    """
    Appends card information to an existing frame to help with sorting.
    :param frame: The pandas frame which contains the card performance data.
    :param card_dict: The dictionary of card names and card objects.
    :return: A DataFrame with the card information attached.
    """
    frame['Cast Color'] = [get_color_identity(card_dict[card_name].MANA_COST) for card_name in frame.index]
    frame['CMC'] = [card_dict[card_name].CMC for card_name in frame.index]
    frame['Type Line'] = [card_dict[card_name].TYPE_LINE for card_name in frame.index]
    frame['Supertypes'] = [card_dict[card_name].SUPERTYPES for card_name in frame.index]
    frame['Types'] = [card_dict[card_name].TYPES for card_name in frame.index]
    frame['Subtypes'] = [card_dict[card_name].SUBTYPES for card_name in frame.index]
    frame['Power'] = [card_dict[card_name].POW for card_name in frame.index]
    frame['Toughness'] = [card_dict[card_name].TOU for card_name in frame.index]

    column_names = STAT_COL_NAMES + SHARED_COL_NAMES + CARD_INFO_COL_NAMES
    frame = frame.reindex(columns=column_names)
    return frame


def gen_meta_frame(meta_dict: list[dict[str, object]]) -> tuple[pd.DataFrame, pd.DataFrame]:
    """
    Turns a dictionary into a DataFrame, with some data cleaning applied.
    :param meta_dict: The dictionary containing data on the metagame.
    :return: A DataFrame filled with the cleaned card data
    """
    # If there's no (meaningful) data, make a blank frame and return it.
    if meta_dict is None or len(meta_dict) <= 1:
        frame = pd.DataFrame(columns=['Name', 'Colors', 'Splash', 'Wins', 'Games', 'Win %'])
        frame = frame.set_index('Name')
        return frame, frame.copy()

    # Otherwise, load in the data and split it into summaries and archetypes.
    frame = pd.DataFrame(meta_dict)
    frame = frame.rename(columns=META_COLS_ALIAS_DICT)

    frame['Name'] = frame['Color Name']
    frame = frame.set_index('Name')
    frame['Win %'] = round((frame['Wins'] / frame['Games']) * 100, 2)
    frame['Splash'] = frame['Color Name'].str.contains("Splash", case=False)
    frame['Colors'] = frame['Color Name'].map(lambda x: x.replace(' + Splash', ''))
    frame = frame[['Colors', 'Splash', 'Wins', 'Games', 'Win %', 'is_summary']]

    summary_frame = frame[frame['is_summary'] == True].copy()
    summary_frame = summary_frame.drop(['is_summary'], axis=1)
    summary_frame['Colors'] = summary_frame['Colors'].map(COLOR_COUNT_MAP)

    archetype_frame = frame[frame['is_summary'] == False].copy()
    archetype_frame = archetype_frame.drop(['is_summary'], axis=1)
    archetype_frame['Colors'] = archetype_frame['Colors'].map(
        lambda x: x[0: (x.find('(') if x.find('(') != -1 else len(x))].strip())
    archetype_frame['Colors'] = archetype_frame['Colors'].map(lambda x: x.replace('Mono-', ''))
    archetype_frame['Colors'] = archetype_frame['Colors'].map(COLOR_ALIASES)
    archetype_frame['Name'] = archetype_frame['Colors']
    archetype_frame = archetype_frame.set_index('Name')

    return summary_frame, archetype_frame
