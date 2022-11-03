import logging
import os
import unittest

from Utilities import TRIES, FAIL_DELAY, SUCCESS_DELAY
from Utilities import load_json_file, save_json_file, reformat_json_file
from Utilities import Requester
from Utilities import auto_logging


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
        self.assertIsInstance(ret, dict)

    def test_invalid_url(self):
        requester = Requester(2, 2, 2)
        ret = requester.request('Hello World')
        self.assertIsNone(ret)


class TestLogging(unittest.TestCase):
    def test_logger(self):
        auto_logging.addLoggingLevel('TEST', 100, 'test')
        self.assertEqual(logging.TEST, 100)

        auto_logging.auto_log()
        self.assertEqual(logging.VERBOSE, 15)
        self.assertEqual(logging.SPARSE, 25)


class TestFuncs(unittest.TestCase):
    def setUp(self) -> None:
        try:
            with open(r'C:\Users\Zachary\Coding\GitHub\DraftMetaReporter\Tests\Misc\test.json', 'w') as f:
                f.write('{"test": "results", "second": 2}')
        except FileNotFoundError:
            pass

    def tearDown(self) -> None:
        try:
            os.remove(r'Tests\Misc\test.json')
        except FileNotFoundError:
            pass

    def test_get_invalid_save(self):
        ret = save_json_file('./+%', 'test+test.json', {'test': 'results'})
        self.assertFalse(ret)

    def test_get_valid_save(self):
        ret = save_json_file(r'C:\Users\Zachary\Coding\GitHub\DraftMetaReporter\Tests\Misc', 'test.json', {'test': 'results'})
        self.assertTrue(ret)

    def test_get_invalid_load(self):
        ret = load_json_file('./+%', 'test+test.json')
        self.assertIsNone(ret)

    def test_get_valid_load(self):
        ret = load_json_file(r'C:\Users\Zachary\Coding\GitHub\DraftMetaReporter\Tests\Misc', 'test.json')
        self.assertIsInstance(ret, dict)

    def test_reformat(self):
        reformat_json_file(r'C:\Users\Zachary\Coding\GitHub\DraftMetaReporter\Tests\Misc', 'test.json', indent=8)
