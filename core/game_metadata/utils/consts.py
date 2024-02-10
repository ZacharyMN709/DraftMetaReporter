"""
Contains constants about magic cards and arena ranks.

Key things outlined are:
 - Card Templating (Split, Adventure, etc.)
 - Card Rarity (Rarity list, Aliases, Indexes for sorting)
 - Types (Supertypes, Types, and Subtypes, split by Type)
 - Arena Ranks (Bronze - Mythic)
"""

import typing
from enum import Flag, auto
from core.game_metadata.utils.typing import *

# Event Data Text Format
DATE_FMT = "%b %d, %Y"


# Arena Rank Consts
RANKS: list[RANK] = ['None', 'Bronze', 'Silver', 'Gold', 'Platinum', 'Diamond', 'Mythic']


# region Rarity
RARITIES: list[RARITY] = ['M', 'R', 'U', 'C']

RARITY_ALIASES: dict[str, RARITY] = {
    'common': "C",
    'uncommon': "U",
    'rare': "R",
    'mythic': "M",
    # TODO: See if there's a better way to handle this.
    'basic': "C"  # This comes from arena, for common lands in draft packs.
}

RARITY_INDEXES: dict[RARITY, int] = {
    "C": 0,
    "U": 1,
    "R": 2,
    "M": 3,
}
# endregion Rarity


# region Card Types
# Extracting the card types from the data type definitions.
SUPERTYPES: set[SUPERTYPE] = set(typing.get_args(SUPERTYPE))
TYPES: set[TYPE] = set(typing.get_args(TYPE))
LAND_SUBTYPES: set[LAND_SUBTYPE] = set(typing.get_args(LAND_SUBTYPE))
CREATURE_SUBTYPES: set[CREATURE_SUBTYPE] = set(typing.get_args(CREATURE_SUBTYPE))
ARTIFACT_SUBTYPES: set[ARTIFACT_SUBTYPE] = set(typing.get_args(ARTIFACT_SUBTYPE))
ENCHANTMENT_SUBTYPES: set[ENCHANTMENT_SUBTYPE] = set(typing.get_args(ENCHANTMENT_SUBTYPE))
PLANESWALKER_SUBTYPES: set[PLANESWALKER_SUBTYPE] = set(typing.get_args(PLANESWALKER_SUBTYPE))
INSTANT_SUBTYPES: set[INSTANT_SUBTYPE] = set(typing.get_args(INSTANT_SUBTYPE))
SORCERY_SUBTYPES: set[SORCERY_SUBTYPE] = set(typing.get_args(SORCERY_SUBTYPE))
BATTLE_SUBTYPES: set[SORCERY_SUBTYPE] = set(typing.get_args(BATTLE_SUBTYPE))
SUBTYPES: set[SUBTYPE] = LAND_SUBTYPES | CREATURE_SUBTYPES | ARTIFACT_SUBTYPES | ENCHANTMENT_SUBTYPES | \
                     PLANESWALKER_SUBTYPES | INSTANT_SUBTYPES | SORCERY_SUBTYPES | BATTLE_SUBTYPES

SUBTYPE_DICT: dict[TYPE, set[SUBTYPE]] = {
    "Land": LAND_SUBTYPES,
    "Creature": CREATURE_SUBTYPES,
    "Artifact": ARTIFACT_SUBTYPES,
    "Enchantment": ENCHANTMENT_SUBTYPES,
    "Planeswalker": PLANESWALKER_SUBTYPES,
    "Instant": INSTANT_SUBTYPES,
    "Sorcery": SORCERY_SUBTYPES
}
# endregion Card Types


# region Card Layouts
# https://scryfall.com/docs/api/layouts
class CardLayouts(Flag):
    NORMAL = auto()
    SPLIT = auto()
    FLIP = auto()
    TRANSFORM = auto()
    MODAL_DFC = auto()
    MELD = auto()
    LEVELER = auto()
    CASE = auto()
    CLASS = auto()
    SAGA = auto()
    ADVENTURE = auto()
    PROTOTYPE = auto()
    BATTLE = auto()
    MUTATE = auto()

    BASIC = NORMAL | LEVELER | CASE | CLASS | SAGA | MUTATE
    FUSED = ADVENTURE | SPLIT | FLIP | PROTOTYPE
    TWO_SIDED = TRANSFORM | MODAL_DFC | MELD | BATTLE


LAYOUT_DICT: dict[str, CardLayouts] = {
    "normal": CardLayouts.NORMAL,
    "split": CardLayouts.SPLIT,
    "flip": CardLayouts.FLIP,
    "transform": CardLayouts.TRANSFORM,
    "modal_dfc": CardLayouts.MODAL_DFC,
    "meld": CardLayouts.MELD,
    "leveler": CardLayouts.LEVELER,
    "case": CardLayouts.CASE,
    "class": CardLayouts.CLASS,
    "saga": CardLayouts.SAGA,
    "adventure": CardLayouts.ADVENTURE,
    "prototype": CardLayouts.PROTOTYPE,
    "battle": CardLayouts.BATTLE,
    "mutate": CardLayouts.MUTATE
}
# endregion Card Layouts
