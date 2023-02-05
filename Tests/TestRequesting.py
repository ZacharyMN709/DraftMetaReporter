import unittest

from core.data_requesting.utils.settings import TRIES, FAIL_DELAY, SUCCESS_DELAY
from core.data_requesting.Requester import Requester


# TODO: Create new test suites for Requesting objects.

class TestFetcher(unittest.TestCase):
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
        requester = Requester(2, 10, 2)
        ret = requester.request('https://api.scryfall.com/')
        self.assertIsNone(ret)

    def test_invalid_url(self):
        requester = Requester(2, 2, 2)
        ret = requester.request('Hello World')
        self.assertIsNone(ret)
