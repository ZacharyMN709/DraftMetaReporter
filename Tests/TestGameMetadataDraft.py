import unittest
from datetime import date

from Utilities.utils.funcs import load_json_file
from Utilities.auto_logging import auto_log, LogLvl
from wubrg import COLOR_COMBINATIONS

from game_metadata.utils.consts import CardLayouts
from game_metadata.GameMetadata import SetMetadata, FormatMetadata
from game_metadata.RequestScryfall import RequestScryfall, trap_error
from game_metadata.game_objects.Card import Card, CardManager
from game_metadata.game_objects.Deck import LimitedDeck
from game_metadata.game_objects.Draft import Draft, Pick, DraftManager


class TestBaseDraft(unittest.TestCase):
    def setUp(self) -> None:
        auto_log(LogLvl.DEBUG)
        # Load all arena cards to speed up tests and reduce load on Scryfall server.
        CardManager.load_from_file()

    def eval_pick(self, pick):
        self.assertEqual(0, pick.pack_number)
        self.assertEqual(0, pick.pick_number)
        self.assertListEqual(list(), pick.pool)
        self.assertListEqual(list(), pick.cards_missing)
        self.assertEqual(14, len(pick.cards_available))
        self.assertEqual(Card.from_name("Llanowar Greenwidow"), pick.card_picked)

    def eval_draft(self, draft):
        self.assertEqual('0bea16f8b69c4ea1887d8bf15ed69f62', draft.DRAFT_ID)
        self.assertEqual('DMU', draft.SET)
        self.assertEqual('PremierDraft', draft.FORMAT)
        self.assertEqual('0bea16f8b69c4ea1887d8bf15ed69f62', draft.deck.DECK_ID)
        TestPick.eval_pick(self, draft.picks[0])


class TestPick(TestBaseDraft):
    def test_pick_init(self):
        file_path = r'C:\Users\Zachary\Coding\GitHub\DraftMetaReporter\Tests\Drafts'
        data = load_json_file(file_path, 'pick_1.json')
        pick = Pick(data)
        self.eval_pick(pick)


class TestDraft(TestBaseDraft):
    def test_draft_init(self):
        file_path = r'C:\Users\Zachary\Coding\GitHub\DraftMetaReporter\Tests\Drafts'
        data = load_json_file(file_path, 'draft_1.json')
        draft = Draft(data, '0bea16f8b69c4ea1887d8bf15ed69f62')
        self.eval_draft(draft)


class TestDraftManager(TestBaseDraft):
    def test_from_draft_id_valid(self):
        draft = DraftManager.from_draft_id("2c653e26dc0647ca934af503d57eee3d")
        self.assertIsInstance(draft, Draft)
        recall = DraftManager.from_draft_id("2c653e26dc0647ca934af503d57eee3d")
        self.assertEqual(draft, recall)

    def test_from_draft_id_invalid(self):
        draft = DraftManager.from_draft_id("TunaSandwich")
        self.assertIsNone(draft)
        recall = DraftManager.from_draft_id("TunaSandwich")
        self.assertEqual(draft, recall)

    def test_clear_blank_drafts(self):
        is_valid = True
        draft = DraftManager.from_draft_id("TunaSandwich")
        self.assertIsNone(draft)
        DraftManager.clear_blank_drafts()
        for draft in DraftManager.DRAFTS.values():
            is_valid = is_valid and draft is not None
        self.assertTrue(is_valid)

    def test_flush_cache(self):
        DraftManager.from_draft_id("2c653e26dc0647ca934af503d57eee3d")
        DraftManager.from_draft_id("TunaSandwich")
        DraftManager.flush_cache()
        self.assertFalse(DraftManager.SETS)
        self.assertFalse(DraftManager.DRAFTS)
