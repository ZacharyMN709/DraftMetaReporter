from typing import Optional
from datetime import date, timedelta
import pandas as pd

from core.wubrg import COLOR_PAIRS
from core.data_fetching import cast_color_filter, rarity_filter, filter_frame, FilterLike

from core.data_graphing.PlotterHelper import PlotterHelper

MIN_ALSA = 6
TRG_STAT = 'GIH WR'


class PickOrderAnalyzer:
    COLUMNS = ['ALSA', 'ALSA Change', 'ATA', 'ATA Change', 'GIH WR', 'OH WR', 'Color', 'Cast Color', 'Rarity', 'Rank']
    KEPT_COLUMNS = ['ALSA', 'ATA', 'GIH WR', 'OH WR', 'Color', 'Cast Color', 'Rarity', 'Rank']

    def _gen_pick_order_diffs(self,
                              deck_color: str = '',
                              start_date: Optional[date] = None,
                              end_date: Optional[date] = None):
        start_date = start_date or self.DATA.SET_METADATA.RELEASE_DATE
        end_date = end_date or date.today() - timedelta(days=1)

        diff = self.DATA.simplified_card_frame(deck_color=deck_color).copy()
        first = self.DATA.simplified_card_frame(date=start_date)
        last = self.DATA.simplified_card_frame(date=end_date)

        diff['ALSA'] = last['ALSA']
        diff['ATA'] = last['ATA']
        diff['ALSA Change'] = first['ALSA'] - last['ALSA']
        diff['ATA Change'] = first['ATA'] - last['ATA']
        return diff[self.COLUMNS]

    def __init__(self, data, sort_col: str, start_date: Optional[date] = None, end_date: Optional[date] = None):
        self.DATA = data
        self.PLOTTER = PlotterHelper(self.DATA)
        self.sort_col = sort_col
        self.start_date = start_date
        self.end_date = end_date
        self.diff = self._gen_pick_order_diffs(start_date=start_date, end_date=end_date)

    def filter_by(self, colors: FilterLike = None, rarities: FilterLike = None, order=None):
        return filter_frame(self.diff, order=order, filters=[cast_color_filter(colors), rarity_filter(rarities)])

    @property
    def commons(self) -> pd.DataFrame:
        return self.filter_by(rarities='C', order=self.sort_col)

    @property
    def uncommons(self) -> pd.DataFrame:
        return self.filter_by(rarities='U', order=self.sort_col)

    @property
    def rares(self) -> pd.DataFrame:
        return self.filter_by(rarities='R', order=self.sort_col)

    @property
    def mythics(self) -> pd.DataFrame:
        return self.filter_by(rarities='M', order=self.sort_col)

    def _gen_title(self, rarity: str, top: bool = True):
        contested_str, rarity_str = self._gen_title_strings(rarity, top)
        return f"{contested_str}{rarity_str}"

    @classmethod
    def _gen_title_strings(cls, rarity: str, top: bool = True):
        if rarity == 'C':
            rarity_str = 'Commons'
        elif rarity == 'U':
            rarity_str = 'Uncommons'
        elif rarity == 'R':
            rarity_str = 'Rares'
        elif rarity == 'M':
            rarity_str = 'Mythics'
        else:
            rarity_str = 'All'

        contested_str = 'Contested' if top else 'Uncontested'
        return contested_str, rarity_str

    def _get_frame_and_row_count(self, rarity: str):
        if rarity == 'C':
            frame = self.commons
            head_cnt = 20
        elif rarity == 'U':
            frame = self.uncommons
            head_cnt = 10
        elif rarity == 'R':
            frame = self.rares
            head_cnt = 5
        elif rarity == 'M':
            frame = self.mythics
            head_cnt = 5
        else:
            frame = self.diff
            head_cnt = 40

        return frame, head_cnt

    def save_frame_image(self, rarity: str, top: bool = True):
        frame, head_cnt = self._get_frame_and_row_count(rarity)
        title_stub = self._gen_title(rarity, top)
        title = f"{self.sort_col} - {title_stub}CCE.png"
        frame = frame.sort_values(self.sort_col, ascending=not top).head(head_cnt)
        return self.PLOTTER.frame_to_png(frame, title)

    def gen_card_evaluation_summary(self):
        return {
            "ContestedCommons": self.save_frame_image('C', top=True),
            "UncontestedCommons": self.save_frame_image('C', top=False),
            "TopPerformingCommons": self.top_card_summary('C'),
            "ContestedUncommons": self.save_frame_image('U', top=True),
            "UncontestedUncommons": self.save_frame_image('U', top=False),
            "TopPerformingUncommons": self.top_card_summary('U'),
        }

    def top_card_summary(self, rarity: str, sort_col: str = 'GIH WR'):
        _, rarity_str = self._gen_title_strings(rarity)
        title = f"{self.sort_col} - TopPerforming{rarity_str}CCE.png"

        frame, head_cnt = self._get_frame_and_row_count(rarity)
        sub_frame = frame.sort_values(sort_col, ascending=False).head(head_cnt)
        return self.PLOTTER.frame_to_png(sub_frame, title)

    def _get_winrate(self, color=''):
        if color:
            sub_frame = self.DATA.deck_archetype_frame(summary=True)
            sub_frame = sub_frame[sub_frame['Splash'] == False]
            return sub_frame['Win %'][color]
        else:
            return self.DATA.deck_group_frame(summary=True)['Win %']['All Decks']

    # https://mtgazone.com/how-to-wheel-in-drafts/
    def get_best_wheel_cards(self, deck_color, min_alsa=None, trg_stat=None, save=False):
        min_alsa = min_alsa or MIN_ALSA
        trg_stat = trg_stat or TRG_STAT
        target_wr = self._get_winrate(deck_color)

        frame = self._gen_pick_order_diffs(deck_color=deck_color)
        sub_frame = frame[frame['ALSA'] >= min_alsa].sort_values('ALSA', ascending=True)
        sub_frame = sub_frame[sub_frame[trg_stat] >= target_wr]
        axis_name = deck_color or 'All Decks'
        sub_frame = sub_frame.rename_axis(f"{axis_name} (%{target_wr})")
        sub_frame = sub_frame.sort_values(trg_stat, ascending=False)
        if deck_color:
            title = f"Wheelable Cards - {deck_color}.png"
        else:
            title = f"Wheelable Cards - All Cards.png"

        return self.PLOTTER.frame_to_png(sub_frame, title, save=save)

    def get_wheelable_summary(self, save=False):
        archetypes = [''] + COLOR_PAIRS
        wheelable_cards = {c: self.get_best_wheel_cards(c, save=save) for c in archetypes}
        frame_iterator = iter(wheelable_cards.values())
        return frame_iterator
