from typing import Optional, Union
from datetime import date, timedelta
import pandas as pd

from core.data_fetching import cast_color_filter, rarity_filter, filter_frame, FilterLike

from core.data_graphing.PlotterHelper import PlotterHelper


class PickOrderAnalyzer:
    COLUMNS = ['ALSA', 'ALSA Change', 'ATA', 'ATA Change', 'GIH WR', 'OH WR', 'Color', 'Cast Color', 'Rarity']
    KEPT_COLUMNS = ['ALSA', 'ATA', 'GIH WR', 'OH WR', 'Color', 'Cast Color', 'Rarity']

    def _gen_pick_order_diffs(self, start_date: Optional[date] = None, end_date: Optional[date] = None):
        def frame_by_date(target_date: Optional[date]):
            df = self.DATA.card_frame(date=target_date, deck_color='')
            df.index = [tup[2] for tup in df.index]
            return df

        start_date = start_date or self.DATA.SET_METADATA.RELEASE_DATE
        end_date = end_date or date.today() - timedelta(days=1)

        # TODO: Remove the extra index from this.
        diff = self.DATA.card_frame(deck_color='', summary=True).copy()
        diff.index = [tup[1] for tup in diff.index]
        first = frame_by_date(target_date=start_date)
        last = frame_by_date(target_date=end_date)
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