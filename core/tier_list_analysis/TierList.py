import logging
from typing import Optional
import pandas as pd

from core.data_fetching import cast_color_filter, rarity_filter, filter_frame
from core.data_interface import Request17Lands
from core.game_metadata import SetMetadata, RARITIES

from core.tier_list_analysis.utils.consts import TIER_LIST_ROOT, tier_to_rank, rank_to_tier
from core.wubrg import WUBRG, COLOR_COMBINATIONS


class TierList:
    def __init__(self, link, user):
        self.user: str = user
        self.link: str = link
        self.tiers: pd.DataFrame = self.gen_frame()

    def gen_frame(self) -> pd.DataFrame:
        def gen_card_dict(data):
            return {
                'Card': data['name'],
                'Tier': data['tier'],
                'Rank': tier_to_rank[data['tier']],
                'Synergy': data['flags']['synergy'],
                'Buildaround': data['flags']['buildaround']
            }

        fetcher = Request17Lands()
        raw_data = fetcher.get_tier_list(self.link.replace(TIER_LIST_ROOT, ""))
        tier_data = {card_data['name']: gen_card_dict(card_data) for card_data in raw_data}
        frame = pd.DataFrame.from_dict(tier_data, orient="index")
        frame.index.name = self.user
        return frame

    def refresh_data(self):
        self.tiers = self.gen_frame()


class TierAggregator:
    def __init__(self, SET):
        self.set_data: SetMetadata = SetMetadata.get_metadata(SET)
        self.tier_dict: dict[str, TierList] = dict()
        self._tier_frame: Optional[pd.DataFrame] = None
        self._avg_frame: Optional[pd.DataFrame] = None

    @property
    def SET(self) -> str:
        return self.set_data.SET

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

    def style_frame(self, frame):
        # Set the display to accommodate the card count.
        card_dict = self.set_data.CARD_DICT
        pd.set_option('display.max_rows', len(card_dict))

        def hover_img(card_name):
            card = card_dict[card_name]
            html = '<style>.hover_img a { position:relative; }\n' + \
                   '.hover_img a span { position:absolute; display:none; z-index:300; }\n' + \
                   '.hover_img a:hover span { display:block; height: 300px; width: 300px; overflow: visible; ' \
                   'margin-left: -175px; }</style>\n' + \
                   '<div class="hover_img">\n' + \
                   f'<a href="#">{card_name}<span><img src="{card.IMAGE_URL}" alt="image"/></span></a>\n' + \
                   '</div>'
            return html

        def to_int(val):
            try:
                return int(val)
            except Exception:
                return ' - '

        def format_short_float(val):
            return '{:.1f}'.format(val)

        def format_long_float(val):
            return '{:.3f}'.format(val)

        def card_color(val):
            single = {
                'W': '#fffeeb',
                'U': '#d2edfa',
                'B': '#ccc7c6',
                'R': '#fadcd2',
                'G': '#caedd5',
            }
            if len(val) == 1:
                return f'color: black; background-color: {single[val]}'
            elif len(val) > 1:
                return f'color: black; background-color: #f2d79d'

        def color_map(val):
            colors = ['#e67c73', '#eb8b70', '#ef9b6e', '#f3a96c', '#f7b96a',
                      '#fbc768', '#ffd666', '#e3d16c', '#c7cd72',
                      '#abc878', '#8fc47e', '#73bf84', '#57bb8a']
            try:
                x = round(val)
                return f'color: black; background-color: {colors[x]}'
            except:
                return f'color: black; background-color: grey'

        user_formats = {name: to_int for name in self.tier_dict.keys()}
        default_formats = {
            'Image': hover_img,
            'CMC': to_int,
            'mean': format_long_float,
            'max': to_int,
            'min': to_int,
            'range': format_short_float,
            'dist': format_short_float,
            'std': format_short_float,
        }

        styler = frame.style.format(default_formats | user_formats)
        return styler.applymap(card_color, subset=['Color', 'Cast Color']).applymap(color_map, subset=self.users)

    # region Calculate Tables
    def append_stat_summary(self, frame, round_to=2):
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

    def merge_rankings(self):
        # Create an empty frame, to be indexed by card names.
        frame = pd.DataFrame()
        frame.index.name = 'Card'

        # Get each user's converted ranks as ints.
        ranks = pd.DataFrame()
        for indiv in self.tier_dict.values():
            user_frame = indiv.tiers
            ranks[user_frame.index.name] = user_frame['Rank'].astype('Int64')
            frame[user_frame.index.name] = user_frame['Rank'].astype('Int64')

        self.append_stat_summary(frame)

        # Append card information to the frame.
        series = frame.index.to_series()
        frame['Image'] = series.map({card.NAME: card.NAME for card in self.set_data.CARD_DICT.values()})
        frame['Cast Color'] = series.map({card.NAME: card.CAST_IDENTITY for card in self.set_data.CARD_DICT.values()})
        frame['Color'] = series.map({card.NAME: card.COLOR_IDENTITY for card in self.set_data.CARD_DICT.values()})
        frame['Rarity'] = series.map({card.NAME: card.RARITY for card in self.set_data.CARD_DICT.values()})
        frame['CMC'] = series.map({card.NAME: card.CMC for card in self.set_data.CARD_DICT.values()})

        # Re-order the frame so card information is first.
        cols = list(frame.columns)
        frame = frame[['Image', 'CMC', 'Rarity', 'Color', 'Cast Color'] + cols[:-5]]

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
    def add_tier(self, link: str, user: str):
        try:
            t = TierList(link, user)
            self.tier_dict[user] = t
            self._tier_frame = None
        except:
            logging.warning("Failed to create TierList object. Please check the link provided.")
        pass

    def add_tiers(self, lst: list[tuple[str, str]]):
        for link, user, in lst:
            self.add_tier(link, user)

    def refresh_data(self, key=None):
        if key is None:
            for tier in self.tier_dict.values():
                tier.refresh_data()
            self._tier_frame = self.merge_rankings()
        else:
            try:
                self.tier_dict[key].refresh_data()
                self._tier_frame = self.merge_rankings()

            except KeyError:
                logging.warning("Failed to find TierList object. Please check the key provided.")
    # endregion Tier Management

    def __getitem__(self, item) -> TierList:
        return self.tier_dict[item]

