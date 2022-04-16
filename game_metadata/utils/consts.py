from enum import Flag, auto


# Card Consts
RARITY_ALIASES: dict[str, str] = {
    'common': "C",
    'uncommon': "U",
    'rare': "R",
    'mythic': "M"
}


# https://scryfall.com/docs/api/layouts
class CardLayouts(Flag):
    NORMAL = auto()
    SPLIT = auto()
    FLIP = auto()
    TRANSFORM = auto()
    MODAL_DFC = auto()
    MELD = auto()
    LEVELER = auto()
    CLASS = auto()
    SAGA = auto()
    ADVENTURE = auto()

    TWO_SIDED = TRANSFORM | MODAL_DFC
    FUSED = ADVENTURE | SPLIT | FLIP


LAYOUT_DICT = {
    "normal": CardLayouts.NORMAL,
    "split": CardLayouts.SPLIT,
    "flip": CardLayouts.FLIP,
    "transform": CardLayouts.TRANSFORM,
    "modal_dfc": CardLayouts.MODAL_DFC,
    "meld": CardLayouts.MELD,
    "leveler": CardLayouts.LEVELER,
    "class": CardLayouts.CLASS,
    "saga": CardLayouts.SAGA,
    "adventure": CardLayouts.ADVENTURE
}
