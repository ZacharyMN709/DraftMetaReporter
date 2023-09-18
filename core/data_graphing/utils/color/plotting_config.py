import enum

from core.data_graphing.utils.color.colors import Color
from core.data_graphing.utils.color.color_dicts import COLOR_MAPPINGS


class PlotConfig:
    file_name_prefix: str
    column_list: list[str]
    color_mapping: dict[str, Color]

    @classmethod
    def from_name(cls, key: str):
        color_mapping = COLOR_MAPPINGS[key]
        column_list = list(color_mapping.keys())
        return PlotConfig(key, column_list, color_mapping)

    def __init__(self, file_name_prefix, column_list, color_mapping):
        self.file_name_prefix = file_name_prefix
        self.column_list = column_list
        self.color_mapping = color_mapping


class DefaultPlotConfigs(enum.Enum):
    plot_config: PlotConfig

    def __init__(self, key: str):
        self.plot_config = PlotConfig.from_name(key)

    @property
    def file_name_prefix(self) -> str:
        return self.plot_config.file_name_prefix

    @property
    def column_list(self) -> list[str]:
        return self.plot_config.column_list

    @property
    def color_mapping(self) -> dict[str, Color]:
        return self.plot_config.color_mapping

    WHITE = "White"
    BLUE = "Blue"
    BLACK = "Black"
    RED = "Red"
    GREEN = "Green"
    ALLIED = "Allied"
    ENEMY = "Enemy"
    SHARD = "Shard"
    WEDGE = "Wedge"
    NEPHILIM = "Nephilim"
    TWO_COLOR = "Two Color"
    THREE_COLOR = "Three Color"
    FOUR_COLOR = "Four Color"
    STATS = "Stats"
    BLANK = "Blank"
