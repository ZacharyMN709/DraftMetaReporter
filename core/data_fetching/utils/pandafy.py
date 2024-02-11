from typing import Optional
import numpy as np
import pandas as pd
from scipy.stats import norm

from core.utilities import logging
from core.data_fetching.utils.consts import rank_to_tier, range_map_vals
from core.wubrg import ALIAS_MAP
from core.game_metadata import Card, RARITY_ALIASES

from core.data_fetching.utils.consts import STAT_NAME_DICT, META_COLS_ALIAS_DICT, \
    STAT_COL_NAMES, SHARED_COL_NAMES, CARD_INFO_COL_NAMES, COLOR_COUNT_MAP


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

    for name in ['GP', 'OH', 'GD', 'GIH', 'GND']:
        frame[f'{name} GW'] = (frame[f'# {name}'] * frame[f'{name} WR']).astype(int, errors='ignore')
        frame[f'{name} WR'] = frame[f'{name} WR'] * 100

    frame["IIO"] = frame["OH WR"] - frame["GIH WR"]
    frame["IWD"] = frame["GD WR"] - frame["GIH WR"]
    frame["IWS"] = frame["GIH WR"] - frame["GND WR"]
    frame = frame.drop(['url', 'url_back'], axis=1)
    frame['Rarity'] = frame['Rarity'].map(RARITY_ALIASES)

    column_names = STAT_COL_NAMES + SHARED_COL_NAMES
    frame = frame.reindex(columns=column_names)

    frame = frame.round(3)
    return frame


def get_stats_grades(frame) -> Optional[pd.DataFrame]:
    frame = _get_stats_grades(frame, 'OH')
    frame = _get_stats_grades(frame, 'GIH')
    frame = _get_stats_grades(frame, 'GD')
    return frame


def _get_stats_grades(frame, stat) -> Optional[pd.DataFrame]:
    key_col = f'{stat} WR'
    percentile_col = f'{stat} Percentile'
    tier_col = f'{stat} Tier'
    rank_col = f'{stat} Rank'

    # Get all the rows where GIH WR is non NaN, convert it to a float, cancelling if none exist.
    available_rows = frame[~frame[key_col].isna()]
    if len(available_rows) == 0:
        return frame

    # Filter by a minimum number of games, to prevent one win to skew data.
    filtered_rows = available_rows[available_rows['# GP'] >= round(available_rows['# GP'].max() * 0.005)]
    filtered_rows = filtered_rows.copy()

    # Get the stats, and use it to normalize the data, assigning it back to the available rows.
    available_gih = np.array(filtered_rows[key_col], dtype=float)
    mu, std = norm.fit(available_gih)
    filtered_rows[percentile_col] = norm.cdf(available_gih, mu, std).round(4) * 100

    # Re-map the available rows back to the main frame by reindexing, making empty rows.
    filtered_rows = filtered_rows.reindex(frame.index, fill_value=None)
    frame[percentile_col] = filtered_rows[percentile_col]

    # For each "Percentile", use a pre-defined mapping to assign that a tier, and in turn, a letter grade.
    range_map = [frame[percentile_col].between(start, end) for start, end in range_map_vals]
    frame[tier_col] = np.select(range_map, [i for i in range(0, len(range_map))], 0)
    frame[rank_col] = frame[tier_col].map(rank_to_tier)

    # Reset any ranks and tiers which weren't originally found.
    mask = frame[percentile_col].isna()
    frame.loc[mask, tier_col] = None
    frame.loc[mask, rank_col] = None
    return frame


def append_card_info(frame: pd.DataFrame, card_dict: dict[str, Card]) -> pd.DataFrame:
    """
    Appends card information to an existing frame to help with sorting.
    :param frame: The pandas frame which contains the card performance data.
    :param card_dict: The dictionary of card names and card objects.
    :return: A DataFrame with the card information attached.
    """
    # Get each card from the provided card dictionary, relying on the Card's fallback
    #  on an unknown name. This helps be forgiving about names, and patches spotty data
    #  which can come back from 17Lands, which originates in MTGA.
    card_list = list()
    for card_name in frame.index:
        try:
            card = card_dict[card_name]
        except KeyError:  # pragma: nocover
            card = Card.from_name(card_name)
        card_list.append(card)

    # TODO: This should be handled as a join.
    frame['Cast Color'] = [card.CAST_IDENTITY for card in card_list]
    frame['CMC'] = [card.CMC for card in card_list]
    frame['Type Line'] = [card.TYPE_LINE for card in card_list]
    frame['Supertypes'] = [card.SUPERTYPES for card in card_list]
    frame['Types'] = [card.TYPES for card in card_list]
    frame['Subtypes'] = [card.SUBTYPES for card in card_list]
    frame['Power'] = [card.POW for card in card_list]
    frame['Toughness'] = [card.TOU for card in card_list]

    # TODO: Make this re-indexing more dynamic.
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
    frame['Colors'] = frame['Color Name'].map(lambda x: x.replace(' + Splash', '').title())
    frame = frame[['Colors', 'Splash', 'Wins', 'Games', 'Win %', 'is_summary']]

    summary_frame = frame[frame['is_summary'] == True].copy()
    summary_frame = summary_frame.drop(['is_summary'], axis=1)
    summary_frame['Name'] = summary_frame['Colors']
    summary_frame['Colors'] = summary_frame['Colors'].map(COLOR_COUNT_MAP)
    summary_frame = summary_frame.set_index('Name')

    archetype_frame = frame[frame['is_summary'] == False].copy()
    archetype_frame = archetype_frame.drop(['is_summary'], axis=1)
    archetype_frame['Colors'] = archetype_frame['Colors'].map(
        lambda x: x[0: (x.find('(') if x.find('(') != -1 else len(x))].strip())
    archetype_frame['Colors'] = archetype_frame['Colors'].map(lambda x: x.replace('Mono-', ''))
    archetype_frame['Colors'] = archetype_frame['Colors'].map(ALIAS_MAP)
    archetype_frame['Name'] = archetype_frame['Colors']
    archetype_frame = archetype_frame.set_index('Name')

    return summary_frame, archetype_frame
