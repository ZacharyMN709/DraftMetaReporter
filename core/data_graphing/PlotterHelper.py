from typing import Optional
import os

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as plot_dates
import seaborn as sns
import dataframe_image as dfi

from core.data_fetching import FramedData

from core.data_graphing.utils import prettify_frame
from core.data_graphing.utils import settings
from core.data_graphing.utils.color.plotting_config import PlotConfig, DefaultPlotConfigs


class PlotterHelper:  # pragma: no cover
    DATA: FramedData
    alpha: float
    _plotter_config: PlotConfig
    _palette_name: Optional[str]
    _palette: sns.palettes._ColorPalette
    _palette_idx: int

    def __init__(self, data: FramedData, plotter_config: PlotConfig = None,
                 alpha: float = None, palette_name: str = None):
        self.DATA = data
        self.FIG = None
        self.AX = None
        self.alpha = alpha or settings.ALPHA
        self._plotter_config = plotter_config or DefaultPlotConfigs.BLANK.plot_config
        self._palette_name = None
        self.reset_palette(palette_name)
        os.makedirs(self.get_folder_path(), exist_ok=True)

    # region Color Handling
    def reset_palette(self, palette_name: str = None):
        if palette_name:
            self._palette_name = palette_name
        self._palette = sns.color_palette(self._palette_name)
        self._palette_idx = 0

    def _get_color(self, col_name=None):
        color = self._plotter_config.color_mapping.get(col_name, None)
        if color:
            r = color.value[0] / 255
            g = color.value[1] / 255
            b = color.value[2] / 255
            return r, g, b, self.alpha
        else:
            color = self._palette[self._palette_idx % len(self._palette)]
            self._palette_idx += 1
            return color
    # endregion Color Handling

    # region Helper Methods
    def accredit(self, *, y=0.01, x=0.5):
        plt.figtext(x, y, settings.ACCREDIT_STR, **settings.ACCREDIT_KWARGS)

    def desc_note(self, colors=None, roll=1, *, y=0.95, x=0.5):
        color_filter = f"Color Filter: {colors}"
        roll_filter = f"Rolling Average: {roll} Days"

        if colors and roll > 1:
            txt = f"{roll_filter}\n{color_filter}"
        elif colors:
            txt = f"\n{color_filter}"
        elif roll > 1:
            txt = f"\n{roll_filter}"
        else:
            txt = ""

        plt.figtext(x, y, txt, **settings.FILTER_KWARGS)

    def set_x_axis_weekly(self, ax):
        weeks = plot_dates.DayLocator(interval=7)
        ax.xaxis.set_major_locator(weeks)
        days = plot_dates.DayLocator(interval=1)
        ax.xaxis.set_minor_locator(days)

    def set_x_axis_daily(self, ax):
        two_days = plot_dates.DayLocator(interval=2)
        ax.xaxis.set_major_locator(two_days)
        days = plot_dates.DayLocator(interval=1)
        ax.xaxis.set_minor_locator(days)
    # endregion Helper Methods

    def _get_sub_ax(self, x=None, y=None):
        if not isinstance(self.AX, np.ndarray):
            return self.AX
        elif self.AX.ndim == 1:
            return self.AX[x if x is not None else y]
        elif self.AX.ndim == 2:
            return self.AX[x, y]
        else:
            raise Exception('Unknown axes format.')

    def get_folder_path(self, sub_dir=None):
        file_path = os.path.join(settings.GRAPH_DIR_LOC, settings.GRAPH_DIR_NAME, self.DATA.SET, self.DATA.FORMAT)
        if sub_dir is not None:
            file_path = os.path.join(file_path, sub_dir)
            os.makedirs(file_path, exist_ok=True)
        return file_path

    def get_file_path(self, filename, sub_dir=None):
        return os.path.join(self.get_folder_path(sub_dir), filename)

    def new_single_plot(self, title, width=8, height=6, fontsize=settings.TITLE_SIZE):
        self.reset_palette()
        self.FIG, self.AX = plt.subplots(1, 1)
        self.FIG.set_size_inches(width, height)
        self.AX.set_title(f"{self.DATA.SET} {self.DATA.FORMAT_ALIAS}: {title}", fontsize=fontsize)
        return self.FIG, self.AX

    def new_quad_plot(self, title, width=12, height=8, fontsize=settings.TITLE_SIZE):
        self.reset_palette()
        self.FIG, self.AX = plt.subplots(2, 2)
        self.FIG.set_size_inches(width, height)
        plt.figtext(0.4, 0.9, f"{self.DATA.SET} {self.DATA.FORMAT_ALIAS}: {title}", fontsize=fontsize)
        # TODO: Tinker with this so the layout is a little clearer.
        self.FIG.autofmt_xdate(rotation=45, ha='right')
        return self.FIG, self.AX

    def set_labels(self, x_label="", y_label="", fontsize=settings.LABEL_SIZE, g_x=None, g_y=None):
        ax = self._get_sub_ax(g_x, g_y)
        ax.set_xlabel(x_label, fontsize=fontsize)
        ax.set_ylabel(y_label, fontsize=fontsize)

    def set_data(self, data, col_list, inv_y=False, inv_x=False, g_x=None, g_y=None):
        ax = self._get_sub_ax(g_x, g_y)
        if len(data.index) > 14:
            self.set_x_axis_weekly(ax)
        else:
            self.set_x_axis_daily(ax)
        for col in col_list:
            ax.plot(data.index, data[[col]], label=col, color=self._get_color(col))
        if inv_y:
            ax.invert_yaxis()
        if inv_x:
            ax.invert_xaxis()
        ax.legend()

    def save_fig(self, filename, sub_dir=None, dpi=None):
        if dpi is None:
            dpi = settings.DPI
        self.FIG.savefig(self.get_file_path(filename.replace(' ', '_'), sub_dir), dpi=dpi)

    def frame_to_png(self, frame, file_name):
        s = prettify_frame(frame)
        dfi.export(s, self.get_file_path(file_name, 'Tables'))
        return s
