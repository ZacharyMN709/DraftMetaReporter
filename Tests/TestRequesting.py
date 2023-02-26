import unittest
import json

from core.utilities import validate_json
from core.wubrg import COLOR_COMBINATIONS
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
        ret = self.REQUESTER.get_json_response('https://api.scryfall.com/')
        self.assertIsNone(ret)

    def test_invalid_url(self):
        ret = self.REQUESTER.get_json_response('Hello World')
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

    def test_get_colors(self):
        colors = self.REQUESTER.get_colors()
        baseline: list = COLOR_COMBINATIONS.copy()
        baseline[0] = None
        self.assertListEqual(baseline, colors)

    def test_get_expansions(self):
        expansions = self.REQUESTER.get_expansions()
        self.assertIsInstance(expansions, list)
        self.assertTrue('ONE' in expansions)

    def test_get_event_types(self):
        events = self.REQUESTER.get_event_types()
        self.assertTrue('PremierDraft' in events)
        self.assertTrue('TradDraft' in events)
        self.assertTrue('QuickDraft' in events)
        self.assertTrue('Sealed' in events)
        self.assertTrue('TradSealed' in events)

    def test_get_deck(self):
        # Test a bad request
        deck = self.REQUESTER.get_deck('Fish')
        self.assertIsNone(deck)

        # Send a good request
        _id = 'f5383f215c364c129632cdc559f0ac3a'
        deck = self.REQUESTER.get_deck(_id)

        # Validate the structure
        self.assertIsInstance(deck, dict)
        self.assertIsInstance(deck['event_info'], dict)
        self.assertIsInstance(deck['groups'], list)
        self.assertIsInstance(deck['groups'][0], dict)
        self.assertIsInstance(deck['groups'][0]['cards'], list)
        self.assertIsInstance(deck['groups'][0]['cards'][0], dict)

        # Validate the contents
        self.assertEqual(deck['text_link'], f'/deck/{_id}/0.txt')
        self.assertEqual(deck['builder_link'], f'https://sealeddeck.tech/17lands/deck/{_id}/0')
        self.assertEqual(deck['event_info']['expansion'], 'ONE')
        self.assertEqual(deck['event_info']['format'], 'PremierDraft')
        self.assertEqual(deck['groups'][0]['name'], 'Maindeck')
        self.assertEqual(deck['groups'][1]['name'], 'Sideboard')
        self.assertEqual(deck['groups'][0]['cards'][0]['name'], 'Axiom Engraver')

        # Validate the other build
        deck = self.REQUESTER.get_deck(_id, 1)
        self.assertIsInstance(deck, dict)
        self.assertEqual(deck['text_link'], f'/deck/{_id}/1.txt')
        self.assertEqual(deck['builder_link'], f'https://sealeddeck.tech/17lands/deck/{_id}/1')

    def test_get_details(self):
        # Test a bad request
        details = self.REQUESTER.get_details('Fish')
        self.assertIsNone(details)

        # Send a good request
        details = self.REQUESTER.get_details('f5383f215c364c129632cdc559f0ac3a')

        # Validate the structure
        self.assertIsInstance(details, dict)
        self.assertIsInstance(details['event_course'], dict)
        self.assertIsInstance(details['match_results'], list)
        self.assertIsInstance(details['match_results'][0], dict)
        self.assertIsInstance(details['match_results'][0]['game_results'], list)
        self.assertIsInstance(details['match_results'][0]['game_results'][0], dict)

        # Validate the contents
        self.assertEqual(details['expansion'], 'ONE')
        self.assertEqual(details['format'], 'PremierDraft')
        self.assertEqual(details['wins'], 7)
        self.assertEqual(details['losses'], 2)
        self.assertEqual(details['start_rank'], 'Platinum-4')
        self.assertEqual(details['end_rank'], 'Platinum-3')
        self.assertEqual(details['event_course']['wins'], 7)
        self.assertEqual(details['event_course']['losses'], 2)

    def test_get_draft(self):
        # Test a bad request
        draft = self.REQUESTER.get_draft('Fish')
        self.assertIsNone(draft)

        # Send a good request
        draft = self.REQUESTER.get_draft('f5383f215c364c129632cdc559f0ac3a')

        # Validate the structure
        self.assertIsInstance(draft, dict)
        self.assertIsInstance(draft['picks'], list)
        self.assertIsInstance(draft['picks'][0], dict)
        self.assertIsInstance(draft['picks'][0]['pick'], dict)
        self.assertIsInstance(draft['picks'][0]['available'], list)
        self.assertIsInstance(draft['picks'][0]['available'][0], dict)

        # Validate the contents
        self.assertEqual(draft['expansion'], 'ONE')
        self.assertEqual(draft['picks'][0]['pack_number'], 0)
        self.assertEqual(draft['picks'][0]['pick_number'], 0)
        self.assertEqual(draft['picks'][0]['pick']['name'], 'Solphim, Mayhem Dominus')
        self.assertEqual(draft['picks'][0]['available'][0]['name'], 'Solphim, Mayhem Dominus')

    def test_get_tier_list(self):
        # Test a bad request
        tiers = self.REQUESTER.get_tier_list('Fish')
        self.assertIsNone(tiers)

        # Send a good request
        tiers = self.REQUESTER.get_tier_list('45a3a3a84d9f46178d6750ff96d85f8c')

        # Validate the structure
        self.assertIsInstance(tiers, list)
        self.assertIsInstance(tiers[0], dict)
        self.assertIsInstance(tiers[0]['flags'], dict)

        # Validate the contents
        self.assertEqual(len(tiers), 261)
        self.assertEqual(tiers[0]['name'], 'Against All Odds')
        self.assertEqual(tiers[0]['tier'], 'C-')
        self.assertEqual(tiers[0]['comment'], '')
        self.assertEqual(tiers[0]['flags']['sideboard'], False)
        self.assertEqual(tiers[0]['flags']['synergy'], False)
        self.assertEqual(tiers[0]['flags']['buildaround'], False)
