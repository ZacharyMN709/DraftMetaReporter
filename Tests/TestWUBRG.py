import unittest

from WUBRG.funcs import get_color_string, get_color_identity, get_color_alias, list_color_dict, \
    get_color_supersets, get_color_subsets, parse_cost, color_compare_wubrg, color_compare_group
from WUBRG.consts import FAILSAFE, COLOR_COMBINATIONS, ALLIED, ENEMY, GUILDS


class TestWUBRGStringFuncs(unittest.TestCase):
    def test_get_color_string(self):
        s = 'RU'
        ret = get_color_string(s)
        self.assertEqual(ret, 'RU')

    def test_get_color_string_none(self):
        s = None
        ret = get_color_string(s)
        self.assertEqual(ret, FAILSAFE)

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

    def test_parse_cost_valid_split(self):
        s = '{U/R} // {4}{U}{R}'
        ret = parse_cost(s)
        self.assertListEqual(ret, ['U/R', '4', 'U', 'R'])

    def test_parse_cost_invalid(self):
        s = '{2}{V}{U}'
        ret = parse_cost(s)
        self.assertListEqual(ret, ['A'])

    def test_parse_cost_malformed(self):
        s = '{2}{V}U}'
        ret = parse_cost(s)
        self.assertListEqual(ret, ['A'])

    def test_list_color_dict(self):
        ret = list_color_dict(ALLIED)
        self.assertListEqual(ret, ["WU", "UB", "BR", "RG", "WG"])

        ret = list_color_dict(ENEMY)
        self.assertListEqual(ret, ["WB", "BG", "UG", "UR", "WR"])

        ret = list_color_dict(GUILDS)
        self.assertListEqual(ret, ["WU", "UB", "BR", "RG", "WG", "WB", "BG", "UG",  "UR", "WR"])


class TestWUBRGSortFuncs(unittest.TestCase):
    def test_compare_wubrg(self):
        self.assertEqual(color_compare_wubrg('', 'W'), -1)
        self.assertEqual(color_compare_wubrg('W', 'U'), -1)
        self.assertEqual(color_compare_wubrg('U', 'W'), 1)
        self.assertEqual(color_compare_wubrg('U', ''), 1)
        self.assertEqual(color_compare_wubrg('G', 'UB'), -1)
        self.assertEqual(color_compare_wubrg('UB', 'WUB'), -1)
        self.assertEqual(color_compare_wubrg('WUB', 'UBRG'), -1)
        self.assertEqual(color_compare_wubrg('UBRG', 'WUBRG'), -1)
        self.assertEqual(color_compare_wubrg('WUBRG', 'WUBRG'), 1)
        self.assertRaises(KeyError, color_compare_wubrg, 'UW', 'BU')

    def test_get_color_group(self):
        self.assertEqual(color_compare_group('W', 'UB'), -1)
        self.assertEqual(color_compare_group('WU', 'UB'), -1)
        self.assertEqual(color_compare_group('UB', 'WU'), 1)
        self.assertEqual(color_compare_group('WB', 'UB'), 1)
        self.assertEqual(color_compare_group('WB', 'WR'), -1)
        self.assertEqual(color_compare_group('WUR', 'WBG'), -1)
        self.assertEqual(color_compare_group('WUB', 'WUG'), -1)
        self.assertEqual(color_compare_group('WUB', 'WUR'), 1)
        self.assertEqual(color_compare_group('WUBR', 'UBRG'), -1)
        self.assertEqual(color_compare_group('WUBRG', 'WUBRG'), 1)
        self.assertRaises(KeyError, color_compare_group, 'UW', 'BU')
