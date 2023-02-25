import unittest
import json

from core.utilities import validate_json
from core.data_requesting.utils.settings import TRIES, FAIL_DELAY, SUCCESS_DELAY
from core.data_requesting import Requester, RequestScryfall, Request17Lands

from Tests.settings import _tries, _fail_delay, _success_delay, TEST_MASS_DATA_PULL


class TestRequester(unittest.TestCase):
    REQUESTER = Requester(_tries, _fail_delay, _success_delay)

    def test_default_init(self):
        fetcher = Requester()
        self.assertEqual(fetcher._TRIES, TRIES)
        self.assertEqual(fetcher._FAIL_DELAY, FAIL_DELAY)
        self.assertEqual(fetcher._SUCCESS_DELAY, SUCCESS_DELAY)

    def test_arg_init(self):
        fetcher = Requester(2, 120, 10)
        self.assertEqual(fetcher._TRIES, 2)
        self.assertEqual(fetcher._FAIL_DELAY, 120)
        self.assertEqual(fetcher._SUCCESS_DELAY, 10)

    def test_valid_url(self):
        ret = self.REQUESTER.request('https://api.scryfall.com/')
        self.assertIsNone(ret)

    def test_invalid_url(self):
        ret = self.REQUESTER.request('Hello World')
        self.assertIsNone(ret)


class TestRequestScryfall(unittest.TestCase):
    REQUESTER = RequestScryfall(_tries, _fail_delay, _success_delay)

    def test_get_set_cards_valid(self):
        cards = self.REQUESTER.get_set_cards('NEO')
        self.assertIsInstance(cards, list)
        self.assertEqual(cards[0]['name'], 'Ancestral Katana')

    def test_get_set_review_valid(self):
        cards = self.REQUESTER.get_set_review_order('NEO')
        self.assertIsInstance(cards, list)
        self.assertEqual(cards[0]['name'], 'Hotshot Mechanic')

    def test_get_set_cards_invalid(self):
        ret = self.REQUESTER.get_set_cards('INVALID')
        self.assertListEqual(list(), ret)

    def test_get_set_info_valid(self):
        cards = self.REQUESTER.get_set_info('NEO')
        self.assertIsInstance(cards, tuple)

    def test_get_set_info_invalid(self):
        _set, _icon = self.REQUESTER.get_set_info('INVALID')
        self.assertIsNone(_set)
        self.assertIsNone(_icon)

    def test_get_card_by_name_valid(self):
        card = self.REQUESTER.get_card_by_name('Virus Beetle')
        self.assertIsInstance(card, dict)
        self.assertEqual(card['object'], 'card')
        self.assertEqual(card['name'], 'Virus Beetle')

    def test_get_card_by_name_valid_misspelled(self):
        card = self.REQUESTER.get_card_by_name('Vires Beetle')
        self.assertIsInstance(card, dict)
        self.assertEqual(card['object'], 'card')
        self.assertEqual(card['name'], 'Virus Beetle')

    def test_get_card_by_name_multiple(self):
        name = 'Bolt'
        card = self.REQUESTER.get_card_by_name(name)
        self.assertIsInstance(card, dict)
        self.assertEqual(card['err_msg'], f'Error: Multiple card matches for "{name}"')

    def test_get_card_by_name_dne(self):
        name = 'Supercalifragilisticexpialidocious'
        card = self.REQUESTER.get_card_by_name(name)
        self.assertIsInstance(card, dict)
        self.assertEqual(card['err_msg'], f'Error: Cannot find card "{name}"')

    @unittest.skipUnless(TEST_MASS_DATA_PULL, "Not testing mass data functions. 'TEST_MASS_DATA_PULL' set to False.")
    def test_get_bulk_data(self):
        data = self.REQUESTER.get_bulk_data()
        self.assertIsInstance(data, list)
        json_str = json.dumps(data)
        self.assertTrue(validate_json(json_str))

    @unittest.skipUnless(TEST_MASS_DATA_PULL, "Not testing mass data functions. 'TEST_MASS_DATA_PULL' set to False.")
    def test_get_arena_cards(self):
        data = self.REQUESTER.get_arena_cards()
        self.assertIsInstance(data, list)
        json_str = json.dumps(data)
        self.assertTrue(validate_json(json_str))


class TestRequestRequest17Lands(unittest.TestCase):
    REQUESTER = Request17Lands(_tries, _fail_delay, _success_delay)

    def test_(self):
        pass

    def test_get_deck(self):
        deck = self.REQUESTER.get_deck('Fish')
        self.assertIsNone(deck)

        _id = 'f5383f215c364c129632cdc559f0ac3a'
        deck = self.REQUESTER.get_deck(_id)
        self.assertIsInstance(deck, dict)
        self.assertIsInstance(deck['event_info'], dict)
        self.assertIsInstance(deck['groups'], list)
        self.assertIsInstance(deck['groups'][0], dict)
        self.assertIsInstance(deck['groups'][0]['cards'], list)
        self.assertIsInstance(deck['groups'][0]['cards'][0], dict)

        self.assertEqual(deck['text_link'], f'/deck/{_id}/0.txt')
        self.assertEqual(deck['builder_link'], f'https://sealeddeck.tech/17lands/deck/{_id}/0')
        self.assertEqual(deck['event_info']['expansion'], 'ONE')
        self.assertEqual(deck['event_info']['format'], 'PremierDraft')
        self.assertEqual(deck['groups'][0]['name'], 'Maindeck')
        self.assertEqual(deck['groups'][1]['name'], 'Sideboard')
        self.assertEqual(deck['groups'][0]['cards'][0]['name'], 'Axiom Engraver')

        deck = self.REQUESTER.get_deck(_id, 1)
        self.assertIsInstance(deck, dict)
        self.assertEqual(deck['text_link'], f'/deck/{_id}/1.txt')
        self.assertEqual(deck['builder_link'], f'https://sealeddeck.tech/17lands/deck/{_id}/1')

    def test_get_details(self):
        details = self.REQUESTER.get_details('Fish')
        self.assertIsNone(details)

        details = self.REQUESTER.get_details('f5383f215c364c129632cdc559f0ac3a')
        self.assertIsInstance(details, dict)
        self.assertIsInstance(details['event_course'], dict)
        self.assertIsInstance(details['match_results'], list)
        self.assertIsInstance(details['match_results'][0], dict)
        self.assertIsInstance(details['match_results'][0]['game_results'], list)
        self.assertIsInstance(details['match_results'][0]['game_results'][0], dict)

        self.assertEqual(details['expansion'], 'ONE')
        self.assertEqual(details['format'], 'PremierDraft')
        self.assertEqual(details['wins'], 7)
        self.assertEqual(details['losses'], 2)
        self.assertEqual(details['start_rank'], 'Platinum-4')
        self.assertEqual(details['end_rank'], 'Platinum-3')

        self.assertEqual(details['event_course']['wins'], 7)
        self.assertEqual(details['event_course']['losses'], 2)

    def test_get_draft(self):
        draft = self.REQUESTER.get_draft('Fish')
        self.assertIsNone(draft)

        draft = self.REQUESTER.get_draft('f5383f215c364c129632cdc559f0ac3a')
        self.assertIsInstance(draft, dict)
        self.assertEqual(draft['expansion'], 'ONE')
        self.assertIsInstance(draft['picks'], list)

        pick = draft['picks'][0]
        self.assertIsInstance(pick, dict)
        self.assertIsInstance(pick['pick'], dict)
        self.assertIsInstance(pick['available'], list)
        self.assertIsInstance(pick['available'][0], dict)

        self.assertEqual(pick['pack_number'], 0)
        self.assertEqual(pick['pick_number'], 0)
        self.assertEqual(pick['pick']['name'], 'Solphim, Mayhem Dominus')
        self.assertEqual(pick['available'][0]['name'], 'Solphim, Mayhem Dominus')

    def test_get_tier_list(self):
        tiers = self.REQUESTER.get_tier_list('Fish')
        self.assertIsInstance(tiers, list)
        self.assertEqual(len(tiers), 0)

        tiers = self.REQUESTER.get_tier_list('45a3a3a84d9f46178d6750ff96d85f8c')
        self.assertIsInstance(tiers, list)
        self.assertIsInstance(tiers[0], dict)
        self.assertEqual(len(tiers), 261)
