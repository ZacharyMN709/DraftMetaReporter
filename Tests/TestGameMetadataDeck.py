import unittest
from datetime import date

from wubrg import COLOR_COMBINATIONS
from Utilities.auto_logging import auto_log, LogLvl

from game_metadata.utils.consts import CardLayouts
from game_metadata.GameMetadata import SetMetadata, FormatMetadata
from game_metadata.RequestScryfall import RequestScryfall, trap_error
from game_metadata.GameObjects.Card import Card, CardManager
from game_metadata.GameObjects.Deck import Deck, LimitedDeck, ConstructedDeck, TrophyStub, DeckManager
from game_metadata.GameObjects.Draft import Draft, Pack


class TestBaseDeck(unittest.TestCase):
    def setUp(self) -> None:
        auto_log(LogLvl.DEBUG)
        # Load all arena cards to speed up tests and reduce load on Scryfall server.
        CardManager.load_from_file()


class TestDeck(TestBaseDeck):
    def test_parse_decklist_from_file_e3(self):
        loc = r"C:\Users\Zachary\Coding\GitHub\DraftMetaReporter\Tests\DeckLists\E3.txt"
        maindeck, sideboard = Deck.parse_decklist_from_file(loc)

        self.assertEqual(60, len(maindeck))
        self.assertEqual(15, len(sideboard))

    def test_parse_decklist_from_file_e1(self):
        loc = r"C:\Users\Zachary\Coding\GitHub\DraftMetaReporter\Tests\DeckLists\E1.txt"
        maindeck, sideboard = Deck.parse_decklist_from_file(loc)

        self.assertEqual(60, len(maindeck))
        self.assertEqual(0, len(sideboard))

    def test_parse_decklist_comparison(self):
        loc_bo3 = r"C:\Users\Zachary\Coding\GitHub\DraftMetaReporter\Tests\DeckLists\H3.txt"
        maindeck, sideboard = Deck.parse_decklist_from_file(loc_bo3)
        deck_bo3 = Deck(maindeck, sideboard, 'Azorius Affinity', 0, 0)

        loc_bo1 = r"C:\Users\Zachary\Coding\GitHub\DraftMetaReporter\Tests\DeckLists\H1.txt"
        maindeck, sideboard = Deck.parse_decklist_from_file(loc_bo1)
        deck_bo1 = Deck(maindeck, sideboard, 'Azorius Affinity', 0, 0)

        self.assertEqual(60, len(deck_bo3.maindeck))
        self.assertEqual(15, len(deck_bo3.sideboard))
        self.assertEqual(60, len(deck_bo1.maindeck))

        maindeck_diff, sideboard_diff = deck_bo3 - deck_bo1
        print(maindeck_diff)
        print(sideboard_diff)

        maindeck_comp = {
            "Soul-Guide Lantern": -2,
            "Karn, Scion of Urza": 2
        }

        sideboard_comp = {
            "Karn, Scion of Urza": 1,
            "Sai, Master Thopterist": 2,
            "Dovin's Veto": 3,
            "Mystical Dispute": 1,
            "Soul-Guide Lantern": 2,
            "Glass Casket": 4,
            "Unlicensed Hearse": 1,
            "Skysovereign, Consul Flagship": 1,
        }

        self.assertDictEqual(maindeck_comp, maindeck_diff)
        self.assertDictEqual(sideboard_comp, sideboard_diff)

    def test_parse_decklist_from_file_invalid(self):
        loc = r"C:\Users\Zachary\Coding\GitHub\DraftMetaReporter\Tests\DeckLists\DNE.txt"
        self.assertRaises(ValueError, Deck.parse_decklist_from_file, loc)

    def test_parse_decklist_from_url(self):
        loc = r"https:/DNE.html"
        self.assertRaises(NotImplementedError, Deck.parse_decklist_from_url, loc)

    def test_mangled_parse(self):
        decklist = """
4 Liliana of the Veil (DMU)
4 Stitcher's Supplier
Raffine's Informant
4 (NEO) 220"""

        maindeck, sideboard = Deck.parse_decklist(decklist.split('\n'))
        print(maindeck)
        self.assertEqual(9, len(maindeck))
        self.assertEqual(0, len(sideboard))

    def test_deck_simple_init(self):
        deck = Deck([Card.from_name('Island')], [], 'Test Deck', 0, 0)
        self.assertEqual(1, len(deck.maindeck))
        self.assertEqual(0, len(deck.sideboard))
        self.assertEqual(1, len(deck.cardpool))
        self.assertEqual('Test Deck', deck.name)
        self.assertEqual(0, deck.wins)
        self.assertEqual(0, deck.losses)
        self.assertEqual(0, deck.win_rate)
        self.assertEqual(1, len(deck._maindeck_dict))
        self.assertEqual(0, len(deck._sideboard_dict))

        self.assertIsInstance(deck.maindeck[0], Card)
        self.assertEqual(1, deck._maindeck_dict['Island'])

    def test_deck_from_file(self):
        loc = r"C:\Users\Zachary\Coding\GitHub\DraftMetaReporter\Tests\DeckLists\E3.txt"
        maindeck, sideboard = Deck.parse_decklist_from_file(loc)
        deck = Deck(maindeck, sideboard, 'Mono-Blue Spirits', 3, 1)

        self.assertEqual(60, len(deck.maindeck))
        self.assertEqual(15, len(deck.sideboard))
        self.assertEqual(75, len(deck.cardpool))
        self.assertEqual('Mono-Blue Spirits', deck.name)
        self.assertEqual(3, deck.wins)
        self.assertEqual(1, deck.losses)
        self.assertEqual(75.0, deck.win_rate)
        self.assertEqual(13, len(deck._maindeck_dict))
        self.assertEqual(8, len(deck._sideboard_dict))
        self.assertEqual(21, len(deck.unique_cards))


class TestConstructedDeck(TestBaseDeck):
    def test_deck_from_file(self):
        loc = r"C:\Users\Zachary\Coding\GitHub\DraftMetaReporter\Tests\DeckLists\E3.txt"
        maindeck, sideboard = Deck.parse_decklist_from_file(loc)
        deck = ConstructedDeck(maindeck, sideboard, 'Mono-Blue Spirits', 3, 1)

        self.assertEqual(60, len(deck.maindeck))
        self.assertEqual(15, len(deck.sideboard))
        self.assertEqual(75, len(deck.cardpool))
        self.assertEqual('Mono-Blue Spirits', deck.name)
        self.assertEqual(3, deck.wins)
        self.assertEqual(1, deck.losses)
        self.assertEqual(75.0, deck.win_rate)
        self.assertEqual(13, len(deck._maindeck_dict))
        self.assertEqual(8, len(deck._sideboard_dict))
        self.assertEqual(21, len(deck.unique_cards))
        self.assertTrue(deck.is_valid)
        self.assertRaises(NotImplementedError, deck._calc_colors)


class TestLimitedDeck(TestBaseDeck):
    pass


class TestTrophyStub(TestBaseDeck):
    pass


class TestDeckManager(TestBaseDeck):
    pass
