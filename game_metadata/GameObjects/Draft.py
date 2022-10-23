from __future__ import annotations
from typing import Optional

from Utilities.auto_logging import logging
from game_metadata.Request17Lands import Request17Lands
from game_metadata.GameObjects.Card import Card, CardManager
from game_metadata.GameObjects.Deck import LimitedDeck


class Pack:

    def __init__(self, pick):
        pick_dict = {
            'pack_number': pick['pack_number'],
            'pick_number': pick['pick_number'],
            'colors': pick['colors'],
            'pick': CardManager.from_name(pick['pick']['name']),
            'available': [CardManager.from_name(a['name']) for a in pick['available']],
            'known_missing': [CardManager.from_name(m['name']) for m in pick['known_missing']],
            'pool': [CardManager.from_name(p['name']) for p in pick['pool']],
        }
        pass


class Draft:

    @classmethod
    def from_id(cls, draft_id: str) -> Draft:
        return DraftManager.from_draft_id(draft_id)

    def __init__(self, result):
        self.DRAFT_ID: str = ''
        self.SET: str = ''
        self.FORMAT: str = ''
        self._DECK: Optional[LimitedDeck] = None

        self.PICKS: list[Pack] = list()

        # Parse payload
        payload = result['payload']
        expansion = payload['expansion']

        # Parse picks
        picks_accum = []
        for pick in payload['picks']:
            picks_accum.append({
                'expansion': expansion,
                'pack_number': pick['pack_number'],
                'pick_number': pick['pick_number'],
                'colors': pick['colors'],
                'pick': Card.from_name(pick['pick']['name']),
                'available': [Card.from_name(a['name']) for a in pick['available']],
                'known_missing': [Card.from_name(m['name']) for m in pick['known_missing']],
                'pool': [Card.from_name(p['name']) for p in pick['pool']],
                'possible_maindeck': [
                    Card.from_name(m['name'])
                    for m in [
                        i for l in pick['possible_maindeck']
                        for i in l
                    ]
                ],
                'probable_sideboard': [
                    Card.from_name(s['name'])
                    for s in [
                        i for l in pick['probable_sideboard']
                        for i in l
                    ]
                ]
            })

    @property
    def DECK(self):
        if self._DECK is None:
            self._DECK = LimitedDeck.from_id(self.DRAFT_ID)
        return self._DECK


class DraftManager:
    # Used to maintain a constant-time lookup cache of previously requested cards.
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
            draft = cls.REQUESTER.get_draft(draft_id)
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
        for draft_id in cls.DRAFTS:
            if cls.DRAFTS[draft_id] is None:
                del cls.DRAFTS[draft_id]

    @classmethod
    def flush_cache(cls) -> None:
        """
        Clears the caches of drafts.
        """
        del cls.SETS
        del cls.DRAFTS

        cls.SETS = dict()
        cls.DRAFTS = dict()
