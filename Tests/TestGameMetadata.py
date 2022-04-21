import unittest

from game_metadata import CallScryfall
from game_metadata.CallScryfall import trap_error

from game_metadata import Card
from game_metadata.utils.consts import CardLayouts

from game_metadata import CardManager


class TestCallScryfall(unittest.TestCase):
    def test_trap_error(self):
        def raise_test_error(v=True, void=None):
            if v:
                raise Exception("Test Error!")
            else:
                return list()

        val = trap_error(raise_test_error)(True, None)
        self.assertIsNone(val)
        trap_error(raise_test_error)(False, None)  # To enable full code coverage.

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

    def test_get_card_by_name_invalid(self):
        name = 'IOF(B*#R(&*(FC (HUCH( FEP( FU C JXCBJ CIBU FWUIPB F'
        card = CallScryfall.get_card_by_name(name)
        self.assertIsInstance(card, dict)
        self.assertEqual(card['err_msg'], f'Error: Cannot find card "{name}"')

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

    def test_card_flip(self):
        name = 'Bushi Tenderfoot'
        self.assertRaises(Exception, self.gen_card, name)

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
        self.assertFalse(CardManager.REDIRECT)

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
    def test_from_set(self):
        pass


class TestFormatMetadata(unittest.TestCase):
    def test_from_set(self):
        pass

