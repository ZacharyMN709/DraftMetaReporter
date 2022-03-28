from CallScryfall import CallScryfall
from CARD import Card

class CardManager():
    SCRYFALL = CallScryfall()
    REDIRECT = dict()
    SETS = dict()
    CARDS = dict()
    
    
    def _add_card(card):
        CardManager.CARDS[card.NAME] = card
        CardManager.REDIRECT[card.NAME] = card.NAME
        CardManager.REDIRECT[card.FULL_NAME] = card.NAME 
    
    def from_name(name):
        if set_code not in CardManager.CARDS:
            json = CardManager.SCRYFALL.get_card_by_name(name)
            card = Card(json)
            CardManager._add_card(card)
        
        return CardManager.CARDS[name]

    def from_set(set_code):
        if set_code not in CardManager.SETS:
            CardManager.SETS[set_code] = dict()
            for json in CardManager.SCRYFALL.get_set_cards(set_code):
                card = Card(json)
                CardManager._add_card(card)
                CardManager.SETS[set_code][card.NAME] = card 
                
        return CardManager.SETS[set_code] 
    
    def find_card(card_name):
        if card_name in CardManager.REDIRECT:
            card_name = CardManager.REDIRECT[card_name]
            return CARDS[card_name]
        else:
            return None
