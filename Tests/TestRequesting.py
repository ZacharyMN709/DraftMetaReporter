from typing import Optional
import unittest
import json
from requests import Response

from core.utilities import validate_json
from core.wubrg import COLOR_COMBINATIONS
from core.data_requesting.utils.settings import TRIES, FAIL_DELAY, SUCCESS_DELAY
from core.data_requesting import Requester, RequestScryfall, Request17Lands

from Tests.settings import _tries, _fail_delay, _success_delay, TEST_MASS_DATA_PULL


class TestRequester(unittest.TestCase):
    REQUESTER = Requester(_tries, _fail_delay, _success_delay)

    def test_init(self):
        # Tests default initialization
        fetcher = Requester()
        self.assertEqual(fetcher._TRIES, TRIES)
        self.assertEqual(fetcher._FAIL_DELAY, FAIL_DELAY)
        self.assertEqual(fetcher._SUCCESS_DELAY, SUCCESS_DELAY)

        # Tests initialization.
        fetcher = Requester(2, 120, 10)
        self.assertEqual(fetcher._TRIES, 2)
        self.assertEqual(fetcher._FAIL_DELAY, 120)
        self.assertEqual(fetcher._SUCCESS_DELAY, 10)

    def test_request(self):
        # This uses 200 as a valid code by default, and the url should return a 400 code, ultimately scrubbing the
        #  response in favour of None.
        response = self.REQUESTER.request('https://api.scryfall.com/')
        self.assertIsNone(response)

        # Test that changing the list of code accepted allows this to return a response.
        requester = Requester(_tries, _fail_delay, _success_delay, [200, 400])
        response = requester.request('https://api.scryfall.com/')
        self.assertIsInstance(response, Response)

        # This should throw an error inside the function, which is caught, and then suppressed, returning None.
        ret = self.REQUESTER.request('Hello World')
        self.assertIsNone(ret)

    def test_get_response(self):
        # Use a bad url to test the retry mechanism.
        response = self.REQUESTER.request('https://api.scryfall.com/')
        self.assertIsNone(response)

        # Use a good url, with parameters, to test that a response is returned
        url = 'https://api.scryfall.com/cards/5a70e8fa-b71d-441e-b049-dacb09a9a7af'
        params = {
            'format': 'json',
            'pretty': True
        }
        response = self.REQUESTER.get_response(url, params)
        self.assertIsInstance(response, Response)

    def test_get_json_response(self):
        # Use a good url, with parameters, to test that a json response is returned.
        url = 'https://api.scryfall.com/cards/5a70e8fa-b71d-441e-b049-dacb09a9a7af'
        params = {
            'format': 'json',
            'pretty': True
        }
        response = self.REQUESTER.get_json_response(url, params)
        self.assertIsInstance(response, dict)

        # Use a valid url, but one that doesn't return json to test error handling.
        response = self.REQUESTER.get_json_response('https://www.google.com/')
        self.assertIsNone(response)

    def test_get_paginated_response(self):
        pass

    def test_get_paginated_json_response(self):
        pass


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

    def test_get_colors(self):
        # Get some baselines to help handle data.
        baseline: list = COLOR_COMBINATIONS.copy()
        baseline[0] = None

        # Make sure the color list matches what's expected.
        colors = self.REQUESTER.get_colors()
        self.assertListEqual(baseline, colors)

    def test_get_expansions(self):
        # Validate the payload, by checking if it contains some known sets.
        expansions = self.REQUESTER.get_expansions()
        self.assertIsInstance(expansions, list)
        self.assertTrue('ONE' in expansions)
        self.assertTrue('AFR' in expansions)
        self.assertTrue('KHM' in expansions)
        self.assertTrue('STX' in expansions)
        self.assertTrue('RNA' in expansions)

    def test_get_event_types(self):
        # Validate the payload, by checking if it contains the most important event types.
        events = self.REQUESTER.get_event_types()
        self.assertTrue('PremierDraft' in events)
        self.assertTrue('TradDraft' in events)
        self.assertTrue('QuickDraft' in events)
        self.assertTrue('Sealed' in events)
        self.assertTrue('TradSealed' in events)

    def test_get_play_draw_stats(self):
        # Validate the key parts of the structure, to make sure that changes in it haven't occurred.
        play_draw = self.REQUESTER.get_play_draw_stats()
        self.assertIsInstance(play_draw, list)
        self.assertIsInstance(play_draw[0], dict)
        self.assertIsInstance(play_draw[0]['expansion'], str)
        self.assertIsInstance(play_draw[0]['event_type'], str)
        self.assertIsInstance(play_draw[0]['average_game_length'], float)
        self.assertIsInstance(play_draw[0]['win_rate_on_play'], float)

    def test_get_color_ratings(self):
        # Validate the key parts of the structure, to make sure that changes in it haven't occurred.
        #  We don't check the length of the list, as multi-colour decks aren't guaranteed to show up, meaning the
        #  number of archetypes we have summaries on is variable.
        color_ratings = self.REQUESTER.get_color_ratings('ONE')
        self.assertIsInstance(color_ratings, list)
        self.assertIsInstance(color_ratings[0], dict)
        self.assertIsInstance(color_ratings[0]['is_summary'], bool)
        self.assertIsInstance(color_ratings[0]['color_name'], str)
        self.assertIsInstance(color_ratings[0]['wins'], int)
        self.assertIsInstance(color_ratings[0]['games'], int)

    def test_get_card_ratings(self):
        # Validate the key parts of the structure, to make sure that changes in it haven't occurred.
        #  We don't check any of the stats, as those are liable to change. Simply check that the number of cards in the
        #  data, and the first card returned is correct, and the data type otherwise.
        card_ratings = self.REQUESTER.get_card_ratings('ONE')
        self.assertIsInstance(card_ratings, list)
        self.assertIsInstance(card_ratings[0], dict)
        self.assertIsInstance(card_ratings[0]['seen_count'], int)
        self.assertIsInstance(card_ratings[0]['avg_seen'], float)
        self.assertIsInstance(card_ratings[0]['pick_count'], int)
        self.assertIsInstance(card_ratings[0]['avg_pick'], float)
        self.assertIsInstance(card_ratings[0]['game_count'], int)
        self.assertIsInstance(card_ratings[0]['win_rate'], float)
        self.assertIsInstance(card_ratings[0]['opening_hand_game_count'], int)
        self.assertIsInstance(card_ratings[0]['opening_hand_win_rate'], float)
        self.assertIsInstance(card_ratings[0]['drawn_game_count'], int)
        self.assertIsInstance(card_ratings[0]['drawn_win_rate'], float)
        self.assertIsInstance(card_ratings[0]['ever_drawn_game_count'], int)
        self.assertIsInstance(card_ratings[0]['ever_drawn_win_rate'], float)
        self.assertIsInstance(card_ratings[0]['never_drawn_game_count'], int)
        self.assertIsInstance(card_ratings[0]['never_drawn_win_rate'], float)
        self.assertIsInstance(card_ratings[0]['drawn_improvement_win_rate'], float)
        self.assertIsInstance(card_ratings[0]['name'], str)

        self.assertEqual(len(card_ratings), 265)
        self.assertEqual(card_ratings[0]['name'], 'Vorinclex, Monstrous Raider')

    def test_get_card_evaluations(self):
        # Validate the key parts of the structure, to make sure that changes in it haven't occurred.
        #  Card images are contained in the data, but we ignore them, so they aren't checked.
        card_evaluations = self.REQUESTER.get_card_evaluations('ONE')
        self.assertIsInstance(card_evaluations, dict)
        self.assertIsInstance(card_evaluations['cards'], list)
        self.assertIsInstance(card_evaluations['dates'], list)
        self.assertIsInstance(card_evaluations['data'], list)
        self.assertIsInstance(card_evaluations['cards'][0], str)
        self.assertIsInstance(card_evaluations['dates'][0], str)
        self.assertIsInstance(card_evaluations['data'][0], list)
        self.assertIsInstance(card_evaluations['data'][0][0], dict)
        self.assertIsInstance(card_evaluations['data'][0][0]['pick_n'], float)
        self.assertIsInstance(card_evaluations['data'][0][0]['pick_avg'], float)
        self.assertIsInstance(card_evaluations['data'][0][0]['seen_n'], float)
        self.assertIsInstance(card_evaluations['data'][0][0]['seen_avg'], float)

        self.assertEqual(card_evaluations['cards'][0], 'Vorinclex, Monstrous Raider')
        self.assertEqual(card_evaluations['dates'][0], '2023-02-02')

    def test_get_trophy_deck_metadata(self):
        # Test a bad request.
        trophy_deck_stubs = self.REQUESTER.get_trophy_deck_metadata('Fish')
        self.assertIsNone(trophy_deck_stubs)

        # Validate the key parts of the structure, to make sure that changes in it haven't occurred.
        trophy_deck_stubs = self.REQUESTER.get_trophy_deck_metadata('ONE')
        self.assertIsInstance(trophy_deck_stubs, list)
        self.assertIsInstance(trophy_deck_stubs[0], dict)

        # Since this data may change minute to minute, check the typing of the payload, instead of its contents.
        self.assertIsInstance(trophy_deck_stubs[0]['wins'], int)
        self.assertIsInstance(trophy_deck_stubs[0]['losses'], int)
        # Sometimes the rank is lost or isn't available, and may be None. Accounting for that using Optional.
        self.assertIsInstance(trophy_deck_stubs[0]['start_rank'], Optional[str])
        self.assertIsInstance(trophy_deck_stubs[0]['end_rank'], Optional[str])
        self.assertIsInstance(trophy_deck_stubs[0]['colors'], str)
        self.assertIsInstance(trophy_deck_stubs[0]['aggregate_id'], str)
        self.assertIsInstance(trophy_deck_stubs[0]['deck_index'], int)

    def test_get_deck(self):
        # Test a bad request.
        deck = self.REQUESTER.get_deck('Fish')
        self.assertIsNone(deck)

        # Validate the key parts of the structure, to make sure that changes in it haven't occurred.
        _id = 'f5383f215c364c129632cdc559f0ac3a'
        deck = self.REQUESTER.get_deck(_id)
        self.assertIsInstance(deck, dict)
        self.assertIsInstance(deck['event_info'], dict)
        self.assertIsInstance(deck['groups'], list)
        self.assertIsInstance(deck['groups'][0], dict)
        self.assertIsInstance(deck['groups'][0]['cards'], list)
        self.assertIsInstance(deck['groups'][0]['cards'][0], dict)

        # Validate the contents.
        #  Its contents are for ONE, and a completed draft of mine, so it should stay constant.
        self.assertEqual(deck['text_link'], f'/deck/{_id}/0.txt')
        self.assertEqual(deck['builder_link'], f'https://sealeddeck.tech/17lands/deck/{_id}/0')
        self.assertEqual(deck['event_info']['expansion'], 'ONE')
        self.assertEqual(deck['event_info']['format'], 'PremierDraft')
        self.assertEqual(deck['groups'][0]['name'], 'Maindeck')
        self.assertEqual(deck['groups'][1]['name'], 'Sideboard')
        self.assertEqual(deck['groups'][0]['cards'][0]['name'], 'Axiom Engraver')

        # Validate a part of the other build, to make sure different data is received.
        #  Its contents are for ONE, and a completed draft of mine, so it should stay constant.
        deck = self.REQUESTER.get_deck(_id, 1)
        self.assertIsInstance(deck, dict)
        self.assertEqual(deck['text_link'], f'/deck/{_id}/1.txt')
        self.assertEqual(deck['builder_link'], f'https://sealeddeck.tech/17lands/deck/{_id}/1')

    def test_get_details(self):
        # Test a bad request.
        details = self.REQUESTER.get_details('Fish')
        self.assertIsNone(details)

        # Validate the key parts of the structure, to make sure that changes in it haven't occurred.
        details = self.REQUESTER.get_details('f5383f215c364c129632cdc559f0ac3a')
        self.assertIsInstance(details, dict)
        self.assertIsInstance(details['event_course'], dict)
        self.assertIsInstance(details['match_results'], list)
        self.assertIsInstance(details['match_results'][0], dict)
        self.assertIsInstance(details['match_results'][0]['game_results'], list)
        self.assertIsInstance(details['match_results'][0]['game_results'][0], dict)

        # Validate the contents.
        #  Its contents are for ONE, and a completed draft of mine, so it should stay constant.
        self.assertEqual(details['expansion'], 'ONE')
        self.assertEqual(details['format'], 'PremierDraft')
        self.assertEqual(details['wins'], 7)
        self.assertEqual(details['losses'], 2)
        self.assertEqual(details['start_rank'], 'Platinum-4')
        self.assertEqual(details['end_rank'], 'Platinum-3')
        self.assertEqual(details['event_course']['wins'], 7)
        self.assertEqual(details['event_course']['losses'], 2)

    def test_get_draft(self):
        # Test a bad request.
        draft = self.REQUESTER.get_draft('Fish')
        self.assertIsNone(draft)

        # Validate the key parts of the structure, to make sure that changes in it haven't occurred.
        draft = self.REQUESTER.get_draft('f5383f215c364c129632cdc559f0ac3a')
        self.assertIsInstance(draft, dict)
        self.assertIsInstance(draft['picks'], list)
        self.assertIsInstance(draft['picks'][0], dict)
        self.assertIsInstance(draft['picks'][0]['pick'], dict)
        self.assertIsInstance(draft['picks'][0]['available'], list)
        self.assertIsInstance(draft['picks'][0]['available'][0], dict)

        # Validate the payload contents.
        #  Its contents are for ONE, and a completed draft of mine, so it should stay constant.
        self.assertEqual(draft['expansion'], 'ONE')
        self.assertEqual(draft['picks'][0]['pack_number'], 0)
        self.assertEqual(draft['picks'][0]['pick_number'], 0)
        self.assertEqual(draft['picks'][0]['pick']['name'], 'Solphim, Mayhem Dominus')
        self.assertEqual(draft['picks'][0]['available'][0]['name'], 'Solphim, Mayhem Dominus')

    def test_get_tier_list(self):
        # Test a bad request.
        tiers = self.REQUESTER.get_tier_list('Fish')
        self.assertIsNone(tiers)

        # Validate the key parts of the structure, to make sure that changes in it haven't occurred.
        tiers = self.REQUESTER.get_tier_list('45a3a3a84d9f46178d6750ff96d85f8c')
        self.assertIsInstance(tiers, list)
        self.assertIsInstance(tiers[0], dict)
        self.assertIsInstance(tiers[0]['flags'], dict)

        # Validate the contents, based on known information about the Tier List.
        #  Its contents are for ONE, and created by me, so it should stay constant.
        self.assertEqual(len(tiers), 261)
        self.assertEqual(tiers[0]['name'], 'Against All Odds')
        self.assertEqual(tiers[0]['tier'], 'C-')
        self.assertEqual(tiers[0]['comment'], '')
        self.assertEqual(tiers[0]['flags']['sideboard'], False)
        self.assertEqual(tiers[0]['flags']['synergy'], False)
        self.assertEqual(tiers[0]['flags']['buildaround'], False)
