"""
Tests code from the wubrg module.
"""

import unittest

from wubrg import *
from wubrg import FAILSAFE, GROUP_COLOR_COMBINATIONS, index_dist_wubrg, index_dist_pentad, \
    order_by_wubrg, order_by_pentad, exact, superset, subset, adjacent, shares


class TestWUBRGStringFuncs(unittest.TestCase):
    def test_is_color_string(self):
        self.assertEqual(is_color_string('RU'), True)
        # noinspection SpellCheckingInspection
        self.assertEqual(is_color_string('RRRUUU'), True)
        # noinspection SpellCheckingInspection
        self.assertEqual(is_color_string('rrruuu'), True)
        self.assertEqual(is_color_string('Fish'), False)
        self.assertEqual(is_color_string('Ox'), False)

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
        # noinspection SpellCheckingInspection
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


class TestWUBRGSortFuncs(unittest.TestCase):
    def test_compare_wubrg(self):
        self.assertEqual(index_dist_wubrg('', 'W'), -1)
        self.assertEqual(index_dist_wubrg('W', 'U'), -1)
        self.assertEqual(index_dist_wubrg('U', 'W'), 1)
        self.assertEqual(index_dist_wubrg('U', ''), 2)
        self.assertEqual(index_dist_wubrg('G', 'UB'), -5)
        self.assertEqual(index_dist_wubrg('UB', 'WUB'), -6)
        self.assertEqual(index_dist_wubrg('WUB', 'UBRG'), -14)
        self.assertEqual(index_dist_wubrg('UBRG', 'WUBRG'), -1)
        self.assertEqual(index_dist_wubrg('WUBRG', 'WUBRG'), 0)
        self.assertRaises(KeyError, index_dist_wubrg, 'UW', 'BU')

    def test_get_color_group(self):
        self.assertEqual(index_dist_pentad('', 'W'), -1)
        self.assertEqual(index_dist_pentad('W', 'UB'), -6)
        self.assertEqual(index_dist_pentad('WU', 'UB'), -1)
        self.assertEqual(index_dist_pentad('UB', 'WU'), 1)
        self.assertEqual(index_dist_pentad('WB', 'UB'), 4)
        self.assertEqual(index_dist_pentad('WB', 'WR'), -4)
        self.assertEqual(index_dist_pentad('WUR', 'WBG'), -4)
        self.assertEqual(index_dist_pentad('WUB', 'WUG'), -4)
        self.assertEqual(index_dist_pentad('WUB', 'WUR'), 5)
        self.assertEqual(index_dist_pentad('WUBR', 'UBRG'), -4)
        self.assertEqual(index_dist_pentad('WUBRG', 'WUBRG'), 0)
        self.assertRaises(KeyError, index_dist_pentad, 'UW', 'BU')


class TestWUBRGColorFilterFuncs(unittest.TestCase):
    def test_sorting(self):
        self.assertListEqual(order_by_wubrg(['U', 'W', 'G', 'B', 'R']), ['W', 'U', 'B', 'R', 'G'])
        self.assertListEqual(order_by_pentad(COLOR_PAIRS), GROUP_COLOR_COMBINATIONS[6:16])

    def test_exact(self):
        self.assertListEqual(exact(''), [''])
        self.assertListEqual(exact('W'), ['W'])
        self.assertListEqual(exact('WRG'), ['WRG'])
        self.assertListEqual(exact('WUBRG'), ['WUBRG'])
        # Testing mis-ordered string.
        # noinspection PyTypeChecker
        # noinspection SpellCheckingInspection
        self.assertListEqual(exact('WUGRB'), ['WUBRG'])

    def test_subset(self):
        self.assertListEqual(subset(''), [''])
        self.assertListEqual(subset('W'), ['', 'W'])
        self.assertListEqual(subset('WG'), ['', 'W', 'G', 'WG'])
        self.assertListEqual(subset('WUBRG'), COLOR_COMBINATIONS)
        # Testing mis-ordered string.
        # noinspection PyTypeChecker
        # noinspection SpellCheckingInspection
        self.assertListEqual(subset('WUGRB'), COLOR_COMBINATIONS)

    def test_superset(self):
        self.assertListEqual(superset('W'), ['W', 'WU', 'WB', 'WR', 'WG', 'WUB', 'WUR', 'WUG', 'WBR', 'WBG',
                                             'WRG', 'WUBR', 'WUBG', 'WURG', 'WBRG', 'WUBRG'])
        self.assertListEqual(superset('WRG'), ['WRG', 'WURG', 'WBRG', 'WUBRG'])
        self.assertListEqual(superset(''), COLOR_COMBINATIONS)
        self.assertListEqual(superset('WUBRG'), ['WUBRG'])
        # Testing mis-ordered string.
        # noinspection PyTypeChecker
        # noinspection SpellCheckingInspection
        self.assertListEqual(superset('WUGRB'), ['WUBRG'])

    def test_adjacent(self):
        self.assertListEqual(adjacent(''), ['', 'W', 'U', 'B', 'R', 'G'])
        self.assertListEqual(adjacent('W'), ['', 'W', 'WU', 'WB', 'WR', 'WG'])
        self.assertListEqual(adjacent('WRG'), ['WR', 'WG', 'RG', 'WRG', 'WURG', 'WBRG'])
        self.assertListEqual(adjacent('WUBRG'), ['WUBR', 'WUBG', 'WURG', 'WBRG', 'UBRG', 'WUBRG'])
        # Testing mis-ordered string.
        # noinspection PyTypeChecker
        # noinspection SpellCheckingInspection
        self.assertListEqual(adjacent('WUGRB'), ['WUBR', 'WUBG', 'WURG', 'WBRG', 'UBRG', 'WUBRG'])

    def test_shares(self):
        self.assertListEqual(shares(''), [''])
        self.assertListEqual(shares('W'), ['W', 'WU', 'WB', 'WR', 'WG',
                                           'WUB', 'WUR', 'WUG', 'WBR', 'WBG', 'WRG',
                                           'WUBR', 'WUBG', 'WURG', 'WBRG', 'WUBRG'])
        self.assertListEqual(shares('WRG'), ['W', 'R', 'G',
                                             'WU', 'WB', 'WR', 'WG', 'UR', 'UG', 'BR', 'BG', 'RG',
                                             'WUB', 'WUR', 'WUG', 'WBR', 'WBG',
                                             'WRG', 'UBR', 'UBG', 'URG', 'BRG',
                                             'WUBR', 'WUBG', 'WURG', 'WBRG', 'UBRG', 'WUBRG'])
        self.assertListEqual(shares('WUBRG'), COLOR_COMBINATIONS[1:])
        # Testing mis-ordered string.
        # noinspection PyTypeChecker
        # noinspection SpellCheckingInspection
        self.assertListEqual(shares('WUGRB'), COLOR_COMBINATIONS[1:])

    def test_color_filter(self):
        self.assertRaises(ValueError, color_filter, 'WUBRG', None, )
        self.assertListEqual(color_filter('WUBRG', ColorSortStyles.exact), ['WUBRG'])
        self.assertListEqual(color_filter('WUBRG', ColorSortStyles.subset), COLOR_COMBINATIONS)
        self.assertListEqual(color_filter('WUBRG', ColorSortStyles.superset), ['WUBRG'])
        self.assertListEqual(color_filter('WUBRG', ColorSortStyles.adjacent),
                             ['WUBR', 'WUBG', 'WURG', 'WBRG', 'UBRG', 'WUBRG'])
        self.assertListEqual(color_filter('WUBRG', ColorSortStyles.shares), COLOR_COMBINATIONS[1:])
