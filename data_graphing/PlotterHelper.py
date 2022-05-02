import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

from data_fetching import FramedData

from data_graphing.utils import settings
from data_graphing.ColorHandler import ColorHandler


class PlotterHelper:  # pragma: no cover
    def __init__(self, data: FramedData, palette=None, color_dict=None):
        self.DATA = data
        self.FIG = None
        self.AX = None
        self.COLORS = ColorHandler(palette, color_dict)
        os.makedirs(self.get_folder_path(), exist_ok=True)

    def _get_sub_ax(self, x=None, y=None):
        if not isinstance(self.AX, np.ndarray):
            return self.AX
        elif self.AX.ndim == 1:
            return self.AX[x if x is not None else y]
        elif self.AX.ndim == 2:
            return self.AX[x, y]
        else:
            raise Exception('Unknown axes format.')

    def get_folder_path(self):
        return os.path.join(settings.GRAPH_DIR_LOC, settings.GRAPH_DIR_NAME, self.DATA.SET, self.DATA.FORMAT)

    def get_file_path(self, filename):
        return os.path.join(self.get_folder_path(), filename)

    def new_single_plot(self, title, width=8, height=6, fontsize=settings.TITLE_SIZE):
        self.FIG, self.AX = plt.subplots(1, 1)
        self.FIG.set_size_inches(width, height)
        self.AX.set_title(f"{self.DATA.SET} {self.DATA.FORMAT_ALIAS}: {title}", fontsize=fontsize)
        self.set_x_axis_weekly()
        return self.FIG, self.AX

    def new_quad_plot(self, title, width=12, height=8, fontsize=settings.TITLE_SIZE):
        self.FIG, self.AX = plt.subplots(2, 2)
        self.FIG.set_size_inches(width, height)
        plt.figtext(0.4, 0.9, f"{self.DATA.SET} {self.DATA.FORMAT_ALIAS}: {title}", fontsize=fontsize)
        self.set_x_axis_weekly(g_x=0, g_y=0)
        self.set_x_axis_weekly(g_x=0, g_y=1)
        self.set_x_axis_weekly(g_x=1, g_y=0)
        self.set_x_axis_weekly(g_x=1, g_y=1)
        return self.FIG, self.AX

    def accredit(self, y=0.01):
        plt.figtext(0.5, y, settings.ACCREDIT_STR, **settings.ACCREDIT_KWARGS)

    def desc_note(self, colors=None, roll=1, y=0.95):
        col_filt = f"Color Filter: {colors}"
        rol_filt = f"Rolling Average: {roll} Days"

        if colors and roll > 1:
            txt = f"{rol_filt}\n{col_filt}"
        elif colors:
            txt = f"\n{col_filt}"
        elif roll > 1:
            txt = f"\n{rol_filt}"
        else:
            txt = ""

        plt.figtext(0.5, y, txt, **settings.FILTER_KWARGS)

    def set_labels(self, x_label="", y_label="", fontsize=settings.LABEL_SIZE, g_x=None, g_y=None):
        ax = self._get_sub_ax(g_x, g_y)
        ax.set_xlabel(x_label, fontsize=fontsize)
        ax.set_ylabel(y_label, fontsize=fontsize)

    def set_data(self, data, col_list, inv_y=False, inv_x=False, g_x=None, g_y=None):
        ax = self._get_sub_ax(g_x, g_y)
        for col in col_list:
            ax.plot(data.index, data[[col]], label=col, color=self.COLORS.get_color(col))
        if inv_y: ax.invert_yaxis()
        if inv_x: ax.invert_xaxis()
        ax.legend()

    def set_x_axis_weekly(self, g_x=None, g_y=None):
        ax = self._get_sub_ax(g_x, g_y)
        weeks = mdates.DayLocator(interval=7)
        ax.xaxis.set_major_locator(weeks)
        days = mdates.DayLocator(interval=1)
        ax.xaxis.set_minor_locator(days)

    def save_fig(self, filename, dpi=None):
        if dpi is None: dpi = settings.DPI
        self.FIG.savefig(self.get_file_path(filename.replace(' ', '_')), dpi=dpi)