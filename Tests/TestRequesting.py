import unittest

from core.data_requesting.utils.settings import TRIES, FAIL_DELAY, SUCCESS_DELAY
from core.data_requesting import Requester, RequestScryfall, Request17Lands

from settings import _tries, _fail_delay, _success_delay


# TODO: Create new test suites for Requesting objects.

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


class TestRequestRequest17Lands(unittest.TestCase):
    REQUESTER = Request17Lands(_tries, _fail_delay, _success_delay)

    def test_(self):
        pass
