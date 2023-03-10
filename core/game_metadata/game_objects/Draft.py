"""
Used to represent Drafts, which are parsed from 17Lands data.

Condenses information from a user's draft into a Draft object, with Pick objects
helping to show the state of the pack and current cards taken.
"""

from __future__ import annotations
from typing import Optional

from core.utilities import logging
from core.data_requesting import Request17Lands

from core.game_metadata.game_objects.Card import Card
import core.game_metadata.game_objects.Deck as Deck


class Pick:
    @classmethod
    def from_json_list(cls, pick_list: list[dict]) -> list[Pick]:
        picks = [Pick(pick_data) for pick_data in pick_list]

        pick_cnt = len(picks)
        for i in range(0, pick_cnt):
            last_pick = None
            if i != 0:
                last_pick = picks[i-1]
            next_pick = None
            if i != pick_cnt-1:
                next_pick = picks[i+1]
            current_pick = picks[i]
            current_pick.last_pick = last_pick
            current_pick.next_pick = next_pick

        return picks

    def __init__(self, pick: dict, next_pick: Pick = None, last_pick: Pick = None):
        self.pack_number = pick['pack_number']
        self.pick_number = pick['pick_number']
        self.card_picked = Card.from_name(pick['pick']['name'])
        self.cards_available = [Card.from_name(a['name']) for a in pick['available']]
        self.cards_missing = [Card.from_name(m['name']) for m in pick['known_missing']]
        self.pool = [Card.from_name(p['name']) for p in pick['pool']]

        self.next_pick: Optional[Pick] = next_pick
        self.last_pick: Optional[Pick] = last_pick

    def __str__(self):
        return f"P{self.pack_number+1}P{self.pick_number+1}: {self.card_picked}"

    def __repr__(self):
        return self.__str__()


class Draft:
    @classmethod
    def from_id(cls, draft_id: str) -> Draft:
        return DraftManager.from_draft_id(draft_id)

    def __init__(self, result: dict, draft_id: str):
        self.DRAFT_ID: str = draft_id
        self.SET: str = result['expansion']
        self._FORMAT: str = ''
        self.picks: list[Pick] = Pick.from_json_list(result['picks'])
        self.pack_size: int = len(self.picks[0].cards_available)
        self._deck: Optional[Deck.LimitedDeck] = None

    def get_pick(self, pack: int = 1, pick: int = 1) -> Pick:
        i = ((pack - 1) * self.pack_size) + (pick - 1)
        return self.picks[i]

    @property
    def deck(self):
        if self._deck is None:
            self._deck = Deck.LimitedDeck.from_id(self.DRAFT_ID)
            self._FORMAT = self._deck.FORMAT
        return self._deck

    @property
    def FORMAT(self):
        if self._FORMAT == '':
            self._FORMAT = self.deck.FORMAT
        return self._FORMAT

    def __str__(self):
        return f"Draft {self.SET}-{self.FORMAT}: {self.DRAFT_ID}"

    def __repr__(self):
        return self.__str__()


class DraftManager:
    # Used to maintain a constant-time lookup cache of previously requested drafts.
    SETS: dict[str, dict[str, Draft]] = dict()
    DRAFTS: dict[str, Optional[Draft]] = dict()
    REQUESTER = Request17Lands()

    @classmethod
    def _add_draft(cls, draft: Draft, force_update=True) -> None:
        """
        An internal method to help more easily track drafts as they're found/fetched.
        :param draft: The draft object to track
        """
        # If the deck object isn't tracked in DECKS, add it to DECKS and SETS.
        if draft.DRAFT_ID not in cls.DRAFTS or force_update:

            # If the set the deck is from doesn't exist in the dictionary, initialize an empty dictionary.
            if draft.SET not in cls.SETS:
                cls.SETS[draft.SET] = dict()
            cls.DRAFTS[draft.DRAFT_ID] = draft
            cls.SETS[draft.SET][draft.DRAFT_ID] = draft

    @classmethod
    def from_draft_id(cls, draft_id: str) -> Optional[Draft]:
        # If the deck already exists, return it.
        prev_draft, found = cls._find_draft(draft_id)
        if found:
            return prev_draft

        # Otherwise, try and get it from 17Lands.
        try:
            data = cls.REQUESTER.get_draft(draft_id)
            draft = Draft(data, draft_id)
            cls._add_draft(draft)
            return draft
        except:
            # TODO: Better handle errors here.
            logging.info(f"Could not get draft with draft_id: '{draft_id}'")
            cls.DRAFTS[draft_id] = None
            return None

    @classmethod
    def _find_draft(cls, draft_id: str) -> tuple[Optional[Draft], bool]:
        if draft_id in cls.DRAFTS:
            return cls.DRAFTS[draft_id], True
        else:
            return None, False

    @classmethod
    def clear_blank_drafts(cls) -> None:
        """ Clears cls.DRAFTS of pairs where the value is None. """
        to_del = list()
        for deck_id in cls.DRAFTS:
            if cls.DRAFTS[deck_id] is None:
                to_del.append(deck_id)

        for deck_id in to_del:
            del cls.DRAFTS[deck_id]

    @classmethod
    def flush_cache(cls) -> None:
        """ Clears the caches of drafts. """
        del cls.SETS
        del cls.DRAFTS

        cls.SETS = dict()
        cls.DRAFTS = dict()
