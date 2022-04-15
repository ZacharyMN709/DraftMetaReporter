import pandas as pd

from utils import consts, WUBRG


def panadafy_card_dict(card_dict: dict) -> pd.DataFrame:
    """
    Turns a dictionary into a DataFrame, with some data cleaning applied.
    :param card_dict: The dictionary containing card data for a colour group
    :return: A DataFrame filled with the cleaned card data
    """
    frame = pd.DataFrame.from_dict(card_dict)
    frame = frame.rename(columns=consts.STAT_NAMES)

    # If there's no data, make a blank frame and return it.
    if card_dict is None or len(card_dict) == 0:
        return frame

    frame = frame.set_index('Name')

    for col in ["GP WR", "OH WR", "GD WR", "GIH WR", "GND WR", "IWD"]:
        frame[col] = frame[col] * 100

    frame = frame.drop(['sideboard_game_count', 'sideboard_win_rate', 'url', 'url_back'], axis=1)
    frame['Rarity'] = frame['Rarity'].map(consts.RARITY_ALIASES)

    column_names = ['# Seen', 'ALSA', '# Picked', 'ATA', '# GP', 'GP WR', '# OH', 'OH WR', '# GD', 'GD WR', '# GIH',
                    'GIH WR', '# GND', 'GND WR', 'IWD', 'Color', 'Rarity']
    frame = frame.reindex(columns=column_names)

    frame = frame.round(3)
    return frame


def panadafy_meta_dict(meta_dict: dict) -> tuple[pd.DataFrame, pd.DataFrame]:
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
    frame = pd.DataFrame.from_dict(meta_dict)
    frame = frame.rename(columns=consts.META_COLS)

    frame['Name'] = frame['Color Name']
    frame = frame.set_index('Name')
    frame['Win %'] = round((frame['Wins'] / frame['Games']) * 100, 2)
    frame['Splash'] = frame['Color Name'].str.contains("Splash", case=False)
    frame['Colors'] = frame['Color Name'].map(lambda x: x.replace(' + Splash', ''))
    frame = frame[['Colors', 'Splash', 'Wins', 'Games', 'Win %', 'is_summary']]

    summary_frame = frame[frame['is_summary'] == True].copy()
    summary_frame = summary_frame.drop(['is_summary'], axis=1)
    summary_frame['Colors'] = summary_frame['Colors'].map(WUBRG.COLOR_COUNT_MAP)

    archetype_frame = frame[frame['is_summary'] == False].copy()
    archetype_frame = archetype_frame.drop(['is_summary'], axis=1)
    archetype_frame['Colors'] = archetype_frame['Colors'].map(
        lambda x: x[0: (x.find('(') if x.find('(') != -1 else len(x))].strip())
    archetype_frame['Colors'] = archetype_frame['Colors'].map(lambda x: x.replace('Mono-', ''))
    archetype_frame['Colors'] = archetype_frame['Colors'].map(WUBRG.COLOR_ALIASES)
    archetype_frame['Name'] = archetype_frame['Colors']
    archetype_frame = archetype_frame.set_index('Name')

    return summary_frame, archetype_frame