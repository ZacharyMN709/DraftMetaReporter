import unittest
from datetime import date

from wubrg import COLOR_COMBINATIONS

from game_metadata.utils.funcs import new_color_count_dict
from game_metadata.GameMetadata import SetMetadata, FormatMetadata
from data_interface.RequestScryfall import RequestScryfall, trap_error
from game_metadata.game_objects.Card import Card


class TestRequestScryfall(unittest.TestCase):
    def test_trap_error(self):
        def raise_test_error(v=True, _=None):
            if v:
                raise Exception("Test Error!")

        val = trap_error(raise_test_error)(True, None)
        self.assertIsNone(val)

    def test_get_set_cards_valid(self):
        cards = RequestScryfall.get_set_cards('NEO')
        self.assertIsInstance(cards, list)

    def test_get_set_cards_invalid(self):
        ret = RequestScryfall.get_set_cards('INVALID')
        self.assertIsNone(ret)

    def test_get_set_info_valid(self):
        cards = RequestScryfall.get_set_info('NEO')
        self.assertIsInstance(cards, tuple)

    def test_get_set_info_invalid(self):
        ret = RequestScryfall.get_set_info('INVALID')
        self.assertIsNone(ret)

    def test_get_card_by_name_valid(self):
        card = RequestScryfall.get_card_by_name('Virus Beetle')
        self.assertIsInstance(card, dict)
        self.assertEqual(card['object'], 'card')
        self.assertEqual(card['name'], 'Virus Beetle')

    def test_get_card_by_name_valid_misspelled(self):
        card = RequestScryfall.get_card_by_name('Vires Beetle')
        self.assertIsInstance(card, dict)
        self.assertEqual(card['object'], 'card')
        self.assertEqual(card['name'], 'Virus Beetle')

    def test_get_card_by_name_multiple(self):
        name = 'Bolt'
        card = RequestScryfall.get_card_by_name(name)
        self.assertIsInstance(card, dict)
        self.assertEqual(card['err_msg'], f'Error: Multiple card matches for "{name}"')

    def test_get_card_by_name_dne(self):
        name = 'Supercalifragilisticexpialidocious'
        card = RequestScryfall.get_card_by_name(name)
        self.assertIsInstance(card, dict)
        self.assertEqual(card['err_msg'], f'Error: Cannot find card "{name}"')


class TestSetMetadata(unittest.TestCase):
    def test_get_metadata(self):
        meta = SetMetadata.get_metadata('NEO')
        self.assertIsInstance(meta, SetMetadata)
        self.assertIsInstance(meta.CARD_DICT, dict)
        self.assertEqual(len(meta.CARD_DICT), 282)
        self.assertEqual(len(meta.CARD_LIST), 282)
        self.assertIsInstance(meta.CARD_DICT['Virus Beetle'], Card)

        get = SetMetadata['NEO']
        self.assertEqual(meta, get)

    def test_get_metadata_invalid_constructor(self):
        self.assertRaises(Exception, SetMetadata, object(), 'NEO')

    def test_find_card(self):
        meta = SetMetadata.get_metadata('NEO')
        card_1 = meta.find_card('Boseiju Reaches Skyward')
        card_2 = meta.find_card('Boseiju Reaches Skyward // Branch of Boseiju')

        self.assertIsInstance(card_1, Card)
        self.assertEqual(card_1, card_2)

        card_3 = meta.find_card('Shock')
        self.assertIsNone(card_3)

    def test_get_cards_by_color(self):
        meta = SetMetadata.get_metadata('NEO')
        red_or_blue = meta.get_cards_by_colors(['R', 'U'])
        izzet = meta.get_cards_by_colors(['R', 'U', 'UR', 'RU'])

        self.assertGreater(len(izzet), len(red_or_blue))
        self.assertEqual(len(red_or_blue), 86)
        self.assertEqual(len(izzet),  88)

        card = meta.find_card('Enthusiastic Mechanaut')
        self.assertIn(card, izzet)
        self.assertNotIn(card, red_or_blue)

    def test_print_order_compare(self):
        meta = SetMetadata.get_metadata('NEO')

        name_1 = meta.CARD_LIST[0].NAME
        name_2 = meta.CARD_LIST[-1].NAME
        name_3 = meta.CARD_LIST[2].NAME

        self.assertLessEqual(meta._print_order_compare(name_1, name_2), -1)
        self.assertGreaterEqual(meta._print_order_compare(name_2, name_1), 1)
        self.assertLessEqual(meta._print_order_compare(name_1, name_3), -1)
        self.assertGreaterEqual(meta._print_order_compare(name_3, name_1), 1)
        self.assertLessEqual(meta._print_order_compare(name_3, name_2), -1)
        self.assertGreaterEqual(meta._print_order_compare(name_2, name_3), 1)
        self.assertEqual(meta._print_order_compare(name_3, name_3), 0)

    def test_review_order_compare(self):
        meta = SetMetadata.get_metadata('NEO')

        name_1 = meta.CARD_LIST[0].NAME
        name_2 = meta.CARD_LIST[-1].NAME
        name_3 = meta.CARD_LIST[2].NAME

        self.assertLessEqual(meta._review_order_compare(name_1, name_2), -1)
        self.assertGreaterEqual(meta._review_order_compare(name_2, name_1), 1)
        self.assertLessEqual(meta._review_order_compare(name_1, name_3), -1)
        self.assertGreaterEqual(meta._review_order_compare(name_3, name_1), 1)
        self.assertLessEqual(meta._review_order_compare(name_3, name_2), -1)
        self.assertGreaterEqual(meta._review_order_compare(name_2, name_3), 1)
        self.assertEqual(meta._review_order_compare(name_3, name_3), 0)

    def test_frame_order_compare(self):
        meta = SetMetadata.get_metadata('NEO')

        tup_1 = (COLOR_COMBINATIONS[0], meta.CARD_LIST[0].NAME)
        tup_2 = (COLOR_COMBINATIONS[-1], meta.CARD_LIST[-1].NAME)
        tup_3 = (COLOR_COMBINATIONS[0], meta.CARD_LIST[2].NAME)

        self.assertEqual(meta._frame_order_compare(tup_1, tup_2), -31)
        self.assertEqual(meta._frame_order_compare(tup_2, tup_1), 31)
        self.assertEqual(meta._frame_order_compare(tup_1, tup_3), -2)
        self.assertEqual(meta._frame_order_compare(tup_3, tup_1), 2)
        self.assertEqual(meta._frame_order_compare(tup_3, tup_2), -31)
        self.assertEqual(meta._frame_order_compare(tup_2, tup_3), 31)


class TestFormatMetadata(unittest.TestCase):
    def test_get_metadata(self):
        form = FormatMetadata.get_metadata('NEO', 'PremierDraft')
        self.assertIsInstance(form, FormatMetadata)
        self.assertIsInstance(form.CARD_DICT, dict)
        self.assertEqual(len(form.CARD_DICT), 282)
        self.assertEqual(len(form.CARD_LIST), 282)
        self.assertIsInstance(form.CARD_DICT['Virus Beetle'], Card)

    def test_get_metadata_invalid_constructor(self):
        self.assertRaises(Exception, FormatMetadata, object(), 'NEO', 'PremierDraft')

    def test_find_card(self):
        form = FormatMetadata.get_metadata('NEO', 'PremierDraft')
        card_1 = form.find_card('Boseiju Reaches Skyward // Branch of Boseiju')
        card_2 = form.find_card('Boseiju Reaches Skyward')
        self.assertNotEqual(card_1.NAME, card_1.FULL_NAME)
        self.assertIsInstance(card_1, Card)
        self.assertIsInstance(card_2, Card)
        self.assertEqual(card_1, card_2)

        card_3 = form.find_card('Shock')
        self.assertIsNone(card_3)

    def test_active_dates(self):
        form = FormatMetadata.get_metadata('NEO', 'PremierDraft')
        active = form.get_active_days()
        start = date(2022, 2, 10)
        end = date(2022, 4, 28)

        self.assertEqual(active[0], start)
        self.assertEqual(active[-1], end)

    def test_is_active(self):
        form = FormatMetadata.get_metadata('NEO', 'PremierDraft')
        active = form.is_active(date(2022, 2, 1))
        self.assertFalse(active)

        active = form.is_active(date(2022, 3, 15))
        self.assertTrue(active)

        active = form.is_active()
        self.assertEqual(active, date.today() <= date(2022, 4, 28))

        self.assertTrue(form.has_started)


class TestMetadataUtilities(unittest.TestCase):
    def test_new_color_count_dict(self):
        d = new_color_count_dict()
        self.assertIsInstance(d, dict)

