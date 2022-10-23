import unittest

from game_metadata.utils.consts import CardLayouts, CARD_SIDE
from game_metadata.RequestScryfall import RequestScryfall
from game_metadata.GameObjects.Card import Card, CardFace, CardManager

target_cards = {
    # Tests Mana Production
    'Deathbloom Gardener':
        "https://api.scryfall.com/cards/88dee3d1-0496-40ea-b208-7362a932f531?format=json&pretty=true",

    # Tests Color Identities
    'Brutal Cathar // Moonrage Brute':
        "https://api.scryfall.com/cards/0dbac7ce-a6fa-466e-b6ba-173cf2dec98e?format=json&pretty=true",

    # Tests Alternate Costs
    'Archangel of Wrath':
        "https://api.scryfall.com/cards/2d00bab2-e95d-4296-a805-2a05e7640efb?format=json&pretty=true",

    # Tests Activated Abilities Costs
    'Nicol Bolas, the Ravager // Nicol Bolas, the Arisen':
        "https://api.scryfall.com/cards/7b215968-93a6-4278-ac61-4e3e8c3c3943?format=json&pretty=true",

    # Tests Activated Abilities Costs
    'Tatsunari, Toad Rider':
        "https://api.scryfall.com/cards/abf42833-43d0-4b05-b499-d13b2c577ee8?format=json&pretty=true",

    # Tests Activated Abilities Costs
    'Eldrazi Displacer':
        "https://api.scryfall.com/cards/f0bb1a5c-0f59-4951-827f-fe9df968232d?format=json&pretty=true",

    # Tests Colorless Handling
    'Matter Reshaper':
        "https://api.scryfall.com/cards/3906b61a-3865-4dfd-ae06-a7d2a608851a?format=json&pretty=true",
}


class TestCardFace(unittest.TestCase):
    @staticmethod
    def get_card_face(card_name: str, face: CARD_SIDE):
        json = RequestScryfall.get_card_by_name(card_name)
        return CardFace.single_face(json, face)

    def test_card_face_normal(self):
        # https://api.scryfall.com/cards/e66120a5-95a3-4d15-873c-cfba221a2299?format=json&pretty=true
        name = 'Jukai Preserver'
        face = self.get_card_face(name, 'default')

    def test_card_face_saga(self):
        # https://api.scryfall.com/cards/3a613a01-6145-4e34-987c-c9bdcb068370?format=json&pretty=true
        name = 'Fall of the Thran'
        face = self.get_card_face(name, 'default')

    def test_card_face_class(self):
        # https://api.scryfall.com/cards/37d6343a-c514-4ca6-a415-62d1a473ae20?format=json&pretty=true
        name = 'Bard Class'
        face = self.get_card_face(name, 'default')

    def test_card_face_adventure_main(self):
        # https://api.scryfall.com/cards/09fd2d9c-1793-4beb-a3fb-7a869f660cd4?format=json&pretty=true
        name = 'Bonecrusher Giant'
        face = self.get_card_face(name, 'main')

    def test_card_face_adventure_adventure(self):
        # https://api.scryfall.com/cards/09fd2d9c-1793-4beb-a3fb-7a869f660cd4?format=json&pretty=true
        name = 'Bonecrusher Giant'
        face = self.get_card_face(name, 'adventure')

    def test_card_face_adventure_default(self):
        # https://api.scryfall.com/cards/09fd2d9c-1793-4beb-a3fb-7a869f660cd4?format=json&pretty=true
        name = 'Bonecrusher Giant'
        face = self.get_card_face(name, 'default')

    def test_card_face_split_left(self):
        # https://api.scryfall.com/cards/054a4e4f-8baa-41cf-b24c-d068e8b9a070?format=json&pretty=true
        name = 'Invert // Invent'
        face = self.get_card_face(name, 'left')

    def test_card_face_split_right(self):
        # https://api.scryfall.com/cards/054a4e4f-8baa-41cf-b24c-d068e8b9a070?format=json&pretty=true
        name = 'Invert // Invent'
        face = self.get_card_face(name, 'right')

    def test_card_face_split_default(self):
        # https://api.scryfall.com/cards/054a4e4f-8baa-41cf-b24c-d068e8b9a070?format=json&pretty=true
        name = 'Invert // Invent'
        face = self.get_card_face(name, 'default')

    def test_card_face_transform_front(self):
        # https://api.scryfall.com/cards/1144014b-f13b-4397-97ed-a8de46371a2c?format=json&pretty=true
        name = 'Boseiju Reaches Skyward'
        face = self.get_card_face(name, 'front')

    def test_card_face_transform_back(self):
        # https://api.scryfall.com/cards/1144014b-f13b-4397-97ed-a8de46371a2c?format=json&pretty=true
        name = 'Boseiju Reaches Skyward'
        face = self.get_card_face(name, 'back')

    def test_card_face_transform_default(self):
        # https://api.scryfall.com/cards/1144014b-f13b-4397-97ed-a8de46371a2c?format=json&pretty=true
        name = 'Boseiju Reaches Skyward'
        face = self.get_card_face(name, 'default')

    def test_card_face_modal_dfc_front(self):
        # https://api.scryfall.com/cards/bc7239ea-f8aa-4a6f-87bd-c35359635673?format=json&pretty=true
        name = 'Shatterskull Smashing'
        face = self.get_card_face(name, 'front')

    def test_card_face_modal_dfc_back(self):
        # https://api.scryfall.com/cards/bc7239ea-f8aa-4a6f-87bd-c35359635673?format=json&pretty=true
        name = 'Shatterskull Smashing'
        face = self.get_card_face(name, 'back')

    def test_card_face_modal_dfc_default(self):
        # https://api.scryfall.com/cards/bc7239ea-f8aa-4a6f-87bd-c35359635673?format=json&pretty=true
        name = 'Shatterskull Smashing'
        face = self.get_card_face(name, 'default')

    def test_card_face_flip_main(self):
        # TODO: Implement logic for flip cards.
        # https://api.scryfall.com/cards/864ad989-19a6-4930-8efc-bbc077a18c32?format=json&pretty=true
        name = 'Bushi Tenderfoot'
        face = self.get_card_face(name, 'main')

    def test_card_face_flip_flipped(self):
        # TODO: Implement logic for flip cards.
        # https://api.scryfall.com/cards/864ad989-19a6-4930-8efc-bbc077a18c32?format=json&pretty=true
        name = 'Bushi Tenderfoot'
        face = self.get_card_face(name, 'flipped')

    def test_card_face_flip_default(self):
        # TODO: Implement logic for flip cards.
        # https://api.scryfall.com/cards/864ad989-19a6-4930-8efc-bbc077a18c32?format=json&pretty=true
        name = 'Bushi Tenderfoot'
        face = self.get_card_face(name, 'default')


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

    def test_card_type_parsing(self):
        card = self.gen_card('Enthusiastic Mechanaut')

        self.assertRaises(ValueError, card.DEFAULT_FACE.handle_types, None)
        self.assertRaises(ValueError, card.DEFAULT_FACE.handle_types, 'Gobbledygook')
        self.assertRaises(ValueError, card.DEFAULT_FACE.handle_types, 'Creature — Gobbledygook')


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
