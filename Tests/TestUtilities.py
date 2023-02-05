import logging
import os
import unittest

from core.utilities import load_json_file, save_json_file, auto_logging
from core.utilities.funcs import reformat_json_file


class TestLogging(unittest.TestCase):
    def test_logger(self):
        auto_logging.addLoggingLevel('TEST', 100, 'test')
        self.assertEqual(logging.TEST, 100)

        auto_logging.auto_log()
        self.assertEqual(logging.VERBOSE, 15)
        self.assertEqual(logging.SPARSE, 25)


class TestFuncs(unittest.TestCase):
    test_dir = r'C:\Users\Zachary\Coding\GitHub\DraftMetaReporter\Tests\Misc'

    def setUp(self) -> None:
        try:
            with open(os.path.join(self.test_dir, 'test.json'), 'w') as f:
                f.write('{"test": "results", "second": 2}')
        except FileNotFoundError as ex:  # pragma: nocover
            raise ex

    def tearDown(self) -> None:
        try:
            os.remove(os.path.join(self.test_dir, 'test.json'))
        except FileNotFoundError as ex:  # pragma: nocover
            raise ex

    def test_get_invalid_save(self):
        ret = save_json_file('./+%', 'test+test.json', {'test': 'results'})
        self.assertFalse(ret)

    def test_get_valid_save(self):
        ret = save_json_file(self.test_dir, 'test.json', {'test': 'results'})
        self.assertTrue(ret)

    def test_get_invalid_load(self):
        ret = load_json_file('./+%', 'test+test.json')
        self.assertIsNone(ret)

    def test_get_valid_load(self):
        ret = load_json_file(self.test_dir, 'test.json')
        self.assertIsInstance(ret, dict)

    def test_reformat(self):
        reformat_json_file(self.test_dir, 'test.json', indent=8)
