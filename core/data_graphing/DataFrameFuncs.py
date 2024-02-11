import pandas as pd
import numpy as np
import datetime
from functools import partial, wraps

from core.wubrg import get_color_identity
from core.wubrg import COLOR_PAIRS, COLOR_COMBINATIONS, get_color_subsets
from core.game_metadata import SetMetadata

from core.data_fetching.utils.consts import COLOR_COUNT_REVERSE_MAP, COLOR_COUNT_SHORTHAND_MAP, STAT_COL_NAMES
from core.data_fetching.utils import get_name_slice, get_color_slice, rarity_filter, card_color_filter, filter_frame
from core.data_fetching import FramedData

from core.data_graphing.utils.settings import ROLL
from core.data_graphing.utils.funcs import hyperlink_card_index, prettify_frame
from core.data_graphing.utils.color.plotting_config import DefaultPlotConfigs
from core.data_graphing.PlotterHelper import PlotterHelper


def auto_prettify(method):
    @wraps(method)
    def _wrapped_function(self, *method_args, **method_kwargs):
        frame = method(self, *method_args, **method_kwargs)
        if self.auto_prettify:
            styler = prettify_frame(frame)
            styler.format_index(formatter=self.hyperlink_card_index)
            return styler
        else:
            return frame
    return _wrapped_function


class DataFrameFuncs:
    def __init__(self, DATA, auto_prettify=False):
        self._DATA: FramedData = DATA
        self._COLOR_IDX = 0
        self.auto_prettify = auto_prettify
        self.hyperlink_card_index = partial(hyperlink_card_index, card_dict=self._DATA.SET_METADATA.CARD_DICT)

    @property
    def SET(self):
        """The draft set."""
        return self._DATA.SET

    @property
    def FULL_SET(self):
        """The full name of the draft set."""
        return self._DATA.FULL_SET

    @property
    def FORMAT(self):
        """The format type."""
        return self._DATA.FORMAT

    @property
    def SHORT_FORMAT(self):
        """The shorthand of the format type."""
        return self._DATA.FULL_FORMAT

    @property
    def DATA(self):
        """The object which contains the data about the set and format."""
        return self._DATA

    def check_for_updates(self):
        """Populates and updates all data properties, filling in missing data."""
        self._DATA.check_for_updates()

    def reload_data(self):
        """Populates and updates all data properties, reloading all data."""
        self._DATA.reload_data()

    def deck_group_frame(self, name=None, date=None, summary=False):
        """Returns a subset of the 'GROUPED_ARCHETYPE' data as a DataFrame."""
        return self.DATA.deck_group_frame(name, date, summary)

    def deck_archetype_frame(self, deck_color=None, date=None, summary=False):
        """Returns a subset of the 'SINGLE_ARCHETYPE' data as a DataFrame."""
        return self.DATA.deck_archetype_frame(deck_color, date, summary)

    def card_frame(self, name=None, deck_color=None, date=None, summary=False):
        """Returns a subset of the 'CARD' data as a DataFrame."""
        return self.DATA.card_frame(name, deck_color, date, summary)

    def compress_date_range_data(self, start_date, end_date, card_name=None):
        """Summarizes card data over a provided set of time."""
        return self.DATA.compress_date_range_data(start_date, end_date, card_name)

    # region ArchFuncs
    @staticmethod
    def _get_play_stat_frame(frame, col, roll=None, aggfunc=None):
        roll = roll or ROLL
        aggfunc = aggfunc or np.sum

        ret = frame[[col]]
        ret.reset_index(inplace=True, level=1)
        ret = ret.pivot_table(values=col, index=ret.index, columns='Name', dropna=False, aggfunc=aggfunc)
        ret = ret.rolling(window=roll, min_periods=1, center=True).mean()
        ret.columns.names = [col]
        return ret

    def _get_all_stat(self, stat, roll=None, aggfunc=None):
        archetypes = self._get_play_stat_frame(self._DATA.deck_archetype_frame(), stat, roll, aggfunc)
        archetypes = archetypes[[color for color in COLOR_COMBINATIONS if color in archetypes.columns]]

        groups = self._get_play_stat_frame(self._DATA.deck_group_frame(), stat, roll, aggfunc)
        groups.rename(columns=COLOR_COUNT_SHORTHAND_MAP, inplace=True)
        groups = groups[COLOR_COUNT_SHORTHAND_MAP.values()]

        return pd.concat([groups, archetypes], axis=1)

    def get_winrates(self, roll=None):
        wins = self._get_all_stat('Wins', roll, np.sum)
        games = self._get_all_stat('Games', roll, np.sum)
        frame = (wins / games) * 100
        frame.columns.names = ['Avg. Win %']
        return frame

    def get_playrates(self, num_colors=0, roll=None):
        # TODO: Remove num_colors, and handle bubbling changes from that.
        games = self._get_all_stat('Games', roll, np.sum)

        if num_colors == 0:
            frame = games.div(games['ALL'], axis='rows') * 100
            frame.columns.names = ['% of Decks']
            return frame

        true_name = COLOR_COUNT_REVERSE_MAP[num_colors].title()
        summ_id = COLOR_COUNT_SHORTHAND_MAP[true_name]

        frame = games.div(games[summ_id], axis='rows') * 100
        frame.columns.names = [f'% of {num_colors}C Decks']
        return frame

    def get_archetype_winrate_history(self, color_filter=None, roll=None, *, save=False):
        roll = roll or ROLL
        frame = self.get_winrates(roll)

        if isinstance(color_filter, str):
            # TODO: Make this more flexible.
            # col_filt = ['ALL', f'{len(color_filter)}C'] + [col for col in COLOR_PAIRS if color_filter in col]
            col_filt = ['ALL', '2C'] + [col for col in COLOR_PAIRS if color_filter in col]
            frame = frame[col_filt]
        elif isinstance(color_filter, list):
            frame = frame[color_filter]

        if save:
            PlotterHelper(self._DATA).frame_to_png(frame, "archetype_winrate_table.png")

        return frame

        # TODO: Implement a more generic version of this that takes in a list of deck colours to include as output.

    def get_archetype_playrate_history(self, color_filter=None, color_count=0, roll=None, *, save=False):
        roll = roll or ROLL

        frame = self.get_playrates(color_count, roll)

        if isinstance(color_filter, str):
            sub_filter = [color for color in COLOR_PAIRS if color_filter in color]
            frame = frame[sub_filter]
        if isinstance(color_filter, list):
            frame = frame[color_filter]

        if save:
            PlotterHelper(self._DATA).frame_to_png(frame, "archetype_playrate_table.png")

        return frame

    def plot_archetype_winrate_history(self, plot_config, roll=None, derivs=0, save=False):
        if roll is None: roll = ROLL
        color_filter = plot_config.column_list

        data = self.get_archetype_winrate_history(color_filter, roll)
        for _ in range(0, derivs):
            data = data.diff()
        data.index = [idx[5:] for idx in data.index]
        colors = str(color_filter)  # TODO: Make this cleverer at showing filter.

        plot_help = PlotterHelper(self._DATA, plot_config)
        fig, ax = plot_help.new_single_plot('Archetype Winrates', width=16, height=8)
        plot_help.accredit(y=0.02, x=0.51)
        plot_help.desc_note(colors=colors, roll=roll, y=0.94, x=0.51)

        plot_help.set_labels(x_label="Date", y_label="Win Rate")
        plot_help.set_data(data, color_filter)

        if save:
            plot_help.save_fig(f"{plot_config.file_name_prefix}_win_rates_{roll}day_avg.png", "Metagame")

    def plot_archetype_playrate_history(self, plot_config, color_count=0, roll=None, derivs=0, save=False):
        if roll is None: roll = ROLL
        color_filter = plot_config.column_list

        data = self.get_archetype_playrate_history(color_filter, color_count, roll)
        for _ in range(0, derivs):
            data = data.diff()
        data.index = [idx[5:] for idx in data.index]

        plot_help = PlotterHelper(self._DATA, plot_config)
        fig, ax = plot_help.new_single_plot('Archetype Playrates', width=16, height=8)
        plot_help.accredit(y=0.02, x=0.51)
        plot_help.desc_note(colors=color_filter, roll=roll, y=0.94, x=0.51)

        plot_help.set_labels(x_label="Date", y_label="Percent of Metagame")
        plot_help.set_data(data, color_filter)

        if save:
            plot_help.save_fig(f"{plot_config.file_name_prefix}_play_rates_{roll}day_avg.png", "Metagame")

    def card_relative_winrates(self, deck_colors=None, win_rate_col='GIH WR'):
        deck_colors = get_color_identity(deck_colors)

        # Get the relevant list of cards, and then trim it down to the relevant colours.
        sub_frame = self._DATA.DATA.CARD_HISTORY_FRAME.loc[
            slice(None), get_color_slice(deck_colors), get_name_slice(None)
        ]
        sub_frame = sub_frame.reset_index(level=1)
        if deck_colors:
            sub_frame = sub_frame[sub_frame['Cast Color'].isin(get_color_subsets(deck_colors))]

        # Get the win rates for the cards and average winrate of the archetype,
        # then re-center the card win rates with it.
        win_frame = self._get_play_stat_frame(sub_frame, win_rate_col, roll=1, aggfunc=np.mean)
        avg_frame = self.get_archetype_winrate_history(deck_colors)
        target_avg = deck_colors if deck_colors else 'ALL'
        ret_frame = win_frame.sub(avg_frame[target_avg], axis='rows').T

        # Get the games played from the subset of cards and use it to
        # re-weight the win rates per day, to calculate an accurate average.
        games_frame = self._get_play_stat_frame(sub_frame, '# GP', roll=1, aggfunc=np.mean).T
        ret_frame[f'AVG'] = (ret_frame * games_frame).sum(axis=1) / games_frame.sum(axis=1)
        ret_frame['# GP'] = games_frame.sum(axis=1)

        # Sort by most winning first.
        ret_frame = ret_frame.sort_values(f'AVG', ascending=False).T
        return ret_frame[::-1]
    # endregion ArchFuncs

    # region SingleCardFuncs
    def _shorten_data(self, card_name, roll, cols, colors=''):
        frame = self._DATA.card_frame(name=card_name, deck_color=colors)[cols]
        frame.index = [tup[0][5:] for tup in frame.index]
        rolling = frame.rolling(window=roll, min_periods=1, center=True).mean()
        return rolling

    def plot_card_summary(self, card_name, colors='', roll=None, plot_config=None):
        if roll is None: roll = ROLL
        plot_config = plot_config or DefaultPlotConfigs.STATS.plot_config
        rolling = self._shorten_data(card_name, roll, plot_config.column_list, colors=colors)
        if rolling.empty:
            print(
                f"""Could not find data for "{card_name}". Please make sure it is spelled correctly, or you are accessing the right set.""")
            return False

        plot_help = PlotterHelper(self._DATA, plot_config)
        # TODO: Better center the title.
        fig, ax = plot_help.new_quad_plot(card_name)
        plot_help.accredit(y=0.1)
        plot_help.desc_note(colors=colors, roll=roll, x=0.505)

        plot_help.set_labels(y_label="Win Percent", g_x=0, g_y=0)
        plot_help.set_data(rolling, ['GP WR', 'GIH WR', 'OH WR', 'GD WR'], g_x=0, g_y=0)

        plot_help.set_labels(y_label="Pick Number", g_x=0, g_y=1)
        plot_help.set_data(rolling, ['ALSA', 'ATA'], inv_y=True, g_x=0, g_y=1)

        plot_help.set_labels(x_label="Date", y_label="# of Games", g_x=1, g_y=0)
        plot_help.set_data(rolling, ['# GP', '# GIH', '# OH', '# GD'], g_x=1, g_y=0)

        plot_help.set_labels(x_label="Date", y_label="# of Cards", g_x=1, g_y=1)
        plot_help.set_data(rolling, ['# Seen', '# Picked'], g_x=1, g_y=1)

        if colors:
            plot_help.save_fig(f"pcs_{card_name}_{colors}.png", "Summary")
        else:
            plot_help.save_fig(f"pcs_{card_name}.png", "Summary")

        return True

    def plot_pick_stats(self, card_name, roll=None, plot_config=None):
        if roll is None: roll = ROLL
        plot_config = plot_config or DefaultPlotConfigs.STATS.plot_config
        taken_data = self._shorten_data(card_name, roll, ['ALSA', 'ATA'])
        if taken_data.empty:
            print(
                f"""Could not find data for "{card_name}". 
                Please make sure it is spelled correctly, or you are accessing the right set.""")
            return

        plot_help = PlotterHelper(self._DATA, plot_config)
        fig, ax = plot_help.new_single_plot(card_name)
        plot_help.accredit(y=-0.01)
        plot_help.desc_note(roll=roll, y=0.96)

        plot_help.set_labels(x_label="Date", y_label="Pick Number")
        plot_help.set_data(taken_data, ['ALSA', 'ATA'], inv_y=True)

        plot_help.save_fig(f"pps_{card_name}.png", "Pick Stats")

    def card_archetype_performance(self, card_name, color_cols=None):
        frame = self._DATA.card_frame(card_name, summary=True).T
        if color_cols is not None:
            ret = frame.loc[STAT_COL_NAMES].T
            return ret[color_cols]
        else:
            return frame

    def stat_archetype_performance(self, stat_name, color_cols=None):
        series = self._DATA.card_frame(summary=True)[stat_name]
        frame = series.reset_index(level=0)
        ret = pd.pivot_table(frame, index='Name', columns='Deck Colors')
        ret.columns = ret.columns.droplevel(0)
        if color_cols is not None:
            ret = ret[color_cols]
        return ret
    # endregion SingleCardFuncs

    def compare_card_evaluations(self, start_date=None, end_date=None):
        def inner_func(target_date):
            df = self.card_frame(date=target_date, deck_color='')
            df.index = [tup[2] for tup in df.index]
            return df

        if start_date is None:
            metadata = SetMetadata.get_metadata(self.SET)
            start_date = metadata.RELEASE_DATE

        if end_date is None:
            end_date = datetime.date.today() - datetime.timedelta(days=1)

        first = inner_func(target_date=start_date)
        last = inner_func(target_date=end_date)
        diff = last[['ALSA', 'ATA', 'Color', 'Rarity']].copy()
        diff['ALSA Change'] = first['ALSA'] - last['ALSA']
        diff['ATA Change'] = first['ATA'] - last['ATA']
        return diff[['ALSA', 'ALSA Change', 'ATA', 'ATA Change', 'Color', 'Rarity']]

    def get_top(self, column, count=10, asc=False, card_color=None, card_rarity=None, deck_color='', play_lim=None):
        frame = self.card_frame(deck_color=deck_color, summary=True)
        filters = list()
        if card_color:
            filters.append(card_color_filter(card_color))
        if card_rarity:
            filters.append(rarity_filter(card_rarity))
        frame = filter_frame(frame, column, filters, asc)

        if play_lim is not None:
            # TODO: Fix this.
            if type(play_lim) is float:
                play_lim *= self.get_games_played(deck_color)
            print(f'Minimum Games played to be included: {play_lim}')
            frame = frame[frame['# GP'] >= play_lim]

        return frame.head(count)

    @auto_prettify
    def get_top_performers(self, card_color=None, common_cnt=10, uncommon_cnt=5, deck_color='', play_lim=None, stat='GIH WR'):
        to_drop = [
            '# GP', '# OH', '# GD', '# GIH', '# GND',
            'GP GW', 'OH GW', 'GD GW', 'GIH GW', 'GND GW',
            'Type Line', 'Supertypes', 'Types', 'Subtypes', 'Power', 'Toughness',
            'OH Tier', 'GD Tier',  'GIH Tier', 'OH Percentile', 'GD Percentile', 'GIH Percentile'
        ]
        play_lim = play_lim or round(self.card_frame(deck_color=deck_color, summary=True)['# GP'].max() * 0.005)
        commons = self.get_top(stat, count=common_cnt, card_color=card_color, card_rarity='C',
                               deck_color=deck_color, play_lim=play_lim)
        uncommons = self.get_top(stat, count=uncommon_cnt, card_color=card_color, card_rarity='U',
                                 deck_color=deck_color, play_lim=play_lim)
        top_cards = pd.concat([commons, uncommons])
        top_cards = top_cards.drop(to_drop, axis=1)
        return top_cards.sort_values(stat, ascending=False)
