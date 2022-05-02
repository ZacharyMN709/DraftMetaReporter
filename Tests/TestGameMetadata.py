import unittest
from datetime import date

import WUBRG
from game_metadata import CallScryfall
from game_metadata.CallScryfall import trap_error

from game_metadata import Card
from game_metadata.utils.consts import CardLayouts

from game_metadata import CardManager

from game_metadata import SetMetadata, FormatMetadata


class TestCallScryfall(unittest.TestCase):
    def test_trap_error(self):
        def raise_test_error(v=True, void=None):
            if v:
                raise Exception("Test Error!")
            else:  # pragma: no cover
                return list()

        val = trap_error(raise_test_error)(True, None)
        self.assertIsNone(val)

    def test_get_set_cards_valid(self):
        cards = CallScryfall.get_set_cards('NEO')
        self.assertIsInstance(cards, list)

    def test_get_set_cards_invalid(self):
        ret = CallScryfall.get_set_cards('INVALID')
        self.assertIsNone(ret)

    def test_get_set_info_valid(self):
        cards = CallScryfall.get_set_info('NEO')
        self.assertIsInstance(cards, tuple)

    def test_get_set_info_invalid(self):
        ret = CallScryfall.get_set_info('INVALID')
        self.assertIsNone(ret)

    def test_get_card_by_name_valid(self):
        card = CallScryfall.get_card_by_name('Virus Beetle')
        self.assertIsInstance(card, dict)
        self.assertEqual(card['object'], 'card')
        self.assertEqual(card['name'], 'Virus Beetle')

    def test_get_card_by_name_valid_misspelled(self):
        card = CallScryfall.get_card_by_name('Vires Beetle')
        self.assertIsInstance(card, dict)
        self.assertEqual(card['object'], 'card')
        self.assertEqual(card['name'], 'Virus Beetle')

    def test_get_card_by_name_multiple(self):
        name = 'Bolt'
        card = CallScryfall.get_card_by_name(name)
        self.assertIsInstance(card, dict)
        self.assertEqual(card['err_msg'], f'Error: Multiple card matches for "{name}"')

    def test_get_card_by_name_dne(self):
        name = 'Supercalifragilisticexpialidocious'
        card = CallScryfall.get_card_by_name(name)
        self.assertIsInstance(card, dict)
        self.assertEqual(card['err_msg'], f'Error: Cannot find card "{name}"')


class TestCard(unittest.TestCase):
    @staticmethod
    def gen_card(card_name):
        json = CallScryfall.get_card_by_name(card_name)
        return Card(json)

    def test_card_normal(self):
        name = 'Jukai Preserver'
        card = self.gen_card(name)
        self.assertEqual(card.LAYOUT, CardLayouts.NORMAL)

    def test_card_adventure(self):
        name = 'Bonecrusher Giant'
        card = self.gen_card(name)
        self.assertEqual(card.LAYOUT, CardLayouts.ADVENTURE)

    def test_card_split(self):
        name = 'Invert // Invent'
        card = self.gen_card(name)
        self.assertEqual(card.LAYOUT, CardLayouts.SPLIT)

    def test_card_transform(self):
        name = 'Boseiju Reaches Skyward'
        card = self.gen_card(name)
        self.assertEqual(card.LAYOUT, CardLayouts.TRANSFORM)

    def test_card_modal_dfc(self):
        name = 'Shatterskull Smashing'
        card = self.gen_card(name)
        self.assertEqual(card.LAYOUT, CardLayouts.MODAL_DFC)

    def test_card_saga(self):
        name = 'Fall of the Thran'
        card = self.gen_card(name)
        self.assertEqual(card.LAYOUT, CardLayouts.SAGA)

    def test_card_class(self):
        name = 'Ranger Class'
        card = self.gen_card(name)
        self.assertEqual(card.LAYOUT, CardLayouts.CLASS)

    def test_card_flip(self):
        name = 'Bushi Tenderfoot'
        self.assertRaises(Exception, self.gen_card, name)

    def test_card_legendary(self):
        name = 'Cormella, Glamor Thief'
        card = self.gen_card(name)
        self.assertEqual(card.LAYOUT, CardLayouts.NORMAL)

    def test_card_snow(self):
        name = 'Berg Strider'
        card = self.gen_card(name)
        self.assertEqual(card.LAYOUT, CardLayouts.NORMAL)

    def test_card_planeswalker(self):
        name = 'The Wandering Emperor'
        card = self.gen_card(name)
        self.assertEqual(card.LAYOUT, CardLayouts.NORMAL)

    def test_card_error(self):
        name = 'ujbn uiblubiihno;cinoef r'
        self.assertRaises(Exception, self.gen_card, name)

    def test_card_short_name(self):
        name = 'Jukai Preserver'
        card = self.gen_card(name)
        self.assertEqual(card.LAYOUT, CardLayouts.NORMAL)
        self.assertEqual(str(card), name)
        self.assertEqual(repr(card), name)
        self.assertEqual(card.NAME, name)
        self.assertEqual(card.MANA_COST, '{3}{G}')

    def test_card_dual_name(self):
        name = 'Boseiju Reaches Skyward'
        full_name = 'Boseiju Reaches Skyward // Branch of Boseiju'
        card = self.gen_card(name)
        self.assertEqual(card.LAYOUT, CardLayouts.TRANSFORM)
        self.assertEqual(str(card), full_name)
        self.assertEqual(repr(card), full_name)
        self.assertEqual(card.NAME, name)
        self.assertEqual(card.MANA_COST, '{3}{G}')

    def test_card_full_name(self):
        name = 'Invert // Invent'
        card = self.gen_card(name)
        self.assertEqual(card.LAYOUT, CardLayouts.SPLIT)
        self.assertEqual(str(card), name)
        self.assertEqual(repr(card), name)
        self.assertEqual(card.NAME, name)
        self.assertEqual(card.MANA_COST, '{U/R} // {4}{U}{R}')

    def test_card_links(self):
        name = 'Shatterskull Smashing'
        card = self.gen_card(name)
        self.assertEqual(card.API, 'https://api.scryfall.com/cards/bc7239ea-f8aa-4a6f-87bd-c35359635673')
        self.assertEqual(card.URL, 'https://scryfall.com/card/znr/161')
        self.assertEqual(card.IMAGE_URL, 'https://c1.scryfall.com/file/scryfall-cards/normal/'
                                         'front/b/c/bc7239ea-f8aa-4a6f-87bd-c35359635673.jpg')


class TestCardManager(unittest.TestCase):
    def test_from_set(self):
        cards = CardManager.from_set('NEO')
        self.assertIsInstance(cards, dict)
        self.assertEqual(len(cards), 282)

    def test_from_name(self):
        card = CardManager.from_name('Shock')
        self.assertIsInstance(card, Card)

    def test_from_name_invalid(self):
        card = CardManager.from_name('ucbubfsvudgiru  bvubvfyfj ')
        self.assertIsNone(card)

    def test_reset_redirects(self):
        CardManager.reset_redirects()
        for name in CardManager.REDIRECT.keys():
            self.assertEqual(CardManager.REDIRECT[name], name)

    def test_redirects(self):
        proper_name = 'Virus Beetle'
        misspell_name = 'Vires Beetle'
        gibberish = 'ucbubfsvudgiru  bvubvfyfj '
        # Clear any data in CardManager
        CardManager.flush_cache()

        # This redirect should not exist yet.
        card, found = CardManager._find_card(proper_name)
        self.assertIsNone(card)
        self.assertFalse(found)

        # Get the card
        org_card = CardManager.from_name(proper_name)

        # The redirect should now exist.
        card, found = CardManager._find_card(proper_name)
        self.assertIsInstance(card, Card)
        self.assertTrue(found)

        # The redirect should not exist yet.
        card, found = CardManager._find_card(misspell_name)
        self.assertIsNone(card)
        self.assertFalse(found)

        # Tests "from_name"'s use of a previous copy of a card on a misspelled card name.
        miss_card = CardManager.from_name(misspell_name)
        self.assertEqual(org_card, miss_card)  # Tests if the objects are the same instance

        # The redirect should now exist.
        card, found = CardManager._find_card(misspell_name)
        self.assertIsInstance(card, Card)
        self.assertTrue(found)

        # This tests the short-circuit to not re-call a cached card.
        CardManager.from_name(proper_name)

        # Tests redirection of unresolvable card names
        CardManager.from_name(gibberish)
        card, found = CardManager._find_card(gibberish)
        self.assertIsNone(card)
        self.assertTrue(found)


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

    def test_sort_compare(self):
        meta = SetMetadata.get_metadata('NEO')

        tup_1 = (WUBRG.COLOR_COMBINATIONS[0], meta.CARD_LIST[0].NAME)
        tup_2 = (WUBRG.COLOR_COMBINATIONS[-1], meta.CARD_LIST[-1].NAME)
        tup_3 = (WUBRG.COLOR_COMBINATIONS[0], meta.CARD_LIST[2].NAME)

        self.assertEqual(meta._frame_compare(tup_1, tup_2), -1)
        self.assertEqual(meta._frame_compare(tup_2, tup_1), 1)
        self.assertEqual(meta._frame_compare(tup_1, tup_3), -1)
        self.assertEqual(meta._frame_compare(tup_3, tup_1), 1)
        self.assertEqual(meta._frame_compare(tup_3, tup_2), -1)
        self.assertEqual(meta._frame_compare(tup_2, tup_3), 1)


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
        card_1 = form.find_card('Boseiju Reaches Skyward')
        card_2 = form.find_card('Boseiju Reaches Skyward // Branch of Boseiju')
        self.assertIsInstance(card_1, Card)
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
