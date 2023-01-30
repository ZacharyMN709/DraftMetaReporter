import datetime
import unittest
import requests
from requests import Response

from utilities.auto_logging import auto_log, LogLvl
from Tests.settings import TEST_PERIPHERAL_URLS, FULL_TEST

from data_interface.Request17Lands import Request17Lands
from game_metadata.game_objects.Card import Card, CardManager
from game_metadata.game_objects.Deck import Deck, LimitedDeck, ConstructedDeck, TrophyStub, DeckManager
from game_metadata.game_objects.Draft import Draft


class TestBaseDeck(unittest.TestCase):
    def setUp(self) -> None:
        auto_log(LogLvl.DEBUG)
        # Load all arena cards to speed up tests and reduce load on Scryfall server.
        CardManager.load_cache_from_file()


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

        maindeck_comp = {
            CardManager.from_name("Soul-Guide Lantern"): -2,
            CardManager.from_name("Karn, Scion of Urza"): 2
        }

        sideboard_comp = {
            CardManager.from_name("Karn, Scion of Urza"): 1,
            CardManager.from_name("Sai, Master Thopterist"): 2,
            CardManager.from_name("Dovin's Veto"): 3,
            CardManager.from_name("Mystical Dispute"): 1,
            CardManager.from_name("Soul-Guide Lantern"): 2,
            CardManager.from_name("Glass Casket"): 4,
            CardManager.from_name("Unlicensed Hearse"): 1,
            CardManager.from_name("Skysovereign, Consul Flagship"): 1,
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
        self.assertEqual(1, deck._maindeck_dict[CardManager.from_name('Island')])

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
    @staticmethod
    def gen_deck(deck_id) -> LimitedDeck:
        caller = Request17Lands()
        deck_json = caller.get_deck(deck_id, 0)
        deck = LimitedDeck(deck_json)
        return deck

    def validate_deck(self, deck):
        self.assertEqual(40, len(deck.maindeck))
        self.assertEqual(17, len(deck.sideboard))
        # TODO: Consider removing lands from the card pool?
        self.assertEqual(57, len(deck.cardpool))
        self.assertEqual(5, deck.wins)
        self.assertEqual(3, deck.losses)

        self.assertEqual("b20a97b818f3418b94a8f4e7584398a8", deck.DECK_ID)
        self.assertEqual(1, deck.deck_builds)
        self.assertEqual(0, deck.selected_build)
        self.assertEqual('DMU', deck.SET)
        self.assertEqual('PremierDraft', deck.FORMAT)
        self.assertTrue(deck.is_valid)
        self.assertFalse(deck.has_trophy_stub)
        self.assertRaises(NotImplementedError, deck._calc_colors)

    def test_limited_deck_init(self):
        deck = self.gen_deck("b20a97b818f3418b94a8f4e7584398a8")
        self.validate_deck(deck)

    @unittest.skipUnless(TEST_PERIPHERAL_URLS, "Not testing peripheral links. 'TEST_PERIPHERAL_URLS' set to False.")
    def test_link_properties(self):
        def handle_link(link):
            resp: Response = requests.get(link)
            self.assertIsNotNone(resp)
            self.assertEqual(200, resp.status_code)

        deck = self.gen_deck("b20a97b818f3418b94a8f4e7584398a8")

        handle_link(deck.details_link)
        handle_link(deck.pool_link)
        handle_link(deck.draft_link)
        handle_link(deck.builder_link)
        handle_link(deck.deck_link)
        handle_link(deck.text_link)

    def test_relay(self):
        deck = LimitedDeck.from_id("b20a97b818f3418b94a8f4e7584398a8")
        self.validate_deck(deck)

    def test_get_draft(self):
        deck = LimitedDeck.from_id("b20a97b818f3418b94a8f4e7584398a8")
        draft = deck.draft
        self.assertIsNotNone(draft)
        self.assertIsInstance(draft, Draft)


class TestTrophyStub(TestBaseDeck):
    def validate_trophy_stub(self, trophy, data):
        rank = TrophyStub.parse_simple_rank(data['start_rank'], data['end_rank'])

        self.assertEqual(data['aggregate_id'], trophy.DECK_ID)
        self.assertEqual(data['start_rank'], trophy.start_rank)
        self.assertEqual(data['end_rank'], trophy.end_rank)
        self.assertEqual(rank, trophy.rank)
        self.assertEqual(data['deck_index'], trophy.deck_idx)
        self.assertIsInstance(trophy.time, datetime.datetime)

    def test_get_trophy_deck_list(self):
        requester = Request17Lands()
        data = requester.get_trophy_deck_metadata('DMU')

        self.assertIsInstance(data, list)
        self.assertIsInstance(data[0], dict)
        self.assertEqual(500, len(data))

    def test_options_switch(self):
        import data_interface.utils.settings as settings

        requester = Request17Lands()

        self.assertEqual(settings.DEFAULT_FORMAT, 'PremierDraft')
        bo1 = requester.get_trophy_deck_metadata('DMU')

        settings.DEFAULT_FORMAT = 'TradDraft'
        self.assertEqual(settings.DEFAULT_FORMAT, 'TradDraft')
        bo3 = requester.get_trophy_deck_metadata('DMU')

        settings.DEFAULT_FORMAT = 'PremierDraft'
        self.assertEqual(settings.DEFAULT_FORMAT, 'PremierDraft')

        self.assertEqual(500, len(bo1))
        self.assertEqual(500, len(bo3))
        self.assertNotEqual(bo1[0]['aggregate_id'], bo3[0]['aggregate_id'])

    def test_trophy_stub_init(self):
        data_1 = {
            'wins': 7,
            'losses': 1,
            'start_rank': 'Silver-4',
            'end_rank': 'Silver-2',
            'colors': 'WBR',
            'aggregate_id': '2c653e26dc0647ca934af503d57eee3d',
            'deck_index': 4,
            'time': '2022-11-01 13:18'
        }

        trophy = TrophyStub(data_1)
        self.validate_trophy_stub(trophy, data_1)

        data_2 = {
            'wins': 7,
            'losses': 1,
            'start_rank': 'Gold-4',
            'end_rank': 'Silver-3',
            'colors': 'WUBG',
            'aggregate_id': '4163636bf1b044fdb2e78433eba333ff',
            'deck_index': 1,
            'time': '2022-11-01 21:47'
        }

        trophy = TrophyStub(data_2)
        self.validate_trophy_stub(trophy, data_2)

    def test_get_deck(self):
        data = {
            'wins': 7,
            'losses': 1,
            'start_rank': 'Silver-4',
            'end_rank': 'Silver-2',
            'colors': 'WBR',
            'aggregate_id': '2c653e26dc0647ca934af503d57eee3d',
            'deck_index': 4,
            'time': '2022-11-01 13:18'
        }

        trophy = TrophyStub(data)
        deck = trophy.deck

        self.assertEqual("2c653e26dc0647ca934af503d57eee3d", deck.DECK_ID)
        self.assertEqual('DMU', deck.SET)
        self.assertEqual('PremierDraft', deck.FORMAT)
        self.assertTrue(deck.is_valid)
        self.assertTrue(deck.has_trophy_stub)

    @unittest.skipUnless(FULL_TEST, "Not performing full test. 'FULL_TEST' set to False.")
    def test_mass_gen(self):
        import data_interface.utils.settings as settings

        requester = Request17Lands()

        def convert_data(data_list):
            for data in data_list:
                try:
                    trophy = TrophyStub(data)
                    self.validate_trophy_stub(trophy, data)
                except:  # pragma: nocover
                    # If the trophy stub can't be handled, some possible oddities in data need to be better handled.
                    print(data)

        self.assertEqual(settings.DEFAULT_FORMAT, 'PremierDraft')
        bo1 = requester.get_trophy_deck_metadata('DMU')
        convert_data(bo1)

        settings.DEFAULT_FORMAT = 'TradDraft'
        self.assertEqual(settings.DEFAULT_FORMAT, 'TradDraft')
        bo3 = requester.get_trophy_deck_metadata('DMU')
        convert_data(bo3)

        settings.DEFAULT_FORMAT = 'PremierDraft'
        self.assertEqual(settings.DEFAULT_FORMAT, 'PremierDraft')


class TestDeckManager(TestBaseDeck):
    def test_from_deck_id_valid(self):
        deck = DeckManager.from_deck_id("2c653e26dc0647ca934af503d57eee3d")
        self.assertIsInstance(deck, LimitedDeck)

    def test_from_deck_id_invalid(self):
        deck = DeckManager.from_deck_id("TunaSandwich")
        self.assertIsNone(deck)

    def test_clear_blank_decks(self):
        is_valid = True
        DeckManager.from_deck_id("2c653e26dc0647ca934af503d57eee3d")
        deck = DeckManager.from_deck_id("TunaSandwich")
        self.assertIsNone(deck)
        DeckManager.clear_blank_decks()
        for deck in DeckManager.DECKS.values():
            is_valid = is_valid and deck is not None
        self.assertTrue(is_valid)

    def test_flush_cache(self):
        DeckManager.from_deck_id("2c653e26dc0647ca934af503d57eee3d")
        DeckManager.from_deck_id("TunaSandwich")
        DeckManager.flush_cache()
        self.assertFalse(DeckManager.SETS)
        self.assertFalse(DeckManager.DECKS)
