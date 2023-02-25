import logging
import os
import unittest

from core.utilities import validate_json, load_json_file, save_json_file, auto_logging, flatten_lists, invert_dict
from core.utilities.funcs import reformat_json_file


class TestLogging(unittest.TestCase):
    # noinspection PyUnresolvedReferences
    def test_logger(self):
        auto_logging.add_logging_level('TEST', 100)
        self.assertEqual(logging.TEST, 100)
        self.assertIsNotNone(logging.test)
        self.assertIsNotNone(logging.getLoggerClass().test)

        auto_logging.auto_log()
        self.assertEqual(logging.VERBOSE, 15)
        self.assertEqual(logging.SPARSE, 25)

        auto_logging.set_log_level(logging.TEST)
        logging.test("Testing logging!")
        logging.getLogger(__name__).test("Testing logging!")

    def test_logger_errors(self):
        # Check that setting an existing level fails.
        self.assertRaises(AttributeError, auto_logging.add_logging_level, 'WARNING', 100, 'warning')

        # Check that setting a function which exists fails.
        self.assertRaises(AttributeError, auto_logging.add_logging_level, 'AUTOLOG', 100, 'warning')

        # Check that setting a function in the active logger class fails.
        log_class_prop = list(logging.getLoggerClass().__dict__.keys())[0]
        self.assertRaises(AttributeError, auto_logging.add_logging_level, 'ERROR_TEST', 100, log_class_prop)


class TestFuncs(unittest.TestCase):
    test_dir = r'C:\Users\Zachary\Coding\GitHub\DraftMetaReporter\Tests\Misc'

    def setUp(self) -> None:
        with open(os.path.join(self.test_dir, 'test.json'), 'w') as f:
            f.write('{"test": "results", "second": 2}')

    def tearDown(self) -> None:
        os.remove(os.path.join(self.test_dir, 'test.json'))

    def test_validate_json(self):
        self.assertTrue(validate_json('{"Test": "Data"}'))
        self.assertFalse(validate_json("'Test"))

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
        self.assertTrue(True)

    def test_flatten_lists(self):
        _in = [[1, 2], [3], [4, 5, 6, 7], [8, ]]
        _out = [1, 2, 3, 4, 5, 6, 7, 8]
        self.assertListEqual(flatten_lists(_in), _out)

    def test_invert_dict(self):
        _in = {
            'A': 1,
            'B': 2,
            'C': 3,
        }

        _out = {
            1: 'A',
            2: 'B',
            3: 'C',
        }

        self.assertDictEqual(invert_dict(_in), _out)
