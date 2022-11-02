import unittest
from datetime import date

from Utilities.utils.funcs import load_json_file
from Utilities.auto_logging import auto_log, LogLvl
from wubrg import COLOR_COMBINATIONS

from game_metadata.utils.consts import CardLayouts
from game_metadata.GameMetadata import SetMetadata, FormatMetadata
from game_metadata.RequestScryfall import RequestScryfall, trap_error
from game_metadata.GameObjects.Card import Card, CardManager
from game_metadata.GameObjects.Deck import Deck, LimitedDeck
from game_metadata.GameObjects.Draft import Draft, Pick


class TestBaseDraft(unittest.TestCase):
    def setUp(self) -> None:
        auto_log(LogLvl.DEBUG)
        # Load all arena cards to speed up tests and reduce load on Scryfall server.
        CardManager.load_from_file()


class TestPick(TestBaseDraft):
    def eval_pick(self, pick):
        self.assertEqual(0, pick.pack_number)
        self.assertEqual(0, pick.pick_number)
        self.assertListEqual(list(), pick.pool)
        self.assertListEqual(list(), pick.cards_missing)
        self.assertEqual(14, len(pick.cards_available))
        self.assertEqual(Card.from_name("Llanowar Greenwidow"), pick.card_picked)

    def test_pick_init(self):
        file_path = r'C:\Users\Zachary\Coding\GitHub\DraftMetaReporter\Tests\Drafts'
        data = load_json_file(file_path, 'pick_1.json')
        pick = Pick(data)
        self.eval_pick(pick)


class TestDraft(TestBaseDraft):
    pass


class TestDraftManager(TestBaseDraft):
    pass
