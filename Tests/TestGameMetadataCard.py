import unittest

from game_metadata.utils.consts import CardLayouts
from game_metadata.RequestScryfall import RequestScryfall, trap_error
from game_metadata.GameObjects.Card import Card, CardManager


class TestCard(unittest.TestCase):
    @staticmethod
    def gen_card(card_name):
        json = RequestScryfall.get_card_by_name(card_name)
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
        # noinspection SpellCheckingInspection
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
        self.assertEqual(card.CAST_IDENTITY, 'G')

    def test_card_dual_name(self):
        name = 'Boseiju Reaches Skyward'
        full_name = 'Boseiju Reaches Skyward // Branch of Boseiju'
        card = self.gen_card(name)
        self.assertEqual(card.LAYOUT, CardLayouts.TRANSFORM)
        self.assertEqual(str(card), full_name)
        self.assertEqual(repr(card), full_name)
        self.assertEqual(card.NAME, name)
        self.assertEqual(card.MANA_COST, '{3}{G}')
        self.assertEqual(card.CAST_IDENTITY, 'G')

    def test_card_full_name(self):
        name = 'Invert // Invent'
        card = self.gen_card(name)
        self.assertEqual(card.LAYOUT, CardLayouts.SPLIT)
        self.assertEqual(str(card), name)
        self.assertEqual(repr(card), name)
        self.assertEqual(card.NAME, name)
        self.assertEqual(card.MANA_COST, '{U/R} // {4}{U}{R}')
        self.assertEqual(card.CAST_IDENTITY, 'UR')

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

    def test_relay_call(self):
        card_1 = CardManager.from_name('Shock')
        card_2 = Card.from_name('Shock')
        self.assertIsInstance(card_1, Card)
        self.assertIsInstance(card_2, Card)
        self.assertEqual(card_1, card_2)

    def test_from_name_invalid(self):
        # noinspection SpellCheckingInspection
        card = CardManager.from_name('ucbubfsvudgiru  bvubvfyfj ')
        self.assertIsNone(card)

    def test_reset_redirects(self):
        CardManager.reset_redirects()
        for name in CardManager.REDIRECT.keys():
            self.assertEqual(CardManager.REDIRECT[name], name)

    def test_redirects(self):
        proper_name = 'Virus Beetle'
        misspell_name = 'Vires Beetle'
        # noinspection SpellCheckingInspection
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
