import os.path

from core.game_metadata.game_objects.Deck import Deck


def parse_deck_name(file_path):
    file_name = os.path.splitext(os.path.split(file_path)[1])[0]
    deck_name = file_name.replace('_', ' ').title()
    return deck_name


def remove_negative_cards(card_dict):
    to_remove = [k for k, v in card_dict.items() if v <= 0]
    for key in to_remove:
        del card_dict[key]


def compare_decks(path_1, path_2):
    deck_1 = Deck.from_file(path_1, parse_deck_name(path_1))
    deck_2 = Deck.from_file(path_2, parse_deck_name(path_2))

    shared_cards = (deck_1 & deck_2)[0]
    deck_1_only = (deck_1 - deck_2)[0]
    deck_2_only = (deck_2 - deck_1)[0]
    remove_negative_cards(deck_1_only)
    remove_negative_cards(deck_2_only)

    return shared_cards, deck_1_only, deck_2_only


if __name__ == "__main__":
    deck_1_path = r"C:\Users\Zachary\Downloads\ghen,_arcanum weaver - budget.txt"
    deck_2_path = r"C:\Users\Zachary\Downloads\ghen,_arcanum weaver - high-power.txt"
    shared, deck_1, deck_2 = compare_decks(deck_1_path, deck_2_path)

    for card_list in [shared, deck_1, deck_2]:
        for k, v in card_list.items():
            print(f"{v} {k.NAME}")
        print()
