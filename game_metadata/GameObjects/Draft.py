from __future__ import annotations

from game_metadata.GameObjects import Card, Deck


class Pick:

    def __init__(self, pick):
        pick_dict = {
            'pack_number': pick['pack_number'],
            'pick_number': pick['pick_number'],
            'colors': pick['colors'],
            'pick': Card.from_name(pick['pick']['name']),
            'available': [Card.from_name(a['name']) for a in pick['available']],
            'known_missing': [Card.from_name(m['name']) for m in pick['known_missing']],
            'pool': [Card.from_name(p['name']) for p in pick['pool']],
        }
        pass


class Draft:

    @classmethod
    def from_id(cls, draft_id: str) -> Draft:
        result = None  # Get `result` with `draft_id`
        return Draft(result)

    def __init__(self, result):
        # TODO: Get the id used for the draft, so it can be linked to the deck.
        self.DRAFT_ID: str = None
        self.SET: str = None
        self.FORMAT: str = None

        self.PICKS: list[Pick] = list()


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
        return Deck.from_id(self.DRAFT_ID)


class DraftManager:

    def __init__(self):
        pass
