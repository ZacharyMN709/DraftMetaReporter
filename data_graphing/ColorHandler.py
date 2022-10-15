import seaborn as sns

from Utilities.auto_logging import logging


sns.set_theme()
sns.set_color_codes()


class ColorHandler:  # pragma: no cover
    def __init__(self, palette=None, color_dict=None):
        self.PALETTE = sns.color_palette(palette)
        self.COLOR_DICT = color_dict
        # self._PALETTE = ['b', 'y', 'r', 'g', 'm', 'b', 'c']
        self._PALETTE_IDX = 0

    @property
    def PALETTE(self):
        return self._PALETTE

    @PALETTE.setter
    def PALETTE(self, val):
        if val is None:
            self._PALETTE = sns.color_palette(val)
        elif isinstance(val, str):
            try:
                self._PALETTE = sns.color_palette(val)
            except ValueError:
                logging.sparse(f"'{val}' is not a valid palette name. Using default.")
                self._PALETTE = sns.color_palette(None)
        elif isinstance(val, sns.palettes._ColorPalette):
            self._PALETTE = sns.color_palette(val)
        else:
            logging.sparse(f"Cannot derive palette from '{type(val)}'. Using default.")
            self._PALETTE = sns.color_palette(None)

        self._PALETTE_IDX = 0

    @property
    def COLOR_DICT(self):
        return self._COLOR_DICT

    @COLOR_DICT.setter
    def COLOR_DICT(self, val):
        if val is None:
            self._COLOR_DICT = val
        elif isinstance(val, dict):
            self._COLOR_DICT = val
        else:
            logging.sparse(f"'{type(val)}' is not 'dict' or 'None'. Defaulting to None.")
            self._COLOR_DICT = None

    @COLOR_DICT.deleter
    def COLOR_DICT(self):
        """Since some of the dictionaries are stored statically,
        set the reference to null instead of electing the underlying data."""
        self._COLOR_DICT = None

    def get_color(self, col_name=None):
        if self.COLOR_DICT is None:
            return self.next_color()
        elif col_name is None:
            return self.next_color()
        elif col_name in self.COLOR_DICT:
            return self.COLOR_DICT[col_name]
        else:
            return self.next_color()

    def next_color(self):
        color = self._PALETTE[self._PALETTE_IDX % len(self._PALETTE)]
        self._PALETTE_IDX += 1
        return color
