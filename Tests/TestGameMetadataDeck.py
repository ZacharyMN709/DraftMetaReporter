import unittest
from datetime import date

from wubrg import COLOR_COMBINATIONS
from game_metadata.utils.consts import CardLayouts
from game_metadata.GameMetadata import SetMetadata, FormatMetadata
from game_metadata.RequestScryfall import RequestScryfall, trap_error
from game_metadata.GameObjects.Card import Card, CardManager
from game_metadata.GameObjects.Deck import Deck, LimitedDeck
from game_metadata.GameObjects.Draft import Draft, Pack


class TestDeck(unittest.TestCase):
    pass


class TestDeckManager(unittest.TestCase):
    pass
