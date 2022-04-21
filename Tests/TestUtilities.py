import unittest

from Utilities import TRIES, FAIL_DELAY, SUCCESS_DELAY
from Utilities import load_json_file, save_json_file
from Utilities import Fetcher


class TestFetcher(unittest.TestCase):
    def test_default_init(self):
        fetcher = Fetcher()
        self.assertEqual(fetcher._TRIES, TRIES)
        self.assertEqual(fetcher._FAIL_DELAY, FAIL_DELAY)
        self.assertEqual(fetcher._SUCCESS_DELAY, SUCCESS_DELAY)

    def test_arg_init(self):
        fetcher = Fetcher(2, 120, 10)
        self.assertEqual(fetcher._TRIES, 2)
        self.assertEqual(fetcher._FAIL_DELAY, 120)
        self.assertEqual(fetcher._SUCCESS_DELAY, 10)

    def test_valid_url(self):
        fetcher = Fetcher(2, 10, 2)
        ret = fetcher.fetch('https://api.scryfall.com/')
        self.assertIsInstance(ret, dict)

    def test_invalid_url(self):
        fetcher = Fetcher(2, 2, 2)
        ret = fetcher.fetch('Hello World')
        self.assertIsNone(ret)


# TODO: Revamp logger, then implement tests.
class TestLogger(unittest.TestCase):
    def test_get_color_supersets(self):
        pass


class TestFuncs(unittest.TestCase):
    def test_get_invalid_save(self):
        ret = save_json_file('./+%', 'test+test.txt', {'test': 'results'})
        self.assertFalse(ret)
        pass

    def test_get_valid_save(self):
        ret = save_json_file('Tests/', 'test.txt', {'test': 'results'})
        self.assertTrue(ret)
        pass

    def test_get_invalid_load(self):
        ret = load_json_file('./+%', 'test+test.txt')
        self.assertIsNone(ret)
        pass

    def test_get_valid_load(self):
        ret = load_json_file('Tests/', 'test.txt')
        self.assertIsInstance(ret, dict)
        pass
