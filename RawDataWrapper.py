from RawDataHandler import RawDataHandler
from LineColors import LineColors

class RawDataWrapper:   
    def __init__(self, SET, FORMAT):
        self._SET = SET
        self._FORMAT = FORMAT
        self._DATA = RawDataHandler(SET, FORMAT)
        
    
    @property
    def SET(self):
        """The draft set."""
        return self._SET
    
    @property
    def FORMAT(self):
        """The format type."""
        return self._FORMAT
    
    @property
    def DATA(self):
        """The object which contains the data about the set and format."""
        return self._DATA
    
    @property
    def FUNCS(self):
        """A helper object which contains convenience functions for plotting and subsetting."""
        return self._FUNCS
    
    
    def deck_group_frame(self, name=slice(None, None, None), date=slice(None, None, None), summary=False):
        """Returns a subset of the 'GROUPED_ARCHTYPE' data as a DataFrame."""
        if summary:
            return self.DATA.GROUPED_ARCHTYPE_SUMMARY_FRAME.loc(axis=0)[pd.IndexSlice[name]]
        else:
            return self.DATA.GROUPED_ARCHTYPE_HISTORY_FRAME.loc(axis=0)[pd.IndexSlice[date, name]]
     
    def deck_archetype_frame(self, name=slice(None, None, None), date=slice(None, None, None), summary=False):
        """Returns a subset of the 'SINGLE_ARCHTYPE' data as a DataFrame."""
        if summary:
            return self.DATA.SINGLE_ARCHTYPE_SUMMARY_FRAME.loc(axis=0)[pd.IndexSlice[name]]
        else:
            return self.DATA.SINGLE_ARCHTYPE_HISTORY_FRAME.loc(axis=0)[pd.IndexSlice[date, name]]
    
    def card_frame(self, name=slice(None, None, None), deck_colors=slice(None, None, None), date=slice(None, None, None), card_color=None, card_rarity=None, summary=False):
        """Returns a subset of the 'CARD' data as a DataFrame."""
        if type(deck_colors) is str:
            deck_colors = WUBRG.get_color_identity(deck_colors)
        
        if summary:
            ret = self.DATA.CARD_SUMMARY_FRAME.loc(axis=0)[pd.IndexSlice[deck_colors, name]]
        else:
            ret = self.DATA.CARD_HISTORY_FRAME.loc(axis=0)[pd.IndexSlice[date, deck_colors, name]]
            
        if card_color:
            card_color = WUBRG.get_color_identity(card_color)
            ret = ret[ret['Color'] == card_color]
            
        if card_rarity:
            ret = ret[ret['Rarity'] == card_rarity]
        
        return ret
    
    
    
    
    #Helper Functions
    def graph_pick_stats(self, card_name, roll=1):
        taken_data = self.card_frame(name=card_name, deck_colors='')[['ALSA', 'ATA']]
        taken_data.index = [tup[0][5:] for tup in taken_data.index]
        rolling = taken_data.rolling(window=roll, min_periods=1, center=True).mean()

        mx = min(max(taken_data.max()) + 0.25, 15) 
        mn = max(min(taken_data.min()) - 0.25, 1)
        tit_str = f"{self.SET} - {self.FORMAT}\n{card_name}"

        rolling.plot(ylim=(mx, mn), grid=True, title=tit_str)

        return taken_data

    def compare_card_evaluations(self, start_date, end_date):
        def inner_func(date):
            df = self.card_frame(date=date, deck_colors='')
            df.index = [tup[2] for tup in df.index]
            return df

        first = inner_func(date='2022-02-10')
        last = inner_func(date='2022-02-15')
        diff = last[['ALSA', 'ATA', 'Color', 'Rarity']].copy()
        diff['Δ ALSA'] = first['ALSA'] - last['ALSA']
        diff['Δ ATA'] = first['ATA'] - last['ATA']
        return diff[['ALSA', 'Δ ALSA', 'ATA', 'Δ ATA', 'Color', 'Rarity']]

    
    
    def get_card_summary(self, card_name, colors='', roll=1):
        frame = self.card_frame(name=card_name, deck_colors=colors)[['GIH WR', 'ALSA', '# GP', 'IWD']]
        frame.index = [tup[0][5:] for tup in frame.index]
        rolling = frame.rolling(window=roll, min_periods=1, center=True).mean()
        return rolling

    def plot_card_summary(self, card_name, colors='', roll=1):
        rolling = self.get_card_summary(card_name, colors, roll)
        title = f"{card_name}"

        col_filt = f"Color Filter: {colors}"
        rol_filt = f"Rolling Average: {roll} Days"

        if colors and roll > 1:
            title += f"\n{col_filt}  -  {rol_filt}"
        elif colors:
                title += f"\n{col_filt}"
        elif roll > 1:
                title += f"\n{rol_filt}"

        rolling.plot(subplots=True, layout=(2,2), figsize=(12,8), title=title)
        
    def get_top(self, column, count=10, asc=True, color=None, rarity=None):
        frame = self.card_frame(deck_colors='', summary=True)
        frame = frame.sort_values(column, ascending=asc)

        if color is not None:
            color = WUBRG.get_color_identity(color)
            frame = frame[frame['Color'] == color]

        if rarity:
            frame = frame[frame['Rarity'].isin(list(rarity))]

        return frame.head(count)

        
    def get_avg_winrate(self, day=None, arch='All Decks'):
        if day:
            return self.deck_group_frame(date=day, summary=False).loc[(day, arch)]['Win %']
        else:
            return self.deck_group_frame(date=day, summary=True).loc[arch]['Win %']
    
    def get_archetype_frame(self, colors, roll=1):
        win_rate_frame = self.deck_archetype_frame(name=colors)
        win_rate_frame.index = [tup[0] for tup in win_rate_frame.index]
        #win_rate_frame = win_rate_frame[['Splash', 'Games', 'Win %']]
        win_rate_frame = win_rate_frame[win_rate_frame['Splash'] == False][['Wins', 'Games']]
        rolling = win_rate_frame.rolling(window=roll, min_periods=1, center=True).mean().round()
        rolling['Win %'] = round((rolling['Wins'] / rolling['Games']) * 100, 2)
        rolling['Avg. Win%'] = [self.get_avg_winrate(idx) for idx in win_rate_frame.index]
        rolling['2C Win%'] = [self.get_avg_winrate(idx, arch='Two-color') for idx in win_rate_frame.index]
        rolling['Win % Offset'] = rolling['Win %'] - rolling['Avg. Win%']
        return rolling

    def get_archetype_winrate_history(self, color_filter=None, roll=1):
        d = dict()
        for col in WUBRG.COLOR_PAIRS:
            temp_frame = self.get_archetype_frame(col)
            d[col] = temp_frame['Win %']
        d['AVG'] = temp_frame ['Avg. Win%']
        d['2C'] = temp_frame ['2C Win%']

        test_frame = pd.DataFrame.from_dict(d)
        test_frame.index = [idx[5:] for idx in test_frame.index]
        if color_filter:
            col_filt = [col for col in WUBRG.COLOR_PAIRS if color_filter in col] + ['AVG', '2C'] 
            test_frame = test_frame[col_filt]

        rolling = test_frame.rolling(window=roll, min_periods=1, center=True).mean()
        return rolling

    def plot_archetype_winrate_history(self, color_filter=None, roll=1):
        test_frame = self.get_archetype_winrate_history(color_filter, roll)
        lc = LineColors()
        title = "Archetpye Winrates"

        col_filt = f"Color Filter: {color_filter}"
        rol_filt = f"Rolling Average: {roll} Days"

        if color_filter and roll > 1:
            title += f"\n{col_filt}  -  {rol_filt}"
        elif color_filter:
                title += f"\n{col_filt}"
        elif roll > 1:
                title += f"\n{rol_filt}"
        test_frame.plot(figsize=(20, 10), color=lc.get_col_array(color_filter), title=title, lw=2.5, grid=True)
        
        
    def get_archetype_playrate_history(self, color_filter=None, roll=1):    
        d = dict()
        for col in WUBRG.COLOR_PAIRS:
            d[col] = self.get_archetype_frame(col)['Games']

        test_frame = pd.DataFrame.from_dict(d)
        test_frame.index = [idx[5:] for idx in test_frame.index]
        rolling = test_frame.rolling(window=roll, min_periods=1, center=True).mean()
        total = rolling.sum(axis=1)
        playrate = rolling.divide(list(total),axis=0) * 100

        if color_filter:
            col_filt = [col for col in WUBRG.COLOR_PAIRS if color_filter in col]
            playrate = playrate[col_filt]

        return playrate

    def plot_archetype_playrate_history(self, color_filter=None, roll=1):
        test_frame = self.get_archetype_playrate_history(color_filter, roll)
        lc = LineColors()
        title = "Archetpye Playrates"

        col_filt = f"Color Filter: {color_filter}"
        rol_filt = f"Rolling Average: {roll} Days"

        if color_filter and roll > 1:
            title += f"\n{col_filt}  -  {rol_filt}"
        elif color_filter:
                title += f"\n{col_filt}"
        elif roll > 1:
                title += f"\n{rol_filt}"
        test_frame.plot(figsize=(20, 10), color=lc.get_col_array(color_filter), title=title, lw=2.5, grid=True) 
