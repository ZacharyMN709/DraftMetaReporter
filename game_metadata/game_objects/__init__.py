"""
This package helps simplify dealing with constructs related to game objects and concepts, like drafts, decks and cards.
"""

from game_metadata.game_objects.Card import *
from game_metadata.game_objects.Deck import *
from game_metadata.game_objects.Draft import *

# Explicitly masking the name of the file.
from game_metadata.game_objects.Card import Card as Card
from game_metadata.game_objects.Deck import Deck as Deck
from game_metadata.game_objects.Draft import Draft as Draft

from_card = ['CardFace', 'Card', 'CardManager']

from_deck = ['TrophyStub', 'Deck', 'LimitedDeck', 'ConstructedDeck', 'DeckManager']

from_draft = ['Pick', 'Draft', 'DraftManager']


__all__ = from_card + from_deck + from_draft
