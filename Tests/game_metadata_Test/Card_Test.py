import unittest
from typing import Union

from core.data_requesting import RequestScryfall
from core.game_metadata import CardLayouts, Card, CardFace, CardManager
from core.game_metadata.utils.consts import CARD_SIDE

from Tests.settings import TEST_MASS_DATA_PULL
from Tests.settings import _tries, _success_delay, _fail_delay
from core.utilities import load_json_file


def _eval_card_face(self, eval_dict: [str, Union[set, str]], face: CardFace):
    """
    Handles the evaluation of a card face, based on the dictionary handed in.
    If the dictionary does not have an expected key, the class' default will be used,
    except for SCRYFALL_ID, as that may change as sets release. If not provided that
    test will be skipped.
    """

    eval_dict['__STR__'] = eval_dict['NAME']
    eval_dict['__REPR__'] = f"{eval_dict['NAME']} {eval_dict['MANA_COST']}: {eval_dict['TYPE_LINE']}"

    if "SCRYFALL_ID" in eval_dict:
        self.assertEqual(face.SCRYFALL_ID, eval_dict.get("SCRYFALL_ID"))

    self.assertEqual(eval_dict.get("ORACLE_ID"), face.ORACLE_ID, msg="Error in ORACLE_ID")
    self.assertEqual(eval_dict.get("LAYOUT"), face.LAYOUT, msg="Error in LAYOUT")
    self.assertEqual(eval_dict.get("CARD_SIDE"), face.CARD_SIDE, msg="Error in CARD_SIDE")
    self.assertEqual(eval_dict.get("IMG_SIDE"), face.IMG_SIDE, msg="Error in IMG_SIDE")

    self.assertEqual(eval_dict.get("NAME"), face.NAME, msg="Error in NAME")
    self.assertEqual(eval_dict.get("MANA_COST", ""), face.MANA_COST, msg="Error in MANA_COST")
    self.assertEqual(eval_dict.get("CMC"), face.CMC, msg="Error in CMC")
    self.assertEqual(eval_dict.get("COLORS", ""), face.COLORS, msg="Error in COLORS")
    self.assertEqual(eval_dict.get("COLOR_IDENTITY", ""), face.COLOR_IDENTITY, msg="Error in COLOR_IDENTITY")
    # TODO: Add in more colour information, based on activated costs, kickers or similar.

    self.assertEqual(eval_dict.get("TYPE_LINE", ""), face.TYPE_LINE, msg="Error in TYPE_LINE")
    self.assertSetEqual(eval_dict.get("ALL_TYPES", set()), face.ALL_TYPES, msg="Error in ALL_TYPES")
    self.assertSetEqual(eval_dict.get("SUPERTYPES", set()), face.SUPERTYPES, msg="Error in SUPERTYPES")
    self.assertSetEqual(eval_dict.get("TYPES", set()), face.TYPES, msg="Error in TYPES")
    self.assertSetEqual(eval_dict.get("SUBTYPES", set()), face.SUBTYPES, msg="Error in SUBTYPES")

    self.assertEqual(eval_dict.get("ORACLE"), face.ORACLE, msg="Error in ORACLE")
    # TODO: Re-enable KEYWORDS at a later date
    # self.assertSetEqual(eval_dict.get("KEYWORDS", set()), face.KEYWORDS, msg="Error in KEYWORDS")
    self.assertSetEqual(eval_dict.get("MANA_PRODUCED", set()), face.MANA_PRODUCED, msg="Error in MANA_PRODUCED")
    self.assertEqual(eval_dict.get("FLAVOR_TEXT"), face.FLAVOR_TEXT, msg="Error in FLAVOR_TEXT")

    self.assertEqual(eval_dict.get("POW"), face.POW, msg="Error in POW")
    self.assertEqual(eval_dict.get("TOU"), face.TOU, msg="Error in TOU")
    self.assertEqual(eval_dict.get("LOYALTY"), face.LOYALTY, msg="Error in LOYALTY")
    self.assertEqual(eval_dict.get("DEFENSE"), face.DEFENSE, msg="Error in DEFENSE")

    self.assertEqual(eval_dict.get("__STR__"), face.__str__(), msg="Error in __str__")
    self.assertEqual(eval_dict.get("__REPR__"), face.__repr__(), msg="Error in __repr__")


def _eval_card(self, eval_dict: [str, Union[set, str]], card: Card):
    """
    Handles the evaluation of a card face, based on the dictionary handed in.
    If the dictionary does not have an expected key, the class' default will be used,
    except for SCRYFALL_ID, as that may change as sets release. If not provided that
    test will be skipped.
    """

    eval_dict['__STR__'] = eval_dict['FULL_NAME']
    eval_dict['__REPR__'] = f"{eval_dict['FULL_NAME']} {eval_dict['MANA_COST']}: {eval_dict['TYPE_LINE']}"

    if "SCRYFALL_ID" in eval_dict:
        self.assertEqual(card.SCRYFALL_ID, eval_dict.get("SCRYFALL_ID"))

    self.assertEqual(eval_dict.get("ORACLE_ID"), card.ORACLE_ID, msg="Error in ORACLE_ID")
    self.assertEqual(eval_dict.get("LAYOUT"), card.LAYOUT, msg="Error in LAYOUT")
    self.assertEqual(eval_dict.get("CARD_SIDE"), card.CARD_SIDE, msg="Error in CARD_SIDE")
    self.assertEqual(eval_dict.get("IMG_SIDE"), card.IMG_SIDE, msg="Error in IMG_SIDE")

    self.assertEqual(eval_dict.get("NAME"), card.NAME, msg="Error in NAME")
    self.assertEqual(eval_dict.get("FULL_NAME"), card.FULL_NAME, msg="Error in FULL_NAME")
    self.assertEqual(eval_dict.get("MANA_COST", ""), card.MANA_COST, msg="Error in MANA_COST")
    self.assertEqual(eval_dict.get("CMC"), card.CMC, msg="Error in CMC")
    self.assertEqual(eval_dict.get("COLORS", ""), card.COLORS, msg="Error in COLORS")
    self.assertEqual(eval_dict.get("COLOR_IDENTITY", ""), card.COLOR_IDENTITY, msg="Error in COLOR_IDENTITY")
    # TODO: Add in more colour information, based on activated costs, kickers or similar.

    self.assertEqual(eval_dict.get("TYPE_LINE", ""), card.TYPE_LINE, msg="Error in TYPE_LINE")
    self.assertSetEqual(eval_dict.get("ALL_TYPES", set()), card.ALL_TYPES, msg="Error in ALL_TYPES")
    self.assertSetEqual(eval_dict.get("SUPERTYPES", set()), card.SUPERTYPES, msg="Error in SUPERTYPES")
    self.assertSetEqual(eval_dict.get("TYPES", set()), card.TYPES, msg="Error in TYPES")
    self.assertSetEqual(eval_dict.get("SUBTYPES", set()), card.SUBTYPES, msg="Error in SUBTYPES")

    self.assertEqual(eval_dict.get("ORACLE"), card.ORACLE, msg="Error in ORACLE")
    # TODO: Re-enable KEYWORDS at a later date
    # self.assertSetEqual(eval_dict.get("KEYWORDS", set()), face.KEYWORDS, msg="Error in KEYWORDS")
    self.assertSetEqual(eval_dict.get("MANA_PRODUCED", set()), card.MANA_PRODUCED, msg="Error in MANA_PRODUCED")

    self.assertEqual(eval_dict.get("POW"), card.POW, msg="Error in POW")
    self.assertEqual(eval_dict.get("TOU"), card.TOU, msg="Error in TOU")

    self.assertEqual(eval_dict.get("__STR__"), card.__str__(), msg="Error in __str__")
    self.assertEqual(eval_dict.get("__REPR__"), card.__repr__(), msg="Error in __repr__")


class TestCardFace(unittest.TestCase):
    REQUESTER = RequestScryfall(tries=2, fail_delay=15, success_delay=1)

    def get_card_face(self, card_name: str, layout: CardLayouts, face: CARD_SIDE):
        json = self.REQUESTER.get_card_by_name(card_name)
        return CardFace(json, layout, face)

    def eval_card_face(self, eval_dict: [str, Union[set, str]], face: CardFace):
        _eval_card_face(self, eval_dict, face)

    # region Basic Face Tests
    """ These tests cover the main faces use, in their simplest forms. """
    def test_card_face_normal(self):
        # https://api.scryfall.com/cards/e66120a5-95a3-4d15-873c-cfba221a2299?format=json&pretty=true
        name = 'Jukai Preserver'
        layout: CardLayouts = CardLayouts.NORMAL
        side: CARD_SIDE = 'default'
        face = self.get_card_face(name, layout, side)
        eval_dict = {
            "SCRYFALL_ID": "e66120a5-95a3-4d15-873c-cfba221a2299",
            "ORACLE_ID": "a8ce90be-f0ab-4f8d-896a-cde8aaf24579",
            "LAYOUT": layout,
            "CARD_SIDE": side,
            "IMG_SIDE": "front",
            "NAME": "Jukai Preserver",
            "MANA_COST": "{3}{G}",
            "CMC": 4,
            "COLORS": "G",
            "COLOR_IDENTITY": "G",
            "TYPE_LINE": "Enchantment Creature — Human Druid",
            "ALL_TYPES": {"Enchantment", "Creature", "Human", "Druid"},
            "TYPES": {"Enchantment", "Creature"},
            "SUBTYPES": {"Human", "Druid"},
            "ORACLE": "When Jukai Preserver enters the battlefield, "
                      "put a +1/+1 counter on target creature you control."
                      "\nChannel — {2}{G}, Discard Jukai Preserver: "
                      "Put a +1/+1 counter on each of up to two target creatures you control.",
            "KEYWORDS": {"Channel"},
            "FLAVOR_TEXT": "\"The kami grant you this boon, not I.\"",
            "POW": "3",
            "TOU": "3"
        }
        self.eval_card_face(eval_dict, face)

    def test_card_face_saga(self):
        # https://api.scryfall.com/cards/3a613a01-6145-4e34-987c-c9bdcb068370?format=json&pretty=true
        name = 'Fall of the Thran'
        layout: CardLayouts = CardLayouts.SAGA
        side: CARD_SIDE = 'default'
        face = self.get_card_face(name, layout, side)
        eval_dict = {
            "ORACLE_ID": "341803d9-fd29-4721-81bf-ae9b7f1c01d2",
            "LAYOUT": layout,
            "CARD_SIDE": side,
            "IMG_SIDE": "front",
            "NAME": "Fall of the Thran",
            "MANA_COST": "{5}{W}",
            "CMC": 6,
            "COLORS": "W",
            "COLOR_IDENTITY": "W",
            "TYPE_LINE": "Enchantment — Saga",
            "ALL_TYPES": {"Enchantment", "Saga"},
            "TYPES": {"Enchantment"},
            "SUBTYPES": {"Saga"},
            "ORACLE": "(As this Saga enters and after your draw step, add a lore counter. Sacrifice after III.)"
                      "\nI — Destroy all lands."
                      "\nII, III — Each player returns two land cards from their graveyard to the battlefield.",
        }
        self.eval_card_face(eval_dict, face)

    def test_card_face_class(self):
        # https://api.scryfall.com/cards/37d6343a-c514-4ca6-a415-62d1a473ae20?format=json&pretty=true
        name = 'Bard Class'
        layout: CardLayouts = CardLayouts.CLASS
        side: CARD_SIDE = 'default'
        face = self.get_card_face(name, layout, side)
        eval_dict = {
            "ORACLE_ID": "5bbc3ad0-4865-43f0-8baf-e7f4af5db656",
            "LAYOUT": layout,
            "CARD_SIDE": side,
            "IMG_SIDE": "front",
            "NAME": "Bard Class",
            "MANA_COST": "{R}{G}",
            "CMC": 2,
            "COLORS": "RG",
            "COLOR_IDENTITY": "RG",
            "TYPE_LINE": "Enchantment — Class",
            "ALL_TYPES": {"Enchantment", "Class"},
            "TYPES": {"Enchantment"},
            "SUBTYPES": {"Class"},
            "ORACLE": "(Gain the next level as a sorcery to add its ability.)"
                      "\nLegendary creatures you control enter the "
                      "battlefield with an additional +1/+1 counter on them."
                      "\n{R}{G}: Level 2"
                      "\nLegendary spells you cast cost {R}{G} less to cast. "
                      "This effect reduces only the amount of colored mana you pay."
                      "\n{3}{R}{G}: Level 3"
                      "\nWhenever you cast a legendary spell, exile the top two cards of your library. "
                      "You may play them this turn.",
        }
        self.eval_card_face(eval_dict, face)

    def test_card_face_adventure_main(self):
        # https://api.scryfall.com/cards/09fd2d9c-1793-4beb-a3fb-7a869f660cd4?format=json&pretty=true
        name = 'Bonecrusher Giant'
        layout: CardLayouts = CardLayouts.ADVENTURE
        side: CARD_SIDE = 'main'
        face = self.get_card_face(name, layout, side)
        eval_dict = {
            "ORACLE_ID": "d6d72f5f-8f5d-4180-b514-f22ff5482902",
            "LAYOUT": layout,
            "CARD_SIDE": side,
            "IMG_SIDE": "front",
            "NAME": "Bonecrusher Giant",
            "MANA_COST": "{2}{R}",
            "CMC": 3,
            "COLORS": "R",
            "COLOR_IDENTITY": "R",
            "TYPE_LINE": "Creature — Giant",
            "ALL_TYPES": {"Creature", "Giant"},
            "TYPES": {"Creature"},
            "SUBTYPES": {"Giant"},
            "ORACLE": "Whenever Bonecrusher Giant becomes the target of a spell, "
                      "Bonecrusher Giant deals 2 damage to that spell's controller.",
            "FLAVOR_TEXT": "Not every tale ends in glory.",
            "POW": "4",
            "TOU": "3"
        }
        self.eval_card_face(eval_dict, face)

    def test_card_face_adventure_adventure(self):
        # https://api.scryfall.com/cards/09fd2d9c-1793-4beb-a3fb-7a869f660cd4?format=json&pretty=true
        name = 'Bonecrusher Giant'
        layout: CardLayouts = CardLayouts.ADVENTURE
        side: CARD_SIDE = 'adventure'
        face = self.get_card_face(name, layout, side)
        eval_dict = {
            "ORACLE_ID": "d6d72f5f-8f5d-4180-b514-f22ff5482902",
            "LAYOUT": layout,
            "CARD_SIDE": side,
            "IMG_SIDE": "front",
            "NAME": "Stomp",
            "MANA_COST": "{1}{R}",
            "CMC": 2,
            "COLORS": "R",
            "COLOR_IDENTITY": "R",
            "TYPE_LINE": "Instant — Adventure",
            "ALL_TYPES": {"Instant", "Adventure"},
            "TYPES": {"Instant"},
            "SUBTYPES": {"Adventure"},
            "ORACLE": "Damage can't be prevented this turn. Stomp deals 2 damage to any target.",
        }
        self.eval_card_face(eval_dict, face)

    def test_card_face_adventure_default(self):
        # https://api.scryfall.com/cards/09fd2d9c-1793-4beb-a3fb-7a869f660cd4?format=json&pretty=true
        name = 'Bonecrusher Giant'
        layout: CardLayouts = CardLayouts.ADVENTURE
        side: CARD_SIDE = 'default'
        face = self.get_card_face(name, layout, side)
        eval_dict = {
            "ORACLE_ID": "d6d72f5f-8f5d-4180-b514-f22ff5482902",
            "LAYOUT": layout,
            "CARD_SIDE": side,
            "IMG_SIDE": "front",
            "NAME": "Bonecrusher Giant // Stomp",
            "MANA_COST": "{2}{R} // {1}{R}",
            "CMC": 3,
            "COLORS": "R",
            "COLOR_IDENTITY": "R",
            "TYPE_LINE": "Creature — Giant // Instant — Adventure",
            "ALL_TYPES": {"Creature", "Instant", "Giant", "Adventure"},
            "TYPES": {"Creature", "Instant"},
            "SUBTYPES": {"Giant", "Adventure"},
            "FLAVOR_TEXT": "Not every tale ends in glory.",
            "POW": "4",
            "TOU": "3"
        }
        self.eval_card_face(eval_dict, face)

    def test_card_face_split_left(self):
        # https://api.scryfall.com/cards/054a4e4f-8baa-41cf-b24c-d068e8b9a070?format=json&pretty=true
        name = 'Invert // Invent'
        layout: CardLayouts = CardLayouts.SPLIT
        side: CARD_SIDE = 'left'
        face = self.get_card_face(name, layout, side)
        eval_dict = {
            "ORACLE_ID": "9a378964-2c04-4d60-a905-c819d37ed4c3",
            "LAYOUT": layout,
            "CARD_SIDE": side,
            "IMG_SIDE": "front",
            "NAME": "Invert",
            "MANA_COST": "{U/R}",
            "CMC": 1,
            "COLORS": "UR",
            "COLOR_IDENTITY": "UR",
            "TYPE_LINE": "Instant",
            "ALL_TYPES": {"Instant"},
            "TYPES": {"Instant"},
            "ORACLE": "Switch the power and toughness of each of up to two target creatures until end of turn."
        }
        self.eval_card_face(eval_dict, face)

    def test_card_face_split_right(self):
        # https://api.scryfall.com/cards/054a4e4f-8baa-41cf-b24c-d068e8b9a070?format=json&pretty=true
        name = 'Invert // Invent'
        layout: CardLayouts = CardLayouts.SPLIT
        side: CARD_SIDE = 'right'
        face = self.get_card_face(name, layout, side)
        eval_dict = {
            "ORACLE_ID": "9a378964-2c04-4d60-a905-c819d37ed4c3",
            "LAYOUT": layout,
            "CARD_SIDE": side,
            "IMG_SIDE": "front",
            "NAME": "Invent",
            "MANA_COST": "{4}{U}{R}",
            "CMC": 6,
            "COLORS": "UR",
            "COLOR_IDENTITY": "UR",
            "TYPE_LINE": "Instant",
            "ALL_TYPES": {"Instant"},
            "TYPES": {"Instant"},
            "ORACLE": "Search your library for an instant card and/or a sorcery card, "
                      "reveal them, put them into your hand, then shuffle."
        }
        self.eval_card_face(eval_dict, face)

    def test_card_face_split_default(self):
        # https://api.scryfall.com/cards/054a4e4f-8baa-41cf-b24c-d068e8b9a070?format=json&pretty=true
        name = 'Invert // Invent'
        layout: CardLayouts = CardLayouts.SPLIT
        side: CARD_SIDE = 'default'
        face = self.get_card_face(name, layout, side)
        eval_dict = {
            "ORACLE_ID": "9a378964-2c04-4d60-a905-c819d37ed4c3",
            "LAYOUT": layout,
            "CARD_SIDE": side,
            "IMG_SIDE": "front",
            "NAME": "Invert // Invent",
            "MANA_COST": "{U/R} // {4}{U}{R}",
            "CMC": 7,
            "COLORS": "UR",
            "COLOR_IDENTITY": "UR",
            "TYPE_LINE": "Instant // Instant",
            "ALL_TYPES": {"Instant"},
            "TYPES": {"Instant"},
        }
        self.eval_card_face(eval_dict, face)

    def test_card_face_transform_front(self):
        # https://api.scryfall.com/cards/1144014b-f13b-4397-97ed-a8de46371a2c?format=json&pretty=true
        name = 'Boseiju Reaches Skyward'
        layout: CardLayouts = CardLayouts.TRANSFORM
        side: CARD_SIDE = 'front'
        face = self.get_card_face(name, layout, side)
        eval_dict = {
            "ORACLE_ID": "ec08aeb3-bba7-4982-9160-68d25bd411d6",
            "LAYOUT": layout,
            "CARD_SIDE": side,
            "IMG_SIDE": "front",
            "NAME": "Boseiju Reaches Skyward",
            "MANA_COST": "{3}{G}",
            "CMC": 4,
            "COLORS": "G",
            "COLOR_IDENTITY": "G",
            "TYPE_LINE": "Enchantment — Saga",
            "ALL_TYPES": {"Enchantment", "Saga"},
            "TYPES": {"Enchantment"},
            "SUBTYPES": {"Saga"},
            "ORACLE": "(As this Saga enters and after your draw step, add a lore counter.)\n"
                      "I — Search your library for up to two basic Forest cards, reveal them, "
                      "put them into your hand, then shuffle.\n"
                      "II — Put up to one target land card from your graveyard on top of your library.\n"
                      "III — Exile this Saga, then return it to the battlefield transformed under your control.",
            "KEYWORDS": {"Reach", "Transform"},
        }
        self.eval_card_face(eval_dict, face)

    def test_card_face_transform_back(self):
        # https://api.scryfall.com/cards/1144014b-f13b-4397-97ed-a8de46371a2c?format=json&pretty=true
        name = 'Boseiju Reaches Skyward'
        layout: CardLayouts = CardLayouts.TRANSFORM
        side: CARD_SIDE = 'back'
        face = self.get_card_face(name, layout, side)
        eval_dict = {
            "ORACLE_ID": "ec08aeb3-bba7-4982-9160-68d25bd411d6",
            "LAYOUT": layout,
            "CARD_SIDE": side,
            "IMG_SIDE": "back",
            "NAME": "Branch of Boseiju",
            "MANA_COST": '',
            "CMC": 4,
            "COLORS": "G",
            "COLOR_IDENTITY": "G",
            "TYPE_LINE": "Enchantment Creature — Plant",
            "ALL_TYPES": {"Enchantment", "Creature", "Plant"},
            "TYPES": {"Enchantment", "Creature"},
            "SUBTYPES": {"Plant"},
            "ORACLE": "Reach\nBranch of Boseiju gets +1/+1 for each land you control.",
            "FLAVOR_TEXT": "Though they razed the surrounding forest, the builders of Towashi left Boseiju unscathed, "
                           "shaping the city around the ancient tree.",
            "KEYWORDS": {"Reach", "Transform"},
            "POW": "0",
            "TOU": "0"
        }
        self.eval_card_face(eval_dict, face)

    def test_card_face_transform_default(self):
        # https://api.scryfall.com/cards/1144014b-f13b-4397-97ed-a8de46371a2c?format=json&pretty=true
        name = 'Boseiju Reaches Skyward'
        layout: CardLayouts = CardLayouts.TRANSFORM
        side: CARD_SIDE = 'default'
        face = self.get_card_face(name, layout, side)
        eval_dict = {
            "ORACLE_ID": "ec08aeb3-bba7-4982-9160-68d25bd411d6",
            "LAYOUT": layout,
            "CARD_SIDE": side,
            "IMG_SIDE": "front",
            "NAME": "Boseiju Reaches Skyward // Branch of Boseiju",
            "MANA_COST": "{3}{G}",
            "CMC": 4,
            "COLORS": "G",
            "COLOR_IDENTITY": "G",
            "TYPE_LINE": "Enchantment — Saga // Enchantment Creature — Plant",
            "ALL_TYPES": {"Enchantment", "Saga", "Creature", "Plant"},
            "TYPES": {"Enchantment", "Creature"},
            "SUBTYPES": {"Saga", "Plant"},
            "ORACLE": "(As this Saga enters and after your draw step, add a lore counter.)\n"
                      "I — Search your library for up to two basic Forest cards, reveal them, "
                      "put them into your hand, then shuffle.\n"
                      "II — Put up to one target land card from your graveyard on top of your library.\n"
                      "III — Exile this Saga, then return it to the battlefield transformed under your control.",
            "KEYWORDS": {"Reach", "Transform"},
        }
        self.eval_card_face(eval_dict, face)

    def test_card_face_modal_dfc_front(self):
        # https://api.scryfall.com/cards/bc7239ea-f8aa-4a6f-87bd-c35359635673?format=json&pretty=true
        name = 'Shatterskull Smashing'
        layout: CardLayouts = CardLayouts.MODAL_DFC
        side: CARD_SIDE = 'front'
        face = self.get_card_face(name, layout, side)
        eval_dict = {
            "ORACLE_ID": "78301998-fd9b-4cd5-afad-dbcb43cac2a7",
            "LAYOUT": layout,
            "CARD_SIDE": side,
            "IMG_SIDE": "front",
            "NAME": "Shatterskull Smashing",
            "MANA_COST": "{X}{R}{R}",
            "CMC": 2,
            "COLORS": "R",
            "COLOR_IDENTITY": "R",
            "TYPE_LINE": "Sorcery",
            "ALL_TYPES": {"Sorcery"},
            "TYPES": {"Sorcery"},
            "ORACLE": "Shatterskull Smashing deals X damage divided as you choose among up to two "
                      "target creatures and/or planeswalkers. If X is 6 or more, Shatterskull Smashing deals twice "
                      "X damage divided as you choose among them instead.",
        }
        self.eval_card_face(eval_dict, face)

    def test_card_face_modal_dfc_back(self):
        # https://api.scryfall.com/cards/bc7239ea-f8aa-4a6f-87bd-c35359635673?format=json&pretty=true
        name = 'Shatterskull Smashing'
        layout: CardLayouts = CardLayouts.MODAL_DFC
        side: CARD_SIDE = 'back'
        face = self.get_card_face(name, layout, side)
        eval_dict = {
            "ORACLE_ID": "78301998-fd9b-4cd5-afad-dbcb43cac2a7",
            "LAYOUT": layout,
            "CARD_SIDE": side,
            "IMG_SIDE": "back",
            "NAME": "Shatterskull, the Hammer Pass",
            "MANA_COST": "",
            "CMC": 0,
            "COLORS": "",
            "COLOR_IDENTITY": "R",
            "TYPE_LINE": "Land",
            "ALL_TYPES": {"Land"},
            "TYPES": {"Land"},
            "ORACLE": "As Shatterskull, the Hammer Pass enters the battlefield, you may pay 3 life. "
                      "If you don't, it enters the battlefield tapped.\n"
                      "{T}: Add {R}.",
            "MANA_PRODUCED": {"R"},
            "FLAVOR_TEXT": "\"The safest way across the Skyfangs is to fly. "
                           "Shatterskull Pass is a pretty distant second.\""
                           "\n—Samila, Murasa Expeditionary House",
        }
        self.eval_card_face(eval_dict, face)

    def test_card_face_modal_dfc_default(self):
        # https://api.scryfall.com/cards/bc7239ea-f8aa-4a6f-87bd-c35359635673?format=json&pretty=true
        name = 'Shatterskull Smashing'
        layout: CardLayouts = CardLayouts.MODAL_DFC
        side: CARD_SIDE = 'default'
        face = self.get_card_face(name, layout, side)
        eval_dict = {
            "ORACLE_ID": "78301998-fd9b-4cd5-afad-dbcb43cac2a7",
            "LAYOUT": layout,
            "CARD_SIDE": side,
            "IMG_SIDE": "front",
            "NAME": "Shatterskull Smashing // Shatterskull, the Hammer Pass",
            "MANA_COST": "{X}{R}{R}",
            "CMC": 2,
            "COLORS": "R",
            "COLOR_IDENTITY": "R",
            "TYPE_LINE": "Sorcery // Land",
            "ALL_TYPES": {"Sorcery", "Land"},
            "TYPES": {"Sorcery", "Land"},
            "ORACLE": "Shatterskull Smashing deals X damage divided as you choose among up to two "
                      "target creatures and/or planeswalkers. If X is 6 or more, Shatterskull Smashing deals twice "
                      "X damage divided as you choose among them instead.",
            "MANA_PRODUCED": {"R"}
        }
        self.eval_card_face(eval_dict, face)

    def test_card_face_flip_main(self):
        # https://api.scryfall.com/cards/864ad989-19a6-4930-8efc-bbc077a18c32?format=json&pretty=true
        name = 'Bushi Tenderfoot'
        layout: CardLayouts = CardLayouts.FLIP
        side: CARD_SIDE = 'main'
        face = self.get_card_face(name, layout, side)
        eval_dict = {
            "ORACLE_ID": "82959ca2-cd96-4cca-9ce0-afb8db209860",
            "LAYOUT": layout,
            "CARD_SIDE": side,
            "IMG_SIDE": "front",
            "NAME": "Bushi Tenderfoot",
            "MANA_COST": "{W}",
            "CMC": 1,
            "COLORS": "W",
            "COLOR_IDENTITY": "W",
            "TYPE_LINE": "Creature — Human Soldier",
            "ALL_TYPES": {"Creature", "Human", "Soldier"},
            "TYPES": {"Creature"},
            "SUBTYPES": {"Human", "Soldier"},
            "ORACLE": "When a creature dealt damage by Bushi Tenderfoot this turn dies, flip Bushi Tenderfoot.",
            "POW": "1",
            "TOU": "1"
        }
        self.eval_card_face(eval_dict, face)

    def test_card_face_flip_flipped(self):
        # https://api.scryfall.com/cards/864ad989-19a6-4930-8efc-bbc077a18c32?format=json&pretty=true
        name = 'Bushi Tenderfoot'
        layout: CardLayouts = CardLayouts.FLIP
        side: CARD_SIDE = 'flipped'
        face = self.get_card_face(name, layout, side)
        eval_dict = {
            "ORACLE_ID": "82959ca2-cd96-4cca-9ce0-afb8db209860",
            "LAYOUT": layout,
            "CARD_SIDE": side,
            "IMG_SIDE": "front",
            "NAME": "Kenzo the Hardhearted",
            "MANA_COST": "{W}",
            "CMC": 1,
            "COLORS": "W",
            "COLOR_IDENTITY": "W",
            "TYPE_LINE": "Legendary Creature — Human Samurai",
            "ALL_TYPES": {"Legendary", "Creature", "Human", "Samurai"},
            "SUPERTYPES": {"Legendary"},
            "TYPES": {"Creature"},
            "SUBTYPES": {"Human", "Samurai"},
            "ORACLE": "Double strike; bushido 2 "
                      "(Whenever this creature blocks or becomes blocked, it gets +2/+2 until end of turn.)",
            "KEYWORDS": {"Bushido", "Double strike"},
            "POW": "3",
            "TOU": "4"
        }
        self.eval_card_face(eval_dict, face)

    def test_card_face_flip_default(self):
        # https://api.scryfall.com/cards/864ad989-19a6-4930-8efc-bbc077a18c32?format=json&pretty=true
        name = 'Bushi Tenderfoot'
        layout: CardLayouts = CardLayouts.FLIP
        side: CARD_SIDE = 'default'
        face = self.get_card_face(name, layout, side)
        eval_dict = {
            "ORACLE_ID": "82959ca2-cd96-4cca-9ce0-afb8db209860",
            "LAYOUT": layout,
            "CARD_SIDE": side,
            "IMG_SIDE": "front",
            "NAME": "Bushi Tenderfoot // Kenzo the Hardhearted",
            "MANA_COST": "{W}",
            "CMC": 1,
            "COLORS": "W",
            "COLOR_IDENTITY": "W",
            "TYPE_LINE": "Creature — Human Soldier // Legendary Creature — Human Samurai",
            "ALL_TYPES": {"Creature", "Human", "Soldier", "Legendary", "Samurai"},
            "SUPERTYPES": {"Legendary"},
            "TYPES": {"Creature", },
            "SUBTYPES": {"Human", "Soldier", "Samurai"},
            "KEYWORDS": {"Bushido", "Double strike"},
            "POW": "1",
            "TOU": "1"
        }
        self.eval_card_face(eval_dict, face)

    def test_card_face_prototype_main(self):
        # https://api.scryfall.com/cards/62d37423-3445-412a-9abd-0480da404637?format=json&pretty=true
        name = 'Phyrexian Fleshgorger'
        layout: CardLayouts = CardLayouts.PROTOTYPE
        side: CARD_SIDE = 'default'
        face = self.get_card_face(name, layout, side)
        eval_dict = {
            "ORACLE_ID": "d3a5a830-cd14-49da-9412-c50049c74c92",
            "LAYOUT": layout,
            "CARD_SIDE": side,
            "IMG_SIDE": "front",
            "NAME": "Phyrexian Fleshgorger",
            "MANA_COST": "{7}",
            "CMC": 7,
            "COLORS": "",
            "COLOR_IDENTITY": "B",
            "TYPE_LINE": "Artifact Creature — Phyrexian Wurm",
            "ALL_TYPES": {"Artifact", "Creature", "Phyrexian", "Wurm"},
            "TYPES": {"Artifact", "Creature"},
            "SUBTYPES": {"Phyrexian", "Wurm"},
            "ORACLE": "Prototype {1}{B}{B} — 3/3 (You may cast this spell with "
                      "different mana cost, color, and size. It keeps its abilities and types.)\n"
                      "Menace, lifelink\n"
                      "Ward—Pay life equal to Phyrexian Fleshgorger's power.",
            "POW": "7",
            "TOU": "5"
        }
        self.eval_card_face(eval_dict, face)

    def test_card_face_prototype_prototype(self):
        # https://api.scryfall.com/cards/62d37423-3445-412a-9abd-0480da404637?format=json&pretty=true
        name = 'Phyrexian Fleshgorger'
        layout: CardLayouts = CardLayouts.PROTOTYPE
        side: CARD_SIDE = 'prototype'
        face = self.get_card_face(name, layout, side)
        eval_dict = {
            "ORACLE_ID": "d3a5a830-cd14-49da-9412-c50049c74c92",
            "LAYOUT": layout,
            "CARD_SIDE": side,
            "IMG_SIDE": "front",
            "NAME": "Phyrexian Fleshgorger",
            "MANA_COST": "{1}{B}{B}",                                      # NOTE: Prototype diff.
            "CMC": 3,                                                      # NOTE: Prototype diff.
            "COLORS": "B",                                                 # NOTE: Prototype diff.
            "COLOR_IDENTITY": "B",
            "TYPE_LINE": "Artifact Creature — Phyrexian Wurm",
            "ALL_TYPES": {"Artifact", "Creature", "Phyrexian", "Wurm"},
            "TYPES": {"Artifact", "Creature"},
            "SUBTYPES": {"Phyrexian", "Wurm"},
            "ORACLE": "Prototype {1}{B}{B} — 3/3 (You may cast this spell with "
                      "different mana cost, color, and size. It keeps its abilities and types.)\n"
                      "Menace, lifelink\n"
                      "Ward—Pay life equal to Phyrexian Fleshgorger's power.",
            "POW": "3",                                                   # NOTE: Prototype diff.
            "TOU": "3"                                                    # NOTE: Prototype diff.
        }
        self.eval_card_face(eval_dict, face)

    def test_card_face_prototype_default(self):
        # https://api.scryfall.com/cards/62d37423-3445-412a-9abd-0480da404637?format=json&pretty=true
        name = 'Phyrexian Fleshgorger'
        layout: CardLayouts = CardLayouts.PROTOTYPE
        side: CARD_SIDE = 'default'
        face = self.get_card_face(name, layout, side)
        eval_dict = {
            "ORACLE_ID": "d3a5a830-cd14-49da-9412-c50049c74c92",
            "LAYOUT": layout,
            "CARD_SIDE": side,
            "IMG_SIDE": "front",
            "NAME": "Phyrexian Fleshgorger",
            "MANA_COST": "{7}",
            "CMC": 7,
            "COLORS": "",
            "COLOR_IDENTITY": "B",
            "TYPE_LINE": "Artifact Creature — Phyrexian Wurm",
            "ALL_TYPES": {"Artifact", "Creature", "Phyrexian", "Wurm"},
            "TYPES": {"Artifact", "Creature"},
            "SUBTYPES": {"Phyrexian", "Wurm"},
            "ORACLE": "Prototype {1}{B}{B} — 3/3 (You may cast this spell with "
                      "different mana cost, color, and size. It keeps its abilities and types.)\n"
                      "Menace, lifelink\n"
                      "Ward—Pay life equal to Phyrexian Fleshgorger's power.",
            "POW": "7",
            "TOU": "5"
        }
        self.eval_card_face(eval_dict, face)

    def test_card_face_meld_front(self):
        # https://api.scryfall.com/cards/8aefe8bd-216a-4ec1-9362-3f9dbf7fd083?format=json&pretty=true
        # https://api.scryfall.com/cards/40a01679-3224-427e-bd1d-b797b0ab68b7?format=json&pretty=true
        name = 'Urza, Lord Protector'
        layout: CardLayouts = CardLayouts.MELD
        side: CARD_SIDE = 'front'
        face = self.get_card_face(name, layout, side)
        eval_dict = {
            "ORACLE_ID": "df2af646-3e5b-43a3-8f3e-50565889f456",
            "LAYOUT": layout,
            "CARD_SIDE": side,
            "IMG_SIDE": "front",
            "NAME": "Urza, Lord Protector",
            "MANA_COST": "{1}{W}{U}",
            "CMC": 3,
            "COLORS": "WU",
            "COLOR_IDENTITY": "WU",
            "TYPE_LINE": "Legendary Creature — Human Artificer",
            "ALL_TYPES": {"Legendary", "Creature", "Human", "Artificer"},
            "SUPERTYPES": {"Legendary"},
            "TYPES": {"Creature"},
            "SUBTYPES": {"Human", "Artificer"},
            "ORACLE": "Artifact, instant, and sorcery spells you cast cost {1} less to cast.\n"
                      "{7}: If you both own and control Urza, Lord Protector and an artifact named "
                      "The Mightstone and Weakstone, exile them, then meld them into Urza, Planeswalker. "
                      "Activate only as a sorcery.",
            "KEYWORDS": {"Meld"},
            "POW": "2",
            "TOU": "4"
        }
        self.eval_card_face(eval_dict, face)

    def test_card_face_meld_melded(self):
        # https://api.scryfall.com/cards/8aefe8bd-216a-4ec1-9362-3f9dbf7fd083?format=json&pretty=true
        # https://api.scryfall.com/cards/40a01679-3224-427e-bd1d-b797b0ab68b7?format=json&pretty=true
        card_name = 'Urza, Lord Protector'
        json = RequestScryfall().get_card_by_name(card_name)
        dicts = json["all_parts"]
        name = None
        for d in dicts:
            if d["component"] == "meld_result":
                name = d["name"]
        layout: CardLayouts = CardLayouts.MELD
        side: CARD_SIDE = 'melded'
        face = self.get_card_face(name, layout, side)
        eval_dict = {
            "ORACLE_ID": "759406d7-44ae-4260-9ef5-3bb2c92f751a",
            "LAYOUT": layout,
            "CARD_SIDE": side,
            "IMG_SIDE": "back",
            "NAME": "Urza, Planeswalker",
            "MANA_COST": "",
            "CMC": 8.0,
            "COLORS": "WU",
            "COLOR_IDENTITY": "WU",
            "TYPE_LINE": "Legendary Planeswalker — Urza",
            "ALL_TYPES": {"Legendary", "Planeswalker", "Urza"},
            "SUPERTYPES": {"Legendary"},
            "TYPES": {"Planeswalker"},
            "SUBTYPES": {"Urza"},
            "ORACLE":  "You may activate the loyalty abilities of Urza, Planeswalker "
                       "twice each turn rather than only once.\n"
                       "+2: Artifact, instant, and sorcery spells you cast this turn cost {2} less to cast. "
                       "You gain 2 life.\n"
                       "+1: Draw two cards, then discard a card.\n"
                       "0: Create two 1/1 colorless Soldier artifact creature tokens.\n"
                       "−3: Exile target nonland permanent.\n"
                       "−10: Artifacts and planeswalkers you control gain indestructible until end of turn. "
                       "Destroy all nonland permanents.",
        }
        self.eval_card_face(eval_dict, face)

    def test_card_face_meld_default(self):
        # https://api.scryfall.com/cards/8aefe8bd-216a-4ec1-9362-3f9dbf7fd083?format=json&pretty=true
        # https://api.scryfall.com/cards/40a01679-3224-427e-bd1d-b797b0ab68b7?format=json&pretty=true
        name = 'Urza, Lord Protector'
        layout: CardLayouts = CardLayouts.MELD
        side: CARD_SIDE = 'default'
        face = self.get_card_face(name, layout, side)
        eval_dict = {
            "ORACLE_ID": "df2af646-3e5b-43a3-8f3e-50565889f456",
            "LAYOUT": layout,
            "CARD_SIDE": side,
            "IMG_SIDE": "front",
            "NAME": "Urza, Lord Protector",
            "MANA_COST": "{1}{W}{U}",
            "CMC": 3,
            "COLORS": "WU",
            "COLOR_IDENTITY": "WU",
            "TYPE_LINE": "Legendary Creature — Human Artificer",
            "ALL_TYPES": {"Legendary", "Creature", "Human", "Artificer"},
            "SUPERTYPES": {"Legendary"},
            "TYPES": {"Creature"},
            "SUBTYPES": {"Human", "Artificer"},
            "ORACLE": "Artifact, instant, and sorcery spells you cast cost {1} less to cast.\n"
                      "{7}: If you both own and control Urza, Lord Protector and an artifact named "
                      "The Mightstone and Weakstone, exile them, then meld them into Urza, Planeswalker. "
                      "Activate only as a sorcery.",
            "KEYWORDS": {"Meld"},
            "POW": "2",
            "TOU": "4"
        }
        self.eval_card_face(eval_dict, face)

    def test_card_face_battle_front(self):
        # https://api.scryfall.com/cards/8fed056f-a8f5-41ec-a7d2-a80a238872d1?format=json&pretty=true
        name = 'Invasion of Zendikar'
        layout: CardLayouts = CardLayouts.BATTLE
        side: CARD_SIDE = 'front'
        face = self.get_card_face(name, layout, side)
        eval_dict = {
            "ORACLE_ID": "4b1874af-4ea5-4e22-a4d4-e718d75fe95e",
            "LAYOUT": layout,
            "CARD_SIDE": side,
            "IMG_SIDE": "front",
            "NAME": "Invasion of Zendikar",
            "MANA_COST": "{3}{G}",
            "CMC": 4,
            "COLORS": "G",
            "COLOR_IDENTITY": "G",
            "TYPE_LINE": "Battle — Siege",
            "ALL_TYPES": {"Battle", "Siege"},
            "TYPES": {"Battle"},
            "SUBTYPES": {"Siege"},
            "ORACLE": "(As a Siege enters, choose an opponent to protect it. You and others can attack it. "
                      "When it's defeated, exile it, then cast it transformed.)\n"
                      "When Invasion of Zendikar enters the battlefield, "
                      "search your library for up to two basic land cards, "
                      "put them onto the battlefield tapped, then shuffle.",
            "KEYWORDS": {"Vigilance", "Transform", "Haste"},
            "DEFENSE": "3",
        }
        self.eval_card_face(eval_dict, face)

    def test_card_face_battle_defeated(self):
        # https://api.scryfall.com/cards/8fed056f-a8f5-41ec-a7d2-a80a238872d1?format=json&pretty=true
        name = 'Invasion of Zendikar'
        layout: CardLayouts = CardLayouts.BATTLE
        side: CARD_SIDE = 'back'
        face = self.get_card_face(name, layout, side)
        eval_dict = {
            "ORACLE_ID": "4b1874af-4ea5-4e22-a4d4-e718d75fe95e",
            "LAYOUT": layout,
            "CARD_SIDE": side,
            "IMG_SIDE": "back",
            "NAME": "Awakened Skyclave",
            "MANA_COST": '',
            "CMC": 4,
            "COLORS": "G",
            "COLOR_IDENTITY": "G",
            "TYPE_LINE": "Creature — Elemental",
            "ALL_TYPES": {"Creature", "Elemental"},
            "TYPES": {"Creature"},
            "SUBTYPES": {"Elemental"},
            "ORACLE": "Vigilance, haste\n"
                      "As long as Awakened Skyclave is on the battlefield, "
                      "it's a land in addition to its other types.\n"
                      "{T}: Add one mana of any color.",
            "KEYWORDS": {"Vigilance", "Transform", "Haste"},
            # "MANA_PRODUCED": {"W", "U", "B", "G", "R"},
            "FLAVOR_TEXT": "Nahiri tried to bend Zendikar to Phyrexia's will. In response, the world rose against her.",
            "POW": "4",
            "TOU": "4"
        }
        self.eval_card_face(eval_dict, face)

    def test_card_face_battle_default(self):
        # https://api.scryfall.com/cards/8fed056f-a8f5-41ec-a7d2-a80a238872d1?format=json&pretty=true
        name = 'Invasion of Zendikar'
        layout: CardLayouts = CardLayouts.BATTLE
        side: CARD_SIDE = 'default'
        face = self.get_card_face(name, layout, side)
        eval_dict = {
            "ORACLE_ID": "4b1874af-4ea5-4e22-a4d4-e718d75fe95e",
            "LAYOUT": layout,
            "CARD_SIDE": side,
            "IMG_SIDE": "front",
            "NAME": "Invasion of Zendikar // Awakened Skyclave",
            "MANA_COST": "{3}{G}",
            "CMC": 4,
            "COLORS": "G",
            "COLOR_IDENTITY": "G",
            "TYPE_LINE": "Battle — Siege // Creature — Elemental",
            "ALL_TYPES": {"Battle", "Siege", "Creature", "Elemental"},
            "TYPES": {"Battle", "Creature"},
            "SUBTYPES": {"Siege", "Elemental"},
            "ORACLE": "(As a Siege enters, choose an opponent to protect it. You and others can attack it. "
                      "When it's defeated, exile it, then cast it transformed.)\n"
                      "When Invasion of Zendikar enters the battlefield, "
                      "search your library for up to two basic land cards, "
                      "put them onto the battlefield tapped, then shuffle.",
            "MANA_PRODUCED": {"W", "U", "B", "G", "R"},
            "KEYWORDS": {"Vigilance", "Transform", "Haste"},
            "DEFENSE": "3",
        }
        self.eval_card_face(eval_dict, face)
    # endregion Basic Face Tests

    # region Additional Face Tests
    def test_card_face_mana_dork(self):
        # https://api.scryfall.com/cards/88dee3d1-0496-40ea-b208-7362a932f531?format=json&pretty=true
        name = 'Deathbloom Gardener'
        layout: CardLayouts = CardLayouts.NORMAL
        side: CARD_SIDE = 'default'
        face = self.get_card_face(name, layout, side)
        eval_dict = {
            "ORACLE_ID": "0c7f9701-c39e-4f14-844a-15f2e3c41ca9",
            "LAYOUT": layout,
            "CARD_SIDE": side,
            "IMG_SIDE": "front",
            "NAME": "Deathbloom Gardener",
            "MANA_COST": "{2}{G}",
            "CMC": 3,
            "COLORS": "G",
            "COLOR_IDENTITY": "G",
            "TYPE_LINE": "Creature — Elf Druid",
            "ALL_TYPES": {"Creature", "Elf", "Druid"},
            "TYPES": {"Creature"},
            "SUBTYPES": {"Elf", "Druid"},
            "ORACLE": "Deathtouch\n{T}: Add one mana of any color.",
            "KEYWORDS": {"Deathtouch"},
            "MANA_PRODUCED": {"W", "U", "B", "G", "R"},
            "FLAVOR_TEXT": "\"I can provide the Coalition with poisons that will break down "
                           "Phyrexian machinery as easily as they stop the heart.\"",
            "POW": "1",
            "TOU": "1"
        }
        self.eval_card_face(eval_dict, face)

    def test_card_face_land(self):
        # https://api.scryfall.com/cards/bd250c9d-c65f-4293-a6b0-007fac634d3d?format=json&pretty=true
        name = 'Crystal Grotto'
        layout: CardLayouts = CardLayouts.NORMAL
        side: CARD_SIDE = 'default'
        face = self.get_card_face(name, layout, side)
        eval_dict = {
            "ORACLE_ID": "f15fb0cc-8e96-4f03-94d0-b51410415afd",
            "LAYOUT": layout,
            "CARD_SIDE": side,
            "IMG_SIDE": "front",
            "NAME": "Crystal Grotto",
            "MANA_COST": "",
            "CMC": 0,
            "COLORS": "",
            "COLOR_IDENTITY": "",
            "TYPE_LINE": "Land",
            "ALL_TYPES": {"Land"},
            "TYPES": {"Land"},
            "ORACLE": "When Crystal Grotto enters the battlefield, scry 1. "
                      "(Look at the top card of your library. You may put that card on the bottom of your library.)\n"
                      "{T}: Add {C}."
                      "\n{1}, {T}: Add one mana of any color.",
            "KEYWORDS": {"Scry"},
            "MANA_PRODUCED": {"B", "C", "G", "R", "U", "W"},
        }
        self.eval_card_face(eval_dict, face)

    def test_card_face_color_identity(self):
        # https://api.scryfall.com/cards/0dbac7ce-a6fa-466e-b6ba-173cf2dec98e?format=json&pretty=true
        name = 'Brutal Cathar // Moonrage Brute'
        layout: CardLayouts = CardLayouts.TRANSFORM
        side: CARD_SIDE = 'default'
        face = self.get_card_face(name, layout, side)
        eval_dict = {
            "ORACLE_ID": "1ed2d8e0-462b-468e-8fd3-1f3c6d99fb8a",
            "LAYOUT": layout,
            "CARD_SIDE": side,
            "IMG_SIDE": "front",
            "NAME": "Brutal Cathar // Moonrage Brute",
            "MANA_COST": "{2}{W}",
            "CMC": 3,
            "COLORS": "W",
            "COLOR_IDENTITY": "WR",
            "TYPE_LINE": "Creature — Human Soldier Werewolf // Creature — Werewolf",
            "ALL_TYPES": {"Creature", "Human", "Soldier", "Werewolf"},
            "TYPES": {"Creature"},
            "SUBTYPES": {"Human", "Soldier", "Werewolf"},
            "ORACLE": "When this creature enters the battlefield or transforms into Brutal Cathar, "
                      "exile target creature an opponent controls until this creature leaves the battlefield.\n"
                      "Daybound (If a player casts no spells during their own turn, it becomes night next turn.)",
            "KEYWORDS": {"Daybound", "First strike", "Ward", "Nightbound"},
            "POW": "2",
            "TOU": "2"
        }
        self.eval_card_face(eval_dict, face)

    def test_card_face_kicker(self):
        # https://api.scryfall.com/cards/2d00bab2-e95d-4296-a805-2a05e7640efb?format=json&pretty=true
        name = 'Archangel of Wrath'
        layout: CardLayouts = CardLayouts.NORMAL
        side: CARD_SIDE = 'default'
        face = self.get_card_face(name, layout, side)
        eval_dict = {
            "ORACLE_ID": "022e97af-2a3a-4e13-9b6b-d34fcc8cf168",
            "LAYOUT": layout,
            "CARD_SIDE": side,
            "IMG_SIDE": "front",
            "NAME": "Archangel of Wrath",
            "MANA_COST": "{2}{W}{W}",
            "CMC": 4,
            "COLORS": "W",
            "COLOR_IDENTITY": "WBR",
            "TYPE_LINE": "Creature — Angel",
            "ALL_TYPES": {"Creature", "Angel"},
            "TYPES": {"Creature"},
            "SUBTYPES": {"Angel"},
            "ORACLE": "Kicker {B} and/or {R} (You may pay an additional {B} and/or {R} as you cast this spell.)\n"
                      "Flying, lifelink\n"
                      "When Archangel of Wrath enters the battlefield, if it was kicked, "
                      "it deals 2 damage to any target.\n"
                      "When Archangel of Wrath enters the battlefield, if it was kicked twice, "
                      "it deals 2 damage to any target.",
            "KEYWORDS": {"Kicker", "Flying", "Lifelink"},
            "POW": "3",
            "TOU": "4"
        }
        self.eval_card_face(eval_dict, face)

    def test_card_face_activated_ability(self):
        # https://api.scryfall.com/cards/7b215968-93a6-4278-ac61-4e3e8c3c3943?format=json&pretty=true
        name = 'Nicol Bolas, the Ravager // Nicol Bolas, the Arisen'
        layout: CardLayouts = CardLayouts.TRANSFORM
        side: CARD_SIDE = 'default'
        face = self.get_card_face(name, layout, side)
        eval_dict = {
            "ORACLE_ID": "55e4b27e-5447-4fc2-8cae-a03e344600c6",
            "LAYOUT": layout,
            "CARD_SIDE": side,
            "IMG_SIDE": "front",
            "NAME": "Nicol Bolas, the Ravager // Nicol Bolas, the Arisen",
            "MANA_COST": "{1}{U}{B}{R}",
            "CMC": 4,
            "COLORS": "UBR",
            "COLOR_IDENTITY": "UBR",
            "TYPE_LINE": "Legendary Creature — Elder Dragon // Legendary Planeswalker — Bolas",
            "ALL_TYPES": {"Legendary",  "Creature", "Elder", "Dragon", "Planeswalker", "Bolas"},
            "SUPERTYPES": {"Legendary"},
            "TYPES": {"Creature", "Planeswalker"},
            "SUBTYPES": {"Elder", "Dragon", "Bolas"},
            "ORACLE": "Flying\n"
                      "When Nicol Bolas, the Ravager enters the battlefield, each opponent discards a card.\n"
                      "{4}{U}{B}{R}: Exile Nicol Bolas, the Ravager, then return him to the battlefield "
                      "transformed under his owner's control. Activate only as a sorcery.",
            "KEYWORDS": {"Flying", "Transform"},
            "POW": "4",
            "TOU": "4"
        }
        self.eval_card_face(eval_dict, face)

    def test_card_face_activated_ability_hybrid(self):
        # https://api.scryfall.com/cards/abf42833-43d0-4b05-b499-d13b2c577ee8?format=json&pretty=true
        name = 'Tatsunari, Toad Rider'
        layout: CardLayouts = CardLayouts.NORMAL
        side: CARD_SIDE = 'default'
        face = self.get_card_face(name, layout, side)
        eval_dict = {
            "ORACLE_ID": "e87be082-eafd-480e-b150-d27fd937e1b1",
            "LAYOUT": layout,
            "CARD_SIDE": side,
            "IMG_SIDE": "front",
            "NAME": "Tatsunari, Toad Rider",
            "MANA_COST": "{2}{B}",
            "CMC": 3,
            "COLORS": "B",
            "COLOR_IDENTITY": "UBG",
            "TYPE_LINE": "Legendary Creature — Human Ninja",
            "ALL_TYPES": {"Legendary", "Creature", "Human", "Ninja"},
            "SUPERTYPES": {"Legendary"},
            "TYPES": {"Creature"},
            "SUBTYPES": {"Human", "Ninja"},
            "ORACLE": "Whenever you cast an enchantment spell, if you don't control a creature named Keimi, "
                      "create Keimi, a legendary 3/3 black and green Frog creature token with "
                      "\"Whenever you cast an enchantment spell, each opponent loses 1 life and you gain 1 life.\"\n"
                      "{1}{G/U}: Tatsunari, Toad Rider and target Frog you control can't be blocked this turn "
                      "except by creatures with flying or reach.",
            "POW": "3",
            "TOU": "3"
        }
        self.eval_card_face(eval_dict, face)

    def test_card_face_planeswalker(self):
        # https://api.scryfall.com/cards/7641f4d9-4614-41c8-87f5-4845bd78e9b3?format=json&pretty=true
        name = 'Ajani, Sleeper Agent'
        layout: CardLayouts = CardLayouts.NORMAL
        side: CARD_SIDE = 'default'
        face = self.get_card_face(name, layout, side)
        eval_dict = {
            "ORACLE_ID": "37714eb9-a39d-4534-a2d3-27908c418f8a",
            "LAYOUT": layout,
            "CARD_SIDE": side,
            "IMG_SIDE": "front",
            "NAME": "Ajani, Sleeper Agent",
            "MANA_COST": "{1}{G}{G/W/P}{W}",
            "CMC": 4,
            "COLORS": "WG",
            "COLOR_IDENTITY": "WG",
            "TYPE_LINE": "Legendary Planeswalker — Ajani",
            "ALL_TYPES": {"Legendary", "Planeswalker", "Ajani"},
            "SUPERTYPES": {"Legendary"},
            "TYPES": {"Planeswalker"},
            "SUBTYPES": {"Ajani"},
            "ORACLE": "Compleated ({G/W/P} can be paid with {G}, {W}, or 2 life. "
                      "If life was paid, this planeswalker enters with two fewer loyalty counters.)\n"
                      "+1: Reveal the top card of your library. If it's a creature or planeswalker card, "
                      "put it into your hand. Otherwise, you may put it on the bottom of your library.\n"
                      "−3: Distribute three +1/+1 counters among up to three target creatures. "
                      "They gain vigilance until end of turn.\n"
                      "−6: You get an emblem with "
                      "\"Whenever you cast a creature or planeswalker spell, "
                      "target opponent gets two poison counters.\"",
            "LOYALTY": "4",
        }
        self.eval_card_face(eval_dict, face)

    def test_card_face_colorless(self):
        # https://api.scryfall.com/cards/3906b61a-3865-4dfd-ae06-a7d2a608851a?format=json&pretty=true
        name = 'Matter Reshaper'
        layout: CardLayouts = CardLayouts.NORMAL
        side: CARD_SIDE = 'default'
        face = self.get_card_face(name, layout, side)
        eval_dict = {
            "ORACLE_ID": "38538aff-b6f9-4c30-992e-7fd78da3c44a",
            "LAYOUT": layout,
            "CARD_SIDE": side,
            "IMG_SIDE": "front",
            "NAME": "Matter Reshaper",
            "MANA_COST": "{2}{C}",
            "CMC": 3,
            "COLORS": "",
            "COLOR_IDENTITY": "",
            "TYPE_LINE": "Creature — Eldrazi",
            "ALL_TYPES": {"Creature", "Eldrazi"},
            "TYPES": {"Creature"},
            "SUBTYPES": {"Eldrazi"},
            "ORACLE": "({C} represents colorless mana.)\n"
                      "When Matter Reshaper dies, reveal the top card of your library. You may put that card "
                      "onto the battlefield if it's a permanent card with mana value 3 or less. "
                      "Otherwise, put that card into your hand.",
            "POW": "3",
            "TOU": "2"
        }
        self.eval_card_face(eval_dict, face)

    def test_card_face_devoid(self):
        # https://api.scryfall.com/cards/f0bb1a5c-0f59-4951-827f-fe9df968232d?format=json&pretty=true
        name = 'Eldrazi Displacer'
        layout: CardLayouts = CardLayouts.NORMAL
        side: CARD_SIDE = 'default'
        face = self.get_card_face(name, layout, side)
        eval_dict = {
            "ORACLE_ID": "9b1f552a-bddc-4fcb-ac67-b4a65b2f48ba",
            "LAYOUT": layout,
            "CARD_SIDE": side,
            "IMG_SIDE": "front",
            "NAME": "Eldrazi Displacer",
            "MANA_COST": "{2}{W}",
            "CMC": 3,
            "COLORS": "",
            "COLOR_IDENTITY": "W",
            "TYPE_LINE": "Creature — Eldrazi",
            "ALL_TYPES": {"Creature", "Eldrazi"},
            "TYPES": {"Creature"},
            "SUBTYPES": {"Eldrazi"},
            "ORACLE": "Devoid (This card has no color.)\n"
                      "{2}{C}: Exile another target creature, then return it to the battlefield tapped "
                      "under its owner's control. ({C} represents colorless mana.)",
            "KEYWORDS": {"Devoid"},
            "POW": "3",
            "TOU": "3"
        }
        self.eval_card_face(eval_dict, face)

    def test_card_face_out_of_scope(self):
        # https://api.scryfall.com/cards/456149a1-0f15-466a-8d07-803efb5721d5?format=json&pretty=true
        name = 'Treacherous Trapezist'
        layout: CardLayouts = CardLayouts.NORMAL
        side: CARD_SIDE = 'default'
        face = self.get_card_face(name, layout, side)
        eval_dict = {
            "ORACLE_ID": "8db4b43d-aabd-45fd-a5f8-6f2a49eec7cf",
            "LAYOUT": layout,
            "CARD_SIDE": side,
            "IMG_SIDE": "front",
            "NAME": "Treacherous Trapezist",
            "MANA_COST": "{1}{U}{U}",
            "CMC": 3,
            "COLORS": "U",
            "COLOR_IDENTITY": "U",
            "TYPE_LINE": "Creature — Porcupine Performer",
            "ALL_TYPES": {"Creature", "Porcupine", "Performer"},
            "TYPES": {"Creature"},
            # "Porcupine" and "Performer" are not in scope. THey will trigger a warning and be filtered out.
            # "SUBTYPES": {"Porcupine", "Performer"},
            "SUBTYPES": set(),
            "ORACLE": "Flying\n"
                      "Whenever you cast an alliterative spell, scry 2. "
                      "(Anything with two or more capitalized words in its name that begin with the same "
                      "letter is alliterative.)\n"
                      "Other alliterative creatures you control have flying.",
            "KEYWORDS": {"Scry", "Flying"},
            "POW": "2",
            "TOU": "3"
        }
        self.eval_card_face(eval_dict, face)
    # endregion Additional Face Tests


class TestCard(unittest.TestCase):
    REQUESTER = RequestScryfall(tries=2, fail_delay=15)

    def gen_card(self, card_name):
        json = self.REQUESTER.get_card_by_name(card_name)
        return Card(json)

    def eval_card_face(self, eval_dict: [str, Union[set, str]], face: CardFace):
        _eval_card_face(self, eval_dict, face)

    def eval_card(self, eval_dict: [str, Union[set, str]], card: Card):
        _eval_card(self, eval_dict, card)

    # region Basic CardLayouts Tests
    def test_card_normal(self):
        name = 'Jukai Preserver'
        layout: CardLayouts = CardLayouts.NORMAL
        card = self.gen_card(name)
        self.assertEqual(layout, card.LAYOUT)
        self.assertEqual('default', card.DEFAULT_FACE.CARD_SIDE)
        self.assertEqual('default', card.FACE_1.CARD_SIDE)
        self.assertEqual(card.DEFAULT_FACE, card.FACE_1)
        self.assertEqual(card.ORACLE, card.FACE_1.ORACLE)

    def test_card_saga(self):
        name = 'Fall of the Thran'
        layout: CardLayouts = CardLayouts.SAGA
        card = self.gen_card(name)
        self.assertEqual(layout, card.LAYOUT)
        self.assertEqual('default', card.DEFAULT_FACE.CARD_SIDE)
        self.assertEqual('default', card.FACE_1.CARD_SIDE)
        self.assertEqual(card.DEFAULT_FACE, card.FACE_1)
        self.assertEqual(card.ORACLE, card.FACE_1.ORACLE)

    def test_card_class(self):
        name = 'Bard Class'
        layout: CardLayouts = CardLayouts.CLASS
        card = self.gen_card(name)
        self.assertEqual(layout, card.LAYOUT)
        self.assertEqual('default', card.DEFAULT_FACE.CARD_SIDE)
        self.assertEqual('default', card.FACE_1.CARD_SIDE)
        self.assertEqual(card.DEFAULT_FACE, card.FACE_1)
        self.assertEqual(card.ORACLE, card.FACE_1.ORACLE)

    def test_card_adventure(self):
        name = 'Bonecrusher Giant'
        layout: CardLayouts = CardLayouts.ADVENTURE
        card = self.gen_card(name)
        self.assertEqual(layout, card.LAYOUT)
        self.assertEqual('default', card.DEFAULT_FACE.CARD_SIDE)
        self.assertEqual('main', card.FACE_1.CARD_SIDE)
        self.assertEqual('adventure', card.FACE_2.CARD_SIDE)

        self.assertNotEqual(card.DEFAULT_FACE.NAME, card.FACE_1.NAME)
        self.assertNotEqual(card.FACE_1.NAME, card.FACE_2.NAME)
        self.assertNotEqual(card.FACE_2.NAME, card.DEFAULT_FACE.NAME)
        self.assertNotEqual(card.ORACLE, card.FACE_1.ORACLE)

    def test_card_split(self):
        name = 'Invert // Invent'
        layout: CardLayouts = CardLayouts.SPLIT
        card = self.gen_card(name)
        self.assertEqual(layout, card.LAYOUT)
        self.assertEqual('default', card.DEFAULT_FACE.CARD_SIDE)
        self.assertEqual('left', card.FACE_1.CARD_SIDE)
        self.assertEqual('right', card.FACE_2.CARD_SIDE)

        self.assertNotEqual(card.DEFAULT_FACE.NAME, card.FACE_1.NAME)
        self.assertNotEqual(card.FACE_1.NAME, card.FACE_2.NAME)
        self.assertNotEqual(card.FACE_2.NAME, card.DEFAULT_FACE.NAME)
        self.assertNotEqual(card.ORACLE, card.FACE_1.ORACLE)

    def test_card_transform(self):
        name = 'Boseiju Reaches Skyward'
        layout: CardLayouts = CardLayouts.TRANSFORM
        card = self.gen_card(name)
        self.assertEqual(layout, card.LAYOUT)
        self.assertEqual('default', card.DEFAULT_FACE.CARD_SIDE)
        self.assertEqual('front', card.FACE_1.CARD_SIDE)
        self.assertEqual('back', card.FACE_2.CARD_SIDE)

        self.assertNotEqual(card.DEFAULT_FACE.NAME, card.FACE_1.NAME)
        self.assertNotEqual(card.FACE_1.NAME, card.FACE_2.NAME)
        self.assertNotEqual(card.FACE_2.NAME, card.DEFAULT_FACE.NAME)
        self.assertNotEqual(card.ORACLE, card.FACE_1.ORACLE)

    def test_card_modal_dfc(self):
        name = 'Shatterskull Smashing'
        layout: CardLayouts = CardLayouts.MODAL_DFC
        card = self.gen_card(name)
        self.assertEqual(layout, card.LAYOUT)
        self.assertEqual('default', card.DEFAULT_FACE.CARD_SIDE)
        self.assertEqual('front', card.FACE_1.CARD_SIDE)
        self.assertEqual('back', card.FACE_2.CARD_SIDE)

        self.assertNotEqual(card.DEFAULT_FACE.NAME, card.FACE_1.NAME)
        self.assertNotEqual(card.FACE_1.NAME, card.FACE_2.NAME)
        self.assertNotEqual(card.FACE_2.NAME, card.DEFAULT_FACE.NAME)
        self.assertNotEqual(card.ORACLE, card.FACE_1.ORACLE)

    def test_card_flip(self):
        name = 'Bushi Tenderfoot'
        layout: CardLayouts = CardLayouts.FLIP
        card = self.gen_card(name)
        self.assertEqual(layout, card.LAYOUT)
        self.assertEqual('default', card.DEFAULT_FACE.CARD_SIDE)
        self.assertEqual('main', card.FACE_1.CARD_SIDE)
        self.assertEqual('flipped', card.FACE_2.CARD_SIDE)

        self.assertNotEqual(card.DEFAULT_FACE.NAME, card.FACE_1.NAME)
        self.assertNotEqual(card.FACE_1.NAME, card.FACE_2.NAME)
        self.assertNotEqual(card.FACE_2.NAME, card.DEFAULT_FACE.NAME)
        self.assertNotEqual(card.ORACLE, card.FACE_1.ORACLE)

    def test_card_prototype(self):
        name = 'Phyrexian Fleshgorger'
        layout: CardLayouts = CardLayouts.PROTOTYPE
        card = self.gen_card(name)
        self.assertEqual(layout, card.LAYOUT)
        self.assertEqual('default', card.DEFAULT_FACE.CARD_SIDE)
        self.assertEqual('default', card.FACE_1.CARD_SIDE)
        self.assertEqual('prototype', card.FACE_2.CARD_SIDE)
        self.assertEqual(card.ORACLE, card.FACE_1.ORACLE)

        self.assertEqual(card.DEFAULT_FACE, card.FACE_1)

    def test_card_meld(self):
        name = 'Urza, Lord Protector'
        layout: CardLayouts = CardLayouts.MELD
        card = self.gen_card(name)
        self.assertEqual(layout, card.LAYOUT)
        self.assertEqual('default', card.DEFAULT_FACE.CARD_SIDE)
        self.assertEqual('default', card.FACE_1.CARD_SIDE)
        self.assertEqual('melded', card.FACE_2.CARD_SIDE)

        self.assertEqual(card.DEFAULT_FACE, card.FACE_1)
        self.assertEqual(card.ORACLE, card.FACE_1.ORACLE)

        self.assertNotEqual(card.FACE_2.NAME, card.DEFAULT_FACE.NAME)
        self.assertNotEqual(card.FACE_2.NAME, card.FACE_1.NAME)

    def test_card_face_generation(self):
        name = 'Boseiju Reaches Skyward'
        layout: CardLayouts = CardLayouts.TRANSFORM
        card = self.gen_card(name)
        card_dict = {
            "SCRYFALL_ID": "1144014b-f13b-4397-97ed-a8de46371a2c",
            "ORACLE_ID": "ec08aeb3-bba7-4982-9160-68d25bd411d6",
            "LAYOUT": layout,
            "CARD_SIDE": 'default',
            "IMG_SIDE": "front",
            "NAME": "Boseiju Reaches Skyward",
            "FULL_NAME": "Boseiju Reaches Skyward // Branch of Boseiju",
            "MANA_COST": "{3}{G}",
            "CMC": 4,
            "COLORS": "G",
            "COLOR_IDENTITY": "G",
            "TYPE_LINE": "Enchantment — Saga // Enchantment Creature — Plant",
            "ALL_TYPES": {"Enchantment", "Saga", "Creature", "Plant"},
            "TYPES": {"Enchantment", "Creature"},
            "SUBTYPES": {"Saga", "Plant"},
            "ORACLE": "(As this Saga enters and after your draw step, add a lore counter.)\n"
                      "I — Search your library for up to two basic Forest cards, reveal them, "
                      "put them into your hand, then shuffle.\n"
                      "II — Put up to one target land card from your graveyard on top of your library.\n"
                      "III — Exile this Saga, then return it to the battlefield transformed under your control."
                      "\n\n  ---  \n\n"
                      "Reach\nBranch of Boseiju gets +1/+1 for each land you control.",
            "KEYWORDS": {"Reach", "Transform"},
        }
        default_dict = {
            "SCRYFALL_ID": "1144014b-f13b-4397-97ed-a8de46371a2c",
            "ORACLE_ID": "ec08aeb3-bba7-4982-9160-68d25bd411d6",
            "LAYOUT": layout,
            "CARD_SIDE": 'default',
            "IMG_SIDE": "front",
            "NAME": "Boseiju Reaches Skyward // Branch of Boseiju",
            "MANA_COST": "{3}{G}",
            "CMC": 4,
            "COLORS": "G",
            "COLOR_IDENTITY": "G",
            "TYPE_LINE": "Enchantment — Saga // Enchantment Creature — Plant",
            "ALL_TYPES": {"Enchantment", "Saga", "Creature", "Plant"},
            "TYPES": {"Enchantment", "Creature"},
            "SUBTYPES": {"Saga", "Plant"},
            "ORACLE": "(As this Saga enters and after your draw step, add a lore counter.)\n"
                      "I — Search your library for up to two basic Forest cards, reveal them, "
                      "put them into your hand, then shuffle.\n"
                      "II — Put up to one target land card from your graveyard on top of your library.\n"
                      "III — Exile this Saga, then return it to the battlefield transformed under your control.",
            "KEYWORDS": {"Reach", "Transform"},
        }
        front_dict = {
            "SCRYFALL_ID": "1144014b-f13b-4397-97ed-a8de46371a2c",
            "ORACLE_ID": "ec08aeb3-bba7-4982-9160-68d25bd411d6",
            "LAYOUT": layout,
            "CARD_SIDE": 'front',
            "IMG_SIDE": "front",
            "NAME": "Boseiju Reaches Skyward",
            "MANA_COST": "{3}{G}",
            "CMC": 4,
            "COLORS": "G",
            "COLOR_IDENTITY": "G",
            "TYPE_LINE": "Enchantment — Saga",
            "ALL_TYPES": {"Enchantment", "Saga"},
            "TYPES": {"Enchantment"},
            "SUBTYPES": {"Saga"},
            "ORACLE": "(As this Saga enters and after your draw step, add a lore counter.)\n"
                      "I — Search your library for up to two basic Forest cards, reveal them, "
                      "put them into your hand, then shuffle.\n"
                      "II — Put up to one target land card from your graveyard on top of your library.\n"
                      "III — Exile this Saga, then return it to the battlefield transformed under your control.",
            "KEYWORDS": {"Reach", "Transform"},
        }
        back_dict = {
            "SCRYFALL_ID": "1144014b-f13b-4397-97ed-a8de46371a2c",
            "ORACLE_ID": "ec08aeb3-bba7-4982-9160-68d25bd411d6",
            "LAYOUT": layout,
            "CARD_SIDE": 'back',
            "IMG_SIDE": "back",
            "NAME": "Branch of Boseiju",
            "MANA_COST": '',
            "CMC": 4,
            "COLORS": "G",
            "COLOR_IDENTITY": "G",
            "TYPE_LINE": "Enchantment Creature — Plant",
            "ALL_TYPES": {"Enchantment", "Creature", "Plant"},
            "TYPES": {"Enchantment", "Creature"},
            "SUBTYPES": {"Plant"},
            "ORACLE": "Reach\nBranch of Boseiju gets +1/+1 for each land you control.",
            "FLAVOR_TEXT": "Though they razed the surrounding forest, the builders of Towashi left Boseiju unscathed, "
                           "shaping the city around the ancient tree.",
            "KEYWORDS": {"Reach", "Transform"},
            "POW": "0",
            "TOU": "0"
        }

        self.assertEqual(layout, card.LAYOUT)
        self.eval_card(card_dict, card)
        self.eval_card_face(default_dict, card.DEFAULT_FACE)
        self.eval_card_face(front_dict, card.FACE_1)
        self.eval_card_face(back_dict, card.FACE_2)
    # endregion Basic CardLayouts Tests

    def test_card_error(self):
        # noinspection SpellCheckingInspection
        name = 'ujbn uiblubiihno;cinoef r'
        self.assertRaises(Exception, self.gen_card, name)

    def test_card_short_name(self):
        name = 'Jukai Preserver'
        card = self.gen_card(name)
        self.assertEqual(card.LAYOUT, CardLayouts.NORMAL)
        self.assertEqual(card.NAME, name)
        self.assertEqual(card.MANA_COST, '{3}{G}')
        self.assertEqual(card.CAST_IDENTITY, 'G')

    def test_card_dual_name(self):
        name = 'Boseiju Reaches Skyward'
        full_name = 'Boseiju Reaches Skyward // Branch of Boseiju'
        card = self.gen_card(name)
        self.assertEqual(card.LAYOUT, CardLayouts.TRANSFORM)
        self.assertEqual(card.NAME, name)
        self.assertEqual(card.MANA_COST, '{3}{G}')
        self.assertEqual(card.CAST_IDENTITY, 'G')

    def test_card_full_name(self):
        name = 'Invert // Invent'
        card = self.gen_card(name)
        self.assertEqual(card.LAYOUT, CardLayouts.SPLIT)
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

    def test_card_alchemy_changes(self):
        rebalanced = self.gen_card('A-Speakeasy Server')
        self.assertTrue(rebalanced.IS_DIGITAL)
        self.assertTrue(rebalanced.IS_REBALANCED)

        alchemy = self.gen_card('Herald of Vengeance')
        self.assertTrue(alchemy.IS_DIGITAL)
        self.assertFalse(alchemy.IS_REBALANCED)

        base = self.gen_card('Speakeasy Server')
        self.assertFalse(base.IS_DIGITAL)
        self.assertFalse(base.IS_REBALANCED)


class TestCardManager(unittest.TestCase):
    def setUp(self) -> None:
        CardManager.REQUESTER._TRIES = _tries
        CardManager.REQUESTER._SUCCESS_DELAY = _success_delay
        CardManager.REQUESTER._FAIL_DELAY = _fail_delay

    @unittest.skipUnless(TEST_MASS_DATA_PULL, "Not testing mass data functions. 'TEST_MASS_DATA_PULL' set to False.")
    def test_generate_cache_file(self):
        # Generate each cache, and the load each cache to ensure that no error is thrown, meaning the json is valid.
        CardManager.generate_cache_file()
        CardManager.generate_arena_cache_file(['YONE', 'KLD', 'AER'])

        load_json_file(r'C:\Users\Zachary\Coding\GitHub\ScryfallData', 'oracle-cards.json')
        load_json_file(r'C:\Users\Zachary\Coding\GitHub\ScryfallData', 'oracle-cards-arena.json')

    def test_from_file(self):
        CardManager.flush_cache()
        CardManager.load_cache_from_file()
        self.assertGreaterEqual(len(CardManager.CARDS), 5640)

    def test_from_set(self):
        cards = CardManager.from_set('NEO')
        self.assertIsInstance(cards, dict)
        self.assertEqual(len(cards), 289)

    def test_from_name(self):
        card = CardManager.from_name('Shock')
        self.assertIsInstance(card, Card)

    def test_relay_call(self):
        card_name = 'The Kami War'
        card_1 = CardManager.from_name(card_name)
        card_2 = Card.from_name(card_name)
        self.assertIsInstance(card_1, Card)
        self.assertIsInstance(card_2, Card)
        self.assertEqual(card_1, card_2)

        card_dict = Card.from_set('NEO')
        card_3 = card_dict[card_name]
        self.assertIsInstance(card_3, Card)
        self.assertEqual(card_3, card_2)

    def test_from_name_invalid(self):
        # noinspection SpellCheckingInspection
        card = CardManager.from_name('ucbubfsvudgiru  bvubvfyfj ')
        self.assertIsNone(card)

    def test_reset_redirects(self):
        CardManager.flush_cache()
        CardManager.from_set('NEO')
        CardManager.reset_redirects()

        self.assertEqual(317, len(CardManager.REDIRECT))
        for name in CardManager.REDIRECT.keys():
            self.assertTrue(name.startswith(CardManager.REDIRECT[name]))

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
