from CallScryfall import CallScryfall
from Card import Card
from utils.Logger import Logger


class CardManager:
    REDIRECT = dict()
    SETS = dict()
    CARDS = dict()

    @staticmethod
    def _add_card(card: Card, name: str):
        CardManager.CARDS[card.name] = card
        CardManager.REDIRECT[card.name] = card.name
        CardManager.REDIRECT[card.full_name] = card.name
        # Used to re-direct mis-spellings.
        CardManager.REDIRECT[name] = card.name

    @staticmethod
    def from_name(name: str):
        # If the card already exists, return it.
        prev_card = CardManager.find_card(name)
        if prev_card is not None:
            return prev_card
        # Otherwise, get the card info from scryfall.
        else:
            json = CallScryfall.get_card_by_name(name)
            # If there's an error, log it and return None.
            if 'err_msg' in json:
                Logger.LOGGER.log(f'Could not get card for {name}', Logger.FLG.DEFAULT)
                Logger.LOGGER.log(f'Error: {json["err_msg"]}', Logger.FLG.DEFAULT)
                return None
            # If the card is found, return it.
            else:
                card = Card(json)

                # See if a copy of the card already exists, likely
                # due to a misspelling. If so, use that instead.
                prev_card = CardManager.find_card(card.name)
                if prev_card is not None:
                    card = prev_card

                CardManager._add_card(card, name)
                return card

    @staticmethod
    def from_set(set_code):
        if set_code not in CardManager.SETS:
            CardManager.SETS[set_code] = dict()
            for json in CallScryfall.get_set_cards(set_code):
                card = Card(json)
                CardManager._add_card(card, card.name)
                CardManager.SETS[set_code][card.name] = card

        return CardManager.SETS[set_code]

    @staticmethod
    def find_card(card_name):
        if card_name in CardManager.REDIRECT:
            card_name = CardManager.REDIRECT[card_name]
            return CardManager.CARDS[card_name]
        else:
            return None
