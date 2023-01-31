import logging
from typing import Optional
import pandas as pd

from core.data_interface import Request17Lands
from core.game_metadata import SetMetadata

from core.tier_list_analysis.utils.consts import TIER_LIST_ROOT, tier_to_rank


class TierList:
    def __init__(self, user, link):
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

    @property
    def SET(self) -> str:
        return self.set_data.SET

    @property
    def tier_frame(self) -> pd.DataFrame:
        if self._tier_frame is None:
            self._tier_frame = self.merge_rankings()
        return self._tier_frame

    def add_tier(self, user, link):
        try:
            t = TierList(user, link)
            self.tier_dict[user] = t
            self._tier_frame = None
        except:
            logging.warning("Failed to create TierList object. Please check the link provided.")
        pass

    def merge_rankings(self):
        # Create an empty frame, to be indexed by card names.
        frame = pd.DataFrame()
        frame.index.name = 'Card'

        # Get each user's converted ranks as ints.
        ranks = pd.DataFrame()
        for indiv in self.tier_dict.values():
            ranks[indiv.index.name] = indiv['Rank'].astype('Int64')
            frame[indiv.index.name] = indiv['Rank'].astype('Int64')

        # Calculate the general stats and append them.
        frame['mean'] = ranks.mean(axis=1)
        frame['max'] = ranks.max(axis=1)
        frame['min'] = ranks.min(axis=1)
        frame['range'] = frame['max'] - frame['min']
        frame['std'] = ranks.std(axis=1).round(1)

        # Get the difference of squares distance to figure out most 'controversial' cards.
        dist = pd.DataFrame()
        for indiv in self.tier_dict.values():
            dist[indiv.index.name] = abs(frame['mean'] - ranks[indiv.index.name])
        frame['dist'] = dist.mean(axis=1).round(1)

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
