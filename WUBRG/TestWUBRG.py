import unittest

from WUBRG.funcs import get_color_string, get_color_identity, get_color_alias
from WUBRG.funcs import get_color_supersets, get_color_subsets, parse_cost
from WUBRG.consts import FAILSAFE, COLOR_COMBINATIONS


class TestWUBRGStringFuncs(unittest.TestCase):
    def test_get_color_string(self):
        s = 'RU'
        ret = get_color_string(s)
        self.assertEqual(ret, 'RU')

    def test_get_color_string_invalid(self):
        s = 'V'
        ret = get_color_string(s)
        self.assertEqual(ret, FAILSAFE)

    def test_get_color_string_semivalid(self):
        s = 'PURPLE'
        ret = get_color_string(s)
        self.assertEqual(ret, 'UR')

    def test_get_color_identity(self):
        s = 'RU'
        ret = get_color_identity(s)
        self.assertEqual(ret, 'UR')

    def test_get_color_identity_doubled(self):
        s = 'RUURURU'
        ret = get_color_identity(s)
        self.assertEqual(ret, 'UR')

    def test_get_color_alias(self):
        s = 'WUR'
        ret = get_color_alias(s)
        self.assertEqual(ret, 'Jeskai')

    def test_get_color_alias_scramble(self):
        s = 'URW'
        ret = get_color_alias(s)
        self.assertEqual(ret, 'Jeskai')

    def test_get_color_alias_invalid(self):
        s = 'X'
        ret = get_color_alias(s)
        self.assertIsNone(ret)


class TestWUBRGListFuncs(unittest.TestCase):
    def test_get_color_supersets(self):
        s = ''
        ret = get_color_supersets(s)
        self.assertListEqual(ret, COLOR_COMBINATIONS)

    def test_get_color_subsets(self):
        s = 'WUBRG'
        ret = get_color_subsets(s)
        self.assertListEqual(ret, COLOR_COMBINATIONS)

    def test_get_color_supersets_invalid(self):
        s = 'A'
        ret = get_color_supersets(s)
        self.assertListEqual(ret, COLOR_COMBINATIONS)

    def test_get_color_subsets_invalid(self):
        s = 'A'
        ret = get_color_subsets(s)
        self.assertListEqual(ret, [''])

    def test_get_color_supersets_lim(self):
        s = 'R'
        ret = get_color_supersets(s, 2)
        self.assertListEqual(ret, ['R', 'WR', 'UR', 'BR', 'RG'])

    def test_get_color_subsets_lim(self):
        s = 'WUB'
        ret = get_color_subsets(s, 1)
        self.assertListEqual(ret, ['W', 'U', 'B', 'WU', 'WB', 'UB', 'WUB'])

    def test_get_color_supersets_strict(self):
        s = 'R'
        ret = get_color_supersets(s, 2, True)
        self.assertListEqual(ret, ['WR', 'UR', 'BR', 'RG'])

    def test_get_color_subsets_strict(self):
        s = 'WUB'
        ret = get_color_subsets(s, 1, True)
        self.assertListEqual(ret, ['W', 'U', 'B', 'WU', 'WB', 'UB'])

    def test_parse_cost_valid(self):
        s = '{2}{W}{U}'
        ret = parse_cost(s)
        self.assertListEqual(ret, ['2', 'W', 'U'])

    def test_parse_cost_invalid(self):
        s = '{2}{V}{U}'
        ret = parse_cost(s)
        self.assertListEqual(ret, ['A'])

    def test_parse_cost_malformed(self):
        s = '{2}{V}U}'
        ret = parse_cost(s)
        self.assertListEqual(ret, ['A'])

