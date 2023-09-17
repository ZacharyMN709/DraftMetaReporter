import enum

from colors import Color
from color_dicts import COLOR_MAPPINGS


class PlotConfig:
    file_name: str
    color_list: list[str]
    color_mapping: dict[str, Color]

    @classmethod
    def from_name(cls, key: str):
        color_mapping = COLOR_MAPPINGS[key]
        color_list = list(color_mapping.keys())
        return PlotConfig(key, color_list, color_mapping)

    def __init__(self, file_name, color_list, color_mapping):
        self.file_name = file_name
        self.color_list = color_list
        self.color_mapping = color_mapping


class DefaultPlotConfigs(enum.Enum):
    plot_config: PlotConfig

    def __init__(self, key: str):
        self.plot_config = PlotConfig.from_name(key)

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
