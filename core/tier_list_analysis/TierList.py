from __future__ import annotations
from typing import Optional
from functools import partial
import pandas as pd
import os
import pickle
from pandas.io.formats.style import Styler
from datetime import datetime, date

from core.wubrg import WUBRG, COLOR_COMBINATIONS
from core.utilities import logging
from core.data_requesting import Request17Lands
from core.game_metadata import SetMetadata, RARITIES, CardManager, SET_EXTRAS
from core.data_fetching import cast_color_filter, rarity_filter, filter_frame, tier_to_rank, SetManager, \
    FORMAT_NICKNAME_DICT, DATA_DIR_LOC, DATA_DIR_NAME

from core.tier_list_analysis.utils import *


class CardTier:
    name: str
    tier: str
    rank: int
    sideboard: bool
    synergy: bool
    buildaround: bool
    comment: str


class TierList:
    @staticmethod
    def adjust_data(data: dict):
        for tier in data:
            # Use the card name from 17Lands to get the relevant card from Scryfall.
            # This patches bad names coming back from Arena or 17Lands.
            card = CardManager.from_name(tier['name'])
            tier['name'] = card.NAME
            tier['rank'] = tier_to_rank[tier['tier']]
        return data

    def __init__(self, data, user, _set):
        # Apply adjustments to the data.
        self.data = self.adjust_data(data)
        self.user: str = user
        self.SET: str = _set  # TODO: Auto determine the set from cards in tierlist.

        self.tiers: pd.DataFrame = self.gen_frame(self.data)
        self.creation_time = datetime.utcnow()

        self.data_root: str = os.path.join(DATA_DIR_LOC, DATA_DIR_NAME, self.SET, 'Tiers')
        self.filename = f'{self.SET}-{self.user}-{self.creation_time.strftime("%y%m%d")}{TIER_LIST_EXT}'

    @classmethod
    def from_link(cls, link, user, _set):
        # Pull the data from 17Lands.
        fetcher = Request17Lands()
        data = fetcher.get_tier_list(link.replace(TIER_LIST_ROOT, ""))
        return TierList(data, user, _set)

    def gen_frame(self, data) -> pd.DataFrame:
        # Create the DataFrame, setting the index to be the user who provided the TierList.
        frame_dict = {tier['name']: tier for tier in data}
        frame = pd.DataFrame.from_dict(frame_dict, orient="index")
        frame.index.name = self.user
        return frame

    def save(self) -> str:
        os.makedirs(self.data_root, exist_ok=True)
        file_path = os.path.join(self.data_root, self.filename)
        with open(file_path, 'wb') as f:
            pickle.dump(self, f, pickle.HIGHEST_PROTOCOL)
        return file_path

    @classmethod
    def load(cls, filename: str) -> TierList:
        data_root = os.path.join(DATA_DIR_LOC, DATA_DIR_NAME, filename[:3], 'Tiers')
        with open(os.path.join(data_root, filename), 'rb') as f:
            obj = pickle.load(f)
        return obj


class TierAggregator:
    def __init__(self, _set):
        self.set_metadata: SetMetadata = SetMetadata.get_metadata(_set)
        self.card_list = self.set_metadata.CARD_LIST
        for x in SET_EXTRAS[_set]:
            extra_metadata = SetMetadata.get_metadata(x)
            self.card_list += extra_metadata.CARD_LIST
        self.set_data: SetManager = SetManager(_set)
        self.tier_dict: dict[str, TierList] = dict()
        self._tier_frame: Optional[pd.DataFrame] = None
        self._avg_frame: Optional[pd.DataFrame] = None
        self._comparer: Optional[TierComparer] = None

        self.data_root: str = os.path.join(DATA_DIR_LOC, DATA_DIR_NAME, self.SET, 'Tiers')

    @property
    def SET(self) -> str:
        return self.set_metadata.SET

    @property
    def users(self) -> list[str]:
        return list(self.tier_dict.keys())

    @property
    def tier_frame(self) -> pd.DataFrame:
        if self._tier_frame is None:
            self._tier_frame = self.merge_rankings()
        return self._tier_frame

    @property
    def avg_frame(self) -> pd.DataFrame:
        if self._avg_frame is None:
            self._avg_frame = self.calc_avgs()
        return self._avg_frame

    @property
    def comparer(self) -> TierComparer:
        if self._comparer is None:
            self._comparer = TierComparer(self)
        return self._comparer

    def suborder_by_rarity(self, ordering='mean', style=False):
        rarities = RARITIES
        by_rarities = [filter_frame(self.tier_frame, order=ordering, filters=[rarity_filter(r)]) for r in rarities]
        frame = pd.concat(by_rarities)
        if style:
            return self.style_frame(frame)
        else:
            return frame

    def suborder_by_color(self, ordering='mean', style=False):
        colors = COLOR_COMBINATIONS
        by_colors = [filter_frame(self.tier_frame, order=ordering, filters=[cast_color_filter(c)]) for c in colors]
        frame = pd.concat(by_colors)
        if style:
            return self.style_frame(frame)
        else:
            return frame

    def top_picks(self, ordering='mean', style=False):
        top = list()

        for c in WUBRG:
            filters = [rarity_filter('U'), cast_color_filter(c)]
            top.append(filter_frame(self.tier_frame, order=ordering, filters=filters).head(3))

            filters = [rarity_filter('C'), cast_color_filter(c)]
            top.append(filter_frame(self.tier_frame, order=ordering, filters=filters).head(5))

        frame = pd.concat(top)
        if style:
            return self.style_frame(frame)
        else:
            return frame

    # TODO: Revisit this function.
    def get_top(self, color=None, rarity=None, ordering='mean', count=5):
        filters = list()
        if color:
            filters.append(cast_color_filter(color))
        if rarity:
            filters.append(rarity_filter(rarity))
        frame = filter_frame(self.tier_frame, order=ordering, filters=filters).head(count)

    # region Styling & Formatting
    def apply_formatting(self, styler: Styler) -> Styler:
        # TODO: Consider if this should be able to be more finely controlled.
        card_info = {
            'Image': hover_card,
            'CMC': safe_to_int,
        }

        data_rank_formats = {
            'BO1': safe_to_int,
            'BO3': safe_to_int,
            'Sealed': safe_to_int,
        }

        user_rank_formats = {name: safe_to_int for name in self.tier_dict.keys()}

        stat_formats = {
            'mean': format_long_float,
            'max': safe_to_int,
            'min': safe_to_int,
        }

        disagree_formats = {
            'range': format_short_float,
            'dist': format_short_float,
            'std': format_short_float,
        }

        all_dicts = card_info | data_rank_formats | user_rank_formats | stat_formats | disagree_formats
        styler = styler.format(all_dicts)
        return styler

    def apply_styles(self, styler: Styler) -> Styler:
        # TODO: Consider if this should be able to be more finely controlled.
        # https://pandas.pydata.org/docs/reference/api/pandas.io.formats.style.Styler.background_gradient.html
        # https://pandas.pydata.org/docs/user_guide/style.html
        # https://matplotlib.org/stable/tutorials/colors/colormaps.html

        # Create methods to be converted into partials with a consistent set of arguments.
        def apply(m: callable, s: Styler, c: str) -> Styler:
            return s.applymap(m, subset=[c])

        def gradient(m: str, s: Styler, c: str) -> Styler:
            # TODO: Handle NANs here.
            return s.background_gradient(subset=[c], cmap=m)

        # Create mappings of partial functions for each column name to style.
        user_style_dict = {user: partial(apply, user_map) for user in self.users}
        const_style_dict = {
            "Color": partial(apply, color_map),
            "Cast Color": partial(apply, color_map),
            "Rarity": partial(apply, rarity_map),
            "mean": partial(apply, stat_map),
            "max": partial(apply, stat_map),
            "min": partial(apply, stat_map),
            "BO1": partial(apply, user_map),
            "BO3": partial(apply, user_map),
            "range": partial(apply, range_map),
            "std": partial(gradient, 'Purples'),
            "dist": partial(gradient, 'Purples'),
        }
        style_dict = user_style_dict | const_style_dict

        for col in styler.data.columns:
            if col in style_dict:
                styler = style_dict[col](styler, col)

        return styler

    def style_frame(self, frame) -> Styler:
        # Set the display to accommodate the card count.
        pd.set_option('display.max_rows', len(self.set_metadata.CARD_DICT))

        # Then apply the formatting and styling.
        styler = frame.style
        styler = self.apply_formatting(styler)
        styler = self.apply_styles(styler)

        return styler
    # endregion Styling & Formatting

    # region Calculate Tables
    def append_stat_summary(self, frame, round_to=2) -> pd.DataFrame:
        # Keep a list of the original columns, to use later.
        org_cols = list(frame.columns)

        # Calculate the general stats, keeping them separate to not contaminate the frame.
        frame_mean = frame.mean(axis=1).round(round_to)
        frame_max = frame.max(axis=1)
        frame_min = frame.min(axis=1)
        frame_range = frame_max - frame_min
        frame_std = frame.std(axis=1).round(round_to)

        # Append the general stats after they've all been calculated.
        frame['mean'] = frame_mean
        frame['max'] = frame_max
        frame['min'] = frame_min
        frame['range'] = frame_range
        frame['std'] = frame_std

        # Get the sum of distances to figure out most 'controversial' rows.
        dist = pd.DataFrame()
        for col in org_cols:
            dist[col] = abs(frame['mean'] - frame[col])
        frame['dist'] = dist.mean(axis=1).round(round_to)
        return frame

    # noinspection PyPep8Naming
    def prepend_17L_ranks(self, frame) -> pd.DataFrame:
        # Note the original columns, so the new ones can be put before them.
        org_cols = list(frame.columns)
        new_cols = list()

        for col, data in self.set_data.DATA.items():
            if data.DATA.CARD_SUMMARY_FRAME is not None:
                tier_frame = data.get_stats_grades()
                if tier_frame is None:
                    continue
                short_col = FORMAT_NICKNAME_DICT[col]
                frame[short_col] = tier_frame.droplevel(0)['tier'].astype('Int64')
                new_cols.append(short_col)

        # Re-order the frame so the data-based stats are first.
        frame = frame[new_cols + org_cols]
        return frame

    def prepend_card_info(self, frame) -> pd.DataFrame:
        # Note the original columns, so the new ones can be put before them.
        org_cols = list(frame.columns)

        # Append card information to the frame.
        series = frame.index.to_series()
        # TODO: Handle bonus sheets here.
        frame['Image'] = series.map({card.NAME: card.NAME for card in self.card_list})
        frame['Cast Color'] = series.map({card.NAME: card.CAST_IDENTITY for card in self.card_list})
        frame['Color'] = series.map({card.NAME: card.COLOR_IDENTITY for card in self.card_list})
        frame['Rarity'] = series.map({card.NAME: card.RARITY for card in self.card_list})
        frame['CMC'] = series.map({card.NAME: card.CMC for card in self.card_list})

        # Re-order the frame so card information is first.
        frame = frame[['Image', 'CMC', 'Rarity', 'Color', 'Cast Color'] + org_cols]
        return frame

    def merge_rankings(self) -> pd.DataFrame:
        # Create an empty frame, to be indexed by card names.
        frame = pd.DataFrame()
        frame.index.name = 'Card'

        # Get each user's converted ranks as ints.
        for indiv in self.tier_dict.values():
            user_frame = indiv.tiers
            frame[user_frame.index.name] = user_frame['rank'].astype('Int64')

        frame = self.append_stat_summary(frame)
        frame = self.prepend_17L_ranks(frame)
        frame = self.prepend_card_info(frame)
        return frame

    def calc_avgs(self):
        avgs = dict()

        # For each rarity and colour, get each user's average evaluation.
        for r in RARITIES:
            color_frame = pd.DataFrame()

            for c in WUBRG:
                working = filter_frame(self.tier_frame, filters=[cast_color_filter(c), rarity_filter(r)])
                working = working.drop(
                    ['Image', 'CMC', 'Rarity', 'Color', 'Cast Color', 'std', 'max', 'min', 'mean', 'range', 'dist'],
                    axis=1)
                working = working.dropna(how='all', axis=1)
                color_frame[c] = working.mean().round(1)

            # Translate it to a row, and add it to the inner frame.
            avgs[r] = color_frame.T

        # Concatenate the inner frames to make the full frame, and add the stat summary.
        ret = pd.concat(avgs)
        self.append_stat_summary(ret)
        return ret
    # endregion Calculate Tables

    # region Tier Management
    def add_tier(self, tier: TierList):
        self.tier_dict[tier.user] = tier
        self._tier_frame = None

    def add_tiers(self, lst: list[TierList]):
        for tier, in lst:
            self.add_tier(tier)
    # endregion Tier Management

    def __getitem__(self, item) -> TierList:
        return self.tier_dict[item]


class TierComparer:
    DIFF_COL = 'diff'

    def __init__(self, agg: TierAggregator):
        self.agg: TierAggregator = agg
        self._user: str = self.agg.users[0]
        self._cmp_trg: str = 'mean'
        self._play_frame: Optional[pd.DataFrame] = None

    def make_frame(self) -> pd.DataFrame:
        frame = self.agg.tier_frame.copy(True)
        frame[self.DIFF_COL] = self.agg.tier_frame[self.user] - self.agg.tier_frame[self.compare_target]
        return frame

    def validate_column(self, val: str) -> bool:
        # If the value is in the users, it's safe.
        if val in self.agg.users:
            return True

        # If the value a format name, check that it's actually in the columns.
        if val in FORMAT_NICKNAME_DICT.values():
            return val in self.agg.tier_frame.columns

        # Otherwise, the value has to be 'mean', or it's invalid for a comparison column.
        return val == 'mean'

    @property
    def user(self) -> str:
        return self._user

    @user.setter
    def user(self, value: str):
        if self.validate_column(value):
            self._play_frame = None
            self._user = value
        else:
            logging.warning(f"'{value}' is not a valid column name.")

    @property
    def compare_target(self) -> str:
        return self._cmp_trg

    @compare_target.setter
    def compare_target(self, value: str):
        if self.validate_column(value):
            self._play_frame = None
            self._cmp_trg = value
        else:
            logging.warning(f"'{value}' is not a valid column name.")

    @property
    def play_frame(self) -> pd.DataFrame:
        if self._play_frame is None:
            self._play_frame = self.make_frame()
        return self._play_frame

    def default_diff(self):
        # TODO: Come up with calculation for default diff, possibly based on if compare_target is 'mean' or not.
        if self.compare_target == 'mean' or self.user == 'mean':
            return 1
        else:
            return 1

    def apply_thresholds(self, frame: pd.DataFrame, user_thresh: float, trg_thresh: float) -> pd.DataFrame:
        if user_thresh:
            frame = frame[frame[self.user] >= user_thresh]
        if trg_thresh:
            frame = frame[frame[self.compare_target] >= trg_thresh]
        return frame

    def get_overrated(self, diff: float = None, user_thresh: float = None, trg_thresh: float = None) -> pd.DataFrame:
        if diff is None:
            diff = self.default_diff()

        frame = self.play_frame[self.play_frame[self.DIFF_COL] >= diff]
        frame = self.apply_thresholds(frame, user_thresh, trg_thresh)
        return frame.sort_values(self.DIFF_COL, ascending=False)

    def get_underrated(self, diff: float = None, user_thresh: float = None, trg_thresh: float = None) -> pd.DataFrame:
        if diff is None:
            diff = self.default_diff()

        frame = self.play_frame[self.play_frame[self.DIFF_COL] <= -diff]
        frame = self.apply_thresholds(frame, user_thresh, trg_thresh)
        return frame.sort_values(self.DIFF_COL, ascending=True)

    def get_default_comparisons(self, diff: float = None, thresh: float = None) -> tuple[pd.DataFrame, pd.DataFrame]:
        over = self.get_overrated(diff, user_thresh=thresh)
        under = self.get_underrated(diff, trg_thresh=thresh)
        return over, under

