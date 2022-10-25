import unittest
from typing import Union
from Utilities.auto_logging import auto_log, LogLvl

from game_metadata.utils.consts import CardLayouts, CARD_SIDE
from game_metadata.RequestScryfall import RequestScryfall
from game_metadata.GameObjects.Card import Card, CardFace, CardManager

target_cards = {
    # Tests Mana Production
    'Deathbloom Gardener':
        "https://api.scryfall.com/cards/88dee3d1-0496-40ea-b208-7362a932f531?format=json&pretty=true",

    # Tests Mana Production
    'Crystal Grotto':
        "https://api.scryfall.com/cards/bd250c9d-c65f-4293-a6b0-007fac634d3d?format=json&pretty=true",

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
    def setUp(self) -> None:
        auto_log(LogLvl.DEBUG)
        # auto_log(LogLvl.WARNING)
        # auto_log(LogLvl.VERBOSE)
        pass

    @staticmethod
    def get_card_face(card_name: str, layout: CardLayouts, face: CARD_SIDE):
        json = RequestScryfall.get_card_by_name(card_name)
        return CardFace(json, layout, face)

    def eval_card_face(self, face: CardFace, eval_dict: [str, Union[set, str]]):
        """
        Handles the evaluation of a card face, based on the dictionary handed in.
        If the dictionary does not have an expected key, the class' default will be used,
        except for SCRYFALL_ID, as that may change as sets release. If not provided that
        test will be skipped.
        """

        if "SCRYFALL_ID" in eval_dict:
            self.assertEqual(face.SCRYFALL_ID, eval_dict.get("SCRYFALL_ID"))

        self.assertEqual(eval_dict.get("ORACLE_ID"), face.ORACLE_ID, msg="Error in ORACLE_ID")
        self.assertEqual(eval_dict.get("CARD_SIDE"), face.CARD_SIDE, msg="Error in CARD_SIDE")
        self.assertEqual(eval_dict.get("IMG_SIDE"), face.IMG_SIDE, msg="Error in IMG_SIDE")

        self.assertEqual(eval_dict.get("NAME"), face.NAME, msg="Error in NAME")
        self.assertEqual(eval_dict.get("MANA_COST", ""), face.MANA_COST, msg="Error in MANA_COST")
        self.assertEqual(eval_dict.get("CMC"), face.CMC, msg="Error in CMC")
        self.assertEqual(eval_dict.get("COLORS", ""), face.COLORS, msg="Error in COLORS")
        self.assertEqual(eval_dict.get("COLOR_IDENTITY", ""), face.COLOR_IDENTITY, msg="Error in COLOR_IDENTITY")

        self.assertEqual(eval_dict.get("TYPE_LINE", ""), face.TYPE_LINE, msg="Error in TYPE_LINE")
        self.assertSetEqual(eval_dict.get("ALL_TYPES", set()), face.ALL_TYPES, msg="Error in ALL_TYPES")
        self.assertSetEqual(eval_dict.get("SUPERTYPES", set()), face.SUPERTYPES, msg="Error in SUPERTYPES")
        self.assertSetEqual(eval_dict.get("TYPES", set()), face.TYPES, msg="Error in TYPES")
        self.assertSetEqual(eval_dict.get("SUBTYPES", set()), face.SUBTYPES, msg="Error in SUBTYPES")

        self.assertEqual(eval_dict.get("ORACLE"), face.ORACLE, msg="Error in ORACLE")
        # self.assertSetEqual(eval_dict.get("KEYWORDS", set()), face.KEYWORDS, msg="Error in KEYWORDS")
        self.assertSetEqual(eval_dict.get("MANA_PRODUCED", set()), face.MANA_PRODUCED, msg="Error in MANA_PRODUCED")
        self.assertEqual(eval_dict.get("FLAVOR_TEXT"), face.FLAVOR_TEXT, msg="Error in FLAVOR_TEXT")

        self.assertEqual(eval_dict.get("POW"), face.POW, msg="Error in POW")
        self.assertEqual(eval_dict.get("TOU"), face.TOU, msg="Error in TOU")

    # region Basic Face Tests
    """ These tests cover the main faces use, in their simplest forms. """
    def test_card_face_normal(self):
        # https://api.scryfall.com/cards/e66120a5-95a3-4d15-873c-cfba221a2299?format=json&pretty=true
        name = 'Jukai Preserver'
        face = self.get_card_face(name, CardLayouts.NORMAL, 'default')
        eval_dict = {
            "SCRYFALL_ID": "e66120a5-95a3-4d15-873c-cfba221a2299",
            "ORACLE_ID": "a8ce90be-f0ab-4f8d-896a-cde8aaf24579",
            "CARD_SIDE": "default",
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
        self.eval_card_face(face, eval_dict)

    def test_card_face_saga(self):
        # https://api.scryfall.com/cards/3a613a01-6145-4e34-987c-c9bdcb068370?format=json&pretty=true
        name = 'Fall of the Thran'
        face = self.get_card_face(name, CardLayouts.SAGA, 'default')
        eval_dict = {
            "ORACLE_ID": "341803d9-fd29-4721-81bf-ae9b7f1c01d2",
            "CARD_SIDE": "default",
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
        self.eval_card_face(face, eval_dict)

    def test_card_face_class(self):
        # https://api.scryfall.com/cards/37d6343a-c514-4ca6-a415-62d1a473ae20?format=json&pretty=true
        name = 'Bard Class'
        face = self.get_card_face(name, CardLayouts.CLASS, 'default')
        eval_dict = {
            "ORACLE_ID": "5bbc3ad0-4865-43f0-8baf-e7f4af5db656",
            "CARD_SIDE": "default",
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
        self.eval_card_face(face, eval_dict)

    def test_card_face_adventure_main(self):
        # https://api.scryfall.com/cards/09fd2d9c-1793-4beb-a3fb-7a869f660cd4?format=json&pretty=true
        name = 'Bonecrusher Giant'
        face = self.get_card_face(name, CardLayouts.ADVENTURE, 'main')
        eval_dict = {
            "ORACLE_ID": "d6d72f5f-8f5d-4180-b514-f22ff5482902",
            "CARD_SIDE": "main",
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
        self.eval_card_face(face, eval_dict)

    def test_card_face_adventure_adventure(self):
        # https://api.scryfall.com/cards/09fd2d9c-1793-4beb-a3fb-7a869f660cd4?format=json&pretty=true
        name = 'Bonecrusher Giant'
        face = self.get_card_face(name, CardLayouts.ADVENTURE, 'adventure')
        eval_dict = {
            "ORACLE_ID": "d6d72f5f-8f5d-4180-b514-f22ff5482902",
            "CARD_SIDE": "adventure",
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
        self.eval_card_face(face, eval_dict)

    def test_card_face_adventure_default(self):
        # https://api.scryfall.com/cards/09fd2d9c-1793-4beb-a3fb-7a869f660cd4?format=json&pretty=true
        name = 'Bonecrusher Giant'
        face = self.get_card_face(name, CardLayouts.ADVENTURE, 'default')
        eval_dict = {
            "ORACLE_ID": "d6d72f5f-8f5d-4180-b514-f22ff5482902",
            "CARD_SIDE": "default",
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
        self.eval_card_face(face, eval_dict)

    def test_card_face_split_left(self):
        # https://api.scryfall.com/cards/054a4e4f-8baa-41cf-b24c-d068e8b9a070?format=json&pretty=true
        name = 'Invert // Invent'
        face = self.get_card_face(name, CardLayouts.SPLIT, 'left')
        eval_dict = {
            "ORACLE_ID": "9a378964-2c04-4d60-a905-c819d37ed4c3",
            "CARD_SIDE": "left",
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
        self.eval_card_face(face, eval_dict)

    def test_card_face_split_right(self):
        # https://api.scryfall.com/cards/054a4e4f-8baa-41cf-b24c-d068e8b9a070?format=json&pretty=true
        name = 'Invert // Invent'
        face = self.get_card_face(name, CardLayouts.SPLIT, 'right')
        eval_dict = {
            "ORACLE_ID": "9a378964-2c04-4d60-a905-c819d37ed4c3",
            "CARD_SIDE": "right",
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
        self.eval_card_face(face, eval_dict)

    def test_card_face_split_default(self):
        # https://api.scryfall.com/cards/054a4e4f-8baa-41cf-b24c-d068e8b9a070?format=json&pretty=true
        name = 'Invert // Invent'
        face = self.get_card_face(name, CardLayouts.SPLIT, 'default')
        eval_dict = {
            "ORACLE_ID": "9a378964-2c04-4d60-a905-c819d37ed4c3",
            "CARD_SIDE": "default",
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
        self.eval_card_face(face, eval_dict)

    def test_card_face_transform_front(self):
        # https://api.scryfall.com/cards/1144014b-f13b-4397-97ed-a8de46371a2c?format=json&pretty=true
        name = 'Boseiju Reaches Skyward'
        face = self.get_card_face(name, CardLayouts.TRANSFORM, 'front')
        eval_dict = {
            "ORACLE_ID": "ec08aeb3-bba7-4982-9160-68d25bd411d6",
            "CARD_SIDE": "front",
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
        self.eval_card_face(face, eval_dict)

    def test_card_face_transform_back(self):
        # https://api.scryfall.com/cards/1144014b-f13b-4397-97ed-a8de46371a2c?format=json&pretty=true
        name = 'Boseiju Reaches Skyward'
        face = self.get_card_face(name, CardLayouts.TRANSFORM, 'back')
        eval_dict = {
            "ORACLE_ID": "ec08aeb3-bba7-4982-9160-68d25bd411d6",
            "CARD_SIDE": "back",
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
        self.eval_card_face(face, eval_dict)

    def test_card_face_transform_default(self):
        # https://api.scryfall.com/cards/1144014b-f13b-4397-97ed-a8de46371a2c?format=json&pretty=true
        name = 'Boseiju Reaches Skyward'
        face = self.get_card_face(name, CardLayouts.TRANSFORM, 'default')
        eval_dict = {
            "ORACLE_ID": "ec08aeb3-bba7-4982-9160-68d25bd411d6",
            "CARD_SIDE": "default",
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
        self.eval_card_face(face, eval_dict)

    def test_card_face_modal_dfc_front(self):
        # https://api.scryfall.com/cards/bc7239ea-f8aa-4a6f-87bd-c35359635673?format=json&pretty=true
        name = 'Shatterskull Smashing'
        face = self.get_card_face(name, CardLayouts.MODAL_DFC, 'front')
        eval_dict = {
            "ORACLE_ID": "78301998-fd9b-4cd5-afad-dbcb43cac2a7",
            "CARD_SIDE": "front",
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
        self.eval_card_face(face, eval_dict)

    def test_card_face_modal_dfc_back(self):
        # https://api.scryfall.com/cards/bc7239ea-f8aa-4a6f-87bd-c35359635673?format=json&pretty=true
        name = 'Shatterskull Smashing'
        face = self.get_card_face(name, CardLayouts.MODAL_DFC, 'back')
        eval_dict = {
            "ORACLE_ID": "78301998-fd9b-4cd5-afad-dbcb43cac2a7",
            "CARD_SIDE": "back",
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
        self.eval_card_face(face, eval_dict)

    def test_card_face_modal_dfc_default(self):
        # https://api.scryfall.com/cards/bc7239ea-f8aa-4a6f-87bd-c35359635673?format=json&pretty=true
        name = 'Shatterskull Smashing'
        face = self.get_card_face(name, CardLayouts.MODAL_DFC, 'default')
        eval_dict = {
            "ORACLE_ID": "78301998-fd9b-4cd5-afad-dbcb43cac2a7",
            "CARD_SIDE": "default",
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
        self.eval_card_face(face, eval_dict)
    # endregion Basic Face Tests

    # region Additional Face Tests
    def test_card_face_flip_main(self):
        # TODO: Implement logic for flip cards.
        # https://api.scryfall.com/cards/864ad989-19a6-4930-8efc-bbc077a18c32?format=json&pretty=true
        name = 'Bushi Tenderfoot'
        face = self.get_card_face(name, CardLayouts.FLIP, 'main')
        eval_dict = {
            "ORACLE_ID": "82959ca2-cd96-4cca-9ce0-afb8db209860",
            "CARD_SIDE": "main",
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
        self.eval_card_face(face, eval_dict)

    def test_card_face_flip_flipped(self):
        # TODO: Implement logic for flip cards.
        # https://api.scryfall.com/cards/864ad989-19a6-4930-8efc-bbc077a18c32?format=json&pretty=true
        name = 'Bushi Tenderfoot'
        face = self.get_card_face(name, CardLayouts.FLIP, 'flipped')
        eval_dict = {
            "ORACLE_ID": "82959ca2-cd96-4cca-9ce0-afb8db209860",
            "CARD_SIDE": "flipped",
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
        self.eval_card_face(face, eval_dict)

    def test_card_face_flip_default(self):
        # TODO: Implement logic for flip cards.
        # https://api.scryfall.com/cards/864ad989-19a6-4930-8efc-bbc077a18c32?format=json&pretty=true
        name = 'Bushi Tenderfoot'
        face = self.get_card_face(name, CardLayouts.FLIP, 'default')
        eval_dict = {
            "ORACLE_ID": "82959ca2-cd96-4cca-9ce0-afb8db209860",
            "CARD_SIDE": "default",
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
        self.eval_card_face(face, eval_dict)
    # region Additional Face Tests


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

        # self.assertRaises(ValueError, card.DEFAULT_FACE.handle_types, None)
        # self.assertRaises(ValueError, card.DEFAULT_FACE.handle_types, 'Gobbledygook')
        # self.assertRaises(ValueError, card.DEFAULT_FACE.handle_types, 'Creature — Gobbledygook')
        self.assertEqual(True, False)


class TestCardManager(unittest.TestCase):
    def test_from_set(self):
        cards = CardManager.from_set('NEO')
        self.assertIsInstance(cards, dict)
        self.assertEqual(len(cards), 282)

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
