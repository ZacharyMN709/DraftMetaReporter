import pandas as pd

from game_metadata.GameObjects import Card


class Draft:

    DRAFT_ID: str

    def __init__(self, result):
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
        picks = pd.DataFrame(picks_accum)


class DraftManager:

    def __init__(self):
        pass
