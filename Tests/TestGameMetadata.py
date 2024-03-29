import unittest
from datetime import date, datetime

from core.wubrg import COLOR_COMBINATIONS
from core.game_metadata import SetMetadata, FormatMetadata, Card
from core.game_metadata import new_color_count_dict

from Tests.settings import _tries, _success_delay, _fail_delay


class TestSetMetadata(unittest.TestCase):
    def setUp(self) -> None:
        # Load all arena cards to speed up tests and reduce load on Scryfall server.
        SetMetadata.REQUESTER._TRIES = _tries
        SetMetadata.REQUESTER._SUCCESS_DELAY = _success_delay
        SetMetadata.REQUESTER._FAIL_DELAY = _fail_delay

    def test_get_metadata(self):
        neo_cards = 282
        alchemy_cards = 7
        meta = SetMetadata.get_metadata('NEO')
        self.assertIsInstance(meta, SetMetadata)
        self.assertIsInstance(meta.CARD_DICT, dict)
        self.assertEqual(len(meta.CARD_DICT), neo_cards + alchemy_cards)
        self.assertEqual(len(meta.CARD_LIST), neo_cards + alchemy_cards)
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
        red_or_blue_cnt = 88
        meta = SetMetadata.get_metadata('NEO')
        red_or_blue = meta.get_cards_by_colors(['R', 'U'])
        izzet = meta.get_cards_by_colors(['R', 'U', 'UR', 'RU'])

        self.assertGreater(len(izzet), len(red_or_blue))
        self.assertEqual(len(red_or_blue), red_or_blue_cnt)
        self.assertEqual(len(izzet),  red_or_blue_cnt + 2)

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
        neo_cards = 282
        alchemy_cards = 7
        form = FormatMetadata.get_metadata('NEO', 'PremierDraft')
        self.assertIsInstance(form, FormatMetadata)
        self.assertIsInstance(form.CARD_DICT, dict)
        self.assertEqual(len(form.CARD_DICT), neo_cards + alchemy_cards)
        self.assertEqual(len(form.CARD_LIST), neo_cards + alchemy_cards)
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
        end = date(2023, 2, 7)

        self.assertEqual(active[0], start)
        self.assertEqual(active[-1], end)

    def test_is_active(self):
        form = FormatMetadata.get_metadata('NEO', 'PremierDraft')
        self.assertTrue(form.has_started)
        self.assertTrue(form.has_data)

        self.assertFalse(form.is_active(date(2022, 2, 1)))
        self.assertFalse(form.is_active(datetime(2022, 2, 1, 11, 20)))

        self.assertTrue(form.is_active(date(2022, 3, 15)))
        self.assertTrue(form.is_active(datetime(2022, 3, 15, 11, 20)))

        active = form.is_active()
        self.assertEqual(active, date.today() <= date(2022, 4, 28))


class TestMetadataUtilities(unittest.TestCase):
    def test_new_color_count_dict(self):
        d = new_color_count_dict()
        self.assertIsInstance(d, dict)

