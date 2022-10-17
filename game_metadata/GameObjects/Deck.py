import pandas as pd

from game_metadata.GameObjects import Card


class Deck:

    DECK_ID: str

    def __init__(self, result):

        # Compile a deck dataframe
        deck_accum = []
        for group in result['groups']:
            for card in group['cards']:
                deck_accum.append({
                    'group': group['name'],
                    'name': Card.from_name(card['name']).NAME
                })
        deck = pd.DataFrame(deck_accum)

        # Compile deck metadata
        event_info = result['event_info']
        deck_metadata = {
            'expansion': event_info['expansion'],
            'event_type': event_info['format'],
            'wins': event_info['wins'],
            'losses': event_info['losses'],
            'pool_link': event_info['pool_link'],
            'deck_links': event_info['deck_links'],
            'details_link': event_info['details_link'],
            'draft_link': event_info['draft_link'],
            'sealed_deck_tech_link': result['builder_link']
        }


class DeckManager:

    def __init__(self):
        pass


